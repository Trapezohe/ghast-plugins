#!/usr/bin/env python3
"""Verify Twilio's complete official skill tree and public docs MCP."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

import official_plugin_verification as verify

REVISION = "8aba46fb65dc8d9a20f4b301a68352064b4159a5"
MCP_URL = "https://mcp.twilio.com/docs"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=verify.REPOSITORY_ROOT / "plugins/twilio-developer-kit")
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(source) != imp.normalized_repository_url("https://github.com/twilio/ai"):
        raise ValueError("Twilio official source changed")
    verify.manifest(plugin, name="twilio-developer-kit", version='0.2.0', revision=REVISION)
    with tempfile.TemporaryDirectory(prefix="ghast-twilio-expected-") as temp:
        expected = Path(temp) / "skills"
        imp.copy_skill_tree(source / "skills", expected, recursive=True, preserve_agent_metadata=False, frontmatter_overrides=imp.PLUGINS["twilio-developer-kit"]["frontmatter_overrides"])
        count = verify.compare_trees(expected, plugin / "skills", ignore_skill_frontmatter=True)
    if count != 170 or len(list((plugin / "skills").rglob("SKILL.md"))) != 57:
        raise ValueError("Twilio skill inventory changed")
    mcp = json.loads((plugin / "mcp.json").read_text())
    if mcp["mcpServers"]["twilio-docs"].get("url") != MCP_URL:
        raise ValueError("Twilio MCP declaration changed")
    status, _, initialized = verify.curl_json(MCP_URL, payload=verify.initialize_payload())
    if status != 200 or not isinstance(initialized, dict) or initialized.get("result", {}).get("serverInfo", {}).get("name") != "twilio-docs-mcp":
        raise ValueError(f"unexpected Twilio MCP initialization: HTTP {status}")
    status, _, listed = verify.curl_json(MCP_URL, payload=verify.tools_list_payload())
    tools = listed.get("result", {}).get("tools", []) if isinstance(listed, dict) else []
    names = {tool.get("name") for tool in tools}
    if status != 200 or not {"twilio__search", "twilio__retrieve"}.issubset(names) or any(not tool.get("annotations", {}).get("readOnlyHint") for tool in tools):
        raise ValueError("Twilio public read-only tool contract changed")
    print("verified Twilio official 57-skill/170-file tree, anonymous read-only docs MCP tools, Agent Plugins 1.0, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
