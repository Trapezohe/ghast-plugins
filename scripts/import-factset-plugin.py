#!/usr/bin/env python3
"""Build the verified Ghast FactSet plugin from official FactSet services and SDK."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


sys.dont_write_bytecode = True

PLUGIN_ID = "factset"
PLUGIN_DIR = Path("plugins")
REVIEWS_PATH = Path("third-party-plugin-reviews.json")

OFFICIAL_REPOSITORY = "https://github.com/factset/enterprise-sdk"
OFFICIAL_REVISION = "36c67dfb8ff2b9893d0f8822ecb5d62abd30dc3f"
OFFICIAL_TREE = "970e0ff5a53917234d0581783c04ac2fb8f18d60"
UPSTREAM_REVISION = (
    "mcp-248bd4b02bb4"
    "+sdk-36c67dfb8ff2"
    "+oauth-446c80d9c183"
    "+auth-b8e63e5e699e"
)
SOURCE_HASHES = {
    "LICENSE": "58d1e17ffe5109a7ae296caafcadfdbe6a7d176f0bc4ab01e12a689b0499d8bd",
    "README.md": "02440c8e78df7bc74cc5b3fe0d67d052cbb98607821d7a8486f4d276bc570900",
    "specs/InvestmentResearch.v1.yaml": (
        "1830c8c758109e55372452eefd6c8e142079e8c1d6be7eebaaacae1022a7b870"
    ),
    "specs/SecurityExplanation.v1.json": (
        "281dff322a66ba5b262df6f966474af1d1503d206ba8b207b457917480fb24fd"
    ),
}

MCP_URL = "https://mcp.factset.com/content/v1"
MCP_PRODUCT_URL = (
    "https://developer.factset.com/api/v2/content/page/mcp/"
    "factset-ai-ready-data-mcp"
)
MCP_PRODUCT_SHA256 = (
    "248bd4b02bb48df52db939ff4e0d8200bb62f0ca6ee654bc74d02d4ddf88967c"
)
MCP_TOOL_NAMES_SHA256 = (
    "e11b82c355b2f2a94f0cd88c1397792c65d4dbfd6f2582661232cd64bc1cf6a6"
)
MCP_TOOL_NAMES = [
    "FactSet_Fundamentals",
    "FactSet_DebtCapitalStructure",
    "FactSet_EstimatesConsensus",
    "FactSet_GlobalPrices",
    "FactSet_Ownership",
    "FactSet_MergersAcquisitions",
    "FactSet_People",
    "FactSet_CalendarEvents",
    "FactSet_EntityReference",
    "FactSet_FundsETF",
    "FactSet_FundsScreener",
    "FactSet_CompanyScreener",
    "FactSet_UnstructuredContent",
    "FactSet_Metrics",
    "FactSet_PrivateEquityVC",
    "FactSet_PrivateCompany",
    "FactSet_GeoRev",
    "FactSet_SupplyChain",
    "FactSet_RBICS",
    "FactSet_TermsConditions",
]

RESOURCE_URL = (
    "https://mcp.factset.com/.well-known/oauth-protected-resource/content/v1"
)
RESOURCE_SHA256 = (
    "446c80d9c18385005dc67d81fbcee89d248d4b117eddaab38dd3a69e2f1425c0"
)
OIDC_URL = "https://auth.factset.com/.well-known/openid-configuration"
OIDC_SHA256 = (
    "b8e63e5e699e31197a954e529437ffff13a2fa45b344939f71a27477bc66410b"
)

RESEARCH_BASE = "https://api.factset.com/content/investment-research/v1"
EXPLANATION_BASE = (
    "https://api.factset.com/analytics/security-explanation/v1"
)

OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
OPENAI_HASHES = {
    ".codex-plugin/plugin.json": (
        "87982e3634eecea9041b862451dec5cc4b64325722943c711f7cbb2c600fcd17"
    ),
    ".app.json": (
        "d4373baca75cdc8445ad6e9d09165fae9ea61d86dc1a5a4aa6ced0faf185be19"
    ),
    "assets/logo.png": (
        "9473b27b9cb6906a23ebe0fea83bd198b012965c00fa9a25bcf575d54a57ca2f"
    ),
    "assets/app-icon.svg": (
        "ec341e0e2a3d3dfe48f59ecbf279a7cd925b9bc6e2bdad7830cce50eb3c5e477"
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        required=True,
        help="Pinned checkout of factset/enterprise-sdk.",
    )
    parser.add_argument(
        "--openai-source",
        type=Path,
        required=True,
        help="Pinned checkout of github.com/openai/plugins.",
    )
    return parser.parse_args()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: object) -> str:
    return sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    )


def git_value(source: Path, expression: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", expression],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def fetch(
    url: str,
    *,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[bytes, object]:
    request = urllib.request.Request(
        url,
        data=data,
        method="POST" if data is not None else "GET",
        headers={
            "User-Agent": "ghast-factset-import/1.0",
            **(headers or {}),
        },
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read(), response.headers


def fetch_json(url: str) -> dict:
    body, _ = fetch(url)
    return json.loads(body)


def verify_source(source: Path) -> None:
    if git_value(source, "HEAD") != OFFICIAL_REVISION:
        raise ValueError("FactSet Enterprise SDK revision changed")
    if git_value(source, "HEAD^{tree}") != OFFICIAL_TREE:
        raise ValueError("FactSet Enterprise SDK tree changed")
    if subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout:
        raise ValueError("FactSet Enterprise SDK checkout is dirty")

    for relative, expected in SOURCE_HASHES.items():
        if sha256((source / relative).read_bytes()) != expected:
            raise ValueError(f"FactSet Enterprise SDK changed at {relative}")

    license_text = (source / "LICENSE").read_text()
    if (
        "Apache License" not in license_text
        or "Version 2.0, January 2004" not in license_text
    ):
        raise ValueError("FactSet Apache-2.0 license evidence changed")

    investment = (
        source / "specs/InvestmentResearch.v1.yaml"
    ).read_text()
    for marker in (
        "title: 'Investment Research API'",
        "version: '1.0.0'",
        "https://api.factset.com/content/investment-research/v1",
        "FactSet collects research reports and models from brokers",
        "FactSet Research Connect",
        "operationId: 'getInvestmentResearchData'",
        "operationId: 'getCount'",
        "operationId: 'getResearchContributor'",
        "operationId: 'getResearchAnalyst'",
        "headline:",
        "storyDateTime:",
        "contributorName:",
        "analystName:",
        "ratingActions:",
        "targetActions:",
        "weightingActions:",
    ):
        if marker not in investment:
            raise ValueError(
                f"FactSet Investment Research spec is missing {marker!r}"
            )

    explanation = json.loads(
        (source / "specs/SecurityExplanation.v1.json").read_text()
    )
    info = explanation.get("info", {})
    schemas = explanation.get("components", {}).get("schemas", {})
    request = schemas.get("SecurityExplanationRequestParameters", {})
    broker = schemas.get("BrokerResearchSummary", {})
    if (
        info.get("title") != "Security Explanation API"
        or info.get("version") != "1.6.0"
        or explanation.get("servers")
        != [{"url": EXPLANATION_BASE}]
        or request.get("required") != ["id", "startDate", "endDate"]
        or broker.get("properties", {})
        .get("style", {})
        .get("enum")
        != ["none", "summary", "footnote"]
        or set(explanation.get("paths", {}))
        != {
            "/explanation",
            "/explanation/{id}/status",
            "/explanation/{id}/result",
        }
    ):
        raise ValueError("FactSet Security Explanation schema changed")


def verify_openai_source(source: Path) -> None:
    if git_value(source, "HEAD") != OPENAI_REVISION:
        raise ValueError("OpenAI plugin source revision changed")
    plugin = source / "plugins/factset"
    for relative, expected in OPENAI_HASHES.items():
        if sha256((plugin / relative).read_bytes()) != expected:
            raise ValueError(f"FactSet Codex evidence changed at {relative}")

    manifest = json.loads(
        (plugin / ".codex-plugin/plugin.json").read_text()
    )
    app = json.loads((plugin / ".app.json").read_text())
    prompts = manifest.get("interface", {}).get("defaultPrompt", [])
    if (
        manifest.get("name") != PLUGIN_ID
        or manifest.get("author", {}).get("name") != "FactSet"
        or manifest.get("interface", {}).get("developerName") != "FactSet"
        or app.get("apps", {}).get("factset", {}).get("id")
        != "asdk_app_699727751b1c819193883394649579e2"
        or len(prompts) != 3
        or "broker research headlines" not in prompts[2]
    ):
        raise ValueError("FactSet Codex identity or capability evidence changed")


def verify_remote_service() -> None:
    product = fetch_json(MCP_PRODUCT_URL)
    if canonical_sha256(product) != MCP_PRODUCT_SHA256:
        raise ValueError("FactSet MCP product page changed")
    try:
        card = product["components"][0]["card"]
        tools = card["versions"][0]["tools"]
    except (KeyError, IndexError, TypeError) as error:
        raise ValueError("FactSet MCP product structure changed") from error
    names = [tool.get("name") for tool in tools]
    if (
        card.get("owner") != "content.api.mcp@factset.com"
        or names != MCP_TOOL_NAMES
        or sha256("\0".join(names).encode()) != MCP_TOOL_NAMES_SHA256
    ):
        raise ValueError("FactSet MCP tool catalog changed")
    product_text = json.dumps(product, ensure_ascii=False)
    for marker in (
        "FactSet_EstimatesConsensus",
        "FactSet_GlobalPrices",
        "StreetAccount News",
        "CallStreet Transcripts",
        "Codex CLI (OpenAI)",
        "https://mcp.factset.com/content/v1",
    ):
        if marker not in product_text:
            raise ValueError(f"FactSet MCP product is missing {marker!r}")

    resource = fetch_json(RESOURCE_URL)
    oidc = fetch_json(OIDC_URL)
    if (
        canonical_sha256(resource) != RESOURCE_SHA256
        or resource.get("resource") != MCP_URL
        or resource.get("authorization_servers") != ["https://auth.factset.com"]
        or resource.get("scopes_supported") != ["openid", "mcp", "email"]
    ):
        raise ValueError("FactSet protected-resource metadata changed")
    if (
        canonical_sha256(oidc) != OIDC_SHA256
        or oidc.get("issuer") != "https://auth.factset.com"
        or oidc.get("registration_endpoint")
        != "https://auth.factset.com/as/clients.oauth2"
        or "authorization_code" not in oidc.get("grant_types_supported", [])
        or "client_credentials" not in oidc.get("grant_types_supported", [])
        or "S256" not in oidc.get("code_challenge_methods_supported", [])
    ):
        raise ValueError("FactSet OIDC metadata changed")

    initialize = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {
                "name": "ghast-factset-audit",
                "version": "1.0.0",
            },
        },
    }
    probes = [
        (
            MCP_URL,
            initialize,
            "application/json, text/event-stream",
        ),
        (
            f"{RESEARCH_BASE}/search",
            {
                "data": {"ids": ["AAPL-US"]},
                "meta": {
                    "pagination": {"limit": 1, "offset": 0},
                    "sort": ["-storyDateTime"],
                },
            },
            "application/json",
        ),
        (
            f"{EXPLANATION_BASE}/explanation",
            {
                "data": {
                    "id": "AAPL-US",
                    "startDate": "2026-08-01",
                    "endDate": "2026-08-14",
                }
            },
            "application/json",
        ),
    ]
    for url, payload, accept in probes:
        try:
            fetch(
                url,
                data=json.dumps(payload).encode(),
                headers={
                    "Accept": accept,
                    "Content-Type": "application/json",
                },
            )
            raise ValueError(f"FactSet unexpectedly allowed anonymous {url}")
        except urllib.error.HTTPError as error:
            if error.code != 401 or error.read() != b"Authentication Failed":
                raise ValueError(
                    f"FactSet unauthenticated boundary changed at {url}"
                ) from error


def render_api_script() -> str:
    return r'''#!/usr/bin/env python3
"""Call FactSet Investment Research and Security Explanation APIs."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


