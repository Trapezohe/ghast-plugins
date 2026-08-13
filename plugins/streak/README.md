# streak

Read, analyze, and update Streak CRM pipelines, boxes, deals, contacts,
organizations, comments, tasks, assignments, and timelines through Streak's
official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute Streak's hosted MCP implementation, private Codex connector,
service source code, or marketplace artwork.

The adapter is pinned to Streak's official MCP integration page with SHA-256
`87c17a922fb538f958c36f4528f2ea8a23d221182eade3202d55700738dc11e6` and its official Claude integration page with SHA-256
`f49193624657662fa71218d4070e1cf16bcd103b67a91375b5d80db7a1a86c0a`. The OAuth protected-resource metadata is pinned
at canonical JSON SHA-256 `493b0f31d7f3620ba61363bf0108f84382bbd151611070a05875f7264f6cff67`. The OAuth
authorization-server metadata is pinned at canonical JSON SHA-256
`b6e067661810a32ab8d4704e08161a47c8fb344080baac1fcc0c8ab792672a4f`.

## Ghast compatibility

- Ghast connects directly to `https://api.streak.com/mcp` using Streamable HTTP and
  Streak OAuth. The service declares dynamic client registration,
  authorization-code and refresh-token grants, public clients, and PKCE S256.
- Official capabilities include search and reporting across pipelines, boxes,
  deals, contacts, organizations, fields, and timelines, plus creating and
  updating records, stages, comments, assignments, tasks, call or meeting
  logs, custom-column options, and selected Gmail timeline entries.
- This is a superset of the Codex app's recent-deals and CRM context
  capability. State-changing operations are guarded by explicit confirmation.
- Streak's MCP exposes CRM data and timeline context, not Gmail email bodies
  for analysis. It can attach a user-selected Gmail thread to a box timeline.
- Endpoint discovery and the complete OAuth protocol were verified without an
  account. Authenticated tool execution was not run and requires an eligible
  Streak Pro, Pro+, or Enterprise account with appropriate workspace access.
- A generic CRM pipeline icon is used because no licensed catalog icon is
  included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Streak accounts, subscriptions, hosted service behavior, CRM data,
permissions, automations, trademarks, and terms remain controlled by Streak.
