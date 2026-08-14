#!/usr/bin/env python3
"""Build the verified Ghast adapter for Dow Jones Factiva Retrieval API."""

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
import urllib.request
from pathlib import Path


sys.dont_write_bytecode = True

PLUGIN_ID = "dow-jones-factiva"
PLUGIN_DIR = Path("plugins")
REVIEWS_PATH = Path("third-party-plugin-reviews.json")
OFFICIAL_REPOSITORY = "https://github.com/dowjones/factiva-retrievalapi-demo"
OFFICIAL_REVISION = "231615fb3369ccafd4afb6fea4d817080922e772"
OFFICIAL_TREE = "fb75da2d4ecbc4297ecd81aabb88fac0b9d852e2"
UPSTREAM_REVISION = (
    f"{OFFICIAL_REVISION}+retrieval-28c28089596e"
    "+auth-80e5c6cd55d8+links-376678f49e7f"
)
OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
OPENAI_HASHES = {
    ".app.json": "f9feaccef8a5982cc92c0efcdc770f0f5a5c48925b582f71be3e248b7b629d4f",
    ".codex-plugin/plugin.json": (
        "999868cb2abb9c8a18a2ff192ddea2c29304e6d25bbd204c4fc4699118c92be5"
    ),
    "assets/logo.png": (
        "0aee504bacdbd6e3f57d8c55c4d77bf9d2619e01c2aaaa787593733bb045d004"
    ),
}
SOURCE_HASHES = {
    "README.md": "632ebc71d01c6309581680aafc23152ea7683df23ac0ebf7029128ee204c9414",
    "LICENSE": "7dbc27c779c62c2d918f55dd109b3dc9838e6c275835b2865c5cbea14955828e",
    "utils.py": "3bcbefec4f914cc58d04d6b2a5bd83b7f63514e13c2c0dc26561e5e0330e3b46",
    "1_get_chunks.ipynb": (
        "739e1e130656b69a02d562049714b4ee23065018f1b11c7000fadd6e0e27a9a1"
    ),
    "query.json": "2798e838d94d86a4b668095935034626fe0321b6eafdb3b9171402eb67f619bb",
    "chunks.json": "b4a547bf2cae8ab86582ea75eebc896c04f745c140d3647b5d59a0e11fb20ace",
    "article.json": "0e411cd58959870c4cc7af89faec4319a343913109dbc20c7ad7d08fae6e50f9",
    ".env.example": "0430cc2ec270b13d0ec1c63944b3dce00fa70f6e0116aaea0060befd708df799",
    "requirements.txt": (
        "e62ca971db7ea1d989174781b8d7be9454186edbacbb55682d41acb6ee9b8f8f"
    ),
}
DOCUMENTS = {
    46357: (
        "a02a68e1319120cf5d9e0644307234cf9340f35a9c59f52593de0597b70c96c1",
        (
            "contextual news searches",
            "retrieval-augmented generation",
        ),
    ),
    46361: (
        "ebf00d3b4a946c3abe398f4264628e6f64d313a0ca7eb201c6e6b9a9035ed434",
        (
            "GenAI Machine Use Subscription",
            "must not use content for model training",
        ),
    ),
    46363: (
        "b8e36ae4b51e8d4f04ef7393326ead3f1fbe7e24563c3f75d9e8ba91cd031eba",
        (
            "Chunks may not be stored persistently",
            "Direct URL to Factiva",
            "60 Transactions Per Second",
        ),
    ),
    46367: (
        "28c28089596eef83a994f35538b51fbf9398b5d7dbd27554d89a1c068aa6c7fe",
        (
            "https://api.dowjones.com/content/gen-ai/retrieve",
            "application/vnd.dowjones.genai-content.v_1.0",
            "metrics_data.work_id",
        ),
    ),
    46309: (
        "566900f2a094875705ce827c28d0237e8f75f091c65ee7bdfe0d981cd49915ee",
        (
            "Direct URLs to Factiva.com",
            "Factiva Article Fetch Endpoint",
        ),
    ),
    46307: (
        "376678f49e7f77abadd6cb9a9680135431e682541c90422c0ea9b40177d380e0",
        (
            "https://app.dowjones.com/factiva/article?id=",
            "Authentication and entitlements are managed by Factiva",
        ),
    ),
    46305: (
        "a5fe48fe83c9eea8125821197d5ce0af3d8c7a68312c52462fde132e69f3dcb4",
        (
            "https://api.dowjones.com/content/refs/",
            "article_format=FullArticle",
        ),
    ),
    47186: (
        "5953cfb053c70d4d2b6bb1af02fcd8393a894b5e692782a4d875bd324431c07c",
        (
            "This endpoint is deprecated",
            "Token Usage endpoint",
        ),
    ),
    47371: (
        "4a0a49d7f093e7ee5327d1d2adb29fb53ebe29654b18a63279838b3c775ca96d",
        (
            "https://api.dowjones.com/content/gen-ai/token-usage",
            "tokens_used",
            "twice per day",
        ),
    ),
    46236: (
        "80e5c6cd55d8e0287d19829bb103aafc135106111841dbdf7cd80043b5380e73",
        (
            "https://accounts.dowjones.com/oauth2/v1/token",
            "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "openid pib",
        ),
    ),
}
RETRIEVAL_URL = "https://api.dowjones.com/content/gen-ai/retrieve"
UNAUTHENTICATED_CODE = 1011001


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_output(repository: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def fetch(url: str, *, data: bytes | None = None, headers: dict | None = None) -> bytes:
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "User-Agent": "ghast-factiva-audit/1.0",
            **(headers or {}),
        },
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def verify_source(source: Path) -> None:
    if git_output(source, "rev-parse", "HEAD") != OFFICIAL_REVISION:
        raise ValueError(f"{source}: unexpected Factiva demo revision")
    if git_output(source, "rev-parse", "HEAD^{tree}") != OFFICIAL_TREE:
        raise ValueError(f"{source}: unexpected Factiva demo tree")
    if git_output(source, "status", "--porcelain"):
        raise ValueError(f"{source}: Factiva demo checkout is dirty")

    for path, expected_hash in SOURCE_HASHES.items():
        content = (source / path).read_bytes()
        if sha256(content) != expected_hash:
            raise ValueError(f"{source / path}: source hash changed")

    license_text = (source / "LICENSE").read_text()
    if (
        "MIT License" not in license_text
        or "Copyright (c) 2025 Dow Jones" not in license_text
    ):
        raise ValueError("Factiva demo MIT license evidence changed")

    notebook = json.loads((source / "1_get_chunks.ipynb").read_text())
    notebook_text = "\n".join(
        "".join(cell.get("source", [])) for cell in notebook.get("cells", [])
    )
    for marker in (
        "api.dowjones.com",
        "/content/gen-ai/retrieve",
        "FACTIVA_CLIENTID",
        "FACTIVA_USERNAME",
        "FACTIVA_PASSWORD",
        "metrics_data",
        "response_limit",
    ):
        if marker not in notebook_text:
            raise ValueError(f"Factiva notebook is missing {marker!r}")

    chunks = json.loads((source / "chunks.json").read_text())
    if len(chunks) != 10:
        raise ValueError("Factiva chunks sample count changed")
    for chunk in chunks:
        if not (
            chunk.get("id", "").startswith("drn:archive.newsarticle.")
            and chunk.get("links", {}).get("self", "").startswith(
                "https://api.dowjones.com/content/"
            )
            and chunk.get("attributes", {}).get("content")
            and chunk.get("meta", {}).get("source", {}).get("name")
        ):
            raise ValueError("Factiva chunks sample schema changed")


