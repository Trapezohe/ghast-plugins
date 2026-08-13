# docusign

Create, send, search, inspect, and automate Docusign agreements, envelopes,
recipients, dates, obligations, and Workflow Builder processes through
Docusign's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, a local loopback
OAuth compatibility bridge, safety instructions, setup documentation, catalog
metadata, and a generic icon. It does not copy or redistribute Docusign's
hosted MCP implementation, private Codex connector, OAuth credentials,
agreements, signatures, account data, branded icon, or marketplace artwork.

The official overview page-data response is pinned at SHA-256
`ee7baa0a1615e41a3f4ea932883d527f0c9e1ab5e92699754f72a69c6593626f` and the official OpenAI ChatGPT setup guide
at `0c1925822c08e4f1ba7d776a0bbc34db005f16ae036813eb802aa21ced92de1b`. Docusign's production ordered 22-tool
inventory and complete normalized schemas are pinned at
`dc9de26eddd7ec862946fc7e6bd609b3f101734d70e2652f2000a3395d74c7ed` and
`8d3bb21db1fb1ef261bead46d4e59314fa7123dc7d732cb63cad98d587b64624`. The demo ordered 35-tool
inventory and schemas are pinned at `16ad3b3322a9a8bcac402655d3dd10f1f7f666de88122d63290d9519d7068378` and
`f64203b8c7d1f0a213e5dfdaa51f4ffd83f9df7518344aa30223a0eaddea1764`.

The demo protected-resource and authorization-server metadata are pinned at
canonical JSON SHA-256 `bd92cd62509ac430ee0d81ac6cfccf633cca4452915dedd14a147a1e2855c1fa` and
`862196c4cd352e193efb8e950831ad8e564a81e4c5d511bcf55bc3312679b3a5`. Production is pinned at
`e0ae93ab64080e35b3dd782f2d58bb46df95406de516b75c3905a3bca099b6b4` and
`2c653b9e53f11c8b02b77c1ed6a32e257a0a21ceed46c6b2a821b85902bbe750`. The Codex capability evidence
is pinned to OpenAI plugin snapshot `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without
copying its private app identifier or artwork.

## Ghast compatibility

- Docusign requires a user-created Confidential Authorization Code Grant
  client with an Integration Key, Client Secret, and registered
  `http://localhost:3335/oauth/callback` redirect URI. Dynamic client
  registration is not supported.
- The credential values stay in a user-managed, permission-restricted JSON
  file referenced by `DOCUSIGN_OAUTH_CLIENT_FILE`; they are not stored in the
  plugin or passed directly on the process command line.
- Demo is the default. Set `DOCUSIGN_MCP_ENVIRONMENT=production` only with a
  production app and account. The environments use separate official MCP,
  authorization, data, credential, and token boundaries.
- The adapter requests `adm_store_unified_repo_read`, `aow_manage`, and
  `signature`, intentionally omitting demo app-key management.
- Docusign currently returns HTTP 403 instead of an OAuth 401 when no bearer
  token is present. A built-in localhost-only proxy injects an invalid
  sentinel only for that first unauthenticated request, allowing pinned
  `mcp-remote@0.1.38` to start Docusign's official OAuth flow. Real bearer
  tokens are then forwarded unchanged.
- Production's 14 read-only tools cover account context, envelopes,
  recipients, templates, users, Agreement Manager records and details, and
  Workflow Builder state. Eight Docusign-annotated destructive tools cover
  envelope creation and updates, recipient changes, reminders, and workflow
  trigger, pause, resume, and cancellation.
- This covers the Codex app's waiting-envelope summary, customer agreement
  status, recipient and key-date lookup, renewal and obligation extraction,
  contract creation and sending, and automated agreement workflows.
- Official documentation, both complete public tool catalogs and schemas,
  OAuth metadata, Codex capability evidence, pinned bridge package, and
  invalid-token OAuth trigger behavior were verified without a Docusign
  account. Authenticated tools/list and real account operations were not run.
- A generic agreement-signing icon is used because no redistributable catalog
  artwork is included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Docusign accounts, subscriptions, hosted service behavior, agreements,
signatures, permissions, trademarks, and terms remain controlled by Docusign.
