---
name: install
description: >
  Set up Mixpanel for this project using Mixpanel's official hosted MCP
  server, the official mixpanel-headless Python SDK, or an existing custom
  integration. Use when the user asks to install, connect, configure, switch
  region, change authentication, or repair Mixpanel. Interactive; do not
  handle raw credentials in conversation.
compatibility: "Works in Ghast projects and profiles. Configures an official Mixpanel engine."
metadata:
  engine: none
---

# Mixpanel Install

> **No engine required** - this skill sets an engine up.

Read [`../../ENGINE.md`](../../ENGINE.md) before starting. Engines can coexist;
the user's explicit choice for this session wins.

## Step 0 - Detect current state

1. If Mixpanel MCP tools are already listed, report that the hosted MCP engine
   is connected. If the endpoint is visible, identify US, EU, or India. Ask
   whether to keep it, change region/authentication, or add another engine.
2. Otherwise run `mp --version` once. If it succeeds, report that the headless
   SDK is available and ask whether to connect MCP or keep using headless.
3. If neither is available, continue to engine selection.

## Step 1 - Select an engine

Ask one concise question with these choices:

1. **Official Mixpanel MCP** - recommended for interactive analytics and
   product management; browser OAuth by default.
2. **Official mixpanel-headless SDK** - recommended for scripts, CI, Python
   analysis, and coding-agent workflows.
3. **Existing custom integration** - use only instructions the user supplies.

## Step 2a - Official MCP

Read
[`references/mcp-setup.md`](references/mcp-setup.md), then:

1. Ask for region: US, EU, or India. If unsure, `eu.mixpanel.com` means EU,
   `in.mixpanel.com` means India, and other Mixpanel URLs normally mean US.
2. Ask whether the session is interactive OAuth or a non-interactive official
   service account. Never ask for the credential itself.
3. Tell the user the exact non-secret environment names and values to set:
   `MIXPANEL_MCP_REGION=us|eu|in`; for service accounts only,
   `MIXPANEL_MCP_SA_TOKEN` is the base64 encoding of `username:secret`.
4. Have the user store secrets outside chat, reload the active Ghast profile,
   and connect the bundled `mixpanel` MCP server. OAuth users complete the
   browser flow opened by the bridge.
5. Verify that tools are listed and call the project-listing tool. Do not
   continue if authentication or project access fails.

## Step 2b - mixpanel-headless

Follow
[`references/headless-setup.md`](references/headless-setup.md). Install the
official package into the project's existing Python environment if needed,
run `mp login`, and verify with `mp account test`. Never put credentials in a
tracked file or command argument.

## Step 2c - Custom integration

Acknowledge the integration and follow only the context the user provides.
Do not interrogate the environment or infer an undocumented API.

## Step 3 - Confirm

Re-run the chosen engine's verification and summarize:

- engine and region;
- authentication mode without credential values;
- where the engine is configured;
- whether project discovery succeeded.

Then suggest a concrete next workflow such as `analyze-report`,
`deep-research`, `create-dashboard`, or `tracking-implementation`.
