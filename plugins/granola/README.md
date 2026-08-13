# granola

Search and analyze Granola meeting notes, transcripts, attendees, folders,
decisions, and action items through Granola's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, catalog metadata, and a generic icon. It does not
copy or redistribute Granola's hosted MCP implementation, private Codex
connector, meeting data, OAuth credentials, branded icon, or marketplace
artwork.

The adapter is pinned to Granola's official MCP documentation with SHA-256
`b091dacafcec3672ae15a7b8e3ed6edfe82a8f887ebb1d1abe525292bb47b7d8`. The exact ordered six-tool inventory has SHA-256
`30b13518fdef35595ad1411cec22a13da9027599275702bb4f537114b25c717c`. The official protected-resource metadata is pinned
at canonical JSON SHA-256 `ffbe7699c7ae6cbfcbd3a9c0ddc89e081e1d48ec7b49ca93bb2608bbaa7b0adb`, and the
authorization-server metadata at `710cc56359dd3b0725ff8a797a54de42c0cdf5e630d957ad16e8d7c117bed07c`. The Codex
capability evidence is pinned to OpenAI's plugin snapshot revision
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its connector mapping or artwork.

## Ghast compatibility

- Ghast connects directly to `https://mcp.granola.ai/mcp` using Streamable HTTP and
  Granola browser OAuth. The service supports Dynamic Client Registration,
  authorization-code and refresh-token grants, public clients, and PKCE S256.
- Granola documents six read-only tools for natural-language meeting queries,
  folder listing, filtered meeting listing, note retrieval, raw transcript
  retrieval, and connected account or active workspace identity.
- This covers the Codex app's topic, person, company, and timeframe search,
  conversation citation, customer-feedback retrieval, deal-history summary,
  decision and action-item extraction, and cross-meeting synthesis workflows.
- Access follows the user's active Granola workspace. Personal, public, and
  Enterprise-admin scopes, note sharing, workspace policy, and plan
  entitlements determine which meetings and tools are available.
- Basic accounts are limited to personal notes from the last 30 days. Some
  folder, search, and transcript tools require a paid plan. Granola documents
  rate limits averaging around 100 requests per minute, varying by plan and
  tool.
- The hosted MCP implementation is not open source and is not redistributed.
  Documentation, the complete published six-tool catalog, OAuth metadata,
  disposable public-client registration, Codex capability evidence, and
  unauthenticated protocol behavior were verified without a Granola account.
  Authenticated tools/list and meeting-data operations were not run.
- A generic meeting-notes icon is used because no licensed catalog artwork is
  included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Granola accounts, subscriptions, hosted service behavior, meeting notes,
transcripts, permissions, trademarks, and terms remain controlled by Granola.
