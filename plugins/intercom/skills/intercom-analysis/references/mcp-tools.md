# Intercom Hosted MCP Reference

This plugin connects directly to Intercom's official hosted MCP service:

- `intercom-us`: `https://mcp.intercom.com/mcp`
- `intercom-eu`: `https://mcp.eu.intercom.com/mcp`

Choose the server matching the workspace region. Australia is not supported
by the hosted MCP service. Authentication uses the host's browser OAuth flow.

The current official service documents 13 tools. The live MCP schemas are the
authority for exact parameters.

| Tool | Purpose |
|------|---------|
| `search` | Universal query-DSL search for conversations or contacts |
| `fetch` | Fetch a conversation, contact, or company by its prefixed ID |
| `search_conversations` | Search conversations with conversation-specific filters |
| `get_conversation` | Retrieve one conversation and its complete parts |
| `search_contacts` | Search contacts by IDs, identity fields, attributes, or email domain |
| `get_contact` | Retrieve one complete contact profile |
| `list_companies` | List or filter companies |
| `get_company` | Retrieve one complete company |
| `list_articles` | List Help Center articles |
| `search_articles` | Search Help Center articles |
| `get_article` | Retrieve one article and its HTML body |
| `create_article` | Create a Help Center article |
| `update_article` | Update an existing Help Center article |

## Search workflow

1. Start with `search`, `search_conversations`, `search_contacts`, or
   `list_companies` using the narrowest available identifier and bounded page
   size.
2. Preserve all filters when following a `starting_after` cursor. Stop when
   the requested scope is satisfied rather than enumerating the workspace.
3. Use `fetch`, `get_conversation`, `get_contact`, or `get_company` only for
   the records needed to answer the question.
4. Cite returned IDs and distinguish facts returned by Intercom from
   interpretation or recommendations.

The universal `search` query supports `object_type:conversations` or
`object_type:contacts`, field filters, free text, `limit`, and
`starting_after`. Direct search tools provide richer object-specific filters.
Do not invent a query field when the live tool schema does not expose it.

## Article writes

`create_article` and `update_article` are state-changing tools. Before either
call, read the relevant parent or existing article, show the exact title,
author, description, body, parent, and `draft` or `published` state, and wait
for explicit confirmation. Never publish, move, or overwrite an article from
an analysis-only request.

## Tickets

The hosted MCP service does not expose ticket tools. Use the bundled
`intercom-ticket-analysis` skill, which relies on Intercom's separately
installed official CLI and official Tickets REST API for read-only search and
retrieval.
