#!/usr/bin/env python3
"""Verify Figma's official MCP surface and independent-client blocker."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


sys.dont_write_bytecode = True

OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
OFFICIAL_REVISION = "72fcf1f4b170bcaa78fa8bef2f27cce15f4d58f4"
OFFICIAL_TREE = "15eabd7564b5c30511c0e25281def746b0b172c8"
OFFICIAL_INVENTORY_SHA256 = (
    "cea948ec79d7c1c1002be48639568abd426d7ad32d72fdb51911353c36753309"
)
MCP_URL = "https://mcp.figma.com/mcp"
PROTECTED_RESOURCE_URL = (
    "https://mcp.figma.com/.well-known/oauth-protected-resource/mcp"
)
PROTECTED_RESOURCE_SHA256 = (
    "adaf46086cfbe6f836da39563f63ead46ea144d4dc507b72766c9694f71eb93a"
)
AUTHORIZATION_SERVER_URL = (
    "https://mcp.figma.com/.well-known/oauth-authorization-server"
)
AUTHORIZATION_SERVER_SHA256 = (
    "dc715479f1f4a13741cb9ae3d6a99b45433a807de9cc026a7fbf60644d0b2929"
)
REMOTE_INSTALL_URL = (
    "https://developers.figma.com/docs/figma-mcp-server/"
    "remote-server-installation/"
)
TOOLS_URL = "https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/"
DEVELOPER_TERMS_URL = "https://www.figma.com/legal/developer-terms/"

SKILLS = (
    "figma-code-connect",
    "figma-create-new-file",
    "figma-design-to-code",
    "figma-generate-design",
    "figma-generate-diagram",
    "figma-generate-library",
    "figma-implement-motion",
    "figma-swiftui",
    "figma-use",
    "figma-use-figjam",
    "figma-use-motion",
    "figma-use-slides",
)

TOOLS = (
    "add_code_connect_map",
    "create_new_file",
    "download_assets",
    "generate_diagram",
    "generate_figma_design",
    "get_code_connect_map",
    "get_code_connect_suggestions",
    "get_context_for_code_connect",
    "get_design_context",
    "get_figjam",
    "get_libraries",
    "get_metadata",
    "get_motion_context",
    "get_screenshot",
    "get_shader_effect",
    "get_shader_fill",
    "get_variable_defs",
    "list_shader_effects",
    "list_shader_fills",
    "search_design_system",
    "send_code_connect_mappings",
    "upload_assets",
    "use_figma",
    "whoami",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--openai-source", type=Path, required=True)
    parser.add_argument("--official-source", type=Path, required=True)
    return parser.parse_args()


def run(*args: str, cwd: Path) -> bytes:
    return subprocess.check_output(args, cwd=cwd)


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    return sha256(encoded)


def fetch(url: str, accept: str = "*/*") -> bytes:
    request = urllib.request.Request(
        url,
        headers={"Accept": accept, "User-Agent": "ghast-figma-audit/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def verify_official_source(source: Path) -> None:
    revision = run("git", "rev-parse", "HEAD", cwd=source).decode().strip()
    tree = run("git", "rev-parse", "HEAD^{tree}", cwd=source).decode().strip()
    inventory = run(
        "git", "ls-tree", "-r", "--full-tree", "HEAD", cwd=source
    )
    if revision != OFFICIAL_REVISION or tree != OFFICIAL_TREE:
        raise ValueError("Figma official source revision changed")
    if sha256(inventory) != OFFICIAL_INVENTORY_SHA256:
        raise ValueError("Figma official source inventory changed")

    license_names = {
        "license",
        "license.txt",
        "license.md",
        "licence",
        "copying",
        "notice",
    }
    tracked = run(
        "git", "ls-tree", "-r", "--name-only", "HEAD", cwd=source
    ).decode().splitlines()
    found_licenses = [
        path for path in tracked if Path(path).name.lower() in license_names
    ]
    if found_licenses:
        raise ValueError(
            "Figma official source now contains license-like files; re-audit: "
            + ", ".join(found_licenses)
        )

    skills = sorted(
        path.split("/")[1]
        for path in tracked
        if path.startswith("skills/") and path.endswith("/SKILL.md")
    )
    if tuple(skills) != SKILLS:
        raise ValueError("Figma official skill inventory changed")

    readme = (source / "README.md").read_text()
    for marker in (
        MCP_URL,
        "Write to the canvas",
        "Generate code from selected frames",
        "Extract design context",
        "Code Connect",
        "Figma Developer Terms",
        "Beta feature",
    ):
        if marker not in readme:
            raise ValueError(f"Figma official README is missing {marker!r}")


def verify_live_surface() -> None:
    protected_resource = json.loads(fetch(PROTECTED_RESOURCE_URL))
    authorization_server = json.loads(fetch(AUTHORIZATION_SERVER_URL))
    if (
        canonical_json_sha256(protected_resource)
        != PROTECTED_RESOURCE_SHA256
        or protected_resource.get("resource") != MCP_URL
        or protected_resource.get("authorization_servers")
        != ["https://api.figma.com"]
        or protected_resource.get("scopes_supported") != ["mcp:connect"]
    ):
        raise ValueError("Figma protected-resource metadata changed")
    if (
        canonical_json_sha256(authorization_server)
        != AUTHORIZATION_SERVER_SHA256
        or authorization_server.get("registration_endpoint")
        != "https://api.figma.com/v1/oauth/mcp/register"
        or authorization_server.get("code_challenge_methods_supported")
        != ["S256"]
        or authorization_server.get("scopes_supported") != ["mcp:connect"]
    ):
        raise ValueError("Figma authorization-server metadata changed")

    request = urllib.request.Request(
        MCP_URL,
        data=json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "ghast-figma-audit", "version": "1"},
                },
            }
        ).encode(),
        headers={
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
            "User-Agent": "ghast-figma-audit/1.0",
        },
        method="POST",
    )
    try:
        urllib.request.urlopen(request, timeout=60)
    except urllib.error.HTTPError as exc:
        if exc.code != 401 or "resource_metadata=" not in (
            exc.headers.get("WWW-Authenticate") or ""
        ):
            raise ValueError("Figma unauthenticated MCP behavior changed") from exc
    else:
        raise ValueError("Figma MCP no longer requires authentication")

    tools_page = fetch(TOOLS_URL, "text/html").decode("utf-8", "replace")
    missing_tools = [tool for tool in TOOLS if tool not in tools_page]
    if missing_tools:
        raise ValueError("Figma tool documentation changed: " + ", ".join(missing_tools))

    install_page = fetch(REMOTE_INSTALL_URL, "text/html").decode(
        "utf-8", "replace"
    )
    for marker in (
        "Only clients listed in the",
        "MCP Catalog",
        "can connect to the Figma MCP Server",
        "join the waitlist",
        "codex mcp add figma --url https://mcp.figma.com/mcp",
    ):
        if marker not in install_page:
            raise ValueError(f"Figma client-onboarding guidance is missing {marker!r}")

    terms = fetch(DEVELOPER_TERMS_URL, "text/html").decode("utf-8", "replace")
    for marker in (
        "Effective Date",
        "May 5, 2026",
        "Model Context Protocol servers",
        "develop, test, and support an integration",
        "All rights not expressly granted are reserved",
    ):
        if marker not in terms:
            raise ValueError(f"Figma Developer Terms are missing {marker!r}")


def verify_openai_snapshot(source: Path) -> None:
    revision = run("git", "rev-parse", "HEAD", cwd=source).decode().strip()
    if revision != OPENAI_REVISION:
        raise ValueError("OpenAI plugin source revision changed")
    plugin = source / "plugins" / "figma"
    manifest = json.loads((plugin / ".codex-plugin" / "plugin.json").read_text())
    mcp = json.loads((plugin / ".mcp.json").read_text())
    if (
        manifest.get("name") != "figma"
        or manifest.get("author", {}).get("name") != "Figma"
        or manifest.get("license") != "LicenseRef-Figma-Developer-Terms"
        or mcp.get("mcpServers", {}).get("figma", {}).get("url") != MCP_URL
    ):
        raise ValueError("OpenAI Figma plugin identity changed")
    license_text = (plugin / "LICENSE.txt").read_text()
    if "governed by the Figma Developer Terms" not in license_text:
        raise ValueError("OpenAI Figma material-license evidence changed")
    skills = sorted(path.parent.name for path in (plugin / "skills").glob("*/SKILL.md"))
    if tuple(skills) != SKILLS:
        raise ValueError("OpenAI Figma skill inventory changed")


def main() -> int:
    args = parse_args()
    verify_official_source(args.official_source)
    verify_live_surface()
    verify_openai_snapshot(args.openai_source)
    if Path("plugins/figma").exists() or Path("packages/figma.zip").exists():
        raise ValueError(
            "Figma must remain unpublished until Ghast receives independent-client "
            "access and uses independently authored workflows and artwork"
        )
    print("verified Figma official MCP, licensing, and client-onboarding blockers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
