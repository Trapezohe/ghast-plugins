#!/usr/bin/env python3
"""Verify the pinned official Temporal skill trees and Ghast package."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path
from types import ModuleType


EXPECTED_REVISION = "e9a28b0de6beb5305bd49d73453ab0f1cbd8d160"
EXPECTED_VERSION = "0.4.0"
EXPECTED_SKILLS = 4
EXPECTED_FILES = 152
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/temporal")
    return parser.parse_args()


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


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    importer = load_importer()
    revision = importer.git_revision(source)
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")
    if importer.normalized_git_remote(source) != importer.normalized_repository_url(
        "https://github.com/temporalio/codex-temporal-plugin"
    ):
        raise ValueError("Temporal official repository origin changed")

    upstream = json.loads(
        (source / "plugins/temporal/.codex-plugin/plugin.json").read_text()
    )
    manifest = json.loads((plugin / "plugin.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION:
        raise ValueError("official Temporal version changed")
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("Temporal is not Agent Plugins 1.0")
    if manifest.get("version") != f"{EXPECTED_VERSION}-ghast.1":
        raise ValueError("unexpected Ghast Temporal version")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("Temporal manifest revision differs from source")
    if not (plugin / ghast["icon"].removeprefix("./")).is_file():
        raise ValueError("Temporal icon is missing")

    with tempfile.TemporaryDirectory(prefix="ghast-temporal-output-") as temp:
        expected_root = Path(temp) / "skills"
        importer.copy_skill_tree(
            source / "plugins/temporal/skills",
            expected_root,
            recursive=False,
            preserve_agent_metadata=False,
            frontmatter_overrides={},
        )
        expected = file_map(expected_root)
        actual = file_map(plugin / "skills")
        if expected.keys() != actual.keys():
            raise ValueError("Temporal source and Ghast skill file sets differ")
        if len(expected) != EXPECTED_FILES:
            raise ValueError(f"expected {EXPECTED_FILES} Temporal files, found {len(expected)}")
        skill_count = sum(
            name.count("/") == 1 and name.endswith("/SKILL.md")
            for name in expected
        )
        if skill_count != EXPECTED_SKILLS:
            raise ValueError(f"expected {EXPECTED_SKILLS} Temporal skills, found {skill_count}")
        for relative, expected_path in expected.items():
            actual_path = actual[relative]
            if relative.endswith("/SKILL.md"):
                _, expected_body = split_skill(expected_path)
                _, actual_body = split_skill(actual_path)
                if expected_body.lstrip("\r\n") != actual_body.lstrip("\r\n"):
                    raise ValueError(f"{relative}: body differs from official source")
            elif expected_path.read_bytes() != actual_path.read_bytes():
                raise ValueError(f"{relative}: file differs from official source")

    provision = plugin / "skills/temporal-cloud-setup/scripts/provision.sh"
    subprocess.run(["bash", "-n", str(provision)], check=True)
    help_result = subprocess.run(
        ["bash", str(provision), "--help"],
        check=True,
        text=True,
        capture_output=True,
    )
    help_text = help_result.stdout + help_result.stderr
    for command in (
        "preflight",
        "preview",
        "start-namespace",
        "await-namespace",
        "scaffold",
        "create-key",
        "run-workflow",
        "cleanup-info",
    ):
        if command not in help_text:
            raise ValueError(f"Temporal provision command changed: {command}")
    preview = subprocess.run(
        [
            "bash",
            str(provision),
            "preview",
            "run-workflow",
            "--sdk",
            "python",
            "--dir",
            "/tmp/ghast-temporal-preview",
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    for marker in (
        "status=ok",
        "preview=run-workflow",
        "WORKFLOW_ID=money-transfer-",
        "Worker - runs in the background",
    ):
        if marker not in preview.stdout:
            raise ValueError(f"Temporal provision preview changed: {marker}")

    print(
        "verified Temporal 0.4.0 official 4-skill, 152-file tree, "
        "runnable Cloud provision helper and side-effect-free workflow "
        "preview, Agent Plugins 1.0 manifest, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
