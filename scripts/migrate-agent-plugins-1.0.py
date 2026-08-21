#!/usr/bin/env python3
"""Migrate Ghast plugin sources to the Agent Plugins 1.0.0 layout."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
GHAST_NAMESPACE = "ai.trapezohe.ghast"
PORTABLE_FIELDS = (
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
)
DISCOVERY_FIELDS = {"skills", "mcpServers"}
SENSITIVE_HEADER_MARKERS = (
    "authorization",
    "api-key",
    "apikey",
    "access-token",
    "token",
    "secret",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugins", type=Path, default=Path("plugins"))
    args = parser.parse_args()

    migrated = 0
    for plugin_dir in sorted(path for path in args.plugins.iterdir() if path.is_dir()):
        legacy_manifest = plugin_dir / ".ghast-plugin/plugin.json"
        portable_manifest = plugin_dir / "plugin.json"
        if legacy_manifest.is_file():
            migrate_plugin(plugin_dir, legacy_manifest)
            migrated += 1
        elif not portable_manifest.is_file():
            raise ValueError(f"{plugin_dir}: missing plugin manifest")

    print(f"migrated {migrated} plugins to Agent Plugins 1.0.0")
    return 0


def migrate_plugin(plugin_dir: Path, legacy_manifest_path: Path) -> None:
    legacy = load_object(legacy_manifest_path)
    if legacy.get("name") != plugin_dir.name:
        raise ValueError(f"{legacy_manifest_path}: name must match directory")

    manifest = {"$schema": PLUGIN_SCHEMA}
    for field in PORTABLE_FIELDS:
        if field in legacy:
            manifest[field] = legacy[field]

    existing_extensions = legacy.get("extensions")
    if existing_extensions is not None and not isinstance(existing_extensions, dict):
        raise ValueError(f"{legacy_manifest_path}: extensions must be an object")
    extensions = dict(existing_extensions or {})
    ghast = dict(extensions.get(GHAST_NAMESPACE) or {})
    for key, value in legacy.items():
        if key in PORTABLE_FIELDS or key in DISCOVERY_FIELDS or key == "extensions":
            continue
        ghast[key] = value

    legacy_mcp_path = plugin_dir / ".mcp.json"
    if legacy_mcp_path.is_file():
        mcp, server_extensions = migrate_mcp(legacy_mcp_path)
        write_json(plugin_dir / "mcp.json", mcp)
        if server_extensions:
            ghast["mcpServerExtensions"] = server_extensions
        legacy_mcp_path.unlink()

    commands_dir = plugin_dir / "commands"
    if commands_dir.is_dir():
        extension_dir = plugin_dir / GHAST_NAMESPACE
        extension_dir.mkdir(exist_ok=True)
        target = extension_dir / "commands"
        if target.exists():
            raise ValueError(f"{target}: extension command directory already exists")
        shutil.move(str(commands_dir), target)
        ghast["commands"] = f"./{GHAST_NAMESPACE}/commands/"

    if ghast:
        extensions[GHAST_NAMESPACE] = ghast
    if extensions:
        manifest["extensions"] = extensions

    write_json(plugin_dir / "plugin.json", manifest)
    shutil.rmtree(plugin_dir / ".ghast-plugin")


def migrate_mcp(path: Path) -> tuple[dict, dict]:
    source = load_object(path)
    raw_servers = source.get("mcpServers")
    if raw_servers is None:
        raw_servers = {
            key: value
            for key, value in source.items()
            if key != "$schema"
        }
    if not isinstance(raw_servers, dict):
        raise ValueError(f"{path}: MCP server map must be an object")

    servers = {}
    extensions = {}
    for name, value in raw_servers.items():
        if not isinstance(value, dict):
            raise ValueError(f"{path}: server {name!r} must be an object")
        raw = dict(value)
        transport = raw.pop("type", None) or raw.pop("transport", None)
        if transport is None:
            transport = "stdio" if "command" in raw else "streamable-http"
        if transport == "http":
            transport = "streamable-http"

        server_extension = {}
        for field in ("oauth", "note"):
            if field in raw:
                server_extension[field] = raw.pop(field)

        if transport == "stdio":
            server = {"type": "stdio", "command": raw.pop("command")}
            for field in ("args", "env", "cwd"):
                if field in raw:
                    value = raw.pop(field)
                    if field == "cwd" and value == ".":
                        value = "./"
                    server[field] = value
        elif transport in {"streamable-http", "sse"}:
            server = {"type": transport, "url": raw.pop("url")}
            headers = raw.pop("headers", None)
            if headers is not None:
                if not isinstance(headers, dict):
                    raise ValueError(f"{path}: server {name!r} headers must be an object")
                literal_headers = {}
                credential_headers = {}
                for header_name, header_value in headers.items():
                    if is_credential_header(header_name, header_value):
                        credential_headers[header_name] = header_value
                    else:
                        literal_headers[header_name] = header_value
                if literal_headers:
                    server["headers"] = literal_headers
                if credential_headers:
                    server_extension["credentialHeaders"] = credential_headers
        else:
            raise ValueError(f"{path}: unsupported MCP transport {transport!r}")

        if raw:
            server_extension["legacyFields"] = raw
        servers[name] = server
        if server_extension:
            extensions[name] = server_extension

    return {"$schema": MCP_SCHEMA, "mcpServers": servers}, extensions


def is_credential_header(name: str, value: object) -> bool:
    lowered = name.lower()
    if any(marker in lowered for marker in SENSITIVE_HEADER_MARKERS):
        return True
    if not isinstance(value, str):
        return True
    return "$VAULT:" in value or "${" in value


def load_object(path: Path) -> dict:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return data


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
