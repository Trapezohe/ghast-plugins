# semrush

Retrieve read-only SEO, keyword, backlink, traffic, audience, market, paid
search, shopping, site audit, position tracking, and project data through
Semrush's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, and catalog metadata. It does not copy or redistribute
Semrush's hosted MCP implementation, proprietary data, or private connector.

The adapter is pinned to Semrush's official current MCP documentation with
SHA-256 `2508d6192982bd86eb524a5605e7367f6c9186e600e808d4d633d5627e5de25c`. The version-2 OAuth protected-resource
metadata is pinned at SHA-256 `5d0b459a41d7ae3596cc2c72b480888d3dd7fa85a3fb32dd1282e89e2840f1be`, and the
authorization-server metadata is pinned at SHA-256
`4e70ad04ad9ce53dcc59818a702f197d5c521c3b7e4f967111814e41b35871e3`.

## Ghast compatibility

- Ghast connects directly to `https://mcp.semrush.com/v2/mcp` using Streamable HTTP and
  Semrush OAuth. API-key authentication remains an optional client-managed
  fallback.
- The 14 documented tool entry points cover domain, organic, keyword,
  competitor, backlink, audience, traffic, paid search, shopping, position
  tracking, site audit, and project discovery plus schema lookup and report
  execution.
- This covers the Codex app's domain analytics, keyword metrics, backlink
  profiles, traffic channels and history, geographic and demographic data,
  and competitive or market indicators.
- The service is read-only: Trends and SEO APIs are available according to
  subscription, and only read methods are exposed for Projects API v3.
- A generic web-analytics icon is used because no licensed catalog icon is
  included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Semrush accounts, subscriptions, API units, hosted service behavior, data,
permissions, trademarks, and terms remain controlled by Semrush.
