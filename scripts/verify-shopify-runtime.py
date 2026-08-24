#!/usr/bin/env python3
"""Verify Shopify's official documentation search and GraphQL validator."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


SKILL_DIR = Path("plugins/shopify/skills/shopify-admin")
SEARCH_SCRIPT = SKILL_DIR / "scripts/search_docs.mjs"
VALIDATE_SCRIPT = SKILL_DIR / "scripts/validate.mjs"
QUERY = "query ProductsForAudit { products(first: 5) { nodes { id title } } }"


def run_node(script: Path, *args: str) -> str:
    environment = os.environ.copy()
    environment["OPT_OUT_INSTRUMENTATION"] = "true"
    return subprocess.run(
        ["node", str(script), *args],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    ).stdout


def main() -> int:
    search = json.loads(
        run_node(
            SEARCH_SCRIPT,
            "products GraphQL query title",
            "--model",
            "codex",
            "--client-name",
            "ghast-audit",
            "--client-version",
            "1.0",
        )
    )
    if not isinstance(search, list) or not search:
        raise ValueError("Shopify documentation search returned no results")
    if any(
        not isinstance(result, dict)
        or not str(result.get("url", "")).startswith("https://shopify.dev/")
        for result in search
    ):
        raise ValueError("Shopify search returned a non-official result")

    validation = json.loads(
        run_node(
            VALIDATE_SCRIPT,
            "--code",
            QUERY,
            "--artifact-id",
            "ghast-shopify-runtime-audit",
            "--revision",
            "1",
            "--model",
            "codex",
            "--client-name",
            "ghast-audit",
            "--client-version",
            "1.0",
            "--json",
        )
    )
    if validation.get("success") is not True:
        raise ValueError(f"Shopify GraphQL validation failed: {validation!r}")
    responses = validation.get("responses")
    if not isinstance(responses, list) or not responses or any(
        response.get("result") != "success" for response in responses
    ):
        raise ValueError(f"unexpected Shopify validation response: {validation!r}")

    print(
        "verified Shopify official documentation search and GraphQL schema "
        f"validation ({validation.get('resolvedVersion')})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
