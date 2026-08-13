# brex

Analyze Brex expenses, cards, limits, banking, bills, accounting, travel, and
organization data, or safely update supported expense details through Brex's
official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, catalog metadata, and a generic expense-control
icon. It does not copy or redistribute Brex's hosted MCP implementation,
private Codex connector, service source code, financial or personal data,
OAuth or API credentials, branded artwork, or marketplace icon.

Brex's official MCP guide is pinned at update timestamp
`2026-05-07T15:57:03.000Z` and exact Markdown SHA-256
`0d1f82f38bb572f82c4a16d9c4ddd787333b3f466ddc485b5e6399903ec7adf9`. Its ordered 43-tool names have SHA-256
`b3ecc5bbc619380164541cf93f16678da4a9df256859c62f9b26d4a054958fef`, and the complete name, description, and access table
has SHA-256 `ad0bf121e350bb47363ce6603e994c88cb1d0955d24fc363918d54fa2a3490a8`.

The official protected-resource metadata is pinned at canonical JSON SHA-256
`06b076acaecafd323510dffc6eec88d4615377444808bfa57a34e7828ab3a818`, and the authorization-server metadata at
`6cf20c287281acae2a8bad5ce78e5650ccc193f9040f2d43c2ba9a6a333f8299`. Codex capability evidence is pinned to OpenAI's
plugin snapshot revision `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying the private
app ID or marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://api.brex.com/mcp` using Streamable HTTP and Brex
  browser OAuth. An account or card admin must accept the Developer API
  agreement and enable the current Brex in AI assistants beta.
- The service declares 19 OAuth scopes, Dynamic Client Registration,
  authorization-code and refresh-token grants, public clients, optional
  `client_secret_post`, and PKCE S256. Brex also supports user-managed,
  least-privileged API tokens for clients that cannot use OAuth.
- On August 13, 2026, an unauthenticated MCP initialize request returned HTTP
  401 with Brex's authorization and protected-resource challenge. One
  disposable loopback public client registered with HTTP 201 and no client
  secret, and its PKCE authorization request reached the Brex login flow. The
  response provided no registration management URI or access token, so the
  audit client could not be deleted through RFC 7592 management.
- The official beta catalog exposes 43 tools covering users and organization
  dimensions, reward points, expenses, analytics, receipts, attendees, spend
  limits, reimbursements, exports, merchants, cards, policy, business
  accounts, banking transactions, bills, vendors, accounting integration and
  records, GL accounts, trips, bookings, group events, and product feedback.
- Thirty-seven tools are read-oriented. Six require confirmation because they
  update expense memos, upload receipts, replace attendees, assign limits,
  start sensitive expense exports, or send feedback to Brex.
- This covers the Codex app's spend analysis, anomaly review, policy
  questions, reimbursement status, role-aware finance queries, and Delta
  merchant-spend workflow through Brex's official public MCP transport.
- Brex explicitly states that approvals and card management are not yet
  available through MCP. Travel tools currently list trips, bookings, and
  group events rather than modifying reservations.
- Authenticated tools/list and financial-data operations were not run because
  no user Brex account, credentials, or company data was used during the
  audit. The server is beta and its tool surface can change.
- The included skill protects financial and personal data, preserves
  currency, date, entity, and filter provenance, prevents unsupported claims
  of audit or settlement, and requires exact-target confirmation for every
  mutation, export, URL fetch, or external feedback action.
- A generic expense-control icon is used because no licensed Brex catalog
  artwork is included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Brex accounts, financial products, Developer API access, hosted service
behavior, data, permissions, beta availability, trademarks, privacy policy,
access agreement, and terms remain controlled by Brex.
