# similarweb

Research website traffic, acquisition channels, referrals, audiences,
keywords, competitors, industries, mobile apps, and shopper intelligence
through Similarweb's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute Similarweb's hosted MCP implementation, proprietary datasets,
private Codex connector, or marketplace artwork.

The adapter is pinned to Similarweb's official MCP overview. Its SHA-256 is
`eac1d71df3350d455fcdd7d793ae7c6a1a1029fe43cc3a170bd6474ed0c6e816`. The current Claude integration guide has SHA-256
`aa84c3a66647dca14f6a78172176a1e731e4ff5cad092547a909bb148c36679a`. The official OAuth protected-resource
metadata is pinned at SHA-256 `4f4e48ae9c754ff1c1a31371be71d27738437576e8d6a668cd7b627e360978a7`. The
authorization-server metadata is pinned at SHA-256
`537ef1981b3bb69036da41c59f4c9e1da74c84d652aa21e3e3bfaad7005db480`.

## Ghast compatibility

- Ghast connects directly to `https://mcp.similarweb.com` using Streamable HTTP and
  Similarweb OAuth with dynamic client registration and PKCE. The service also
  accepts an API-key header as a client-managed alternative.
- Similarweb documents 75+ data endpoints spanning web traffic and engagement,
  channel mix, referrals, rankings, audiences, demographics, keywords, SEO,
  mobile-app intelligence, competitive analysis, and Amazon shopper data.
- This covers the Codex app's traffic-trend comparisons, acquisition channels,
  referring sites, audience geography, search keywords, app intelligence, and
  industry benchmarking, with additional official datasets where subscribed.
- Data access and historical coverage mirror the user's Similarweb API plan,
  and requests consume the same data-credit allocation as REST API calls.
- Brand logo source: https://avatars.githubusercontent.com/u/6529581?v=4. Brand names and logos belong to SimilarWeb. 品牌名称与标识归对应服务商所有。

The MIT license in this package applies only to the Ghast-authored adapter.
Similarweb accounts, subscriptions, data credits, hosted service behavior,
datasets, permissions, trademarks, and terms remain controlled by Similarweb.
