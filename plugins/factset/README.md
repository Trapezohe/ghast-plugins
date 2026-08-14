# factset

Connect financial data, analytics, and licensed research through FactSet's
official hosted MCP and official REST APIs.

## Official sources

The hosted MCP endpoint is `https://mcp.factset.com/content/v1`. FactSet's current public product page
publishes 20 tools for fundamentals, debt, estimates, prices, ownership, M&A,
people, events, entity reference, funds, screeners, unstructured content,
metrics, private markets, GeoRev, supply chain, RBICS, and fixed-income terms.
The canonical product JSON SHA-256 is `248bd4b02bb48df52db939ff4e0d8200bb62f0ca6ee654bc74d02d4ddf88967c` and the ordered
tool-name SHA-256 is `e11b82c355b2f2a94f0cd88c1397792c65d4dbfd6f2582661232cd64bc1cf6a6`.

The official `factset/enterprise-sdk` repository is pinned to
`36c67dfb8ff2b9893d0f8822ecb5d62abd30dc3f` with tree `970e0ff5a53917234d0581783c04ac2fb8f18d60` and Apache-2.0 licensing.
Its Investment Research 1.0 and Security Explanation 1.6 specifications have
SHA-256 values `1830c8c758109e55372452eefd6c8e142079e8c1d6be7eebaaacae1022a7b870` and
`281dff322a66ba5b262df6f966474af1d1503d206ba8b207b457917480fb24fd`.

The bundled standard-library adapter has SHA-256 `1640c4073152866e095891b510ae8077850c7277b4306fe678b416ab71c7f572`. It calls only
the official Investment Research and Security Explanation endpoints, accepts
existing bearer or API-key credentials from the environment, performs no
automatic retries, and does not download research documents.

## Capability comparison

- Codex: consensus estimates and recent prices, peer margin/growth/valuation
  comparisons, and recent broker research headlines with sentiment through a
  private FactSet app connector.
- Ghast MCP: the same estimates, price, fundamentals, valuation, screening,
  entity, ownership, event, transcript, news, private-market, supply-chain,
  fund, and fixed-income product surfaces through FactSet's official hosted
  MCP and browser OAuth.
- Ghast API adapter: exact broker research headlines, contributors, analysts,
  dates, categories, rating/target/weighting actions, entitlement-aware links,
  and FactSet Security Explanation with optional broker summaries.

The broker-research API supplement is important: the public MCP catalog names
StreetAccount News, CallStreet transcripts, and filings under unstructured
content, but does not name investment research. Ghast does not mislabel news
as broker research.

## Authentication and licensing

Hosted MCP authentication uses FactSet browser OAuth. The canonical protected
resource and OIDC metadata SHA-256 values are `446c80d9c18385005dc67d81fbcee89d248d4b117eddaab38dd3a69e2f1425c0` and
`b8e63e5e699e31197a954e529437ffff13a2fa45b344939f71a27477bc66410b`. Anonymous initialization and anonymous API probes return the
expected HTTP 401 `Authentication Failed` boundary.

The REST adapter accepts `FACTSET_ACCESS_TOKEN`, or
`FACTSET_USERNAME_SERIAL` plus `FACTSET_API_KEY`. A FactSet account,
subscriptions, dataset and contributor entitlements, API access, OAuth
approval, and service limits remain customer-managed. Authenticated calls were
not executed during import because no customer account was supplied.

The Apache-2.0 license covers the official SDK license copied into this
package and the Ghast-authored adapter, workflow, documentation, and generic
financial-research icon. FactSet services, data, reports, trademarks, customer
content, and commercial terms remain controlled by FactSet and contributing
publishers.
