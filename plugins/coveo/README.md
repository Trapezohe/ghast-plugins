# coveo

Search authorized enterprise content, retrieve grounded passages, and
generate source-linked answers through Coveo's pinned official Labs MCP
implementation.

## Official source adapter

This package contains only a Ghast-authored launcher, safety instructions,
documentation, metadata, and a generic enterprise-search icon. It does not
redistribute Coveo source code, hosted implementation, OAuth client
credentials, API keys, indexed content, branded artwork, or marketplace
icons.

Coveo Labs' official `coveo-mcp-server` repository is pinned to revision
`d93b77ee3d1a53b8547adad431e8c6355bb85f23` with Git tree `2b9534586e817ff09189e40af245228ad957471b` and complete
audited source-inventory SHA-256
`6483ccc364bae642147e46005ec100ea962e5abddcdd9c6f3a88b42befb9cbc9`.
Critical source and dependency-lock files are independently hash-checked by
the generated launcher before execution.

The repository declares MIT in `pyproject.toml` but contains no LICENSE,
LICENSE.md, LICENSE.txt, COPYING, or NOTICE file at the pinned revision.
Ghast therefore does not copy or redistribute any upstream source. On first
run, the launcher clones the exact official revision into a local cache,
verifies its origin, revision, and critical hashes, installs only the frozen
runtime dependencies with Astral `uv`, and starts the source directly over
stdio.

Coveo's official product, hosted-server management, client-reference, and
ChatGPT setup documentation are pinned as normalized visible text at
SHA-256 `9b812db53c251698f2756836b0b7903ca21f5995626ee58a3855d1bc543ccaa2`, `0c675ab69739498e93fc74114c95b4bd53633278b309dbd6b05ed8c8a3d9773a`,
`2329b6a90bf2f7c0b2a538406afc398c84f846366a9390252c737827b686c6d0`, and `b0e032be201c7fd5ff6e842608b53f343ab38158fe3d752c52b5dedd0ca7c365`.

The hosted protected-resource and authorization-server metadata are pinned at
canonical JSON SHA-256 `2737b1fa85396573a760abb9daf892b8be9039bdab2b623be1c94be0b27d76d0` and
`fa329c67e2a41c2cb83bb64672e29cd5fa6300f1a66789d22574af0afecffe33`.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app mapping or artwork.

## Ghast compatibility

- Set `COVEO_API_KEY` and `COVEO_ORGANIZATION_ID`; optionally set
  `COVEO_ANSWER_CONFIG_ID` for Relevance Generative Answering. Git and Astral
  `uv` must be available on `PATH`.
- The official source exposes `search_coveo`, `passage_retrieval`, and
  `answer_question`. This covers the Codex plugin's enterprise-search
  capability and adds official passage retrieval and cited answer synthesis.
- The pinned `uv.lock` uses Python 3.12.3 and MCP 1.5.0. The source's broad
  dependency declaration can resolve to incompatible MCP 2.x releases when
  installed with plain `pip`; the launcher intentionally uses the verified
  frozen lock instead.
- The source's `__main__` module prints status text to stdout before opening
  stdio. The launcher invokes the official FastMCP server object directly so
  those lines cannot corrupt the MCP protocol.
- In an isolated frozen-lock audit, all 19 upstream tests passed. A manual
  stdio initialization and `tools/list` returned exactly the three documented
  tools.
- Coveo's current hosted MCP at `https://mcp.cloud.coveo.com/mcp` separately supports
  configurable Search, Fetch, Answer, and Passage Retrieval tools. OAuth
  metadata publishes authorization code, refresh tokens, PKCE S256, and
  `full` scope, but no dynamic registration endpoint.
- Coveo documents product-specific pre-registered OAuth clients, including
  separate ChatGPT and Claude client identifiers. Ghast does not reuse those
  identifiers or represent itself as one of those products; it uses the
  official API-key Labs implementation instead.
- On August 13, 2026, missing, invalid query-token, and invalid Bearer
  initialization requests to the hosted endpoint returned HTTP 401. No user
  login, token, organization data, source content, or reusable credential was
  obtained or retained.
- Authenticated searches, passage retrieval, generated answers, private
  source access, and real organization configuration were not exercised
  because no Coveo account or enterprise data was used.
- A generic document-search icon is used because no licensed Coveo
  marketplace artwork is redistributed.

The MIT license in this package applies only to the Ghast-authored launcher,
configuration, skill, documentation, metadata, and icon. Coveo accounts,
API keys, plans, indexed sources, service behavior, trademarks, privacy
policy, and terms remain controlled by Coveo and the applicable data owners.
