# fiscal-ai

Research public companies with source-linked financials, filings, ratios,
segments, KPIs, prices, ownership, news, events, and fund letters through
Fiscal.ai's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, catalog metadata, and a generic financial-
research icon. It does not copy or redistribute Fiscal.ai's hosted MCP
implementation, private Codex connector, API key, account data, official
workflow bundle, source skill, branded artwork, or marketplace icon.

Fiscal.ai's current MCP guide main content is pinned at normalized SHA-256
`ed7d01d13419e9aa2aa6f8d674b82400e9aacf50d4664bf9d3b1f64435150418`. Its documentation index and OpenAPI document are
pinned at `00315b347e49ef2d5373f0a7ee582d50686acf39f3ad9aacfa2da45571a0fad8` and `aaf1105c93c6bdadb599eed30d38f3cf7d94ebc5940a56258bcfb64dc01bc912`. The OpenAPI
contains 49 GET operations and no POST, PUT, PATCH, or DELETE operations at
the audited revision.

The official MCP tool descriptor is pinned at raw and canonical SHA-256
`8c53424110e002a0a0fbbe70741668d6aeae442a6ded7673361727760a6a4fd6` and `81b3f6f1dd2fac2a677e1ad87ed136b50ff0cfaf9327b201e98b3d9457c66e17`. It exposes
`api_docs` and `execute_code`; their ordered-name, name-description, and
input-schema hashes are `7e1c1556c635358e29d25a6a29f3635480ad3549f245f9a279bffce4db163baf`,
`61e2e6aed93df38f4acee16d0fad76b94b7bf77ef34ce980a7e5d207b248b7a3`, and `7aecaac4c90f91b846e5afef4ced770daf93b78f6cf5d121cab7d17d92f894b7`.

Protected-resource and authorization-server metadata are pinned at canonical
JSON SHA-256 `d3acf769990a6a15a4eeab9e21d0d0968af9ead6bd77b261d76fa50c5031d6ce` and
`4cedf324baa9e5aa99a25ee1e2d89be2ce8b64e541d8298ba55a9ff67585e810`. They publish 11 data scopes, bearer-header
authentication, authorization code, refresh tokens, public clients, Dynamic
Client Registration, and PKCE S256.

Fiscal.ai's official workflow release metadata is pinned at
`c7a7851ea9e784e0eb933e15f50b829c9d9ab57c234ff7bc19a181b9156ed5f1`. The 35-file version 5 archive is pinned at
`25015c6addfbb41ced0e678e191288aa6c838b4db5f0971aada7106430cf7a28`. The official client repository is pinned to
`20b67b677a21723cb76f30202a2495f20b8f22af`. Neither source contains a license file at the
audited revision, so none of its skill text or client files are redistributed.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying the private app identifier or
marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://api.fiscal.ai/mcp` over Streamable HTTP and
  sends the user-owned API key from the `fiscal-api-key` vault entry as an
  Authorization Bearer header, matching Fiscal.ai's documented setup for
  coding clients.
- API-key and OAuth access use the same Fiscal.ai account, plan, company
  coverage, data entitlements, and rate limits. The official guide describes
  a free-plan surface of 100 companies, but live account responses remain
  authoritative.
- The current MCP surface uses `api_docs` to discover helper signatures and
  `execute_code` to run exact async JavaScript in a network-isolated,
  30-second sandbox with at most six concurrent calls.
- The underlying documented API covers 49 read operations across company
  profiles, as-reported and standardized financial statements, metrics,
  ratios, adjusted numbers, segments and KPIs, ownership, events, splits,
  prices and shares, filings and filing pages, IR events and transcripts,
  news, fund letters, and related source material.
- This reproduces the Codex workflows for recent financials, filings, risks,
  revenue growth, margins, valuation, peer comparison, ticker insights,
  source links, company KPIs, revenue segments, adjusted metrics, and
  historical or current quotes at Fiscal.ai's official product surface.
- Every material figure should retain company identity, period, currency,
  units, basis, timestamp, and source-document provenance. The included skill
  distinguishes reported, standardized, adjusted, calculated, assumed, and
  judgmental values and prevents traceability from being mislabeled as audit
  assurance.
- The separately downloadable official skill bundle covers broader guided
  workflows such as financial models, valuation, screening, watchlists,
  ownership, earnings reaction, credit analysis, and industry research. It
  is not packaged because no redistribution license was found. Ghast includes
  an independently authored safety and evidence workflow instead.
- On August 13, 2026, an unauthenticated initialize request returned HTTP 401
  with Fiscal.ai's exact missing-token response and official protected-
  resource challenge. One public OAuth client had previously registered
  without a client secret and reached Fiscal.ai's consent page through PKCE;
  it could not be deleted because the response supplied no registration
  access token.
- Authenticated tools/list and company-data requests were not exercised
  because no Fiscal.ai API key, account, private entitlement, or research
  data was used during the audit.
- A generic financial-research icon is used because no licensed Fiscal.ai
  catalog artwork is redistributed.

The MIT license in this package applies only to the Ghast-authored adapter.
Fiscal.ai accounts, plans, hosted service behavior, financial data, source
documents, official skills, permissions, trademarks, and terms remain
controlled by Fiscal.ai and the applicable data providers.
