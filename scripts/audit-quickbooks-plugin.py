#!/usr/bin/env python3
"""Verify QuickBooks public MCP gaps against the current private app contract."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path


OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
OPENAI_HASHES = {
    ".app.json": "66697f0309cd7babbb2cc48bcc6d00033b3a132e5927ee6f018a2336f00ab6ad",
    ".codex-plugin/plugin.json": (
        "f906385b74f00de6c926fdbd8f215016cbfb7a9ca727ee8b5f7de2e8a3ce5ce6"
    ),
    "assets/logo.png": (
        "42e48fa87c5745e1e34cc970ced7be76fdb6dea83e66b06f5609c47409d50219"
    ),
}
OPENAI_INVENTORY_SHA256 = (
    "7cc71442b598b2bb20b66c1dddbb2908ba54b645408e1782b4574199657c8c46"
)
OFFICIAL_REVISION = "c351dc011d9cb14b211857457085f7994d8b1e15"
OFFICIAL_HASHES = {
    "LICENSE": "01668910a21c98711aef80c660ca3ac22a437ade84b51ba4969aa718f0b6969c",
    "README.md": (
        "1b9164e29332ceebe12e7f1852946dead0d74508f07ccb2f820fb793328b9f30"
    ),
    "package.json": (
        "839c063724d9c074c0fc8affa217c1129dbf986f2e6e07d2de4c5b117f58adf3"
    ),
    "package-lock.json": (
        "da718a6a1ff211c53025d09ba357ada7cd4ff3d73a9942ca5ed305ecc4c53ac7"
    ),
}
TRACKED_PATHS_SHA256 = (
    "6b2b9fc76d847923db904934264487a97df0779cd730a058adc6bb7dff74ee89"
)
TOOL_FILES_SHA256 = (
    "d8ef6980d86880ed5f818ab301f928c2c57e9a4de56ad5664f1bf77c7eb68df0"
)
ANNOUNCEMENT_URL = (
    "https://quickbooks.intuit.com/r/news/"
    "quickbooks-expands-into-claude-and-chatgpt-with-new-features/"
)
ANNOUNCEMENT_FETCH_URL = ANNOUNCEMENT_URL + "?output=1"
ANNOUNCEMENT_SHA256 = (
    "88027a69cf9fac2a50751886166e085fe380bdee87b7bb9288d1b137d2d4fa43"
)
NPM_URL = "https://registry.npmjs.org/@qboapi%2Fqbo-mcp-server"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--openai-source",
        type=Path,
        required=True,
        help="Pinned checkout of github.com/openai/plugins.",
    )
    parser.add_argument(
        "--official-source",
        type=Path,
        required=True,
        help="Pinned checkout of intuit/quickbooks-online-mcp-server.",
    )
    parser.add_argument(
        "--verify-announcement",
        action="store_true",
        help="Fetch and verify Intuit's intermittently available news page.",
    )
    return parser.parse_args()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git(repository: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def inventory_hash(plugin: Path) -> str:
    entries = []
    for path in sorted(item for item in plugin.rglob("*") if item.is_file()):
        value = path.read_bytes()
        entries.append(
            f"{path.relative_to(plugin).as_posix()}\0{sha256(value)}\0{len(value)}"
        )
    return sha256("\n".join(entries).encode())


def normalize_html(value: bytes) -> str:
    text = value.decode("utf-8", "replace")
    text = re.sub(
        r"<script[^>]*>.*?</script>", " ", text, flags=re.IGNORECASE | re.DOTALL
    )
    text = re.sub(
        r"<style[^>]*>.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL
    )
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def verify_announcement() -> None:
    raw = subprocess.run(
        [
            "curl",
            "--fail",
            "--location",
            "--http1.1",
            "--silent",
            "--show-error",
            "--max-time",
            "120",
            "--user-agent",
            "ghast-quickbooks-audit/1.0",
            ANNOUNCEMENT_FETCH_URL,
        ],
        check=True,
        capture_output=True,
    ).stdout
    text = normalize_html(raw)
    if sha256(text.encode()) != ANNOUNCEMENT_SHA256:
        raise ValueError("QuickBooks connector announcement changed")
    for marker in (
        "Published on",
        "July 28, 2026",
        "full sales quote-to-cash workflow",
        "deeper payroll query tools",
        "Who's on payroll?",
        "payslip history",
        "payroll readiness status",
        "peer loan benchmarking",
        "top 10% of QuickBooks businesses",
        "available now",
        "no extra setup required",
    ):
        if marker not in text:
            raise ValueError(f"QuickBooks announcement is missing {marker!r}")


def verify_openai(source: Path) -> None:
    if git(source, "rev-parse", "HEAD") != OPENAI_REVISION:
        raise ValueError("Unexpected OpenAI plugin snapshot")
    plugin = source / "plugins/quickbooks"
    actual = {
        path.relative_to(plugin).as_posix()
        for path in plugin.rglob("*")
        if path.is_file()
    }
    if actual != set(OPENAI_HASHES):
        raise ValueError("QuickBooks Codex file inventory changed")
    for relative, expected_hash in OPENAI_HASHES.items():
        if sha256((plugin / relative).read_bytes()) != expected_hash:
            raise ValueError(f"QuickBooks Codex evidence changed at {relative}")
    if inventory_hash(plugin) != OPENAI_INVENTORY_SHA256:
        raise ValueError("QuickBooks Codex inventory hash changed")

    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    app = json.loads((plugin / ".app.json").read_text())
    interface = manifest.get("interface", {})
    if (
        manifest.get("name") != "quickbooks"
        or manifest.get("version") != "1.0.3"
        or manifest.get("author", {}).get("name") != "QuickBooks"
        or interface.get("developerName") != "QuickBooks"
        or app.get("apps", {}).get("quickbooks", {}).get("id")
        != "asdk_app_697aea3231288191b28a0061066e51bd"
    ):
        raise ValueError("QuickBooks Codex identity changed")
    description = re.sub(r"\s+", " ", interface.get("longDescription", "")).strip()
    for marker in (
        "profitability",
        "cash flow",
        "accounts receivable and payable",
        "payroll",
        "Upload or paste transactions",
        "peer loan benchmarks",
    ):
        if marker not in description:
            raise ValueError(f"QuickBooks Codex capability is missing {marker!r}")


def verify_official_source(source: Path) -> None:
    if git(source, "rev-parse", "HEAD") != OFFICIAL_REVISION:
        raise ValueError("Unexpected Intuit QuickBooks MCP revision")
    if git(source, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("Intuit QuickBooks MCP tracked files are modified")
    tracked = git(source, "ls-files").splitlines()
    if sha256("\n".join(sorted(tracked)).encode()) != TRACKED_PATHS_SHA256:
        raise ValueError("Intuit QuickBooks MCP tracked inventory changed")
    for relative, expected_hash in OFFICIAL_HASHES.items():
        value = subprocess.run(
            ["git", "show", f"HEAD:{relative}"],
            cwd=source,
            check=True,
            capture_output=True,
        ).stdout
        if sha256(value) != expected_hash:
            raise ValueError(f"Intuit QuickBooks MCP evidence changed at {relative}")

    package = json.loads((source / "package.json").read_text())
    if (
        package.get("name") != "@qboapi/qbo-mcp-server"
        or package.get("version") != "0.0.1"
        or package.get("license") != "MIT"
    ):
        raise ValueError("QuickBooks package metadata changed")
    license_text = (source / "LICENSE").read_text()
    if "Apache License" not in license_text or "Version 2.0" not in license_text:
        raise ValueError("QuickBooks root Apache license changed")

    tool_files = sorted((source / "src/tools").glob("*.tool.ts"))
    tool_names = [path.stem.removesuffix(".tool") for path in tool_files]
    if len(tool_names) != 142 or sha256("\n".join(tool_names).encode()) != TOOL_FILES_SHA256:
        raise ValueError("QuickBooks public MCP tool inventory changed")
    categories = Counter(name.split("-", 1)[0] for name in tool_names)
    if categories != {
        "create": 25,
        "update": 26,
        "delete": 20,
        "get": 40,
        "search": 29,
        "read": 2,
    }:
        raise ValueError("QuickBooks public MCP tool categories changed")

    tool_text = "\n".join(path.read_text(errors="replace") for path in tool_files)
    for marker in (
        "payroll",
        "paycheck",
        "payslip",
        "pay run",
        "payroll readiness",
        "peer loan",
        "loan benchmark",
        "quickbooks capital",
    ):
        if marker in tool_text.lower():
            raise ValueError(
                f"QuickBooks public MCP may now cover {marker!r}; re-audit"
            )


def verify_npm_blocker() -> None:
    request = urllib.request.Request(
        NPM_URL,
        headers={"User-Agent": "ghast-quickbooks-audit/1.0"},
    )
    try:
        urllib.request.urlopen(request, timeout=60)
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise ValueError("Unexpected QuickBooks npm registry response") from error
    else:
        raise ValueError(
            "QuickBooks MCP package is now published; re-audit distribution"
        )


def main() -> int:
    args = parse_args()
    if args.verify_announcement:
        verify_announcement()
    verify_openai(args.openai_source.resolve())
    verify_official_source(args.official_source.resolve())
    verify_npm_blocker()
    if Path("plugins/quickbooks").exists() or Path("packages/quickbooks.zip").exists():
        raise ValueError(
            "QuickBooks must remain unpublished until the official public "
            "implementation covers payroll, transaction ingestion, and peer "
            "loan benchmarks or the Codex contract is narrowed"
        )
    print("verified QuickBooks private-connector capability and distribution gaps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