RESEARCH_BASE = "https://api.factset.com/content/investment-research/v1"
EXPLANATION_BASE = "https://api.factset.com/analytics/security-explanation/v1"
META_ENDPOINTS = {
    "time-zones": "/meta/time-zones",
    "categories": "/meta/categories",
    "research-contributors": "/meta/research-contributors",
    "research-analysts": "/meta/research-analysts",
    "security-types": "/meta/security-types",
    "asset-types": "/meta/asset-types",
}
SEARCH_FILTERS = {
    "startDateRelative",
    "endDateRelative",
    "timezone",
    "categories",
    "primaryId",
    "reportFoci",
    "securityTypes",
    "assetTypes",
    "assetClasses",
    "coverageActions",
    "compilationIndicators",
    "disciplines",
    "issuerTypes",
    "periodicities",
    "purposes",
    "researchApproaches",
}
EXPLANATION_ID = re.compile(r"^[A-Za-z0-9._:-]{1,160}$")


class FactSetError(RuntimeError):
    pass


def env(name):
    value = os.environ.get(name)
    return value if value else None


def authentication():
    token = env("FACTSET_ACCESS_TOKEN")
    if token:
        return "bearer", f"Bearer {token}"
    username = env("FACTSET_USERNAME_SERIAL")
    api_key = env("FACTSET_API_KEY")
    if username and api_key:
        encoded = base64.b64encode(f"{username}:{api_key}".encode()).decode()
        return "api-key", f"Basic {encoded}"
    raise FactSetError(
        "Set FACTSET_ACCESS_TOKEN, or both FACTSET_USERNAME_SERIAL and "
        "FACTSET_API_KEY, in the local environment"
    )


