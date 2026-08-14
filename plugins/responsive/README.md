# responsive

Search governed proposal content and work with Responsive projects through
Responsive's official hosted MCP server.

## Official service

Responsive publishes `https://app.rfpio.com/oa/v1/mcp` as its US production
Streamable HTTP endpoint for ChatGPT, Claude, Cursor, VS Code, Databricks,
Windsurf, and other MCP-compatible clients. Authentication uses OAuth 2.0 with
PKCE and inherits the connected Responsive user's permissions.

The current official tools are:

- `get_project_list`
- `get_project_details`
- `get_project_sections`
- `get_project_question`
- `get_unanswered_questions`
- `search`
- `fetch`
- `generate_draft_response`
- `get_my_profile`

## Capability comparison

- Codex: search the Responsive Content Library and generate responses using a
  private app connector.
- Ghast: connect directly to Responsive's official hosted MCP, search and fetch
  governed Library content, inspect projects and open questions, retrieve user
  context, and generate grounded draft responses.
- The official MCP is a functional superset of the Codex description because
  it adds explicit project navigation, work tracking, source provenance, and
  user-context tools.

## Verification and licensing

The importer pins the complete OpenAI marketplace evidence, five official
Responsive developer-document pages, the exact nine documented tool names,
the live protected-resource and OAuth metadata, and the anonymous MCP
authentication boundary. An optional disposable registration check verifies
that authorization routes to Responsive's official login. Authenticated
`tools/list` and customer-data calls require a Responsive account and were not
executed.

Responsive's OAuth metadata advertises dynamic registration, authorization
code, refresh token, and PKCE S256. Disposable registration currently returns
a client secret while omitting `token_endpoint_auth_method`, and the initial
authorization redirect currently names the official login with an `http` URL;
the service also emits HSTS over HTTPS. This adapter stores no static client
credential and leaves the OAuth exchange to the host MCP client.

The MIT license in this package covers only the Ghast-authored endpoint
declaration, workflow guidance, metadata, documentation, and generic document
icon. It does not license or redistribute Responsive's hosted implementation,
private Codex connector, service data, credentials, developer documentation,
logos, trademarks, or customer content. Accounts, subscriptions, regional
endpoints, permissions, service limits, and terms remain controlled by
Responsive.
