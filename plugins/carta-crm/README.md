# Carta CRM

Manage investors, companies, contacts, deals, notes, fundraisings, tasks, themes, reports, campaigns, files, and relationship context through Carta's official CRM skills and hosted MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/carta/plugins` at `daef48d9c7d110a1b3ea55d2b9bad3d19d079d75`.

Twenty-three workflow skills and their three HTML templates come from Carta's pinned v1.5.3 release. Ghast adapts only Claude-specific tool routing, removes unsupported hook-based telemetry, updates the two stale note workflows to Carta's current direct note tools, and adds one clearly labeled current-service safety and routing skill. Carta operates the hosted MCP service.

## Ghast compatibility

- The Codex private app connector is replaced by Carta's official public Streamable HTTP endpoint and browser OAuth.
- Carta's source skills use Claude's crm_call_tool dispatcher. Ghast maps those examples to the current direct MCP tool names documented by Carta.
- Carta's Claude hooks and local telemetry registry are not included. Ghast does not inject _instrumentation_v2 into tool arguments.
- The current official service documentation lists 143 direct tools, while the pinned skills reference 47 CRM operations. The added current-service skill routes the broader official surface without presenting Ghast-authored guidance as Carta-authored source.
- A generic CRM icon is used because Apache-2.0 does not grant Carta trademark rights and no separate catalog-artwork license was identified.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
