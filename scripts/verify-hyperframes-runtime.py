#!/usr/bin/env python3
"""Verify HyperFrames' official skills, tests, and published CLI contract."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

import official_plugin_verification as verify

REVISION = "dd0626a55a0d0f24cae1b00bd2c95c0ebfa7a573"
REPOSITORY = "https://github.com/heygen-com/hyperframes"
VERSION = "0.8.10"
NPM_INTEGRITY = (
    "sha512-koK5dsyJG6uJ/8higXmnEZc0sDfFVs/F4xdbKHtx+AyMs8Q+"
    "gYpI45Elbh/JQn7OkYl8dJ1ojm7sa5/J6Ha6jQ=="
)


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        command, cwd=cwd, env=env, check=True, text=True, capture_output=True
    )
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--plugin", type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/hyperframes",
    )
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(
        source
    ) != imp.normalized_repository_url(REPOSITORY):
        raise ValueError("HyperFrames official source identity changed")
    verify.manifest(
        plugin, name="hyperframes", version=f"{VERSION}-ghast.1", revision=REVISION
    )

    with tempfile.TemporaryDirectory(prefix="ghast-hyperframes-skills-") as temp:
        expected = Path(temp) / "skills"
        imp.copy_skill_tree(
            source / "skills", expected, recursive=False,
            preserve_agent_metadata=False, frontmatter_overrides={},
        )
        count = verify.compare_trees(
            expected, plugin / "skills", ignore_skill_frontmatter=True
        )
    if count != 902 or len(list((plugin / "skills").rglob("SKILL.md"))) != 20:
        raise ValueError("HyperFrames packaged skill inventory changed")

    tests = run(["node", "--test", "skills/**/*.test.mjs"], cwd=source)
    for marker in ("tests 525", "pass 518", "fail 0", "skipped 7"):
        if marker not in tests:
            raise ValueError(f"HyperFrames skill tests changed: missing {marker!r}")
    npm = json.loads(run([
        "npm", "view", f"hyperframes@{VERSION}", "version", "repository.url",
        "license", "dist.integrity", "--json",
    ], cwd=source))
    if npm != {
        "version": VERSION,
        "repository.url": "git+https://github.com/heygen-com/hyperframes.git",
        "license": "Apache-2.0",
        "dist.integrity": NPM_INTEGRITY,
    }:
        raise ValueError("HyperFrames official npm identity changed")
    with tempfile.TemporaryDirectory(prefix="ghast-hyperframes-cli-") as temp:
        work = Path(temp)
        env = os.environ.copy()
        env.update({
            "HOME": str(work / "home"),
            "XDG_CONFIG_HOME": str(work / "config"),
            "HYPERFRAMES_NO_TELEMETRY": "1",
        })
        version = run(
            ["npx", "--yes", f"hyperframes@{VERSION}", "--version"],
            cwd=work, env=env,
        ).strip()
        help_text = run(
            ["npx", "--yes", f"hyperframes@{VERSION}", "--help"],
            cwd=work, env=env,
        )
    if version != VERSION:
        raise ValueError("HyperFrames CLI version changed")
    for command in (
        "init", "capture", "catalog", "preview", "render", "lint", "check",
        "snapshot", "cloud", "lambda", "cloudrun", "transcribe", "tts",
    ):
        if command not in help_text:
            raise ValueError(f"HyperFrames CLI help is missing {command!r}")
    print(
        "verified HyperFrames 0.8.10 official 20-skill/902-file tree, "
        "518 passing and 7 skipped skill tests, npm integrity, isolated CLI, "
        "Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
