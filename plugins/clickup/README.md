# clickup

Search and manage ClickUp tasks, lists, folders, documents, comments, chat,
assignments, relationships, attachments, and time tracking through ClickUp's
official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute ClickUp's hosted MCP implementation, private Codex connector,
service source code, Workspace data, or marketplace artwork.

The adapter is pinned to ClickUp's official tool reference, updated
`2026-03-19T23:41:01.000Z`, with SHA-256
`2d3fddb826de9a8577e0fde3ff109952a5d4ee929066152e24ba1efd887c5937`. The official overview is pinned at SHA-256
`dff0d558c63b4a0d30a239cb12eeeb5d17d5f0ce8cbf0a47cd1bf2bd32eda6bb` and the setup guide at SHA-256
`3d9416ff8959bec9225469da49f43cfcbadf179542c2b5219bb90e5ea4aef354`. The OAuth protected-resource metadata is pinned at
canonical JSON SHA-256 `19f2f7a0a70cc0d6197ac779d2eb4be43f0c8c303c229e5563e871f95222235b` and the
authorization-server metadata at `595d813bb7cb5ed08af4a0db8d2d34e0f0c2ca79388278c378c9876ffa94d3f7`.

## Ghast compatibility

- Ghast connects directly to `https://mcp.clickup.com/mcp` using Streamable HTTP and
  ClickUp OAuth. The service declares dynamic client registration,
  authorization-code grants, public clients, read and write scopes, and PKCE
  S256. ClickUp also documents `mcp-remote` for other compatible clients.
- The official tool reference lists 48 entries spanning Workspace search,
  tasks and bulk operations, attachments, comments, tags, relationships,
  time tracking, hierarchy, members, chat, Docs, and time-in-status reports.
- This covers the Codex app's deep Workspace search, create and update
  workflows, command-center use, and sprint-risk assessment, with additional
  official reporting, collaboration, hierarchy, and time-tracking workflows.
- Official documentation currently conflicts on deletion: the tool reference
  lists task deletion, while the newer overview FAQ says deletion tools have
  not been added. The skill does not promise deletion and requires fresh
  confirmation if an authenticated live tool list exposes it.
- Live OAuth discovery, unauthenticated endpoint challenge, and dynamic client
  registration with localhost callbacks were verified without a ClickUp
  account. Authenticated tool listing and Workspace operations were not run.
- A generic work-management icon is used because no licensed catalog icon is
  included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
ClickUp accounts, subscriptions, hosted service behavior, Workspace data,
permissions, trademarks, fair-use policy, and terms remain controlled by
ClickUp.
