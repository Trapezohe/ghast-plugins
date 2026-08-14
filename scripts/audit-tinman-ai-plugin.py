#!/usr/bin/env python3
"""Verify Better Tinman evidence and enforce its private-platform blocker."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path


EXPECTED_OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
TINMAN_URL = "https://better.com/b/tinman"
TINMAN_APP_CORE_SHA256 = (
    "f849dcb291b1ad64737169eada6b587b75496908484c6df2ff222444b67374e8"
)
CHATGPT_RELEASE_URL = (
    "https://investors.better.com/news/news-details/2026/"
    "Better-Announces-First-Conversational-Credit-Decision-Engine-in-"
    "ChatGPT-with-OpenAI/default.aspx"
)
CHATGPT_RELEASE_CORE_SHA256 = (
    "9b2aceeb4cc27f6f3e4409f5ff279a9ffa591d94ae8b491f13d1384b19974cbe"
)
PARTNER_RELEASE_URL = (
    "https://investors.better.com/news/news-details/2025/"
    "Finance-of-America-Partners-with-Better-com-to-Leverage-Tinman-AI-"
    "Platform--Expanding-Home-Equity-Product-Suite-for-Homeowners-Over-"
    "55/default.aspx"
)
PARTNER_RELEASE_CORE_SHA256 = (
    "737549e9d48fe1bc7c6adaece94f6c687a6874a764922c3404bd94636a1eeb19"
)
TERMS_URL = "https://better.com/about-us/terms-of-use"
TERMS_CORE_SHA256 = (
    "7ec6dfdb49287dd04b0716e4f3065dba3405410cfe09095e8a1e9b7b427b8a4b"
)
AUTHORIZATION_METADATA_URL = (
    "https://better.com/.well-known/oauth-authorization-server"
)
AUTHORIZATION_METADATA_SHA256 = (
    "52bfe15d9f9010147fcfab38a3ba6034ec885a5aeb5a40fea46dd67d20d2d69f"
)
PROTECTED_RESOURCE_URL = "https://better.com/.well-known/oauth-protected-resource"
CONVENTIONAL_MCP_URL = "https://better.com/mcp"
OPENAI_HASHES = {
    ".app.json": (
        "9625b354cbc9dfef1931b873259aaa1870e3f1b614b20e15545ac54de1793841"
    ),
    ".codex-plugin/plugin.json": (
        "4f943695d3d006e6012e6628720d9d36f753beaf05aff6ae1484b2aa8264cf1c"
    ),
    "assets/logo.png": (
        "9597f638129859ec2f1d09f819c2c3c07e886410606cced3b31c3d9db4cffdd4"
    ),
}
OPENAI_INVENTORY_SHA256 = (
    "8aea24a74e771e39566f674df742d6987f66583c475e84d37ca7c86b85376152"
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
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    )


def fetch(url: str, accept: str = "text/html") -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/140.0.0.0 Safari/537.36"
            ),
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
        raise ValueError(f"Better evidence is missing {start_marker!r}")
    end = value.find(end_marker, start + len(start_marker))
    if end < 0:
        raise ValueError(f"Better evidence is missing {end_marker!r}")
    return value[start:end].strip()


def verify_public_tinman_page() -> None:
    text = normalize_html(fetch(TINMAN_URL))
    core = section(
        text,
        "Tinman AI Credit Decision Engine App Available in ChatGPT",
        "Better Better is a family",
    )
    if sha256(core.encode()) != TINMAN_APP_CORE_SHA256:
        raise ValueError("Better Tinman public test page changed")
    for marker in (
        "first conversational credit decision engine",
        "mortgages and home equity loans",
        "available to banks, fintechs, and loan officer teams",
        "Sign up to test Tinman AI in ChatGPT",
        "Company",
        "Annual Mortgage Originations",
    ):
        if marker not in core:
            raise ValueError(f"Better Tinman page is missing {marker!r}")


def verify_chatgpt_release() -> None:
    text = normalize_html(fetch(CHATGPT_RELEASE_URL))
    core = section(
        text,
        (
            "Better Announces First Conversational Credit Decision Engine in "
            "ChatGPT with OpenAI March 5, 2026"
        ),
        "About Better Home & Finance Holding Company",
    )
    if sha256(core.encode()) != CHATGPT_RELEASE_CORE_SHA256:
        raise ValueError("Better Tinman ChatGPT release changed")
    for marker in (
        "custom Model Context Protocol (MCP) connector",
        "built by Better’s engineering and AI teams in collaboration with OpenAI",
        "ChatGPT Enterprise account",
        "connect their guidelines, pricing, and CRM",
        "real-time snapshot across every loan file",
        "read docs, apply guidelines",
        "over 45 different institutional buyers",
        "fully underwrite a mortgage loan",
    ):
        if marker not in core:
            raise ValueError(f"Better Tinman ChatGPT release is missing {marker!r}")


def verify_partner_release() -> None:
    text = normalize_html(fetch(PARTNER_RELEASE_URL))
    core = section(
        text,
        (
            "Finance of America Partners with Better.com to Leverage Tinman® "
            "AI Platform — Expanding Home Equity Product Suite for Homeowners "
            "Over 55 October 14, 2025"
        ),
        "For more information, follow",
    )
    if sha256(core.encode()) != PARTNER_RELEASE_CORE_SHA256:
        raise ValueError("Better Tinman partner release changed")
    for marker in (
        "proprietary Tinman® AI Platform",
        "Through this partnership",
        "plug-and-play technology",
        "originate HELOCs and HELOANs",
        "private labeled experience",
        "underwriting and closing tasks 24/7",
        "modular, API-accessible solution",
        "available to lenders and brokers across the nation",
    ):
        if marker not in core:
            raise ValueError(f"Better Tinman partner release is missing {marker!r}")


def verify_terms() -> None:
    text = normalize_html(fetch(TERMS_URL))
    core = section(text, "Terms of Use Please Read", "Accessing the Website")
    if sha256(core.encode()) != TERMS_CORE_SHA256:
        raise ValueError("Better website terms changed")
    for marker in (
        "Your eligibility for particular products and services",
        "cannot warrant the accuracy, completeness, or timeliness",
        "is copyrighted and protected",
        "Any commercial use of this website or its content is prohibited",
        "only for your personal use",
    ):
        if marker not in core:
            raise ValueError(f"Better website terms are missing {marker!r}")


def verify_public_auth_boundary() -> None:
    metadata = json.loads(fetch(AUTHORIZATION_METADATA_URL, "application/json"))
    if canonical_json_sha256(metadata) != AUTHORIZATION_METADATA_SHA256:
        raise ValueError("Better public authorization metadata changed")
    if (
        metadata.get("issuer")
        != "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_ZQ2HayNPw"
        or metadata.get("authorization_endpoint")
        != "https://prod.bettermg.com/api/idp/sso"
        or metadata.get("token_endpoint")
        != "https://prod.bettermg.com/api/idp/token"
        or sorted(metadata.get("scopes_supported", []))
        != ["email", "openid", "phone", "profile"]
        or "resource" in metadata
        or "mcp" in json.dumps(metadata).lower()
    ):
        raise ValueError("Better generic identity metadata contract changed")

    for url in (PROTECTED_RESOURCE_URL, CONVENTIONAL_MCP_URL):
        try:
            urllib.request.urlopen(
                urllib.request.Request(
                    url,
                    headers={"User-Agent": "ghast-tinman-audit/1.0"},
                ),
                timeout=60,
            )
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise ValueError(f"Unexpected public Better response at {url}")
        else:
            raise ValueError(
                f"Better published a candidate portable MCP surface at {url}; "
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

    plugin = source / "plugins/tinman-ai"
    actual_files = {
        path.relative_to(plugin).as_posix()
        for path in plugin.rglob("*")
        if path.is_file()
    }
    if actual_files != set(OPENAI_HASHES):
        raise ValueError("Tinman AI Codex file inventory changed")
    for relative_path, expected_hash in OPENAI_HASHES.items():
        if sha256((plugin / relative_path).read_bytes()) != expected_hash:
            raise ValueError(f"Tinman AI Codex evidence changed: {relative_path}")
    if inventory_hash(plugin) != OPENAI_INVENTORY_SHA256:
        raise ValueError("Tinman AI Codex inventory hash changed")

    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    app = json.loads((plugin / ".app.json").read_text())
    interface = manifest.get("interface", {})
    if (
        manifest.get("name") != "tinman-ai"
        or manifest.get("version") != "1.0.3"
        or manifest.get("author", {}).get("name") != "Better"
        or interface.get("developerName") != "Better"
        or interface.get("defaultPrompt")
        != ["I have borrower at 52% DTI who wants HELOC w/ $450/month"]
        or app.get("apps", {}).get("tinman-ai", {}).get("id")
        != "asdk_app_695d4fa044b48191ac7a81f333111b29"
    ):
        raise ValueError("Tinman AI Codex identity changed")
    description = re.sub(r"\s+", " ", interface.get("longDescription", "")).strip()
    for marker in (
        "loan officers and underwriters",
        "trusted credit decision data and underwriting logic",
        "eligibility, DTI restructuring, and income calculations",
        "broad set of lenders and investors",
        "which investors a loan qualifies for and why",
        "real-time, compliant decisions",
    ):
        if marker not in description:
            raise ValueError(
                f"Tinman AI Codex capability evidence is missing {marker!r}"
            )


def main() -> int:
    args = parse_args()
    verify_public_tinman_page()
    verify_chatgpt_release()
    verify_partner_release()
    verify_terms()
    verify_public_auth_boundary()
    verify_openai_snapshot(args.openai_source.resolve())
    if Path("plugins/tinman-ai").exists() or Path("packages/tinman-ai.zip").exists():
        raise ValueError(
            "Tinman AI must remain unpublished until Better supplies a supported "
            "portable MCP or API contract, independent client authorization and "
            "institutional onboarding, stable schemas, and sufficient adapter "
            "and artwork rights"
        )
    print("verified Better Tinman private-MCP and partner-API portability blockers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
