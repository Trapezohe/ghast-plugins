#!/usr/bin/env python3
"""Install one catalog icon for every Ghast plugin."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


EXPECTED_OPENAI_REVISION = "11c74d6ba24d3a6d48f54a194cd00ef3beea18f9"
PLUGIN_DIR = Path("plugins")

OPENAI_ICONS = {
    "boltz-api-cli": "plugins/boltz-api-cli/assets/app-icon.png",
    "cloudflare": "plugins/cloudflare/assets/cloudflare-small.svg",
    "expo": "plugins/expo/assets/expo.png",
    "github-stats": "plugins/github/assets/github-small.svg",
    "hyperframes": "plugins/hyperframes/assets/icon.png",
    "linear": "plugins/linear/assets/linear-icon.svg",
    "mixpanel-headless": "plugins/mixpanel-headless/assets/app-icon.png",
    "notion": "plugins/notion/assets/notion-small.svg",
    "nvidia": "plugins/nvidia/assets/nvidia.png",
    "remotion": "plugins/remotion/assets/icon.png",
    "render": "plugins/render/assets/logo.svg",
    "sentry": "plugins/sentry/assets/sentry-small.svg",
    "superpowers": "plugins/superpowers/assets/superpowers-small.svg",
    "test-android-apps": "plugins/test-android-apps/assets/test-android-apps-small.svg",
    "twilio-developer-kit": "plugins/twilio-developer-kit/assets/logo.svg",
}

LOCAL_ICONS = {
    "temporal": "assets/temporal-logo.svg",
}

CUSTOM_ICONS = {
    "binance": (
        "#F0B90B",
        '<path d="M14 47h38M18 41V27M29 41V18M40 41V31M51 41V12"/>'
        '<path d="M14 22l12-7 10 6 15-11"/>',
    ),
    "bilibili-search": (
        "#FB7299",
        '<rect x="13" y="18" width="38" height="29" rx="6"/>'
        '<path d="M22 18l-5-6M42 18l5-6"/>'
        '<path d="M28 29l10 6-10 6z" fill="white" stroke="none"/>',
    ),
    "current-datetime": (
        "#087E8B",
        '<circle cx="32" cy="32" r="19"/>'
        '<path d="M32 20v13l9 6"/>',
    ),
    "defillama": (
        "#176B87",
        '<path d="M15 45V31h8v14M28 45V22h8v23M41 45V15h8v30"/>'
        '<path d="M13 49h38"/>',
    ),
    "hacker-news": (
        "#F0652F",
        '<path d="M19 17l13 16 13-16M32 33v15"/>',
    ),
    "mermaid-mindmap": (
        "#0F766E",
        '<circle cx="18" cy="32" r="6"/><circle cx="46" cy="18" r="6"/>'
        '<circle cx="46" cy="46" r="6"/>'
        '<path d="M24 30l16-9M24 34l16 9"/>',
    ),
    "realtime-weather": (
        "#1D82B6",
        '<circle cx="25" cy="24" r="9"/>'
        '<path d="M25 10V6M25 42v-4M11 24H7M43 24h-4M15 14l-3-3M38 37l-3-3"/>'
        '<path d="M24 46h24a9 9 0 0 0-2-18 13 13 0 0 0-24 6 7 7 0 0 0 2 12z" fill="#1D82B6"/>',
    ),
    "seo-meta": (
        "#2563EB",
        '<rect x="14" y="12" width="27" height="38" rx="4"/>'
        '<path d="M21 22h13M21 30h10"/>'
        '<circle cx="42" cy="40" r="8" fill="#2563EB"/>'
        '<path d="M48 46l5 5"/>',
    ),
    "steam-search": (
        "#1B4965",
        '<circle cx="22" cy="40" r="7"/><circle cx="44" cy="22" r="8"/>'
        '<path d="M28 37l10-10M15 37l-7-3M22 40l17 7 7-6"/>',
    ),
    "stock-quote": (
        "#16825D",
        '<path d="M13 49V15M13 49h39"/>'
        '<path d="M18 42l10-11 8 6 14-18"/>'
        '<path d="M42 19h8v8"/>',
    ),
    "uptime-check": (
        "#2E7D32",
        '<path d="M8 34h12l5-13 9 26 6-13h16"/>',
    ),
    "website-fetcher": (
        "#5B5BD6",
        '<circle cx="32" cy="32" r="21"/>'
        '<path d="M11 32h42M32 11c7 7 10 14 10 21s-3 14-10 21M32 11c-7 7-10 14-10 21s3 14 10 21"/>',
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--openai-source",
        type=Path,
        required=True,
        help="Checkout of github.com/openai/plugins at the pinned revision.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    openai_source = args.openai_source.resolve()
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=openai_source,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if revision != EXPECTED_OPENAI_REVISION:
        raise ValueError(
            f"{openai_source}: expected revision {EXPECTED_OPENAI_REVISION}, "
            f"found {revision}"
        )

    plugin_dirs = {
        path.name: path
        for path in PLUGIN_DIR.iterdir()
        if path.is_dir() and (path / ".ghast-plugin/plugin.json").is_file()
    }
    classified = set(OPENAI_ICONS) | set(LOCAL_ICONS) | set(CUSTOM_ICONS)
    if set(plugin_dirs) != classified:
        raise ValueError(
            "Icon classification is out of date: "
            f"missing={sorted(set(plugin_dirs) - classified)}, "
            f"stale={sorted(classified - set(plugin_dirs))}"
        )

    for name, plugin_dir in sorted(plugin_dirs.items()):
        assets_dir = plugin_dir / "assets"
        assets_dir.mkdir(exist_ok=True)
        if name in OPENAI_ICONS:
            source_path = openai_source / OPENAI_ICONS[name]
            if not source_path.is_file():
                raise ValueError(f"{source_path}: icon source is missing")
            icon_path = assets_dir / f"icon{source_path.suffix.lower()}"
            shutil.copy2(source_path, icon_path)
        elif name in LOCAL_ICONS:
            icon_path = plugin_dir / LOCAL_ICONS[name]
            if not icon_path.is_file():
                raise ValueError(f"{icon_path}: local icon is missing")
        else:
            background, body = CUSTOM_ICONS[name]
            icon_path = assets_dir / "icon.svg"
            icon_path.write_text(render_svg(background, body))

        manifest_path = plugin_dir / ".ghast-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["icon"] = f"./{icon_path.relative_to(plugin_dir)}"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        )

    print(f"installed icons for {len(plugin_dirs)} plugins")
    return 0


def render_svg(background: str, body: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
        f'  <rect width="64" height="64" rx="12" fill="{background}"/>\n'
        f'  <g fill="none" stroke="white" stroke-width="4" '
        f'stroke-linecap="round" stroke-linejoin="round">{body}</g>\n'
        "</svg>\n"
    )


if __name__ == "__main__":
    raise SystemExit(main())
