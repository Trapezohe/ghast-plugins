#!/usr/bin/env python3
"""Verify Meticulate evidence and enforce its portability blocker."""

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
HOMEPAGE_URL = "https://meticulate.ai/"
HOMEPAGE_SHA256 = (
    "eda7f54b8924e594a7f445a330bfbf8238db2e3db26c16fb5be9dd008d347844"
)
TERMS_URL = "https://meticulate.ai/terms"
TERMS_SHA256 = (
    "42e004b8a67f4b7ef55ba536f5c11728ab18a3d12b6d1d867bc87112ee39ed2c"
)
TERMS_NORMALIZED_SHA256 = (
    "15506cdecc56b56ca4c84e5361e46230a260dbf80d4ab0b48f10821de0d9094e"
)
STOREFRONT_URL = (
    "https://storefront.meticulate.ai/api/ask-agent?question=product"
)
STOREFRONT_SHA256 = (
    "1e5b54a3215692b54118d178ae83ec91a8092094ae2290a748a9df9cb56f3aff"
)
APP_JS_URL = "https://app.meticulate.ai/assets/index-DrCUAsaM.js"
APP_JS_SHA256 = (
    "b00a3ac552b795d22c1f8cda0ad8134a8f407c7381b9242ec8666661d8692e49"
)
OPENAPI_URL = "https://brain.meticulate.ai/openapi.json"
OPENAPI_SHA256 = (
    "3f1e739c5e0a82d65640379388c82277991e73563a2a86f5ec14b3a53b5787b3"
)
OPENAI_HASHES = {
    ".app.json": (
        "604ee738313c024ebcd4494881b1ed2f3516b6995650e181d352bbd650f75488"
    ),
    ".codex-plugin/plugin.json": (
        "ef2822c5bdb5b8222d6822c66cd6e5927d57e2e87cb7b14260a6bbdeac2cc1b3"
    ),
    "assets/app-icon.svg": (
        "1736c03c720ea2fbb29454109e925396793c756b83b9372926c30139a71b4b2e"
    ),
    "assets/logo.png": (
        "9172ca18507017237fda5a8cf0366c9c9ddf162bbf566cc838dbe0184538755f"
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--openai-source",
        type=Path,
        required=True,
        help="Pinned checkout of github.com/openai/plugins.",
    )
    return parser.parse_args()


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": "ghast-meticulate-audit/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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


def verify_official_web() -> None:
    homepage = fetch(HOMEPAGE_URL)
    if sha256(homepage) != HOMEPAGE_SHA256:
        raise ValueError("Meticulate homepage changed; re-audit required")
    homepage_text = homepage.decode("utf-8", "replace")
    for marker in (
        "Custom messaging for every prospect",
        "Start outbounding based on signals",
        "Screen for your ICP with custom topics",
        "Native integrations with Hubspot and Salesforce",
        "storefront.meticulate.ai/api/ask-agent",
    ):
        if marker not in homepage_text:
            raise ValueError(f"Meticulate homepage is missing {marker!r}")

    terms = fetch(TERMS_URL)
    normalized = normalize_html(terms)
    if (
        sha256(terms) != TERMS_SHA256
        or sha256(normalized.encode("utf-8")) != TERMS_NORMALIZED_SHA256
    ):
        raise ValueError("Meticulate terms changed; re-audit required")
    for marker in (
        "copy, modify, translate or create derivative works",
        "make available the Services or Documentation to any third party",
        "reverse engineer, disassemble, decompile, decode, decipher",
        "competitive or benchmarking analysis",
    ):
        if marker not in normalized:
            raise ValueError(f"Meticulate terms are missing {marker!r}")

    storefront = fetch(STOREFRONT_URL)
    if sha256(storefront) != STOREFRONT_SHA256:
        raise ValueError("Meticulate public storefront changed")
    storefront_text = storefront.decode("utf-8")
    for marker in (
        "Approved Public Knowledge",
        "discover and enrich companies and people",
        "Salesforce and HubSpot through Nango-powered sync",
        "call GET or POST /api/ask-agent",
        "route the buyer to the Meticulate team",
    ):
        if marker not in storefront_text:
            raise ValueError(f"Meticulate storefront is missing {marker!r}")


def verify_private_platform_surface() -> None:
    app_js = fetch(APP_JS_URL)
    if sha256(app_js) != APP_JS_SHA256:
        raise ValueError("Meticulate web application changed; re-audit required")
    app_text = app_js.decode("utf-8")
    for marker in (
        "https://brain.meticulate.ai",
        "/brain/v1/internal_dashboard/mcp-tool-calls",
        "/brain/v1/user_and_workspace/get_nango_connect_session_token",
        "Authorization:`Bearer ${e}`",
    ):
        if marker not in app_text:
            raise ValueError(f"Meticulate app evidence is missing {marker!r}")

    raw = fetch(OPENAPI_URL)
    if sha256(raw) != OPENAPI_SHA256:
        raise ValueError("Meticulate OpenAPI changed; re-audit required")
    spec = json.loads(raw)
    paths = spec.get("paths", {})
    if (
        spec.get("info", {}).get("title")
        != "Meticulate Web Server - OpenAPI 3.0"
        or spec.get("info", {}).get("version") != "0.0.1"
        or len(paths) != 712
        or spec.get("components", {}).get("securitySchemes")
        != {"HTTPBearer": {"type": "http", "scheme": "bearer"}}
    ):
        raise ValueError("Meticulate internal API identity changed")
    required_paths = {
        "/brain/v1/internal_dashboard/mcp-tool-calls",
        "/brain/v1/internal_dashboard/mcp-tool-calls/{tool_call_id}",
        "/brain/v1/searcher/get_company_searcher_page",
        "/brain/v1/find_similar_companies_light",
        "/brain/v1/company_searches_v2/get_search",
        "/brain/v1/company_searches_v2/find_similar_search_inputs_to_instructions",
    }
    if not required_paths.issubset(paths):
        raise ValueError("Meticulate internal capability evidence changed")
    mcp_paths = sorted(path for path in paths if "mcp" in path.lower())
    if mcp_paths != [
        "/brain/v1/internal_dashboard/mcp-tool-calls",
        "/brain/v1/internal_dashboard/mcp-tool-calls/{tool_call_id}",
    ]:
        raise ValueError("Meticulate published a changed MCP-related surface")

    for url in (
        "https://brain.meticulate.ai/mcp",
        "https://brain.meticulate.ai/.well-known/oauth-protected-resource",
    ):
        try:
            fetch(url)
        except urllib.error.HTTPError as exc:
            if exc.code != 404 or json.loads(exc.read()) != {"detail": "Not Found"}:
                raise ValueError(f"Meticulate endpoint behavior changed: {url}")
        else:
            raise ValueError(f"Meticulate unexpectedly published {url}")


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
    plugin = source / "plugins/meticulate"
    for relative_path, expected_hash in OPENAI_HASHES.items():
        if sha256((plugin / relative_path).read_bytes()) != expected_hash:
            raise ValueError(f"Meticulate Codex evidence changed: {relative_path}")
    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    app = json.loads((plugin / ".app.json").read_text())
    if (
        manifest.get("name") != "meticulate"
        or manifest.get("version") != "1.0.2"
        or manifest.get("author", {}).get("name") != "Meticulate"
        or manifest.get("interface", {}).get("developerName") != "Meticulate"
        or app.get("apps", {}).get("meticulate", {}).get("id")
        != "asdk_app_69f8fe2bcac08191b6025acec161ce1e"
    ):
        raise ValueError("Meticulate Codex identity changed")


def main() -> int:
    args = parse_args()
    verify_official_web()
    verify_private_platform_surface()
    verify_openai_snapshot(args.openai_source.resolve())
    if Path("plugins/meticulate").exists() or Path("packages/meticulate.zip").exists():
        raise ValueError(
            "Meticulate must remain unpublished until it supplies an authorized "
            "portable MCP/API contract, independent authentication, and rights"
        )
    print("verified Meticulate private-interface and license blockers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
