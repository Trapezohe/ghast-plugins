# omni-analytics

Query governed Omni semantic models, run multi-step analysis, and search Omni
documentation through Omni's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored configuration, safety instructions,
documentation, metadata, and a generic analytics icon. It does not
redistribute Omni's hosted implementation, private Codex connector, OAuth
PAT, organization data, semantic models, branded artwork, or marketplace
icon.

Omni's official MCP overview, tools, authentication, and Codex guides are
pinned at normalized visible-text SHA-256 `d22f4d9c42b15fa97eeaefe37dce4d31bbb52ce968c1c7dbcf47637abc0872fa`,
`18dce31231e8f0b1dd62c5b4e107d54b4803f99c74ad25ec024fd5e1ab28d5f8`, `779b685508cd2f7c9b761f12f29a19f0008846a7be48e61c17aefd1321a24c0f`, and
`1974715a5941f16c8813bbe4f51dc60df89da88fb1d5e421dbc41b78f4b2a475`. The documented six-tool order is pinned at
`37c5604086f9169334cd49d7e055ec0efe9dfa1cf6f7f4107f785e2d29280c34`.

Protected-resource and authorization-server metadata are pinned at canonical
JSON SHA-256 `14b3543ee3f07ac43c85f360aa9f88459d8fc90fce9bbb5fc158c1627d6a2037` and
`c75b0e080de0aa01d92f76bb50443d9d6b3879cfee1ee96c44c63ef1cc60b780`. Codex capability evidence is pinned to OpenAI
plugin snapshot `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app ID
or marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://callbacks.omniapp.co/callback/mcp` and uses Omni's recommended
  browser OAuth flow for Codex-compatible clients.
- The official tools select models and topics, execute governed queries,
  submit and poll multi-step agentic analysis, and search Omni documentation.
- This covers the Codex workflow for last year's orders by status and the
  described semantic-model, permissions, row-level-security, business-logic,
  and business-definition boundaries.
- `askOmni` can also create recurring routines delivered by email or Slack.
  The included skill treats this as an external persistent action and
  requires schedule, recipients, query, permissions, and explicit
  confirmation.
- On August 13, 2026, a loopback public OAuth client registered with HTTP 201
  and no client secret. The authorization page returned Omni's login-required
  response because the audit browser had no active Omni instance cookie,
  matching the official requirement that OAuth uses the last logged-in Omni
  instance.
- An unauthenticated initialize request returned HTTP 401 with the exact
  `mcp:access` protected-resource challenge. Authenticated tools/list and
  organization-data queries were not run because no Omni account or data was
  used.
- A generic analytics icon is used because no licensed Omni catalog artwork
  is redistributed.

The MIT license in this package applies only to the Ghast-authored adapter.
Omni accounts, organizations, PATs, semantic models, hosted behavior, data,
permissions, trademarks, privacy policy, and terms remain controlled by
Omni and the connected data providers.
