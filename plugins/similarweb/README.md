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
`b3970ea5dd3348773500820d6d5d63d5b878d038155f02c68b276313242f4073`. The current Claude integration guide has SHA-256
`228a7abde362e0a923a4ab299dbd688e994153ad02305668b64b1054bcc241ac`. The official OAuth protected-resource
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
- A generic market-analytics icon is used because no licensed catalog icon is
  included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Similarweb accounts, subscriptions, data credits, hosted service behavior,
datasets, permissions, trademarks, and terms remain controlled by Similarweb.
