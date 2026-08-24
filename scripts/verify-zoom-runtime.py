#!/usr/bin/env python3
"""Verify Zoom's complete official skills and seven OAuth MCP servers."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

import official_plugin_verification as verify

REVISION = "1858eadc17d9bd0d1279ce7f66304362a774e3b4"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=verify.REPOSITORY_ROOT / "plugins/zoom")
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(source) != imp.normalized_repository_url("https://github.com/zoom/skills"):
        raise ValueError("Zoom official source changed")
    verify.manifest(plugin, name="zoom", version="1.0.0-ghast.1", revision=REVISION)
    with tempfile.TemporaryDirectory(prefix="ghast-zoom-expected-") as temp:
        staging = Path(temp) / "staging"
        staging.mkdir()
        expected = staging / "skills"
        imp.copy_skill_tree(source / "skills", expected, recursive=False, preserve_agent_metadata=False, frontmatter_overrides={})
        imp.copy_root_skill(source, expected, {"source": "skills/SKILL.md", "name": "zoom-skills"})
        imp.apply_ghast_compatibility("zoom", staging)
        count = verify.compare_trees(expected, plugin / "skills", ignore_skill_frontmatter=True)
    if count != 808 or len(list((plugin / "skills").rglob("SKILL.md"))) != 58:
        raise ValueError("Zoom skill inventory changed")
    source_mcp = json.loads((source / ".mcp.json").read_text())["mcpServers"]
    packaged = json.loads((plugin / "mcp.json").read_text())["mcpServers"]
    if source_mcp.keys() != packaged.keys() or len(packaged) != 7:
        raise ValueError("Zoom MCP inventory changed")
    for name, source_server in source_mcp.items():
        server = packaged[name]
        if server.get("url") != source_server.get("url") or server.get("type") != "streamable-http":
            raise ValueError(f"Zoom MCP declaration differs: {name}")
        status, headers, body = verify.curl_json(server["url"], payload=verify.initialize_payload())
        if status != 401 or "oauth-protected-resource" not in headers.lower() or "Access token is required" not in json.dumps(body):
            raise ValueError(f"unexpected Zoom MCP boundary for {name}: HTTP {status}")
    print("verified Zoom official 58-skill/808-file tree, all 7 OAuth-protected MCP endpoints, Agent Plugins 1.0, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
