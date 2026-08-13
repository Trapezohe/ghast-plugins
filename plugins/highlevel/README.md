# HighLevel

Inspect contacts, opportunities, pipelines, appointments, calendars, conversations, messages, and related CRM activity through HighLevel's official hosted MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/GoHighLevel/highlevel-api-docs` at `0af86a4cbd48c66a4071c7e509d1079f9f10ed17`.

The CC0-1.0 license is copied from HighLevel's pinned official API documentation repository. Ghast connects directly to HighLevel's official hosted MCP endpoint and adds only adapter metadata, a safety workflow, and a generic CRM icon; no HighLevel server code, private connector mapping, logo, or marketplace artwork is packaged.

## Ghast compatibility

- The Codex private app mapping is replaced by HighLevel's official original /mcp/ endpoint, which supports any HTTP-based MCP client through browser OAuth or an optional user-managed Private Integration Token.
- The original endpoint covers contacts, conversations, opportunities, calendars, payments, social planning, blogs, and email. Its contacts, opportunities, appointments, and conversation surface matches the Codex snapshot's declared CRM overview, pipeline analysis, lead qualification, and follow-up preparation workflows.
- HighLevel's wider per-client /mcp/{client}/v2 catalog is currently published for Anthropic clients. Ghast uses the official client-neutral endpoint instead of impersonating another client or claiming access to unavailable tools.
- Every connection targets one authorized HighLevel sub-account. Actual tools are filtered by the user's OAuth or PIT scopes, account role, product entitlements, and location permissions.
- A generic CRM icon is used because the official CC0 documentation repository does not grant trademark rights and this package does not copy HighLevel brand artwork.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
