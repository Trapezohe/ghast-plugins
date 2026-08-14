# cogedim

Find current Cogedim new-build lots and developments, retrieve official
program details, and research Cogedim buying or investment guidance through
Cogedim's official public hosted MCP.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, workflow and
safety instructions, documentation, metadata, and a generic residential
search icon. It does not redistribute Cogedim's hosted implementation,
private Codex app mapping, property data, official documentation text,
trademarks, branded artwork, or marketplace icons.

Cogedim's official `https://www.cogedim.com/mcp` entry identifies
`cogedim-mcp-server` version `1.0.0` and publishes its Streamable HTTP JSON-RPC
transport. Its canonical JSON SHA-256 is
`69802ca971dc6ac35e8ede7caecb60d2cef04085d0c25c131b2f56d948677aad`.

The API and developer section of Cogedim's official LLM reference is pinned
at normalized SHA-256 `3bd622452f97c133d8220c81e12fa1aba3f118577f919cfdcd53775abc38eac0`. It directly links the MCP
endpoint and documents location, budget, and room-based development search,
detailed lot prices and returns, complete program descriptions and visuals,
offers, and buying or investment content.

The live MCP `initialize` result is pinned at canonical JSON SHA-256
`ec7893b3a416a1326bc00aabd0a5aab8930ad7f339f9a94227d14c984e1d4004`. The exact ordered eight-tool schema is pinned
at canonical JSON SHA-256 `6351b9900840a77a488e27c22f27295f5f51c3914d9b98aa02a122ed85417c5b`; its NUL-delimited name
inventory is pinned at SHA-256 `348da8b99b5eb5a51fc4d6117aefbfa0098239007ecce7773b221e2dde9901d5`.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app ID or marketplace
artwork.

## Ghast compatibility

- Ghast connects directly to `https://www.cogedim.com/mcp` over Streamable HTTP. The
  audited public endpoint does not require an account, API key, or OAuth.
- The service exposes `search_programs`, `search_lots`, `get_program`,
  `search_content`, `get_content`, `render_search_programs`,
  `render_search_lots`, and `render_program`.
- Every live tool advertises `readOnlyHint=true`,
  `destructiveHint=false`, and `openWorldHint=false`.
- The server's own instructions require property searches to start with
  `search_lots`, fall back to `search_programs`, and use `get_program` for
  selected developments. Informational questions use official content search
  and retrieval.
- On August 14, 2026, a real unauthenticated Paris search with a maximum
  budget of EUR 800,000 returned structured current lots with official
  Cogedim URLs, program identifiers and names, property details, multiple
  price structures, delivery information, regulations, and stated returns.
  The verifier checks live structure and official URLs rather than pinning
  mutable listing values.
- The five core search and retrieval tools provide the portable data
  capability. The three render tools may require a host that supports the
  returned Apps UI and are optional in text-only clients.
- This matches and extends the Codex default workflow for finding relevant
  Cogedim properties from a brief: the official service additionally exposes
  detailed lot, program, content, and optional rendering tools.
- Inventory, prices, promotions, returns, construction schedules, and
  delivery dates remain live and mutable. The included skill records
  retrieval time, preserves price types and assumptions, flags conflicting
  records, and requires current confirmation before a consequential decision.
- No public source repository for the hosted implementation was identified.
  Ghast therefore integrates the directly usable official service instead of
  inventing or redistributing a substitute server.
- A generic residential-search icon is used because no licensed Cogedim
  catalog artwork is included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Cogedim's hosted service, listings, program material, trademarks, privacy
policy, terms, prices, promotions, availability, and service behavior remain
controlled by Cogedim and the applicable rights holders.
