# convex

Build and inspect Convex backends with Convex's official CLI, project-level
Agent Skills, and the official 12-tool Convex MCP server.

## Official runtime adapter

Ghast runs `npx --yes convex@1.44.0 mcp start`. The npm tarball is
fixed at SHA-256 `8bdb320a17ed370b9635611b4c8b951a6913c9a830e470a28934ffe0a5735493` and includes the Apache-2.0 license.
Protocol initialization and the complete ordered tool schema are pinned at
SHA-256 `e1637c4cf48c8431e4131bcbc86cdb9dd6edc4155308411804b46f0b1361b1e1` and `5d3be1fb3d20a781021c53b808de2c5286f0dce8b478f77c45e0d2c75c82567d`.

The tools are `status`, `data`, `tables`, `functionSpec`, `run`, `envList`,
`envGet`, `envSet`, `envRemove`, `runOneoffQuery`, `logs`, and `insights`.
The default launcher does not enable production deployments, production PII,
or production writes.

Convex's official Codex guide says the OpenAI directory entry is the lighter
ChatGPT-app connector. It recommends the full marketplace build for skills,
subagents, and an error watcher, but that public repository has no license.
Ghast therefore does not redistribute those files. Instead, the included
workflow uses the licensed CLI's `ai-files install` command to install and
refresh current Convex-authored project guidance at runtime.

The catalog icon is copied from Convex's MIT-licensed
`get-convex/convex-agent-plugins` revision `7023eb599ffe326d3f451cdc27a2d88b70b7bb4d` and has SHA-256
`cd6eaca42d7c12f8be21f07905dc7d042eef9b8342c61f8e0afd8db8f77ca261`.

Node.js 18 or newer, npm 7 or newer, network access, a Convex project, and the
appropriate login or scoped deploy key remain user-managed. Deployment data,
logs, environment variables, mutations, actions, schedules, and external
effects remain subject to Convex permissions and explicit confirmation.
