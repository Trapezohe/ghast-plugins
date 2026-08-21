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
    "daloopa": "plugins/daloopa/assets/app-icon.png",
    "github-stats": "plugins/github/assets/github-small.svg",
    "linear": "plugins/linear/assets/linear-icon.svg",
    "mixpanel-headless": "plugins/mixpanel-headless/assets/app-icon.png",
    "notion": "plugins/notion/assets/notion-small.svg",
    "sentry": "plugins/sentry/assets/sentry-small.svg",
    "supabase": "plugins/supabase/assets/logo.svg",
    "test-android-apps": "plugins/test-android-apps/assets/test-android-apps-small.svg",
    "twilio-developer-kit": "plugins/twilio-developer-kit/assets/logo.svg",
}

LOCAL_ICONS = {
    "aiera": "assets/icon.png",
    "airtable": "assets/icon.svg",
    "alation": "assets/icon.png",
    "alpaca": "assets/icon.svg",
    "asana": "assets/icon.svg",
    "atlassian-rovo": "assets/icon.svg",
    "base44": "assets/icon.png",
    "boltz-api-cli": "assets/icon.png",
    "circleci": "assets/icon.svg",
    "cloudflare": "assets/icon.svg",
    "convex": "assets/icon.png",
    "coderabbit": "assets/icon.svg",
    "deepnote": "assets/icon.svg",
    "egnyte": "assets/logo.svg",
    "expo": "assets/icon.png",
    "factset": "assets/icon.svg",
    "glean": "assets/icon.png",
    "hyperframes": "assets/icon.png",
    "heygen": "assets/icon.png",
    "marcopolo": "assets/icon.png",
    "motherduck": "assets/icon.png",
    "neon-postgres": "assets/icon.svg",
    "nvidia": "assets/icon.png",
    "picsart": "assets/icon.png",
    "remotion": "assets/icon.png",
    "render": "assets/icon.svg",
    "replayio": "assets/icon.svg",
    "shopify": "assets/icon.svg",
    "stripe": "assets/icon.png",
    "superhuman": "assets/icon.svg",
    "superpowers": "assets/icon.png",
    "temporal": "assets/icon.svg",
    "vantage": "assets/icon.svg",
    "vercel": "assets/icon.svg",
    "wix": "assets/icon.svg",
    "zoho": "assets/icon.svg",
}

