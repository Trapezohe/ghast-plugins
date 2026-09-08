#!/usr/bin/env python3
"""Verify Superhuman's official skills and Mail OAuth MCP contract."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

import official_plugin_verification as verify

REVISION = "a83580e994604edca1cd5661a4a1865f3f39abc9"
MCP_URL = "https://mcp.mail.superhuman.com/mcp"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--plugin",
        type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/superhuman",
    )
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(
        source
    ) != imp.normalized_repository_url("https://github.com/superhuman/mcp-mail"):
        raise ValueError("Superhuman official source changed")
    verify.manifest(
        plugin,
        name="superhuman",
        version='0.1.0',
        revision=REVISION,
    )
    with tempfile.TemporaryDirectory(prefix="ghast-superhuman-skills-") as temp:
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
    if count != 7 or len(list((plugin / "skills").rglob("SKILL.md"))) != 7:
        raise ValueError("Superhuman packaged skill inventory changed")

    mcp = json.loads((plugin / "mcp.json").read_text())
    if mcp["mcpServers"]["superhuman-mail"] != {
        "type": "streamable-http",
        "url": MCP_URL,
    }:
        raise ValueError("Superhuman packaged MCP declaration changed")
    status, headers, body = verify.curl_json(
        MCP_URL, payload=verify.initialize_payload()
    )
    if status != 401 or "oauth-protected-resource" not in headers.lower() or "missing-mcp-token" not in str(body):
        raise ValueError(f"unexpected Superhuman MCP boundary: HTTP {status}")
    status, _, resource = verify.curl_json(
        "https://mcp.mail.superhuman.com/.well-known/oauth-protected-resource/mcp"
    )
    if status != 200 or not isinstance(resource, dict) or resource.get(
        "authorization_servers"
    ) != ["https://mcp.auth.mail.superhuman.com"]:
        raise ValueError("Superhuman protected-resource metadata changed")
    status, _, oauth = verify.curl_json(
        "https://mcp.auth.mail.superhuman.com/.well-known/oauth-authorization-server"
    )
    grants = set(oauth.get("grant_types_supported", [])) if isinstance(oauth, dict) else set()
    if (
        status != 200
        or not isinstance(oauth, dict)
        or oauth.get("registration_endpoint") != "https://mcp.auth.mail.superhuman.com/oauth2/register"
        or not {"authorization_code", "refresh_token", "urn:ietf:params:oauth:grant-type:device_code"}.issubset(grants)
        or "S256" not in oauth.get("code_challenge_methods_supported", [])
    ):
        raise ValueError("Superhuman OAuth metadata changed")
    print(
        "verified Superhuman official 7-skill tree, hosted Mail MCP, dynamic "
        "OAuth, PKCE S256, authorization/refresh/device grants, Agent Plugins "
        "1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
