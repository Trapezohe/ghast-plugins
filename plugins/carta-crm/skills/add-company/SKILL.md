---
name: add-company
description: Adds one or more company records to the Carta CRM via the Carta CRM MCP Server. Use this skill when the user says things like "add a company", "create company record", "add company to CRM", "add company to Carta CRM", or "/add-company". Collects company information conversationally, then creates it via the MCP server.
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

Help the user create one or more company records in the Carta CRM using the
`create_company` MCP tool. Collect company details conversationally, validate
required fields, then call the tool.

## Step 1 — Discover available custom fields (optional but recommended)

Call the custom fields tool to see what fields the tenant has configured:

```
get_company_custom_fields({})
```

Use the returned field IDs and labels as hints when collecting company data.
If the call fails, proceed without it — custom fields are optional.

## Step 2 — Collect company information

Ask the user for:
- **Name** (required) — the company name (e.g. "Stripe", "Acme Corp")
- **Image URL** (optional) — company logo URL
- **Custom fields** (optional) — any fields returned in Step 1 (e.g. website, industry, location, about, tags)

If the user has already provided details in their message, extract them directly
without re-asking.

## Step 3 — Create the company

Call:

```
create_company({
    name: "<company name>",
    image: "<logo url>",
    fields: {
      "<field_id>": "<value>"
    }
  })
```

Omit `image` and `fields` if not provided.

## Step 4 — Report result

On success, respond with:
> "Company **{name}** created successfully (ID: `{id}`)."

On error, show the error message and suggest:
- Check that `name` is provided and non-empty
- Verify custom field IDs match the keys returned by `get_company_custom_fields`

## Adding multiple companies

If the user wants to add multiple companies at once, repeat Steps 2–4 for each one.
After all are done, summarize:
> "Created N companies: [list of names with IDs]"
