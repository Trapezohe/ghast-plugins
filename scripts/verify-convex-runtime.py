#!/usr/bin/env python3
"""Verify Convex's licensed official npm runtime and Ghast adapter."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
from pathlib import Path

import official_plugin_verification as verify

IMPORTER = verify.REPOSITORY_ROOT / "scripts/import-convex-plugin.py"
REVISION = "convex-npm-1.44.0-8bdb320a17ed+icon-7023eb599ffe+tools-5d3be1fb3d20"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--icon-source", type=Path, required=True)
    parser.add_argument(
        "--plugin",
        type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/convex",
    )
    args = parser.parse_args()
    icon_source, plugin = args.icon_source.resolve(), args.plugin.resolve()
    spec = importlib.util.spec_from_file_location("ghast_convex_importer", IMPORTER)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Convex importer")
    importer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(importer)

    importer.verify_official_sources(icon_source)
    importer.verify_mcp()
    manifest = verify.manifest(
        plugin,
        name="convex",
        version=None,
        revision=REVISION,
    )
    if manifest.get("license") != "Apache-2.0 AND MIT":
        raise ValueError("Convex adapter license boundary changed")
    mcp = json.loads((plugin / "mcp.json").read_text())
    server = mcp["mcpServers"]["convex"]
    if server != {
        "type": "stdio",
        "command": "npx",
        "args": ["--yes", "convex@1.44.0", "mcp", "start"],
    }:
        raise ValueError("Convex packaged MCP command changed")
    joined = " ".join(server["args"])
    for unsafe in (
        "--prod",
        "--cautiously-allow-production-pii",
        "--dangerously-enable-production-deployments",
    ):
        if unsafe in joined:
            raise ValueError(f"Convex launcher unexpectedly enables {unsafe}")
    help_result = subprocess.run(
        ["npx", "--yes", "convex@1.44.0", "ai-files", "--help"],
        cwd="/tmp",
        check=True,
        text=True,
        capture_output=True,
    )
    for command in ("status", "install", "enable", "update", "disable", "remove"):
        if command not in help_result.stdout:
            raise ValueError(f"Convex ai-files command changed: {command}")
    print(
        "verified Convex 1.44.0 official npm hashes, Apache-2.0 runtime, "
        "12-tool MCP schema, project AI-files command family, production-safe "
        "launcher, Agent Plugins 1.0, MIT icon, and package identity"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
