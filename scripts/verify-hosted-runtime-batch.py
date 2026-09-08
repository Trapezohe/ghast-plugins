#!/usr/bin/env python3
"""Verify six official hosted MCP ports and their recorded runtime boundary."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import official_plugin_verification as verify

HOSTED_IMPORTER = verify.REPOSITORY_ROOT / "scripts/import-official-hosted-plugins.py"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"

PLUGINS = {
    "cogedim": {
        "version": None,
        "revision": (
            "cogedim-mcp-69802ca971dc+llms-3bd622452f97+"
            "init-ec7893b3a416+tools-6351b9900840"
        ),
        "url": "https://www.cogedim.com/mcp",
        "verify": "verify_cogedim_evidence",
    },
    "quartr": {
        "version": None,
        "revision": "quartr-docs-b37a9c381ded+oauth-a379a77612f2",
        "url": "https://mcp.quartr.com/mcp",
        "verify": "verify_quartr_evidence",
    },
    "read-ai": {
        "version": None,
        "revision": (
            "zendesk-49381158409491-2026-08-19T23:57:53Z-"
            "0050b9f9a3b3"
        ),
        "url": "https://api.read.ai/mcp",
        "verify": "verify_read_ai_evidence",
    },
    "semrush": {
        "version": None,
        "revision": "semrush-docs-e34fd6ac1924+oauth-5d0b459a41d7",
        "url": "https://mcp.semrush.com/v2/mcp",
        "verify": "verify_semrush_evidence",
    },
    "similarweb": {
        "version": None,
        "revision": (
            "similarweb-docs-eac1d71df335+claude-aa84c3a66647+"
            "oauth-4f4e48ae9c75"
        ),
        "url": "https://mcp.similarweb.com",
        "verify": "verify_similarweb_evidence",
    },
    "skywatch": {
        "version": None,
        "revision": (
            "skywatch-docs-f4ed1fbadb7c+client-a16e47fecde3+"
            "tools-c6b9fe481f16"
        ),
        "url": "https://api.skywatch.co/mcp",
        "verify": "verify_skywatch_evidence",
    },
}


def load_hosted_importer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ghast_hosted_importer", HOSTED_IMPORTER)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load hosted plugin importer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_plugin(name: str, expected: dict, hosted: ModuleType) -> None:
    plugin = verify.REPOSITORY_ROOT / "plugins" / name
    verify.manifest(
        plugin,
        name=name,
        version=expected["version"],
        revision=expected["revision"],
    )
    mcp = json.loads((plugin / "mcp.json").read_text())
    if mcp.get("$schema") != MCP_SCHEMA:
        raise ValueError(f"{name}: Agent Plugins MCP schema differs")
    servers = mcp.get("mcpServers", {})
    if servers != {
        name: {"type": "streamable-http", "url": expected["url"]}
    }:
        raise ValueError(f"{name}: hosted MCP declaration differs")
    getattr(hosted, expected["verify"])()


def main() -> int:
    hosted = load_hosted_importer()
    for name, expected in PLUGINS.items():
        verify_plugin(name, expected, hosted)
        print(f"verified {name} official evidence and packaged contract")
    print(
        "verified 6 official hosted MCP ports; Cogedim and SkyWatch include "
        "live anonymous core calls, while Quartr, Read AI, Semrush, and "
        "Similarweb stop at their live authentication boundaries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
