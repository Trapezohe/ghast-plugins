# scite

Search and verify scientific literature, patents, clinical trials, grants,
regulatory records, adverse-event reports, drug records, and research
collections through Scite's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored configuration, safety instructions,
metadata, documentation, and a generic research-evidence icon. It does not
redistribute Scite's hosted implementation, OpenAI's private connector,
credentials, account collections, proprietary citation model, branded
artwork, full-text corpus, or marketplace icon.

Scite's official `scitedotai/scite-mcp-skill` repository is pinned at
`9f3e3cd02c477e16c0a9b5c9114c9692d9a73317`. Its MIT LICENSE, README, and skill have pinned
SHA-256 values `a966b74650ff29ba15438f9382e2a1a0f9ef24761ec31fb851cc62dc30063780`,
`087062c06fb7e6beb21e400ca3b10594eb945658e2a7d3eef07ba4e01b16cb69`, and
`8fe719117b30d6fac41cd6bc63a8ffbf7e995a413587acdb37d89768654e54fe`. The public official skill describes the
original one-tool research workflow and supplies source and license evidence;
the current hosted server is verified independently.

Official MCP overview, coding-agent, authentication, and Search documentation
are pinned at SHA-256 `c08e15802a061de741a8f297e87520bbd07b76c5dda69b27d93fe0f1fd694f45`,
`cd0d02523607bef72859908f83854fc0a842635dcf3f878b61ba176c03711a32`, `b5954817ea50850f85e6ed9680fb51fec753b742c3ec1266279ece670b9bdf96`, and
`27a710ab2fe11904c1fbb64c71124b9d92a2f11cb08c59fc15b877b2a2341b1f`. Protected-resource and authorization-server
metadata are pinned at canonical JSON SHA-256
`9ee615b8e06246903cc05bedec3606914c7206bdfc8738c41d2e21c4fde8e9d1` and `5b1fd2b681cb4b704008c8176fed5286891d927fe59ff6c06148a8ce48e4a76c`.

The live official server's ordered 25-tool inventory and complete normalized
tool definitions are pinned at `6c1d660c935a050ea8978174321ac4f007acedfdd94dbf500d3e83a406bd1b81` and
`f59f02f87994d39dcae0bd63e8c000927f333888016663819c1f8e682140585e`. Its four prompt names and complete prompt
definitions are pinned at `d51bc5f4ebdc3e769baeaec57b888d087bae0041dbe08806516941a33f563b86` and
`46439a5bccc43ebb1c3f8d06c2244e4e93652815a216ff61474f6c79868b337c`. Codex evidence is pinned to OpenAI
snapshot `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private connector ID
or artwork.

## Ghast compatibility

- Ghast connects directly to `https://api.scite.ai/mcp` and uses Scite OAuth. The
  service publishes authorization-code and refresh-token grants, public
  clients, Dynamic Client Registration, PKCE S256, and the `mcp` and
  `offline_access` scopes.
- The 20 read-only tools cover literature and full-text excerpts, Smart
  Citations, patents, clinical trials, grants, FDA 510(k) clearances and
  summaries, MHRA alerts, MAUDE and FAERS reports, FDA drug records, and
  collection reads.
- Five state-changing tools create, update, delete, add DOIs to, and remove
  DOIs from Scite collections. Delete and DOI removal are marked destructive;
  collection creation is non-idempotent. The included skill requires fresh
  state, exact target review, visibility review, DOI diffs, and explicit
  confirmation.
- Four official prompts cover structured literature reviews, scientific claim
  checks, systematic-review screening, and bibliography verification.
- This is a functional superset of the Codex workflow for recent research and
  evidence-backed answers. It preserves paper identity, editorial notices,
  Smart Citation context, full-text source type, and reference formatting.
- On August 13, 2026, unauthenticated and invalid-token initialization both
  returned protocol success plus Scite's OAuth challenge. Unauthenticated
  `tools/list`, `prompts/list`, and a one-paper DOI lookup also succeeded,
  confirming the public evaluation surface without accessing an account.
  Account collections and protected entitlements were not accessed.
- Scite's authorization metadata advertises Dynamic Client Registration, but
  a direct audit registration request was blocked by the service's CloudFront
  layer with HTTP 403. Browser OAuth and DCR are therefore documented and
  discoverable but were not independently completed in this environment.
- The official `/mcp/health` response still lists only `search_literature`,
  while `/mcp/info` and the live MCP catalog expose 25 tools. This upstream
  metadata inconsistency is recorded rather than treating the old health
  list as authoritative.
- Scite documents that a premium subscription is required for its first-party
  plugin or connector. Programmatic MCP keys require the `mcp` scope, and
  optional datasets and full citation snippets depend on plan and license.
- Scite also states that commercial or research use of Search beyond
  evaluation requires a separate license agreement. Self-service keys can
  return redacted citation text through `snippetHidden`.
- Smart Citation classifications, registry records, patents, grants,
  clearances, labels, and spontaneous adverse-event reports are evidence
  inputs, not automatic proof of truth, causality, efficacy, incidence, legal
  status, or professional advice.
- A generic research-evidence icon is used because the official source
  repository and hosted documentation do not grant redistribution rights for
  the catalog logo.

The MIT license in this package applies only to the Ghast-authored adapter.
Scite's source skill repository has its own MIT license. Scite accounts,
subscriptions, hosted behavior, data, search licensing, collections,
permissions, citation model, trademarks, and terms remain controlled by
Scite and Research Solutions.
