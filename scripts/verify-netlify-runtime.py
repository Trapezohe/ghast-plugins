#!/usr/bin/env python3
"""Verify Netlify's pinned official generated outputs and Ghast package."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
import urllib.error
from pathlib import Path
from types import ModuleType


EXPECTED_REVISION = "32a261b6b2437464aca7e51bf9b48bcac1e2835c"
EXPECTED_VERSION = "1.3.0"
EXPECTED_SKILLS = 15
EXPECTED_FILES = 37
VALIDATOR_VERSION = "1.5.6"
VALIDATOR_SHA256 = {
    ("Darwin", "arm64"): "38f838c4103e0fd1897154ba0236ce59218011ba2c639c0cadf9f36e4e7a6572",
    ("Linux", "x86_64"): "c97faee388056023c616e312927faffd07e028bcd76d799e42da612dad7972df",
}
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
IMPORTER_PATH = REPOSITORY_ROOT / "scripts/import-official-third-party-plugins.py"
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_URL = "https://netlify-mcp.netlify.app/mcp"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=REPOSITORY_ROOT / "plugins/netlify")
    parser.add_argument("--skill-validator", type=Path)
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


def resolve_validator(explicit: Path | None, root: Path) -> Path:
    if explicit:
        binary = explicit.expanduser().resolve()
    else:
        system = platform.system()
        machine = platform.machine()
        checksum = VALIDATOR_SHA256.get((system, machine))
        if checksum is None:
            raise ValueError(f"unsupported skill-validator platform: {system}/{machine}")
        os_name = "darwin" if system == "Darwin" else "linux"
        arch = "arm64" if machine == "arm64" else "amd64"
        archive = root / "skill-validator.tar.gz"
        url = (
            "https://github.com/agent-ecosystem/skill-validator/releases/download/"
            f"v{VALIDATOR_VERSION}/skill-validator_{VALIDATOR_VERSION}_{os_name}_{arch}.tar.gz"
        )
        urllib.request.urlretrieve(url, archive)
        actual = hashlib.sha256(archive.read_bytes()).hexdigest()
        if actual != checksum:
            raise ValueError(f"skill-validator checksum differs: {actual}")
        with tarfile.open(archive) as package:
            member = package.getmember("skill-validator")
            package.extract(member, root, filter="data")
        binary = root / "skill-validator"
        binary.chmod(0o755)
    output = run([str(binary), "--version"], capture_output=True).stdout
    if VALIDATOR_VERSION not in output:
        raise ValueError(f"unexpected skill-validator version: {output.strip()}")
    return binary


def verify_output(source: Path, plugin: Path, importer: ModuleType) -> None:
    expected = file_map(source / "agent-plugin/skills")
    actual = file_map(plugin / "skills")
    if expected.keys() != actual.keys() or len(expected) != EXPECTED_FILES:
        raise ValueError("Netlify official and Ghast skill file sets differ")
    if sum(name.count("/") == 1 and name.endswith("/SKILL.md") for name in expected) != EXPECTED_SKILLS:
        raise ValueError("unexpected Netlify skill count")
    with tempfile.TemporaryDirectory(prefix="ghast-netlify-normalized-") as temp:
        normalized = Path(temp) / "skills"
        importer.copy_skill_tree(
            source / "agent-plugin/skills", normalized, recursive=False,
            preserve_agent_metadata=False, frontmatter_overrides={},
        )
        expected_normalized = file_map(normalized)
        for relative, expected_path in expected_normalized.items():
            actual_path = actual[relative]
            if relative.endswith("/SKILL.md"):
                if split_skill(expected_path) != split_skill(actual_path):
                    raise ValueError(f"{relative}: body differs from official source")
            elif expected_path.read_bytes() != actual_path.read_bytes():
                raise ValueError(f"{relative}: differs from official source")


def verify_official_ci(source: Path, explicit_validator: Path | None) -> None:
    with tempfile.TemporaryDirectory(prefix="ghast-netlify-runtime-") as temp:
        root = Path(temp)
        archive = root / "source.tar"
        checkout = root / "checkout"
        checkout.mkdir()
        run(["git", "archive", "--output", str(archive), EXPECTED_REVISION], cwd=source)
        with tarfile.open(archive) as package:
            package.extractall(checkout, filter="data")
        run(["git", "init", "--quiet"], cwd=checkout)
        run(["git", "add", "."], cwd=checkout)
        run(
            [
                "git", "-c", "user.name=Ghast Verifier",
                "-c", "user.email=verifier@invalid.example",
                "commit", "--quiet", "-m", "verification baseline",
            ],
            cwd=checkout,
        )
        for script in ("build-cursor-rules.sh", "build-codex-skills.sh", "build-agent-plugin.sh"):
            run(["bash", f"scripts/{script}"], cwd=checkout)
        for generated in ("cursor", "codex", "agent-plugin/skills"):
            run(["git", "diff", "--exit-code", "--", generated], cwd=checkout)
        validator = resolve_validator(explicit_validator, root)
        run([str(validator), "check", "--strict", "--emit-annotations", "skills/"], cwd=checkout)


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
            raise ValueError(f"unexpected Netlify MCP auth boundary: HTTP {error.code}") from error
    else:
        raise ValueError("Netlify MCP unexpectedly allowed unauthenticated tools/list")


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    importer = load_importer()
    if importer.git_revision(source) != EXPECTED_REVISION:
        raise ValueError("Netlify source revision changed")
    if importer.normalized_git_remote(source) != importer.normalized_repository_url(
        "https://github.com/netlify/context-and-tools"
    ):
        raise ValueError("Netlify official repository origin changed")
    upstream = json.loads((source / "agent-plugin/plugin.json").read_text())
    manifest = json.loads((plugin / "plugin.json").read_text())
    mcp = json.loads((plugin / "mcp.json").read_text())
    if upstream.get("version") != EXPECTED_VERSION:
        raise ValueError("official Netlify version changed")
    if manifest.get("$schema") != PLUGIN_SCHEMA or manifest.get("version") != f"{EXPECTED_VERSION}-ghast.1":
        raise ValueError("unexpected Netlify Agent Plugins 1.0 manifest")
    ghast = manifest["extensions"]["ai.trapezohe.ghast"]
    if ghast.get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("Netlify manifest revision differs")
    if not (plugin / ghast["icon"].removeprefix("./")).is_file():
        raise ValueError("Netlify icon is missing")
    if mcp["mcpServers"]["netlify"].get("url") != MCP_URL:
        raise ValueError("Netlify official MCP endpoint changed")
    verify_output(source, plugin, importer)
    verify_official_ci(source, args.skill_validator)
    verify_auth_boundary()
    print("verified Netlify 1.3.0 official generated outputs, 15 skills, strict validation, authenticated MCP boundary, Agent Plugins 1.0, and icon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
