#!/usr/bin/env python3
"""Verify Atlassian's official skills, JQL helper, and Rovo OAuth MCP."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import official_plugin_verification as verify

REVISION = "94a30436435fb526a29f820f5f46250870eb75a0"
MCP_URL = "https://mcp.atlassian.com/v1/mcp/authv2"
RESOURCE_METADATA = (
    "https://mcp.atlassian.com/.well-known/"
    "oauth-protected-resource/v1/mcp/authv2"
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--plugin",
        type=Path,
        default=verify.REPOSITORY_ROOT / "plugins/atlassian-rovo",
    )
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(
        source
    ) != imp.normalized_repository_url(
        "https://github.com/atlassian/atlassian-mcp-server"
    ):
        raise ValueError("Atlassian official source changed")
    verify.manifest(
        plugin,
        name="atlassian-rovo",
        version=None,
        revision=REVISION,
    )

    with tempfile.TemporaryDirectory(prefix="ghast-atlassian-skills-") as temp:
        staging = Path(temp) / "staging"
        staging.mkdir()
        expected = staging / "skills"
        imp.copy_skill_tree(
            source / "skills",
            expected,
            recursive=False,
            preserve_agent_metadata=False,
            frontmatter_overrides={},
        )
        imp.apply_ghast_compatibility("atlassian-rovo", staging)
        count = verify.compare_trees(
            expected,
            plugin / "skills",
            ignore_skill_frontmatter=True,
        )
    if count != 15 or len(list((plugin / "skills").rglob("SKILL.md"))) != 6:
        raise ValueError("Atlassian skill inventory changed")

    validation = subprocess.run(
        ["node", "scripts/validate-template.mjs"],
        cwd=source,
        check=True,
        text=True,
        capture_output=True,
    )
    if "Validation passed" not in validation.stdout:
        raise ValueError("Atlassian official template validation changed")
    helper = (
        plugin
        / "skills/generate-status-report/scripts/jql_builder.py"
    )
    execution = subprocess.run(
        ["python3", str(helper)],
        check=True,
        text=True,
        capture_output=True,
    )
    if "ORDER BY priority DESC, updated DESC" not in execution.stdout:
        raise ValueError("Atlassian JQL helper default output changed")
    spec = importlib.util.spec_from_file_location("atlassian_jql_builder", helper)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not import Atlassian JQL helper")
    module = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(module)
    for unsafe in (
        "priority DESC AND status = Open",
        "priority DESC; DELETE",
        "priority DESC, updated DESC OR created ASC",
    ):
        try:
            module.build_project_query("PROJ", order_by=unsafe)
        except ValueError:
            continue
        raise ValueError(f"Atlassian JQL helper accepted unsafe order: {unsafe}")

    mcp = json.loads((plugin / "mcp.json").read_text())
    if mcp["mcpServers"]["atlassian"] != {
        "type": "streamable-http",
        "url": MCP_URL,
    }:
        raise ValueError("Atlassian packaged MCP declaration changed")
    status, headers, body = verify.curl_json(
        MCP_URL,
        payload=verify.initialize_payload(),
    )
    if status != 401 or "oauth-protected-resource" not in headers.lower() or not isinstance(body, dict) or body.get("error") != "invalid_token":
        raise ValueError(f"unexpected Atlassian MCP boundary: HTTP {status}")
    status, _, resource = verify.curl_json(RESOURCE_METADATA)
    required_scopes = {
        "read:jira-work",
        "write:jira-work",
        "read:page:confluence",
        "write:page:confluence",
        "read:all:twg",
        "write:all:twg",
    }
    if status != 200 or not isinstance(resource, dict) or not required_scopes.issubset(resource.get("scopes_supported", [])):
        raise ValueError("Atlassian protected-resource scopes changed")
    status, _, oauth = verify.curl_json(
        "https://mcp.atlassian.com/.well-known/oauth-authorization-server"
    )
    if status != 200 or not isinstance(oauth, dict) or oauth.get("registration_endpoint") != "https://mcp.atlassian.com/v1/register" or "S256" not in oauth.get("code_challenge_methods_supported", []):
        raise ValueError("Atlassian dynamic OAuth/PKCE metadata changed")

    print(
        "verified Atlassian official 6-skill/15-file tree, template check, "
        "hardened runnable JQL helper, OAuth read/write scopes, dynamic "
        "registration, Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
