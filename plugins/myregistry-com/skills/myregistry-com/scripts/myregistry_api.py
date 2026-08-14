#!/usr/bin/env python3
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
