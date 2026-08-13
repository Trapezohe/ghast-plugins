# coupler-io

Analyze marketing, sales, finance, ecommerce, product, and other business data from Coupler.io data flows through Coupler.io's official hosted OAuth MCP and Analytical Engine.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/railsware/coupler-io-mcp-server` at `550ec75cb48bbbe0be286577b30c3a32f9bb0eea`.

Coupler.io's pinned MIT-licensed Railsware repository supplies the official self-hosted server source, manifest, documentation, and four-tool reference implementation. Ghast follows the same repository's recommendation to use Coupler.io's broader hosted OAuth MCP and adds one independently authored routing and safety skill; it does not redistribute the hosted service.

## Ghast compatibility

- The Codex private app connector is replaced by Coupler.io's official Streamable HTTP endpoint with browser OAuth, Dynamic Client Registration, a public client, and PKCE S256.
- The current hosted service documents 22 tools: ten data and analysis operations, two server-delivered skill operations, and ten feature-flagged guided data-flow setup operations.
- The official local server was also audited and passed all 25 tests, lint, and TypeScript compilation, but its four read-only tools are narrower than the Codex capability surface, so Ghast uses the hosted service by default.
- The README's general security section describes scoped read-only tokens while the remote catalog also documents refresh, metadata-update, and data-flow creation tools. Ghast therefore treats the live authenticated schema as authoritative and requires confirmation for every such operation.
- A generic multi-source analytics icon is used rather than Coupler.io marketplace artwork.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
