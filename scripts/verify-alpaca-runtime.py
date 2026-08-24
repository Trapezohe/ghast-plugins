#!/usr/bin/env python3
"""Verify Alpaca's hosted MCP contract and open-source no-credential core."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import official_plugin_verification as verify

AGENTIC_REVISION = "a97b49ecdf47b6b46d8fc1027139c475296dc696"
SERVER_REVISION = "803b07a31721033aa21110c31d14be25cb23882c"
EXPECTED_ENDPOINTS = {
    "alpaca-trading": "https://api.alpaca.markets/mcp",
    "alpaca-trading-paper": "https://paper-api.alpaca.markets/mcp",
    "alpaca-market-data": "https://data.alpaca.markets/mcp",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        required=True,
        help="Directory containing alpaca-agentic and alpaca-mcp-server checkouts.",
    )
    parser.add_argument(
        "--python",
        type=Path,
        required=True,
        help="Python from an environment with the official dev dependencies.",
    )
    parser.add_argument(
        "--plugin",
        type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/alpaca",
    )
    args = parser.parse_args()
    source_root = args.source_root.resolve()
    agentic = source_root / "alpaca-agentic"
    server = source_root / "alpaca-mcp-server"
    plugin = args.plugin.resolve()
    # Preserve the virtual-environment symlink instead of resolving it to the
    # base interpreter, which would discard the environment's site-packages.
    python = args.python.expanduser().absolute()
    if not python.is_file():
        raise ValueError(f"Alpaca verification Python is missing: {python}")

    imp = verify.load_importer()
    if imp.git_revision(agentic) != AGENTIC_REVISION:
        raise ValueError("Alpaca agentic revision changed")
    if imp.git_revision(server) != SERVER_REVISION:
        raise ValueError("Alpaca MCP server revision changed")
    imp.verify_alpaca_evidence(agentic)

    manifest = verify.manifest(
        plugin,
        name="alpaca",
        version="0.1.0-ghast.1",
        revision=AGENTIC_REVISION,
    )
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    extensions = ghast.get("mcpServerExtensions", {})
    mcp = json.loads((plugin / "mcp.json").read_text())
    servers = mcp.get("mcpServers", {})
    if servers.keys() != EXPECTED_ENDPOINTS.keys():
        raise ValueError("Alpaca packaged MCP inventory changed")
    for name, endpoint in EXPECTED_ENDPOINTS.items():
        if servers[name] != {"type": "streamable-http", "url": endpoint}:
            raise ValueError(f"Alpaca packaged endpoint changed: {name}")
        if extensions.get(name, {}).get("oauth", {}).get("client_id") != (
            "PCIEJZTPCQEBUBAINMQOGDHF7I"
        ):
            raise ValueError(f"Alpaca public OAuth client changed: {name}")

    tests = [
        "tests/test_integrity.py",
        "tests/test_server_construction.py",
        "tests/test_prompt_injection_envelope.py",
        "tests/test_trust_boundary_middleware.py",
    ]
    result = subprocess.run(
        [str(python), "-m", "pytest", *tests, "-q"],
        cwd=server,
        check=True,
        text=True,
        capture_output=True,
    )
    if "40 passed" not in result.stdout:
        raise ValueError("Alpaca no-credential test count changed")

    print(
        "verified Alpaca official three-endpoint OAuth contract, 74-tool "
        "open-source server, 40 no-credential core tests, Agent Plugins "
        "1.0, and official icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
