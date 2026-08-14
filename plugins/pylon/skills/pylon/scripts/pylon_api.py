#!/usr/bin/env python3
"""Minimal client for Pylon's official REST API note endpoint."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from unittest import mock


BASE_URL = "https://api.usepylon.com"
CONFIRMATION = "ADD_INTERNAL_NOTE"
ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,200}$")


def api_token() -> str:
    value = os.environ.get("PYLON_API_TOKEN", "")
    if not value or any(character in value for character in "\0\r\n"):
        raise ValueError("Set PYLON_API_TOKEN in the Ghast host environment.")
    return value


def validate_id(label: str, value: str | None) -> str | None:
    if value is None:
        return None
    if not ID_PATTERN.fullmatch(value):
        raise ValueError(f"{label} contains unsupported characters.")
    return value


def text_to_html(value: str) -> str:
    escaped = html.escape(value.strip())
    paragraphs = [
        "<p>" + paragraph.replace("\n", "<br>") + "</p>"
        for paragraph in re.split(r"\n\s*\n", escaped)
        if paragraph
    ]
    return "".join(paragraphs)


def validate_attachment_url(value: str) -> str:
    parsed = urllib.parse.urlparse(value)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValueError(
            "Attachment URLs must use HTTPS and must not embed credentials."
        )
    return value


def build_note_payload(args: argparse.Namespace, body: str) -> dict:
    if not body.strip():
        raise ValueError("Internal note body is empty.")
    if args.thread_id and args.message_id:
        raise ValueError("Use at most one of --thread-id and --message-id.")
    if args.thread_name and (args.thread_id or args.message_id):
        raise ValueError("--thread-name is only valid for a new default thread.")
    payload = {
        "body_html": body.strip()
        if args.body_format == "html"
        else text_to_html(body)
    }
    for key in ("thread_id", "message_id", "thread_name", "user_id"):
        value = getattr(args, key)
        if value:
            payload[key] = value
    if args.attachment_url:
        payload["attachment_urls"] = [
            validate_attachment_url(value) for value in args.attachment_url
        ]
    return payload


def api_request(method: str, path: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(
        BASE_URL + path,
        data=data,
        method=method,
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer " + api_token(),
            **({"Content-Type": "application/json"} if data is not None else {}),
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        request_id = error.headers.get("X-Pylon-Request-ID", "")
        try:
            response = json.loads(error.read())
            request_id = response.get("request_id") or request_id
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
        suffix = f", request_id={request_id}" if request_id else ""
        raise RuntimeError(
            f"Pylon API request failed (HTTP {error.code}{suffix})."
        ) from None
    except urllib.error.URLError:
        raise RuntimeError("Pylon API request failed due to a network error.") from None


def command_config_check(_: argparse.Namespace) -> int:
    api_token()
    print(json.dumps({"configured": True, "base_url": BASE_URL}))
    return 0


def command_me(_: argparse.Namespace) -> int:
    print(json.dumps(api_request("GET", "/me"), indent=2))
    return 0


def command_add_note(args: argparse.Namespace) -> int:
    if args.confirm != CONFIRMATION:
        raise ValueError(
            f"Pass --confirm {CONFIRMATION} after explicit user approval."
        )
    issue_id = validate_id("issue ID", args.issue_id)
    args.thread_id = validate_id("thread ID", args.thread_id)
    args.message_id = validate_id("message ID", args.message_id)
    args.user_id = validate_id("user ID", args.user_id)
    if args.thread_name and len(args.thread_name) > 200:
        raise ValueError("Thread name must be 200 characters or fewer.")
    body = sys.stdin.read()
    payload = build_note_payload(args, body)
    result = api_request(
        "POST",
        f"/issues/{urllib.parse.quote(issue_id, safe='')}/note",
        payload,
    )
    data = result.get("data") if isinstance(result, dict) else None
    output = {
        "ok": True,
        "issue_id": data.get("issue_id") if isinstance(data, dict) else issue_id,
        "message_id": data.get("id") if isinstance(data, dict) else None,
        "request_id": result.get("request_id")
        if isinstance(result, dict)
        else None,
    }
    print(json.dumps(output, indent=2))
    return 0


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self) -> bytes:
        return json.dumps(self.payload).encode()


def self_test() -> int:
    secret = "pylon-self-test-token"
    old_token = os.environ.get("PYLON_API_TOKEN")
    os.environ["PYLON_API_TOKEN"] = secret
    args = argparse.Namespace(
        thread_id=None,
        message_id=None,
        thread_name="Investigation",
        user_id=None,
        attachment_url=[],
        body_format="text",
    )
    payload = build_note_payload(args, "Refund issued.\n\nFollow up tomorrow.")
    if payload != {
        "body_html": "<p>Refund issued.</p><p>Follow up tomorrow.</p>",
        "thread_name": "Investigation",
    }:
        raise AssertionError("Pylon note payload normalization failed")
    args.thread_id = "thread_1"
    args.message_id = "message_1"
    try:
        build_note_payload(args, "test")
    except ValueError:
        pass
    else:
        raise AssertionError("Pylon note target exclusivity failed")

    seen = {}

    def fake_open(request, timeout):
        seen["url"] = request.full_url
        seen["authorization"] = request.get_header("Authorization")
        return FakeResponse({"data": {"id": "message_2"}})

    with mock.patch("urllib.request.urlopen", fake_open):
        result = api_request("GET", "/me")
    transcript = json.dumps({"result": result, "url": seen.get("url")})
    if (
        result.get("data", {}).get("id") != "message_2"
        or seen.get("authorization") != "Bearer " + secret
        or secret in transcript
    ):
        raise AssertionError("Pylon API transport self-test failed")
    if old_token is None:
        del os.environ["PYLON_API_TOKEN"]
    else:
        os.environ["PYLON_API_TOKEN"] = old_token
    print("Pylon REST adapter self-test passed")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--self-test", action="store_true")
    commands = root.add_subparsers(dest="command")
    commands.add_parser("config-check")
    commands.add_parser("me")
    note = commands.add_parser("add-note")
    note.add_argument("--issue-id", required=True)
    note.add_argument("--thread-id")
    note.add_argument("--message-id")
    note.add_argument("--thread-name")
    note.add_argument("--user-id")
    note.add_argument("--attachment-url", action="append", default=[])
    note.add_argument("--body-format", choices=("text", "html"), default="text")
    note.add_argument("--confirm")
    return root


def main() -> int:
    args = parser().parse_args()
    if args.self_test:
        return self_test()
    try:
        if args.command == "config-check":
            return command_config_check(args)
        if args.command == "me":
            return command_me(args)
        if args.command == "add-note":
            return command_add_note(args)
        raise ValueError("Choose config-check, me, or add-note.")
    except (ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