def verify_documents() -> None:
    for document_id, (expected_hash, markers) in DOCUMENTS.items():
        data = json.loads(
            fetch(
                "https://developer.dowjones.com/wp-json/wp/v2/documents/"
                f"{document_id}"
            )
        )
        content = data.get("content", {}).get("rendered", "")
        if sha256((content + "\n").encode()) != expected_hash:
            raise ValueError(f"Dow Jones document {document_id} changed")
        for marker in markers:
            if marker not in content:
                raise ValueError(
                    f"Dow Jones document {document_id} is missing {marker!r}"
                )


def verify_api_boundary() -> None:
    payload = {
        "data": {
            "attributes": {
                "response_limit": 1,
                "query": {"value": "test"},
                "metrics_data": {
                    "user_id": "0" * 32,
                    "work_id": "0" * 32,
                },
            },
            "id": "GenAIRetrieval",
            "type": "genai-content",
        }
    }
    try:
        fetch(
            RETRIEVAL_URL,
            data=json.dumps(payload).encode(),
            headers={
                "Accept": "application/vnd.dowjones.genai-content.v_1.0",
                "Content-Type": "application/json",
            },
        )
        raise ValueError("Factiva Retrieval unexpectedly allowed anonymous access")
    except urllib.error.HTTPError as error:
        body = json.loads(error.read())
        errors = body.get("errors", [])
        if (
            error.code != 403
            or not errors
            or errors[0].get("code") != UNAUTHENTICATED_CODE
            or errors[0].get("title") != "Authentication parameters missing"
        ):
            raise ValueError("Factiva Retrieval authentication boundary changed")


