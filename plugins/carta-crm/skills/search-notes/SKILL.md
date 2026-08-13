---
name: search-notes
description: >
  Searches for and retrieves note records from the Carta CRM.
  Use this skill when the user says things like "find a note", "search notes",
  "look up a note", "show me notes about [topic]", "list notes",
  "find notes mentioning [keyword]", or "/search-notes".
  Returns note details including ID, title, and text content.
version: 1.0.0
model: haiku
---


## Ghast MCP routing

This port connects directly to Carta's hosted MCP server. Use the direct tool
name shown in each example and pass the displayed object as that tool's
arguments. Do not look for Claude's `crm_call_tool` dispatcher or add a
`crm:` prefix. The authenticated live tool schema is authoritative if an
argument differs from this pinned workflow text.

Ghast does not run Carta's Claude hooks and does not inject
`_instrumentation_v2`. Never add undeclared telemetry fields to a tool call.


## Overview

Search for notes in the Carta CRM by keyword using `search_notes`.
Return results in a readable summary.

## Step 1 — Collect the search term

If the user provided a keyword or topic, use it directly.
If no search term was given, ask for one.

## Step 2 — Execute the search

```
search_notes({
    query: "<search term>",
    limit: 20
  })
```

Increase `limit` if the user asks to see more results. Use `offset` to paginate
when `remainingCount > 0`.

## Step 3 — Present results

For each note returned, display:
- Title
- Text content (truncated to ~200 chars if long)
- Creation date and owner if available

If no notes are found:
> "No notes found matching your search. Try a different keyword."

Note the total count and offer to paginate if there are more results.
