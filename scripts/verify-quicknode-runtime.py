#!/usr/bin/env python3
"""Verify the pinned official QuickNode CLI release without authenticating."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import platform
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path


EXPECTED_REVISION = "4265b0a97048d8e64dae0124013c66b8dd34533f"
VERSION = "0.6.1"
RELEASE_API = "https://api.github.com/repos/quicknode/cli/releases/latest"
ARCHIVE_NAME = "quicknode-cli-aarch64-apple-darwin.tar.xz"
ARCHIVE_SHA256 = "51d096f798c128e96cb311328e3114894c43314ef15c914b3c6fc5708905570f"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    return parser.parse_args()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "ghast-audit/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


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

    release = json.loads(fetch(RELEASE_API))
    if release.get("tag_name") != f"v{VERSION}":
        raise ValueError(f"unexpected QuickNode release: {release.get('tag_name')}")
    asset = next(
        (
            candidate
            for candidate in release.get("assets", [])
            if candidate["name"] == ARCHIVE_NAME
        ),
        None,
    )
    if asset is None or asset.get("digest") != f"sha256:{ARCHIVE_SHA256}":
        raise ValueError(f"QuickNode release digest changed: {asset!r}")
    archive = fetch(asset["browser_download_url"])
    actual_hash = hashlib.sha256(archive).hexdigest()
    if actual_hash != ARCHIVE_SHA256:
        raise ValueError(f"QuickNode archive SHA-256 {actual_hash} != {ARCHIVE_SHA256}")

    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as package:
        binary_member = next(
            (member for member in package.getmembers() if member.name.endswith("/qn")),
            None,
        )
        if binary_member is None or not binary_member.isfile():
            raise ValueError("QuickNode archive does not contain qn")
        extracted = package.extractfile(binary_member)
        if extracted is None:
            raise ValueError("QuickNode qn member could not be read")
        binary_bytes = extracted.read()

    with tempfile.TemporaryDirectory(prefix="ghast-quicknode-runtime-") as temp:
        root = Path(temp)
        binary = root / "qn"
        binary.write_bytes(binary_bytes)
        binary.chmod(0o755)
        environment = os.environ.copy()
        environment["HOME"] = str(root / "home")
        Path(environment["HOME"]).mkdir()

        if run(binary, "--version", environment=environment).strip() != f"qn {VERSION}":
            raise ValueError("QuickNode binary reported an unexpected version")
        context = json.loads(
            run(binary, "agent", "context", "-o", "json", environment=environment)
        )
        if context.get("version") != VERSION or "# qn" not in context.get("guide", ""):
            raise ValueError(f"unexpected QuickNode agent context: {context!r}")

        help_expectations = {
            ("endpoint", "--help"): ("create", "logs", "metrics", "security", "rate-limit"),
            ("usage", "--help"): ("summary", "by-endpoint", "by-method", "by-chain"),
            ("billing", "--help"): ("invoices", "payments"),
            ("endpoint", "security", "--help"): ("token", "referrer", "ip", "jwt"),
            ("endpoint", "rate-limit", "--help"): ("get", "set", "method-create"),
        }
        for command, markers in help_expectations.items():
            output = run(binary, *command, environment=environment)
            for marker in markers:
                if marker not in output:
                    raise ValueError(f"QuickNode {' '.join(command)} is missing {marker}")

        auth = subprocess.run(
            [str(binary), "auth", "whoami"],
            capture_output=True,
            text=True,
            env=environment,
        )
        if auth.returncode == 0 or "no API key found" not in auth.stderr:
            raise ValueError(f"unexpected QuickNode auth boundary: {auth!r}")

    print("verified QuickNode 0.6.1 release, agent context, command surface, and auth boundary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
