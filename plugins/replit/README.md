# replit

Create, find, inspect, explain, update, publish, and check the publish status
of Replit Apps through Replit's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute Replit's hosted implementation, native connector, Agent code,
app source, account data, secrets, databases, or marketplace artwork.

The adapter is pinned to Replit's official direct-client documentation with
SHA-256 `8391016162ecef084f30546fbb55f5e2f179f52f87fb7d67e192609df65b1ce4`. Replit explicitly documents
`https://replit-mcp.com/server/mcp` for Codex and other Streamable HTTP clients and says not to
add a bearer token, custom headers, or a custom OAuth server.

The OAuth protected-resource metadata is pinned at canonical JSON SHA-256
`41b41e6b0d6d9a7f73fde4d2e772d649f82744bc2dd54d7d92f6935fac3b7996` and the order-normalized authorization-server
metadata at `dfe20c56545aad3736e4e007ddfcd7551b7f4f445db73ff846fc70ac57b023e0`.

## Native connector comparison

- Replit's unauthenticated native ChatGPT/Codex endpoint negotiated MCP
  `2025-06-18` and exposed eight user-visible tools plus three app-only widget
  tools. The direct-client documentation lists the same eight user workflows.
- The sorted user-visible names have SHA-256
  `a32202cfa25aba7164d82ea3234142f74f0c33eea3ab7bd8eebba6b946e5a9c9`, their annotations have canonical JSON
  SHA-256 `a335c94f380f000186605e9e16c7f0571eb6ca7e205718c377743cc725cdcb98`, and their complete name,
  description, input, annotation, execution, and output-schema inventory has
  SHA-256 `6c682a9cf3ef23d5b360432d9531f3d7986d01804d65ab252640e3da2d45075d`.
- The native server instructions have SHA-256
  `93868a13f251a22bf6315568a8f3e8807e07782c1b20f74aad2ca945355b91a8` and describe the same create or find,
  inspect or ask, update, repeat, publish, and publish-status workflow.
- The three app-only widget tools support Replit's embedded preview UI and are
  intentionally absent from the public direct-client catalog. They are not
  user-callable app-management capabilities.

## Ghast compatibility

- Ghast connects directly to `https://replit-mcp.com/server/mcp` using Streamable HTTP and
  Replit OAuth. Dynamic registration returned a public client with
  authorization-code and refresh-token grants and PKCE S256.
- The eight tools create a new app from a natural-language prompt; search,
  resolve, and list editable apps; ask Replit Agent read-only questions about
  codebase behavior and debugging; apply natural-language changes; publish or
  republish; and check publish status and public URL.
- This directly matches the Codex connector's app creation, recent-project
  discovery, app explanation, iterative development, publishing, and
  deployment-status workflows. The native tool schemas themselves were used
  for the comparison, not only the marketplace description.
- Replit requires the chat response to avoid raw code, file contents, file
  paths, configuration, and terminal commands. The included skill preserves
  that boundary and directs implementation inspection to the Replit UI.
- Remixing an existing app can copy secrets and database contents when the
  user has the relevant access, but it does not copy connected integrations.
  The skill requires a specific warning and confirmation before creation.
- Updates are marked destructive. Creation, updates, and publishing start
  asynchronous work and must not be blindly retried. Publishing may use
  public visibility for personal apps, while workspace apps default private.
- Endpoint discovery, OAuth metadata, DCR, direct-endpoint authentication
  behavior, native initialization, native user-visible schemas, and public
  documentation were verified without a Replit account. Authenticated app
  listing, Agent execution, creation, update, and publishing were not run.
- A generic app-builder icon is used instead of Replit marketplace artwork.

The MIT license in this package applies only to the Ghast-authored adapter.
Replit accounts, plans, Agent behavior, hosted services, app data, secrets,
databases, deployments, usage charges, permissions, trademarks, privacy
policy, and terms remain controlled by Replit.
