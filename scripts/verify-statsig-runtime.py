#!/usr/bin/env python3
"""Verify Statsig's official skills, scripts, and Console-key MCP bridge."""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import tempfile
from pathlib import Path

import official_plugin_verification as verify

REVISION = "e720bbb3fc7bb4f5d50ad6175e050138ddb1a1c6"
MCP_URL = "https://api.statsig.com/v1/mcp"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=verify.REPOSITORY_ROOT / "plugins/statsig")
    args = parser.parse_args()
    source, plugin = args.source.resolve(), args.plugin.resolve()
    imp = verify.load_importer()
    if imp.git_revision(source) != REVISION or imp.normalized_git_remote(source) != imp.normalized_repository_url("https://github.com/statsig-io/agent-skills"):
        raise ValueError("Statsig official source changed")
    verify.manifest(plugin, name="statsig", version=None, revision=REVISION)
    with tempfile.TemporaryDirectory(prefix="ghast-statsig-expected-") as temp:
        expected = Path(temp) / "skills"
        imp.copy_skill_tree(source / "skills", expected, recursive=False, preserve_agent_metadata=False, frontmatter_overrides={})
        (expected / "statsig-create-cloud-metric").rename(Path(temp) / "excluded")
        staging = Path(temp) / "staging"
        staging.mkdir()
        expected.rename(staging / "skills")
        imp.apply_ghast_compatibility("statsig", staging)
        count = verify.compare_trees(staging / "skills", plugin / "skills", ignore_skill_frontmatter=True)
    if count != 8 or len(list((plugin / "skills").rglob("SKILL.md"))) != 2:
        raise ValueError("Statsig retained skill inventory changed")
    scripts = sorted((plugin / "skills/statsig-dashboard/scripts").glob("*.py"))
    if len(scripts) != 4:
        raise ValueError("Statsig dashboard script inventory changed")
    for script in scripts:
        ast.parse(script.read_text(), filename=str(script))
        result = subprocess.run(["python3", str(script), "--help"], check=True, text=True, capture_output=True)
        if "--dry-run" not in result.stdout:
            raise ValueError(f"Statsig dry-run option missing: {script.name}")
    mcp = json.loads((plugin / "mcp.json").read_text())["mcpServers"]["statsig"]
    joined = " ".join(mcp.get("args", []))
    if mcp.get("command") != "npx" or "mcp-remote@0.1.38" not in joined or "${STATSIG_CONSOLE_API_KEY}" not in joined:
        raise ValueError("Statsig environment-backed MCP bridge changed")
    status, headers, body = verify.curl_json(MCP_URL, payload=verify.initialize_payload())
    if status != 401 or "oauth-protected-resource" not in headers.lower() or not isinstance(body, dict) or "active CONSOLE key" not in str(body.get("message")):
        raise ValueError(f"unexpected Statsig MCP boundary: HTTP {status}")
    status, _, oauth = verify.curl_json("https://api.statsig.com/.well-known/oauth-authorization-server")
    if status != 200 or not isinstance(oauth, dict) or "S256" not in oauth.get("code_challenge_methods_supported", []):
        raise ValueError("Statsig OAuth metadata changed")
    print("verified Statsig 2 retained official skills/8 files, 4 parseable dry-run scripts, environment-backed MCP bridge, auth boundary, Agent Plugins 1.0, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
