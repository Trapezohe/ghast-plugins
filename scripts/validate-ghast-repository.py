#!/usr/bin/env python3
"""Validate Ghast plugin sources, packages, and audit metadata."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree


PLUGIN_DIR = Path("plugins")
PACKAGE_DIR = Path("packages")
CATALOG_PATH = Path("plugin-catalog.json")
AUDIT_PATH = Path("third-party-plugin-audit.json")
REVIEWS_PATH = Path("third-party-plugin-reviews.json")

# This signed NVIDIA source file is byte-identical to the pinned official
# catalog. macOS ships Bash 3.2, whose parser rejects the quoted heredoc inside
# command substitution. The skill executes this helper inside its NVIDIA
# container. Any content change invalidates this narrow compatibility exception.
BASH_32_EXCEPTIONS = {
    (
        "plugins/nvidia/skills/vss-deploy-detection-tracking-2d/"
        "scripts/write_deployment_log.sh"
    ): "c62d8335d30708e7a6d5f23b8bc66f8e693bb1d71bb16ba2fa6239b92f87e765",
}

SECRET_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{32,}"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{30,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
)
TEXT_SUFFIXES = {
    ".cjs",
    ".css",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    manifests = validate_sources(errors)
    validate_catalog_and_packages(manifests, errors)
    validate_audit(errors)
    validate_python(errors)
    validate_node(errors, warnings)
    validate_shell(errors, warnings)
    validate_secrets(errors)

    for warning in warnings:
        print(f"warning: {warning}")
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1

    print(
        "validated "
        f"{len(manifests)} plugins, "
        f"{count_skills()} skills, "
        f"{len(list(PACKAGE_DIR.glob('*.zip')))} packages"
    )
    return 0


def validate_sources(errors: list[str]) -> dict[str, dict]:
    manifests: dict[str, dict] = {}
    for plugin_dir in sorted(path for path in PLUGIN_DIR.iterdir() if path.is_dir()):
        manifest_path = plugin_dir / ".ghast-plugin/plugin.json"
        if not manifest_path.is_file():
            continue
        manifest = load_json(manifest_path, errors)
        if manifest is None:
            continue
        name = manifest.get("name")
        if name != plugin_dir.name:
            errors.append(f"{manifest_path}: name must match directory")
            continue
        manifests[name] = manifest

        icon = manifest.get("icon")
        if not isinstance(icon, str) or not icon.startswith("./assets/"):
            errors.append(f"{manifest_path}: invalid icon path")
        else:
            icon_path = plugin_dir / icon.removeprefix("./")
            if not icon_path.is_file():
                errors.append(f"{manifest_path}: missing icon {icon}")
            elif icon_path.suffix.lower() == ".svg":
                try:
                    ElementTree.parse(icon_path)
                except ElementTree.ParseError as exc:
                    errors.append(f"{icon_path}: invalid SVG: {exc}")

        for field, relative in (
            ("skills", "skills"),
            ("commands", "commands"),
            ("mcpServers", ".mcp.json"),
        ):
            if field in manifest and not (plugin_dir / relative).exists():
                errors.append(f"{manifest_path}: {field} points to missing {relative}")

        mcp_path = plugin_dir / ".mcp.json"
        if mcp_path.is_file():
            load_json(mcp_path, errors)
        validate_skill_frontmatter(plugin_dir, errors)

    return manifests


def validate_skill_frontmatter(plugin_dir: Path, errors: list[str]) -> None:
    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        return
    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append(f"{skills_dir}: empty skills directory")
    for skill_dir in skill_dirs:
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue
        text = skill_path.read_text(errors="replace")
        if not text.startswith("---\n") or text.find("\n---\n", 4) < 0:
            errors.append(f"{skill_path}: missing YAML frontmatter")


def validate_catalog_and_packages(
    manifests: dict[str, dict], errors: list[str]
) -> None:
    catalog = load_json(CATALOG_PATH, errors)
    if catalog is None:
        return
    entries = catalog.get("plugins")
    if not isinstance(entries, list):
        errors.append(f"{CATALOG_PATH}: plugins must be a list")
        return

    catalog_names = {entry.get("id") for entry in entries}
    if catalog_names != set(manifests):
        errors.append(
            f"{CATALOG_PATH}: plugin IDs differ from source manifests"
        )

    for entry in entries:
        name = entry.get("id")
        if name not in manifests:
            continue
        package_path = PACKAGE_DIR / f"{name}.zip"
        if not package_path.is_file():
            errors.append(f"{package_path}: missing package")
            continue
        expected_hash = (entry.get("package") or {}).get("sha256")
        actual_hash = sha256(package_path)
        if expected_hash != actual_hash:
            errors.append(
                f"{package_path}: SHA-256 {actual_hash} != {expected_hash}"
            )
        try:
            with zipfile.ZipFile(package_path) as archive:
                bad_member = archive.testzip()
                if bad_member:
                    errors.append(f"{package_path}: bad CRC at {bad_member}")
                prefix = f"{name}/"
                names = set(archive.namelist())
                manifest_member = f"{prefix}.ghast-plugin/plugin.json"
                if manifest_member not in names:
                    errors.append(f"{package_path}: missing {manifest_member}")
                    continue
                packaged_manifest = json.loads(archive.read(manifest_member))
                if packaged_manifest != manifests[name]:
                    errors.append(f"{package_path}: manifest differs from source")
                icon_member = prefix + packaged_manifest["icon"].removeprefix("./")
                if icon_member not in names:
                    errors.append(f"{package_path}: missing packaged icon")
                if any(not member.startswith(prefix) for member in names):
                    errors.append(f"{package_path}: member outside {prefix}")
        except (OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
            errors.append(f"{package_path}: invalid package: {exc}")


def validate_audit(errors: list[str]) -> None:
    audit = load_json(AUDIT_PATH, errors)
    reviews = load_json(REVIEWS_PATH, errors)
    if audit is None or reviews is None:
        return
    rows = audit.get("plugins")
    if not isinstance(rows, list):
        errors.append(f"{AUDIT_PATH}: plugins must be a list")
        return
    status_counts = Counter(row["auditStatus"] for row in rows)
    implementation_counts = Counter(
        row["ghast"]["implementationStatus"] for row in rows
    )
    summary = audit.get("summary") or {}
    if dict(sorted(status_counts.items())) != summary.get("auditStatus"):
        errors.append(f"{AUDIT_PATH}: auditStatus summary is stale")
    if dict(sorted(implementation_counts.items())) != summary.get(
        "ghastImplementationStatus"
    ):
        errors.append(f"{AUDIT_PATH}: implementation summary is stale")
    verified = {
        row["id"]
        for row in rows
        if row["ghast"]["implementationStatus"] == "implemented-verified"
    }
    reviewed = set((reviews.get("plugins") or {}).keys())
    if verified != reviewed:
        errors.append(
            f"{AUDIT_PATH}: implemented-verified IDs differ from reviews"
        )


def validate_python(errors: list[str]) -> None:
    paths = list(PLUGIN_DIR.rglob("*.py")) + list(Path("scripts").glob("*.py"))
    for path in sorted(paths):
        try:
            ast.parse(path.read_text(errors="replace"), filename=str(path))
        except SyntaxError as exc:
            errors.append(f"{path}: Python syntax error: {exc}")


def validate_node(errors: list[str], warnings: list[str]) -> None:
    node = shutil.which("node")
    if node is None:
        warnings.append("node is unavailable; JavaScript syntax checks skipped")
        return
    for path in sorted(PLUGIN_DIR.rglob("*")):
        if (
            path.is_file()
            and "scripts" in path.parts
            and path.suffix in {".js", ".mjs", ".cjs"}
        ):
            result = subprocess.run(
                [node, "--check", str(path)],
                capture_output=True,
                text=True,
            )
            if result.returncode:
                errors.append(
                    f"{path}: Node syntax error: "
                    f"{(result.stderr or result.stdout).strip()}"
                )


def validate_shell(errors: list[str], warnings: list[str]) -> None:
    bash = shutil.which("bash")
    if bash is None:
        warnings.append("bash is unavailable; shell syntax checks skipped")
        return
    version = subprocess.run(
        [bash, "--version"], capture_output=True, text=True, check=False
    ).stdout
    bash_32 = "version 3.2" in version
    for path in sorted(
        list(PLUGIN_DIR.rglob("*.sh")) + list(Path("scripts").glob("*.sh"))
    ):
        result = subprocess.run(
            [bash, "-n", str(path)],
            capture_output=True,
            text=True,
        )
        if not result.returncode:
            continue
        expected_hash = BASH_32_EXCEPTIONS.get(str(path))
        if bash_32 and expected_hash and sha256(path) == expected_hash:
            warnings.append(
                f"{path}: official signed container script is not parseable "
                "by macOS Bash 3.2; exact audited hash retained"
            )
            continue
        errors.append(
            f"{path}: shell syntax error: "
            f"{(result.stderr or result.stdout).strip()}"
        )


def validate_secrets(errors: list[str]) -> None:
    for root in (PLUGIN_DIR, Path("scripts")):
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            text = path.read_text(errors="replace")
            for pattern in SECRET_PATTERNS:
                for match in pattern.finditer(text):
                    value = match.group(0).lower()
                    if any(marker in value for marker in ("your", "example", "placeholder")):
                        continue
                    errors.append(f"{path}: possible embedded secret {match.group(0)[:12]}...")


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{path}: JSON root must be an object")
        return None
    return data


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def count_skills() -> int:
    return sum(1 for _ in PLUGIN_DIR.glob("*/skills/*/SKILL.md"))


if __name__ == "__main__":
    raise SystemExit(main())
