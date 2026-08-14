---
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
python3 "$FACTIVA_API" search \
  "What is the latest outlook for Nvidia earnings?" \
  --days-range LastMonth \
  --filter Language=en \
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
python3 "$FACTIVA_API" article-url \
  "drn:archive.newsarticle.DJDN000020251022elam001f8"
```

Read account token consumption:

```bash
python3 "$FACTIVA_API" token-usage \
  --from-date 2026-08-01 \
  --to-date 2026-08-14 \
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
