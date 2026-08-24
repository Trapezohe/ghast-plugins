#!/usr/bin/env python3
"""Verify Stripe's official Agent Plugins 1.0 package and OAuth MCP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import official_plugin_verification as verify

REVISION = "bad904b02f7071592c38bcca83d33667ff015bb1"
MCP_URL = "https://mcp.stripe.com"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=verify.REPOSITORY_ROOT / "plugins/stripe")
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(source) != imp.normalized_repository_url("https://github.com/stripe/ai"):
        raise ValueError("Stripe official source changed")
    source_plugin = source / "providers/agent-plugins/plugin"
    upstream = json.loads((source_plugin / "plugin.json").read_text())
    if upstream.get("$schema") != verify.PLUGIN_SCHEMA or upstream.get("version") != "0.1.3":
        raise ValueError("Stripe official Agent Plugins manifest changed")
    verify.manifest(plugin, name="stripe", version="0.1.3-ghast.1", revision=REVISION)
    count = verify.compare_trees(source_plugin / "skills", plugin / "skills", ignore_skill_frontmatter=False)
    if count != 32 or len(list((plugin / "skills").rglob("SKILL.md"))) != 8:
        raise ValueError("Stripe skill inventory changed")
    if json.loads((source_plugin / "mcp.json").read_text()) != json.loads((plugin / "mcp.json").read_text()):
        raise ValueError("Stripe official MCP declaration differs")
    status, headers, _ = verify.curl_json(MCP_URL, payload=verify.initialize_payload())
    if status != 401 or "oauth-protected-resource" not in headers.lower():
        raise ValueError(f"unexpected Stripe MCP boundary: HTTP {status}")
    status, _, resource = verify.curl_json(f"{MCP_URL}/.well-known/oauth-protected-resource")
    if status != 200 or not isinstance(resource, dict) or resource.get("authorization_servers") != ["https://access.stripe.com/mcp"]:
        raise ValueError("Stripe protected-resource metadata changed")
    status, _, oauth = verify.curl_json(f"{MCP_URL}/.well-known/oauth-authorization-server")
    if status != 200 or not isinstance(oauth, dict) or oauth.get("registration_endpoint") != "https://access.stripe.com/mcp/oauth2/register" or "S256" not in oauth.get("code_challenge_methods_supported", []):
        raise ValueError("Stripe dynamic OAuth/PKCE metadata changed")
    print("verified Stripe official Agent Plugins 1.0 package, 8 skills/32 files, hosted MCP, dynamic OAuth S256, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
