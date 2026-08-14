# Auth and Setup

## Hosted MCP

This plugin declares Egnyte's official Streamable HTTP endpoint:

```json
{
  "mcpServers": {
    "egnyte": {
      "type": "http",
      "url": "https://mcp-server.egnyte.com/mcp"
    }
  }
}
```

The MCP host should open browser OAuth on first use. Sign in to the intended
Egnyte domain and verify the acting account and folder scope before accessing
enterprise content.

Smoke check:

```text
list_filesystem_by_path(path="/Shared", intent="Confirming Egnyte access")
```

If MCP authentication is stale, use the host's normal reconnect or credential
removal flow. Do not edit another application's MCP configuration.

## Official CLI

The optional CLI is `@egnyte/agentic-cli@1.0.1` and requires Node.js 14 or
newer. Prefer a pinned one-shot invocation where practical:

```bash
npx --yes @egnyte/agentic-cli@1.0.1 schema --list
```

Install globally only with user approval:

```bash
npm install -g @egnyte/agentic-cli@1.0.1
```

### Authentication

The CLI supports a built-in OAuth application:

```bash
egnyte login --domain https://yourcompany.egnyte.com
```

Ask the user for the exact domain before running this command. A browser opens
for approval and the user completes the redirect-code step. Never automate
developer-portal registration or request a new OAuth application.

For CI or headless use, pass existing credentials through the environment:

```bash
export EGNYTE_TOKEN=<bearer-token>
export EGNYTE_DOMAIN=https://yourcompany.egnyte.com
```

Optional custom OAuth credentials are supported, but secrets must come from
the user's secret manager or environment and must never be printed:

```bash
egnyte login --domain https://yourcompany.egnyte.com   --client-id <client-id> --client-secret <client-secret>
```

Credentials are stored at `~/.config/egnyte-cli/config.json` with mode `0600`.
Precedence is command flags, environment variables, then the selected stored
profile.

### Profiles and verification

```bash
egnyte profiles list
egnyte profiles use <name>
egnyte profiles remove <name>
egnyte whoami
egnyte userinfo
egnyte schema --list
```

`whoami` reports local profile metadata. `userinfo` makes a live API call and
is the stronger check when actor identity matters.

All Egnyte paths begin with `/`, commonly `/Shared/` or a user's
`/Private/<username>/` tree.
