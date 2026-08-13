# thoughtspot

Search governed ThoughtSpot content, answer business-data questions with
Spotter 3, explain drivers and anomalies, and save explicitly approved
analyses as dashboards through ThoughtSpot's official hosted MCP.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, metadata, and a generic analytics icon. It does
not redistribute ThoughtSpot's MCP implementation, official source skill,
private Codex connector, OAuth credentials, customer data, trademarks,
branded artwork, or marketplace icons.

ThoughtSpot's official MCP overview and connection guide are pinned as
normalized visible text at SHA-256 `19631cc2bc1a489d579407235986299214fa94e98d2a28f19a6bac6281f5ae15` and
`4ca5e2674b0492fddb8e62334d4daf17329b2c857518fafaa549c42dc53778b8`.

The official `thoughtspot/mcp-server` repository is pinned to
`79e978603135fc079427db091c2b79bea34cbe68` with Git tree
`bbee5589fd152788377db9ee0910b4c7df8086e6`. Its source, tests, version registry, tool
definitions, and official skill are audit evidence only. The repository uses
the ThoughtSpot Development Tools EULA, which restricts redistribution and
modification, so none of those files is included in this plugin.

The pinned `2026-05-01` Spotter 3 inventory contains eight tools with ordered
name SHA-256 `5d067ec65a48ae86126cf9bfacb208c8033234fe4b61d412c2efbdcd6864aada` and normalized safety-classification
SHA-256 `7eec1b6ef4db5b41ee06f5e6945f13438e2552dc8882694dfc2cf9368d3577cd`. The authorization-server metadata
is pinned at canonical JSON SHA-256 `bd3db075f410942be77b1bd9923231ea9d5146f421eba5a03a8dec8d90c8e27c`.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app ID or
marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://agent.thoughtspot.app/mcp?api-version=2026-05-01` over Streamable HTTP.
  The date-pinned endpoint avoids silently opting into later tool or schema
  changes.
- ThoughtSpot's official hosted service supports OAuth authorization code and
  refresh tokens, Dynamic Client Registration, public clients, and PKCE S256.
- The eight pinned tools search Answers, Liveboards, visualizations, and
  Worksheets; test connectivity; create and continue analytical sessions;
  poll streamed analysis; save approved results as dashboards; list Orgs; and
  switch the active Org.
- This covers and extends the Codex workflows for sales-performance answers,
  pipeline movement, revenue-by-segment analysis, trusted business drivers,
  anomalies, governed semantic context, and actionable links.
- Spotter 3 adds advanced analysis, forecasting, multi-step reasoning,
  automatic data-source selection, and deep research. ThoughtSpot continues
  to enforce object, row-level, and column-level security.
- `create_dashboard` writes durable content. `switch_org` changes a durable
  active context shared across sessions. The included skill requires exact
  target review and explicit confirmation for both.
- `create_analysis_session` and `send_session_message` are annotated as not
  read-only because they create transient analytical state. The skill avoids
  duplicate sessions, waits for completion, and preserves query context.
- On August 13, 2026, missing and invalid Bearer initialize requests returned
  HTTP 401 with body SHA-256 values
  `fde5a2f4681d6c07ac053684ff82e9c3a1b6d6141388f8551d551f27e3d3ad45` and
  `db9fe3458a7a7b7f968eda46e4283a391a29eec5d070b593291b327caab742da`.
- A disposable loopback public client registered with HTTP 201, no client
  secret, authorization-code and refresh-token grants, and PKCE S256. Its
  authorization request reached ThoughtSpot's official instance-selection
  page. The response supplied no registration access token, so the normal
  importer does not repeat this side-effecting probe.
- The clean pinned source installed from its lockfile with scripts disabled
  and passed 31 test files containing 704 tests. The dependency audit
  reported 34 upstream advisories, including three critical advisories.
  Ghast packages none of those source dependencies or server code.
- Authenticated tools/list, customer data, analytical queries, forecasts,
  dashboard creation, and Org switching were not exercised because no
  ThoughtSpot account or business data was used.
- A generic governed-analytics icon is used because ThoughtSpot's source and
  brand assets are not licensed for redistribution in this package.

The MIT license in this package applies only to the independently authored
Ghast adapter. ThoughtSpot accounts, hosted service behavior, source code,
customer data, analytics, permissions, trademarks, privacy policy, EULA, and
terms remain controlled by ThoughtSpot and the applicable data providers.
