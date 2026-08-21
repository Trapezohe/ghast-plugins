---
name: search-contacts
description: Searches for and retrieves contact (people) records from the Carta CRM. Use this skill when the user says things like "find a contact", "search contacts", "look up a person", "show me contact details for [name]", "get contact by ID", "list contacts", "find people at [company]", "search people", or "/search-contacts". Returns contact details including ID, name, email, title, company, and tags. The contact ID returned can be used with the update-contact skill.
metadata:
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

Search for contacts in the Carta CRM. If the user provided an ID, fetch the single
record directly. Otherwise search by name/keyword and return results in a readable
summary. Always surface the contact ID so the user can reference it for updates.

## Step 1 — Determine search mode

- **By ID** — user provided a contact ID → call `fetch_contact_by_id`
- **By name / keyword** — user provided a name, email, or keyword → call `search_contacts`

If it's unclear, default to search and ask the user for a search term.

## Step 2 — Execute the search

**By ID:**
```
fetch_contact_by_id({ id: "<contact id>" })
```

**By name / keyword:**
```
search_contacts({
    query: "<search term>",
    limit: 20
  })
```

If the user mentions a specific list or folder by name, call `get_contact_lists` first
to resolve the name to a list ID, then pass `list_id` to narrow the search:

```
get_contact_lists({})
```

Increase `limit` if the user asks to see more results. Use `offset` to paginate.

## Step 3 — Present results

For each contact returned, display all non-empty fields in a readable summary,
including name, title, company, email, phone, and tags.
Always show the ID prominently — the user will need it to run `/update-contact`.

`fetch_contact_by_id` also returns related deals and notes — surface those if the
user is looking for context on a specific person.

If no contacts are found:
> "No contacts found matching your search. Try a different name, email, or keyword."

If multiple results are returned, list them all and note the total count.
