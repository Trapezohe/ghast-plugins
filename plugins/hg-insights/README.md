# hg-insights

Research companies, markets, technology adoption, buying signals, spend,
contracts, contacts, and GTM segments through HG Insights' official Phoenix
MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, metadata, and a generic revenue-intelligence
icon. It does not redistribute HG Insights' hosted implementation, private
Codex connector, API key, OAuth credential, customer data, proprietary
datasets, partner data, branded artwork, or marketplace icon.

HG Insights' official getting-started, authentication, OAuth, MCP tools, MCP
prompts, MCP resources, and security pages are pinned as normalized visible
text at SHA-256 `b6e3666c469eb531839866f62f38c7372cb0099f0600d4e7402e03960a32ca01`,
`57567aa2b2e3ddb6ea6d318789a1f45b07c412626bae0647f7018e93cb018ece`, `ebef11b2db8f3456ee7750a3486ecb869bdbb65fa5187abbc80d2a67b1487644`,
`c6ffc8835205c221b3f229ba205f2f946042804b406feb01ee4e1440cdde463b`, `14c9fca2cd9aa51a31a2364bd07e6d6478d381c5a4ab4d0e0d913bb2e1d2bb88`,
`2141c28856bcd3dfa369ca90981753d90a6cf8ddbc7eb9d89deb6cad874735c1`, and
`60950ba964321a84fb6f13199f970ad5b1c475f25485b528370e8d42cc1533be`.

Protected-resource and authorization-server metadata are pinned at canonical
JSON SHA-256 `8bce6138eff9a6e27fef713ec8ab3e7633119427819e5d45bf0c185cd0fa0290` and
`b8c5272ae66b4b5921abdd8e463bdb9eefb7b9aa3538c3b06fa4742892d72fb7`. The ordered 33-name tool-identifier
inventory extracted from the official overview is pinned at
`52b53bfbd2774c844a5dfa00a0cb2c96d4220c8d50e787ddb54654b65efa76ec`.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` with complete four-file inventory SHA-256
`c0e819826a9d60e83ff36b1cf881cafc64288857e5d1b5e15d6a7fde08116aee`. The private app ID and marketplace
artwork are verified as evidence but are not copied into this package.

## Ghast compatibility

- Ghast connects directly to `https://phoenix.hginsights.com/api/mcp` over Streamable HTTP and
  sends the user-owned Phoenix API key from the `hg-insights-api-key` vault
  entry as an Authorization Bearer header.
- HG Insights officially documents this header-based endpoint for gateways
  that should not put keys in URLs and states that it exposes the same MCP
  tools as the URL-path endpoint. This avoids copying or depending on
  OpenAI's private app connector.
- The official OAuth endpoint `https://phoenix.hginsights.com/api/ai/mcp` and OAuth 2.1
  discovery metadata are also verified. They publish authorization code,
  refresh tokens, PKCE S256, dynamic client registration, revocation, and
  `mcp:read`, `mcp:tools`, and `offline_access` scopes. This package uses the
  simpler official API-key route because Phoenix documents it for direct
  integrations controlled by the client owner.
- The official product surface covers company identity and firmographics,
  technographics and install history, operating and AI maturity signals,
  functional adoption, buyer intent, IT and cloud spend, contracts, contacts,
  product and vendor intelligence, SEC filings, federal contracts and
  opportunities, governed warehouse queries, web research, and Phoenix agent
  invocation.
- This is a functional superset of the Codex description and all three
  default workflows: account prioritization using buyer intent, market sizing
  and GTM segmentation, and target-account enrichment with technographics,
  spend, and buying signals.
- The official prompt catalog adds guided onboarding, account research,
  qualification, intent targeting, vendor-sprawl analysis, pre-call briefs,
  competitive analysis, TAM sizing, battlecards, ICP refinement, and market
  analysis. Four official UI resources render company, technology, intent,
  and spending views when supported by the client.
- HG Insights explicitly permits MCP data for agentic workflows but excludes
  populating or maintaining systems of record and deterministic scheduled,
  per-record, or scripted batch processes. The included skill enforces that
  boundary and directs CRM, MDM, and warehouse loading to separately licensed
  HG Insights API or SaaS workflows.
- Contacts can contain PII, partner integrations can impose separate
  entitlements, and many data, query, reveal, web, and agent operations can
  consume credits. The skill minimizes retrieval, preserves source and model
  distinctions, and confirms broad or materially billable work.
- The official tools overview headline says 29 native tools plus two
  aggregated tools, but its current body contains 33 distinct tool
  identifiers after excluding protocol and integration identifiers. The
  adapter records this documentation inconsistency and treats authenticated
  `tools/list` as authoritative.
- On August 14, 2026, missing and invalid API-key initialize requests to
  `https://phoenix.hginsights.com/api/mcp` returned HTTP 401 with distinct official Bearer
  challenges. Missing and invalid OAuth tokens at
  `https://phoenix.hginsights.com/api/ai/mcp` also returned HTTP 401 and the official
  protected-resource challenge.
- The OAuth metadata advertises dynamic client registration, but a disposable
  registration probe from the audit environment was rejected with HTTP 403
  by the service edge. No client registration, user sign-in, token, reusable
  credential, authenticated tool list, account data, contact data, credits,
  query, or agent run was obtained or used.
- No public source repository for the hosted Phoenix MCP implementation was
  identified at the audited revision. The adapter relies only on
  developer-owned documentation, live authentication boundaries, standard
  metadata, and user-supplied service credentials.
- A generic revenue-intelligence icon is used because no licensed HG Insights
  catalog artwork is redistributed.

The MIT license in this package applies only to the Ghast-authored adapter.
HG Insights and Phoenix accounts, plans, credits, hosted behavior, datasets,
partner data, permissions, trademarks, privacy policy, and terms remain
controlled by HG Insights and the applicable source providers.
