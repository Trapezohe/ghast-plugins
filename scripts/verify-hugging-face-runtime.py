#!/usr/bin/env python3
"""Verify Hugging Face's pinned official skills and public Hub workflow."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from types import ModuleType


EXPECTED_REVISION = "020194918dc4a27d5a5d9a154b6b56cc2bd21364"
EXPECTED_VERSION = "1.0.25"
EXPECTED_SKILLS = 26
EXPECTED_FILES = 159
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_URL = "https://huggingface.co/mcp?login"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/hugging-face")
    return parser.parse_args()


def load_importer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ghast_official_importer", IMPORTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {IMPORTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def split_skill(path: Path) -> str:
    text = path.read_text()
    closing = text.find("\n---\n", 4) if text.startswith("---\n") else -1
    if closing < 0:
        raise ValueError(f"{path}: invalid frontmatter")
    return text[closing + 5 :].lstrip("\r\n")


def file_map(root: Path) -> dict[str, Path]:
    return {path.relative_to(root).as_posix(): path for path in root.rglob("*") if path.is_file()}


def verify_checked_in_output(source: Path, plugin: Path, importer: ModuleType) -> None:
    with tempfile.TemporaryDirectory(prefix="ghast-hugging-face-output-") as temp:
        expected_root = Path(temp) / "skills"
        importer.copy_skill_tree(
            source / "skills", expected_root, recursive=False,
            preserve_agent_metadata=False, frontmatter_overrides={},
        )
        importer.copy_skill_tree(
            source / "hf-mcp/skills", expected_root, recursive=False,
            preserve_agent_metadata=False, frontmatter_overrides={}, merge=True,
        )
        expected = file_map(expected_root)
        actual = file_map(plugin / "skills")
        if expected.keys() != actual.keys() or len(expected) != EXPECTED_FILES:
            raise ValueError("Hugging Face official and Ghast skill file sets differ")
        count = sum(name.count("/") == 1 and name.endswith("/SKILL.md") for name in expected)
        if count != EXPECTED_SKILLS:
            raise ValueError(f"expected {EXPECTED_SKILLS} skills, found {count}")
        for relative, expected_path in expected.items():
            actual_path = actual[relative]
            if relative.endswith("/SKILL.md"):
                if split_skill(expected_path) != split_skill(actual_path):
                    raise ValueError(f"{relative}: body differs from official source")
            elif expected_path.read_bytes() != actual_path.read_bytes():
                raise ValueError(f"{relative}: differs from official source")


def verify_python_syntax(plugin: Path) -> int:
    scripts = sorted(plugin.glob("skills/**/*.py"))
    for path in scripts:
        compile(path.read_text(), str(path), "exec")
    return len(scripts)


def request_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "ghast-plugin-verifier/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def verify_public_hub_and_auth_boundary() -> None:
    model = request_json("https://huggingface.co/api/models/bert-base-uncased")
    if model.get("modelId") != "google-bert/bert-base-uncased":
        raise ValueError("Hugging Face public model metadata workflow changed")
    request = urllib.request.Request(
        MCP_URL,
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        method="POST",
    )
    try:
        urllib.request.urlopen(request, timeout=30)
    except urllib.error.HTTPError as error:
        if error.code not in {401, 403}:
            raise ValueError(f"unexpected Hugging Face MCP boundary: HTTP {error.code}") from error
    else:
        raise ValueError("Hugging Face MCP unexpectedly allowed unauthenticated tools/list")


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    importer = load_importer()
    if importer.git_revision(source) != EXPECTED_REVISION:
        raise ValueError("Hugging Face source revision changed")
    if importer.normalized_git_remote(source) != importer.normalized_repository_url(
        "https://github.com/huggingface/skills"
    ):
        raise ValueError("Hugging Face official repository origin changed")
    upstream = json.loads((source / ".claude-plugin/plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION:
        raise ValueError("official Hugging Face version changed")
    if manifest.get("$schema") != PLUGIN_SCHEMA or manifest.get("version") != '1.0.25':
        raise ValueError("unexpected Hugging Face Agent Plugins 1.0 manifest")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("Hugging Face manifest revision differs")
    if not (plugin / ghast["icon"].removeprefix("./")).is_file():
        raise ValueError("Hugging Face icon is missing")
    if mcp["mcpServers"]["huggingface-skills"].get("url") != MCP_URL:
        raise ValueError("Hugging Face official MCP endpoint changed")
    verify_checked_in_output(source, plugin, importer)
    python_scripts = verify_python_syntax(plugin)
    verify_public_hub_and_auth_boundary()
    print(f"verified Hugging Face 1.0.25 official 26-skill, 159-file tree, {python_scripts} Python scripts, public Hub read, authenticated MCP boundary, Agent Plugins 1.0, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
