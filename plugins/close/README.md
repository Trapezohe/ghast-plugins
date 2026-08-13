# close

Search, analyze, create, and explicitly update Close CRM leads, contacts,
opportunities, activities, tasks, pipelines, workflows, templates, custom
objects, and voice agents through Close's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute Close's hosted MCP implementation, private Codex connector,
service source code, account data, API credentials, or marketplace artwork.

The adapter is pinned to Close's official MCP guide with SHA-256
`ad74a3ce8ca3af94bfd2011c6d19c74b1514b2c8c123457e04e6b0675ae3d3e1` and its official tool catalog with SHA-256
`37b3dda1465bddbb60caece971c0c405f9456cadaef5b4fa68428efc19a65a2b`. The protected-resource metadata is pinned at
canonical JSON SHA-256 `5f59d0eb26ef33250e318f483a14288950ab8f62062fac36ece76e8de3a17402`, and the
authorization-server metadata at `2c3287ebc60fbc38a8790eb8e22573a3798c1197bb15c9af9303e05fafca94d2`.

The published tool order is also pinned independently: 57 `mcp.read` tools
have SHA-256 `7496c2076efbdb2cd9f35341855b1e0ca2345bd0060a7630be14795a9d66cb0b`, 16 `mcp.write_safe` tools have
SHA-256 `67dd13b698f10bed28c55361d872ea60d7522bd0874f660f94430af755a6536f`, 34 `mcp.write_destructive` tools
have SHA-256 `f4e6ff7259dbfb8f0c906ba27038c13ec1f72b90fe42199a1daf10f1c4afc404`, and all 107 tools have
SHA-256 `13b3c6707cd36be3089d78e426dd57e56e7c5bb0cefcae42b0281056774ee1c5`.

## Ghast compatibility

- Ghast connects directly to `https://mcp.close.com/mcp` using Streamable HTTP and
  Close OAuth. The service supports Dynamic Client Registration,
  authorization-code and refresh-token grants, public clients, and PKCE S256.
- Close's 107 official tools cover lead and object search, activity search,
  field discovery, aggregation and reporting, leads, contacts, opportunities,
  pipelines and statuses, tasks, calls, notes, comments, custom activities,
  custom objects, smart views, templates, workflows, forms, scheduling links,
  meeting transcripts, enrichment, and voice agents.
- This is a superset of the Codex app's stale-opportunity review, company lead
  summary, monthly pipeline review, custom reporting, lead-list creation,
  recent-interaction summary, and workflow creation capabilities.
- The three official scopes allow least-privilege analysis with `mcp.read`.
  Creates require `mcp.write_safe`. Close classifies updates, deletes,
  call-task creation, enrichment, voice-agent changes, and scheduled voice
  calls under `mcp.write_destructive`; the included skill requires exact
  target review and immediate explicit confirmation.
- OAuth is preferred. Close also documents API-key headers, but credentials
  must remain in host-managed secret storage and use the least-privileged
  `Close-Scope`.
- The hosted MCP implementation is not open source and is not redistributed.
  Documentation, the complete public catalog, OAuth metadata, disposable
  public-client registration, and unauthenticated protocol behavior were
  verified without a Close account. Authenticated tools/list and account-data
  operations were not run.
- A generic CRM icon is used because no licensed catalog artwork is included
  in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Close accounts, subscriptions, hosted service behavior, CRM data,
permissions, automations, trademarks, and terms remain controlled by Close.
