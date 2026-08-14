# waldo

Use Waldo's official hosted strategy MCP for brand, audience, category, ad,
social, feed, and workspace research.

## Official service

Waldo, operated by Curiosities, Inc., publishes an authenticated remote MCP at
`https://mcp.waldo.fyi`. Its official MCP documentation identifies
`https://mcp.waldo.fyi/strategy` as a separate curated endpoint for strategy
skills covering ad tools, social tools, feeds, and the user's Waldo workspace.
That focused official endpoint is configured here because it most closely
matches the Codex app's Strategy Agent and collected-signal description.

The endpoint supports browser OAuth with public dynamic registration and PKCE
S256. Waldo also documents scoped API keys for clients that do not support
OAuth. Authentication, subscriptions, workspaces, enabled tools, entity
activation, credits, and service availability remain controlled by Waldo.

## Capability comparison

- Codex: run a strategy agent, explore paid ads, brand mentions, audience
  conversations, trending topics, and data across team brand spaces through a
  private OpenAI app mapping.
- Ghast: connect directly to Waldo's official curated strategy MCP and use the
  live tool catalog with the user's own Waldo authorization.
- Waldo documents the strategy endpoint as a focused set of ad, social, feed,
  and workspace tools. Its broader official MCP and REST surfaces also cover
  brands, mentions, owned and paid media, audiences, categories, discovery,
  enrichment, workspace selection, usage, credits, and API-key management.

The Codex manifest's default prompt about "mobile test coverage" is unrelated
to Waldo's current brand-intelligence product and conflicts with the same
manifest's description. It is retained as audit evidence, not implemented or
represented as a Waldo capability.

## Usage and terms

Tracked brands, categories, and audiences generally refresh daily; discovery
and enrichment can query platforms live. Waldo meters usage by credits and may
charge an activation fee for entities it does not already track. Confirm scope
and potentially costly activation or broad analysis before invoking it.

Waldo's terms limit service access to authorized users, reserve Waldo IP, and
prohibit scraping, reselling, excessive automated access, circumvention, and
unlicensed copying or redistribution. Use the official MCP only through the
user's authorized account. Do not mirror the service or publish returned
proprietary data outside the user's rights.

## Verification and licensing

The importer pins the OpenAI marketplace evidence, Waldo's official MCP and
developer documentation, current terms, OAuth metadata, and the anonymous MCP
authentication boundary. Authenticated tools/list and data queries were not
run because no Waldo account was supplied.

The bundled MIT license covers only the independently authored Ghast endpoint
declaration, skill, metadata, documentation, and generic signal-research icon.
It does not license or redistribute Waldo's hosted implementation, data,
analysis, documentation text, private connector, credentials, responses,
logos, trademarks, or customer content.
