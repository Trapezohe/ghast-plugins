#!/usr/bin/env python3
"""Verify MotherDuck's official local core and hosted OAuth MCP contract."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

import official_plugin_verification as verify

REVISION = "275d2e7d2ba4f5b48ce8ad3f01a9aeea8bd08616"
MCP_URL = "https://api.motherduck.com/mcp"
TESTS = [
    "tests/e2e/test_memory_duckdb.py",
    "tests/e2e/test_local_duckdb.py",
    "tests/e2e/test_read_only.py",
    "tests/e2e/test_read_only_concurrent.py",
    "tests/e2e/test_limits.py",
    "tests/e2e/test_timeout.py",
    "tests/e2e/test_type_serialization.py",
    "tests/e2e/test_catalog_tools.py",
    "tests/e2e/test_init_sql.py",
    "tests/e2e/test_http_transport.py",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--python",
        type=Path,
        required=True,
        help="Python executable in an environment with the official dev dependencies and uv",
    )
    parser.add_argument(
        "--plugin",
        type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/motherduck",
    )
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    runtime_python = args.python.expanduser().absolute()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(
        source
    ) != imp.normalized_repository_url(
        "https://github.com/motherduckdb/mcp-server-motherduck"
    ):
        raise ValueError("MotherDuck official source changed")
    if subprocess.run(
        ["git", "tag", "--points-at", "HEAD"],
        cwd=source,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.split() != ["v1.0.8"]:
        raise ValueError("MotherDuck release tag changed")
    if 'version = "1.0.8"' not in (source / "pyproject.toml").read_text():
        raise ValueError("MotherDuck source version changed")
    verify.manifest(
        plugin,
        name="motherduck",
        version="1.0.8-ghast.1",
        revision=REVISION,
    )

    mcp = json.loads((plugin / "mcp.json").read_text())
    if mcp["mcpServers"]["motherduck"] != {
        "type": "streamable-http",
        "url": MCP_URL,
    }:
        raise ValueError("MotherDuck packaged MCP declaration changed")
    if not runtime_python.is_file() or not (runtime_python.parent / "uv").is_file():
        raise ValueError("MotherDuck verifier runtime must include Python and uv")
    env = os.environ.copy()
    env["PATH"] = f"{runtime_python.parent}{os.pathsep}{env.get('PATH', '')}"
    tests = subprocess.run(
        [str(runtime_python), "-m", "pytest", "-q", *TESTS],
        cwd=source,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )
    summary = tests.stdout + tests.stderr
    if "75 passed, 36 skipped" not in summary:
        raise ValueError(f"MotherDuck local-core test inventory changed:\n{summary[-1000:]}")
    lint = subprocess.run(
        [str(runtime_python.parent / "ruff"), "check", "src", "tests/e2e/test_catalog_tools.py"],
        cwd=source,
        check=True,
        text=True,
        capture_output=True,
    )
    if "All checks passed" not in lint.stdout:
        raise ValueError("MotherDuck Ruff result changed")

    status, headers, body = verify.curl_json(
        MCP_URL, payload=verify.initialize_payload()
    )
    if status != 401 or "oauth-protected-resource" not in headers.lower() or "Authentication required" not in str(body):
        raise ValueError(f"unexpected MotherDuck MCP boundary: HTTP {status}")
    status, _, resource = verify.curl_json(
        "https://api.motherduck.com/.well-known/oauth-protected-resource/mcp"
    )
    required_scopes = {"openid", "profile", "email", "read:databases", "offline_access"}
    if (
        status != 200
        or not isinstance(resource, dict)
        or resource.get("authorization_servers") != ["https://mcp-auth.motherduck.com"]
        or not required_scopes.issubset(resource.get("scopes_supported", []))
    ):
        raise ValueError("MotherDuck protected-resource metadata changed")
    status, _, oauth = verify.curl_json(
        "https://mcp-auth.motherduck.com/.well-known/oauth-authorization-server"
    )
    if (
        status != 200
        or not isinstance(oauth, dict)
        or not oauth.get("registration_endpoint")
        or "authorization_code" not in oauth.get("grant_types_supported", [])
        or "refresh_token" not in oauth.get("grant_types_supported", [])
        or "S256" not in oauth.get("code_challenge_methods_supported", [])
        or "none" not in oauth.get("token_endpoint_auth_methods_supported", [])
    ):
        raise ValueError("MotherDuck dynamic OAuth/PKCE metadata changed")
    print(
        "verified MotherDuck v1.0.8 local core (75 passed, 36 credential "
        "tests skipped), Ruff, hosted MCP OAuth scopes, dynamic registration, "
        "PKCE S256, Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
