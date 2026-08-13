# quartr

Research public companies using first-party earnings calls, transcripts,
filings, reports, slides, events, summaries, and financial statements through
Quartr's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, and catalog metadata. It does not copy or redistribute Quartr's
hosted MCP implementation, proprietary data, or private Codex connector.

The adapter is pinned to Quartr's official MCP documentation with SHA-256
`1d651d2a9ac88fa63f904c244c87083c7cd6e17140751ed7a5d2abd48a257b6c`. The official OAuth protected-resource metadata is
pinned at SHA-256 `a379a77612f2fa51d06c105bd11b0c34c83fdeb4b40667cb2792a1093598b7d8`, and the authorization
server metadata is pinned at SHA-256 `20a1464a05ed203ecad5e4aa5bce8fb9e85ea56ea4489294c1343e8fbe90ac3b`.

## Ghast compatibility

- Ghast connects directly to `https://mcp.quartr.com/mcp` using Streamable HTTP and
  Quartr OAuth 2.0 with PKCE.
- The 43 documented tools cover companies, peers, events, conferences,
  transcripts, reports, slides, filings, full-text search, financial
  statements, summaries, watchlists, keywords, folders, workspaces, saved
  filters, and GICS classifications.
- This fully covers the Codex app's earnings-call, competitive-intelligence,
  KPI-tracking, and narrative-assessment workflows and adds Quartr account
  organization features.
- The included skill requires source attribution and confirmation for
  state-changing watchlist, keyword, folder, filter, and workspace actions.
- A generic financial-research icon is used because no licensed catalog icon
  is included in a public official source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Quartr accounts, subscriptions, hosted service behavior, data, permissions,
trademarks, and terms remain controlled by Quartr.
