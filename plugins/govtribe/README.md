# govtribe

Research public-sector opportunities, awards, vendors, agencies, forecasts,
pricing, files, news, and authorized workspace records through GovTribe's
official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, metadata, and a generic government-procurement
icon. It does not redistribute GovTribe's hosted implementation, private
Codex or ChatGPT app connector, API key, account data, proprietary datasets,
branded artwork, or marketplace icon.

GovTribe's official MCP overview, developer guide, server URL guide, Codex
guide, agent server reference, tool index, and credit guide are pinned at raw
SHA-256 `e0cd276f0d5e7e9307d918363a29d8063247de605abab68246764531da46d123`, `60f1edacc30620b830e87b8ffa40b8e90dd48c863f84d77edcd45c0233c24c49`,
`6ea83b94854e1ae8e93c42211ecc36365e30a6740c2f091b82eeaf2abfbb298f`, `eed173f8a6192d07b5557de5be404f5bf60317345293daeb9d0ac154c9cc8fb2`,
`4df552f76669bb618e1a2ee82214be42d15522f53cb9facbf304fe3184412e05`, `80cebed0f45519e12e113404b0a76e8bb78f4b1318e9c413d74282e891453a5c`, and
`0ee127c27f2a3a78cb7ed44c93bbff1afb16c7570960ae58a078f1f02c8eb551`.

The official tool index contains 102 entries representing 101 unique MCP
tool names because `Search_Service_Contract_Inventory` appears in two
categories. The unique-name, complete name-to-annotation, and ordered-entry
hashes are `a3a15c921e76186a7fcc3293dd7d55f644b88a4ca14505b381f8c0a39746d7a0`,
`eed9dde0f2ea29625133259afc34efaa7a0fa9e4abe84dd54c9e93445fc42494`, and
`6cf75419d4b512d0d33285fb3daa75c96fdc4d7c24d9a6d1de1086f2c9bed299`.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app ID or
marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://govtribe.com/mcp` over Streamable HTTP and
  sends the user-owned MCP API key from the `govtribe-mcp-api-key` vault
  entry as an Authorization Bearer header. This is the exact endpoint and
  authentication pattern in GovTribe's official Codex guide.
- The official standard server covers broad public procurement intelligence:
  federal contracts, grants, state and local records, agencies, vendors,
  opportunities, forecasts, awards, IDVs, vehicles, sub-awards, transactions,
  categories, contacts, pricing and labor data, government files, and
  procurement news.
- It also exposes account-dependent workspace, pursuit, pipeline, stage, tag,
  task, saved-search, automation, teaming, file/vector, interactive, memory,
  documentation, and prior-conversation workflows. This is a functional
  superset of the Codex description for opportunity context, vendor
  competition, teaming partners, agency spending patterns, market research,
  competitive analysis, and proposal preparation.
- At the audited revision, 59 unique tools are annotated read-only and 42 are
  state-changing. Of the latter, 20 are destructive and idempotent, 16 are
  destructive and not idempotent, two are non-destructive and idempotent, and
  four are non-destructive and not idempotent. The included skill requires
  exact target review and current-conversation confirmation for every
  state-changing operation.
- Most GovTribe MCP work is credit-billed separately from the subscription.
  The skill discloses credit use before billed work and requires confirmation
  for broad, multi-step, file/vector, interactive, automation, or otherwise
  material workflows. Current prices and exemptions remain authoritative in
  the user's account and GovTribe consumption table.
- GovTribe's OpenAI compatibility endpoint is narrower and intended for an
  existing curated OpenAI-hosted client. Ghast uses the standard endpoint
  because GovTribe's official Codex guide explicitly configures it, preserving
  the complete current official product surface instead of guessing at a
  private app connector.
- On August 13, 2026, missing and invalid Bearer initialize requests to the
  standard endpoint returned HTTP 401 with distinct official
  unauthenticated-token responses. Authenticated tools/list and account-data
  operations were not run because no GovTribe account, API key, credits, or
  private workspace data was used.
- No official public source repository for the hosted MCP implementation was
  identified. The adapter verifies GovTribe-owned documentation, endpoint
  behavior, tool safety metadata, and OpenAI's Codex capability snapshot
  without redistributing service code.
- A generic government-procurement icon is used because no licensed GovTribe
  catalog artwork is redistributed.

The MIT license in this package applies only to the Ghast-authored adapter.
GovTribe accounts, plans, credits, hosted service behavior, data,
permissions, trademarks, privacy policy, and terms remain controlled by
Government Executive Media Group LLC and the applicable source providers.
