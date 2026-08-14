# S&P Global

Query S&P Global financial data through Kensho's official hosted MCP server
and use the official S&P Global agent skills for company tear sheets, funding
digests, and earnings previews.

## Official sources

This package is generated from two Kensho-controlled Apache-2.0 repositories:

- `spglobal-agent-skills` at revision
  `1d7d364a07d755d401b6f66d41affe71bc62a9b9`, which publishes the Codex
  manifest, hosted MCP declaration, and three workflow skills.
- `kfinance` release `v7.1.1` at revision
  `6700379c4026d99f986ead9aff849fa6b5b99d66`, which publishes the Python
  client, local MCP implementation, permission model, and ordered 37-tool
  catalog used to verify the public data surface.

The runtime connects directly to
`https://kfinance.kensho.com/integrations/mcp`. It does not reuse OpenAI's
private app ID or marketplace connector.

## Capability comparison

- Codex: natural-language access to S&P Capital IQ financials, transcripts,
  company information, financial statements, historical market data,
  securities, ratings context, peer comparisons, and research workflows.
- Ghast: the official hosted kFinance MCP surface for company-specific
  financial research plus the official tear-sheet, funding-digest, and
  earnings-preview skills.
- The current public kFinance source registers 37 tools spanning periods,
  companies, relationships, capitalizations, identifiers, earnings and
  transcripts, key developments, line items, prices, professionals, segments,
  statements, M&A, funding rounds, estimates, guidance, recommendations, and
  issuer ratings. The authenticated server filters tools by account
  entitlements.

This port is marked `partial`: the deterministic company-data capability is
official and directly usable, while the earnings-preview skill also requires a
separate Kensho Grounding `search` tool that is referenced by the official
skill but is not declared in the public plugin's MCP configuration. Broad
industry research should not be represented as available when that additional
service is absent.

## Authentication and use

An eligible S&P Global LLM-ready API or Capital IQ subscription is required.
The MCP client opens Kensho's browser authorization flow and applies the
authenticated user's entitlements. Accounts, trials, datasets, permissions,
quotas, and service terms remain controlled by S&P Global and Kensho.

Treat financial values as point-in-time data. Preserve returned periods,
currencies, units, identifiers, source links, and actual-versus-estimate
labels. Verify generated documents and calculations. This package provides
research tooling, not investment, legal, tax, accounting, audit, or valuation
advice.

The official skills are retained with minimal Ghast compatibility notes for
document and presentation tooling. `earnings-preview-beta` must stop when a
Kensho Grounding `search` tool is unavailable; it must not silently substitute
generic web search.

## Licensing and artwork

`LICENSE` is the Apache-2.0 license from the official agent-skills repository.
`KFINANCE_LICENSE` and `KFINANCE_NOTICE` preserve the corresponding official
kFinance notices used as implementation evidence. The generic chart-and-table
icon is independently authored for this package; no S&P Global, Kensho, or
OpenAI logo or marketplace artwork is redistributed.
