# Mixpanel plugin - Ghast engine guide

This plugin gives Ghast Mixpanel expertise for analytics, dashboards,
experiments, feature flags, Lexicon, metrics, business context, and tracking
implementation. Skills describe the desired Mixpanel action; an engine performs
it.

## Resolve an engine

A project can use more than one engine. Resolve one engine for the current
session, in this order:

1. An engine explicitly named by the user or loaded project instructions is
   mandatory. If it is unavailable, offer `/mixpanel:install` for that engine.
2. If Mixpanel MCP tools are available, use the MCP server. This is the default.
3. Otherwise offer `/mixpanel:install`. Never invent a direct HTTP API call.

## Official hosted MCP

The bundled `mixpanel` server launches pinned `mcp-remote@0.1.38` against one
official regional endpoint:

| `MIXPANEL_MCP_REGION` | Endpoint |
| --- | --- |
| `us` (default) | `https://mcp.mixpanel.com/mcp` |
| `eu` | `https://mcp-eu.mixpanel.com/mcp` |
| `in` | `https://mcp-in.mixpanel.com/mcp` |

With `MIXPANEL_MCP_SA_TOKEN` unset, the bridge uses Mixpanel's browser OAuth
flow with PKCE and dynamic client registration. For non-interactive use, the
variable may contain the base64 encoding of an official service-account
`username:secret` pair. Never request, print, log, or write the raw username,
secret, encoded token, access token, or refresh token.

Use the server tool whose description matches the requested action. For any
write, deletion, merge, bulk edit, experiment or flag lifecycle change, show
the exact proposed mutation and obtain explicit confirmation unless the
calling official skill already has a stricter confirmation contract.

Setup and verification live in
[`skills/install/references/mcp-setup.md`](skills/install/references/mcp-setup.md).

## mixpanel-headless SDK

Use the SDK when the user or loaded instructions explicitly prefer it and
`mp --version` succeeds. Read the installed package's
`mixpanel_headless/CLAUDE.md`, `mp --help`, and method docstrings before making
calls. Authentication is managed by `mp login`; verify with `mp account test`.
The separate `mixpanel-headless` Ghast plugin provides its deeper official
analysis workflows.

## Custom integration

If the user supplies an existing integration in the conversation or project
instructions, follow that integration exactly. Do not probe for credentials or
construct an undocumented transport.

## Skill engine tags

Every official `SKILL.md` declares `metadata.engine` as `required`, `optional`,
or `none`. Required skills stop and offer `/mixpanel:install` if no engine is
available. Optional skills use an engine when available and follow their
documented fallback otherwise.
