# lovable

Create, inspect, iterate, deploy, and manage full-stack Lovable apps, code,
knowledge, databases, connectors, analytics, and workspaces through Lovable's
official hosted MCP server.

## Official hosted MCP adapter

This package uses Lovable's official public Streamable HTTP endpoint and
public OAuth client ID. It includes Ghast-authored safety instructions,
catalog metadata, and a generic icon. It does not copy or redistribute
Lovable's hosted MCP implementation, private Codex connector, user projects,
OAuth tokens, branded artwork, or marketplace icon.

Lovable's official public integration repository is pinned at
`0336e6db8026b0f02cb89d1451cc48ea3f469791`. The importer verifies its Apache-2.0 license,
README, security policy, MCP declaration, registry entry, plugin manifest,
marketplace declaration, and build, database, and iteration commands. The
official documentation is pinned at SHA-256 `8dbf8a5024503f837f99cc1c7870c740e0e5e0ff7449ed9b7d788af1449f7278` and the
server-maintained skill at `1171007e1580a6526aa2e20d4faa6bbacf621761ad8c3dbe5c34ed7ec5c6c7c5`.

The endpoint root metadata is pinned at canonical JSON SHA-256
`bcb74970a60d2a7d825de5cf112367e0b8d7239698cb7e04df89c5f07cc3ec61`. Protected-resource and authorization-server
metadata are pinned at `6208a9f26a9c3a2a1b42dafc6e5122772a165da5f022b93ef212c8877f4072d6` and
`908c30410a805628c70620212c4510f819c8233db168f2a360cabb4f21233605`. Codex capability evidence is pinned to OpenAI
plugin snapshot `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app
identifier or artwork.

## Ghast compatibility

- Ghast connects directly to `https://mcp.lovable.dev` and supplies Lovable's
  documented public OAuth client ID. OAuth uses authorization code, refresh
  tokens, public clients, PKCE S256, and bearer-header tokens.
- A live unauthenticated runtime test discovered
  `https://lovable.dev/oauth`, generated a PKCE authorization URL for the
  public client, requested the documented project and workspace scopes, and
  reached the browser authorization wait state.
- The official docs list 41 standard tools for identity, workspaces, projects,
  agent messages, knowledge, workspace skills, code inspection, databases,
  connectors, analytics, and uploads. MCP App and Claude hosts can expose two
  additional client-specific tools.
- This is a functional superset of the Codex app description: it can find
  projects and recent changes, inspect code and screenshots, assess readiness,
  draft or execute build prompts, configure authentication and databases,
  return preview and editor URLs, and deploy when explicitly approved.
- `create_project` and `send_message` consume Lovable credits.
  `deploy_project` publishes a live URL. `query_database` has full read, write,
  and schema permissions. The included skill requires exact target review and
  explicit confirmation for credit use, code changes, deploys, visibility,
  knowledge replacement, workspace-skill changes, connector removal,
  provisioning, and mutating SQL.
- The OAuth connection inherits the user's full Lovable account access, not
  one project. Account plan, credits, role, Enterprise third-party MCP policy,
  SSO lifetime, project permissions, and feature availability remain
  authoritative.
- The root metadata still mentions API-key authentication, while the current
  official documentation says API keys are not available and OAuth is the
  only supported connection path. Ghast follows the documented OAuth flow and
  records this official metadata inconsistency.
- The public `lovablelabs/mcp` repository contains integration manifests,
  commands, security policy, and registry metadata, not the hosted service
  implementation. Authenticated tools/list and real project operations were
  not run because no Lovable account was supplied.
- A generic app-builder icon is used because the official integration
  repository does not include licensed catalog artwork.

The Apache License 2.0 in this package covers the adapter files distributed
here. Lovable accounts, credits, hosted service behavior, project data,
generated applications, connectors, trademarks, and terms remain controlled
by Lovable.
