#!/usr/bin/env python3
"""Verify Readwise's official evidence, CLI tests, and hosted OAuth MCP."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import official_plugin_verification as verify

SKILLS_REVISION = "2d1ce9627c611d24f510dfc2e05a123fa509d2f6"
CLI_REVISION = "414caabf2760cf0577774807f828e1a42d19d01c"
SKILL_SHA256 = "a72340a2f73f9e10b81551b485be88de4322c22a92b105bf8878e94f63213994"
REVISION = "readwise-skills-2d1ce9627c61-a72340a2f73f+oauth-b39687b19dac"
MCP_URL = "https://mcp2.readwise.io/mcp"


def git_identity(source: Path, revision: str, repository: str) -> None:
    imp = verify.load_importer()
    if imp.git_revision(source) != revision or imp.normalized_git_remote(
        source
    ) != imp.normalized_repository_url(repository):
        raise ValueError(f"Readwise official source changed: {repository}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-source", type=Path, required=True)
    parser.add_argument("--cli-source", type=Path, required=True)
    parser.add_argument(
        "--plugin",
        type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/readwise",
    )
    args = parser.parse_args()
    skills = args.skills_source.resolve()
    cli = args.cli_source.resolve()
    plugin = args.plugin.resolve()
    git_identity(skills, SKILLS_REVISION, "https://github.com/readwiseio/readwise-skills")
    git_identity(cli, CLI_REVISION, "https://github.com/readwiseio/readwise-cli")
    skill = skills / "skills/readwise-mcp/SKILL.md"
    if hashlib.sha256(skill.read_bytes()).hexdigest() != SKILL_SHA256:
        raise ValueError("Readwise official MCP skill changed")
    tools = sorted(
        set(re.findall(r"\b(?:reader|readwise)_[a-z0-9_]+(?=\()", skill.read_text()))
    )
    if len(tools) != 22:
        raise ValueError(f"Readwise official tool inventory changed: {tools}")
    verify.manifest(
        plugin,
        name="readwise",
        version="1.0.0-ghast.1",
        revision=REVISION,
    )
    mcp = json.loads((plugin / "mcp.json").read_text())
    if mcp["mcpServers"]["readwise"] != {
        "type": "streamable-http",
        "url": MCP_URL,
    }:
        raise ValueError("Readwise packaged MCP declaration changed")

    build = subprocess.run(
        ["npm", "run", "build"], cwd=cli, check=True, text=True, capture_output=True
    )
    if "tsc" not in build.stdout:
        raise ValueError("Readwise CLI build command changed")
    tests = subprocess.run(
        ["npm", "test"], cwd=cli, check=True, text=True, capture_output=True
    )
    if "tests 15" not in tests.stdout or "pass 15" not in tests.stdout or "fail 0" not in tests.stdout:
        raise ValueError(f"Readwise CLI test result changed:\n{tests.stdout[-1000:]}")
    with tempfile.TemporaryDirectory(prefix="ghast-readwise-cli-") as home:
        env = os.environ.copy()
        env["HOME"] = home
        version = subprocess.run(
            ["node", "dist/index.js", "--version"],
            cwd=cli,
            env=env,
            check=True,
            text=True,
            capture_output=True,
        )
        help_result = subprocess.run(
            ["node", "dist/index.js", "--help"],
            cwd=cli,
            env=env,
            check=True,
            text=True,
            capture_output=True,
        )
    if version.stdout.strip() != "0.5.9" or not {"login", "login-with-token", "config", "skills"}.issubset(help_result.stdout.split()):
        raise ValueError("Readwise CLI identity or unauthenticated help changed")

    status, headers, body = verify.curl_json(
        MCP_URL, payload=verify.initialize_payload()
    )
    if status != 401 or "oauth-protected-resource" not in headers.lower() or "invalid_token" not in str(body):
        raise ValueError(f"unexpected Readwise MCP boundary: HTTP {status}")
    status, _, resource = verify.curl_json(
        "https://mcp2.readwise.io/.well-known/oauth-protected-resource/mcp"
    )
    if (
        status != 200
        or not isinstance(resource, dict)
        or resource.get("authorization_servers") != ["https://readwise.io/o/"]
        or not {"openid", "read", "write"}.issubset(resource.get("scopes_supported", []))
    ):
        raise ValueError("Readwise protected-resource metadata changed")
    status, _, oauth = verify.curl_json(
        "https://readwise.io/.well-known/oauth-authorization-server/o/"
    )
    if (
        status != 200
        or not isinstance(oauth, dict)
        or oauth.get("registration_endpoint") != "https://readwise.io/o/register/"
        or "authorization_code" not in oauth.get("grant_types_supported", [])
        or "refresh_token" not in oauth.get("grant_types_supported", [])
        or "S256" not in oauth.get("code_challenge_methods_supported", [])
        or "none" not in oauth.get("token_endpoint_auth_methods_supported", [])
    ):
        raise ValueError("Readwise dynamic OAuth/PKCE metadata changed")
    print(
        "verified Readwise official 22-tool evidence, CLI 0.5.9 build and "
        "15 tests, isolated unauthenticated CLI, hosted read/write OAuth MCP, "
        "dynamic registration, PKCE S256, Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