def verify_openai(openai_source: Path) -> None:
    if git_output(openai_source, "rev-parse", "HEAD") != OPENAI_REVISION:
        raise ValueError(f"{openai_source}: unexpected OpenAI plugin revision")
    plugin = openai_source / "plugins" / PLUGIN_ID
    for path, expected_hash in OPENAI_HASHES.items():
        if sha256((plugin / path).read_bytes()) != expected_hash:
            raise ValueError(f"{plugin / path}: OpenAI evidence changed")
    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    app = json.loads((plugin / ".app.json").read_text())
    if (
        manifest.get("name") != PLUGIN_ID
        or manifest.get("author", {}).get("name") != "Factiva, Inc."
        or manifest.get("interface", {}).get("developerName") != "Factiva, Inc."
        or app.get("apps", {}).get(PLUGIN_ID, {}).get("id")
        != "asdk_app_69a843c0928081918d0c8ecadf4b5274"
    ):
        raise ValueError("Factiva Codex developer evidence changed")


def render_api_script() -> str:
    return r'''#!/usr/bin/env python3
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
'''


def render_skill() -> str:
    return """---
name: dow-jones-factiva
description: >-
  Search licensed Factiva news for company, industry, market, and event
  research through Dow Jones's official Retrieval API, with compliant citations
  and direct Factiva article links.
---

# Dow Jones Factiva

Use the bundled `scripts/factiva_api.py` thin adapter over Dow Jones's official
Factiva Retrieval API. This is an official API integration, not an MCP server.

## Resolve the script

Resolve `SKILL_DIR` from the absolute path of this loaded skill:

```bash
FACTIVA_API="$SKILL_DIR/scripts/factiva_api.py"
```

## Access and credentials

- Factiva Retrieval API requires a project-scoped GenAI Machine Use
  subscription and service-account credentials issued by Dow Jones.
- Require local environment variables `FACTIVA_CLIENT_ID`,
  `FACTIVA_USERNAME`, and `FACTIVA_PASSWORD`. The official demo's legacy
  `FACTIVA_CLIENTID` spelling is also accepted.
- Require `FACTIVA_USER_ID`: a stable non-PII identifier of at most 32
  characters for the actual downstream user. Do not use an email address.
- `FACTIVA_APPLICATION_ID` is optional and identifies the internal
  application or integration instance.
- Never ask the user to paste credentials or tokens in chat. Never print,
  log, cache, or write them to files. `auth-check` prints only a boolean.

```bash
python3 "$FACTIVA_API" auth-check
```

## Search

Use a narrow natural-language query, a bounded result count, and only filters
supported by the official API: `Language`, `Organization`, `NewsSubject`,
`Industry`, `Source`, and `Region`.

```bash
python3 "$FACTIVA_API" search \\
  "What is the latest outlook for Nvidia earnings?" \\
  --days-range LastMonth \\
  --filter Language=en \\
  --limit 10
```

For a custom range, use both `--from-date YYYY-MM-DD` and
`--to-date YYYY-MM-DD`. Responses do not include content older than
January 1, 2025. Do not represent `Last2Years`, `Last5Years`, or `AllDates` as
covering earlier archive content.

Each search creates a new 32-character `work_id`, because Dow Jones uses it to
track one GenAI transaction. Reuse a supplied work ID only when the user is
continuing the exact same intended transaction and the licensing design calls
for that behavior.

## Licensed context boundary

- The command returns `licensed_rag_context` for transient model grounding.
  It must not be pasted into the answer, displayed for human reading, stored,
  cached, indexed, redistributed, or used to train or fine-tune a model.
- Use only the minimum relevant passages needed to produce a summary,
  comparison, or question-answering response. Do not generate a replacement
  full-length article.
- Every factual claim derived from Factiva must carry a nearby citation. Use
  the returned headline, source, publication date, and `links.factiva`.
- Direct links open in Factiva's secure environment and remain subject to the
  recipient's authentication and entitlements.
- Use `--metadata-only` when the task needs result discovery or citation
  inventory but not licensed text for generation.
- Do not persist terminal output or redirect it into files. If the host
  captures tool output, treat it as confidential licensed content.

## Research quality

- Preserve publication date, source, language, author, copyright, organization
  and taxonomy filters, and the exact query window.
- Distinguish article facts, attributed opinions, market expectations, and
  assistant inference. Do not turn one article into market consensus.
- For "latest" questions, use an explicit recent date range and sort the final
  evidence by publication date. Note when the newest licensed result is older
  than the requested period.
- Deduplicate materially identical syndicated or translated articles before
  summarizing. Keep source and language differences when they affect meaning.
- Factiva access does not validate investment conclusions. Avoid guarantees
  and preserve uncertainty, source conflicts, and stale-data limitations.

## Article links and usage

Build a Factiva deep link without retrieving content:

```bash
python3 "$FACTIVA_API" article-url \\
  "drn:archive.newsarticle.DJDN000020251022elam001f8"
```

Read account token consumption:

```bash
python3 "$FACTIVA_API" token-usage \\
  --from-date 2026-08-01 \\
  --to-date 2026-08-14 \\
  --breakdown day
```

Token usage is aggregated twice daily and is not real-time. The deprecated
Usage Metrics endpoint is intentionally not included.

## Service boundary

- Dow Jones operates the API, authentication, content, entitlements, metering,
  and deep-link destination. The bundled Python file is a Ghast-authored thin
  adapter and uses only the Python standard library.
- Do not call the Factiva AI News Feed GenAI Article Usage API for Retrieval
  API searches. Retrieval uses its own required `metrics_data` and token
  accounting; the separate reporting endpoint is available only to AI News
  Feed customers.
- Do not use Article Fetch unless the customer's separate contract explicitly
  permits content display or embedded article delivery. This plugin does not
  expose Article Fetch as a default workflow.
"""


