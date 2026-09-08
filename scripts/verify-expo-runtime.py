#!/usr/bin/env python3
"""Verify Expo's pinned official checks, hosted MCP boundary, and Ghast output."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from types import ModuleType


EXPECTED_REVISION = "472d040092900dc8bbf84dc7efb0c90abff77a0d"
EXPECTED_VERSION = "1.12.0"
EXPECTED_SKILLS = 24
BUN_VERSION = "1.3.3"
MCP_URL = "https://mcp.expo.dev/mcp"
RESOURCE_METADATA_URL = "https://mcp.expo.dev/.well-known/oauth-protected-resource/mcp"
AUTH_METADATA_URL = "https://mcp.expo.dev/.well-known/oauth-authorization-server"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/expo")
    parser.add_argument("--bun", type=Path)
    return parser.parse_args()


def run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, **kwargs)


def load_importer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ghast_official_importer", IMPORTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {IMPORTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def resolve_bun(explicit: Path | None) -> Path:
    if explicit is not None:
        binary = explicit.expanduser().resolve()
    elif discovered := shutil.which("bun"):
        binary = Path(discovered).resolve()
    else:
        result = run(
            ["npx", "--yes", f"--package=bun@{BUN_VERSION}", "sh", "-c", "command -v bun"],
            capture_output=True,
        )
        binary = Path(result.stdout.strip()).resolve()
    version = run([str(binary), "--version"], capture_output=True).stdout.strip()
    if version != BUN_VERSION:
        raise ValueError(f"expected Bun {BUN_VERSION}, found {version}")
    return binary


def split_skill(path: Path) -> tuple[str, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError(f"{path}: unterminated frontmatter")
    return text[4:closing], text[closing + 5 :]


def file_map(root: Path) -> dict[str, Path]:
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }


def verify_skill_tree(source: Path, plugin: Path) -> None:
    importer = load_importer()
    with tempfile.TemporaryDirectory(prefix="ghast-expo-output-") as temp:
        expected_root = Path(temp) / "skills"
        importer.copy_skill_tree(
            source / "plugins/expo/skills",
            expected_root,
            recursive=False,
            preserve_agent_metadata=False,
            frontmatter_overrides={},
        )
        staging = expected_root.parent
        importer.apply_ghast_compatibility("expo", staging)
        expected = file_map(expected_root)
        actual = file_map(plugin / "skills")
        if expected.keys() != actual.keys():
            raise ValueError("Expo source and Ghast skill file sets differ")
        count = sum(name.endswith("/SKILL.md") for name in expected)
        if count != EXPECTED_SKILLS:
            raise ValueError(f"expected {EXPECTED_SKILLS} Expo skills, found {count}")
        for relative, expected_path in expected.items():
            actual_path = actual[relative]
            if relative.endswith("/SKILL.md"):
                _, expected_body = split_skill(expected_path)
                _, actual_body = split_skill(actual_path)
                if expected_body.lstrip("\r\n") != actual_body.lstrip("\r\n"):
                    raise ValueError(f"{relative}: body differs from official source")
            elif expected_path.read_bytes() != actual_path.read_bytes():
                raise ValueError(f"{relative}: file differs from official source")


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "ghast-audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read())


def verify_mcp_auth_boundary() -> None:
    body = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "ghast-audit", "version": "1.0"},
            },
        }
    ).encode()
    request = urllib.request.Request(
        MCP_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "ghast-audit/1.0",
        },
        method="POST",
    )
    try:
        urllib.request.urlopen(request, timeout=60)
    except urllib.error.HTTPError as error:
        challenge = error.headers.get("WWW-Authenticate", "")
        if error.code != 401 or RESOURCE_METADATA_URL not in challenge:
            raise ValueError(f"unexpected Expo MCP auth boundary: HTTP {error.code}")
    else:
        raise ValueError("Expo MCP accepted an anonymous initialize request")

    resource = fetch_json(RESOURCE_METADATA_URL)
    authorization = fetch_json(AUTH_METADATA_URL)
    if resource.get("resource") != MCP_URL or resource.get("scopes_supported") != ["mcp:access"]:
        raise ValueError("Expo protected-resource metadata changed")
    if authorization.get("issuer") != "https://mcp.expo.dev":
        raise ValueError("Expo authorization issuer changed")
    if "S256" not in authorization.get("code_challenge_methods_supported", []):
        raise ValueError("Expo authorization metadata no longer advertises PKCE S256")
    if not {"authorization_code", "refresh_token"}.issubset(
        authorization.get("grant_types_supported", [])
    ):
        raise ValueError("Expo authorization grants changed")


def verify_official_checks(source: Path, bun: Path) -> None:
    commands = (
        [str(bun), "test", "scripts/check-plugin-version-bump.test.ts"],
        [str(bun), "scripts/check-skill-limits.ts"],
        [str(bun), "scripts/check-plugin-version-bump.ts", "origin/main"],
        [str(bun), "scripts/check-overview-routing.ts"],
    )
    with tempfile.TemporaryDirectory(prefix="ghast-expo-tools-") as temp:
        tool_bin = Path(temp) / "bin"
        tool_bin.mkdir()
        (tool_bin / "bun").symlink_to(bun)
        environment = os.environ.copy()
        environment["PATH"] = os.pathsep.join([str(tool_bin), environment["PATH"]])
        for command in commands:
            run(command, cwd=source, env=environment)


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    revision = run(
        ["git", "rev-parse", "HEAD"], cwd=source, capture_output=True
    ).stdout.strip()
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")
    if run(["git", "status", "--porcelain"], cwd=source, capture_output=True).stdout:
        raise ValueError("Expo source checkout is not clean")

    upstream = json.loads((source / "plugins/expo/.codex-plugin/plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION:
        raise ValueError("official Expo version changed")
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("Expo is not Agent Plugins 1.0")
    if manifest.get("version") != '1.12.0':
        raise ValueError("unexpected Ghast Expo version")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("Expo manifest revision differs from source")
    if mcp.get("$schema") != MCP_SCHEMA:
        raise ValueError("Expo MCP declaration is not Agent Plugins 1.0")
    if mcp.get("mcpServers", {}).get("expo", {}).get("url") != MCP_URL:
        raise ValueError("Expo MCP URL changed")
    if not (plugin / "assets/icon.png").is_file():
        raise ValueError("Expo icon is missing")

    verify_skill_tree(source, plugin)
    verify_official_checks(source, resolve_bun(args.bun))
    verify_mcp_auth_boundary()
    print(
        "verified Expo 1.12.0 official 24-skill tree, 4 CI checks, hosted MCP OAuth "
        "boundary, Agent Plugins 1.0 manifests, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
