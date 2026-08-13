# Catalyst by Zoho

Build, deploy, and operate Catalyst by Zoho applications with official service, SDK, CLI, architecture, pricing, and Zoho MCP skills across eight supported data centers.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/catalystbyzoho/codex-plugin` at `4cfbca7041b14ffa874488cd9b0ba88970cd168f`.

All 16 official skill trees and their 37 reference files come from Catalyst by Zoho's pinned Codex plugin repository. Ghast replaces the OpenAI private app mapping with Zoho's official Global MCP endpoints, adapts only client-specific setup text, and preserves the developer's safety and project pre-flight rules. The hosted MCP service remains operated by Zoho.

## Ghast compatibility

- CATALYST_MCP_REGION selects us, eu, in, au, ca, sa, jp, or ae from a strict allowlist; US is the default.
- The bridge runs pinned mcp-remote@0.1.38 with HTTP-only transport and uses Zoho's browser OAuth, public dynamic client registration, refresh tokens, and PKCE S256.
- Ghast does not support the source SessionStart hook. The ported readiness guidance therefore reads .catalystrc and catalyst.json explicitly before project mutations, while CLI and runtime prerequisite checks run only when relevant.
- The authenticated Global MCP surface is dynamic: four ZohoMCP meta-tools enumerate and execute the available CatalystbyZoho operations. Account, data-center, project, service, and plan entitlements determine the live catalog.
- A generic cloud-development icon is used so the package does not imply trademark rights in Zoho's official logo.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
