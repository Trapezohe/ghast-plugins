---
name: seo-meta
description: Use this skill when the user asks to audit, review, or extract SEO meta tags from a webpage — `<title>`, meta description, canonical, robots, OpenGraph, Twitter Card, H1s. Fetches the raw HTML and pulls out the head-section signals search engines and social scrapers consume.
version: 1.0.0
allowed-tools: [WebFetch, Bash]
---

# SEO Meta Analyzer

When the user asks to audit how a page presents itself to search engines or
social scrapers — "is the title length right", "what does this page look like
when shared on Twitter", "are there missing OG tags" — use this skill.

## Fetch the raw HTML

Use `curl` via `Bash` for the rawest possible HTML (`WebFetch` may pre-process
the page and strip the head). Limit to a reasonable byte cap so a giant SPA
doesn't blow up the context:

```bash
curl -sS -A 'Mozilla/5.0' --max-filesize 1000000 'https://example.com' | head -c 200000
```

## Tags to extract

Walk the HTML head and pull:

| Tag | Selector | What to report |
| --- | --- | --- |
| Title | `<title>` | The text, plus length in chars |
| Description | `<meta name="description" content="...">` | The text, plus length |
| Canonical | `<link rel="canonical" href="...">` | The href |
| Robots | `<meta name="robots" content="...">` | Verbatim |
| Viewport | `<meta name="viewport" content="...">` | Verbatim |
| Open Graph | `<meta property="og:*" content="...">` | Map of all `og:` keys |
| Twitter Card | `<meta name="twitter:*" content="...">` | Map of all `twitter:` keys |
| H1s | `<h1>` ... `</h1>` | First three, text only |
| `<html lang="...">` | root lang attr | The value |

## Diagnostic checklist

After extraction, call out common problems:

- Missing `<title>` → "Search engines have nothing to show"
- Title length > 70 chars → "Truncated in Google snippets"
- Missing `<meta description>` → "Google synthesizes one, often poorly"
- Description length > 160 chars → "Truncated"
- Missing `og:image` → "Links shared without a preview image"
- No `<h1>` or > 1 `<h1>` → "Heading hierarchy issue"
- Missing canonical when the page has query params → "Risk of duplicate-URL indexing"

## Caveats

- JS-rendered SPAs (React/Vue with no SSR) will have a sparse `<head>` —
  warn the user the model is reading the server-shipped HTML, not the
  hydrated DOM.
- Content-Security-Policy nonces or trackers can clutter the head; focus
  the audit on the tags above.
