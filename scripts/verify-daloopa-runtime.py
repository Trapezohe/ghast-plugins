#!/usr/bin/env python3
"""Verify Daloopa's official skill tree and hosted OAuth MCP boundary."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

import official_plugin_verification as verify

REVISION = "1f112599065abb7cac3489c30f9e4bb27c68ad8e"
REPOSITORY = "https://github.com/daloopa/daloopa-plugin-codex"
DATA_URL = "https://mcp.daloopa.com/server/mcp"
DOCS_URL = "https://docs.daloopa.com/mcp"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--plugin", type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/daloopa",
    )
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(
        source
    ) != imp.normalized_repository_url(REPOSITORY):
        raise ValueError("Daloopa official source identity changed")
    verify.manifest(
        plugin, name="daloopa", version="1.0.0-ghast.1", revision=REVISION
    )

    with tempfile.TemporaryDirectory(prefix="ghast-daloopa-skills-") as temp:
        expected = Path(temp) / "skills"
        imp.copy_skill_tree(
            source / "skills", expected, recursive=False,
            preserve_agent_metadata=False, frontmatter_overrides={},
        )
        for name in ("data-access.md", "design-system.md"):
            (expected / name).write_bytes((source / "skills" / name).read_bytes())
        count = verify.compare_trees(
            expected, plugin / "skills", ignore_skill_frontmatter=True
        )
    if count != 26 or len(list((plugin / "skills").rglob("SKILL.md"))) != 21:
        raise ValueError("Daloopa packaged skill inventory changed")
    for skill in (plugin / "skills").rglob("SKILL.md"):
        text = skill.read_text()
        for shared in ("../data-access.md", "../design-system.md"):
            if shared in text and not (skill.parent / shared).resolve().is_file():
                raise ValueError(f"{skill}: missing shared reference {shared}")

    mcp = json.loads((plugin / "mcp.json").read_text())
    if mcp.get("mcpServers") != {
        "daloopa": {"type": "streamable-http", "url": DATA_URL},
        "daloopa-docs": {"type": "streamable-http", "url": DOCS_URL},
    }:
        raise ValueError("Daloopa packaged MCP declarations changed")
    status, headers, _ = verify.curl_json(
        DATA_URL, payload=verify.initialize_payload()
    )
    if status != 401 or "oauth-protected-resource" not in headers.lower():
        raise ValueError(f"unexpected Daloopa data MCP boundary: HTTP {status}")
    status, _, resource = verify.curl_json(
        "https://mcp.daloopa.com/.well-known/oauth-protected-resource"
    )
    if status != 200 or not isinstance(resource, dict) or resource != {
        "resource": DATA_URL,
        "authorization_servers": ["https://mcp.daloopa.com"],
    }:
        raise ValueError("Daloopa protected-resource metadata changed")
    status, _, oauth = verify.curl_json(
        "https://mcp.daloopa.com/.well-known/oauth-authorization-server"
    )
    if (
        status != 200 or not isinstance(oauth, dict)
        or oauth.get("registration_endpoint") != "https://mcp.daloopa.com/register"
        or oauth.get("grant_types_supported") != ["authorization_code"]
        or oauth.get("code_challenge_methods_supported") != ["S256"]
    ):
        raise ValueError("Daloopa OAuth metadata changed")
    print(
        "verified Daloopa official 21-skill/26-file tree, shared references, "
        "two MCP declarations, live data OAuth boundary, dynamic registration, "
        "PKCE S256, Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
