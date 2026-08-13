# clay

Search companies and people, enrich prospect records, and run
administrator-approved GTM functions through Clay's official hosted MCP.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, metadata, and a generic prospect-research icon.
It does not redistribute Clay's hosted implementation, private Codex
connector, OAuth credentials, customer data, official agent-plugin skills,
hooks, CLI wrapper, binaries, branded artwork, or marketplace icon.

Clay's official MCP product-page core is pinned as normalized visible text
with SHA-256 `99faa3c0f6c5c87017292b8f92cb114c057a32cd858da0f863fe1c984c0418f5`. Global navigation, promotional
banners, customer stories, and the footer are excluded. The official
connection guide, security guide, and FAQ remain pinned as normalized visible
text with SHA-256 `52d04c63c45b9bbc09001cd99eb4a05cfd9a78b19ec076c1d95b12cafc9ee8e9`,
`28914f9149135b4a559230cd40cf90176097e4d6e12c26109a9076d6f8181ca2`, and `7a968287f91c9c9a270f3a44fb544317e0780d3a1a0f8d38d56e7d10ef681ca9`.

Clay's official developer-document index plus five Markdown guides are pinned
in `scripts/import-official-hosted-plugins.py`. The current index and
Quickstart no longer publish the former standalone local MCP guide, while the
latest official agent-plugin revision still configures `clay mcp`. Clay's
public OpenAPI is pinned at raw and canonical SHA-256
`258cc399172d40533db4d88844a80b86d804cc4b58f0224169fa2aa076827f0e` and `a95679fb7672d8d0fae3ad073f96378e273bc3532ea7fb4d416b2aa9ed4add3a`. Its ordered
13-operation inventory is pinned at `f5ef66a96b381f0e26e6ed99d846fa73e7b1ec6d62d41ad91b5e806d959838c2`.

The OAuth protected-resource and authorization-server metadata are pinned at
canonical JSON SHA-256 `f114e17a4bc5a52dec7580042a865cdab90c2b1bd60f2f14def6d3c86d532d45` and
`09ef6e27492c1b3b1d34f0477b388095a39380ed1dda9bfcbbb7c0af1014fc8b`.

Clay's official `clay-run/agent-plugins` repository is pinned to
`4ab1ca54c908e04b52123234405e1bb1aac4199a` with Git tree `37f207938630ea88e7e3b45c78540bf665f02aab`. It contains 21
workflow skills plus the official Codex manifest, hooks, CLI wrapper, and
pinned CLI v0.3.0 checksums. The repository has no LICENSE, LICENSE.md,
LICENSE.txt, COPYING, or NOTICE file at that revision, so none of those files
is redistributed.

Codex marketplace capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app ID or artwork.

## Ghast compatibility

- Ghast connects directly to `https://api.clay.com/v3/mcp` over Streamable HTTP and uses
  Clay browser OAuth. Clay publishes authorization-code, refresh-token, and
  device-code grants, dynamic registration, public clients, and PKCE S256.
- The hosted service exposes built-in find-and-enrich tools,
  administrator-enabled Functions, and plan-dependent Audiences data. Clay
  states that the same tools and Audiences capabilities are exposed across
  supported AI platforms, subject to platform and workspace policy.
- Official product and developer documentation covers company and people
  search, work email and phone enrichment, role and firmographic context,
  technology, hiring, funding, news, custom Functions, scoring, routing,
  enrichment waterfalls, CRM write-back, sequences, and reusable GTM logic.
- This covers the Codex workflows for finding ICP-matching Clay records,
  enriching leads with company, role, and outreach context, and building a
  prospecting list with useful signals.
- Clay documents people and company search as free. Live enrichment and
  Functions can consume credits or actions; administrators can set spend
  limits and credit budgets. The included skill discloses material spend and
  requires confirmation before paid work.
- OAuth is scoped to one user and one workspace. Administrators choose
  allowed MCP clients, enable individual Functions, control Audiences access,
  and set budgets. The skill does not treat availability as authorization.
- The public REST OpenAPI currently contains five GET and eight POST
  operations for identity, asynchronous routine results, routine and batch
  execution, structured and advanced search, filter or query references, and
  Enterprise table queries.
- On August 13, 2026, missing and invalid Bearer initialize requests returned
  HTTP 401 with Clay's official protected-resource challenge and identical
  body SHA-256 `7fe66b771b819e775f5b2e6afec58137720fd541f049f8569e10a75e3d0d0d2a`.
- A disposable loopback public client registered with HTTP 201, no client
  secret, authorization-code and refresh-token grants, and `mcp` scope. A
  PKCE request reached Clay's official browser authorization page. No user
  sign-in, authorization code, token, account data, or reusable credential
  was retained.
- The official CLI v0.3.0 Darwin arm64 binary downloaded through Clay's
  checksum-verifying wrapper matched SHA-256
  `7155da2313a1fa1e65c6d862cfd2f3f25ee61f2c90e18318a8a076860f8ce265`.
  Without a user session, `clay mcp` correctly returned `auth_required`
  before exposing tools.
- Authenticated tools/list, workspace Functions, Audiences data, searches,
  paid enrichment, CRM writes, sequence pushes, and outreach were not
  exercised because no Clay account or prospect data was used.
- A generic prospect-research icon is used because no licensed Clay catalog
  artwork is redistributed.

The MIT license in this package applies only to the Ghast-authored adapter.
Clay accounts, plans, credits, hosted service behavior, prospect and customer
data, provider licenses, workspace permissions, trademarks, privacy policy,
and terms remain controlled by Clay and the applicable providers.
