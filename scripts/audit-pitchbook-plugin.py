#!/usr/bin/env python3
"""Verify PitchBook evidence and enforce its private-client portability blocker."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path


EXPECTED_OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
MCP_URL = "https://premium.mcp.pitchbook.com/mcp"
PROTECTED_RESOURCE_URL = (
    "https://premium.mcp.pitchbook.com/"
    ".well-known/oauth-protected-resource/mcp"
)
PROTECTED_RESOURCE_SHA256 = (
    "9577526c79db48e014832b447c5f87290ce93890695f03a32410c63c5881d088"
)
AUTHORIZATION_URL = (
    "https://premium.mcp.pitchbook.com/"
    ".well-known/oauth-authorization-server"
)
AUTHORIZATION_SHA256 = (
    "93f1ae91995c7653c84cc8d2156b86b75521f429863d14bf049d2f7cb54e57f8"
)
REGISTRATION_URL = "https://premium.mcp.pitchbook.com/register"
UNAUTHORIZED_SHA256 = (
    "8599a03b4c1d788236014f851ec320b3ad4a589c59e8c1ea045dd4d052291cce"
)
REGISTRATION_REJECTION_SHA256 = (
    "e16b62c8e5621f34f7efc30c08633c3135dbcd266412162723a7ba659d2301db"
)
OPENAI_HASHES = {
    ".app.json": (
        "6c7ac857a9a23e744c2f5308299d59a119d9742400f54fb706412f8fc7397738"
    ),
    ".codex-plugin/plugin.json": (
        "8498bca6444b9a08a895a5fafbd4f750a2f4504494e45d4b39f607c33e7edd9a"
    ),
    "assets/logo.png": (
        "8c815af116f609e60541129dcb6e55470c1244251e4e55249f70460fcfbe1e63"
    ),
}
OPENAI_INVENTORY_SHA256 = (
    "342c03d3049a30e614cfc5851928921dcbe7147d482b09bdd49594f508ef948e"
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


def canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    )


def fetch_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ghast-pitchbook-audit/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def verify_oauth_metadata() -> None:
    resource = fetch_json(PROTECTED_RESOURCE_URL)
    authorization = fetch_json(AUTHORIZATION_URL)
    if canonical_sha256(resource) != PROTECTED_RESOURCE_SHA256:
        raise ValueError("PitchBook protected-resource metadata changed")
    if canonical_sha256(authorization) != AUTHORIZATION_SHA256:
        raise ValueError("PitchBook authorization metadata changed")
    if (
        resource.get("resource") != MCP_URL
        or resource.get("authorization_servers")
        != ["https://premium.mcp.pitchbook.com/"]
        or sorted(resource.get("scopes_supported", []))
        != ["claudeai", "offline_access", "openid"]
        or resource.get("bearer_methods_supported") != ["header"]
        or authorization.get("issuer")
        != "https://premium.mcp.pitchbook.com/"
        or authorization.get("registration_endpoint") != REGISTRATION_URL
        or sorted(authorization.get("grant_types_supported", []))
        != ["authorization_code", "refresh_token"]
        or authorization.get("response_types_supported") != ["code"]
        or authorization.get("code_challenge_methods_supported") != ["S256"]
        or sorted(authorization.get("token_endpoint_auth_methods_supported", []))
        != ["client_secret_basic", "client_secret_post"]
        or authorization.get("client_id_metadata_document_supported") is not True
    ):
        raise ValueError("PitchBook OAuth contract changed")


def verify_mcp_boundary() -> None:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {
                "name": "ghast-pitchbook-audit",
                "version": "1.0",
            },
        },
    }
    request = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload, separators=(",", ":")).encode(),
        method="POST",
        headers={
            "User-Agent": "ghast-pitchbook-audit/1.0",
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        },
    )
    try:
        urllib.request.urlopen(request, timeout=60)
    except urllib.error.HTTPError as error:
        body = error.read()
        challenge = error.headers.get("WWW-Authenticate", "")
        if (
            error.code != 401
            or sha256(body) != UNAUTHORIZED_SHA256
            or f'resource_metadata="{PROTECTED_RESOURCE_URL}"'
            not in challenge
            or json.loads(body).get("error") != "invalid_token"
        ):
            raise ValueError("PitchBook MCP authentication boundary changed")
    else:
        raise ValueError("PitchBook MCP unexpectedly allowed anonymous access")


def verify_registration_blocker() -> None:
    payload = {
        "client_name": "Ghast PitchBook portability audit",
        "redirect_uris": ["http://127.0.0.1:43893/callback"],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "client_secret_post",
    }
    request = urllib.request.Request(
        REGISTRATION_URL,
        data=json.dumps(payload, separators=(",", ":")).encode(),
        method="POST",
        headers={
            "User-Agent": "ghast-pitchbook-audit/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        urllib.request.urlopen(request, timeout=60)
    except urllib.error.HTTPError as error:
        body = error.read()
        if (
            error.code != 400
            or sha256(body) != REGISTRATION_REJECTION_SHA256
            or json.loads(body)
            != {
                "error": "invalid_redirect_uri",
                "error_description": (
                    "None of the provided redirect URIs are allowed by the "
                    "server's whitelist"
                ),
            }
        ):
            raise ValueError("PitchBook client-registration behavior changed")
    else:
        raise ValueError(
            "PitchBook accepted an unapproved loopback OAuth client; "
            "re-audit portability before publishing"
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

    plugin = source / "plugins/pitchbook"
    actual_files = {
        path.relative_to(plugin).as_posix()
        for path in plugin.rglob("*")
        if path.is_file()
    }
    if actual_files != set(OPENAI_HASHES):
        raise ValueError("PitchBook Codex file inventory changed")
    for relative_path, expected_hash in OPENAI_HASHES.items():
        if sha256((plugin / relative_path).read_bytes()) != expected_hash:
            raise ValueError(f"PitchBook Codex evidence changed: {relative_path}")
    if inventory_hash(plugin) != OPENAI_INVENTORY_SHA256:
        raise ValueError("PitchBook Codex inventory hash changed")

    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    app = json.loads((plugin / ".app.json").read_text())
    interface = manifest.get("interface", {})
    if (
        manifest.get("name") != "pitchbook"
        or manifest.get("version") != "1.0.3"
        or manifest.get("author", {}).get("name") != "PitchBook"
        or interface.get("developerName") != "PitchBook"
        or interface.get("defaultPrompt") != ["Use PitchBook to help with this task"]
        or app.get("apps", {}).get("pitchbook", {}).get("id")
        != "asdk_app_693850f6312c8191be5a026bf3538e80"
    ):
        raise ValueError("PitchBook Codex identity changed")
    description = re.sub(r"\s+", " ", interface.get("longDescription", "")).strip()
    for marker in (
        "companies, investors, funds, deals, limited partners, and people",
        "financing rounds",
        "ownership information",
        "fund performance",
        "LP commitments",
        "investor portfolios",
        "source metadata",
    ):
        if marker not in description:
            raise ValueError(
                f"PitchBook Codex capability evidence is missing {marker!r}"
            )


def main() -> int:
    args = parse_args()
    verify_oauth_metadata()
    verify_mcp_boundary()
    verify_registration_blocker()
    verify_openai_snapshot(args.openai_source.resolve())
    if Path("plugins/pitchbook").exists() or Path("packages/pitchbook.zip").exists():
        raise ValueError(
            "PitchBook must remain unpublished until PitchBook authorizes a "
            "portable OAuth client or public integration path and the user's "
            "license permits the intended data workflows"
        )
    print("verified PitchBook private-client and data-license blockers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
