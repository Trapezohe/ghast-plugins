# morningstar

Use Morningstar's official hosted MCP for authorized fund and ETF screening,
summaries, comparisons, datapoint discovery, analyst research, holdings, and
Morningstar Medalist analysis.

## Official hosted service

Morningstar publishes `https://github.com/Morningstar/morningstar-plugins` from its official GitHub
organization. The pinned repository identifies `https://mcp.morningstar.com/mcp` as the Morningstar
MCP endpoint, requires a Morningstar Direct subscription, and contains five
official workflows: fund screening, fund summarization, fund comparison,
datapoint discovery, and Medalist rating analysis.

Ghast connects directly to that official endpoint using the customer's own
Morningstar authorization. Live OAuth metadata supports authorization code,
refresh tokens, PKCE S256, dynamic registration, and confidential clients. On
August 20, 2026, one disposable loopback client registered with HTTP 201 and
received a client secret. No client value, secret, authorization code, token,
login, or account data was retained.

## Independent adapter boundary

The official repository declares MIT in its manifest but contains no LICENSE,
COPYING, NOTICE, or equivalent license text. This package therefore copies none
of its five skills, detailed workflows, scripts, HTML templates, report styles,
rating icons, logos, fonts, manifests, or documentation. It independently
provides only a factual endpoint declaration, Ghast-owned workflow and safety
guidance, metadata, documentation, and a generic fund-research icon.

The bundled MIT license covers only these independently authored adapter files.
It does not license Morningstar's hosted implementation, official plugin
materials, methodologies, research, data, reports, ratings, trademarks,
credentials, customer content, or service responses.

## Capability comparison

- The Codex snapshot bundles fund screening, single-fund summaries, and
  side-by-side fund comparison through a private OpenAI app mapping.
- The current official Morningstar source adds datapoint discovery and
  Medalist rating analysis and points directly to the public hosted MCP.
- Ghast uses that same official service and independently covers all five
  documented workflows, including accessible Markdown or independently styled
  HTML reporting when requested.

Authenticated tools and licensed data calls were not run during the audit
because no user Morningstar Direct account was supplied. Exact schemas, data
coverage, quotas, ratings, disclosures, and entitlements remain controlled by
Morningstar and the customer's contract.
