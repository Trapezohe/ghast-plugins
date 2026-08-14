#!/usr/bin/env python3
"""Call Dow Jones Factiva Retrieval API without storing content or tokens."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid


AUTH_URL = "https://accounts.dowjones.com/oauth2/v1/token"
RETRIEVAL_URL = "https://api.dowjones.com/content/gen-ai/retrieve"
TOKEN_USAGE_URL = "https://api.dowjones.com/content/gen-ai/token-usage"
FACTIVA_ARTICLE_URL = "https://app.dowjones.com/factiva/article"
ACCEPT = "application/vnd.dowjones.genai-content.v_1.0"
VALID_FILTERS = {
    "Language",
    "Organization",
    "NewsSubject",
    "Industry",
    "Source",
    "Region",
}
VALID_RANGES = {
    "LastDay",
    "Last2Days",
    "LastWeek",
    "Last2Weeks",
    "LastMonth",
    "Last3Months",
    "Last6Months",
    "LastYear",
    "Last2Years",
    "Last5Years",
    "AllDates",
}


class FactivaError(RuntimeError):
    pass


def env(*names):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def require_env(*names):
    value = env(*names)
    if not value:
        raise FactivaError(f"Missing environment variable: {' or '.join(names)}")
    return value


def request_json(url, *, token=None, form=None, payload=None):
    headers = {
        "User-Agent": "ghast-factiva-adapter/1.0",
        "Accept": ACCEPT if url != AUTH_URL else "application/json",
    }
    data = None
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if form is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = urllib.parse.urlencode(form).encode()
    elif payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode()
    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method="POST" if data is not None else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
    except urllib.error.HTTPError as error:
        body = error.read()
        detail = f"HTTP {error.code}"
        try:
            parsed = json.loads(body)
            errors = parsed.get("errors") or []
            if errors:
                item = errors[0]
                detail += (
                    f" code={item.get('code', 'unknown')}"
                    f" title={item.get('title', 'request failed')}"
                )
        except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
            pass
        raise FactivaError(f"Factiva request failed: {detail}") from error
    except urllib.error.URLError as error:
        raise FactivaError(f"Factiva network request failed: {error.reason}") from error
    try:
        return json.loads(body) if body else {}
    except json.JSONDecodeError as error:
        raise FactivaError("Factiva returned invalid JSON") from error


def authz_token():
    client_id = require_env("FACTIVA_CLIENT_ID", "FACTIVA_CLIENTID")
    username = require_env("FACTIVA_USERNAME")
    password = require_env("FACTIVA_PASSWORD")
    authn = request_json(
        AUTH_URL,
        form={
            "client_id": client_id,
            "username": username,
            "password": password,
            "connection": "service-account",
            "grant_type": "password",
            "scope": "openid service_account_id",
        },
    )
    id_token = authn.get("id_token")
    access_token = authn.get("access_token")
    if not id_token or not access_token:
        raise FactivaError("Factiva AuthN response omitted required tokens")
    authz = request_json(
        AUTH_URL,
        form={
            "client_id": client_id,
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "connection": "service-account",
            "scope": "openid pib",
            "access_token": access_token,
            "assertion": id_token,
        },
    )
    token = authz.get("access_token")
    if not token:
        raise FactivaError("Factiva AuthZ response omitted access_token")
    return token


def validate_identifier(name, value, *, required=False):
    if required and not value:
        raise FactivaError(f"Missing {name}")
    if not value:
        return None
    if len(value) > 32:
        raise FactivaError(f"{name} must be at most 32 characters")
    if "@" in value:
        raise FactivaError(f"{name} must not contain an email address or other PII")
    return value


def parse_date(value):
    try:
        return dt.date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from error


def parse_filter(value):
    if "=" not in value:
        raise argparse.ArgumentTypeError("filter must use Scope=value")
    scope, filter_value = value.split("=", 1)
    if scope not in VALID_FILTERS:
        raise argparse.ArgumentTypeError(
            f"unsupported scope {scope!r}; choose from {sorted(VALID_FILTERS)}"
        )
    if not filter_value or len(filter_value) > 2000:
        raise argparse.ArgumentTypeError("filter value must contain 1-2000 characters")
    return {"scope": scope, "value": filter_value}


def article_url(article_id, account_id=None, namespace=None):
    if not article_id.startswith("drn:"):
        article_id = f"drn:archive.newsarticle.{article_id}"
    params = {"id": article_id}
    if account_id:
        params["accountid"] = account_id
    if namespace:
        params["namespace"] = namespace
    return f"{FACTIVA_ARTICLE_URL}?{urllib.parse.urlencode(params)}"


def text_value(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return " ".join(parts)
    return ""


def normalize_retrieval(payload, *, metadata_only=False):
    meta = payload.get("meta") or {}
    metrics = meta.get("metrics_data") or {}
    articles = []
    for item in payload.get("data") or []:
        attributes = item.get("attributes") or {}
        item_meta = item.get("meta") or {}
        source = item_meta.get("source") or {}
        headline = ((attributes.get("headline") or {}).get("main") or {}).get("text")
        snippet = text_value((attributes.get("snippet") or {}).get("content"))
        content = " ".join(
            text_value(part.get("text") if isinstance(part, dict) else part)
            for part in attributes.get("content") or []
        ).strip()
        record = {
            "id": item.get("id"),
            "accession_number": item_meta.get("original_doc_id"),
            "headline": headline.strip() if isinstance(headline, str) else headline,
            "source": {
                "name": source.get("name"),
                "code": source.get("code"),
                "attribution_code": source.get("attribution_code"),
            },
            "publication_date": attributes.get("publication_date"),
            "byline": (attributes.get("byline") or {}).get("text"),
            "copyright": (attributes.get("copyright") or {}).get("text"),
            "language": (item_meta.get("language") or {}).get("code"),
            "snippet": snippet,
            "links": {
                "factiva": article_url(item.get("id") or ""),
                "api": (item.get("links") or {}).get("self"),
            },
        }
        if not metadata_only:
            record["licensed_rag_context"] = content
        articles.append(record)
    return {
        "usage_notice": (
            "Licensed RAG context is for transient model grounding only. "
            "Do not display chunks for human reading, persist them, train on them, "
            "or redistribute them. Cite every derived claim and link entitled "
            "users to Factiva."
        ),
        "metrics": {
            "total_count": meta.get("total_count", len(articles)),
            "user_id": metrics.get("user_id"),
            "work_id": metrics.get("work_id"),
            "application_id": metrics.get("application_id"),
        },
        "articles": articles,
    }


def search(args):
    query_value = args.query.strip()
    if not query_value:
        raise FactivaError("search query must not be empty")
    user_id = validate_identifier(
        "FACTIVA_USER_ID",
        args.user_id or env("FACTIVA_USER_ID"),
        required=True,
    )
    application_id = validate_identifier(
        "FACTIVA_APPLICATION_ID",
        args.application_id or env("FACTIVA_APPLICATION_ID"),
    )
    work_id = validate_identifier(
        "work_id",
        args.work_id or uuid.uuid4().hex,
        required=True,
    )
    if not 1 <= args.limit <= 100:
        raise FactivaError("--limit must be between 1 and 100")
    query = {"value": query_value}
    if args.filters:
        query["search_filters"] = args.filters
    if args.from_date or args.to_date:
        if not args.from_date or not args.to_date:
            raise FactivaError("--from-date and --to-date must be used together")
        if args.from_date > args.to_date:
            raise FactivaError("--from-date must be before or equal to --to-date")
        query["date"] = {
            "custom": {
                "from": args.from_date.isoformat(),
                "to": args.to_date.isoformat(),
            }
        }
    elif args.days_range:
        query["date"] = {"days_range": args.days_range}
    metrics = {"user_id": user_id, "work_id": work_id}
    if application_id:
        metrics["application_id"] = application_id
    payload = {
        "data": {
            "attributes": {
                "response_limit": args.limit,
                "query": query,
                "metrics_data": metrics,
            },
            "id": "GenAIRetrieval",
            "type": "genai-content",
        }
    }
    result = request_json(RETRIEVAL_URL, token=authz_token(), payload=payload)
    return normalize_retrieval(result, metadata_only=args.metadata_only)


def token_usage(args):
    if args.from_date > args.to_date:
        raise FactivaError("--from-date must be before or equal to --to-date")
    attributes = {
        "date": {
            "custom": {
                "from": args.from_date.isoformat(),
                "to": args.to_date.isoformat(),
            }
        }
    }
    if args.breakdown:
        attributes["breakdown"] = {"interval": args.breakdown}
    return request_json(
        TOKEN_USAGE_URL,
        token=authz_token(),
        payload={"data": {"attributes": attributes}},
    )


def build_parser():
    parser = argparse.ArgumentParser(
        description="Official Dow Jones Factiva Retrieval API adapter"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    auth = subparsers.add_parser("auth-check", help="Verify credentials without printing tokens")
    auth.set_defaults(handler=lambda args: {"authenticated": bool(authz_token())})

    url = subparsers.add_parser("article-url", help="Build a current Factiva article deep link")
    url.add_argument("article_id")
    url.add_argument("--account-id")
    url.add_argument("--namespace")
    url.set_defaults(
        handler=lambda args: {
            "article_id": args.article_id,
            "url": article_url(args.article_id, args.account_id, args.namespace),
        }
    )

    retrieve = subparsers.add_parser(
        "search",
        help="Retrieve licensed Factiva chunks for transient RAG grounding",
    )
    retrieve.add_argument("query")
    retrieve.add_argument("--limit", type=int, default=10)
    retrieve.add_argument("--filter", dest="filters", action="append", type=parse_filter)
    retrieve.add_argument("--days-range", choices=sorted(VALID_RANGES))
    retrieve.add_argument("--from-date", type=parse_date)
    retrieve.add_argument("--to-date", type=parse_date)
    retrieve.add_argument("--user-id")
    retrieve.add_argument("--application-id")
    retrieve.add_argument("--work-id")
    retrieve.add_argument(
        "--metadata-only",
        action="store_true",
        help="Omit licensed RAG context and return citations/metadata only",
    )
    retrieve.set_defaults(handler=search)

    usage = subparsers.add_parser("token-usage", help="Read account token consumption")
    usage.add_argument("--from-date", required=True, type=parse_date)
    usage.add_argument("--to-date", required=True, type=parse_date)
    usage.add_argument("--breakdown", choices=["day"])
    usage.set_defaults(handler=token_usage)
    return parser


def main():
    args = build_parser().parse_args()
    result = args.handler(args)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except FactivaError as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
