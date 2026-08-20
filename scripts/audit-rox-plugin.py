#!/usr/bin/env python3
"""Verify Rox evidence and enforce its private-MCP portability blocker."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import urllib.request
from pathlib import Path


EXPECTED_OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
ROX_LLMS_URL = "https://docs.rox.com/development/llms.txt"
ROX_LLMS_SHA256 = (
    "f79878ebe137dca9dcc3c16e633fcbbdbafa6f838ea8ea74ff5a81e95ce9e5bc"
)
ROX_LLMS_FULL_URL = "https://docs.rox.com/development/llms-full.txt"
ROX_LLMS_FULL_SHA256 = (
    "ef14971217979c91d77374a796086ab9894c9b0a8a0d8200d9d39fbb12eb741f"
)
ROX_RELEASE_NOTES_URL = (
    "https://docs.rox.com/development/about-rox/release-notes.md"
)
ROX_RELEASE_NOTES_SHA256 = (
    "af27fa5014f2d73b0cd6b95618b20553ab0f21bd8a4349415b6a50e873d280ba"
)
ROX_APPS_SECTION_SHA256 = (
    "243986ca5c437152f35673bb30638ff0a8cf4b7e8eb2c0627b2aa37c03ed21e9"
)
ROX_TETHER_URL = "https://www.rox.com/articles/tether"
ROX_TETHER_CORE_SHA256 = (
    "390bcd80a721b4181ed9d5101d8d29cf8d2fa21ce9664665bd310ec1ad62d41e"
)
ROX_TERMS_URL = "https://www.rox.com/legal/terms-and-conditions"
ROX_TERMS_RESTRICTIONS_SHA256 = (
    "7332619a3045bf2c72cedd3fbf144fab6be58ed8ea47e5437a573912096bb3c6"
)
ROX_GITHUB_ORG_URL = "https://api.github.com/orgs/Rox-AI"
ROX_GITHUB_ORG_SHA256 = (
    "b15b3eb6ab37281194a87cbc5c987ef4a340ea4d555c951643718f7215714980"
)
ROX_GITHUB_REPOS_URL = (
    "https://api.github.com/orgs/Rox-AI/repos?per_page=100&type=public"
)
ROX_GITHUB_REPOS_SHA256 = (
    "738b402429a9247aa2373a79c7b00eb20139f554b2a10de558f24827baefb25d"
)
OPENAI_HASHES = {
    ".app.json": (
        "ca27e99ed269b614197c15f180b84d4bc8eaeb9a0c155abf18c90b03adff02cf"
    ),
    ".codex-plugin/plugin.json": (
        "c25162ed812569fa8f70e28aa82df12b155d07a2ec9d2da7b25ffbfd934b823a"
    ),
    "assets/app-icon.png": (
        "399190c9e8055dda31a2a295b5bd0122c5f016ab543cf8f01e0d2e1e9e80a3d7"
    ),
}
OPENAI_INVENTORY_SHA256 = (
    "49035b97364e7617ddb3ca1f8d675806645ed233bb01c545cb8f0464d4af733f"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--openai-source",
        type=Path,
        required=True,
        help="Pinned checkout of github.com/openai/plugins.",
    )
    return parser.parse_args()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    return sha256(encoded)


def fetch(url: str, accept: str = "*/*") -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "User-Agent": "ghast-rox-audit/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


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


def section(value: str, start_marker: str, end_marker: str) -> str:
    start = value.find(start_marker)
    if start < 0:
        raise ValueError(f"Rox evidence is missing {start_marker!r}")
    end = value.find(end_marker, start + len(start_marker))
    if end < 0:
        raise ValueError(f"Rox evidence is missing {end_marker!r}")
    return value[start:end].strip()


def verify_documentation_boundary() -> None:
    llms_raw = fetch(ROX_LLMS_URL, "text/markdown")
    if sha256(llms_raw) != ROX_LLMS_SHA256:
        raise ValueError("Rox llms.txt changed; re-audit required")
    llms = llms_raw.decode()
    links = re.findall(r"\[[^\]]*\]\((https?://[^)]+)\)", llms)
    if len(links) != 186 or len(set(links)) != 186:
        raise ValueError("Rox documentation inventory changed; re-audit required")
    if any(
        marker in link.lower()
        for link in links
        for marker in (
            "/mcp",
            "codex",
            "chatgpt",
            "api-reference",
            "developer-api",
            "/api/",
        )
    ):
        raise ValueError(
            "Rox published a candidate connector or developer API path; "
            "re-audit required"
        )

    full_raw = fetch(ROX_LLMS_FULL_URL, "text/markdown")
    if sha256(full_raw) != ROX_LLMS_FULL_SHA256:
        raise ValueError("Rox llms-full.txt changed; re-audit required")
    full = full_raw.decode()
    for marker in ("Model Context Protocol", "Codex"):
        if marker.lower() in full.lower():
            raise ValueError(
                f"Rox documentation now mentions {marker}; re-audit required"
            )


def verify_official_product_evidence() -> None:
    release_raw = fetch(ROX_RELEASE_NOTES_URL, "text/markdown")
    if sha256(release_raw) != ROX_RELEASE_NOTES_SHA256:
        raise ValueError("Rox release notes changed; re-audit required")
    release_notes = release_raw.decode()
    apps = section(
        release_notes,
        "## July 29th, 2026",
        "\n## July 22nd, 2026",
    )
    if sha256(apps.encode()) != ROX_APPS_SECTION_SHA256:
        raise ValueError("Rox Apps release-note section changed")
    for marker in (
        "purpose-built apps that run on the data Rox already holds",
        "Adoption Metrics",
        "Apps are read-only",
        "do not write back to your CRM",
    ):
        if marker not in apps:
            raise ValueError(f"Rox Apps evidence is missing {marker!r}")

    tether = normalize_html(fetch(ROX_TETHER_URL, "text/html"))
    tether_core = section(
        tether,
        "Jul 26, 2026 Jul 26, 2026 Taeuk",
        " References",
    )
    tether_core = f"{tether_core} References"
    if sha256(tether_core.encode()) != ROX_TETHER_CORE_SHA256:
        raise ValueError("Rox Tether architecture article changed")
    for marker in (
        "reps connect MCP servers to their agent",
        "an MCP server and a web app for the same product already share a backend "
        "and a user identity",
        "OAuth",
        "headless-first",
        "Handles, not copies",
        "context_sync",
        "channel-separated authority",
    ):
        if marker not in tether_core:
            raise ValueError(f"Rox Tether evidence is missing {marker!r}")


def verify_terms() -> None:
    terms = normalize_html(fetch(ROX_TERMS_URL, "text/html"))
    restrictions = section(
        terms,
        "Restrictions and responsibilities 2.1",
        "2.2 Customer",
    )
    if sha256(restrictions.encode()) != ROX_TERMS_RESTRICTIONS_SHA256:
        raise ValueError("Rox service-license restrictions changed")
    for marker in (
        "hosted software will be installed, accessed and maintained only by or "
        "for Service Provider and no license is granted thereto",
        "internal use only",
        "reverse engineer, decompile, disassemble",
        "create derivative works",
        "rent, lease, distribute",
        "service bureau purposes",
        "publish the Customer Data without the prior written consent",
        "remove any proprietary notices or labels",
    ):
        if marker not in restrictions:
            raise ValueError(f"Rox terms evidence is missing {marker!r}")


def verify_github_boundary() -> None:
    org_raw = json.loads(fetch(ROX_GITHUB_ORG_URL, "application/json"))
    org = {
        key: org_raw.get(key)
        for key in (
            "login",
            "name",
            "blog",
            "html_url",
            "public_repos",
            "description",
        )
    }
    if (
        canonical_json_sha256(org) != ROX_GITHUB_ORG_SHA256
        or org.get("login") != "Rox-AI"
        or org.get("name") != "Rox"
        or org.get("blog") != "rox.com"
        or org.get("public_repos") != 4
    ):
        raise ValueError("Rox official GitHub organization changed")

    repos_raw = json.loads(fetch(ROX_GITHUB_REPOS_URL, "application/json"))
    repos = sorted(
        (
            {
                "name": repo.get("name"),
                "html_url": repo.get("html_url"),
                "description": repo.get("description"),
                "license": (repo.get("license") or {}).get("spdx_id"),
                "archived": repo.get("archived"),
                "fork": repo.get("fork"),
                "default_branch": repo.get("default_branch"),
                "pushed_at": repo.get("pushed_at"),
            }
            for repo in repos_raw
        ),
        key=lambda repo: str(repo["name"]),
    )
    if canonical_json_sha256(repos) != ROX_GITHUB_REPOS_SHA256:
        raise ValueError("Rox public GitHub repository inventory changed")
    for repo in repos:
        searchable = " ".join(
            str(repo.get(field) or "")
            for field in ("name", "description", "html_url")
        ).lower()
        if "mcp" in searchable or "model context protocol" in searchable:
            raise ValueError(
                "Rox published a candidate official MCP repository; "
                "re-audit required"
            )


def inventory_hash(plugin: Path) -> str:
    entries = []
    for path in sorted(item for item in plugin.rglob("*") if item.is_file()):
        value = path.read_bytes()
        entries.append(
            f"{path.relative_to(plugin).as_posix()}\0{sha256(value)}\0{len(value)}"
        )
    return sha256("\n".join(entries).encode())


def verify_openai_snapshot(source: Path) -> None:
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if revision != EXPECTED_OPENAI_REVISION:
        raise ValueError(
            f"{source}: expected {EXPECTED_OPENAI_REVISION}, found {revision}"
        )

    plugin = source / "plugins/rox"
    actual_files = {
        path.relative_to(plugin).as_posix()
        for path in plugin.rglob("*")
        if path.is_file()
    }
    if actual_files != set(OPENAI_HASHES):
        raise ValueError("Rox Codex file inventory changed")
    for relative_path, expected_hash in OPENAI_HASHES.items():
        if sha256((plugin / relative_path).read_bytes()) != expected_hash:
            raise ValueError(f"Rox Codex evidence changed: {relative_path}")
    if inventory_hash(plugin) != OPENAI_INVENTORY_SHA256:
        raise ValueError("Rox Codex inventory hash changed")

    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    app = json.loads((plugin / ".app.json").read_text())
    interface = manifest.get("interface", {})
    if (
        manifest.get("name") != "rox"
        or manifest.get("version") != "1.0.3"
        or manifest.get("author", {}).get("name") != "Rox Data Corp"
        or interface.get("developerName") != "Rox Data Corp"
        or app.get("apps", {}).get("rox", {}).get("id")
        != "asdk_app_6a1480a4a93c8191be8b8686d450db0a"
    ):
        raise ValueError("Rox Codex identity changed")
    description = interface.get("longDescription", "")
    for marker in (
        "authenticated sales data",
        "accounts, deals, contacts, notes, emails, meetings, documents, "
        "org charts, and Slack activity",
        "discover available data functions",
        "inspect each function's schema and workflow guidance",
        "invoke read-only functions",
    ):
        if marker not in description:
            raise ValueError(f"Rox Codex capability evidence is missing {marker!r}")


def main() -> int:
    args = parse_args()
    verify_documentation_boundary()
    verify_official_product_evidence()
    verify_terms()
    verify_github_boundary()
    verify_openai_snapshot(args.openai_source.resolve())
    if Path("plugins/rox").exists() or Path("packages/rox.zip").exists():
        raise ValueError(
            "Rox must remain unpublished until the developer supplies a public "
            "portable MCP endpoint, independent authentication and onboarding, "
            "authenticated tool schemas proving the Codex capability, and "
            "sufficient adapter and artwork rights"
        )
    print("verified Rox private-MCP portability, schema, license, and artwork blockers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