def request_json(url, *, payload=None):
    _, authorization = authentication()
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(
        url,
        data=data,
        method="GET" if data is None else "POST",
        headers={
            "User-Agent": "ghast-factset-adapter/1.0",
            "Accept": "application/json",
            "Authorization": authorization,
            **({"Content-Type": "application/json"} if data is not None else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
            headers = response.headers
    except urllib.error.HTTPError as error:
        body = error.read()
        request_id = (
            error.headers.get("X-FactSet-Api-Request-Key")
            or error.headers.get("X-DataDirect-Request-Key")
        )
        detail = f"HTTP {error.code}"
        try:
            parsed = json.loads(body)
            errors = parsed.get("errors") or []
            if errors:
                item = errors[0]
                detail += (
                    f" code={item.get('code', 'unknown')}"
                    f" title={item.get('title', 'request failed')}"
                    f" detail={item.get('detail', '')}"
                )
        except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
            pass
        if request_id:
            detail += f" request_id={request_id}"
        raise FactSetError(f"FactSet request failed: {detail}") from error
    except urllib.error.URLError as error:
        raise FactSetError(
            f"FactSet network request failed: {error.reason}"
        ) from error
    try:
        result = json.loads(body) if body else {}
    except json.JSONDecodeError as error:
        raise FactSetError("FactSet returned invalid JSON") from error
    request_id = (
        headers.get("X-FactSet-Api-Request-Key")
        or headers.get("X-DataDirect-Request-Key")
    )
    if request_id and isinstance(result, dict):
        result.setdefault("_factset_request_id", request_id)
    return result


def parse_date(value):
    try:
        return dt.date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from error


def valid_dates(start, end):
    if start and end and start > end:
        raise FactSetError("start date must not be after end date")


def parse_json_object(value):
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise argparse.ArgumentTypeError("value must be a JSON object") from error
    if not isinstance(parsed, dict):
        raise argparse.ArgumentTypeError("value must be a JSON object")
    unknown = sorted(set(parsed) - SEARCH_FILTERS)
    if unknown:
        raise argparse.ArgumentTypeError(
            f"unsupported filter keys: {', '.join(unknown)}"
        )
    return parsed


def research_data(args, *, count=False):
    valid_dates(args.start_date, args.end_date)
    data = dict(args.filters_json or {})
    if args.ids:
        data["ids"] = args.ids
    if args.start_date:
        data["startDate"] = args.start_date.isoformat()
    if args.end_date:
        data["endDate"] = args.end_date.isoformat()
    if args.search_text:
        data["searchText"] = args.search_text
    if args.contributor_id:
        data["contributorId"] = args.contributor_id
    if args.analyst_id:
        data["analystId"] = args.analyst_id
    if args.rating_action:
        data["ratingActions"] = args.rating_action
    if args.target_action:
        data["targetActions"] = args.target_action
    if args.weighting_action:
        data["weightingActions"] = args.weighting_action
    if "startDate" in data and "startDateRelative" in data:
        raise FactSetError(
            "use either startDate or startDateRelative, not both"
        )
    if "endDate" in data and "endDateRelative" in data:
        raise FactSetError(
            "use either endDate or endDateRelative, not both"
        )
    if not data:
        raise FactSetError("research request must contain at least one criterion")
    if len(data.get("ids") or []) > (10 if count else 1000):
        raise FactSetError(
            f"research {'count' if count else 'search'} accepts at most "
            f"{10 if count else 1000} IDs"
        )
    if count:
        data["source"] = "FRC"
    else:
        data["sources"] = ["FRC"]
    return data


def normalize_research(payload):
    groups = []
    for group in payload.get("data") or []:
        documents = []
        for document in group.get("documents") or []:
            documents.append(
                {
                    "headline": document.get("headline"),
                    "source": document.get("source"),
                    "primary_ids": document.get("primaryIds"),
                    "all_ids": document.get("allIds"),
                    "categories": document.get("categories"),
                    "published_at": document.get("storyDateTime"),
                    "contributor": {
                        "name": document.get("contributorName"),
                        "id": document.get("contributorId"),
                    },
                    "analysts": [
                        {"name": name, "id": analyst_id}
                        for name, analyst_id in zip(
                            document.get("analystName") or [],
                            document.get("analystId") or [],
                        )
                    ],
                    "pages": document.get("pages"),
                    "document_id": document.get("documentId"),
                    "report_foci": document.get("reportFoci"),
                    "coverage_actions": document.get("coverageActions"),
                    "rating_actions": document.get("ratingActions"),
                    "target_actions": document.get("targetActions"),
                    "weighting_actions": document.get("weightingActions"),
                    "research_approaches": document.get("researchApproaches"),
                    "licensed_document_link": document.get("link"),
                }
            )
        groups.append(
            {
                "request_id": group.get("requestId"),
                "documents": documents,
                "error": group.get("error"),
            }
        )
    return {
        "usage_notice": (
            "Metadata and links are entitlement-aware. Do not automatically "
            "download, persist, quote, or redistribute licensed research "
            "documents. Open links only for an entitled user who requested it."
        ),
        "groups": groups,
        "pagination": (payload.get("meta") or {}).get("pagination"),
        "_factset_request_id": payload.get("_factset_request_id"),
    }


def research_search(args):
    payload = {
        "data": research_data(args),
        "meta": {
            "pagination": {"limit": args.limit, "offset": args.offset},
            "sort": [
                "storyDateTime" if args.oldest_first else "-storyDateTime"
            ],
        },
    }
    return normalize_research(
        request_json(f"{RESEARCH_BASE}/search", payload=payload)
    )


def research_count(args):
    data = research_data(args, count=True)
    return request_json(f"{RESEARCH_BASE}/count", payload={"data": data})


def research_meta(args):
    query = {}
    if args.kind == "research-analysts" and args.contributor_id is None:
        raise FactSetError(
            "research-analysts requires --contributor-id"
        )
    if args.contributor_id is not None:
        query["contributorId"] = args.contributor_id
    suffix = META_ENDPOINTS[args.kind]
    if query:
        suffix += "?" + urllib.parse.urlencode(query)
    return request_json(RESEARCH_BASE + suffix)


def explanation_payload(args):
    valid_dates(args.start_date, args.end_date)
    if (
        args.start_date <= dt.date(2020, 12, 31)
        or args.end_date <= dt.date(2020, 12, 31)
    ):
        raise FactSetError(
            "Security Explanation dates must be after 2020-12-31"
        )
    if args.broker_id and args.broker_style == "none":
        raise FactSetError(
            "--broker-id requires --broker-style summary or footnote"
        )
    data = {
        "id": validate_explanation_id(args.security_id),
        "startDate": args.start_date.isoformat(),
        "endDate": args.end_date.isoformat(),
        "enableLinks": args.enable_links,
        "explanationStyle": args.explanation_style,
        "includePerformance": args.include_performance,
        "internalInvestmentRationale": args.internal_rationale,
        "includeCompanyDescription": args.include_company_description,
        "includeMarketSummary": not args.no_market_summary,
        "includeSecuritySummary": not args.no_security_summary,
    }
    if args.broker_style != "none" or args.broker_id:
        data["brokerResearchSummary"] = {
            "style": args.broker_style,
            **({"brokerIds": args.broker_id} if args.broker_id else {}),
        }
    return {"data": data}


def explanation_create(args):
    return request_json(
        f"{EXPLANATION_BASE}/explanation",
        payload=explanation_payload(args),
    )


def validate_explanation_id(value):
    if not EXPLANATION_ID.fullmatch(value):
        raise FactSetError("invalid explanation request ID")
    return value


def explanation_status(args):
    request_id = validate_explanation_id(args.request_id)
    return request_json(
        f"{EXPLANATION_BASE}/explanation/"
        f"{urllib.parse.quote(request_id, safe='')}/status"
    )


def explanation_result(args):
    request_id = validate_explanation_id(args.request_id)
    return request_json(
        f"{EXPLANATION_BASE}/explanation/"
        f"{urllib.parse.quote(request_id, safe='')}/result"
    )


def auth_check(_args):
    mode, _ = authentication()
    return {"configured": True, "mode": mode}


def add_research_arguments(parser):
    parser.add_argument(
        "--id",
        dest="ids",
        action="append",
        help="FactSet exchange symbol, CUSIP, ISIN, entity ID, or SEDOL.",
    )
    parser.add_argument("--start-date", type=parse_date)
    parser.add_argument("--end-date", type=parse_date)
    parser.add_argument("--search-text")
    parser.add_argument("--contributor-id", type=int, action="append")
    parser.add_argument("--analyst-id", type=int, action="append")
    parser.add_argument("--rating-action", action="append")
    parser.add_argument("--target-action", action="append")
    parser.add_argument("--weighting-action", action="append")
    parser.add_argument(
        "--filters-json",
        type=parse_json_object,
        help="Additional official search data fields as one JSON object.",
    )


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    auth = subparsers.add_parser("auth-check")
    auth.set_defaults(handler=auth_check)

    search = subparsers.add_parser("research-search")
    add_research_arguments(search)
    search.add_argument("--limit", type=int, choices=range(1, 501), default=25)
    search.add_argument("--offset", type=int, default=0)
    search.add_argument("--oldest-first", action="store_true")
    search.set_defaults(handler=research_search)

    count = subparsers.add_parser("research-count")
    add_research_arguments(count)
    count.set_defaults(handler=research_count)

    meta = subparsers.add_parser("research-meta")
    meta.add_argument("kind", choices=sorted(META_ENDPOINTS))
    meta.add_argument("--contributor-id", type=int)
    meta.set_defaults(handler=research_meta)

    create = subparsers.add_parser("explanation-create")
    create.add_argument("security_id")
    create.add_argument("--start-date", type=parse_date, required=True)
    create.add_argument("--end-date", type=parse_date, required=True)
    create.add_argument(
        "--explanation-style",
        choices=["short", "long", "ultraShort"],
        default="short",
    )
    create.add_argument("--enable-links", action="store_true")
    create.add_argument("--include-performance", action="store_true")
    create.add_argument("--include-company-description", action="store_true")
    create.add_argument("--no-market-summary", action="store_true")
    create.add_argument("--no-security-summary", action="store_true")
    create.add_argument(
        "--internal-rationale",
        choices=["none", "summary", "footnote"],
        default="none",
    )
    create.add_argument(
        "--broker-style",
        choices=["none", "summary", "footnote"],
        default="none",
    )
    create.add_argument("--broker-id", type=int, action="append")
    create.set_defaults(handler=explanation_create)

    status = subparsers.add_parser("explanation-status")
    status.add_argument("request_id")
    status.set_defaults(handler=explanation_status)

    result = subparsers.add_parser("explanation-result")
    result.add_argument("request_id")
    result.set_defaults(handler=explanation_result)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if getattr(args, "offset", 0) < 0:
        parser.error("--offset must be non-negative")
    try:
        result = args.handler(args)
    except FactSetError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def render_skill() -> str:
    return """---
name: factset
description: >-
  Research public and private companies, securities, estimates, prices,
  fundamentals, ownership, events, transcripts, StreetAccount news, supply
  chains, funds, and licensed broker research through FactSet's official MCP
  and APIs.
---

# FactSet

Use the official hosted MCP for the normal FactSet data surface. Use the
bundled `scripts/factset_api.py` only for Investment Research metadata and
Security Explanation workflows that are not named in the public MCP catalog.

## Route the request

| Intent | Official surface |
|---|---|
| Consensus estimates, surprises, ratings, guidance | `FactSet_EstimatesConsensus` |
| Prices, returns, volume, dividends, corporate actions | `FactSet_GlobalPrices` |
| Financial statements, ratios, margins, valuation | `FactSet_Fundamentals` and `FactSet_Metrics` |
| Debt and liquidity | `FactSet_DebtCapitalStructure` |
| Ownership, insiders, institutional or fund holdings | `FactSet_Ownership` |
| Events, transcripts, StreetAccount news, filings | `FactSet_CalendarEvents` and `FactSet_UnstructuredContent` |
| Entity, people, M&A, PE/VC, private companies | Matching `FactSet_*` MCP tool |
| Funds, ETFs, screens, supply chain, GeoRev, RBICS | Matching `FactSet_*` MCP tool |
| Broker research headlines and action metadata | `research-search` adapter command |
| Broker-research-backed performance explanation | `explanation-create`, then status/result |

The live authenticated MCP catalog and schemas are authoritative. Inspect them
before promising a field or dataset.

## Resolve the adapter

Resolve `SKILL_DIR` from this loaded skill, then:

```bash
FACTSET_API="$SKILL_DIR/scripts/factset_api.py"
```

Use one of these local credential modes:

- `FACTSET_ACCESS_TOKEN` for an existing bearer token.
- `FACTSET_USERNAME_SERIAL` plus `FACTSET_API_KEY` for Basic API-key auth.

Never request credentials in chat, print them, write them to files, or place
them in visible command arguments. FactSet's official SDK can obtain OAuth
client-credentials tokens; this adapter intentionally consumes an existing
token instead of managing client secrets.

```bash
python3 "$FACTSET_API" auth-check
```

## Core financial workflows

For estimates and price performance, resolve the exact security first. State:

- Identifier and exchange.
- Currency and unit scaling.
- Fiscal period, calendar date, and estimate snapshot date.
- Reported, adjusted, restated, or consensus basis.
- Price-return window and whether dividends are included.

For peer comparisons, use the same metrics, currency basis, fiscal alignment,
and valuation date across every company. Do not mix trailing, current-year,
and next-year multiples without labels. Preserve unavailable values rather
than silently changing metrics.

For "latest" requests, use explicit absolute dates and report the newest
available observation. Do not treat a stale observation as current.

## Broker research headlines

Search metadata without downloading reports:

```bash
python3 "$FACTSET_API" research-search \\
  --id AAPL-US \\
  --start-date 2026-08-01 \\
  --end-date 2026-08-14 \\
  --limit 25
```

Useful filters include `--search-text`, `--contributor-id`, `--analyst-id`,
`--rating-action`, `--target-action`, and `--weighting-action`. Use
`research-meta research-contributors` and `research-meta research-analysts`
to resolve entitlement-aware IDs. `--filters-json` exposes the remaining
official search fields without accepting arbitrary endpoint or URL changes.

Summarize sentiment only from explicit headline language, rating actions,
target actions, weighting actions, and an entitled Security Explanation.
Separate positive, negative, neutral, and mixed evidence by contributor and
date. A document count is not sentiment.

Returned links point to licensed documents. Do not automatically open,
download, quote, cache, index, persist, or redistribute them. A user request
and the recipient's FactSet Research Connect entitlement are required before
opening a report.

## Security Explanation

Create an asynchronous explanation:

```bash
python3 "$FACTSET_API" explanation-create AAPL-US \\
  --start-date 2026-08-01 \\
  --end-date 2026-08-14 \\
  --broker-style summary \\
  --enable-links
```

Then poll once at a time and retrieve only after completion:

```bash
python3 "$FACTSET_API" explanation-status <request-id>
python3 "$FACTSET_API" explanation-result <request-id>
```

Do not loop rapidly. Respect `Retry-After` and service rate limits. Broker
summaries require the appropriate FactSet entitlement. Broker IDs produce
separate summaries and must not be merged into a false consensus.

## Safety and quality

- All included surfaces are read-only, but API calls can consume licensed
  capacity and asynchronous jobs. Confirm broad searches before execution.
- Do not present FactSet data, estimates, research, or generated explanations
  as investment advice or guaranteed outcomes.
- Distinguish reported facts, analyst opinion, consensus estimates, company
  guidance, FactSet-generated explanation, and assistant inference.
- Preserve source, contributor, analyst, document date, observation date,
  units, currency, and entitlement boundaries.
- Do not expose personal data from people, ownership, insider, or private
  company datasets beyond the user's authorized purpose.
- Do not retry 401, 403, 429, or asynchronous creation automatically. Report
  the request ID when FactSet provides one.
- Never infer that StreetAccount news is broker research. Use the Investment
  Research API for broker reports and Security Explanation for entitled broker
  summaries.
"""


def render_readme(api_hash: str) -> str:
    return f"""# factset

Connect financial data, analytics, and licensed research through FactSet's
official hosted MCP and official REST APIs.

## Official sources

The hosted MCP endpoint is `{MCP_URL}`. FactSet's current public product page
publishes 20 tools for fundamentals, debt, estimates, prices, ownership, M&A,
people, events, entity reference, funds, screeners, unstructured content,
metrics, private markets, GeoRev, supply chain, RBICS, and fixed-income terms.
The canonical product JSON SHA-256 is `{MCP_PRODUCT_SHA256}` and the ordered
tool-name SHA-256 is `{MCP_TOOL_NAMES_SHA256}`.

The official `factset/enterprise-sdk` repository is pinned to
`{OFFICIAL_REVISION}` with tree `{OFFICIAL_TREE}` and Apache-2.0 licensing.
Its Investment Research 1.0 and Security Explanation 1.6 specifications have
SHA-256 values `{SOURCE_HASHES["specs/InvestmentResearch.v1.yaml"]}` and
`{SOURCE_HASHES["specs/SecurityExplanation.v1.json"]}`.

The bundled standard-library adapter has SHA-256 `{api_hash}`. It calls only
the official Investment Research and Security Explanation endpoints, accepts
existing bearer or API-key credentials from the environment, performs no
automatic retries, and does not download research documents.

## Capability comparison

- Codex: consensus estimates and recent prices, peer margin/growth/valuation
  comparisons, and recent broker research headlines with sentiment through a
  private FactSet app connector.
- Ghast MCP: the same estimates, price, fundamentals, valuation, screening,
  entity, ownership, event, transcript, news, private-market, supply-chain,
  fund, and fixed-income product surfaces through FactSet's official hosted
  MCP and browser OAuth.
- Ghast API adapter: exact broker research headlines, contributors, analysts,
  dates, categories, rating/target/weighting actions, entitlement-aware links,
  and FactSet Security Explanation with optional broker summaries.

The broker-research API supplement is important: the public MCP catalog names
StreetAccount News, CallStreet transcripts, and filings under unstructured
content, but does not name investment research. Ghast does not mislabel news
as broker research.

## Authentication and licensing

Hosted MCP authentication uses FactSet browser OAuth. The canonical protected
resource and OIDC metadata SHA-256 values are `{RESOURCE_SHA256}` and
`{OIDC_SHA256}`. Anonymous initialization and anonymous API probes return the
expected HTTP 401 `Authentication Failed` boundary.

The REST adapter accepts `FACTSET_ACCESS_TOKEN`, or
`FACTSET_USERNAME_SERIAL` plus `FACTSET_API_KEY`. A FactSet account,
subscriptions, dataset and contributor entitlements, API access, OAuth
approval, and service limits remain customer-managed. Authenticated calls were
not executed during import because no customer account was supplied.

The Apache-2.0 license covers the official SDK license copied into this
package and the Ghast-authored adapter, workflow, documentation, and generic
financial-research icon. FactSet services, data, reports, trademarks, customer
content, and commercial terms remain controlled by FactSet and contributing
publishers.
"""


def render_icon() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="8" fill="#182850"/>
  <path d="M13 47h38" fill="none" stroke="#ffffff" stroke-width="4"
    stroke-linecap="round"/>
  <path d="M17 42V29h8v13m7 0V19h8v23m7 0V25h8v17"
    fill="none" stroke="#5cc8be" stroke-width="4" stroke-linejoin="round"/>
  <path d="m15 24 10-7 10 5 14-11" fill="none" stroke="#ffffff"
    stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def review(api_hash: str) -> dict:
    return {
        "verificationStatus": "official-source-verified",
        "officialDeveloper": "FactSet Research Systems Inc.",
        "officialRepository": OFFICIAL_REPOSITORY,
        "officialRevision": UPSTREAM_REVISION,
        "license": "Apache-2.0",
        "licenseEvidence": [
            (
                "factset/enterprise-sdk LICENSE at revision "
                f"{OFFICIAL_REVISION} has SHA-256 {SOURCE_HASHES['LICENSE']} "
                "and is Apache License 2.0."
            ),
            (
                "InvestmentResearch.v1.yaml and SecurityExplanation.v1.json "
                "both declare Apache License 2.0 in their official OpenAPI "
                "metadata."
            ),
            (
                "plugins/factset/LICENSE copies the official SDK license. The "
                "Ghast-authored adapter, workflow, documentation, and generic "
                "icon are distributed under the same license."
            ),
        ],
        "officialityEvidence": [
            (
                "FactSet's official developer portal publishes the hosted "
                f"MCP endpoint {MCP_URL}, owner content.api.mcp@factset.com, "
                "and a 20-tool financial-data catalog."
            ),
            (
                "The MCP product JSON has canonical SHA-256 "
                f"{MCP_PRODUCT_SHA256}; the ordered tool-name inventory has "
                f"SHA-256 {MCP_TOOL_NAMES_SHA256}."
            ),
            (
                "The official protected-resource metadata names "
                f"{MCP_URL}, authorization server https://auth.factset.com, "
                "and openid, mcp, and email scopes."
            ),
            (
                "The official OIDC metadata publishes dynamic client "
                "registration, authorization-code and client-credentials "
                "grants, and PKCE S256. Its canonical SHA-256 is "
                f"{OIDC_SHA256}."
            ),
            (
                "FactSet's official GitHub organization owns enterprise-sdk. "
                "The pinned repository publishes generated SDKs and OpenAPI "
                "specifications for FactSet APIs."
            ),
            (
                "The official Investment Research API describes broker and "
                "publisher research delivered through FactSet Research "
                "Connect, including headlines, contributors, analysts, "
                "publication dates, action metadata, and document links."
            ),
            (
                "The official Security Explanation 1.6 specification exposes "
                "an optional brokerResearchSummary with none, summary, or "
                "footnote modes and optional broker IDs."
            ),
            (
                "On August 14, 2026, anonymous MCP initialization, Investment "
                "Research search, and Security Explanation creation each "
                "returned HTTP 401 with Authentication Failed."
            ),
            (
                "A one-time disposable public loopback OAuth client "
                "registration returned HTTP 201 without a client secret. No "
                "token, account login, or credential was retained."
            ),
        ],
        "codexCapabilities": [
            (
                "Pull FactSet consensus estimates and recent price "
                "performance for a ticker."
            ),
            (
                "Compare margins, revenue growth, and valuation multiples "
                "across a peer set."
            ),
            (
                "Find recent broker research headlines for a company and "
                "summarize sentiment."
            ),
            (
                "Connect broader financial data, analytics, and investment "
                "workflows through FactSet's private app connector."
            ),
        ],
        "ghastCapabilities": [
            (
                "Direct standard MCP access to FactSet's official 20-tool "
                "catalog for estimates, pricing, fundamentals, debt, "
                "ownership, events, transcripts, StreetAccount news, filings, "
                "screeners, entity data, funds, private markets, GeoRev, "
                "supply chain, RBICS, and fixed-income terms."
            ),
            (
                "Official Investment Research API search and count workflows "
                "for broker research headlines, contributors, analysts, dates, "
                "categories, rating actions, target actions, weighting "
                "actions, and entitlement-aware document links."
            ),
            (
                "Official Security Explanation asynchronous workflows with "
                "optional performance, source links, market context, internal "
                "rationale, and entitled broker research summaries."
            ),
            (
                "A standard-library adapter supporting existing bearer tokens "
                "or FactSet username-serial/API-key authentication without "
                "persisting credentials or automatically downloading reports."
            ),
        ],
        "capabilityRelationship": (
            "equivalent-official-mcp-plus-broker-research-api-adapter"
        ),
        "limitations": [
            (
                "FactSet does not publish the hosted MCP server source. The "
                "MCP declaration connects to FactSet's service; Apache-2.0 "
                "covers the official SDK and Ghast-authored local materials, "
                "not the hosted implementation or data."
            ),
            (
                "Authenticated tools/list and customer-data calls were not "
                "executed because no FactSet customer account, subscription, "
                "or dataset entitlement was supplied. Live schemas and "
                "workspace permissions remain authoritative."
            ),
            (
                "MCP browser OAuth requires an eligible FactSet account and "
                "service provisioning. The authorization request could not be "
                "completed without a customer login."
            ),
            (
                "Investment Research requires FactSet Research Connect and "
                "contributor entitlements. Document links are licensed and "
                "must not be automatically downloaded, persisted, quoted, "
                "indexed, or redistributed."
            ),
            (
                "Security Explanation is asynchronous and broker summaries "
                "require a separate Broker Research entitlement. The adapter "
                "does not poll automatically or retry job creation."
            ),
            (
                "StreetAccount News is not broker research. The public MCP "
                "unstructured-content tool covers news, transcripts, and "
                "filings; the separate official Investment Research and "
                "Security Explanation APIs close the Codex broker-research "
                "prompt gap."
            ),
            (
                "FactSet estimates, prices, classifications, generated "
                "explanations, and research opinions can be stale, revised, "
                "conflicting, currency-dependent, or entitlement-limited. "
                "They are not investment advice."
            ),
            (
                "People, insider, ownership, private-company, and research "
                "metadata can contain personal or commercially sensitive data "
                "and must remain scoped to the user's authorized purpose."
            ),
            (
                "A generic financial-research icon is used because the private "
                "Codex marketplace artwork is not redistributed."
            ),
        ],
        "verification": [
            (
                "python3 scripts/import-factset-plugin.py "
                "--source-root ../upstreams/factset-enterprise-sdk "
                "--openai-source ../openai-plugins"
            ),
            (
                f"Verify official SDK revision {OFFICIAL_REVISION}, tree "
                f"{OFFICIAL_TREE}, clean worktree, Apache-2.0 license, README, "
                "and both pinned API specification hashes."
            ),
            (
                "Verify FactSet's official MCP product JSON, owner, endpoint, "
                "all 20 ordered tool names, tool summaries, and current client "
                "documentation markers."
            ),
            (
                "Verify protected-resource and OIDC metadata canonical hashes, "
                "authorization server, scopes, dynamic registration endpoint, "
                "grant types, and PKCE S256."
            ),
            (
                "Probe anonymous MCP initialize, Investment Research search, "
                "and Security Explanation create; require HTTP 401 and exact "
                "Authentication Failed response."
            ),
            (
                "Parse and normalize the official Investment Research sample "
                "through the generated adapter; verify metadata, action fields, "
                "entitlement link, and no document download."
            ),
            (
                "Build a Security Explanation request locally and verify "
                "required dates, broker summary mode, broker IDs, and no "
                "network access during the test."
            ),
            (
                f"Verify generated adapter SHA-256 {api_hash} and Python syntax."
            ),
            (
                f"Verify OpenAI snapshot {OPENAI_REVISION} FactSet manifest, "
                "private app ID, default prompts, and both icon hashes without "
                "redistributing those files."
            ),
            "python3 scripts/build-ghast-catalog.py",
            (
                "python3 scripts/audit-third-party-plugins.py "
                "--source ../openai-plugins"
            ),
            "python3 scripts/validate-ghast-repository.py",
            "unzip -tqq packages/factset.zip",
        ],
    }


def test_adapter(script_path: Path) -> None:
    spec = importlib.util.spec_from_file_location(
        "factset_adapter", script_path
    )
    if spec is None or spec.loader is None:
        raise ValueError("Cannot import generated FactSet adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sample = {
        "data": [
            {
                "requestId": "IBM-US",
                "documents": [
                    {
                        "headline": (
                            "Zukin's Next Week Today 4/7/2023 "
                            "(Wolfe Research) 97 pages"
                        ),
                        "source": "FRC",
                        "allIds": ["IBM-US"],
                        "primaryIds": ["IBM-US"],
                        "storyDateTime": "2023-03-07T19:40:26Z",
                        "categories": ["CN:US"],
                        "link": "https://api.factset.com/licensed-document",
                        "contributorName": "Wolfe Research",
                        "contributorId": 6684559,
                        "analystName": ["Alex Zukin"],
                        "analystId": [8240309],
                        "pages": 97,
                        "documentId": "sample",
                        "ratingActions": ["Reiterate"],
                        "targetActions": ["Increase"],
                        "weightingActions": ["Reiterate"],
                    }
                ],
            }
        ],
        "meta": {
            "pagination": {"isEstimatedTotal": False, "total": 1}
        },
        "_factset_request_id": "audit-request",
    }
    normalized = module.normalize_research(sample)
    document = normalized["groups"][0]["documents"][0]
    if (
        document["headline"] != sample["data"][0]["documents"][0]["headline"]
        or document["contributor"]["name"] != "Wolfe Research"
        or document["rating_actions"] != ["Reiterate"]
        or document["target_actions"] != ["Increase"]
        or document["licensed_document_link"]
        != "https://api.factset.com/licensed-document"
        or "content" in document
    ):
        raise ValueError("Generated FactSet research normalization failed")

    parser = module.build_parser()
    args = parser.parse_args(
        [
            "explanation-create",
            "AAPL-US",
            "--start-date",
            "2026-08-01",
            "--end-date",
            "2026-08-14",
            "--broker-style",
            "summary",
            "--broker-id",
            "6",
            "--enable-links",
        ]
    )
    payload = module.explanation_payload(args)
    data = payload["data"]
    if (
        data["id"] != "AAPL-US"
        or data["startDate"] != "2026-08-01"
        or data["endDate"] != "2026-08-14"
        or data["enableLinks"] is not True
        or data["brokerResearchSummary"]
        != {"style": "summary", "brokerIds": [6]}
    ):
        raise ValueError("Generated FactSet explanation payload failed")

    count_args = parser.parse_args(
        ["research-count", "--id", "IBM-US", "--start-date", "2026-08-01"]
    )
    count_data = module.research_data(count_args, count=True)
    if (
        count_data.get("source") != "FRC"
        or "sources" in count_data
        or count_data.get("ids") != ["IBM-US"]
    ):
        raise ValueError("Generated FactSet count payload failed")

    result = subprocess.run(
        ["python3", str(script_path), "--help"],
        check=True,
        capture_output=True,
        text=True,
    )
    for command in (
        "research-search",
        "research-count",
        "research-meta",
        "explanation-create",
        "explanation-status",
        "explanation-result",
    ):
        if command not in result.stdout:
            raise ValueError(f"FactSet adapter help is missing {command}")


def write_plugin(source: Path) -> str:
    api_source = render_api_script()
    api_hash = sha256(api_source.encode())
    with tempfile.TemporaryDirectory(
        prefix=".factset-", dir=PLUGIN_DIR
    ) as temp:
        staging = Path(temp)
        (staging / ".ghast-plugin").mkdir()
        (staging / "assets").mkdir()
        skill_dir = staging / "skills" / PLUGIN_ID
        (skill_dir / "scripts").mkdir(parents=True)

        manifest = {
            "name": PLUGIN_ID,
            "version": "1.0.2-ghast.1",
            "description": (
                "Research financial data, analytics, and licensed broker "
                "research through FactSet's official MCP and APIs."
            ),
            "category": "finance",
            "author": {
                "name": "FactSet Research Systems Inc.",
                "url": "https://www.factset.com",
            },
            "homepage": "https://developer.factset.com/mcp",
            "repository": OFFICIAL_REPOSITORY,
            "upstreamRevision": UPSTREAM_REVISION,
            "license": "Apache-2.0",
            "portStatus": "full",
            "icon": "./assets/icon.svg",
            "skills": "./skills/",
            "mcpServers": "./.mcp.json",
        }
        (staging / ".ghast-plugin/plugin.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        )
        (staging / ".mcp.json").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "factset": {"type": "http", "url": MCP_URL}
                    }
                },
                indent=2,
            )
            + "\n"
        )
        shutil.copy2(source / "LICENSE", staging / "LICENSE")
        (staging / "assets/icon.svg").write_text(render_icon())
        (skill_dir / "SKILL.md").write_text(render_skill())
        script_path = skill_dir / "scripts/factset_api.py"
        script_path.write_text(api_source)
        script_path.chmod(0o755)
        (staging / "README.md").write_text(render_readme(api_hash))
        test_adapter(script_path)

        target = PLUGIN_DIR / PLUGIN_ID
        if target.exists():
            shutil.rmtree(target)
        staging.rename(target)
    return api_hash


def update_review(api_hash: str) -> None:
    data = json.loads(REVIEWS_PATH.read_text())
    data.setdefault("plugins", {})[PLUGIN_ID] = review(api_hash)
    REVIEWS_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    )


def main() -> int:
    args = parse_args()
    source = args.source_root.resolve()
    openai_source = args.openai_source.resolve()
    verify_source(source)
    verify_openai_source(openai_source)
    verify_remote_service()
    api_hash = write_plugin(source)
    update_review(api_hash)
    print(
        "imported verified FactSet official MCP and API adapter "
        f"(adapter SHA-256 {api_hash})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
