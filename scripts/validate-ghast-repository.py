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
from urllib.parse import urlsplit
from xml.etree import ElementTree

try:
    from skills_ref import validate as validate_agent_skill
except ImportError:
    validate_agent_skill = None


PLUGIN_DIR = Path("plugins")
PACKAGE_DIR = Path("packages")
CATALOG_PATH = Path("plugin-catalog.json")
AUDIT_PATH = Path("third-party-plugin-audit.json")
REVIEWS_PATH = Path("third-party-plugin-reviews.json")
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
GHAST_NAMESPACE = "ai.trapezohe.ghast"
PLUGIN_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
PLUGIN_NAME = re.compile(
    r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$"
)

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

    if validate_agent_skill is None:
        errors.append(
            "skills-ref is unavailable; install requirements-agent-plugins.txt"
        )

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
        manifest_path = plugin_dir / "plugin.json"
        if not manifest_path.is_file():
            errors.append(f"{plugin_dir}: missing Agent Plugins plugin.json")
            continue
        manifest = load_json(manifest_path, errors)
        if manifest is None:
            continue
        name = manifest.get("name")
        if name != plugin_dir.name:
            errors.append(f"{manifest_path}: name must match directory")
            continue
        manifests[name] = manifest

        validate_agent_plugin_manifest(manifest_path, manifest, errors)
        for legacy_path in (plugin_dir / ".ghast-plugin", plugin_dir / ".mcp.json"):
            if legacy_path.exists():
                errors.append(f"{legacy_path}: legacy Ghast layout is not allowed")

        ghast = (manifest.get("extensions") or {}).get(GHAST_NAMESPACE, {})
        icon = ghast.get("icon")
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

        commands = ghast.get("commands")
        if commands is not None:
            expected = f"./{GHAST_NAMESPACE}/commands/"
            if commands != expected or not (plugin_dir / GHAST_NAMESPACE / "commands").is_dir():
                errors.append(f"{manifest_path}: invalid Ghast commands extension")

        mcp_path = plugin_dir / "mcp.json"
        if mcp_path.is_file():
            mcp = load_json(mcp_path, errors)
            if mcp is not None:
                validate_agent_plugin_mcp(mcp_path, mcp, errors)
        validate_skill_frontmatter(plugin_dir, errors)

    return manifests


def validate_agent_plugin_manifest(
    path: Path, manifest: dict, errors: list[str]
) -> None:
    unknown = set(manifest) - PLUGIN_FIELDS
    if unknown:
        errors.append(f"{path}: unknown Agent Plugins fields {sorted(unknown)}")
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        errors.append(f"{path}: must target Agent Plugins 1.0.0")
    name = manifest.get("name")
    if (
        not isinstance(name, str)
        or not 1 <= len(name) <= 64
        or PLUGIN_NAME.fullmatch(name) is None
    ):
        errors.append(f"{path}: invalid Agent Plugins name")
    for field in ("version", "description", "homepage", "repository", "license"):
        if field in manifest and not isinstance(manifest[field], str):
            errors.append(f"{path}: {field} must be a string")
    author = manifest.get("author")
    if author is not None:
        if not isinstance(author, dict):
            errors.append(f"{path}: author must be an object")
        elif set(author) - {"name", "email", "url"} or any(
            not isinstance(value, str) for value in author.values()
        ):
            errors.append(f"{path}: invalid author object")
    keywords = manifest.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list)
        or any(not isinstance(value, str) for value in keywords)
    ):
        errors.append(f"{path}: keywords must be an array of strings")
    extensions = manifest.get("extensions")
    if extensions is not None and (
        not isinstance(extensions, dict)
        or any(not isinstance(value, dict) for value in extensions.values())
    ):
        errors.append(f"{path}: extensions must map namespaces to objects")
    ghast = (extensions or {}).get(GHAST_NAMESPACE)
    if not isinstance(ghast, dict):
        errors.append(f"{path}: missing {GHAST_NAMESPACE} metadata extension")


