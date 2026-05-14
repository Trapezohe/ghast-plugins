#!/usr/bin/env python3
"""
Re-merge the latest Anthropic plugin marketplace into ours.

Ghast's marketplace at `.claude-plugin/marketplace.json` is a superset of
Anthropic's curated directory. To pick up new plugins they add, run this
script — it fetches their live marketplace, rewrites internal-relative
sources to `git-subdir` pointing at their repo (pinned to the current
HEAD sha), and merges them with our own starter plugins.

Idempotent: re-running just updates the pinned sha and adds any new
plugins; our 12 originals stay in front, name collisions skip the
Anthropic copy (keeping ours).

Usage:
    python3 scripts/merge-anthropic-plugins.py
"""

from __future__ import annotations

import copy
import json
import sys
import urllib.request
from pathlib import Path

ANTHROPIC_MARKETPLACE_URL = (
    "https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/"
    ".claude-plugin/marketplace.json"
)
ANTHROPIC_REPO_URL = "https://github.com/anthropics/claude-plugins-official.git"
ANTHROPIC_BRANCH_API = (
    "https://api.github.com/repos/anthropics/claude-plugins-official/branches/main"
)

# `example-plugin` is Anthropic's reference template, not a real plugin —
# they don't list it in their own marketplace.json so this is a no-op,
# but kept as a safety net if they ever do.
SKIP_NAMES = {"example-plugin"}


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.load(resp)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    our_path = repo_root / ".claude-plugin" / "marketplace.json"

    print(f"[merge] fetching Anthropic marketplace…")
    anthropic = fetch_json(ANTHROPIC_MARKETPLACE_URL)
    print(f"[merge] fetching Anthropic HEAD sha…")
    head_sha = fetch_json(ANTHROPIC_BRANCH_API)["commit"]["sha"]
    print(f"[merge] anthropic HEAD = {head_sha[:10]}…")

    ours = json.loads(our_path.read_text())
    # Keep only our own originals — drop any prior Anthropic-derived
    # entries so this re-merge always reflects upstream's current state.
    ours_only = [
        p
        for p in ours["plugins"]
        if not _was_anthropic_imported(p)
    ]
    print(f"[merge] keeping {len(ours_only)} Ghast-original entries")

    ghast_names = {p["name"] for p in ours_only}
    merged = list(ours_only)
    added = 0
    skipped = 0
    for plugin in anthropic.get("plugins", []):
        name = plugin.get("name")
        if not name or name in SKIP_NAMES:
            skipped += 1
            continue
        if name in ghast_names:
            # Keep our copy when names collide.
            skipped += 1
            continue
        entry = copy.deepcopy(plugin)
        src = entry.get("source")
        if isinstance(src, str) and src.startswith("./"):
            # Internal-to-Anthropic — rewrite as git-subdir pointing at their repo.
            entry["source"] = {
                "source": "git-subdir",
                "url": ANTHROPIC_REPO_URL,
                "path": src.lstrip("./"),
                "ref": "main",
                "sha": head_sha,
            }
        # else: source already pointed at an external URL; copy verbatim.
        merged.append(entry)
        added += 1

    ours["plugins"] = merged
    our_path.write_text(
        json.dumps(ours, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"[merge] wrote {len(merged)} total plugins to {our_path.relative_to(repo_root)}")
    print(f"[merge]   from Anthropic: {added}")
    print(f"[merge]   skipped       : {skipped}")
    return 0


def _was_anthropic_imported(plugin: dict) -> bool:
    """Identify entries we previously merged from Anthropic so the next
    re-merge can drop and recompute them rather than accumulating duplicates.

    Heuristic: an entry is Anthropic-imported iff its `source` is an
    object (any kind) — every entry we publish ourselves uses the
    plain-string `./plugins/foo` form for `source`. Anthropic's entries
    use object forms (`git-subdir`, `url`, `github`, etc.). If they
    introduce a new source kind in the future, this still catches it
    without needing a schema update on our end.
    """
    return isinstance(plugin.get("source"), dict)


if __name__ == "__main__":
    sys.exit(main())
