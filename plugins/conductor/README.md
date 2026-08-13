# conductor

Analyze AI and traditional search visibility, citations, sentiment, rankings,
competitors, and tracked configuration through Conductor's official hosted
MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute Conductor's hosted MCP implementation, private Codex connector,
proprietary datasets, API tokens, or marketplace artwork.

The adapter is pinned to Conductor's official ChatGPT and Codex setup guide at
SHA-256 `8f616240df58c8ecf056b6cf2964fa11038899ffcb884a3d725eebfc95ee9003`, official data reference at
`159f29e8eeae40472324256dd1519b72f0350d5637396fc52a3511436be2fd4b`, and official MCP FAQ at
`0932a35ad457658f7d53b9322939bab9e9dabc58df9d507072a37661914f258e`.

## Ghast compatibility

- Ghast connects directly to `https://mcp-universal.conductor.com/mcp/v3` over Streamable HTTP using
  a user-managed Conductor API token with Bearer authentication.
- The current official custom connection exposes five tools:
  `tracked_configs`, `ai_brand_insights`, `ai_citation_insights`,
  `keyword_insights`, and `ai_query_fan_out_insights`.
- These tools cover tracked account configuration, AI brand visibility,
  mentions, share of voice, sentiment, citations, source URLs, traditional
  rankings, seasonality, SERP result types, keyword detail, and competitive
  benchmarking. This fully covers and extends the Codex prompt for identifying
  top competitors for a topic such as wireless earbuds.
- Conductor states that custom connections receive the newest MCP tool set
  without waiting for a marketplace review cycle, while the service remains
  read-only.
- Missing and invalid Bearer initialize requests were verified to return HTTP
  401 from the official endpoint. Authenticated tools and customer data were
  not accessed because no Conductor token or account was supplied.
- A generic search-intelligence icon is used because no licensed catalog
  artwork is included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Conductor accounts, subscriptions, tool-call allocations, hosted service
behavior, datasets, permissions, trademarks, privacy policy, and terms remain
controlled by Conductor.
