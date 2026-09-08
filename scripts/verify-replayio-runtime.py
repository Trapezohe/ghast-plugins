#!/usr/bin/env python3
"""Verify Replay.io's pinned official sources and no-credential runtime."""

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


EXPECTED_REVISION = "c6cd28ff3d47f4e8e8b23040c69925ec2a820695"
EXPECTED_VERSION = "0.1.1"
EXPECTED_SKILLS = 2
EXPECTED_SKILL_FILES = 24
EXPECTED_ROOT_SCRIPTS = 5
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_URL = "https://dispatch.replay.io/mcp"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/replayio")
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


def file_map(root: Path) -> dict[str, Path]:
    return {path.relative_to(root).as_posix(): path for path in root.rglob("*") if path.is_file()}


def verify_checked_in_output(source: Path, plugin: Path, importer: ModuleType) -> None:
    with tempfile.TemporaryDirectory(prefix="ghast-replayio-output-") as temp:
        expected_plugin = Path(temp)
        expected_skills = expected_plugin / "skills"
        importer.copy_skill_tree(
            source / "codex/replayio/skills", expected_skills, recursive=False,
            preserve_agent_metadata=False, frontmatter_overrides={},
        )
        importer.copy_skill_tree(
            source / "codex/replay-qa/skills", expected_skills, recursive=False,
            preserve_agent_metadata=False, frontmatter_overrides={}, merge=True,
        )
        shutil.copytree(source / "codex/replayio/scripts", expected_plugin / "scripts")
        importer.apply_ghast_compatibility("replayio", expected_plugin)
        expected = file_map(expected_skills)
        actual = file_map(plugin / "skills")
        if expected.keys() != actual.keys() or len(expected) != EXPECTED_SKILL_FILES:
            raise ValueError("Replay official and Ghast skill file sets differ")
        if sum(name.count("/") == 1 and name.endswith("/SKILL.md") for name in expected) != EXPECTED_SKILLS:
            raise ValueError("unexpected Replay skill count")
        for relative, expected_path in expected.items():
            if expected_path.read_bytes() != actual[relative].read_bytes():
                raise ValueError(f"Replay skill output differs: {relative}")
        expected_scripts = file_map(expected_plugin / "scripts")
        actual_scripts = file_map(plugin / "scripts")
        if expected_scripts.keys() != actual_scripts.keys() or len(expected_scripts) != EXPECTED_ROOT_SCRIPTS:
            raise ValueError("Replay root script file sets differ")
        for relative, expected_path in expected_scripts.items():
            if expected_path.read_bytes() != actual_scripts[relative].read_bytes():
                raise ValueError(f"Replay root script differs: {relative}")


def verify_script_syntax(plugin: Path) -> tuple[int, int]:
    javascript = sorted(plugin.glob("**/*.js"))
    shell = sorted(plugin.glob("**/*.sh"))
    for path in javascript:
        run(["node", "--check", str(path)], capture_output=True)
    for path in shell:
        run(["bash", "-n", str(path)], capture_output=True)
    return len(javascript), len(shell)


def verify_diagnostics(plugin: Path) -> None:
    environment = os.environ.copy()
    environment.pop("REPLAY_API_KEY", None)
    environment.pop("REPLAY_QA_API_KEY", None)
    environment.pop("AGENT_BROWSER_EXECUTABLE_PATH", None)
    with tempfile.TemporaryDirectory(prefix="ghast-replayio-diagnostics-") as temp:
        context = run(
            ["node", str(plugin / "skills/replayio/scripts/context.js")],
            cwd=temp, env=environment, capture_output=True,
        )
        payload = json.loads(context.stdout)
        for key in ("replay_cli", "ffmpeg", "jq", "replay_chromium", "recording_environment", "mp4_guidance"):
            if key not in payload:
                raise ValueError(f"Replay dependency diagnostic omitted {key}")
        qa_context = run(
            ["node", str(plugin / "skills/replay-qa/scripts/context.js")],
            cwd=temp, env=environment, capture_output=True,
        )
        qa_payload = json.loads(qa_context.stdout)
        if "replay_qa_context_unavailable" not in qa_payload:
            raise ValueError("Replay QA no-credential diagnostic boundary changed")


def verify_auth_boundary() -> None:
    request = urllib.request.Request(
        MCP_URL,
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        method="POST",
    )
    try:
        urllib.request.urlopen(request, timeout=30)
    except urllib.error.HTTPError as error:
        metadata = error.headers.get("WWW-Authenticate", "")
        if error.code != 401 or "oauth-protected-resource" not in metadata:
            raise ValueError(f"unexpected Replay MCP auth boundary: HTTP {error.code}") from error
    else:
        raise ValueError("Replay MCP unexpectedly allowed unauthenticated tools/list")


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    importer = load_importer()
    if importer.git_revision(source) != EXPECTED_REVISION:
        raise ValueError("Replay source revision changed")
    if importer.normalized_git_remote(source) != importer.normalized_repository_url(
        "https://github.com/replayio/plugins"
    ):
        raise ValueError("Replay official repository origin changed")
    upstream = json.loads((source / "codex/replayio/.codex-plugin/plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION:
        raise ValueError("official Replay version changed")
    if manifest.get("$schema") != PLUGIN_SCHEMA or manifest.get("version") != '0.1.1':
        raise ValueError("unexpected Replay Agent Plugins 1.0 manifest")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("Replay manifest revision differs")
    if not (plugin / ghast["icon"].removeprefix("./")).is_file():
        raise ValueError("Replay icon is missing")
    if mcp["mcpServers"]["replay"].get("url") != MCP_URL:
        raise ValueError("Replay official MCP endpoint changed")
    verify_checked_in_output(source, plugin, importer)
    javascript, shell = verify_script_syntax(plugin)
    verify_diagnostics(plugin)
    verify_auth_boundary()
    print(f"verified Replay official two-skill tree, {javascript} JavaScript and {shell} Bash scripts, no-credential diagnostics, OAuth MCP boundary, Agent Plugins 1.0, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
