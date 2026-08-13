---
name: install-cli
license: MIT
description: >
  Install and configure Intercom's official @intercom/cli package when the
  user explicitly requests CLI access or needs the read-only ticket workflow.
---

# Install Intercom CLI

Intercom publishes `@intercom/cli` as its official command-line client. Ghast
does not bundle or silently install it.

## Audited release

- Package: `@intercom/cli@0.9.0`
- Required Node.js: 20.6.0 or newer
- npm integrity:
  `sha512-HCJjOJ5S654T03XJdQmI+C5z0CbqHEyYLHf90lcVkJvEHsCffU1N7BhDXgUtug2XGqitcPb74Az9pVueGdC8Tg==`

As of August 13, 2026, npm reports two high-severity vulnerability entries
for this release because it resolves `adm-zip` 0.5.18, affected by
GHSA-xcpc-8h2w-3j85. A crafted ZIP can cause excessive memory allocation, and
the package's declared dependency range has no compatible fix.

Do not install the CLI without telling the user about this advisory and
receiving explicit approval. The ticket workflow uses only the generic HTTP
API command and must not invoke ZIP import, Fin bundle, archive extraction, or
other ZIP-processing features.

## Install

First verify `node --version` is at least 20.6.0. After approval:

```sh
npm install --global @intercom/cli@0.9.0
intercom --version
```

The expected version is `0.9.0`. Do not use `sudo`, an unpinned version, a
third-party mirror, or an unofficial package.

## Authentication

Never ask the user to paste an Intercom token into chat and never place one in
a command argument, shell history, project file, plugin file, or generated
script.

For agent-run commands, the preferred path is a user-managed secret injected
as `INTERCOM_TOKEN` in the host environment. The CLI also supports
`INTERCOM_REGION=us`, `eu`, or `au` for regional REST routing.

For persistent interactive use, the user may run `intercom auth login`
themselves in their own terminal. The currently published command requires a
token; the agent must not construct or execute the token-bearing command.
The CLI prefers the native OS keyring and falls back to an encrypted file in
the user's Intercom configuration directory. Do not inspect either store.

Verify only non-secret status:

```sh
intercom auth status --json
intercom me --json
```

Do not print the environment, credential store, token, authorization header,
or verbose HTTP output.

## Use

Prefer the hosted MCP service for conversations, contacts, companies, and
articles. Use the CLI only for capabilities that the MCP service does not
provide, especially bounded read-only ticket search and retrieval through
`intercom api`.

Uninstalling, upgrading, authenticating, changing the default workspace, or
running any CLI write command requires a separate explicit user request.