def validate_agent_plugin_mcp(path: Path, mcp: dict, errors: list[str]) -> None:
    if set(mcp) != {"$schema", "mcpServers"}:
        errors.append(f"{path}: MCP top-level fields must be $schema and mcpServers")
    if mcp.get("$schema") != MCP_SCHEMA:
        errors.append(f"{path}: must target Agent Plugins MCP 1.0.0")
    servers = mcp.get("mcpServers")
    if not isinstance(servers, dict):
        errors.append(f"{path}: mcpServers must be an object")
        return
    for name, server in servers.items():
        if not isinstance(server, dict):
            errors.append(f"{path}: server {name!r} must be an object")
            continue
        transport = server.get("type")
        if transport == "stdio":
            allowed = {"type", "command", "args", "env", "cwd"}
            command = server.get("command")
            if not isinstance(command, str) or not command:
                errors.append(f"{path}: stdio server {name!r} needs command")
            elif command.startswith(".") and not command.startswith("./"):
                errors.append(f"{path}: invalid relative command for {name!r}")
            args = server.get("args")
            if args is not None and (
                not isinstance(args, list)
                or any(not isinstance(value, str) for value in args)
            ):
                errors.append(f"{path}: invalid args for {name!r}")
            env = server.get("env")
            if env is not None and (
                not isinstance(env, dict)
                or any(not isinstance(key, str) or not isinstance(value, str) for key, value in env.items())
                or "PLUGIN_ROOT" in env
                or "PLUGIN_DATA" in env
            ):
                errors.append(f"{path}: invalid env for {name!r}")
            cwd = server.get("cwd")
            if cwd is not None and (
                not isinstance(cwd, str)
                or not cwd.startswith(("./", "${PLUGIN_ROOT}", "${PLUGIN_DATA}"))
                or contains_parent_segment(cwd)
            ):
                errors.append(f"{path}: invalid cwd for {name!r}")
        elif transport in {"streamable-http", "sse"}:
            allowed = {"type", "url", "headers"}
            validate_mcp_url(path, name, server.get("url"), errors)
            headers = server.get("headers")
            if headers is not None:
                if not isinstance(headers, dict) or any(
                    not isinstance(key, str) or not isinstance(value, str)
                    for key, value in headers.items()
                ):
                    errors.append(f"{path}: invalid headers for {name!r}")
                elif len({key.lower() for key in headers}) != len(headers):
                    errors.append(f"{path}: duplicate case-insensitive header for {name!r}")
                elif any("$VAULT:" in value or "${" in value for value in headers.values()):
                    errors.append(f"{path}: credential placeholders are not portable for {name!r}")
        else:
            errors.append(f"{path}: unsupported MCP transport for {name!r}")
            continue
        unknown = set(server) - allowed
        if unknown:
            errors.append(f"{path}: server {name!r} has unknown fields {sorted(unknown)}")


def validate_mcp_url(path: Path, name: str, value: object, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{path}: server {name!r} needs a URL")
        return
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
        errors.append(f"{path}: invalid MCP URL for {name!r}")
    loopback = parsed.hostname == "localhost" or parsed.hostname in {"127.0.0.1", "::1"}
    if parsed.scheme != "https" and not loopback:
        errors.append(f"{path}: non-loopback MCP URL must use HTTPS for {name!r}")


def contains_parent_segment(value: str) -> bool:
    return ".." in value.replace("\\", "/").split("/")


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
        if validate_agent_skill is not None:
            for problem in validate_agent_skill(skill_dir):
                errors.append(f"{skill_path}: {problem}")


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
                manifest_member = f"{prefix}plugin.json"
                if manifest_member not in names:
                    errors.append(f"{package_path}: missing {manifest_member}")
                    continue
                packaged_manifest = json.loads(archive.read(manifest_member))
                if packaged_manifest != manifests[name]:
                    errors.append(f"{package_path}: manifest differs from source")
                ghast = packaged_manifest["extensions"][GHAST_NAMESPACE]
                icon_member = prefix + ghast["icon"].removeprefix("./")
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
    reviewed = {
        name
        for name, review in (reviews.get("plugins") or {}).items()
        if review.get("verificationStatus") == "official-source-verified"
    }
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
