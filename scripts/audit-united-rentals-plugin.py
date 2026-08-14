#!/usr/bin/env python3
"""Verify United Rentals evidence and enforce its private-agent blocker."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import urllib.request
from pathlib import Path


EXPECTED_OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
LAUNCH_URL = (
    "https://investors.unitedrentals.com/press-releases/"
    "press-releases-details/2026/"
    "United-Rentals-Introduces-AI-Powered-Equipment-Agent/default.aspx"
)
LAUNCH_CORE_SHA256 = (
    "169f00214fe8edfe239f7870b30d077012ba1290e17d74e712fa2bd2c23fe703"
)
CHATGPT_URL = (
    "https://investors.unitedrentals.com/press-releases/"
    "press-releases-details/2026/"
    "United-Rentals-Expands-Digital-Customer-Experience-with-Equipment-"
    "Agent-Launch-in-ChatGPT/default.aspx"
)
CHATGPT_CORE_SHA256 = (
    "2892cb1938cc3cb4293c1a985177a6d0bffd4bd0417f786c3b332059cc4db2b1"
)
OPENAI_HASHES = {
    ".app.json": (
        "b2ae8c37e5a252d8d8e096a4a9f2d0efef996c1b387da7d7d188cfd7f29de343"
    ),
    ".codex-plugin/plugin.json": (
        "75c897e1a6079055727e57a5f74a56ac9e438c911ee3e6987254778c8a9b3309"
    ),
    "assets/logo.png": (
        "b3ac1787cc0f87d8e3636623020e12245196c1c9fcd5224be16901658cb7b77d"
    ),
}
OPENAI_INVENTORY_SHA256 = (
    "89d78bbc9b7f482eef9d9f278822b15bbd4f8a00eefc2156ab51961b5d10ad55"
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


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "text/html",
            "User-Agent": "ghast-united-rentals-audit/1.0",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


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


def section(value: str, start_marker: str, end_marker: str) -> str:
    start = value.find(start_marker)
    if start < 0:
        raise ValueError(f"United Rentals evidence is missing {start_marker!r}")
    end = value.find(end_marker, start + len(start_marker))
    if end < 0:
        raise ValueError(f"United Rentals evidence is missing {end_marker!r}")
    return value[start:end].strip()


def verify_official_product_evidence() -> None:
    launch = section(
        normalize_html(fetch(LAUNCH_URL)),
        "United Rentals Introduces AI-Powered Equipment Agent March 12, 2026",
        "About United Rentals",
    )
    if sha256(launch.encode()) != LAUNCH_CORE_SHA256:
        raise ValueError("United Rentals Equipment Agent launch evidence changed")
    for marker in (
        "AI-powered equipment recommendation solution",
        "personalized recommendations based on a customer’s project requirements",
        "comparing equipment types",
        "capacity, reach, terrain limitations and required accessories",
        "connects users to detailed product pages on unitedrentals.com",
        "fleet knowledge and practical jobsite expertise",
        "available today and can be accessed at unitedrentals.com",
    ):
        if marker not in launch:
            raise ValueError(
                f"United Rentals launch evidence is missing {marker!r}"
            )

    chatgpt = section(
        normalize_html(fetch(CHATGPT_URL)),
        (
            "United Rentals Expands Digital Customer Experience with Equipment "
            "Agent Launch in ChatGPT May 19, 2026"
        ),
        "About United Rentals",
    )
    if sha256(chatgpt.encode()) != CHATGPT_CORE_SHA256:
        raise ValueError("United Rentals ChatGPT launch evidence changed")
    for marker in (
        "Equipment Agent to be accessible in ChatGPT",
        "first equipment rental application available in the ChatGPT store",
        "guide customers through key project requirements",
        "fleet knowledge, application expertise and operational insight",
        "specification and rental-related queries",
    ):
        if marker not in chatgpt:
            raise ValueError(
                f"United Rentals ChatGPT evidence is missing {marker!r}"
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

    plugin = source / "plugins/united-rentals"
    actual_files = {
        path.relative_to(plugin).as_posix()
        for path in plugin.rglob("*")
        if path.is_file()
    }
    if actual_files != set(OPENAI_HASHES):
        raise ValueError("United Rentals Codex file inventory changed")
    for relative_path, expected_hash in OPENAI_HASHES.items():
        if sha256((plugin / relative_path).read_bytes()) != expected_hash:
            raise ValueError(
                f"United Rentals Codex evidence changed: {relative_path}"
            )
    if inventory_hash(plugin) != OPENAI_INVENTORY_SHA256:
        raise ValueError("United Rentals Codex inventory hash changed")

    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    app = json.loads((plugin / ".app.json").read_text())
    interface = manifest.get("interface", {})
    if (
        manifest.get("name") != "united-rentals"
        or manifest.get("version") != "1.0.3"
        or manifest.get("author", {}).get("name") != "United Rentals"
        or interface.get("developerName") != "United Rentals"
        or interface.get("defaultPrompt")
        != ["Find the relevant United Rentals inventory or availability"]
        or app.get("apps", {}).get("united-rentals", {}).get("id")
        != "asdk_app_69ba9e565bd48191b6ed6c024cda5f85"
    ):
        raise ValueError("United Rentals Codex identity changed")
    description = re.sub(r"\s+", " ", interface.get("longDescription", "")).strip()
    for marker in (
        "Share your project details",
        "tailored equipment recommendations",
        "specifications",
        "confident selection",
    ):
        if marker not in description:
            raise ValueError(
                f"United Rentals Codex capability evidence is missing {marker!r}"
            )


def main() -> int:
    args = parse_args()
    verify_official_product_evidence()
    verify_openai_snapshot(args.openai_source.resolve())
    if (
        Path("plugins/united-rentals").exists()
        or Path("packages/united-rentals.zip").exists()
    ):
        raise ValueError(
            "United Rentals must remain unpublished until the developer supplies "
            "a supported portable endpoint or documented recommendation API, "
            "independent authentication and onboarding, stable schemas, and "
            "sufficient adapter and artwork rights"
        )
    print("verified United Rentals private-agent and public-API mismatch blockers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