def render_readme(api_hash: str) -> str:
    return f"""# dow-jones-factiva

Search licensed Factiva news for company, industry, market, and event research
through Dow Jones's official Factiva Retrieval API.

## Official API adapter

Dow Jones publishes Retrieval API 1.0 at `{RETRIEVAL_URL}` for contextual news
search, metadata-rich licensed chunks, summarization, question answering, and
RAG. The official developer demo is pinned to `{OFFICIAL_REVISION}` with tree
`{OFFICIAL_TREE}` and an MIT license.

Ghast packages no private Codex app mapping, Dow Jones credential, bearer
token, licensed article, sample content, official logo, or hosted service
implementation. The included standard-library adapter has SHA-256
`{api_hash}` and performs the documented two-step service-account exchange,
Retrieval request, current Factiva deep-link construction, and Token Usage
request without writing content or tokens to disk.

Official developer-document raw content hashes are pinned for Retrieval
overview, access, usage rules, endpoint 1.0, viewing options, direct links,
Article Fetch, deprecated Usage Metrics, Token Usage, and authentication.
OpenAI capability evidence is pinned to plugin snapshot `{OPENAI_REVISION}`
without redistributing its private connector or marketplace artwork.

## Capability comparison

- Codex: search Factiva's licensed global archive, research companies,
  industries, and markets, and ground answers with citations and direct
  article links through a private app connector.
- Ghast: the same current official semantic Retrieval API for licensed RAG
  context, supported Factiva taxonomy filters, date ranges, source metadata,
  compliant citations, and direct links to the secure Factiva article view.
- Ghast additionally exposes the current Token Usage endpoint for account
  consumption review.

## Contract and content boundary

A project-scoped Factiva GenAI Machine Use subscription and Dow Jones-issued
service-account credentials are required. Retrieved chunks are licensed for
transient generative use. They may not be shown as article text, persisted,
cached, redistributed, or used for model training. Every derived claim must be
attributed, and full reading should occur through an entitled Factiva link.

The MIT license in this package covers the Ghast-authored adapter, metadata,
workflow, documentation, and generic news-research icon. Factiva content,
accounts, API access, metering, rights, terms, trademarks, and service behavior
remain controlled by Dow Jones and applicable publishers.
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


def review(api_hash: str) -> dict:
    return {
        "verificationStatus": "official-source-verified",
        "officialDeveloper": "Factiva, Inc. / Dow Jones",
        "officialRepository": OFFICIAL_REPOSITORY,
        "officialRevision": UPSTREAM_REVISION,
        "license": "MIT",
        "licenseEvidence": [
            (
                "The official dowjones/factiva-retrievalapi-demo repository at "
                f"{OFFICIAL_REVISION} contains an MIT LICENSE under Copyright "
                "2025 Dow Jones."
            ),
            (
                "The plugin redistributes no Dow Jones demo notebook, sample "
                "article, private Codex connector, credential, token, official "
                "logo, or hosted implementation. Its MIT LICENSE covers only "
                "the Ghast-authored adapter and supporting files."
            ),
            f"The packaged standard-library adapter has SHA-256 {api_hash}.",
        ],
        "officialityEvidence": [
            (
                "Dow Jones's official developer platform documents Factiva "
                "Retrieval API 1.0 as a contextual news-search endpoint for "
                "metadata-rich licensed chunks, summarization, question "
                "answering, enterprise search, and RAG."
            ),
            (
                "The documented endpoint is "
                "https://api.dowjones.com/content/gen-ai/retrieve with media "
                "type application/vnd.dowjones.genai-content.v_1.0, a maximum "
                "response limit of 100, required user_id and work_id metrics, "
                "date ranges, and Factiva taxonomy filters."
            ),
            (
                "Dow Jones's current Direct URLs documentation publishes "
                "https://app.dowjones.com/factiva/article?id={article-id}; "
                "Factiva handles authentication and entitlements at the link."
            ),
            (
                "Dow Jones's current authentication documentation specifies "
                "the two-step service-account exchange at "
                "https://accounts.dowjones.com/oauth2/v1/token used by the "
                "adapter without persisting or printing tokens."
            ),
            (
                "The official Token Usage endpoint reports account GenAI token "
                "consumption by date and optional daily breakdown; the older "
                "Usage Metrics endpoint is now deprecated."
            ),
            (
                "The official dowjones/factiva-retrievalapi-demo repository is "
                f"pinned to revision {OFFICIAL_REVISION} and tree "
                f"{OFFICIAL_TREE}. Its notebook, helper, request, chunk, "
                "article, environment, requirements, README, and LICENSE hashes "
                "are verified."
            ),
            (
                "The official sample contains ten licensed search results with "
                "article IDs, source metadata, snippets, retrieval context, "
                "copyright, publication dates, and Dow Jones content links."
            ),
            (
                "An anonymous Retrieval request on August 14, 2026 returned "
                "HTTP 403 with Dow Jones error code 1011001, confirming the "
                "documented authenticated service boundary."
            ),
            (
                "OpenAI's pinned Codex snapshot identifies Factiva, Inc. as "
                "developer and describes global archive search, company, "
                "industry, and market research, licensed grounding, citations, "
                "and direct original-article links."
            ),
        ],
        "codexCapabilities": [
            (
                "Search Factiva's licensed global news archive, including "
                "premium Dow Jones sources, through a private app connector"
            ),
            (
                "Research companies, industries, and markets and ground answers "
                "in licensed content with citations and direct article links"
            ),
        ],
        "ghastCapabilities": [
            (
                "The same official contextual Factiva Retrieval API for "
                "company, industry, market, event, earnings, and news research"
            ),
            (
                "Transient licensed RAG context with headline, source, date, "
                "byline, copyright, language, accession number, and API link"
            ),
            (
                "Supported Language, Organization, NewsSubject, Industry, "
                "Source, and Region filters plus predefined or custom dates"
            ),
            (
                "Current secure Factiva article deep links for entitled users "
                "and nearby citation rules for every derived claim"
            ),
            (
                "Dow Jones two-step service-account authentication, required "
                "per-user and per-work metrics, and account Token Usage review"
            ),
        ],
        "capabilityRelationship": "equivalent-official-api-adapter-with-usage-review",
        "limitations": [
            (
                "Dow Jones does not publish an official Factiva MCP server or "
                "CLI. The bundled standard-library command is a transparent "
                "Ghast-authored adapter over the official REST API, not a "
                "vendor-authored MCP implementation."
            ),
            (
                "A project-scoped GenAI Machine Use subscription, Dow Jones "
                "service account, credentials, allowed integration, content "
                "rights, archive scope, output-distribution terms, and service "
                "limits remain customer-managed."
            ),
            (
                "Authenticated Retrieval and token-usage calls were not "
                "executed because no Factiva customer credentials or licensed "
                "content were supplied. Official sample schemas, current docs, "
                "the unauthenticated boundary, and local adapter behavior were "
                "verified."
            ),
            (
                "Retrieval responses currently exclude content older than "
                "January 1, 2025, even for Last2Years, Last5Years, or AllDates. "
                "This may be narrower than the archive exposed by the private "
                "Codex connector."
            ),
            (
                "Retrieved chunks may not be displayed for human reading, "
                "persisted, cached, indexed, redistributed, or used for model "
                "training. Full-length synthetic articles are prohibited."
            ),
            (
                "Direct Factiva links work only for authenticated, entitled "
                "recipients. Article Fetch is separately licensed for embedded "
                "full-text display and is intentionally not exposed as a "
                "default plugin workflow."
            ),
            (
                "Each Retrieval request records user_id and a new work_id and "
                "consumes licensed tokens. The adapter performs no automatic "
                "retry to avoid duplicate retrieval or metering."
            ),
            (
                "Token usage is aggregated twice daily and may include "
                "duplicate consumption before Dow Jones applies its 24-hour "
                "deduplication rule."
            ),
            (
                "Factiva articles can contain copyrighted, personal, market-"
                "sensitive, translated, duplicated, stale, or conflicting "
                "material. Responses must preserve source attribution, dates, "
                "uncertainty, and user authorization."
            ),
            (
                "A generic news-research icon is used because no official "
                "Factiva brand asset with clear redistribution permission is "
                "copied into this package."
            ),
        ],
        "verification": [
            (
                "python3 scripts/import-factiva-plugin.py "
                "--source-root ../upstreams/factiva-retrievalapi-demo "
                "--openai-source ../openai-plugins"
            ),
            (
                f"Verify official revision {OFFICIAL_REVISION}, tree "
                f"{OFFICIAL_TREE}, MIT license, and all pinned source hashes"
            ),
            (
                "Verify raw official developer-document hashes for Retrieval "
                "overview, access requirements, usage guidelines, endpoint "
                "1.0, article viewing, direct links, Article Fetch, Usage "
                "Metrics, Token Usage, and authentication"
            ),
            (
                "Probe unauthenticated Retrieval and confirm HTTP 403, error "
                "code 1011001, and title Authentication parameters missing"
            ),
            (
                "Parse the official ten-result chunks fixture through the "
                "packaged adapter and verify secure Factiva links, source "
                "metadata, licensed context, and metadata-only redaction"
            ),
            (
                "Run article-url locally and confirm the current "
                "https://app.dowjones.com/factiva/article?id= deep-link format"
            ),
            (
                f"Verify OpenAI plugin snapshot {OPENAI_REVISION} Factiva "
                "manifest, app mapping, and icon hashes without redistributing "
                "those files"
            ),
            "python3 scripts/sync-plugin-icons.py --openai-source ../openai-plugins",
            "python3 scripts/build-ghast-catalog.py",
            "python3 scripts/audit-third-party-plugins.py --source ../openai-plugins",
            "python3 scripts/validate-ghast-repository.py",
            "unzip -tqq packages/dow-jones-factiva.zip",
        ],
    }


def test_adapter(script_path: Path, source: Path) -> None:
    spec = importlib.util.spec_from_file_location("factiva_adapter", script_path)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot import generated Factiva adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sample = {"data": json.loads((source / "chunks.json").read_text())}
    sample["meta"] = {
        "total_count": 10,
        "metrics_data": {
            "user_id": "0" * 32,
            "work_id": "1" * 32,
            "application_id": "ghast-audit",
        },
    }
    full = module.normalize_retrieval(sample)
    metadata = module.normalize_retrieval(sample, metadata_only=True)
    if (
        len(full["articles"]) != 10
        or "licensed_rag_context" not in full["articles"][0]
        or "licensed_rag_context" in metadata["articles"][0]
        or not full["articles"][0]["links"]["factiva"].startswith(
            "https://app.dowjones.com/factiva/article?id=drn%3A"
        )
    ):
        raise ValueError("Generated Factiva adapter sample normalization failed")

    result = subprocess.run(
        [
            "python3",
            str(script_path),
            "article-url",
            "DJDN000020251022elam001f8",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    url_result = json.loads(result.stdout)
    if "app.dowjones.com/factiva/article?id=drn%3Aarchive.newsarticle." not in (
        url_result["url"]
    ):
        raise ValueError("Generated Factiva article URL failed")


def write_plugin(source: Path) -> str:
    api_source = render_api_script()
    api_hash = sha256(api_source.encode())
    with tempfile.TemporaryDirectory(prefix=".factiva-", dir=PLUGIN_DIR) as temp:
        staging = Path(temp)
        (staging / ".ghast-plugin").mkdir()
        skill_dir = staging / "skills" / PLUGIN_ID
        (skill_dir / "scripts").mkdir(parents=True)
        manifest = {
            "name": PLUGIN_ID,
            "version": "1.0.3-ghast.1",
            "description": (
                "Search licensed Factiva news for company, industry, market, "
                "and event research through Dow Jones's official Retrieval API."
            ),
            "category": "business",
            "author": {
                "name": "Factiva, Inc. / Dow Jones",
                "url": "https://www.dowjones.com/business-intelligence/factiva/",
            },
            "homepage": (
                "https://developer.dowjones.com/documents/"
                "factiva_integration-factiva_retrieval_api"
            ),
            "repository": OFFICIAL_REPOSITORY,
            "upstreamRevision": UPSTREAM_REVISION,
            "license": "MIT",
            "portStatus": "full",
            "icon": "./assets/icon.svg",
            "skills": "./skills/",
        }
        (staging / ".ghast-plugin/plugin.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        )
        (skill_dir / "SKILL.md").write_text(render_skill())
        script_path = skill_dir / "scripts" / "factiva_api.py"
        script_path.write_text(api_source)
        script_path.chmod(0o755)
        (staging / "README.md").write_text(render_readme(api_hash))
        (staging / "LICENSE").write_text(render_license())
        test_adapter(script_path, source)

        target = PLUGIN_DIR / PLUGIN_ID
        if target.exists():
            shutil.rmtree(target)
        staging.rename(target)
    return api_hash


def update_review(api_hash: str) -> None:
    data = json.loads(REVIEWS_PATH.read_text())
    plugins = data.setdefault("plugins", {})
    plugins[PLUGIN_ID] = review(api_hash)
    REVIEWS_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        required=True,
        type=Path,
        help="Checkout of dowjones/factiva-retrievalapi-demo.",
    )
    parser.add_argument(
        "--openai-source",
        required=True,
        type=Path,
        help="Pinned checkout of github.com/openai/plugins.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source_root.resolve()
    openai_source = args.openai_source.resolve()
    verify_source(source)
    verify_documents()
    verify_api_boundary()
    verify_openai(openai_source)
    api_hash = write_plugin(source)
    update_review(api_hash)
    print(
        "imported verified Factiva Retrieval API adapter "
        f"(adapter SHA-256 {api_hash})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
