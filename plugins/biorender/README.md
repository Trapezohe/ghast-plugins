# biorender

Search BioRender templates and accessible figures, preview results, and
create editable scientific figure drafts through BioRender's official hosted
MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, catalog metadata, and a generic scientific
figure icon. It does not copy or redistribute BioRender's hosted MCP
implementation, private Codex connector, service source code, templates,
icons, user figures, OAuth credentials, branded artwork, or marketplace icon.

BioRender's official Help Center article is pinned at article ID
`37237276158109`, update timestamp
`2026-08-05T17:54:58Z`, and body SHA-256
`fb87519f40227b34b0a6743ec4dfc92f0e02581a4919adeba14e3029da4c7f2e`. The article documents public-template
search, personal and shared figure search, AI figure generation, previews,
editable BioRender links, plan restrictions, AI-credit consumption, and the
connector's data-sharing boundary.

The official service's authorization-server metadata is pinned at canonical
JSON SHA-256 `7e351acc74e9958aa68ce8ce61a815aaf5b93f7d37dbc4cd455ce2113cd74fe5`. Anthropic's client declaration
for the BioRender connector is pinned at revision
`e96556b637b56d6cc3a5ad33987009be9e60aa5c` and file SHA-256
`3da37488e11aee541992c12743f3ea9cae99df7d56843427a86194e625881e74`; it identifies BioRender as the author
and declares `https://mcp.services.biorender.com/mcp`.

Codex capability evidence is pinned to OpenAI's plugin snapshot revision
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying the private connector ID or
marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://mcp.services.biorender.com/mcp` using Streamable HTTP and
  BioRender browser OAuth.
- The OAuth server declares authorization-code and refresh-token grants,
  Dynamic Client Registration, confidential clients using
  `client_secret_post`, and PKCE S256.
- On August 13, 2026, an unauthenticated MCP initialize request returned HTTP
  401 with BioRender's authorization metadata challenge. One disposable
  loopback client registered with HTTP 201 and the authorization endpoint
  accepted its PKCE request. The registration response provided no management
  URI or access token, so the audit client could not be deleted through the
  standard registration-management protocol.
- The official hosted service covers the Codex GLP-1 template-search workflow
  and expands it with personal and shared figure search plus AI-generated
  first drafts that open in BioRender for continued editing.
- BioRender does not publish the hosted server source, a complete tool
  inventory, or tool schemas. Authenticated tools/list, private figure access,
  and AI generation were not run because no user BioRender account or credits
  were used during the audit.
- The included skill separates public templates from private files, protects
  unpublished and sensitive science, discloses AI-credit use and data sharing,
  requires scientific review of generated figures, and confirms any live
  mutation or sharing operation.
- A generic scientific-figure icon is used because BioRender's catalog artwork
  and scientific asset library are not licensed for redistribution by this
  adapter.

The MIT license in this package applies only to the Ghast-authored adapter.
BioRender accounts, subscriptions, hosted service behavior, templates, icons,
figures, AI credits, permissions, publication rights, trademarks, privacy
policy, and terms remain controlled by BioRender.
