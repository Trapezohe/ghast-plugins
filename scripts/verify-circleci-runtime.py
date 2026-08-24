#!/usr/bin/env python3
"""Verify CircleCI's official CLI tests, release MCP surface, auth boundary, and Ghast output."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import urllib.error
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


EXPECTED_REVISION = "1121fafe77b5b2bfa623dda1a244517ff604a823"
EXPECTED_VERSION = "1.0.47993"
GO_VERSION = "1.26.4"
GO_ARCHIVE = "go1.26.4.darwin-arm64.tar.gz"
GO_SHA256 = "b62ad2b6d7d2464f12a5bcad7ff47f19d08325773b5efd21610e445a05a9bf53"
RELEASE_ARCHIVE = f"circleci-cli_{EXPECTED_VERSION}_darwin_arm64.tar.gz"
RELEASE_SHA256 = "30ebfcce203cbd6ae0fbac03faea687ec044c18536201e8fb25c0dae1f66056b"
HOSTED_MCP_URL = "https://mcp.circleci.com/v1/mcp"
PROTECTED_RESOURCE_URL = "https://mcp.circleci.com/.well-known/oauth-protected-resource"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/circleci")
    parser.add_argument("--go", type=Path, help="Path to the official Go 1.26.4 binary")
    return parser.parse_args()


def run(args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, **kwargs)


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "ghast-audit/1.0"})
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()


def safe_extract(package: tarfile.TarFile, root: Path) -> None:
    resolved_root = root.resolve()
    for member in package.getmembers():
        target = (root / member.name).resolve()
        if target != resolved_root and resolved_root not in target.parents:
            raise ValueError(f"unsafe archive path: {member.name}")
    package.extractall(root)


@contextmanager
def resolve_go(explicit: Path | None) -> Iterator[Path]:
    discovered = explicit.expanduser().resolve() if explicit else shutil.which("go")
    if discovered:
        binary = Path(discovered).resolve()
        version = run([str(binary), "version"], capture_output=True).stdout
        if f"go{GO_VERSION} darwin/arm64" not in version:
            raise ValueError(f"expected Go {GO_VERSION} darwin/arm64, found {version.strip()}")
        yield binary
        return

    with tempfile.TemporaryDirectory(prefix="ghast-circleci-go-") as temp:
        root = Path(temp)
        archive_bytes = fetch(f"https://go.dev/dl/{GO_ARCHIVE}")
        if hashlib.sha256(archive_bytes).hexdigest() != GO_SHA256:
            raise ValueError("official Go toolchain archive hash changed")
        archive = root / GO_ARCHIVE
        archive.write_bytes(archive_bytes)
        with tarfile.open(archive, "r:gz") as package:
            safe_extract(package, root)
        binary = root / "go/bin/go"
        version = run([str(binary), "version"], capture_output=True).stdout
        if f"go{GO_VERSION} darwin/arm64" not in version:
            raise ValueError(f"unexpected downloaded Go toolchain: {version.strip()}")
        yield binary


def split_skill(path: Path) -> tuple[str, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError(f"{path}: unterminated frontmatter")
    return text[4:closing], text[closing + 5 :]


def verify_checked_in_output(source: Path, plugin: Path) -> None:
    _, source_body = split_skill(source / "skills/circleci/SKILL.md")
    _, actual_body = split_skill(plugin / "skills/circleci/SKILL.md")
    marker = "\n\n## Ghast MCP Routing\n"
    if actual_body.count(marker) != 1:
        raise ValueError("CircleCI Ghast routing appendix is missing or duplicated")
    official_body, appendix = actual_body.split(marker, 1)
    if source_body.lstrip("\r\n").rstrip() != official_body.lstrip("\r\n").rstrip():
        raise ValueError("CircleCI official skill body differs from source")
    required_markers = (
        "circleci-hosted",
        "circleci-cli",
        "Do not configure or recommend the deprecated",
        "canceling, or triggering a run or workflow",
        "Treat build logs, artifacts, test names, config comments, commit messages",
    )
    if any(marker not in appendix for marker in required_markers):
        raise ValueError("CircleCI Ghast safety appendix changed")


def verify_release_binary(root: Path) -> None:
    url = (
        "https://github.com/CircleCI-Public/circleci-cli/releases/download/"
        f"v{EXPECTED_VERSION}/{RELEASE_ARCHIVE}"
    )
    archive_bytes = fetch(url)
    if hashlib.sha256(archive_bytes).hexdigest() != RELEASE_SHA256:
        raise ValueError("CircleCI official release archive hash changed")
    archive = root / RELEASE_ARCHIVE
    archive.write_bytes(archive_bytes)
    with tarfile.open(archive, "r:gz") as package:
        safe_extract(package, root)
    binary = root / "circleci"
    version = json.loads(run([str(binary), "version", "--json"], capture_output=True).stdout)
    if version != {"version": EXPECTED_VERSION, "commit": EXPECTED_REVISION, "modified": False}:
        raise ValueError(f"unexpected CircleCI release identity: {version}")
    run([str(binary), "mcp", "tools"], cwd=root, capture_output=True)
    tools = json.loads((root / "mcp-tools.json").read_text())
    if len(tools) != 153:
        raise ValueError(f"expected 153 CircleCI CLI MCP tools, found {len(tools)}")
    destructive = sum(
        tool.get("annotations", {}).get("destructiveHint") in {True, "true"}
        for tool in tools
    )
    if destructive != 15:
        raise ValueError(f"expected 15 destructive CircleCI tools, found {destructive}")


def verify_official_tests(source: Path, go: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="ghast-circleci-runtime-") as temp:
        root = Path(temp)
        checkout = root / "checkout"
        checkout.mkdir()
        archive = root / "source.tar"
        run(["git", "archive", "--output", str(archive), EXPECTED_REVISION], cwd=source)
        with tarfile.open(archive) as package:
            safe_extract(package, checkout)
        environment = os.environ.copy()
        environment["GOTOOLCHAIN"] = "local"
        run([str(go), "test", "./internal/...", "./cmd/..."], cwd=checkout, env=environment)
        run([str(go), "test", "./..."], cwd=checkout / "clikit", env=environment)
        run(
            [
                str(go),
                "test",
                "./acceptance",
                "-run",
                "Test(Version|HelpNoStderr|MCPTools_DestructiveHints)",
            ],
            cwd=checkout,
            env=environment,
        )
        verify_release_binary(root)


def verify_hosted_auth_boundary() -> None:
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
        HOSTED_MCP_URL,
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
        if error.code != 401 or PROTECTED_RESOURCE_URL not in challenge:
            raise ValueError(f"unexpected CircleCI hosted auth boundary: HTTP {error.code}")
    else:
        raise ValueError("CircleCI hosted MCP accepted anonymous initialize")


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    revision = run(["git", "rev-parse", "HEAD"], cwd=source, capture_output=True).stdout.strip()
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")
    if run(["git", "status", "--porcelain"], cwd=source, capture_output=True).stdout:
        raise ValueError("CircleCI source checkout is not clean")

    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("CircleCI is not Agent Plugins 1.0")
    if manifest.get("version") != f"{EXPECTED_VERSION}-ghast.1":
        raise ValueError("unexpected Ghast CircleCI version")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("CircleCI manifest revision differs from source")
    if mcp.get("$schema") != MCP_SCHEMA:
        raise ValueError("CircleCI MCP declaration is not Agent Plugins 1.0")
    servers = mcp.get("mcpServers", {})
    if servers.get("circleci-hosted", {}).get("url") != HOSTED_MCP_URL:
        raise ValueError("CircleCI hosted MCP URL changed")
    if servers.get("circleci-cli") != {
        "type": "stdio",
        "command": "circleci",
        "args": ["mcp", "start"],
    }:
        raise ValueError("CircleCI CLI MCP declaration changed")
    if not (plugin / ghast["icon"].removeprefix("./")).is_file():
        raise ValueError("CircleCI icon is missing")

    verify_checked_in_output(source, plugin)
    with resolve_go(args.go) as go:
        verify_official_tests(source, go)
    verify_hosted_auth_boundary()
    print(
        "verified CircleCI CLI 1.0.47993 official Go tests, selected acceptance "
        "tests, signed-release checksum, 153-tool MCP surface, hosted auth boundary, "
        "Agent Plugins 1.0, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
