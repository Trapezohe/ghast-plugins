# channel99

Analyze read-only B2B marketing performance, channels, vendors, campaigns,
audiences, account engagement, attribution, spend efficiency, and pipeline
influence through Channel99's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, measurement and
privacy instructions, documentation, catalog metadata, and a generic marketing
analytics icon. It does not copy or redistribute Channel99's hosted service,
private Codex connector, customer data, application bundle, official logo,
credentials, or marketplace artwork.

The official Channel99 support evidence is pinned as follows:

- `faq` article 47105598392475, updated `2026-05-27T17:22:19Z`, body SHA-256 `81edc9b0c2066c4f5b6c4d9bb2667af651d2b11e37692c20a7baffe72421a659`
- `mcp_information` article 46757387781275, updated `2026-03-24T18:24:09Z`, body SHA-256 `4cd47d0e997021db3644ec05fefbd275e356cb9d9391301647470547b45e295e`
- `january_release` article 48487117045019, updated `2026-03-30T21:57:22Z`, body SHA-256 `a3f1d62a2d0e9cf4853a1d271ac07c6c4cbab0e46642821e0a584f4f60d331bd`
- `snowflake_schema` article 35162878162331, updated `2026-01-30T15:33:11Z`, body SHA-256 `4acb7bcdb5b5b85e0949d1204ba8ce0292fc0e108aa52fcbf051beddfe176088`
- `reporting_api` article 49766041989787, updated `2026-07-22T17:23:54Z`, body SHA-256 `d35fdf232c66160389cfd05c2a426d2eedc3dd8fafdf78e8ae58a1f8ab0b3da7`

The protected-resource and authorization-server metadata are pinned at
canonical JSON SHA-256 `01e50ee050ad504ca381c30fb182823ac2ea165481ed5ae6b30514eb46add444` and
`2d4dd826e23de65743d61b6dd13256aead0819f212dc4108fa810ebeb6f8c77b`. The stable fields of Channel99's
Stytch authorization metadata, excluding per-request `request_id` and
`status_code`, are pinned at `e3b99805cb989002ab42d2df994eb34f16e32ce699680264bd9fa88ce07297f5`.

Codex marketplace developer and capability evidence is pinned to OpenAI
plugin snapshot `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app
ID or official artwork.

## Ghast compatibility

- Ghast connects directly to `https://mcp.channel99.com/mcp` over Streamable HTTP using
  Channel99 browser OAuth 2.1, public-client authentication, and PKCE S256.
  The service also advertises Client ID Metadata Documents and a public
  registration endpoint; the adapter stores no client secret or user token.
- Official Channel99 evidence covers web traffic, channels, vendors,
  campaigns, paid media spend, impressions, clicks, visits, audiences,
  account identity, company engagement, pixels, fit scores, attribution,
  pipeline influence, closed-won influence, keywords, ad groups, and a
  guarded SQL-backed knowledge and data interface.
- This covers the Codex connection's campaign performance, spend efficiency,
  audience engagement, cross-channel attribution, budget-analysis, and
  pipeline-efficiency questions through the same developer-operated data.
- Channel99's FAQ says the MCP database permission is read-only, and its
  January 2026 release describes enterprise read-only controls. The skill
  therefore does not claim campaign or CRM writes even though a broader
  product-information article markets separate execution pathways.
- The current authenticated tool catalog is account-controlled and was not
  enumerated without a Channel99 customer account. Live tool names, schemas,
  annotations, entitlements, and returned evidence remain authoritative.
- On August 13, 2026, missing and invalid Bearer initialize requests returned
  HTTP 401 with body SHA-256 `8f3246fc96d73ef6ff1c0eca047885cc1899e8541dc545f3eaa5003c848d52ba` and
  `8e53751849c53ad38cad77ba0bd2cc3107ff150bb5e8d5f51a1b4f8674da40de`, respectively, plus the official
  protected-resource challenge.
- No OAuth client was registered, no browser sign-in was completed, and no
  customer data, query, report, campaign, audience, CRM record, or paid
  operation was accessed during this audit.
- A generic marketing analytics icon is used because no licensed Channel99
  catalog artwork is included in redistributable official source.

The MIT license in this package applies only to the Ghast-authored adapter.
Channel99 accounts, subscriptions, hosted behavior, customer data, connected
sources, generated results, permissions, trademarks, privacy policy, and
terms remain controlled by Channel99.
