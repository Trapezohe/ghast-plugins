# otter-ai

Search Otter meeting history and retrieve full transcripts, summaries, action
items, attendees, and meeting context through Otter.ai's official hosted MCP
server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, catalog metadata, and a generic icon. It does not
copy or redistribute Otter's hosted MCP implementation, private Codex
connector, meeting data, OAuth credentials, branded icon, or marketplace
artwork.

The adapter is pinned to Otter's official Help Center article
`35287607569687`, updated `2026-08-12T06:17:46Z`, with canonical
article SHA-256 `49d38efcc92e29f310b30f0dc7b3ae4335c17a13b7d60eff5ce2d7734d39e56e` and body SHA-256
`abbb56e42c6c507338d7e03caedae09d0c62ce5589af7f3a075aec9c01beb535`. The normalized ordered three-tool inventory has
SHA-256 `d68e926a4dcdc7bcf9b30a0ef4b45116bafa70bfb76d8e970438e044454a1ccb`. The official protected-resource metadata is
pinned at canonical JSON SHA-256 `1b480247ee26dee3a9d3ee0b5d80bb7abdc1e137830f36154449d4b04234e920`, and the
authorization-server metadata at `901170a7510699249e6ce0fa12cb7211072205b9a4e996fa3313157d1778dd0e`. The Codex
capability evidence is pinned to OpenAI's plugin snapshot revision
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its connector mapping or artwork.

## Ghast compatibility

- Ghast connects directly to `https://mcp.otter.ai/mcp` using Streamable HTTP and Otter
  browser OAuth. The service supports Dynamic Client Registration,
  authorization-code and refresh-token grants, public clients, and PKCE S256.
- Otter officially documents three read-only tools: profile lookup, meeting
  search, and full transcript fetch. The OAuth scopes are `profile:read` and
  `conversations:read`.
- This covers the Codex app's recent-meeting listing, keyword, date, attendee,
  folder, and channel search, summaries, action items, metadata, speaker-aware
  transcript retrieval, meeting preparation, decision extraction, and
  cross-meeting synthesis workflows.
- Otter can expose meetings captured by the user and meetings shared with the
  user by others in the Workspace. Existing conversation sharing, Channels,
  Workspace permissions, subscriptions, and retention settings remain
  authoritative.
- The hosted MCP implementation is not open source and is not redistributed.
  The official article, complete published three-tool catalog, OAuth metadata,
  disposable public-client registration, Codex capability evidence, and
  unauthenticated protocol behavior were verified without an Otter account.
  Authenticated tools/list and meeting-data operations were not run.
- A generic meeting-transcript icon is used because the downloadable official
  icon does not include a public redistribution license.

The MIT license in this package applies only to the Ghast-authored adapter.
Otter accounts, subscriptions, hosted service behavior, meeting data,
recordings, permissions, trademarks, and terms remain controlled by Otter.ai.
