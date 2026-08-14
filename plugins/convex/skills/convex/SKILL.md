---
name: convex
description: >-
  Build and inspect Convex backends with the official Convex CLI, project-level
  Agent Skills, and the official 12-tool Convex MCP server.
---

# Convex

Use the official pinned Convex CLI MCP declared by this plugin.

## Project setup

- Work from the intended JavaScript or TypeScript project root.
- For a new project, follow Convex's current scaffold flow. For an existing
  Convex project, inspect `package.json`, `convex/`, schema, generated API, and
  deployment configuration before changing code.
- Run `npx --yes convex@1.44.0 ai-files install` only when the user asks to add
  or refresh Convex project guidance. It writes a managed `AGENTS.md` section
  and installs Convex's current official Agent Skills into `.agents/skills/`.
  Review the resulting diff; do not overwrite unrelated project instructions.
- Use generated types and Convex primitives for schema, queries, mutations,
  actions, auth-aware access, realtime subscriptions, scheduled jobs, file
  storage, components, and web or mobile clients. Validate with the project's
  own typecheck and tests.

## MCP workflow

- Start with `status` and use its exact deployment selector. Default to a local
  or personal development deployment.
- Use `tables`, `functionSpec`, and `insights` for low-risk structure and
  health inspection. Bound `data` and `logs` requests and avoid unrelated PII.
- `runOneoffQuery` is sandboxed and read-only, but its output can contain
  sensitive records. Keep queries narrow and disclose the deployment.
- Before `run`, inspect `functionSpec`. Queries may be read-only, while
  mutations and actions can change data or call external services. Show the
  exact deployment, function, arguments, and effects and obtain explicit
  confirmation for any mutation, action, unknown function, or external call.
- `envGet` and `envList` can expose secrets. Use only when strictly necessary,
  never print secret values, and do not copy them into chat or files.
- `envSet` and `envRemove` are state-changing. Show the deployment and variable
  name, redact the value, explain restart or outage impact, and obtain explicit
  confirmation immediately before the call.

## Production safety

- This plugin intentionally omits `--prod`,
  `--cautiously-allow-production-pii`, and
  `--dangerously-enable-production-deployments`.
- Do not restart the server with any production-enabling flag unless the user
  explicitly requests production access after reviewing the exact data and
  write risks. Prefer a scoped deploy key or isolated development deployment.
- Never infer production intent from a project name, environment file, or
  deployment selector. Treat deploy keys, admin keys, environment values,
  user records, logs, and function arguments as sensitive.
- After an ambiguous write or function error, inspect current state before
  retrying to avoid duplicate mutations, actions, schedules, or external calls.

## License boundary

- The runtime MCP and `ai-files` commands come from the Apache-2.0
  `convex@1.44.0` package.
- Convex's current full Codex marketplace repository and separate Agent Skills
  repository do not publish a license. Their files are not bundled here.
- The included icon comes from Convex's MIT-licensed official agent-plugin
  repository. Do not copy branding or unlicensed plugin files beyond this
  audited asset.
