#!/usr/bin/env python3
"""Read-only search client for Shutterstock's official public API."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


API_ROOT = "https://api.shutterstock.com"
ENDPOINTS = {
    "images": ("GET", "/v2/images/search"),
    "videos": ("GET", "/v2/videos/search"),
    "audio": ("GET", "/v2/audio/search"),
    "sfx": ("GET", "/v2/sfx/search"),
    "bulk-images": ("POST", "/v2/bulk_search/images"),
}
def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def per_page(value: str) -> int:
    number = positive_int(value)
    if number > 20:
        raise argparse.ArgumentTypeError("must be 20 or less")
    return number


def add_common(parser: argparse.ArgumentParser, *, safe: bool) -> None:
    parser.add_argument("--query", required=True)
    parser.add_argument("--page", type=positive_int, default=1)
    parser.add_argument("--per-page", type=per_page, default=10)
    parser.add_argument("--language")
    parser.add_argument("--sort")
    parser.add_argument("--view", choices=("minimal", "full"), default="full")
    if safe:
        parser.add_argument(
            "--safe", choices=("true", "false"), default="true"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Search Shutterstock's official API for watermarked media previews. "
            "This client cannot license or download assets."
        )
    )
    subparsers = parser.add_subparsers(dest="media_type", required=True)

    images = subparsers.add_parser("images", help="Search stock images")
    add_common(images, safe=True)
    images.add_argument("--orientation", choices=("horizontal", "vertical"))
    images.add_argument(
        "--image-type",
        action="append",
        choices=("photo", "illustration", "vector"),
    )
    images.add_argument("--color")
    images.add_argument("--aspect-ratio", type=float)
    images.add_argument("--people-number", type=int)
    images.add_argument("--people-gender")
    images.add_argument("--people-ethnicity", action="append")
    images.add_argument("--region")

    videos = subparsers.add_parser("videos", help="Search stock videos")
    add_common(videos, safe=True)
    videos.add_argument("--orientation", choices=("horizontal", "vertical"))
    videos.add_argument("--duration-from", type=positive_int)
    videos.add_argument("--duration-to", type=positive_int)
    videos.add_argument("--resolution")

    audio = subparsers.add_parser("audio", help="Search music tracks")
    add_common(audio, safe=False)
    audio.add_argument("--mood", action="append")
    audio.add_argument("--genre", action="append")
    audio.add_argument("--instrument", action="append")
    audio.add_argument("--bpm-from", type=positive_int)
    audio.add_argument("--bpm-to", type=positive_int)
    audio.add_argument("--duration-from", type=positive_int)
    audio.add_argument("--duration-to", type=positive_int)
    audio.add_argument("--instrumental", choices=("true", "false"))
    audio.add_argument("--vocal-description")
    audio.add_argument("--library")

    sfx = subparsers.add_parser("sfx", help="Search sound effects")
    add_common(sfx, safe=True)
    sfx.add_argument("--duration-from", type=positive_int)
    sfx.add_argument("--duration-to", type=positive_int)

    bulk = subparsers.add_parser(
        "bulk-images", help="Run two to five grouped image searches"
    )
    bulk.add_argument("--query", action="append", required=True)
    bulk.add_argument("--per-page", type=per_page, default=10)
    bulk.add_argument("--language")
    bulk.add_argument("--sort")
    bulk.add_argument("--view", choices=("minimal", "full"), default="full")
    bulk.add_argument("--safe", choices=("true", "false"), default="true")
    bulk.add_argument("--orientation", choices=("horizontal", "vertical"))
    bulk.add_argument(
        "--image-type",
        action="append",
        choices=("photo", "illustration", "vector"),
    )
    bulk.add_argument("--color")
    bulk.add_argument("--aspect-ratio", type=float)
    bulk.add_argument("--region")
    return parser


def authentication_headers() -> dict[str, str]:
    token = os.environ.get("SHUTTERSTOCK_API_TOKEN")
    key = os.environ.get("SHUTTERSTOCK_KEY")
    secret = os.environ.get("SHUTTERSTOCK_SECRET")
    if token:
        return {"Authorization": f"Bearer {token}"}
    if key and secret:
        encoded = base64.b64encode(f"{key}:{secret}".encode()).decode()
        return {"Authorization": f"Basic {encoded}"}
    raise ValueError(
        "Set SHUTTERSTOCK_API_TOKEN or both SHUTTERSTOCK_KEY and "
        "SHUTTERSTOCK_SECRET. Create a Shutterstock API application and use "
        "only credentials issued to you."
    )


def parameters(namespace: argparse.Namespace) -> dict[str, object]:
    values = vars(namespace).copy()
    values.pop("media_type", None)
    return {
        key: value
        for key, value in values.items()
        if value is not None and value != []
    }


def execute(namespace: argparse.Namespace) -> object:
    media_type = namespace.media_type
    method, path = ENDPOINTS[media_type]
    params = parameters(namespace)
    headers = {
        "Accept": "application/json",
        "User-Agent": "Ghast-Shutterstock-Search/1.0",
        "x-shutterstock-application": "Ghast-Search",
        **authentication_headers(),
    }
    data = None
    url = API_ROOT + path

    if media_type == "bulk-images":
        queries = params.pop("query")
        if not isinstance(queries, list) or not 2 <= len(queries) <= 5:
            raise ValueError("bulk-images requires between two and five queries")
        body = []
        for query in queries:
            item = {"query": query, **params}
            body.append(item)
        data = json.dumps(body, separators=(",", ":")).encode()
        headers["Content-Type"] = "application/json"
    else:
        url += "?" + urllib.parse.urlencode(params, doseq=True)

    request = urllib.request.Request(
        url, data=data, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        body = error.read()
        status = error.code
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        payload = {"message": body.decode("utf-8", "replace")}
    if status >= 400:
        raise RuntimeError(
            json.dumps(
                {"status": status, "error": payload},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    return payload


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = execute(args)
    except (ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
