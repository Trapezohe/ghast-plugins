---
name: github
description: Read GitHub repositories, review PRs and issues, diagnose failing Actions, and make requested GitHub changes through the connected official GitHub MCP. Use for GitHub links, PR reviews, CI failures, issues, 仓库、代码审查、拉取请求、持续集成.
---

# GitHub

Use the installed GitHub MCP tools. Discover the needed capability with
`ToolSearch` using `github` and the action (for example `github pull request`,
`github actions logs`, or `github issue`). Read the returned tool schema before
calling it. Tool names come from the running server; never invent a Codex
`mcp__codex_apps__github_*` name or an OpenAI connector ID.

If no GitHub tool is available, direct the user to Plugins → GitHub → service
connections. Connect `github-token` in the password field and retry discovery.
Never ask for a token in chat, read credential files, print a token, or put one
in a shell command. Installation alone does not authorize account access.

## Workflow

1. Resolve the repository and PR/issue/run from the user's link or task context.
   Ask only if the target remains ambiguous.
2. Read current state. For a PR, inspect the diff and checks. For a failing CI
   run, identify the failed job and read its logs before proposing a fix.
3. Report findings with repository links and actual IDs. Separate missing
   permissions, authentication failures and unavailable data from empty results.
4. Perform writes only within the user's requested action. A request to review
   does not authorize posting a review, merging, rerunning CI or creating an
   issue. Preserve Ghast's execution approvals and repository scope.
5. Read back the changed issue/PR/run after a write, and link the result. Do not
   report success from an attempted call or an error response.

Use the existing `gh` CLI only when a required operation is unavailable in MCP
and the CLI is already configured. Keep authentication inside the CLI; never
extract its stored token. Local git operations require an identified workspace.

Suggested tasks: summarize a PR; explain a failed workflow; draft an issue from
a reproducible bug; list unresolved review feedback.
