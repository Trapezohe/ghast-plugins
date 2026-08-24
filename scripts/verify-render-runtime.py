#!/usr/bin/env python3
"""Verify Render's official skills and generic API-key Ghast adapter."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import tempfile
from pathlib import Path
from types import ModuleType

EXPECTED_REVISION = "14032768453fd21c57f7e3a9c0e7659a2c7dce9d"
EXPECTED_VERSION = "0.2.0"
EXPECTED_SKILLS = 21
EXPECTED_FILES = 87
MCP_URL = "https://mcp.render.com/mcp"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/render")
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


def main() -> int:
    parsed = args()
    source, plugin = parsed.source.resolve(), parsed.plugin.resolve()
    imp = importer()
    if imp.git_revision(source) != EXPECTED_REVISION or imp.normalized_git_remote(source) != imp.normalized_repository_url("https://github.com/renderinc/render-codex-plugin"):
        raise ValueError("Render official source changed")
    upstream = json.loads((source / ".codex-plugin/plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION or manifest.get("version") != f"{EXPECTED_VERSION}-ghast.1" or manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("unexpected Render Agent Plugins 1.0 manifest")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION or not (plugin / ghast["icon"].removeprefix("./")).is_file():
        raise ValueError("Render revision or icon differs")
    if mcp["mcpServers"]["render"].get("url") != MCP_URL:
        raise ValueError("Render MCP endpoint changed")
    credential = ghast.get("mcpServerExtensions", {}).get("render", {}).get("credentialHeaders", {}).get("Authorization")
    if credential != "Bearer $VAULT:render-api-key":
        raise ValueError("Render generic API-key Vault binding is missing")
    if "client_id" in json.dumps({"manifest": manifest, "mcp": mcp}) or '"oauth"' in json.dumps({"manifest": manifest, "mcp": mcp}):
        raise ValueError("Render adapter must not reuse the Codex OAuth client")
    with tempfile.TemporaryDirectory(prefix="ghast-render-output-") as temp:
        expected_root = Path(temp) / "skills"
        imp.copy_skill_tree(source / "skills", expected_root, recursive=False, preserve_agent_metadata=False, frontmatter_overrides={})
        expected, actual = files(expected_root), files(plugin / "skills")
        if expected.keys() != actual.keys() or len(expected) != EXPECTED_FILES:
            raise ValueError("Render skill file sets differ")
        if sum(name.count("/") == 1 and name.endswith("/SKILL.md") for name in expected) != EXPECTED_SKILLS:
            raise ValueError("Render skill count changed")
        for name, path in expected.items():
            if path.read_bytes() != actual[name].read_bytes():
                raise ValueError(f"Render output differs: {name}")
    source_scripts, actual_scripts = files(source / "scripts"), files(plugin / "scripts")
    if source_scripts.keys() != actual_scripts.keys():
        raise ValueError("Render script file sets differ")
    for name, path in source_scripts.items():
        if path.read_bytes() != actual_scripts[name].read_bytes():
            raise ValueError(f"Render script differs: {name}")
        subprocess.run(["bash", "-n", str(actual_scripts[name])], check=True)
    environment = os.environ.copy()
    environment["PATH"] = "/usr/bin:/bin"
    diagnostic = subprocess.run(["bash", str(plugin / "scripts/validate-render-yaml.sh")], cwd=tempfile.gettempdir(), env=environment, check=True, text=True, capture_output=True)
    if "Render CLI not found" not in diagnostic.stdout:
        raise ValueError("Render no-CLI diagnostic changed")
    with tempfile.TemporaryDirectory(prefix="ghast-render-http-") as temp:
        headers = Path(temp) / "headers"
        result = subprocess.run(["curl", "-sS", "-D", str(headers), "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "-H", "Content-Type: application/json", "-H", "Accept: application/json, text/event-stream", "--data", '{"jsonrpc":"2.0","id":1,"method":"tools/list"}', MCP_URL], check=True, text=True, capture_output=True)
        if result.stdout != "401" or "oauth-protected-resource" not in headers.read_text().lower():
            raise ValueError(f"unexpected Render MCP boundary: HTTP {result.stdout}")
    print("verified Render official 21-skill, 87-file tree, two scripts, generic API-key Vault adapter without Codex OAuth identity, MCP boundary, Agent Plugins 1.0, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