CUSTOM_ICONS = {
    "actively": (
        "#151515",
        '<circle cx="23" cy="23" r="7"/>'
        '<circle cx="43" cy="19" r="5"/>'
        '<path d="M13 45c2-8 6-12 10-12s8 4 10 12"/>'
        '<path d="M35 45c1-7 4-11 8-11s7 4 8 11"/>'
        '<path d="M31 25l7-3M31 31l7 5"/>',
    ),
    "amplitude": (
        "#005AF0",
        '<path d="M12 47h40M17 42V30h8v12M28 42V21h8v21M39 42V14h8v28"/>'
        '<path d="M15 25l11-8 10 5 14-11"/>',
    ),
    "apollo": (
        "#657000",
        '<circle cx="25" cy="25" r="10"/>'
        '<circle cx="25" cy="25" r="3" fill="white" stroke="none"/>'
        '<path d="M32 32l13 13M40 45h10M45 40v10"/>',
    ),
    "attio": (
        "#C55A45",
        '<rect x="12" y="13" width="40" height="38" rx="3"/>'
        '<path d="M12 25h40M26 13v38"/>'
        '<circle cx="19" cy="19" r="2" fill="white" stroke="none"/>'
        '<path d="M32 32h13M32 40h9"/>',
    ),
    "binance": (
        "#F0B90B",
        '<path d="M14 47h38M18 41V27M29 41V18M40 41V31M51 41V12"/>'
        '<path d="M14 22l12-7 10 6 15-11"/>',
    ),
    "brand24": (
        "#2F6F73",
        '<path d="M11 15h42v27H31l-11 8v-8h-9z"/>'
        '<path d="M18 35l7-7 6 5 10-12 7 6"/>'
        '<circle cx="25" cy="28" r="2" fill="white" stroke="none"/>'
        '<circle cx="31" cy="33" r="2" fill="white" stroke="none"/>'
        '<circle cx="41" cy="21" r="2" fill="white" stroke="none"/>',
    ),
    "brex": (
        "#356C68",
        '<rect x="11" y="14" width="42" height="36" rx="3"/>'
        '<path d="M11 25h42M18 20h12M39 20h7"/>'
        '<path d="M18 33h12M18 41h8"/>'
        '<circle cx="43" cy="38" r="7"/>'
        '<path d="M43 33v10M38 38h10"/>',
    ),
    "biorender": (
        "#2F747A",
        '<path d="M13 14h27l9 9v27H13z"/>'
        '<path d="M40 14v10h9M20 30h22M20 38h13"/>'
        '<circle cx="42" cy="42" r="8"/>'
        '<path d="M42 37v10M37 42h10"/>'
        '<path d="M20 48l6-6 5 4 5-6"/>',
    ),
    "calendly": (
        "#187B62",
        '<rect x="12" y="15" width="40" height="37" rx="4"/>'
        '<path d="M12 26h40M22 10v10M42 10v10"/>'
        '<path d="M20 34h8M36 34h8M20 43h8M36 43h8"/>',
    ),
    "canva": (
        "#007C83",
        '<rect x="11" y="12" width="42" height="40" rx="4"/>'
        '<path d="M11 23h42M23 23v29"/>'
        '<circle cx="17" cy="18" r="1.5" fill="white" stroke="none"/>'
        '<path d="M30 31h15M30 39h11"/>'
        '<path d="M31 48l6-6 5 4 5-7"/>',
    ),
    "cb-insights": (
        "#245D70",
        '<path d="M12 49h40"/>'
        '<path d="M16 42V31h8v11M28 42V23h8v19M40 42V15h8v27"/>'
        '<path d="M15 24l11-7 10 5 14-11"/>'
        '<circle cx="26" cy="17" r="2" fill="white" stroke="none"/>'
        '<circle cx="36" cy="22" r="2" fill="white" stroke="none"/>'
        '<circle cx="50" cy="11" r="2" fill="white" stroke="none"/>',
    ),
    "channel99": (
        "#287067",
        '<path d="M11 49h42"/>'
        '<rect x="14" y="35" width="8" height="10"/>'
        '<rect x="28" y="27" width="8" height="18"/>'
        '<rect x="42" y="18" width="8" height="27"/>'
        '<path d="M14 27l10-7 9 3 16-12"/>'
        '<circle cx="24" cy="20" r="2" fill="white" stroke="none"/>'
        '<circle cx="33" cy="23" r="2" fill="white" stroke="none"/>'
        '<circle cx="49" cy="11" r="2" fill="white" stroke="none"/>',
    ),
    "chronograph-gp": (
        "#315D61",
        '<path d="M12 49h40"/>'
        '<path d="M17 43V30h8v13M29 43V22h8v21M41 43V14h8v29"/>'
        '<path d="M15 24l11-8 10 5 14-11"/>'
        '<circle cx="26" cy="16" r="2" fill="white" stroke="none"/>'
        '<circle cx="36" cy="21" r="2" fill="white" stroke="none"/>'
        '<circle cx="50" cy="10" r="2" fill="white" stroke="none"/>',
    ),
    "chronograph-lp": (
        "#3C6675",
        '<circle cx="32" cy="32" r="20"/>'
        '<path d="M32 12v40M12 32h40"/>'
        '<path d="M18 22c8 5 20 5 28 0M18 42c8-5 20-5 28 0"/>'
        '<path d="M32 18c6 5 9 10 9 14s-3 9-9 14"/>'
        '<path d="M32 18c-6 5-9 10-9 14s3 9 9 14"/>',
    ),
    "coupler-io": (
        "#256A72",
        '<circle cx="16" cy="18" r="5"/>'
        '<circle cx="16" cy="46" r="5"/>'
        '<circle cx="48" cy="18" r="5"/>'
        '<circle cx="48" cy="46" r="5"/>'
        '<rect x="25" y="25" width="14" height="14" rx="2"/>'
        '<path d="M20 20l7 7M44 20l-7 7M20 44l7-7M44 44l-7-7"/>',
    ),
    "coveo": (
        "#276B73",
        '<path d="M16 11h24l9 9v21H16z"/>'
        '<path d="M40 11v10h9M23 28h18M23 35h12"/>'
        '<circle cx="39" cy="43" r="8"/>'
        '<path d="M45 49l7 7"/>',
    ),
    "cogedim": (
        "#2D6F68",
        '<path d="M10 31L32 12l22 19"/>'
        '<path d="M16 28v24h32V28M26 52V38h12v14"/>'
        '<circle cx="46" cy="18" r="7"/>'
        '<path d="M51 23l7 7"/>',
    ),
    "carta-crm": (
        "#2A6F62",
        '<rect x="11" y="13" width="42" height="38" rx="3"/>'
        '<path d="M11 24h42M25 24v27"/>'
        '<circle cx="18" cy="19" r="2" fill="white" stroke="none"/>'
        '<circle cx="18" cy="33" r="4"/>'
        '<path d="M14 45c1-5 3-8 6-8s5 3 6 8M32 31h14M32 39h11M32 47h8"/>',
    ),
    "catalyst-by-zoho": (
        "#236B78",
        '<path d="M14 43h36a9 9 0 0 0 0-18 15 15 0 0 0-29-2A10 10 0 0 0 14 43z"/>'
        '<path d="M22 49h20M27 43v6M37 43v6"/>'
        '<path d="M25 31l5 5 10-11"/>',
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
    "cloudinary": (
        "#1976A3",
        '<path d="M15 44h33a10 10 0 0 0 0-20 16 16 0 0 0-30-2A11 11 0 0 0 15 44z"/>'
        '<circle cx="28" cy="32" r="4"/><path d="M36 26l9 12H27z"/>',
    ),
    "clay": (
        "#087E8B",
        '<path d="M10 13h44L39 31v14l-14 7V31z"/>'
        '<circle cx="19" cy="20" r="3"/>'
        '<circle cx="32" cy="20" r="3"/>'
        '<circle cx="45" cy="20" r="3"/>'
        '<path d="M19 24v3M32 24v3M45 24v3"/>',
    ),
    "clickup": (
        "#4D46C8",
        '<rect x="11" y="13" width="42" height="38" rx="3"/>'
        '<path d="M11 25h42M25 25v26M39 25v26"/>'
        '<path d="M16 19l3 3 6-7M30 19h5M44 19h4"/>',
    ),
    "circleback": (
        "#2E6F76",
        '<path d="M11 14h42v28H32l-11 8v-8H11z"/>'
        '<path d="M19 23h20M19 31h14"/>'
        '<circle cx="45" cy="38" r="9"/>'
        '<path d="M45 33v6l4 3"/>',
    ),
    "close": (
        "#2C6E63",
        '<rect x="11" y="13" width="42" height="38" rx="3"/>'
        '<path d="M11 25h42M25 25v26"/>'
        '<circle cx="18" cy="19" r="2" fill="white" stroke="none"/>'
        '<path d="M31 33h15M31 41h10"/>'
        '<path d="M16 34h4M16 42h4"/>',
    ),
    "common-room": (
        "#2A6D64",
        '<circle cx="21" cy="22" r="6"/>'
        '<circle cx="43" cy="19" r="5"/>'
        '<path d="M12 45c2-9 5-14 9-14s8 5 10 14"/>'
        '<path d="M35 43c1-7 4-11 8-11s7 4 9 11"/>'
        '<path d="M27 23l11-3M28 30l9 6"/>'
        '<path d="M13 52h38"/>',
    ),
    "conductor": (
        "#236B78",
        '<path d="M11 49h42"/>'
        '<path d="M14 41l10-11 8 6 9-14 9 7"/>'
        '<circle cx="24" cy="30" r="2" fill="white" stroke="none"/>'
        '<circle cx="32" cy="36" r="2" fill="white" stroke="none"/>'
        '<circle cx="41" cy="22" r="2" fill="white" stroke="none"/>'
        '<circle cx="50" cy="29" r="2" fill="white" stroke="none"/>'
        '<path d="M14 17h19M14 23h12M43 14l8 8M51 14l-8 8"/>',
    ),
    "cube": (
        "#315F78",
        '<path d="M13 20l19-9 19 9-19 10z"/>'
        '<path d="M13 20v23l19 10 19-10V20M32 30v23"/>'
        '<path d="M19 39l6-5 5 4 7-9 8 6"/>',
    ),
    "demandbase": (
        "#28656F",
        '<circle cx="21" cy="22" r="6"/>'
        '<path d="M11 45c2-9 6-14 10-14s8 5 10 14"/>'
        '<circle cx="44" cy="19" r="5"/>'
        '<path d="M36 39c1-7 4-11 8-11s7 4 9 11"/>'
        '<path d="M27 23l11-3M29 31l8 5"/>'
        '<path d="M12 52h40"/>',
    ),
    "datadog": (
        "#27676A",
        '<rect x="11" y="13" width="42" height="38" rx="3"/>'
        '<path d="M17 38h7l5-13 7 19 5-11h7"/>'
        '<path d="M17 20h13M36 20h12"/>',
    ),
    "digitalocean": (
        "#176B87",
        '<path d="M15 42h34a9 9 0 0 0 0-18 15 15 0 0 0-29-2A10 10 0 0 0 15 42z"/>'
        '<rect x="18" y="38" width="28" height="14" rx="2"/>'
        '<path d="M23 44h18M23 48h12"/>'
        '<circle cx="40" cy="48" r="1.5" fill="white" stroke="none"/>',
    ),
    "docusign": (
        "#B58A00",
        '<path d="M17 11h25l8 8v34H17z"/>'
        '<path d="M42 11v10h8M24 30h18M24 38h11"/>'
        '<path d="M23 47c5-5 9-6 12-2 3 3 7 2 12-3"/>'
        '<path d="M24 52h24"/>',
    ),
    "domotz-preview": (
        "#245F69",
        '<circle cx="32" cy="32" r="6"/>'
        '<circle cx="16" cy="17" r="5"/>'
        '<circle cx="48" cy="17" r="5"/>'
        '<circle cx="16" cy="48" r="5"/>'
        '<circle cx="48" cy="48" r="5"/>'
        '<path d="M20 20l8 8M44 20l-8 8M20 45l8-9M44 45l-8-9"/>',
    ),
    "dow-jones-factiva": (
        "#2B6268",
        '<path d="M14 12h27l9 9v31H14z"/>'
        '<path d="M41 12v10h9M21 29h21M21 37h14M21 45h9"/>'
        '<circle cx="44" cy="43" r="8"/>'
        '<path d="M50 49l6 6"/>',
    ),
    "dovetail": (
        "#26735B",
        '<rect x="10" y="12" width="44" height="40" rx="4"/>'
        '<path d="M10 23h44M22 12v40M35 23v29"/>'
        '<path d="M15 18h2M27 18h2M41 18h8"/>'
        '<path d="M27 31h4M27 38h4M40 31h9M40 38h7M40 45h5"/>',
    ),
    "fal": (
        "#C3274A",
        '<rect x="10" y="12" width="44" height="40" rx="4"/>'
        '<path d="M10 23h44"/>'
        '<path d="m16 45 9-10 7 7 6-6 10 9"/>'
        '<circle cx="43" cy="31" r="3"/>'
        '<path d="M18 18h16M42 17l7 4-7 4z"/>',
    ),
    "fiscal-ai": (
        "#25706A",
        '<path d="M14 11h27l9 9v33H14z"/>'
        '<path d="M41 11v10h9M21 27h22"/>'
        '<path d="M22 46V37M30 46V32M38 46V35M46 46V27"/>'
        '<path d="M20 50h28"/>',
    ),
    "fyxer": (
        "#2F6F73",
        '<path d="M10 15h44v34H10z"/>'
        '<path d="m11 17 21 17 21-17"/>'
        '<path d="M18 43h20M18 37h14"/>'
        '<path d="M43 35l8 5-8 5z"/>',
    ),
    "omni-analytics": (
        "#3B6D62",
        '<path d="M11 49h42"/>'
        '<rect x="14" y="34" width="8" height="11"/>'
        '<rect x="28" y="25" width="8" height="20"/>'
        '<rect x="42" y="15" width="8" height="30"/>'
        '<path d="M14 27l12-8 9 3 15-12"/>',
    ),
    "lovable": (
        "#D84A2B",
        '<rect x="10" y="12" width="44" height="40" rx="4"/>'
        '<path d="M10 22h44M18 17h.01M24 17h.01M30 17h.01"/>'
        '<path d="m25 32-6 5 6 5M39 32l6 5-6 5M35 28l-6 18"/>',
    ),
    "fireflies": (
        "#B34F55",
        '<rect x="12" y="14" width="40" height="37" rx="4"/>'
        '<path d="M12 25h40M22 10v9M42 10v9"/>'
        '<path d="M19 38h5l3-8 5 15 5-11 3 6h5"/>',
    ),
    "granola": (
        "#5C6257",
        '<path d="M16 12h32v40H16z"/>'
        '<path d="M23 21h18M23 29h18M23 37h12"/>'
        '<path d="M36 45l6-6 5 5-6 6-7 2z"/>',
    ),
    "govtribe": (
        "#236A5A",
        '<path d="M12 24h40L32 11z"/>'
        '<path d="M17 25v21M26 25v21M38 25v21M47 25v21"/>'
        '<path d="M11 47h42M8 53h48"/>'
        '<circle cx="45" cy="43" r="8" fill="#236A5A"/>'
        '<path d="M51 49l5 5"/>',
    ),
    "happenstance": (
        "#315F78",
        '<circle cx="18" cy="20" r="6"/>'
        '<circle cx="44" cy="17" r="5"/>'
        '<circle cx="29" cy="43" r="7"/>'
        '<path d="M23 23l15-4M21 25l5 12M41 22l-8 15"/>'
        '<circle cx="46" cy="43" r="8" fill="#315F78"/>'
        '<path d="M52 49l5 5"/>',
    ),
    "hg-insights": (
        "#176B68",
        '<path d="M11 49h42"/>'
        '<rect x="14" y="35" width="7" height="10"/>'
        '<rect x="27" y="28" width="7" height="17"/>'
        '<rect x="40" y="19" width="7" height="26"/>'
        '<path d="M14 28l13-8 9 4 14-12"/>'
        '<circle cx="50" cy="12" r="3" fill="white" stroke="none"/>',
    ),
    "hebbia": (
        "#4657F5",
        '<rect x="11" y="12" width="39" height="40" rx="3"/>'
        '<path d="M11 23h39M24 23v29M37 23v22"/>'
        '<path d="M16 18h12M31 18h13M16 30h3M29 30h3M42 30h3"/>'
        '<path d="M16 38h3M29 38h3"/>'
        '<circle cx="45" cy="45" r="8" fill="#4657F5"/>'
        '<path d="M51 51l5 5"/>',
    ),
    "jam": (
        "#5F4A8B",
        '<rect x="10" y="13" width="44" height="34" rx="4"/>'
        '<path d="M10 23h44M17 18h2M24 18h2M31 18h2"/>'
        '<path d="M20 52l7-5h18"/>'
        '<path d="M20 31h14M20 38h9M39 30l8 5-8 5z"/>',
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
    "hubspot": (
        "#F05A3A",
        '<circle cx="20" cy="20" r="6"/><circle cx="45" cy="16" r="5"/>'
        '<circle cx="45" cy="45" r="7"/>'
        '<path d="M25 22l14-4M24 25l15 15M45 21v17"/>',
    ),
    "hostinger": (
        "#5C4DB1",
        '<path d="M13 47h38M17 47V25l15-10 15 10v22"/>'
        '<path d="M24 47V34h16v13"/>'
        '<path d="M32 10v12M26 16h12"/>'
        '<path d="M21 28h5M38 28h5"/>',
    ),
    "highlevel": (
        "#176B68",
        '<rect x="11" y="13" width="42" height="38" rx="3"/>'
        '<path d="M11 24h42M24 24v27"/>'
        '<circle cx="18" cy="18" r="2" fill="white" stroke="none"/>'
        '<path d="M30 32h16M30 40h11"/>'
        '<path d="M15 33h5M15 40h5"/>',
    ),
    "intercom": (
        "#2375A8",
        '<path d="M12 15h40v29H31l-11 8v-8h-8z"/>'
        '<path d="M21 25v10M28 22v13M35 22v13M42 25v10"/>'
        '<path d="M20 38c8 4 16 4 24 0"/>',
    ),
    "hugging-face": (
        "#F0B429",
        '<circle cx="20" cy="24" r="6"/><circle cx="44" cy="24" r="6"/>'
        '<circle cx="32" cy="43" r="6"/>'
        '<path d="M25 27l4 10M39 27l-4 10M26 24h12"/>',
    ),
    "mermaid-mindmap": (
        "#0F766E",
        '<circle cx="18" cy="32" r="6"/><circle cx="46" cy="18" r="6"/>'
        '<circle cx="46" cy="46" r="6"/>'
        '<path d="M24 30l16-9M24 34l16 9"/>',
    ),
    "magicpath": (
        "#305D3A",
        '<rect x="10" y="12" width="44" height="40" rx="4"/>'
        '<path d="M10 22h44M18 17h2M26 17h2"/>'
        '<path d="M25 31l-6 6 6 6M39 31l6 6-6 6M35 27l-6 20"/>',
    ),
    "mem": (
        "#39736B",
        '<path d="M15 13h27l8 8v31H15z"/>'
        '<path d="M42 13v9h8M22 29h20M22 37h13"/>'
        '<circle cx="42" cy="43" r="7"/>'
        '<path d="M47 48l5 5"/>',
    ),
    "midpage": (
        "#315B54",
        '<path d="M11 24h42M16 24v23M26 24v23M38 24v23M48 24v23"/>'
        '<path d="M9 49h46M13 20l19-10 19 10z"/>'
        '<circle cx="43" cy="39" r="7"/>'
        '<path d="M48 44l6 6"/>',
    ),
    "mixpanel": (
        "#6F4BD8",
        '<path d="M12 48h40M16 42V29h8v13M28 42V20h8v22M40 42V13h8v29"/>'
        '<path d="M15 23l11-7 10 5 14-10"/>',
    ),
    "monday-com": (
        "#4B57DB",
        '<rect x="13" y="14" width="38" height="36" rx="5"/>'
        '<path d="M20 24h24M20 33h15M20 42h20"/>'
        '<path d="M42 31l4 4 7-8"/>',
    ),
    "mt-newswires": (
        "#245C63",
        '<path d="M12 15h34v36H12zM46 23h6v28H46"/>'
        '<path d="M19 23h20M19 31h8M19 43h20"/>'
        '<path d="M30 34l4-5 4 8 5-6"/>',
    ),
    "quicknode": (
        "#2E6FCE",
        '<circle cx="20" cy="20" r="6"/><circle cx="44" cy="20" r="6"/>'
        '<circle cx="20" cy="44" r="6"/><circle cx="44" cy="44" r="6"/>'
        '<path d="M26 20h12M20 26v12M44 26v12M26 44h12"/>',
    ),
    "quartr": (
        "#173F5F",
        '<path d="M12 48h40M17 44V27h8v17M29 44V18h8v26M41 44V33h8v11"/>'
        '<path d="M15 20l11-7 10 5 14-9"/>',
    ),
    "razorpay": (
        "#236B78",
        '<rect x="11" y="15" width="42" height="34" rx="3"/>'
        '<path d="M11 25h42M18 20h12M38 20h8"/>'
        '<path d="M18 34h15M18 42h10"/>'
        '<circle cx="44" cy="39" r="7"/>'
        '<path d="M41 36h6M41 39h6M44 36v7"/>',
    ),
    "read-ai": (
        "#197A7A",
        '<rect x="15" y="12" width="34" height="40" rx="5"/>'
        '<path d="M23 23h18M23 31h12M23 39h16"/>'
        '<path d="M42 36v8M38 40h8"/>',
    ),
    "readwise": (
        "#2F6F61",
        '<path d="M12 17c7-3 14-2 20 3v31c-6-5-13-6-20-3z"/>'
        '<path d="M52 17c-7-3-14-2-20 3v31c6-5 13-6 20-3z"/>'
        '<path d="M20 28h7M20 36h7M37 28h7M37 36h7"/>',
    ),
    "replit": (
        "#C45134",
        '<rect x="11" y="13" width="42" height="38" rx="4"/>'
        '<path d="M11 24h42M19 18h1M27 18h1M35 18h1"/>'
        '<path d="M22 34l6 6-6 6M34 46h9"/>'
        '<path d="M45 29v8M41 33h8"/>',
    ),
    "netlify": (
        "#0E7C7B",
        '<path d="M12 43h40M18 43V27l14-10 14 10v16"/>'
        '<path d="M27 43V32h10v11"/>',
    ),
    "otter-ai": (
        "#2F6B73",
        '<rect x="12" y="13" width="40" height="38" rx="4"/>'
        '<path d="M12 24h40M20 18h1M28 18h1M36 18h1"/>'
        '<path d="M19 38h5l3-8 5 15 5-11 3 6h5"/>'
        '<path d="M20 48h24"/>',
    ),
    "outreach": (
        "#286A63",
        '<rect x="11" y="13" width="42" height="38" rx="4"/>'
        '<path d="M11 24h42M21 24v27M34 24v27"/>'
        '<circle cx="17" cy="18" r="2" fill="white" stroke="none"/>'
        '<path d="M16 35h10M29 35h10M42 35h6"/>'
        '<path d="M44 31l5 4-5 4"/>',
    ),
    "posthog": (
        "#D5A019",
        '<path d="M12 48h40M17 43V31h8v12M29 43V22h8v21M41 43V14h8v29"/>'
        '<path d="M15 25l11-8 10 5 14-11"/>'
        '<circle cx="50" cy="11" r="2" fill="white" stroke="none"/>',
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
    "semrush": (
        "#E85D3F",
        '<path d="M12 48V18M12 48h40"/>'
        '<path d="M18 40l9-10 8 5 13-17"/>'
        '<circle cx="18" cy="40" r="2" fill="white"/>'
        '<circle cx="27" cy="30" r="2" fill="white"/>'
        '<circle cx="35" cy="35" r="2" fill="white"/>'
        '<circle cx="48" cy="18" r="2" fill="white"/>',
    ),
    "scite": (
        "#28705D",
        '<path d="M13 14h27l8 8v17"/>'
        '<path d="M40 14v10h8M20 27h18M20 35h11M20 43h8"/>'
        '<circle cx="41" cy="42" r="9"/>'
        '<path d="M48 49l6 6"/>'
        '<path d="M37 39l-2 3 2 3M45 39l2 3-2 3"/>',
    ),
    "signnow": (
        "#176B5B",
        '<path d="M17 11h25l8 8v34H17z"/>'
        '<path d="M42 11v10h8M24 31h18M24 39h10"/>'
        '<path d="M26 50l16-16 6 6-16 16-8 2z"/>'
        '<path d="M39 37l6 6"/>',
    ),
    "similarweb": (
        "#F07028",
        '<circle cx="32" cy="32" r="20"/>'
        '<path d="M12 32h40M32 12c7 7 10 14 10 20s-3 13-10 20"/>'
        '<path d="M32 12c-7 7-10 14-10 20s3 13 10 20"/>'
        '<path d="M18 39l8-8 7 4 13-14"/>',
    ),
    "skywatch": (
        "#155E75",
        '<circle cx="32" cy="32" r="8"/>'
        '<path d="M11 40c8 8 23 9 34 2s14-20 8-29"/>'
        '<path d="M53 13l-1 10-9-4"/>'
        '<path d="M17 17l7 7M40 40l7 7"/>'
        '<rect x="12" y="11" width="9" height="9" rx="1"/>'
        '<rect x="43" y="44" width="9" height="9" rx="1"/>',
    ),
    "streak": (
        "#D9583B",
        '<path d="M14 17h36M14 32h36M14 47h36"/>'
        '<circle cx="22" cy="17" r="5" fill="#D9583B"/>'
        '<circle cx="39" cy="32" r="5" fill="#D9583B"/>'
        '<circle cx="29" cy="47" r="5" fill="#D9583B"/>',
    ),
    "thoughtspot": (
        "#245B62",
        '<path d="M12 48h40M28 43V34M39 43V26M50 43V17"/>'
        '<circle cx="18" cy="20" r="8"/>'
        '<path d="M24 26l6 6"/>',
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
    "statsig": (
        "#B14AED",
        '<path d="M14 48V18M14 18h24l-5 8 5 8H14"/>'
        '<path d="M24 43l7-7 6 5 12-15"/>'
        '<path d="M42 26h7v7"/>',
    ),
    "uptime-check": (
        "#2E7D32",
        '<path d="M8 34h12l5-13 9 26 6-13h16"/>',
    ),
    "windsor-ai": (
        "#276B73",
        '<circle cx="17" cy="18" r="5"/>'
        '<circle cx="47" cy="18" r="5"/>'
        '<circle cx="17" cy="46" r="5"/>'
        '<circle cx="47" cy="46" r="5"/>'
        '<rect x="25" y="25" width="14" height="14" rx="2"/>'
        '<path d="M21 20l6 7M43 20l-6 7M21 44l6-7M43 44l-6-7"/>'
        '<path d="M12 32h13M39 32h13"/>',
    ),
    "website-fetcher": (
        "#5B5BD6",
        '<circle cx="32" cy="32" r="21"/>'
        '<path d="M11 32h42M32 11c7 7 10 14 10 21s-3 14-10 21M32 11c-7 7-10 14-10 21s3 14 10 21"/>',
    ),
    "yepcode": (
        "#087E8B",
        '<path d="M22 20l-10 12 10 12M42 20l10 12-10 12"/>'
        '<path d="M36 15l-8 34"/>'
        '<circle cx="32" cy="32" r="3" fill="white" stroke="none"/>',
    ),
    "zoom": (
        "#2D6CDF",
        '<rect x="12" y="20" width="28" height="25" rx="5"/>'
        '<path d="M40 28l12-7v23l-12-7z"/>',
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
        if path.is_dir() and (path / "plugin.json").is_file()
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

        manifest_path = plugin_dir / "plugin.json"
        manifest = json.loads(manifest_path.read_text())
        ghast = manifest.setdefault("extensions", {}).setdefault(
            "ai.trapezohe.ghast", {}
        )
        ghast["icon"] = f"./{icon_path.relative_to(plugin_dir)}"
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
