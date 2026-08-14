#!/usr/bin/env python3
"""Verify Network Solutions evidence and enforce its portability blocker."""

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
PARTNER_FAQ_URL = (
    "https://partners.networksolutions.com/en_US/help/faq-main.html"
)
PARTNER_FAQ_NORMALIZED_SHA256 = (
    "5ca154c5e0921dae288b5520266fc03d8965d4c346e8fee9a225929b0d75d0e1"
)
PARTNER_HOW_TO_URL = (
    "https://partners.networksolutions.com/en_US/help/how-to-main.html"
)
PARTNER_HOW_TO_NORMALIZED_SHA256 = (
    "fa530fa8f51c29677b65043dc6c8b9fb4c33fe43a37887c29ab49bf257d4f3da"
)
PARTNER_AGREEMENT_URL = (
    "https://partners.networksolutions.com/en_US/partners/Agreements/"
    "Partner_Agreement.pdf"
)
PARTNER_AGREEMENT_SHA256 = (
    "b0efef9fb7ddcf530b455cfef654de322a612b8f4f41068b026bf73d131a20b8"
)
PARTNER_AGREEMENT_SIZE = 135420
NEWFOLD_TERMS_URL = "https://legal.newfold.com/TermsOfUse.pdf"
NEWFOLD_TERMS_SHA256 = (
    "ec51d68f8b084012454e8222491ca4dbc19bc1f4faf735f4025e704f4a8d2cae"
)
NEWFOLD_TERMS_SIZE = 103572
OPENAI_HASHES = {
    ".app.json": (
        "094e77c63eb5722ed2b76e725750d1b2673f43f33c3cb351e57a8362cbc888d6"
    ),
    ".codex-plugin/plugin.json": (
        "772be70fdffacb9feddb7c584dad43eaf3451979566fdbeaece3fd4d0d26c9c2"
    ),
    "assets/app-icon.png": (
        "d134b3dfb64725ffa5b59b91ff56dde03f5f7dde5967388883af8b8437d970f7"
    ),
}
OPENAI_INVENTORY_SHA256 = (
    "88321c5dc45611168f3fc90c6ffa314bf61894eaedb234ee19528984cd22aba7"
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


def fetch(url: str) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(
        url, headers={"User-Agent": "ghast-network-solutions-audit/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read(), {
            key.lower(): value for key, value in response.headers.items()
        }


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


def verify_partner_pages() -> None:
    faq_raw, _ = fetch(PARTNER_FAQ_URL)
    faq = normalize_html(faq_raw)
    if sha256(faq.encode()) != PARTNER_FAQ_NORMALIZED_SHA256:
        raise ValueError("Network Solutions Partner FAQ changed; re-audit required")
    for marker in (
        "Network Solutions® Partner Protocol",
        "based on an XML API",
        "software development kit",
        "seamlessly integrated into your existing website",
        "direct, real-time administration",
    ):
        if marker not in faq:
            raise ValueError(f"Network Solutions Partner FAQ is missing {marker!r}")

    how_to_raw, _ = fetch(PARTNER_HOW_TO_URL)
    how_to = normalize_html(how_to_raw)
    if sha256(how_to.encode()) != PARTNER_HOW_TO_NORMALIZED_SHA256:
        raise ValueError(
            "Network Solutions Partner how-to index changed; re-audit required"
        )
    for marker in (
        "How do I perform a Standard Registration?",
        "How do I register domain names in bulk?",
        "How do I look up and update a domain name?",
        "How do I delete a domain name or service?",
        "How do I contact Network Solutions Partner Support?",
    ):
        if marker not in how_to:
            raise ValueError(
                f"Network Solutions Partner how-to index is missing {marker!r}"
            )


def verify_legal_documents() -> None:
    documents = (
        (
            PARTNER_AGREEMENT_URL,
            PARTNER_AGREEMENT_SHA256,
            PARTNER_AGREEMENT_SIZE,
        ),
        (NEWFOLD_TERMS_URL, NEWFOLD_TERMS_SHA256, NEWFOLD_TERMS_SIZE),
    )
    for url, expected_hash, expected_size in documents:
        value, headers = fetch(url)
        if len(value) != expected_size or sha256(value) != expected_hash:
            raise ValueError(
                f"Official legal document changed; re-audit required: {url}"
            )
        if headers.get("content-type", "").split(";", 1)[0] != "application/pdf":
            raise ValueError(f"Expected an official PDF at {url}")


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

    plugin = source / "plugins/network-solutions"
    actual_files = {
        path.relative_to(plugin).as_posix()
        for path in plugin.rglob("*")
        if path.is_file()
    }
    if actual_files != set(OPENAI_HASHES):
        raise ValueError("Network Solutions Codex file inventory changed")
    for relative_path, expected_hash in OPENAI_HASHES.items():
        if sha256((plugin / relative_path).read_bytes()) != expected_hash:
            raise ValueError(
                f"Network Solutions Codex evidence changed: {relative_path}"
            )
    if inventory_hash(plugin) != OPENAI_INVENTORY_SHA256:
        raise ValueError("Network Solutions Codex inventory hash changed")

    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    app = json.loads((plugin / ".app.json").read_text())
    interface = manifest.get("interface", {})
    if (
        manifest.get("name") != "network-solutions"
        or manifest.get("version") != "1.0.3"
        or manifest.get("author", {}).get("name") != "Network Solutions"
        or interface.get("developerName") != "Network Solutions"
        or interface.get("defaultPrompt") != ["Searching for specific domain"]
        or app.get("apps", {}).get("network-solutions", {}).get("id")
        != "asdk_app_6944288d82108191a97261e0be991d3a"
    ):
        raise ValueError("Network Solutions Codex identity changed")
    description = interface.get("longDescription", "")
    for marker in (
        "describe their idea in plain language",
        "check domain availability across relevant extensions",
        "suggest alternatives",
        "ready to register",
    ):
        if marker not in description:
            raise ValueError(
                f"Network Solutions Codex capability evidence is missing {marker!r}"
            )


def main() -> int:
    args = parse_args()
    verify_partner_pages()
    verify_legal_documents()
    verify_openai_snapshot(args.openai_source.resolve())
    if (
        Path("plugins/network-solutions").exists()
        or Path("packages/network-solutions.zip").exists()
    ):
        raise ValueError(
            "Network Solutions must remain unpublished until the developer supplies "
            "a public or redistributable API contract, independent authentication, "
            "and written authorization for the intended adapter and artwork"
        )
    print("verified Network Solutions partner-only portability and license blockers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
