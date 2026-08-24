#!/usr/bin/env python3
"""Verify Supabase's official skill tests, release build, OAuth boundary, and Ghast output."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from types import ModuleType


EXPECTED_REVISION = "8331f910845103c08d51f6ca1d86ebb7d1f745e3"
EXPECTED_VERSION = "0.1.8"
EXPECTED_SKILLS = 2
PNPM_VERSION = "10.33.0"
MCP_URL = "https://mcp.supabase.com/mcp"
RESOURCE_METADATA_URL = "https://mcp.supabase.com/.well-known/oauth-protected-resource/mcp"
AUTH_METADATA_URL = "https://api.supabase.com/.well-known/oauth-authorization-server"
EXPECTED_RELEASE_HASHES = {
    "supabase.tar.gz": "e5e368b72cae5d51367b07500988a0e6ba68fae485cbe2fbb85169bc389861ce",
    "supabase-postgres-best-practices.tar.gz": "cc06f3f0f700a9ba12427400f07cb7783a20954d39e1853a065f2af1b7ba07af",
    "index.json": "d5eb4afc86451061acd4a4796f0b47f1430ff4b73da85476f15ae948c5a869e7",
}
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/supabase")
    return parser.parse_args()


def run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, **kwargs)


def capture(args: list[str], **kwargs: object) -> str:
    result = subprocess.run(args, text=True, capture_output=True, **kwargs)
    output = result.stdout + result.stderr
    if result.returncode:
        print(output, end="")
        result.check_returncode()
    return output


def load_importer() -> ModuleType:
    spec = importlib.util.spec_from_file_location("ghast_official_importer", IMPORTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {IMPORTER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    with tempfile.TemporaryDirectory(prefix="ghast-supabase-output-") as temp:
        expected_root = Path(temp) / "skills"
        importer.copy_skill_tree(
            source / "skills",
            expected_root,
            recursive=False,
            preserve_agent_metadata=False,
            frontmatter_overrides={},
        )
        expected = file_map(expected_root)
        actual = file_map(plugin / "skills")
        if expected.keys() != actual.keys():
            raise ValueError("Supabase source and Ghast skill file sets differ")
        skill_count = sum(name.endswith("/SKILL.md") for name in expected)
        if skill_count != EXPECTED_SKILLS:
            raise ValueError(f"expected {EXPECTED_SKILLS} Supabase skills, found {skill_count}")
        for relative, expected_path in expected.items():
            actual_path = actual[relative]
            if relative.endswith("/SKILL.md"):
                _, expected_body = split_skill(expected_path)
                _, actual_body = split_skill(actual_path)
                if expected_body.lstrip("\r\n") != actual_body.lstrip("\r\n"):
                    raise ValueError(f"{relative}: body differs from official source")
            elif expected_path.read_bytes() != actual_path.read_bytes():
                raise ValueError(f"{relative}: file differs from official source")


def verify_official_tests(source: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="ghast-supabase-runtime-") as temp:
        root = Path(temp)
        archive = root / "source.tar"
        checkout = root / "checkout"
        checkout.mkdir()
        run(["git", "archive", "--output", str(archive), EXPECTED_REVISION], cwd=source)
        with tarfile.open(archive) as package:
            package.extractall(checkout)

        pnpm = ["corepack", "pnpm"]
        version = run(
            [*pnpm, "--version"], cwd=checkout, capture_output=True
        ).stdout.strip()
        if version != PNPM_VERSION:
            raise ValueError(f"expected pnpm {PNPM_VERSION}, found {version}")
        run([*pnpm, "install", "--frozen-lockfile"], cwd=checkout)
        output = capture([*pnpm, "test:sanity"], cwd=checkout)
        if "Tests  7 passed (7)" not in output or "Test Files  1 passed (1)" not in output:
            raise ValueError("Supabase official seven-test suite summary changed")

        environment = os.environ.copy()
        environment.update(
            {
                "GITHUB_SERVER_URL": "https://github.com",
                "GITHUB_REPOSITORY": "supabase/agent-skills",
                "RELEASE_TAG": "v0.1.8",
            }
        )
        run([*pnpm, "build:release"], cwd=checkout, env=environment)
        for name, expected_hash in EXPECTED_RELEASE_HASHES.items():
            actual_hash = hashlib.sha256((checkout / "dist" / name).read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                raise ValueError(f"Supabase release hash changed for {name}: {actual_hash}")


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
            raise ValueError(f"unexpected Supabase MCP auth boundary: HTTP {error.code}")
    else:
        raise ValueError("Supabase MCP accepted an anonymous initialize request")

    resource = fetch_json(RESOURCE_METADATA_URL)
    authorization = fetch_json(AUTH_METADATA_URL)
    expected_scopes = {
        "organizations:read",
        "projects:read",
        "projects:write",
        "database:read",
        "database:write",
        "edge_functions:read",
        "edge_functions:write",
        "storage:read",
        "storage:write",
    }
    if resource.get("resource") != MCP_URL:
        raise ValueError("Supabase protected-resource identifier changed")
    if not expected_scopes.issubset(resource.get("scopes_supported", [])):
        raise ValueError("Supabase protected-resource scopes changed")
    if authorization.get("issuer") != "https://api.supabase.com":
        raise ValueError("Supabase authorization issuer changed")
    if "S256" not in authorization.get("code_challenge_methods_supported", []):
        raise ValueError("Supabase authorization metadata no longer advertises PKCE S256")
    if not {"authorization_code", "refresh_token"}.issubset(
        authorization.get("grant_types_supported", [])
    ):
        raise ValueError("Supabase authorization grants changed")


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    revision = run(["git", "rev-parse", "HEAD"], cwd=source, capture_output=True).stdout.strip()
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")
    if run(["git", "status", "--porcelain"], cwd=source, capture_output=True).stdout:
        raise ValueError("Supabase source checkout is not clean")

    upstream = json.loads((source / "package.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION:
        raise ValueError("official Supabase version changed")
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("Supabase is not Agent Plugins 1.0")
    if manifest.get("version") != f"{EXPECTED_VERSION}-ghast.1":
        raise ValueError("unexpected Ghast Supabase version")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("Supabase manifest revision differs from source")
    if mcp.get("$schema") != MCP_SCHEMA:
        raise ValueError("Supabase MCP declaration is not Agent Plugins 1.0")
    if mcp.get("mcpServers", {}).get("supabase", {}).get("url") != MCP_URL:
        raise ValueError("Supabase MCP URL changed")
    icon = plugin / ghast["icon"].removeprefix("./")
    if not icon.is_file():
        raise ValueError("Supabase icon is missing")

    verify_skill_tree(source, plugin)
    verify_official_tests(source)
    verify_mcp_auth_boundary()
    print(
        "verified Supabase 0.1.8 official 7-test install suite, deterministic release "
        "archives, 2-skill tree, hosted MCP OAuth boundary, Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
