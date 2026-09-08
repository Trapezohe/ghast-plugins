#!/usr/bin/env python3
"""Verify HubSpot's official skills and separately installed Agent CLI."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import tempfile
import urllib.request
from pathlib import Path

import official_plugin_verification as verify

SKILLS_REVISION = "71f2bdefcc0247b1f378cb98186800dc57b6f6b1"
PUBLIC_HOME_REVISION = "0cba563cbf8d3efc5b3baade6d81869f95273948"
CLI_VERSION = "hubspot 0.13.0 (build 904, commit c2a1232)"
CLI_SHA256 = "d7fa1b68c17ce9686c7e8873fbf55a3217324af6541b0d5ddd8a86b94685c756"
CHECKSUM_URL = (
    "https://api.hubapi.com/hub/cli/backend/hub-cli/latest/"
    "hubspot-darwin-arm64.sha256"
)


def run(binary: Path, arguments: list[str], environment: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(binary), *arguments],
        env=environment,
        text=True,
        capture_output=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument(
        "--plugin",
        type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/hubspot",
    )
    args = parser.parse_args()
    source_root = args.source_root.resolve()
    skills = source_root / "hubspot-agent-cli-skills"
    public_home = source_root / "hubspot-agent-cli"
    binary = args.binary.expanduser().absolute()
    plugin = args.plugin.resolve()
    imp = verify.load_importer()

    if imp.git_revision(skills) != SKILLS_REVISION:
        raise ValueError("HubSpot official skills revision changed")
    if imp.normalized_git_remote(skills) != imp.normalized_repository_url(
        "https://github.com/HubSpot/agent-cli-skills"
    ):
        raise ValueError("HubSpot official skills origin changed")
    if imp.git_revision(public_home) != PUBLIC_HOME_REVISION:
        raise ValueError("HubSpot Agent CLI public-home revision changed")
    tags = subprocess.run(
        ["git", "tag", "--points-at", "HEAD"],
        cwd=public_home,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.splitlines()
    if tags != ["v0.11.0"]:
        raise ValueError("HubSpot Agent CLI public release tag changed")

    verify.manifest(
        plugin,
        name="hubspot",
        version=None,
        revision=SKILLS_REVISION,
    )
    with tempfile.TemporaryDirectory(prefix="ghast-hubspot-skills-") as temp:
        expected = Path(temp) / "skills"
        imp.copy_skill_tree(
            skills,
            expected,
            recursive=False,
            preserve_agent_metadata=False,
            frontmatter_overrides={},
        )
        count = verify.compare_trees(
            expected,
            plugin / "skills",
            ignore_skill_frontmatter=True,
        )
    if count != 26 or len(list((plugin / "skills").rglob("SKILL.md"))) != 15:
        raise ValueError("HubSpot official skill inventory changed")

    if not binary.is_file():
        raise ValueError(f"HubSpot verification binary is missing: {binary}")
    if hashlib.sha256(binary.read_bytes()).hexdigest() != CLI_SHA256:
        raise ValueError("HubSpot verification binary hash changed")
    request = urllib.request.Request(
        CHECKSUM_URL,
        headers={"User-Agent": "ghast-hubspot-audit/1.0"},
    )
    official_checksum = urllib.request.urlopen(request, timeout=30).read().decode().strip()
    if official_checksum.split()[0] != CLI_SHA256:
        raise ValueError("HubSpot official latest checksum changed")

    with tempfile.TemporaryDirectory(prefix="ghast-hubspot-home-") as home:
        environment = os.environ.copy()
        environment["HOME"] = home
        environment["HUBSPOT_NO_AUTO_UPGRADE"] = "1"
        environment.pop("HUBSPOT_ACCESS_TOKEN", None)
        version = run(binary, ["--version"], environment)
        if version.returncode != 0 or version.stdout.strip() != CLI_VERSION:
            raise ValueError("HubSpot CLI version changed")
        root_help = run(binary, ["--help"], environment)
        for marker in (
            "objects",
            "pipelines",
            "properties",
            "associations",
            "workflows",
            "activities",
            "conversations",
            "segments",
            "sequences",
            "reports",
            "imports",
            "history",
        ):
            if root_help.returncode != 0 or marker not in root_help.stdout:
                raise ValueError(f"HubSpot CLI command surface lost {marker}")
        mutation_help = {
            ("objects", "create", "--help"): ("--dry-run",),
            ("objects", "update", "--help"): ("--dry-run", "--digest", "--confirm"),
            ("objects", "merge", "--help"): ("--dry-run", "--digest", "--confirm", "irreversible"),
            ("objects", "delete", "--help"): ("--dry-run", "--digest", "--confirm", "permanently purge"),
            ("workflows", "create", "--help"): ("--dry-run",),
            ("imports", "start", "--help"): ("--dry-run",),
        }
        for command, markers in mutation_help.items():
            result = run(binary, list(command), environment)
            if result.returncode != 0 or any(marker not in result.stdout for marker in markers):
                raise ValueError(f"HubSpot mutation guard changed: {' '.join(command)}")
        whoami = run(binary, ["whoami"], environment)
        if whoami.returncode == 0 or "Not authenticated" not in whoami.stdout or "HUBSPOT_ACCESS_TOKEN" not in whoami.stdout:
            raise ValueError("HubSpot unauthenticated boundary changed")

    print(
        "verified HubSpot official 15-skill/26-file tree, checksum-pinned "
        "0.13.0 CLI, command surface, mutation guards, unauthenticated "
        "boundary, Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
