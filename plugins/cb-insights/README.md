# cb-insights

Research private companies, markets, deals, competitors, predictive signals,
market maps, and investment questions through CB Insights' official hosted
MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, research-safety
instructions, documentation, catalog metadata, and a generic market-research
icon. It does not copy or redistribute CB Insights' hosted implementation,
private Codex connector, proprietary data, deprecated example source, account
credentials, official logo, or marketplace artwork.

The official MCP documentation core is pinned at normalized visible-text
SHA-256 `97e8c8b7ecf4600250a857275fe09764c81b09d4a27b0584a4828db29f7da9fd`. The current ChatCBI request,
multi-turn, response, and error contract is pinned at normalized visible-text
SHA-256 `92d179a62a18ead5f5c2482414c377c093162be4a85afff50a8b9bc8d17a4897`. The official product-integration
statement is pinned at normalized visible-text SHA-256
`6ce534ffa0e9e61e8c3d1f155be8eb70cbba588f592b19d73e50367b139a081f`.

The OAuth protected-resource metadata is pinned at canonical JSON SHA-256
`7f4d1f126334b7302fc61845eac5d7ec703f7ec940513d312e4123b445a7b5c7` and the authorization-server metadata
at `665a68402114da758382adaf85c731ce32365df30584451b19c8045f1b64be75`.

CB Insights' public `cbi-mcp-server` repository is pinned to
`778e1acb6a749852a82b101b99a701d9c9c1ce68`. Its January 2026 notice deprecates that
self-hosted pass-through example in favor of `https://mcp.cbinsights.com/`. The
repository has no LICENSE, LICENSE.md, LICENSE.txt, COPYING, or NOTICE file at
the pinned revision, so none of its source is redistributed.

Codex marketplace capability and developer evidence is pinned to OpenAI
plugin snapshot `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private
app ID or official artwork.

## Ghast compatibility

- Ghast connects directly to `https://mcp.cbinsights.com/` over Streamable HTTP
  using CB Insights browser OAuth. The service declares dynamic client
  registration, authorization-code and refresh-token grants, public clients,
  and PKCE S256.
- Official ChatCBI documentation supports standard and chunked research,
  multi-turn conversations through `chatID`, Markdown answers, source links,
  related content, suggestions, and explicit error responses.
- Official product and Codex evidence covers company sourcing, private-market
  research, market maps, investment memos, competitor monitoring, deals,
  predictive signals, taxonomies, scores, and technology research.
- This independently authored skill preserves sources, separates evidence
  from inference, highlights missing and contrary evidence, and requires
  verification of material generated claims.
- On August 13, 2026, missing and invalid Bearer initialize requests returned
  HTTP 401 with identical body SHA-256
  `8599a03b4c1d788236014f851ec320b3ad4a589c59e8c1ea045dd4d052291cce` and the official protected-resource
  challenge.
- Initial protocol checks registered loopback public clients with HTTP 201, no
  client secret, authorization-code and refresh-token grants, and OpenID
  profile scopes. A PKCE authorization request reached CB Insights' official
  consent page. The server returned no registration management URI, so the
  importer does not repeat registration. No sign-in, token, account data, or
  reusable credential was retained.
- Authenticated tools, subscription data, company profiles, deals, signals,
  research, and ChatCBI responses were not accessed because no CB Insights
  account or private-market data was supplied.
- A generic market-research icon is used because the official marketplace
  logo is not included in redistributable licensed material.

The MIT license in this package applies only to the Ghast-authored adapter.
CB Insights accounts, subscriptions, hosted service behavior, proprietary
data, generated responses, permissions, trademarks, privacy policy, and terms
remain controlled by CB Insights.
