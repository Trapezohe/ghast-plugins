# pylon

Search, research, create, update, assign, and resolve Pylon support issues and
manage related accounts through Pylon's official hosted MCP. A minimal
standard-library adapter adds the internal-note operation from Pylon's
official REST API.

## Official interfaces

Pylon publishes `https://mcp.usepylon.com` as a stateless Streamable HTTP server with OAuth.
Its detailed reference currently lists 11 tools: issue search, issue fetch,
message history, issue create/update, account search/get/update, contact get,
user get, and authenticated-user get.

The product page says MCP agents can add internal notes, but the detailed tool
reference and Pylon's own documentation query say the MCP has no note or reply
tool. The official REST API separately publishes
`POST /issues/{id}/note`, including thread selection and a 10-request-per-
minute limit. Ghast combines the official MCP with only that missing official
API operation instead of claiming a nonexistent MCP tool.

## Capability comparison

- Codex: check the authenticated agent's queue, research customer issues and
  escalations, resolve an issue, and add an internal note.
- Ghast: use all 11 documented hosted MCP tools for queue, customer, issue,
  message, account, contact, user, create, update, assignment, and resolution
  workflows; use the bundled adapter for the official internal-note endpoint.
- OAuth remains user-scoped. REST notes use a user-managed API token and are
  attributed to that token in Pylon.

## Licensing

The bundled adapter SHA-256 is `4d788c5898469d32dfaff5cbf142a88d64ca4a5ce60afb9e729d8098e380a503`. The MIT license covers only
the Ghast-authored endpoint declaration, adapter, workflow, metadata,
documentation, and generic support-ticket icon. It does not license or
redistribute Pylon's hosted MCP implementation, API service, customer data,
private Codex connector, credentials, documentation, logos, or trademarks.
