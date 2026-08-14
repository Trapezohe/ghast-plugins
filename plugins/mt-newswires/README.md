# mt-newswires

Search and retrieve licensed real-time North American and global financial
news from MT Newswires through its officially authorized viaNexus MCP service.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, catalog metadata, and a generic icon. It does not
copy or redistribute the private Codex connector, MT Newswires articles,
viaNexus service source code, credentials, branded artwork, or marketplace
icons.

MT Newswires' official AI page is pinned at normalized visible-text SHA-256
`d0dbbb14e493acbd13456817ea050397d4f5fc51c262c349908f09627a2a0f4e`. Its official January 22, 2026
viaNexus distribution announcement is pinned at SHA-256
`a154b567803f30739d29e8ab44e07f45e56ccc43242f7fd3e999f67f42baf9c9`. The current vAST
documentation is pinned at SHA-256 `71195676026d8e301b6438bee8acf0cf7d8f18465b55a215898683370d500cf6`.

The protected-resource and authorization-server metadata are pinned at
canonical JSON SHA-256 `d7f7d5f2df32a3c5efc40e5cef86812d8e66b88d9e2bb511ee3dce66ebca5634` and
`52a9e2c6554a753736ae62dfa241debc0819438433cea11945a45f83c6319732`.

## Ghast compatibility

- Ghast connects directly to `https://vast.blueskyapi.com/mtnewswires/mcp` using Streamable HTTP
  and viaNexus OAuth 2.0 with PKCE.
- The dedicated endpoint is news-only and documents two MCP tools, `search`
  and `fetch`, with server-side `EDGE:MT_NEWSWIRES*` entitlement enforcement.
- The verified public workflow covers North American and Global real-time
  headlines, symbol-based search, story retrieval, earnings, M&A, analyst,
  sector, macroeconomic, central-bank, FX, commodity, and crypto news
  research subject to the live authenticated schema and subscription.
- This covers the Codex connector's core MT Newswires news workflows. The
  included skill makes one boundary explicit: the news service can support
  reasoned impact analysis, but actual price movement requires independent
  market data.
- Anthropic's Apache-2.0 financial-services repository still records the old
  `https://vast-mcp.blueskyapi.com/mtnewswires` route at revision
  `38652224c10610fa52eee2acee3ac712dcff01f2`. That route returned HTTP 404 on
  August 14, 2026, so this adapter uses the current endpoint documented by
  viaNexus.
- A one-time disposable RFC 8252 loopback registration returned HTTP 201 on
  August 14, 2026. The non-secret response-shape subset has SHA-256
  `0acd6c03d06cb2a08e8974db5bedab8b9c7e8679020316b1c03f845e0ae52c45`. The importer does not repeat
  registration because the response supplied no management credential for
  deleting the client.
- A generic financial-news icon is used because no licensed catalog icon is
  included in a public official source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
MT Newswires and viaNexus accounts, subscriptions, hosted services, content,
data rights, permissions, trademarks, and terms remain controlled by their
operators.
