#!/usr/bin/env python3
"""Verify the pinned official Remotion plugin build, tests, and Ghast output."""

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


EXPECTED_REVISION = "05075f384a0a28e193876c1fd43ab9fba5ef10f9"
EXPECTED_VERSION = "4.0.515"
BUN_VERSION = "1.3.3"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/remotion")
    parser.add_argument("--bun", type=Path)
    return parser.parse_args()


def run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, **kwargs)


def resolve_bun(explicit: Path | None) -> Path:
    if explicit is not None:
        binary = explicit.expanduser().resolve()
    else:
        discovered = shutil.which("bun")
        if discovered:
            binary = Path(discovered).resolve()
        else:
            result = run(
                [
                    "npx",
                    "--yes",
                    f"--package=bun@{BUN_VERSION}",
                    "sh",
                    "-c",
                    "command -v bun",
                ],
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


def directory_hashes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def verify_checked_in_output(source: Path, plugin: Path) -> None:
    manifest = json.loads((plugin / "plugin.json").read_text())
    extension = manifest["extensions"]["ai.trapezohe.ghast"]
    if manifest["$schema"] != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("Remotion does not use the Agent Plugins 1.0 schema")
    if manifest["version"] != f"{EXPECTED_VERSION}-ghast.1":
        raise ValueError(f"unexpected Ghast Remotion version: {manifest['version']}")
    if extension["upstreamRevision"] != EXPECTED_REVISION:
        raise ValueError("Remotion manifest revision does not match the verifier")
    if not (plugin / "assets/icon.png").is_file():
        raise ValueError("Remotion icon is missing")

    importer = load_importer()
    with tempfile.TemporaryDirectory(prefix="ghast-remotion-output-") as temp:
        expected = Path(temp) / "skills"
        importer.build_remotion_skills(source, expected)
        expected_files = directory_hashes(expected)
        actual_files = directory_hashes(plugin / "skills")
        if expected_files != actual_files:
            missing = sorted(expected_files.keys() - actual_files.keys())
            extra = sorted(actual_files.keys() - expected_files.keys())
            changed = sorted(
                expected_files.keys() & actual_files.keys()
                - {name for name in expected_files if expected_files[name] == actual_files[name]}
            )
            raise ValueError(
                "checked-in Remotion skills differ from the pinned importer: "
                f"missing={missing}, extra={extra}, changed={changed}"
            )


def verify_official_tests(source: Path, bun: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="ghast-remotion-runtime-") as temp:
        root = Path(temp)
        tool_bin = root / "bin"
        tool_bin.mkdir()
        (tool_bin / "bun").symlink_to(bun)
        environment = os.environ.copy()
        environment["PATH"] = os.pathsep.join(
            [str(tool_bin), environment["PATH"]]
        )
        archive = root / "source.tar"
        checkout = root / "checkout"
        checkout.mkdir()
        run(
            ["git", "archive", "--output", str(archive), EXPECTED_REVISION],
            cwd=source,
        )
        with tarfile.open(archive) as package:
            package.extractall(checkout)
        run(["git", "init", "--quiet"], cwd=checkout)
        run([str(bun), "install", "--frozen-lockfile"], cwd=checkout, env=environment)
        run(
            [str(bun), "run", "test"],
            cwd=checkout / "packages/codex-plugin",
            env=environment,
        )


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    revision = run(
        ["git", "rev-parse", "HEAD"],
        cwd=source,
        capture_output=True,
    ).stdout.strip()
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")
    upstream_manifest = json.loads(
        (source / "packages/codex-plugin/.codex-plugin/plugin.json").read_text()
    )
    if upstream_manifest["version"] != EXPECTED_VERSION:
        raise ValueError(f"unexpected official version: {upstream_manifest['version']}")

    verify_checked_in_output(source, plugin)
    verify_official_tests(source, resolve_bun(args.bun))
    print(
        "verified Remotion 4.0.515 official build, 8-test suite, links, "
        "Agent Plugins 1.0 manifest, icon, and deterministic Ghast skills"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
