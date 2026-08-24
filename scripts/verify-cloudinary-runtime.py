#!/usr/bin/env python3
"""Verify Cloudinary's five official hosted MCP authentication contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import official_plugin_verification as verify

REVISION = "dca5790c0af2bcde291d732af05c47ad7f75d341"
OAUTH_SERVERS = {
    "cloudinary-asset-management": (
        "https://asset-management.mcp.cloudinary.com/mcp",
        {"asset_management", "upload", "media_generation"},
    ),
    "cloudinary-environment-config": (
        "https://environment-config.mcp.cloudinary.com/mcp",
        {"asset_management", "upload"},
    ),
    "cloudinary-structured-metadata": (
        "https://structured-metadata.mcp.cloudinary.com/mcp",
        {"asset_management", "upload"},
    ),
    "cloudinary-analysis": (
        "https://analysis.mcp.cloudinary.com/mcp",
        {"media_analysis", "query_analysis_tasks"},
    ),
}
MEDIAFLOWS_NAME = "cloudinary-mediaflows"
MEDIAFLOWS_URL = "https://mediaflows.mcp.cloudinary.com/v2/mcp"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--plugin",
        type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/cloudinary",
    )
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(
        source
    ) != imp.normalized_repository_url("https://github.com/cloudinary/mcp-servers"):
        raise ValueError("Cloudinary official source changed")
    readme = (source / "README.md").read_text()
    for marker in (
        "https://asset-management.mcp.cloudinary.com/mcp",
        "https://environment-config.mcp.cloudinary.com/mcp",
        "https://structured-metadata.mcp.cloudinary.com/mcp",
        "https://analysis.mcp.cloudinary.com/sse",
        "https://mediaflows.mcp.cloudinary.com/v2/mcp",
        "`/mcp` (Streamable HTTP, recommended, stateless)",
        '"cld-cloud-name": "cloud_name"',
        '"cld-api-key": "api_key"',
        '"cld-secret": "api_secret"',
    ):
        if marker not in readme:
            raise ValueError(f"Cloudinary official documentation lost {marker!r}")

    manifest = verify.manifest(
        plugin,
        name="cloudinary",
        version="1.0.0-ghast.1",
        revision=REVISION,
    )
    mcp = json.loads((plugin / "mcp.json").read_text())
    servers = mcp.get("mcpServers", {})
    expected_names = {*OAUTH_SERVERS, MEDIAFLOWS_NAME}
    if servers.keys() != expected_names:
        raise ValueError("Cloudinary packaged server inventory changed")
    for name, (url, _) in OAUTH_SERVERS.items():
        if servers[name] != {"type": "streamable-http", "url": url}:
            raise ValueError(f"Cloudinary packaged endpoint changed: {name}")
    if servers[MEDIAFLOWS_NAME] != {
        "type": "streamable-http",
        "url": MEDIAFLOWS_URL,
    }:
        raise ValueError("Cloudinary MediaFlows endpoint changed")
    credentials = (
        manifest["extensions"]["ai.trapezohe.ghast"]
        .get("mcpServerExtensions", {})
        .get(MEDIAFLOWS_NAME, {})
        .get("credentialHeaders", {})
    )
    if credentials != {
        "cld-cloud-name": "$VAULT:cloudinary-cloud-name",
        "cld-api-key": "$VAULT:cloudinary-api-key",
        "cld-secret": "$VAULT:cloudinary-api-secret",
    }:
        raise ValueError("Cloudinary MediaFlows Vault binding changed")

    for name, (url, required_scopes) in OAUTH_SERVERS.items():
        status, _, body = verify.curl_json(url, payload=verify.initialize_payload())
        if status != 401 or not isinstance(body, dict) or body.get("error") not in {"unauthorized", "invalid_token"}:
            raise ValueError(f"unexpected Cloudinary MCP boundary for {name}: HTTP {status}")
        host = url.split("/mcp", 1)[0]
        status, _, resource = verify.curl_json(
            f"{host}/.well-known/oauth-protected-resource"
        )
        if status != 200 or not isinstance(resource, dict) or not required_scopes.issubset(resource.get("scopes_supported", [])):
            raise ValueError(f"Cloudinary protected-resource scopes changed: {name}")
        status, _, oauth = verify.curl_json(
            f"{host}/.well-known/oauth-authorization-server"
        )
        if status != 200 or not isinstance(oauth, dict) or oauth.get("registration_endpoint") != f"{host}/register" or "S256" not in oauth.get("code_challenge_methods_supported", []) or "refresh_token" not in oauth.get("grant_types_supported", []) or "none" not in oauth.get("token_endpoint_auth_methods_supported", []):
            raise ValueError(f"Cloudinary OAuth metadata changed: {name}")

    status, _, body = verify.curl_json(
        MEDIAFLOWS_URL,
        payload=verify.initialize_payload(),
    )
    if status != 401 or not isinstance(body, dict) or body.get("error") != "invalid_token":
        raise ValueError(f"unexpected Cloudinary MediaFlows boundary: HTTP {status}")
    status, _, _ = verify.curl_json(
        "https://mediaflows.mcp.cloudinary.com/.well-known/oauth-protected-resource"
    )
    if status != 404:
        raise ValueError("Cloudinary MediaFlows now publishes OAuth metadata; re-audit")

    print(
        "verified Cloudinary 5-server official suite, 4 dynamic OAuth S256 "
        "contracts, MediaFlows Vault headers, auth boundaries, Agent Plugins "
        "1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
