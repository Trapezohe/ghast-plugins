#!/usr/bin/env python3
"""Verify Airtable's pinned official skills and OAuth MCP contract."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path
from types import ModuleType

EXPECTED_REVISION = "812ee67f1fd3d76fb45ff8df40afaa0448602ba8"
EXPECTED_VERSION = "0.1.0"
EXPECTED_SKILLS = 8
EXPECTED_FILES = 20
MCP_URL = "https://mcp.airtable.com/mcp"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/airtable")
    return parser.parse_args()


def importer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ghast_importer", IMPORTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load official importer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def files(root: Path) -> dict[str, Path]:
    return {p.relative_to(root).as_posix(): p for p in root.rglob("*") if p.is_file()}


def curl(url: str, *, post: bool = False) -> tuple[int, str, str]:
    with tempfile.TemporaryDirectory(prefix="ghast-airtable-http-") as temp:
        headers, body = Path(temp) / "headers", Path(temp) / "body"
        command = ["curl", "-sS", "-D", str(headers), "-o", str(body), "-w", "%{http_code}"]
        if post:
            command += ["-X", "POST", "-H", "Content-Type: application/json", "-H", "Accept: application/json, text/event-stream", "--data", '{"jsonrpc":"2.0","id":1,"method":"tools/list"}']
        result = subprocess.run(command + [url], check=True, text=True, capture_output=True)
        return int(result.stdout), headers.read_text(), body.read_text()


def main() -> int:
    parsed = args()
    source, plugin = parsed.source.resolve(), parsed.plugin.resolve()
    imp = importer()
    if imp.git_revision(source) != EXPECTED_REVISION:
        raise ValueError("Airtable source revision changed")
    if imp.normalized_git_remote(source) != imp.normalized_repository_url("https://github.com/airtable/skills"):
        raise ValueError("Airtable source origin changed")
    source_plugin = source / "plugins/airtable"
    upstream = json.loads((source_plugin / ".codex-plugin/plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION:
        raise ValueError("Airtable version changed")
    if manifest.get("$schema") != PLUGIN_SCHEMA or manifest.get("version") != '0.1.0':
        raise ValueError("unexpected Airtable Agent Plugins 1.0 manifest")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION or not (plugin / ghast["icon"].removeprefix("./")).is_file():
        raise ValueError("Airtable revision or icon differs")
    if mcp["mcpServers"]["airtable"].get("url") != MCP_URL:
        raise ValueError("Airtable MCP endpoint changed")
    with tempfile.TemporaryDirectory(prefix="ghast-airtable-output-") as temp:
        expected_root = Path(temp) / "skills"
        imp.copy_skill_tree(source_plugin / "skills", expected_root, recursive=False, preserve_agent_metadata=False, frontmatter_overrides={})
        expected, actual = files(expected_root), files(plugin / "skills")
        if expected.keys() != actual.keys() or len(expected) != EXPECTED_FILES:
            raise ValueError("Airtable skill file sets differ")
        if sum(name.count("/") == 1 and name.endswith("/SKILL.md") for name in expected) != EXPECTED_SKILLS:
            raise ValueError("Airtable skill count changed")
        for name, path in expected.items():
            if path.read_bytes() != actual[name].read_bytes():
                raise ValueError(f"Airtable output differs: {name}")
    status, headers, _ = curl(MCP_URL, post=True)
    if status != 401 or "oauth-protected-resource" not in headers.lower():
        raise ValueError(f"unexpected Airtable MCP boundary: HTTP {status}")
    status, _, body = curl("https://mcp.airtable.com/.well-known/oauth-authorization-server")
    metadata = json.loads(body) if status == 200 else {}
    if metadata.get("registration_endpoint") != "https://airtable.com/oauth2/v1/register" or "S256" not in metadata.get("code_challenge_methods_supported", []):
        raise ValueError("Airtable dynamic OAuth/PKCE metadata changed")
    required = {"data.records:read", "data.records:write", "schema.bases:read", "schema.bases:write"}
    if not required.issubset(metadata.get("scopes_supported", [])):
        raise ValueError("Airtable MCP scopes changed")
    print("verified Airtable official 8-skill, 20-file tree, dynamic OAuth S256 contract, read/write scopes, Agent Plugins 1.0, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
