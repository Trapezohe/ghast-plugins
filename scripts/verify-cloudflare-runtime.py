#!/usr/bin/env python3
"""Verify Cloudflare's pinned official skills, CI scan, and public MCPs."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path
from types import ModuleType


EXPECTED_REVISION = "f96bff754e428838818017f75817f0f9428acd48"
EXPECTED_VERSION = "1.0.0"
EXPECTED_SKILLS = 13
EXPECTED_FILES = 375
SEMGREP_VERSION = "1.160.0"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SERVERS = {
    "cloudflare-api": "https://mcp.cloudflare.com/mcp",
    "cloudflare-docs": "https://docs.mcp.cloudflare.com/mcp",
    "cloudflare-bindings": "https://bindings.mcp.cloudflare.com/mcp",
    "cloudflare-builds": "https://builds.mcp.cloudflare.com/mcp",
    "cloudflare-observability": "https://observability.mcp.cloudflare.com/mcp",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/cloudflare")
    parser.add_argument("--semgrep", type=Path)
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


def split_skill(path: Path) -> str:
    text = path.read_text()
    closing = text.find("\n---\n", 4) if text.startswith("---\n") else -1
    if closing < 0:
        raise ValueError(f"{path}: invalid frontmatter")
    return text[closing + 5 :].lstrip("\r\n")


def file_map(root: Path) -> dict[str, Path]:
    return {path.relative_to(root).as_posix(): path for path in root.rglob("*") if path.is_file()}


def verify_checked_in_output(source: Path, plugin: Path, importer: ModuleType) -> None:
    with tempfile.TemporaryDirectory(prefix="ghast-cloudflare-output-") as temp:
        expected_root = Path(temp) / "skills"
        importer.copy_skill_tree(
            source / "skills", expected_root, recursive=False,
            preserve_agent_metadata=False, frontmatter_overrides={},
        )
        expected = file_map(expected_root)
        actual = file_map(plugin / "skills")
        if expected.keys() != actual.keys() or len(expected) != EXPECTED_FILES:
            raise ValueError("Cloudflare official and Ghast skill file sets differ")
        count = sum(name.count("/") == 1 and name.endswith("/SKILL.md") for name in expected)
        if count != EXPECTED_SKILLS:
            raise ValueError(f"expected {EXPECTED_SKILLS} skills, found {count}")
        for relative, expected_path in expected.items():
            actual_path = actual[relative]
            if relative.endswith("/SKILL.md"):
                if split_skill(expected_path) != split_skill(actual_path):
                    raise ValueError(f"{relative}: body differs from official source")
            elif expected_path.read_bytes() != actual_path.read_bytes():
                raise ValueError(f"{relative}: differs from official source")
    command_root = plugin / "ai.trapezohe.ghast/commands"
    for source_path in sorted((source / "commands").glob("*.md")):
        if source_path.read_bytes() != (command_root / source_path.name).read_bytes():
            raise ValueError(f"Cloudflare command differs: {source_path.name}")


def verify_official_semgrep(source: Path, explicit: Path | None) -> None:
    if explicit:
        command = [str(explicit.expanduser().resolve())]
    elif discovered := shutil.which("semgrep"):
        command = [discovered]
    elif uvx := shutil.which("uvx"):
        command = [uvx, "--from", f"semgrep=={SEMGREP_VERSION}", "semgrep"]
    else:
        raise ValueError("semgrep or uvx is required to reproduce Cloudflare CI")
    version = run(command + ["--version"], capture_output=True).stdout.strip()
    if SEMGREP_VERSION not in version:
        raise ValueError(f"expected Semgrep {SEMGREP_VERSION}, found {version}")
    with tempfile.TemporaryDirectory(prefix="ghast-cloudflare-semgrep-") as temp:
        root = Path(temp)
        archive = root / "source.tar"
        checkout = root / "checkout"
        checkout.mkdir()
        run(["git", "archive", "--output", str(archive), EXPECTED_REVISION], cwd=source)
        with tarfile.open(archive) as package:
            package.extractall(checkout, filter="data")
        run(command + ["scan", "--config=auto"], cwd=checkout)


def curl_json_rpc(url: str, payload: dict, root: Path) -> tuple[int, str, str]:
    headers = root / "headers"
    body = root / "body"
    result = run(
        [
            "curl", "--silent", "--show-error", "--dump-header", str(headers),
            "--output", str(body), "--write-out", "%{http_code}", "--request", "POST",
            "--header", "Content-Type: application/json",
            "--header", "Accept: application/json, text/event-stream",
            "--data", json.dumps(payload, separators=(",", ":")), url,
        ],
        capture_output=True,
    )
    return int(result.stdout), headers.read_text(), body.read_text()


def sse_result(body: str) -> dict:
    for line in body.splitlines():
        if line.startswith("data: "):
            return json.loads(line[6:])
    raise ValueError("Cloudflare docs MCP did not return an SSE JSON result")


def verify_public_mcp() -> None:
    with tempfile.TemporaryDirectory(prefix="ghast-cloudflare-mcp-") as temp:
        root = Path(temp)
        status, _, body = curl_json_rpc(
            MCP_SERVERS["cloudflare-docs"],
            {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, root,
        )
        tools = sse_result(body)["result"]["tools"] if status == 200 else []
        names = sorted(tool["name"] for tool in tools)
        if names != ["migrate_pages_to_workers_guide", "search_cloudflare_documentation"]:
            raise ValueError(f"Cloudflare docs tool inventory changed: {names}")
        status, _, body = curl_json_rpc(
            MCP_SERVERS["cloudflare-docs"],
            {
                "jsonrpc": "2.0", "id": 2, "method": "tools/call",
                "params": {
                    "name": "search_cloudflare_documentation",
                    "arguments": {"query": "Durable Objects SQLite storage transactions"},
                },
            }, root,
        )
        response = sse_result(body) if status == 200 else {}
        text = "\n".join(item.get("text", "") for item in response.get("result", {}).get("content", []))
        if "SQLite-backed Durable Objects" not in text:
            raise ValueError("Cloudflare documentation search workflow changed")
        for name, url in MCP_SERVERS.items():
            if name == "cloudflare-docs":
                continue
            status, headers, _ = curl_json_rpc(
                url, {"jsonrpc": "2.0", "id": 3, "method": "tools/list"}, root,
            )
            if status != 401 or "oauth-protected-resource" not in headers.lower():
                raise ValueError(f"unexpected {name} authentication boundary: HTTP {status}")


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    importer = load_importer()
    if importer.git_revision(source) != EXPECTED_REVISION:
        raise ValueError("Cloudflare source revision changed")
    if importer.normalized_git_remote(source) != importer.normalized_repository_url(
        "https://github.com/cloudflare/skills"
    ):
        raise ValueError("Cloudflare official repository origin changed")
    upstream = json.loads((source / ".claude-plugin/plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION:
        raise ValueError("official Cloudflare version changed")
    if manifest.get("$schema") != PLUGIN_SCHEMA or manifest.get("version") != f"{EXPECTED_VERSION}-ghast.1":
        raise ValueError("unexpected Cloudflare Agent Plugins 1.0 manifest")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("Cloudflare manifest revision differs")
    if not (plugin / ghast["icon"].removeprefix("./")).is_file():
        raise ValueError("Cloudflare icon is missing")
    urls = {name: server["url"] for name, server in mcp["mcpServers"].items()}
    if urls != MCP_SERVERS:
        raise ValueError("Cloudflare official MCP declarations changed")
    verify_checked_in_output(source, plugin, importer)
    verify_official_semgrep(source, args.semgrep)
    verify_public_mcp()
    print("verified Cloudflare official 13-skill, 375-file tree, two commands, Semgrep CI, live docs MCP workflow, four OAuth boundaries, Agent Plugins 1.0, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
