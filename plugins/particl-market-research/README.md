# particl-market-research

Research ecommerce companies, products, variants, sales, marketing assets,
events, pricing, and market trends through Particl's official hosted MCP.

## Official service

Particl publishes `https://mcp.particl.com/mcp` for ChatGPT, Claude, Cursor,
VS Code, and other MCP clients. Its current public tool reference lists 17
read-only tools covering company discovery, taxonomy, credit balance, company
details and catalogs, product details and variants, product mix, sales
timeseries, marketing assets and stats, retail events, top products and
companies, pricing analysis, and market sales.

The official documentation and OAuth metadata are pinned by
`scripts/import-particl-plugin.py`. On August 14, 2026, anonymous
initialization returned HTTP 401 with the official protected-resource
challenge. Dynamic public-client registration accepted a loopback callback,
required no client secret, advertised PKCE S256, and routed authorization to
the official Particl account sign-in page.

## Capability comparison

- Codex: company discovery, catalog and product research, variant analysis,
  market leaders and trends, marketing assets, retail events, sales
  timeseries, and product-mix breakdowns through a private app connector.
- Ghast: all 17 currently documented official Particl MCP tools over the
  public hosted endpoint, using standard OAuth and account-scoped access.
- Ghast adds explicit credit estimates, bounded-query rules, retention
  warnings, source-quality guidance, and internal-use restrictions.

## Authentication, licensing, and privacy

A Particl account, eligible plan, export credits, dataset access, OAuth
approval or dashboard API key, and service limits remain customer-managed.
Most tools consume credits per row, call, or data point.

The MIT license in this package covers only the Ghast-authored endpoint
declaration, workflow, metadata, documentation, and generic ecommerce
research icon. It does not license or redistribute Particl's hosted server,
data, private connector, credentials, web application, documentation, logos,
marketing assets, product images, reviews, or third-party content.

Particl's current privacy policy says MCP tool parameters and outputs are
processed and usage, tool-call, and HTTP logs may be retained indefinitely.
Do not place confidential or unrelated proprietary information in requests.
