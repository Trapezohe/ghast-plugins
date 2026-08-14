---
name: factset
description: >-
  Research public and private companies, securities, estimates, prices,
  fundamentals, ownership, events, transcripts, StreetAccount news, supply
  chains, funds, and licensed broker research through FactSet's official MCP
  and APIs.
---

# FactSet

Use the official hosted MCP for the normal FactSet data surface. Use the
bundled `scripts/factset_api.py` only for Investment Research metadata and
Security Explanation workflows that are not named in the public MCP catalog.

## Route the request

| Intent | Official surface |
|---|---|
| Consensus estimates, surprises, ratings, guidance | `FactSet_EstimatesConsensus` |
| Prices, returns, volume, dividends, corporate actions | `FactSet_GlobalPrices` |
| Financial statements, ratios, margins, valuation | `FactSet_Fundamentals` and `FactSet_Metrics` |
| Debt and liquidity | `FactSet_DebtCapitalStructure` |
| Ownership, insiders, institutional or fund holdings | `FactSet_Ownership` |
| Events, transcripts, StreetAccount news, filings | `FactSet_CalendarEvents` and `FactSet_UnstructuredContent` |
| Entity, people, M&A, PE/VC, private companies | Matching `FactSet_*` MCP tool |
| Funds, ETFs, screens, supply chain, GeoRev, RBICS | Matching `FactSet_*` MCP tool |
| Broker research headlines and action metadata | `research-search` adapter command |
| Broker-research-backed performance explanation | `explanation-create`, then status/result |

The live authenticated MCP catalog and schemas are authoritative. Inspect them
before promising a field or dataset.

## Resolve the adapter

Resolve `SKILL_DIR` from this loaded skill, then:

```bash
FACTSET_API="$SKILL_DIR/scripts/factset_api.py"
```

Use one of these local credential modes:

- `FACTSET_ACCESS_TOKEN` for an existing bearer token.
- `FACTSET_USERNAME_SERIAL` plus `FACTSET_API_KEY` for Basic API-key auth.

Never request credentials in chat, print them, write them to files, or place
them in visible command arguments. FactSet's official SDK can obtain OAuth
client-credentials tokens; this adapter intentionally consumes an existing
token instead of managing client secrets.

```bash
python3 "$FACTSET_API" auth-check
```

## Core financial workflows

For estimates and price performance, resolve the exact security first. State:

- Identifier and exchange.
- Currency and unit scaling.
- Fiscal period, calendar date, and estimate snapshot date.
- Reported, adjusted, restated, or consensus basis.
- Price-return window and whether dividends are included.

For peer comparisons, use the same metrics, currency basis, fiscal alignment,
and valuation date across every company. Do not mix trailing, current-year,
and next-year multiples without labels. Preserve unavailable values rather
than silently changing metrics.

For "latest" requests, use explicit absolute dates and report the newest
available observation. Do not treat a stale observation as current.

## Broker research headlines

Search metadata without downloading reports:

```bash
python3 "$FACTSET_API" research-search \
  --id AAPL-US \
  --start-date 2026-08-01 \
  --end-date 2026-08-14 \
  --limit 25
```

Useful filters include `--search-text`, `--contributor-id`, `--analyst-id`,
`--rating-action`, `--target-action`, and `--weighting-action`. Use
`research-meta research-contributors` and `research-meta research-analysts`
to resolve entitlement-aware IDs. `--filters-json` exposes the remaining
official search fields without accepting arbitrary endpoint or URL changes.

Summarize sentiment only from explicit headline language, rating actions,
target actions, weighting actions, and an entitled Security Explanation.
Separate positive, negative, neutral, and mixed evidence by contributor and
date. A document count is not sentiment.

Returned links point to licensed documents. Do not automatically open,
download, quote, cache, index, persist, or redistribute them. A user request
and the recipient's FactSet Research Connect entitlement are required before
opening a report.

## Security Explanation

Create an asynchronous explanation:

```bash
python3 "$FACTSET_API" explanation-create AAPL-US \
  --start-date 2026-08-01 \
  --end-date 2026-08-14 \
  --broker-style summary \
  --enable-links
```

Then poll once at a time and retrieve only after completion:

```bash
python3 "$FACTSET_API" explanation-status <request-id>
python3 "$FACTSET_API" explanation-result <request-id>
```

Do not loop rapidly. Respect `Retry-After` and service rate limits. Broker
summaries require the appropriate FactSet entitlement. Broker IDs produce
separate summaries and must not be merged into a false consensus.

## Safety and quality

- All included surfaces are read-only, but API calls can consume licensed
  capacity and asynchronous jobs. Confirm broad searches before execution.
- Do not present FactSet data, estimates, research, or generated explanations
  as investment advice or guaranteed outcomes.
- Distinguish reported facts, analyst opinion, consensus estimates, company
  guidance, FactSet-generated explanation, and assistant inference.
- Preserve source, contributor, analyst, document date, observation date,
  units, currency, and entitlement boundaries.
- Do not expose personal data from people, ownership, insider, or private
  company datasets beyond the user's authorized purpose.
- Do not retry 401, 403, 429, or asynchronous creation automatically. Report
  the request ID when FactSet provides one.
- Never infer that StreetAccount news is broker research. Use the Investment
  Research API for broker reports and Security Explanation for entitled broker
  summaries.
