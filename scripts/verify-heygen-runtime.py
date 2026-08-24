#!/usr/bin/env python3
"""Verify HeyGen's official skills, update helper, and OAuth MCP contract."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

import official_plugin_verification as verify

REVISION = "1bd5e4d33a028dfed3abf504c5e3dd644fb9ea8a"
MCP_URL = "https://mcp.heygen.com/mcp/v1/"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--plugin",
        type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/heygen",
    )
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(
        source
    ) != imp.normalized_repository_url("https://github.com/heygen-com/skills"):
        raise ValueError("HeyGen official source changed")
    release_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", "v3.2.0", "HEAD"],
        cwd=source,
        check=False,
    )
    if release_ancestor.returncode != 0 or (source / "VERSION").read_text().strip() != "3.2.0":
        raise ValueError("HeyGen release version changed")
    if "## [3.2.0]" not in (source / "CHANGELOG.md").read_text():
        raise ValueError("HeyGen changelog version changed")
    for skill in ("heygen-avatar", "heygen-translate", "heygen-video"):
        if "version: 3.2.0" not in (source / skill / "SKILL.md").read_text():
            raise ValueError(f"HeyGen skill version changed: {skill}")
    verify.manifest(
        plugin,
        name="heygen",
        version="3.2.0-ghast.1",
        revision=REVISION,
    )

    with tempfile.TemporaryDirectory(prefix="ghast-heygen-skills-") as temp:
        expected = Path(temp) / "skills"
        imp.copy_skill_tree(
            source,
            expected,
            recursive=False,
            preserve_agent_metadata=False,
            frontmatter_overrides={},
        )
        staging = Path(temp) / "staging"
        staging.mkdir()
        expected.rename(staging / "skills")
        imp.apply_ghast_compatibility("heygen", staging)
        count = verify.compare_trees(
            staging / "skills",
            plugin / "skills",
            ignore_skill_frontmatter=True,
        )
    if count != 20 or len(list((plugin / "skills").rglob("SKILL.md"))) != 3:
        raise ValueError("HeyGen packaged skill inventory changed")

    checker = plugin / "skills/heygen-video/scripts/update-check.sh"
    subprocess.run(["bash", "-n", str(checker)], check=True)
    with tempfile.TemporaryDirectory(prefix="ghast-heygen-update-") as temp:
        root = Path(temp)
        remote = root / "VERSION"
        remote.write_text("9.9.9\n")
        state = root / "state"
        env = os.environ.copy()
        env.update(
            {
                "HEYGEN_SKILL_DIR": str(plugin / "skills/heygen-video"),
                "HEYGEN_SKILLS_STATE": str(state),
                "HEYGEN_REMOTE_URL": remote.as_uri(),
            }
        )
        result = subprocess.run(
            ["bash", str(checker), "--force"],
            env=env,
            check=True,
            text=True,
            capture_output=True,
        )
        if result.stdout.strip() != "UPGRADE_AVAILABLE 3.2.0 9.9.9":
            raise ValueError("HeyGen packaged update checker changed")

    mcp = json.loads((plugin / "mcp.json").read_text())
    if mcp["mcpServers"]["heygen"] != {
        "type": "streamable-http",
        "url": MCP_URL,
    }:
        raise ValueError("HeyGen packaged MCP declaration changed")
    status, headers, body = verify.curl_json(
        MCP_URL, payload=verify.initialize_payload()
    )
    if status != 401 or "oauth-protected-resource" not in headers.lower() or "invalid_token" not in str(body):
        raise ValueError(f"unexpected HeyGen MCP boundary: HTTP {status}")
    status, _, resource = verify.curl_json(
        "https://mcp.heygen.com/.well-known/oauth-protected-resource/mcp/v1"
    )
    if status != 200 or not isinstance(resource, dict) or resource.get(
        "authorization_servers"
    ) != ["https://api2.heygen.com"]:
        raise ValueError("HeyGen protected-resource metadata changed")
    status, _, oauth = verify.curl_json(
        "https://api2.heygen.com/.well-known/oauth-authorization-server"
    )
    grants = set(oauth.get("grant_types_supported", [])) if isinstance(oauth, dict) else set()
    if (
        status != 200
        or not isinstance(oauth, dict)
        or oauth.get("registration_endpoint") != "https://api2.heygen.com/v1/oauth/register"
        or not {"authorization_code", "refresh_token", "urn:ietf:params:oauth:grant-type:device_code"}.issubset(grants)
        or "S256" not in oauth.get("code_challenge_methods_supported", [])
        or "none" not in oauth.get("token_endpoint_auth_methods_supported", [])
    ):
        raise ValueError("HeyGen OAuth metadata changed")
    print(
        "verified HeyGen v3.2.0 official 3-skill/19-source-file tree plus "
        "VERSION compatibility file, runnable update checker, hosted OAuth "
        "MCP, dynamic registration, PKCE S256, Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
