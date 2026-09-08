#!/usr/bin/env python3
"""Verify the pinned official Superpowers source, tests, and Ghast output."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path


EXPECTED_REVISION = "b36e0829c6d0140e93cfef2ca599b1b07d4a7797"
EXPECTED_VERSION = "6.3.0"
EXPECTED_SKILLS = 14
EXPECTED_BRAINSTORM_TESTS = 134
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--plugin",
        type=Path,
        default=REPOSITORY_ROOT / "plugins/superpowers",
    )
    return parser.parse_args()


def run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, **kwargs)


def capture(args: list[str], **kwargs: object) -> str:
    result = subprocess.run(args, text=True, capture_output=True, **kwargs)
    output = result.stdout + result.stderr
    if result.returncode:
        print(output, end="")
        result.check_returncode()
    return output


def split_skill(path: Path) -> tuple[str, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError(f"{path}: unterminated frontmatter")
    return text[4:closing], text[closing + 5 :]


def verify_skill_tree(source: Path, plugin: Path) -> None:
    source_root = source / "skills"
    plugin_root = plugin / "skills"
    source_files = {
        path.relative_to(source_root).as_posix(): path
        for path in source_root.rglob("*")
        if path.is_file()
    }
    plugin_files = {
        path.relative_to(plugin_root).as_posix(): path
        for path in plugin_root.rglob("*")
        if path.is_file()
    }
    if source_files.keys() != plugin_files.keys():
        raise ValueError("Superpowers source and Ghast skill file sets differ")

    skill_count = sum(name.endswith("/SKILL.md") for name in source_files)
    if skill_count != EXPECTED_SKILLS:
        raise ValueError(f"expected {EXPECTED_SKILLS} skills, found {skill_count}")
    for relative, source_path in source_files.items():
        plugin_path = plugin_files[relative]
        if relative.endswith("/SKILL.md"):
            _, source_body = split_skill(source_path)
            plugin_frontmatter, plugin_body = split_skill(plugin_path)
            expected_name = relative.split("/", 1)[0]
            if not re.search(
                rf"(?m)^name:\s*['\"]?{re.escape(expected_name)}['\"]?\s*$",
                plugin_frontmatter,
            ):
                raise ValueError(f"{relative}: normalized name is missing")
            if source_body.lstrip("\r\n") != plugin_body.lstrip("\r\n"):
                raise ValueError(f"{relative}: body differs from official source")
        elif source_path.read_bytes() != plugin_path.read_bytes():
            raise ValueError(f"{relative}: file differs from official source")


def verify_official_tests(source: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="ghast-superpowers-runtime-") as temp:
        root = Path(temp)
        archive = root / "source.tar"
        checkout = root / "checkout"
        checkout.mkdir()
        run(
            ["git", "archive", "--output", str(archive), EXPECTED_REVISION],
            cwd=source,
        )
        with tarfile.open(archive) as package:
            package.extractall(checkout)

        environment = os.environ.copy()
        environment["TZ"] = "UTC"
        run(["git", "init", "--quiet"], cwd=checkout)
        run(["git", "config", "user.email", "ghast-audit@example.invalid"], cwd=checkout)
        run(["git", "config", "user.name", "Ghast Audit"], cwd=checkout)
        run(["git", "add", "."], cwd=checkout)
        run(["git", "commit", "--quiet", "-m", "audit fixture"], cwd=checkout)

        brainstorm = checkout / "tests/brainstorm-server"
        run(["npm", "ci"], cwd=brainstorm, env=environment)
        output = capture(["npm", "test"], cwd=brainstorm, env=environment)
        passed = sum(int(value) for value in re.findall(r"\b(\d+) passed\b", output))
        if passed != EXPECTED_BRAINSTORM_TESTS or re.search(r"\b[1-9]\d* failed\b", output):
            print(output, end="")
            raise ValueError(
                f"expected {EXPECTED_BRAINSTORM_TESTS} passing brainstorm tests, found {passed}"
            )

        shell_tests = (
            "tests/codex/test-marketplace-manifest.sh",
            "tests/codex/test-package-codex-plugin.sh",
            "tests/codex-plugin-sync/test-sync-to-codex-plugin.sh",
            "tests/hooks/test-session-start.sh",
            "tests/shell-lint/test-lint-shell.sh",
            "tests/systematic-debugging/test-find-polluter.sh",
            "tests/claude-code/test-sdd-workspace.sh",
            "tests/claude-code/test-worktree-path-policy.sh",
        )
        for test in shell_tests:
            run(["bash", test], cwd=checkout, env=environment)


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    revision = run(
        ["git", "rev-parse", "HEAD"], cwd=source, capture_output=True
    ).stdout.strip()
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")
    if run(["git", "status", "--porcelain"], cwd=source, capture_output=True).stdout:
        raise ValueError("Superpowers source checkout is not clean")

    upstream_manifest = json.loads((source / ".codex-plugin/plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    if upstream_manifest["version"] != EXPECTED_VERSION:
        raise ValueError("official Superpowers version changed")
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("Superpowers is not Agent Plugins 1.0")
    if manifest.get("version") != '6.3.0':
        raise ValueError("unexpected Ghast Superpowers version")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("Superpowers manifest revision differs from source")
    if not (plugin / "assets/icon.png").is_file():
        raise ValueError("Superpowers icon is missing")

    verify_skill_tree(source, plugin)
    verify_official_tests(source)
    print(
        "verified Superpowers 6.3.0 official 134-test brainstorm suite, "
        "8 shell integration suites, 14-skill tree, Agent Plugins 1.0 manifest, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
