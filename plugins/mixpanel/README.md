# mixpanel

Analyze Mixpanel data and manage dashboards, Lexicon, data quality, experiments, feature flags, metrics, cohorts, and business context through Mixpanel's official skills and hosted MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/mixpanel/ai-plugins` at `2bde5a300d40afbc934ae74f44444744b80c09b6`.

Eleven non-install skill trees and the install skill's headless reference come from Mixpanel's pinned Apache-2.0 repository. Ghast adapts only the client-specific install skill, MCP setup reference, and engine guide, and adds a small slash-command router. The official hosted MCP server remains operated by Mixpanel.

## Ghast compatibility

- The Codex private app mapping is replaced by Mixpanel's official US, EU, or India hosted MCP endpoint through pinned mcp-remote@0.1.38 and dynamic OAuth registration.
- MIXPANEL_MCP_REGION selects us, eu, or in from a strict allowlist; US is the default.
- OAuth is the default. For non-interactive use, MIXPANEL_MCP_SA_TOKEN may contain only the base64 encoding of the official service-account username:secret pair. The bridge constructs the required header inside the child process and never inserts the secret into argv.
- Mixpanel's current official MCP documentation lists 63 tools across analytics, dashboards, discovery, Lexicon, data quality, custom properties, cohorts, lookup tables, metrics, session replay, experiments, and feature flags.
- A generic analytics icon is used because the official AI plugin repository does not publish a catalog icon.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
