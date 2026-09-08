#!/usr/bin/env python3
"""Verify Wix's pinned official skill suite, scripts, CI, and MCP contract."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path
from types import ModuleType

EXPECTED_REVISION = "f30595361e8d02f0dc432b499d00916a2e3918f3"
EXPECTED_VERSION = "1.16.3"
EXPECTED_TOP_LEVEL_SKILLS = 9
EXPECTED_ALL_SKILLS = 19
EXPECTED_FILES = 478
MCP_URL = "https://mcp.wix.com/mcp"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/wix")
    parser.add_argument("--run-official-ci", action="store_true", help="Install the roughly 2 GiB locked Wix typecheck environment and run it")
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


def split_skill(path: Path) -> tuple[str, str]:
    text = path.read_text()
    closing = text.find("\n---\n", 4) if text.startswith("---\n") else -1
    if closing < 0:
        raise ValueError(f"{path}: invalid frontmatter")
    return text[4:closing], text[closing + 5 :].lstrip("\r\n")


def verify_official_ci(source: Path) -> None:
    if not run(["node", "--version"], capture_output=True).stdout.strip().startswith("v24."):
        raise ValueError("Wix official typecheck requires Node 24")
    with tempfile.TemporaryDirectory(prefix="ghast-wix-ci-") as temp:
        root = Path(temp); archive, checkout = root / "source.tar", root / "source"
        checkout.mkdir()
        run(["git", "archive", "--output", str(archive), EXPECTED_REVISION], cwd=source)
        with tarfile.open(archive) as package:
            package.extractall(checkout, filter="data")
        harness = checkout / ".github/wix-app-typecheck"
        yarn_version = run(["corepack", "yarn", "--version"], cwd=harness, capture_output=True).stdout.strip()
        if yarn_version != "4.12.0":
            raise ValueError(f"expected Yarn 4.12.0, found {yarn_version}")
        run(["corepack", "yarn", "install", "--immutable"], cwd=harness)
        result = run(["node", "extract.mjs"], cwd=harness, capture_output=True)
        output = result.stdout + result.stderr
        if "82 structural error(s) in 16 file(s)" not in output or "No type errors found" not in output:
            raise ValueError("Wix official typecheck warning/result profile changed")


def main() -> int:
    parsed = args()
    source, plugin = parsed.source.resolve(), parsed.plugin.resolve()
    imp = importer()
    if imp.git_revision(source) != EXPECTED_REVISION or imp.normalized_git_remote(source) != imp.normalized_repository_url("https://github.com/wix/skills"):
        raise ValueError("Wix official source changed")
    upstream = json.loads((source / ".codex-plugin/plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION or manifest.get("version") != '1.16.3' or manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("unexpected Wix Agent Plugins 1.0 manifest")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION or not (plugin / ghast["icon"].removeprefix("./")).is_file():
        raise ValueError("Wix revision or icon differs")
    if mcp["mcpServers"]["wix-mcp"].get("url") != MCP_URL:
        raise ValueError("Wix MCP endpoint changed")
    with tempfile.TemporaryDirectory(prefix="ghast-wix-output-") as temp:
        expected_root = Path(temp) / "skills"
        imp.copy_skill_tree(source / "skills", expected_root, recursive=False, preserve_agent_metadata=False, frontmatter_overrides={})
        expected, actual = files(expected_root), files(plugin / "skills")
        if expected.keys() != actual.keys() or len(expected) != EXPECTED_FILES:
            raise ValueError("Wix skill file sets differ")
        top = sum(name.count("/") == 1 and name.endswith("/SKILL.md") for name in expected)
        all_skills = sum(name.endswith("/SKILL.md") for name in expected)
        if (top, all_skills) != (EXPECTED_TOP_LEVEL_SKILLS, EXPECTED_ALL_SKILLS):
            raise ValueError(f"Wix skill inventory changed: top={top}, all={all_skills}")
        for name, path in expected.items():
            if name.endswith("/SKILL.md"):
                _, expected_body = split_skill(path)
                actual_frontmatter, actual_body = split_skill(actual[name])
                expected_name = Path(name).parent.name
                if f"name: {expected_name}\n" not in actual_frontmatter + "\n":
                    raise ValueError(f"Wix normalized skill name differs: {name}")
                if expected_body != actual_body:
                    raise ValueError(f"Wix skill body differs: {name}")
            elif path.read_bytes() != actual[name].read_bytes():
                raise ValueError(f"Wix output differs: {name}")
    javascript = sorted(list(plugin.glob("skills/**/*.js")) + list(plugin.glob("skills/**/*.cjs")) + list(plugin.glob("skills/**/*.mjs")))
    for path in javascript:
        run(["node", "--check", str(path)], capture_output=True)
    if parsed.run_official_ci:
        verify_official_ci(source)
    with tempfile.TemporaryDirectory(prefix="ghast-wix-http-") as temp:
        headers = Path(temp) / "headers"
        result = run(["curl", "-sS", "-D", str(headers), "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "-H", "Content-Type: application/json", "-H", "Accept: application/json, text/event-stream", "--data", '{"jsonrpc":"2.0","id":1,"method":"tools/list"}', MCP_URL], capture_output=True)
        if result.stdout != "401" or "oauth-protected-resource" not in headers.read_text().lower():
            raise ValueError(f"unexpected Wix MCP boundary: HTTP {result.stdout}")
        metadata = json.loads(run(["curl", "-sS", "https://mcp.wix.com/.well-known/oauth-authorization-server"], capture_output=True).stdout)
        if metadata.get("registration_endpoint") != "https://mcp.wix.com/register" or "S256" not in metadata.get("code_challenge_methods_supported", []):
            raise ValueError("Wix dynamic OAuth/PKCE metadata changed")
    ci = " with official Node 24/Yarn 4.12 typecheck" if parsed.run_official_ci else ""
    print(f"verified Wix 1.16.3 official 9-top-level/19-total-skill, 478-file tree, {len(javascript)} scripts, dynamic OAuth boundary, Agent Plugins 1.0, and icon{ci}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
