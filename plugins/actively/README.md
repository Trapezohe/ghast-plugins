# actively

Research and prioritize accounts using Actively's persistent Per-Account
Agent intelligence, buying signals, prospect context, strategy, and
next-best actions.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute Actively's hosted MCP implementation, private Codex connector,
service source code, customer data, or marketplace artwork.

The adapter is pinned to Actively's official MCP product evidence with
canonical JSON SHA-256 `3c7c7f1750eebd00dac261f987ae394b931da7ccbf4b24bdc3d97fddf1adc95c` and its official API
product evidence with canonical JSON SHA-256
`e090dc2a687e70ef0d829f2b8d4ab10b5845e4de926b59e8d632de329daf888d`. The official OAuth protected-resource
metadata is pinned at canonical JSON SHA-256
`908b8114e7a62b7ce79e87afb6a6bcaa90077e19ed928b0496af017e28d1369c` and the authorization-server metadata at
`11a7486ac6ab10e707d1189cbaa61ca5c52a514cebfe1cc505971261ae96abd4`.

## Ghast compatibility

- Ghast connects directly to `https://api.actively.ai/mcp` using Streamable HTTP and
  Actively OAuth. The service declares dynamic client registration,
  authorization-code, refresh-token, and device-code grants, public clients,
  and PKCE S256.
- Actively's official product pages describe account research, strategy,
  persistent memory and reasoning, continuously maintained GTM intelligence,
  next-best actions, and context for CRM, Slack, dashboards, ChatGPT, Claude,
  Cowork, and custom agents.
- This matches the Codex app's published high-fit account, buying-signal,
  prospect-context, ICP prioritization, meeting-preparation, deal-strategy,
  and territory-prioritization use cases at the product capability level.
- The public documentation does not publish tool names or schemas.
  Unauthenticated endpoint discovery, OAuth metadata, dynamic registration,
  and authorization-page startup were verified, but authenticated tool
  listing and account-data operations were not run.
- The included skill treats CRM, email, call, and external-signal data as
  sensitive and untrusted, requires evidence-backed rankings, and guards any
  state-changing tool that an authenticated workspace may expose.
- A generic account-intelligence icon is used because no licensed catalog
  artwork is included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Actively accounts, provisioning, hosted service behavior, customer data,
permissions, trademarks, and terms remain controlled by Actively.
