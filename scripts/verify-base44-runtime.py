#!/usr/bin/env python3
"""Verify the pinned official Base44 skills and CLI contract without login."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path


EXPECTED_REVISION = "773a301cfb79112141add32d19c024f2bafc44ee"
CLI_VERSION = "0.1.7"
NPM_METADATA = f"https://registry.npmjs.org/base44/{CLI_VERSION}"
NPM_INTEGRITY = (
    "sha512-8x8nc2qnNF+OGl+2MWs1rQFMYJouSCBkJaZfUtEHgGbB+TsZYMwF6ORxmRYA1Ws4"
    "bDus0PqUDLfuHjpFpaLOMw=="
)
PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
GHAST_AUTH_NOTE = """

> **Ghast runtime note:** In Base44 CLI 0.1.7, `npx base44 whoami`
> can begin a device-code login and wait when no credential is configured.
> Treat any emitted verification URL and code as an interactive authentication
> transition, not as passive status output. Relay it only to the user who
> requested the Base44 operation, do not persist it, do not start a second
> login flow, and wait for that flow to finish or be cancelled before retrying.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--plugin", type=Path, default=Path("plugins/base44"))
    return parser.parse_args()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "ghast-audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def run(arguments: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(arguments, check=True, text=True, **kwargs)


def split_skill(path: Path) -> tuple[str, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError(f"{path}: unterminated frontmatter")
    return text[4:closing], text[closing + 5 :]


def verify_skill_tree(source: Path, plugin: Path) -> None:
    source_root = source / "skills"
    plugin_root = plugin / "skills"
    source_files = {
        path.relative_to(source_root).as_posix(): path
        for path in source_root.rglob("*")
        if path.is_file()
    }
    plugin_files = {
        path.relative_to(plugin_root).as_posix(): path
        for path in plugin_root.rglob("*")
        if path.is_file()
    }
    if source_files.keys() != plugin_files.keys():
        raise ValueError("Base44 source and Ghast skill file sets differ")
    if len(source_files) != 62:
        raise ValueError(f"expected 62 Base44 skill files, found {len(source_files)}")

    for relative, source_path in source_files.items():
        plugin_path = plugin_files[relative]
        if relative.count("/") == 1 and relative.endswith("/SKILL.md"):
            _, source_body = split_skill(source_path)
            _, plugin_body = split_skill(plugin_path)
            source_body = source_body.lstrip("\r\n")
            plugin_body = plugin_body.lstrip("\r\n")
            if relative == "base44-cli/SKILL.md":
                if plugin_body.count(GHAST_AUTH_NOTE) != 1:
                    raise ValueError("Base44 Ghast authentication note is missing")
                plugin_body = plugin_body.replace(GHAST_AUTH_NOTE, "", 1)
            if source_body != plugin_body:
                raise ValueError(f"{relative}: skill body differs from official source")
        elif source_path.read_bytes() != plugin_path.read_bytes():
            raise ValueError(f"{relative}: file differs from official source")


def verify_npm_cli() -> None:
    metadata = json.loads(fetch(NPM_METADATA))
    if metadata.get("version") != CLI_VERSION:
        raise ValueError(f"unexpected Base44 npm version: {metadata.get('version')}")
    distribution = metadata.get("dist", {})
    if distribution.get("integrity") != NPM_INTEGRITY:
        raise ValueError("Base44 npm integrity changed")
    repository = metadata.get("repository", {}).get("url", "")
    if "github.com/base44/cli" not in repository:
        raise ValueError(f"unexpected Base44 CLI repository: {repository}")
    archive = fetch(distribution["tarball"])
    expected = base64.b64decode(NPM_INTEGRITY.removeprefix("sha512-"))
    if hashlib.sha512(archive).digest() != expected:
        raise ValueError("Base44 npm tarball does not match its SRI digest")

    with tempfile.TemporaryDirectory(prefix="ghast-base44-cli-") as temp:
        root = Path(temp)
        archive_path = root / "base44.tgz"
        archive_path.write_bytes(archive)
        with tarfile.open(archive_path, "r:gz") as package:
            for member in package.getmembers():
                target = (root / member.name).resolve()
                if root.resolve() not in target.parents and target != root.resolve():
                    raise ValueError(f"unsafe Base44 npm path: {member.name}")
            package.extractall(root)
        package_root = root / "package"
        package_json = json.loads((package_root / "package.json").read_text())
        if package_json.get("bin") != {"base44": "./bin/run.js"}:
            raise ValueError("Base44 npm binary declaration changed")
        binary = package_root / "bin/run.js"
        environment = os.environ.copy()
        for key in list(environment):
            if key.startswith("BASE44_"):
                environment.pop(key)
        environment["HOME"] = str(root / "home")
        Path(environment["HOME"]).mkdir()

        version = run(
            ["node", str(binary), "--version"],
            capture_output=True,
            env=environment,
        ).stdout.strip()
        if version != CLI_VERSION:
            raise ValueError(f"Base44 CLI reported {version}")
        help_text = run(
            ["node", str(binary), "--help"],
            capture_output=True,
            env=environment,
        ).stdout
        commands = {
            "agent-skills",
            "agents",
            "auth",
            "connectors",
            "create",
            "deploy",
            "dev",
            "eject",
            "entities",
            "exec",
            "functions",
            "link",
            "logs",
            "sandbox",
            "scaffold",
            "secrets",
            "site",
            "types",
            "visibility",
            "whoami",
            "workspace",
        }
        missing = sorted(command for command in commands if f"  {command}" not in help_text)
        if missing:
            raise ValueError(f"Base44 CLI help is missing commands: {missing}")
        for command in ("connectors", "sandbox", "whoami"):
            run(
                ["node", str(binary), command, "--help"],
                capture_output=True,
                env=environment,
            )


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    plugin = args.plugin.resolve()
    revision = run(
        ["git", "rev-parse", "HEAD"], cwd=source, capture_output=True
    ).stdout.strip()
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")
    if (source / "CLI_VERSION").read_text().strip() != f"v{CLI_VERSION}":
        raise ValueError("Base44 skills no longer pin the expected CLI version")
    run(["node", "scripts/validate-template.mjs"], cwd=source)

    manifest = json.loads((plugin / "plugin.json").read_text())
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        raise ValueError("Base44 is not Agent Plugins 1.0")
    if manifest["extensions"]["ai.trapezohe.ghast"].get("upstreamRevision") != EXPECTED_REVISION:
        raise ValueError("Base44 Ghast revision differs from official source")
    if not (plugin / "assets/icon.png").is_file():
        raise ValueError("Base44 icon is missing")

    verify_skill_tree(source, plugin)
    verify_npm_cli()
    print(
        "verified Base44 official validator, 62-file skill tree, npm SRI, "
        "CLI 0.1.7 command surface, Agent Plugins 1.0 manifest, and icon"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
