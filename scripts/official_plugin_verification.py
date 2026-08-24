#!/usr/bin/env python3
"""Shared checks for pinned official plugin ports."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path
from types import ModuleType

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def load_importer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ghast_importer", IMPORTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load official importer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def file_map(root: Path) -> dict[str, Path]:
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file()
    }


def skill_body(data: bytes) -> bytes:
    if not data.startswith(b"---\n"):
        return data
    end = data.find(b"\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated skill frontmatter")
    return data[end + 5 :].lstrip(b"\n")


def compare_trees(expected: Path, actual: Path, *, ignore_skill_frontmatter: bool) -> int:
    expected_files, actual_files = file_map(expected), file_map(actual)
    if expected_files.keys() != actual_files.keys():
        missing = sorted(expected_files.keys() - actual_files.keys())
        extra = sorted(actual_files.keys() - expected_files.keys())
        raise ValueError(f"file sets differ; missing={missing}, extra={extra}")
    for name, expected_path in expected_files.items():
        expected_data = expected_path.read_bytes()
        actual_data = actual_files[name].read_bytes()
        if ignore_skill_frontmatter and name.endswith("/SKILL.md"):
            expected_data, actual_data = skill_body(expected_data), skill_body(actual_data)
        if expected_data != actual_data:
            raise ValueError(f"official output differs: {name}")
    return len(expected_files)


def manifest(plugin: Path, *, name: str, version: str, revision: str) -> dict:
    value = json.loads((plugin / "plugin.json").read_text())
    if value.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError(f"{name}: Agent Plugins schema differs")
    if value.get("name") != name or value.get("version") != version:
        raise ValueError(f"{name}: manifest identity differs")
    ghast = value.get("extensions", {}).get("ai.trapezohe.ghast", {})
    if ghast.get("upstreamRevision") != revision:
        raise ValueError(f"{name}: upstream revision differs")
    icon = plugin / ghast.get("icon", "").removeprefix("./")
    if not icon.is_file() or icon.stat().st_size == 0:
        raise ValueError(f"{name}: icon is missing")
    return value


def curl_json(url: str, *, payload: dict | None = None) -> tuple[int, str, object]:
    with tempfile.TemporaryDirectory(prefix="ghast-official-http-") as temp:
        headers, body = Path(temp) / "headers", Path(temp) / "body"
        command = [
            "curl", "-sS", "--max-time", "30", "-D", str(headers),
            "-o", str(body), "-w", "%{http_code}",
        ]
        if payload is not None:
            command += [
                "-X", "POST", "-H", "Content-Type: application/json",
                "-H", "Accept: application/json, text/event-stream",
                "--data", json.dumps(payload, separators=(",", ":")),
            ]
        result = subprocess.run(
            command + [url], check=True, text=True, capture_output=True
        )
        raw = body.read_text()
        try:
            parsed: object = json.loads(raw)
        except json.JSONDecodeError:
            parsed = raw
        return int(result.stdout), headers.read_text(), parsed


def initialize_payload() -> dict:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "ghast-audit", "version": "1.0"},
        },
    }


def tools_list_payload() -> dict:
    return {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
