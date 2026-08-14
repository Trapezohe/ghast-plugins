#!/usr/bin/env python3
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
