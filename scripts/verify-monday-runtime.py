#!/usr/bin/env python3
"""Verify monday.com's official skills and hosted OAuth MCP contract."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

import official_plugin_verification as verify

REVISION = "ce381e93a0a6c2ed3b9942ff1803b8078ba89389"
SKILLS_REVISION = "ee1f86171ba8c10879532d8334b2c19b61f1c372"
MCP_URL = "https://mcp.monday.com/mcp"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--skills-source", type=Path, required=True)
    parser.add_argument(
        "--plugin",
        type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/monday-com",
    )
    args = parser.parse_args()
    source = args.source.resolve()
    skills_source = args.skills_source.resolve()
    plugin = args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(
        source
    ) != imp.normalized_repository_url(
        "https://github.com/mondaycom/monday-claude-cowork-plugin"
    ):
        raise ValueError("monday.com official plugin source changed")
    if imp.git_revision(skills_source) != SKILLS_REVISION or imp.normalized_git_remote(
        skills_source
    ) != imp.normalized_repository_url("https://github.com/mondaycom/skills"):
        raise ValueError("monday.com canonical skills source changed")
    verify.manifest(
        plugin,
        name="monday-com",
        version='0.1.0',
        revision=REVISION,
    )

    with tempfile.TemporaryDirectory(prefix="ghast-monday-skills-") as temp:
        expected = Path(temp) / "skills"
        imp.copy_skill_tree(
            source / "skills",
            expected,
            recursive=False,
            preserve_agent_metadata=False,
            frontmatter_overrides={},
        )
        count = verify.compare_trees(
            expected,
            plugin / "skills",
            ignore_skill_frontmatter=True,
        )
    if count != 9 or len(list((plugin / "skills").rglob("SKILL.md"))) != 5:
        raise ValueError("monday.com packaged skill inventory changed")
    if verify.file_map(source / "skills").keys() != verify.file_map(
        skills_source / "skills"
    ).keys():
        raise ValueError("monday.com official skill repositories diverged")
    for name, path in verify.file_map(source / "skills").items():
        if path.read_bytes() != verify.file_map(skills_source / "skills")[name].read_bytes():
            raise ValueError(f"monday.com canonical skill differs: {name}")

    mcp = json.loads((plugin / "mcp.json").read_text())
    if mcp["mcpServers"]["monday"] != {
        "type": "streamable-http",
        "url": MCP_URL,
    }:
        raise ValueError("monday.com packaged MCP declaration changed")
    status, headers, body = verify.curl_json(
        MCP_URL, payload=verify.initialize_payload()
    )
    if status != 401 or "oauth-protected-resource" not in headers.lower() or "invalid_token" not in str(body):
        raise ValueError(f"unexpected monday.com MCP boundary: HTTP {status}")
    status, _, resource = verify.curl_json(
        "https://mcp.monday.com/.well-known/oauth-protected-resource/mcp"
    )
    if status != 200 or not isinstance(resource, dict) or resource.get(
        "authorization_servers"
    ) != ["https://auth.monday.com/mcp"]:
        raise ValueError("monday.com protected-resource metadata changed")
    status, _, oauth = verify.curl_json(
        "https://auth.monday.com/.well-known/oauth-authorization-server/mcp"
    )
    if (
        status != 200
        or not isinstance(oauth, dict)
        or oauth.get("registration_endpoint") != "https://auth.monday.com/oauth_ms/oauth/register"
        or "authorization_code" not in oauth.get("grant_types_supported", [])
        or "refresh_token" not in oauth.get("grant_types_supported", [])
        or "S256" not in oauth.get("code_challenge_methods_supported", [])
    ):
        raise ValueError("monday.com dynamic OAuth/PKCE metadata changed")
    print(
        "verified monday.com official 5-skill/9-file tree against both "
        "official repositories, hosted OAuth MCP, dynamic registration, "
        "PKCE S256, Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
