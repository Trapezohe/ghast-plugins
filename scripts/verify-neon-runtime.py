#!/usr/bin/env python3
"""Verify Neon's pinned official Agent Plugins package and CI."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import tarfile
import tempfile
from pathlib import Path
from types import ModuleType

EXPECTED_REVISION = "b7f87949583782238aef20414a29b1f5ca2773ea"
EXPECTED_VERSION = "1.1.2"
EXPECTED_SKILLS = 8
EXPECTED_FILES = 13
MCP_URL = "https://mcp.neon.tech/mcp"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/neon-postgres")
    parser.add_argument("--node", type=Path, required=True, help="Official CI-compatible Node 20 binary")
    parser.add_argument("--npm", type=Path, required=True, help="Official CI-compatible npm 10 executable")
    return parser.parse_args()


def importer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ghast_importer", IMPORTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load official importer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, text=True, **kwargs)


def files(root: Path) -> dict[str, Path]:
    return {p.relative_to(root).as_posix(): p for p in root.rglob("*") if p.is_file()}


def verify_ci(source: Path, node: Path, npm: Path) -> None:
    node_version = run([str(node), "--version"], capture_output=True).stdout.strip()
    if not node_version.startswith("v20."):
        raise ValueError(f"Neon CI requires Node 20, found {node_version}")
    with tempfile.TemporaryDirectory(prefix="ghast-neon-ci-") as temp:
        root = Path(temp)
        archive, checkout, binary = root / "source.tar", root / "source", root / "bin"
        checkout.mkdir(); binary.mkdir()
        run(["git", "archive", "--output", str(archive), EXPECTED_REVISION], cwd=source)
        with tarfile.open(archive) as package:
            package.extractall(checkout, filter="data")
        (binary / "node").symlink_to(node.resolve())
        (binary / "npm").symlink_to(npm.resolve())
        environment = os.environ.copy()
        environment["PATH"] = os.pathsep.join([str(binary), environment["PATH"]])
        npm_version = run([str(binary / "npm"), "--version"], env=environment, capture_output=True).stdout.strip()
        if not npm_version.startswith("10."):
            raise ValueError(f"Neon CI requires npm 10, found {npm_version}")
        run([str(binary / "npm"), "ci", "--ignore-scripts"], cwd=checkout, env=environment)
        validation = run([str(binary / "npm"), "run", "validate:ci"], cwd=checkout, env=environment, capture_output=True)
        output = validation.stdout + validation.stderr
        for marker in ("Agent Plugins v1.0.0 validation passed", "Plugin skills are in sync", "Versions are in sync at 1.1.2", "All 8 skill(s) have a fully-linked reference graph"):
            if marker not in output:
                raise ValueError(f"Neon official validation omitted: {marker}")
        audit = subprocess.run([str(binary / "npm"), "audit", "--json"], cwd=checkout, env=environment, text=True, capture_output=True)
        report = json.loads(audit.stdout)
        vulnerabilities = report.get("vulnerabilities", {})
        js_yaml = vulnerabilities.get("js-yaml", {})
        if report.get("metadata", {}).get("vulnerabilities", {}).get("high") != 1 or js_yaml.get("isDirect") is not False:
            raise ValueError("Neon validation dependency audit changed; re-audit required")


def main() -> int:
    parsed = args()
    source, plugin = parsed.source.resolve(), parsed.plugin.resolve()
    imp = importer()
    if imp.git_revision(source) != EXPECTED_REVISION or imp.normalized_git_remote(source) != imp.normalized_repository_url("https://github.com/neondatabase/agent-skills"):
        raise ValueError("Neon official source changed")
    upstream = json.loads((source / "plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION or manifest.get("version") != f"{EXPECTED_VERSION}-ghast.1" or manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("unexpected Neon Agent Plugins 1.0 manifest")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION or not (plugin / ghast["icon"].removeprefix("./")).is_file():
        raise ValueError("Neon revision or icon differs")
    if mcp["mcpServers"]["neon"].get("url") != MCP_URL:
        raise ValueError("Neon MCP endpoint changed")
    with tempfile.TemporaryDirectory(prefix="ghast-neon-output-") as temp:
        expected_root = Path(temp) / "skills"
        imp.copy_skill_tree(source / "skills", expected_root, recursive=False, preserve_agent_metadata=False, frontmatter_overrides={})
        expected, actual = files(expected_root), files(plugin / "skills")
        if expected.keys() != actual.keys() or len(expected) != EXPECTED_FILES:
            raise ValueError("Neon skill file sets differ")
        for name, path in expected.items():
            if path.read_bytes() != actual[name].read_bytes():
                raise ValueError(f"Neon output differs: {name}")
    verify_ci(source, parsed.node, parsed.npm)
    with tempfile.TemporaryDirectory(prefix="ghast-neon-http-") as temp:
        headers, body = Path(temp) / "headers", Path(temp) / "body"
        result = run(["curl", "-sS", "-D", str(headers), "-o", str(body), "-w", "%{http_code}", "-X", "POST", "-H", "Content-Type: application/json", "-H", "Accept: application/json, text/event-stream", "--data", '{"jsonrpc":"2.0","id":1,"method":"tools/list"}', MCP_URL], capture_output=True)
        if result.stdout != "401" or "oauth-protected-resource" not in headers.read_text().lower():
            raise ValueError(f"unexpected Neon MCP boundary: HTTP {result.stdout}")
        metadata = json.loads(run(["curl", "-sS", "https://mcp.neon.tech/.well-known/oauth-authorization-server"], capture_output=True).stdout)
        if metadata.get("registration_endpoint") != "https://mcp.neon.tech/api/register" or "S256" not in metadata.get("code_challenge_methods_supported", []):
            raise ValueError("Neon dynamic OAuth/PKCE metadata changed")
    print("verified Neon 1.1.2 official 8-skill, 13-file tree, Node 20/npm 10 validate:ci, known validation-only js-yaml advisory, dynamic OAuth boundary, Agent Plugins 1.0, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
