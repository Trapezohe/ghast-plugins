---
name: add-investor
description: >
  Adds one or more investor records to the Carta CRM via the Carta CRM MCP Server.
  Use this skill when the user says things like "add an investor", "/add-investor",
  "add investor to Carta CRM", "create investor record", "add this VC fund to the CRM", or
  "save investor data". Collects investor information conversationally, then creates
  it via the MCP server.
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

Help the user create one or more investor records in the Carta CRM using the
`create_investor` MCP tool. Collect investor details conversationally, validate
required fields, then call the tool.

## Step 1 — Discover available custom fields (optional but recommended)

Call the custom fields tool to see what fields the tenant has configured:

```
get_investor_custom_fields({})
```

Use the returned field IDs and labels as hints when collecting investor data.
If the call fails, proceed without it — custom fields are optional.

## Step 2 — Collect investor information

Ask the user for:
- **Name** (required) — the investor firm name (e.g. "Sequoia Capital", "a16z")
- **Custom fields** (optional) — any fields returned in Step 1 (e.g. website, location, industry, about, tags)

If the user has already provided details in their message, extract them directly
without re-asking.

## Step 3 — Create the investor

Call:

```
create_investor({
    name: "<investor name>",
    fields: {
      "<field_id>": "<value>"
    }
  })
```

Omit `fields` entirely if no custom field data was provided.

## Step 4 — Report result

On success, respond with:
> "Investor **{name}** created successfully (ID: `{id}`)."

On error, show the error message and suggest:
- Check that `name` is provided and non-empty
- Verify custom field IDs match the keys returned by `get_investor_custom_fields`

## Adding multiple investors

If the user wants to add multiple investors at once, repeat Steps 2–4 for each one.
After all are done, summarize:
> "Created N investors: [list of names with IDs]"
