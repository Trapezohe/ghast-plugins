#!/usr/bin/env python3
"""Build the verified Ghast adapter for MyRegistry's official Registry API."""

from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


sys.dont_write_bytecode = True

PLUGIN_ID = "myregistry-com"
PLUGIN_DIR = Path("plugins")
REVIEWS_PATH = Path("third-party-plugin-reviews.json")
OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
OPENAI_HASHES = {
    ".app.json": (
        "db11946c6dbd2ed776556d26ed59cb957ddffdb05968c8c7d928a5ad53730ff6"
    ),
    ".codex-plugin/plugin.json": (
        "b750a3cdbedf0e1e03e9338fea020e0fb0a358aee1ef0c531130e6aa69f534a4"
    ),
    "assets/logo-dark.png": (
        "2e1f7ed9a19e11dedef0522aff2ac5c6580889a2883fcfc2d98d88e31df994ff"
    ),
    "assets/logo.png": (
        "13118f714489cdf8c6c54f354bc1cd6c8e92df82c2f2aa49b419252224f15613"
    ),
}
OPENAI_INVENTORY_SHA256 = (
    "8a2e60d12f51858ae1cf36bc855d51d77d2beb5aaef9fb828527bd2491f8acb0"
)
DOCUMENTS = {
    "https://developers.myregistry.com/llms.txt": (
        "4d7fc6fcb734b320b6e5dff234401d4c9e27193bf015d9ca2923d0f465b92e5c",
        (
            "https://developers.myregistry.com/reference/new-endpoint.md",
            "https://developers.myregistry.com/reference/get_new-endpoint-1.md",
            "https://developers.myregistry.com/reference/merchant-api1.md",
        ),
    ),
    "https://developers.myregistry.com/docs/getting-started.md": (
        "81d5402e985a93bae1f9caf4d33bb3094f5c2bc1b2687faeffdd254e41a7205c",
        (
            "MyRegistry.com empowers retailers",
            "Plug-N-Play Installation",
            "JavaScript SDK",
            "You retain the transaction, traffic, and customer relationship",
        ),
    ),
    "https://developers.myregistry.com/reference/new-endpoint.md": (
        "815e8bee26f4c8a4e8d25580f8ecb38363dec6a9360cf8e28da3cb89393a7f11",
        (
            "# Registry API",
            "allows your consumers to find registries",
        ),
    ),
    "https://developers.myregistry.com/reference/get_new-endpoint-1.md": (
        "0fbbe1a50b9a4381b970b0e7c73b8369174eb6836baada88f0d71970e4f54e68",
        (
            "# GetRegistries2",
            "https://api.myregistry.com/RegistryApi/1/0/json",
            '"name": "developerKey"',
            '"name": "firstName"',
            '"name": "lastName"',
            '"RegistryUrl": {',
            "Use 0 for Wedding, 1 for Baby and 2 for Gift List",
        ),
    ),
    "https://developers.myregistry.com/reference/merchant-api1.md": (
        "541f8eaf4f1841a42a6bf70125bf233ebcccf0b9c2b1e1d622984f9460f83ccd",
        (
            "allow you as a partner to integrate your backend",
            "Server-Side Access Only",
            "securely store and use your API keys and credentials",
        ),
    ),
}
TERMS_URL = "https://www.myregistry.com/Info/terms.aspx"
TERMS_NORMALIZED_SHA256 = (
    "a0a8295276ac63d87503b13be17ce42b23aae3fa5f110a1e243737e2845d1b2a"
)
PRIVACY_URL = "https://www.myregistry.com/Info/Privacy.aspx"
PRIVACY_NORMALIZED_SHA256 = (
    "140462226a15172f465172743566e2809f1630ec6db9abd0b88401891982f448"
)
REGISTRY_URL = (
    "https://api.myregistry.com/RegistryApi/1/0/json/GetRegistries2"
)
UPSTREAM_REVISION = (
    "myregistry-registry-api-0fbbe1a50b9a"
    "+docs-81d5402e985a"
    "+terms-a0a8295276ac"
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


def fetch(url: str) -> tuple[bytes, object]:
    request = urllib.request.Request(
        url, headers={"User-Agent": "ghast-myregistry-import/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read(), response.headers


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


def verify_documents() -> None:
    for url, (expected_hash, markers) in DOCUMENTS.items():
        value, _ = fetch(url)
        if sha256(value) != expected_hash:
            raise ValueError(f"MyRegistry developer document changed: {url}")
        text = value.decode("utf-8", "replace")
        for marker in markers:
            if marker not in text:
                raise ValueError(f"MyRegistry document {url} is missing {marker!r}")

    terms_raw, _ = fetch(TERMS_URL)
    terms = normalize_html(terms_raw)
    if sha256(terms.encode()) != TERMS_NORMALIZED_SHA256:
        raise ValueError("MyRegistry terms changed; re-audit required")
    for marker in (
        "Merchants’ access to and usage of the Platform is governed by the "
        "Merchant Agreement",
        "robot, spider, scraper, or other automated means",
        "without our express written permission",
        "This Terms and Conditions Statement is effective October 01, 2025",
        "Last Updated : 10/1/2025",
    ):
        if marker not in terms:
            raise ValueError(f"MyRegistry terms are missing {marker!r}")

    privacy_raw, _ = fetch(PRIVACY_URL)
    privacy = normalize_html(privacy_raw)
    if sha256(privacy.encode()) != PRIVACY_NORMALIZED_SHA256:
        raise ValueError("MyRegistry privacy statement changed; re-audit required")
    for marker in (
        "each Merchant hereby agrees to our Privacy Policy and the accompanying "
        "Merchant Agreement",
        "first name, last name, and e-mail address",
        "address will be visible to individuals who have access to your gift list",
        "This Privacy Statement is effective March 1, 2025",
    ):
        if marker not in privacy:
            raise ValueError(f"MyRegistry privacy statement is missing {marker!r}")


def verify_api_boundary() -> None:
    query = urllib.parse.urlencode(
        {"firstName": "GhastAuthProbe", "lastName": "GhastAuthProbe"}
    )
    request = urllib.request.Request(
        f"{REGISTRY_URL}?{query}",
        headers={
            "User-Agent": "ghast-myregistry-import/1.0",
            "Accept": "application/json",
        },
    )
    try:
        urllib.request.urlopen(request, timeout=60)
    except urllib.error.HTTPError as error:
        body = error.read()
        if (
            error.code != 417
            or error.headers.get_content_type() != "application/json"
            or json.loads(body) != {"ErrorMessage": "Developer Key is not valid."}
        ):
            raise ValueError("MyRegistry Registry API auth boundary changed")
    else:
        raise ValueError(
            "MyRegistry Registry API unexpectedly allowed anonymous access"
        )


def git_revision(repository: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
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


def verify_openai(source: Path) -> None:
    if git_revision(source) != OPENAI_REVISION:
        raise ValueError(f"{source}: unexpected OpenAI plugin revision")
    plugin = source / "plugins" / PLUGIN_ID
    actual_files = {
        path.relative_to(plugin).as_posix()
        for path in plugin.rglob("*")
        if path.is_file()
    }
    if actual_files != set(OPENAI_HASHES):
        raise ValueError("MyRegistry Codex file inventory changed")
    for relative, expected_hash in OPENAI_HASHES.items():
        if sha256((plugin / relative).read_bytes()) != expected_hash:
            raise ValueError(f"MyRegistry Codex evidence changed at {relative}")
    if inventory_hash(plugin) != OPENAI_INVENTORY_SHA256:
        raise ValueError("MyRegistry Codex inventory hash changed")

    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    app = json.loads((plugin / ".app.json").read_text())
    interface = manifest.get("interface", {})
    if (
        manifest.get("name") != PLUGIN_ID
        or manifest.get("version") != "1.0.3"
        or manifest.get("author", {}).get("name") != "MyRegistry.com"
        or interface.get("developerName") != "MyRegistry.com"
        or interface.get("defaultPrompt")
        != ["Find the relevant registry details in MyRegistry.com"]
        or app.get("apps", {}).get(PLUGIN_ID, {}).get("id")
        != "asdk_app_69c1b82faf2c81919e80900a7443dcfd"
    ):
        raise ValueError("MyRegistry Codex identity changed")
    for marker in (
        "Create a universal gift list",
        "weddings, baby showers, birthdays",
        "add gifts from any store",
    ):
        if marker not in interface.get("longDescription", ""):
            raise ValueError(f"MyRegistry Codex capability is missing {marker!r}")


def render_api_script() -> str:
    return r'''#!/usr/bin/env python3
"""Find public gift registries through MyRegistry's official Registry API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


REGISTRY_URL = (
    "https://api.myregistry.com/RegistryApi/1/0/json/GetRegistries2"
)
REGISTRY_TYPES = {
    "wedding": 0,
    "baby": 1,
    "gift-list": 2,
}
RESULT_FIELDS = (
    "Registrant",
    "CoRegistrant",
    "RegistryType",
    "Date",
    "RegistryUrl",
    "Location",
)


class MyRegistryError(RuntimeError):
    pass


def developer_key() -> str:
    value = os.environ.get("MYREGISTRY_DEVELOPER_KEY")
    if not value:
        raise MyRegistryError(
            "Set MYREGISTRY_DEVELOPER_KEY in the local environment"
        )
    if len(value) > 512 or any(char in value for char in "\x00\r\n"):
        raise MyRegistryError("MYREGISTRY_DEVELOPER_KEY is malformed")
    return value


def clean_text(name: str, value: str | None, *, required: bool = False):
    if value is None:
        if required:
            raise MyRegistryError(f"{name} is required")
        return None
    cleaned = value.strip()
    if required and not cleaned:
        raise MyRegistryError(f"{name} is required")
    if not cleaned:
        return None
    if len(cleaned) > 120 or any(char in cleaned for char in "\x00\r\n"):
        raise MyRegistryError(f"{name} must contain 1-120 safe characters")
    return cleaned


def registry_rows(payload: dict) -> list[dict]:
    raw = payload.get("Registries")
    if raw is None:
        return []
    if isinstance(raw, list):
        candidates = raw
    elif isinstance(raw, dict):
        if any(field in raw for field in RESULT_FIELDS):
            candidates = [raw]
        else:
            candidates = [
                item for item in raw.values() if isinstance(item, dict)
            ]
    else:
        raise MyRegistryError("MyRegistry returned an unexpected registry list")

    rows = []
    for item in candidates:
        if not isinstance(item, dict):
            continue
        rows.append({field: item.get(field) for field in RESULT_FIELDS})
    return rows


def normalize(payload: dict, *, limit: int) -> dict:
    rows = registry_rows(payload)
    total = payload.get("TotalCount")
    if not isinstance(total, int):
        total = len(rows)
    return {
        "usage_notice": (
            "Registry matches can contain names, event dates, locations, and "
            "public links. Use only for the user's stated gifting purpose; do "
            "not bulk collect, profile, contact, or scrape registry pages."
        ),
        "total_count": total,
        "returned_count": min(len(rows), limit),
        "truncated": len(rows) > limit or total > limit,
        "registries": rows[:limit],
    }


def request_json(params: dict) -> dict:
    query = urllib.parse.urlencode({**params, "developerKey": developer_key()})
    request = urllib.request.Request(
        f"{REGISTRY_URL}?{query}",
        headers={
            "User-Agent": "ghast-myregistry-adapter/1.0",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
    except urllib.error.HTTPError as error:
        body = error.read()
        detail = f"HTTP {error.code}"
        try:
            message = json.loads(body).get("ErrorMessage")
            if isinstance(message, str) and message:
                detail += f": {message}"
        except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
            pass
        raise MyRegistryError(f"MyRegistry request failed: {detail}") from error
    except urllib.error.URLError as error:
        raise MyRegistryError(
            f"MyRegistry network request failed: {error.reason}"
        ) from error
    try:
        result = json.loads(body)
    except json.JSONDecodeError as error:
        raise MyRegistryError("MyRegistry returned invalid JSON") from error
    if not isinstance(result, dict):
        raise MyRegistryError("MyRegistry returned an unexpected response")
    if result.get("ErrorMessage"):
        raise MyRegistryError(
            f"MyRegistry request failed: {result['ErrorMessage']}"
        )
    return result


def search(args):
    params = {
        "firstName": clean_text("first name", args.first_name, required=True),
        "lastName": clean_text("last name", args.last_name, required=True),
    }
    for parameter, value in (
        ("city", args.city),
        ("state", args.state),
        ("country", args.country),
    ):
        cleaned = clean_text(parameter, value)
        if cleaned is not None:
            params[parameter] = cleaned
    if args.registry_type:
        params["registryType"] = REGISTRY_TYPES[args.registry_type]
    return normalize(request_json(params), limit=args.limit)


def auth_check(_args):
    developer_key()
    return {
        "configured": True,
        "credential": "MYREGISTRY_DEVELOPER_KEY",
        "live_request_performed": False,
    }


def self_test(_args):
    sample = {
        "TotalCount": 1,
        "Registries": [
            {
                "Registrant": "Jamie Example",
                "CoRegistrant": "Taylor Example",
                "RegistryType": "Wedding",
                "Date": "10/18/2026",
                "RegistryUrl": "https://www.myregistry.com/example",
                "Location": "Example City, NY",
                "Ignored": "not returned",
            }
        ],
    }
    result = normalize(sample, limit=10)
    if (
        result["total_count"] != 1
        or result["returned_count"] != 1
        or result["truncated"]
        or set(result["registries"][0]) != set(RESULT_FIELDS)
        or "Ignored" in result["registries"][0]
    ):
        raise MyRegistryError("adapter self-test failed")
    return {"self_test": "passed"}


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    auth = subparsers.add_parser(
        "auth-check", help="Check local credential configuration without a request"
    )
    auth.set_defaults(handler=auth_check)

    find = subparsers.add_parser(
        "search", help="Find public registries by registrant name"
    )
    find.add_argument("--first-name", required=True)
    find.add_argument("--last-name", required=True)
    find.add_argument("--city")
    find.add_argument("--state")
    find.add_argument("--country")
    find.add_argument("--registry-type", choices=sorted(REGISTRY_TYPES))
    find.add_argument("--limit", type=int, choices=range(1, 101), default=25)
    find.set_defaults(handler=search)

    test = subparsers.add_parser("self-test")
    test.set_defaults(handler=self_test)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = args.handler(args)
    except MyRegistryError as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def render_skill() -> str:
    return """---
name: myregistry-com
description: >-
  Find public wedding, baby, and gift-list registries through MyRegistry.com's
  official partner Registry API.
---

# MyRegistry.com

Use the bundled `scripts/myregistry_api.py` read-only adapter over
MyRegistry.com's official `GetRegistries2` Registry API. This is a Ghast
adapter to the official service, not MyRegistry-authored source or an MCP
server.

## Access

- The API is for authorized MyRegistry retail partners and requires a
  MyRegistry-issued `developerKey`. A normal consumer registry account does
  not necessarily include API access.
- Store the key as `MYREGISTRY_DEVELOPER_KEY` in the Ghast host environment.
  Never request it in chat, put it in a command argument, print it, log it,
  save it in a project file, or commit it.
- The official API requires the key in the HTTPS query string. Use only the
  fixed endpoint in the adapter and avoid proxy, shell, or debug logging that
  records full request URLs.

Resolve this skill's directory as `SKILL_DIR`, then:

```bash
MYREGISTRY_API="$SKILL_DIR/scripts/myregistry_api.py"
python3 "$MYREGISTRY_API" auth-check
```

`auth-check` checks local configuration only. It does not send a registry
query or expose the key.

## Find a registry

The official API requires both first and last name:

```bash
python3 "$MYREGISTRY_API" search \\
  --first-name Jamie \\
  --last-name Example \\
  --state NY \\
  --registry-type wedding
```

Optional filters are `--city`, `--state`, `--country`, and
`--registry-type wedding|baby|gift-list`. Use every known filter before
searching. For a common name or a potentially broad match, show the exact
search scope and obtain explicit user confirmation before the request.

The result contains only the official lookup fields: registrant,
co-registrant, registry type, event date, location, and public registry URL.
The local `--limit` defaults to 25 and only limits returned output; the
official endpoint does not document server-side pagination.

## Privacy and safety

- Registry results can reveal names, relationships, event types, event dates,
  and approximate locations. Retrieve only the minimum needed for the user's
  stated gifting purpose.
- Do not bulk enumerate names, build datasets, infer pregnancy, marital
  status, religion, sexuality, finances, home address, or other sensitive
  attributes, or use registry data for advertising, outreach, surveillance,
  eligibility, employment, housing, credit, insurance, or law enforcement.
- Do not disclose a match to a new recipient without authorization. When
  multiple people match, present minimal disambiguating fields and ask the
  user to choose rather than guessing.
- A returned result does not prove identity, relationship, event status, or
  current accuracy. Preserve the returned date and location exactly and state
  uncertainty.
- Do not scrape or automatically open returned registry pages. MyRegistry's
  public-site terms prohibit automated access without express permission.
  Use only the partner API covered by the user's developer key and Merchant
  Agreement.
- Password-protected registries, gift contents, purchase state, shipping
  addresses, member accounts, and registry mutations are outside this
  plugin's capability. Never try to bypass those boundaries.
- Do not automatically retry `401`, `403`, `417`, `429`, timeout, or ambiguous
  responses. Report the error without exposing the request URL or key.
"""


def render_readme(adapter_hash: str) -> str:
    return f"""# myregistry-com

Find public wedding, baby, and general gift-list registries through
MyRegistry.com's official Registry API.

## Official interface

MyRegistry's public developer documentation publishes `GetRegistries2` at
`https://api.myregistry.com/RegistryApi/1/0/json/GetRegistries2`. The endpoint
requires first and last name, accepts optional city, state, country, and
registry-type filters, and returns registrant, co-registrant, type, event
date, location, and registry URL. Authentication uses a partner
`developerKey`.

The developer index, integration guide, Registry API overview,
`GetRegistries2` OpenAPI page, and Merchant API server-side guidance are
pinned by `scripts/import-myregistry-plugin.py`. On August 14, 2026, an
anonymous request returned HTTP 417 with `Developer Key is not valid.`,
confirming the independent official API boundary without using the Codex
private app connector.

## Capability comparison

- Codex: find relevant MyRegistry.com registry details through private app ID
  `asdk_app_69c1b82faf2c81919e80900a7443dcfd`.
- Ghast: search the official public partner API by exact first and last name,
  narrow by city, state, country, or wedding/baby/gift-list type, and return
  the documented registry identity, date, location, and URL fields.
- Ghast intentionally excludes account access, gift-item retrieval, purchase
  marking, shipping addresses, registry creation, and any web scraping.

## Authentication and licensing

Set `MYREGISTRY_DEVELOPER_KEY` in the local host environment. API access,
Merchant Agreement acceptance, partner eligibility, data permissions,
service limits, and key issuance remain controlled by MyRegistry.com. An
ordinary consumer account may not include developer access.

The bundled standard-library adapter has SHA-256 `{adapter_hash}`. The MIT
license covers only the Ghast-authored adapter, workflow, metadata,
documentation, and generic gift-search icon. It does not license or
redistribute MyRegistry's service, private connector, API key, customer data,
developer documentation, web content, logos, or trademarks.
"""


def render_license() -> str:
    return """MIT License

Copyright (c) 2026 Ghast contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def render_icon() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="10" fill="#176B5B"/>
  <path d="M12 24h33v28H12zM9 18h39v8H9zM29 18v34"
        fill="none" stroke="#fff" stroke-width="4"
        stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M29 18c-8 0-11-3-11-7 0-3 2-5 5-5 5 0 6 6 6 12zm0 0c8 0 11-3 11-7
           0-3-2-5-5-5-5 0-6 6-6 12z"
        fill="none" stroke="#F6C453" stroke-width="4"
        stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="47" cy="44" r="8" fill="#fff" stroke="#19433B" stroke-width="3"/>
  <path d="m53 50 6 6" fill="none" stroke="#19433B" stroke-width="4"
        stroke-linecap="round"/>
</svg>
"""


def review(adapter_hash: str) -> dict:
    return {
        "verificationStatus": "official-source-verified",
        "officialDeveloper": "MyRegistry.com / MyRegistry LLC",
        "officialRepository": None,
        "officialRevision": UPSTREAM_REVISION,
        "license": "MIT",
        "licenseEvidence": [
            "plugins/myregistry-com/LICENSE licenses only the independently "
            "authored Ghast adapter, workflow, metadata, documentation, and "
            "generic gift-search icon.",
            "No MyRegistry source code, private Codex connector, developer "
            "credential, customer or registry data, API response, developer "
            "documentation, web content, logo, or trademark is redistributed.",
            "MyRegistry API access remains governed by the key holder's "
            "Merchant Agreement and service terms. The plugin cannot grant "
            "API permission or sublicense the hosted service.",
        ],
        "officialityEvidence": [
            "MyRegistry's official developer site publishes a Registry API "
            "specifically for integrations that let consumers find registries.",
            "The official GetRegistries2 OpenAPI page publishes the fixed "
            "api.myregistry.com endpoint, developerKey query authentication, "
            "required firstName and lastName, optional city, state, country, "
            "and registryType filters, and the returned registry identity, "
            "event date, location, and URL fields.",
            "The official developer index, getting-started guide, Registry API "
            "overview, GetRegistries2 definition, and server-side partner "
            "guidance have raw SHA-256 values "
            "4d7fc6fcb734b320b6e5dff234401d4c9e27193bf015d9ca2923d0f465b92e5c, "
            "81d5402e985a93bae1f9caf4d33bb3094f5c2bc1b2687faeffdd254e41a7205c, "
            "815e8bee26f4c8a4e8d25580f8ecb38363dec6a9360cf8e28da3cb89393a7f11, "
            "0fbbe1a50b9a4381b970b0e7c73b8369174eb6836baada88f0d71970e4f54e68, "
            "and 541f8eaf4f1841a42a6bf70125bf233ebcccf0b9c2b1e1d622984f9460f83ccd.",
            "On August 14, 2026, an unauthenticated GetRegistries2 request "
            "returned HTTP 417 and the exact JSON error Developer Key is not "
            "valid, confirming a live independent official API boundary.",
            "OpenAI's pinned snapshot identifies MyRegistry.com as developer, "
            "maps private app ID asdk_app_69c1b82faf2c81919e80900a7443dcfd, "
            "and asks to find relevant registry details. Its complete file "
            "inventory SHA-256 is "
            "8a2e60d12f51858ae1cf36bc855d51d77d2beb5aaef9fb828527bd2491f8acb0.",
        ],
        "codexCapabilities": [
            "Find relevant registry details in MyRegistry.com through a private "
            "app connector",
            "Support universal wedding, baby, birthday, and celebration gift "
            "registry discovery",
        ],
        "ghastCapabilities": [
            "Call MyRegistry.com's official GetRegistries2 API with a "
            "partner-issued developerKey from the local environment",
            "Find public registries by required first and last name and narrow "
            "by city, state, country, or wedding, baby, or gift-list type",
            "Return only the documented registrant, co-registrant, registry "
            "type, event date, location, and public registry URL fields",
            "Apply local result limits, structured errors, secret protection, "
            "privacy guidance, and a strict no-scraping boundary",
        ],
        "capabilityRelationship": "equivalent-official-read-only-api-transport",
        "limitations": [
            "MyRegistry does not publish the hosted API implementation, an "
            "official MCP server, a reusable client repository, or a public "
            "open-source license for its service. Ghast supplies only a thin "
            "independently authored client.",
            "A MyRegistry partner relationship, developerKey, Merchant "
            "Agreement, permitted business purpose, account eligibility, "
            "service availability, and limits remain user-managed. An ordinary "
            "consumer registry account may not provide API access.",
            "Authenticated search was not exercised because no MyRegistry "
            "partner key was supplied. The adapter passed deterministic "
            "normalization tests, missing-secret tests, and the live invalid-key "
            "boundary probe.",
            "The official endpoint does not document server-side pagination. "
            "The adapter's limit bounds displayed results but may not reduce the "
            "number returned by the service.",
            "Registry lookup results can expose names, relationships, event "
            "types, dates, locations, and public links. They must not be bulk "
            "collected, profiled, used for outreach or high-impact decisions, "
            "or disclosed beyond the authorized gifting purpose.",
            "The adapter does not open or scrape registry pages because "
            "MyRegistry's public terms prohibit automated access without "
            "express permission. Password-protected data is never bypassed.",
            "Gift items, purchase state, shipping addresses, user accounts, "
            "registry creation, mutation, checkout, and Merchant API write "
            "operations are intentionally excluded.",
            "The API requires developerKey in the HTTPS query string. Users "
            "must prevent proxy, debug, shell, and request logging from "
            "recording full URLs.",
            "A generic gift-search icon is used because MyRegistry's logos and "
            "OpenAI marketplace artwork are not redistributed.",
        ],
        "verification": [
            "python3 scripts/import-myregistry-plugin.py --openai-source "
            "../openai-plugins",
            "Verify all five official developer-document hashes and their "
            "Registry API, OpenAPI, developerKey, partner, and server-side "
            "integration markers",
            "Verify normalized MyRegistry terms and privacy hashes, Merchant "
            "Agreement boundary, automated-access restriction, effective "
            "dates, and registry personal-data statements",
            "Probe GetRegistries2 without a key and require HTTP 417 plus the "
            "exact invalid developer key JSON error",
            "Verify OpenAI snapshot 11c74d6ba24d3a6d48f54a194cd00ef3beea18f9, "
            "all four file hashes, complete inventory hash, developer identity, "
            "private app ID, default prompt, and universal-registry description",
            f"Verify generated adapter SHA-256 {adapter_hash}, run its self-test, "
            "and confirm missing or fake credentials are not printed",
            "python3 scripts/build-ghast-catalog.py",
            "python3 scripts/audit-third-party-plugins.py --source "
            "../openai-plugins",
            "python3 scripts/validate-ghast-repository.py",
            "unzip -tqq packages/myregistry-com.zip",
        ],
    }


def load_adapter(script_path: Path):
    spec = importlib.util.spec_from_file_location("myregistry_adapter", script_path)
    if spec is None or spec.loader is None:
        raise ValueError("Could not load generated MyRegistry adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_adapter(script_path: Path) -> None:
    result = subprocess.run(
        ["python3", str(script_path), "self-test"],
        check=True,
        capture_output=True,
        text=True,
    )
    if json.loads(result.stdout) != {"self_test": "passed"}:
        raise ValueError("Generated MyRegistry adapter self-test failed")

    env = os.environ.copy()
    env.pop("MYREGISTRY_DEVELOPER_KEY", None)
    missing = subprocess.run(
        ["python3", str(script_path), "auth-check"],
        capture_output=True,
        text=True,
        env=env,
    )
    if (
        missing.returncode != 2
        or "MYREGISTRY_DEVELOPER_KEY" not in missing.stderr
    ):
        raise ValueError("Generated MyRegistry adapter missing-secret test failed")

    fake_key = "ghast-test-key-that-must-not-be-printed"
    env["MYREGISTRY_DEVELOPER_KEY"] = fake_key
    configured = subprocess.run(
        ["python3", str(script_path), "auth-check"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    if (
        json.loads(configured.stdout).get("configured") is not True
        or fake_key in configured.stdout
        or fake_key in configured.stderr
    ):
        raise ValueError("Generated MyRegistry adapter exposed a credential")

    module = load_adapter(script_path)
    sample = module.normalize(
        {
            "TotalCount": 2,
            "Registries": {
                "one": {
                    "Registrant": "A",
                    "RegistryType": "Gift List",
                    "RegistryUrl": "https://www.myregistry.com/a",
                },
                "two": {
                    "Registrant": "B",
                    "RegistryType": "Baby",
                    "RegistryUrl": "https://www.myregistry.com/b",
                },
            },
        },
        limit=1,
    )
    if (
        sample["total_count"] != 2
        or sample["returned_count"] != 1
        or sample["truncated"] is not True
    ):
        raise ValueError("Generated MyRegistry adapter normalization failed")


def write_plugin() -> str:
    api_source = render_api_script()
    api_hash = sha256(api_source.encode())
    with tempfile.TemporaryDirectory(prefix=".myregistry-", dir=PLUGIN_DIR) as temp:
        staging = Path(temp)
        (staging / ".ghast-plugin").mkdir()
        (staging / "assets").mkdir()
        skill_dir = staging / "skills" / PLUGIN_ID
        (skill_dir / "scripts").mkdir(parents=True)
        manifest = {
            "name": PLUGIN_ID,
            "version": "1.0.3-ghast.1",
            "description": (
                "Find public wedding, baby, and gift-list registries through "
                "MyRegistry.com's official Registry API."
            ),
            "category": "productivity",
            "author": {
                "name": "MyRegistry.com / MyRegistry LLC",
                "url": "https://www.myregistry.com/",
            },
            "homepage": "https://developers.myregistry.com/reference/new-endpoint",
            "upstreamRevision": UPSTREAM_REVISION,
            "license": "MIT",
            "portStatus": "full",
            "icon": "./assets/icon.svg",
            "skills": "./skills/",
        }
        (staging / ".ghast-plugin/plugin.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        )
        (staging / "LICENSE").write_text(render_license())
        (staging / "README.md").write_text(render_readme(api_hash))
        (staging / "assets/icon.svg").write_text(render_icon())
        (skill_dir / "SKILL.md").write_text(render_skill())
        script_path = skill_dir / "scripts" / "myregistry_api.py"
        script_path.write_text(api_source)
        script_path.chmod(0o755)
        test_adapter(script_path)

        target = PLUGIN_DIR / PLUGIN_ID
        if target.exists():
            shutil.rmtree(target)
        staging.rename(target)
    return api_hash


def update_review(adapter_hash: str) -> None:
    data = json.loads(REVIEWS_PATH.read_text())
    data.setdefault("plugins", {})[PLUGIN_ID] = review(adapter_hash)
    REVIEWS_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    )


def main() -> int:
    args = parse_args()
    verify_documents()
    verify_api_boundary()
    verify_openai(args.openai_source.resolve())
    adapter_hash = write_plugin()
    update_review(adapter_hash)
    print(
        "imported verified MyRegistry Registry API adapter "
        f"(adapter SHA-256 {adapter_hash})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
