# brand24

Explore current Brand24 project summaries, important events, discussions,
influencers, and mention sources through Brand24's official read-only hosted
MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, catalog metadata, and a generic social-listening
icon. It does not copy or redistribute Brand24's hosted MCP implementation,
private Codex connector, service source code, customer project data, OAuth
credentials, branded artwork, or marketplace icon.

Brand24's official Help Center article is pinned at article ID
`13011375`, update timestamp
`2026-02-27T10:00:11Z`, and normalized Markdown SHA-256
`22c8be2b5c9f893c64c182fa8b271c0dbb98cd0e0bdd4f3827ac44a98cd440b1`. Volatile signed image URLs are removed
before hashing. The article documents account and project summaries,
important events, discussions and topics, influencer insights, mention-source
details, current project data, OAuth, and the official endpoint
`https://mcp.brand24.com/v1/mcp`.

The official protected-resource metadata is pinned at canonical JSON SHA-256
`8bfc708c6d6643b6f72d4bf1bb6fa797f01821226184217bf047f9f470760c93`, and the authorization-server metadata at
`826db8f30f1955186f2f8f6d1f1f0e009d3eeb64d5ae8245fafdcbda206747c4`. Codex capability evidence is pinned to
OpenAI's plugin snapshot revision `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying
the private app ID or marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://mcp.brand24.com/v1/mcp` using Streamable HTTP and
  Brand24 browser OAuth.
- The service declares the single `projects:read` scope, Dynamic Client
  Registration, authorization-code and refresh-token grants, public and
  confidential client authentication methods, and PKCE S256.
- On August 13, 2026, an unauthenticated MCP initialize request returned HTTP
  401 with Brand24's protected-resource challenge. One disposable loopback
  client registered with HTTP 200, and its authorization request was accepted
  and redirected into Brand24's authorization route. The response provided
  no registration management URI or access token, so the audit client could
  not be deleted through the standard registration-management protocol. No
  client secret was retained or committed.
- The official hosted service covers the Codex app's brand-mention,
  sentiment, media-coverage, reputation, trend, discussion-source, emerging
  issue, audience-perception, and campaign-impact workflows at Brand24's
  published product surface.
- Brand24 does not publish the hosted server source, a complete tool
  inventory, or tool schemas. Authenticated tools/list and project-data
  operations were not run because no user Brand24 account or project data was
  used during the audit.
- Brand24 states that its MCP retrieves current active-project data on demand,
  rather than a cached snapshot. Account subscriptions, project configuration,
  data retention, source coverage, permissions, and service limits remain
  authoritative.
- The included skill preserves source and date provenance, treats sentiment
  and influence metrics as estimates, protects personal and campaign data,
  separates assistant drafts from external actions, and prevents read-only
  analysis from being described as publishing or outreach.
- A generic social-listening icon is used because no licensed Brand24 catalog
  artwork is included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Brand24 accounts, subscriptions, hosted service behavior, project data,
permissions, analytics, trademarks, privacy policy, and terms remain
controlled by Brand24.
