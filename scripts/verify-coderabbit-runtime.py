#!/usr/bin/env python3
"""Verify the pinned official CodeRabbit CLI release without authenticating."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import platform
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path


EXPECTED_REVISION = "aa49953c4cb2590e35480637b1b6a29cf4187cfa"
VERSION = "0.7.5"
VERSION_URL = "https://cli.coderabbit.ai/releases/latest/VERSION"
VERSION_SHA256 = "966f2f8695b5c07de3f37c682b1409da1ac84b5c7ce04a27068bb4c017ac0cb8"
INSTALLER_URL = "https://cli.coderabbit.ai/install.sh"
INSTALLER_SHA256 = "4ffc7fb7443f0c562adea5c998867bcbe772a14d0e6620d328dfa6045afe446d"
ARCHIVE_URL = (
    "https://cli.coderabbit.ai/releases/0.7.5/"
    "coderabbit-darwin-arm64.zip"
)
ARCHIVE_SHA256 = "5add1edd7269ceda01303bfd6cd9ce6b1fa204d7dd9c89bed412c36680caf020"
BINARY_SHA256 = "4cfc671318a4449a6ac20a174f7ff8a372eecab2fdd07049be21a0e466a09a0a"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    return parser.parse_args()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "ghast-audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def require_hash(label: str, value: bytes, expected: str) -> None:
    actual = hashlib.sha256(value).hexdigest()
    if actual != expected:
        raise ValueError(f"{label} SHA-256 {actual} != {expected}")


def run(binary: Path, *args: str, environment: dict[str, str]) -> str:
    return subprocess.run(
        [str(binary), *args],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    ).stdout


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if revision != EXPECTED_REVISION:
        raise ValueError(f"expected {EXPECTED_REVISION}, found {revision}")
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        raise RuntimeError("this pinned runtime check requires macOS arm64")

    version = fetch(VERSION_URL)
    require_hash("CodeRabbit VERSION", version, VERSION_SHA256)
    if version.decode().strip() != VERSION:
        raise ValueError(f"unexpected CodeRabbit version: {version!r}")
    installer = fetch(INSTALLER_URL)
    require_hash("CodeRabbit installer", installer, INSTALLER_SHA256)
    for marker in (
        b"CODERABBIT_INSTALL_DIR",
        b"coderabbit-${OS}-${ARCH}.zip",
        b"coderabbit auth login",
    ):
        if marker not in installer:
            raise ValueError(f"CodeRabbit installer is missing {marker!r}")

    archive = fetch(ARCHIVE_URL)
    require_hash("CodeRabbit archive", archive, ARCHIVE_SHA256)
    with zipfile.ZipFile(io.BytesIO(archive)) as package:
        if package.namelist() != ["coderabbit"]:
            raise ValueError(f"unexpected CodeRabbit archive: {package.namelist()}")
        binary_bytes = package.read("coderabbit")
    require_hash("CodeRabbit binary", binary_bytes, BINARY_SHA256)

    with tempfile.TemporaryDirectory(prefix="ghast-coderabbit-runtime-") as temp:
        root = Path(temp)
        binary = root / "coderabbit"
        binary.write_bytes(binary_bytes)
        binary.chmod(0o755)
        environment = os.environ.copy()
        environment["HOME"] = str(root / "home")
        Path(environment["HOME"]).mkdir()

        if run(binary, "--version", environment=environment).strip() != VERSION:
            raise ValueError("CodeRabbit binary reported an unexpected version")
        auth = json.loads(
            run(binary, "auth", "status", "--agent", environment=environment)
        )
        if auth.get("authenticated") is not False:
            raise ValueError(f"unexpected CodeRabbit auth status: {auth!r}")

        review_help = run(binary, "review", "--help", environment=environment)
        for marker in (
            "--committed",
            "--uncommitted",
            "--include-untracked",
            "--agent",
            "findings",
        ):
            if marker not in review_help:
                raise ValueError(f"CodeRabbit review help is missing {marker}")
        findings_help = run(
            binary, "review", "findings", "--help", environment=environment
        )
        if "--dir" not in findings_help:
            raise ValueError("CodeRabbit findings help is missing --dir")
        if "Install or update every skill" not in run(
            binary, "skills", "--help", environment=environment
        ):
            raise ValueError("CodeRabbit skills command is unavailable")

    print("verified CodeRabbit 0.7.5 release, command surface, and auth boundary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
