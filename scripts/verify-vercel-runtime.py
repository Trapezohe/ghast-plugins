#!/usr/bin/env python3
"""Verify Vercel's pinned official build, tests, and Ghast output."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path
from types import ModuleType


EXPECTED_REVISION = "c4a1c4e2e16feefb1d9f2ad2a4a451abd0ae91c6"
EXPECTED_VERSION = "0.48.1"
EXPECTED_SKILLS = 34
EXPECTED_TESTS = 974
BUN_VERSION = "1.3.3"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/vercel")
    parser.add_argument("--bun", type=Path)
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


def resolve_bun(explicit: Path | None) -> Path:
    if explicit is not None:
        binary = explicit.expanduser().resolve()
    elif discovered := shutil.which("bun"):
        binary = Path(discovered).resolve()
    else:
        result = run(
            ["npx", "--yes", f"--package=bun@{BUN_VERSION}", "sh", "-c", "command -v bun"],
            capture_output=True,
        )
        binary = Path(result.stdout.strip()).resolve()
    version = run([str(binary), "--version"], capture_output=True).stdout.strip()
    if version != BUN_VERSION:
        raise ValueError(f"expected Bun {BUN_VERSION}, found {version}")
    return binary


def load_importer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ghast_official_importer", IMPORTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {IMPORTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def split_skill(path: Path) -> tuple[str, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError(f"{path}: unterminated frontmatter")
    return text[4:closing], text[closing + 5 :]


def file_map(root: Path) -> dict[str, Path]:
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }


def verify_checked_in_output(source: Path, plugin: Path) -> None:
    importer = load_importer()
    with tempfile.TemporaryDirectory(prefix="ghast-vercel-output-") as temp:
        expected_root = Path(temp) / "skills"
        importer.copy_skill_tree(
            source / "skills",
            expected_root,
            recursive=False,
            preserve_agent_metadata=False,
            frontmatter_overrides={},
        )
        expected = file_map(expected_root)
        actual = file_map(plugin / "skills")
        if expected.keys() != actual.keys():
            raise ValueError("Vercel source and Ghast skill file sets differ")
        skill_count = sum(
            name.count("/") == 1 and name.endswith("/SKILL.md")
            for name in expected
        )
        if skill_count != EXPECTED_SKILLS:
            raise ValueError(f"expected {EXPECTED_SKILLS} Vercel skills, found {skill_count}")
        for relative, expected_path in expected.items():
            actual_path = actual[relative]
            if relative.endswith("/SKILL.md"):
                _, expected_body = split_skill(expected_path)
                _, actual_body = split_skill(actual_path)
                if expected_body.lstrip("\r\n") != actual_body.lstrip("\r\n"):
                    raise ValueError(f"{relative}: body differs from official source")
            elif expected_path.read_bytes() != actual_path.read_bytes():
                raise ValueError(f"{relative}: file differs from official source")

    command_root = plugin / "ai.trapezohe.ghast/commands"
    for name in ("bootstrap.md", "deploy.md", "env.md", "status.md"):
        if (source / "commands" / name).read_bytes() != (command_root / name).read_bytes():
            raise ValueError(f"Vercel command differs from official source: {name}")


def verify_official_ci(source: Path, bun: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="ghast-vercel-runtime-") as temp:
        root = Path(temp)
        archive = root / "source.tar"
        checkout = root / "checkout"
        checkout.mkdir()
        run(["git", "archive", "--output", str(archive), EXPECTED_REVISION], cwd=source)
        with tarfile.open(archive) as package:
            package.extractall(checkout)

        tool_bin = root / "bin"
        tool_bin.mkdir()
        (tool_bin / "bun").symlink_to(bun)
        environment = os.environ.copy()
        environment["PATH"] = os.pathsep.join([str(tool_bin), environment["PATH"]])

        run([str(bun), "install", "--frozen-lockfile"], cwd=checkout, env=environment)
        commands = (
            [str(bun), "run", "build:manifest:check"],
            [str(bun), "run", "build:from-skills:check"],
            [str(bun), "run", "build"],
            [str(bun), "run", "typecheck"],
            [str(bun), "run", "validate"],
        )
        for command in commands:
            capture(command, cwd=checkout, env=environment)
        output = capture([str(bun), "test"], cwd=checkout, env=environment)
        if f"{EXPECTED_TESTS} pass" not in output or "0 fail" not in output:
            raise ValueError("Vercel official test summary changed")


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    revision = run(["git", "rev-parse", "HEAD"], cwd=source, capture_output=True).stdout.strip()
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")
    if run(["git", "status", "--porcelain"], cwd=source, capture_output=True).stdout:
        raise ValueError("Vercel source checkout is not clean")

    upstream = json.loads((source / ".claude-plugin/plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION:
        raise ValueError("official Vercel version changed")
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("Vercel is not Agent Plugins 1.0")
    if manifest.get("version") != '0.48.1':
        raise ValueError("unexpected Ghast Vercel version")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("Vercel manifest revision differs from source")
    if mcp.get("mcpServers", {}).get("vercel", {}).get("url") != "https://mcp.vercel.com":
        raise ValueError("Vercel MCP URL changed")
    icon = plugin / ghast["icon"].removeprefix("./")
    if not icon.is_file():
        raise ValueError("Vercel icon is missing")

    verify_checked_in_output(source, plugin)
    verify_official_ci(source, resolve_bun(args.bun))
    print(
        "verified Vercel 0.48.1 official build, typecheck, structural validation, "
        "974-test suite, 34 skills, 4 commands, Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
