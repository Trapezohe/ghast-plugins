# CircleCI

Diagnose CircleCI runs, inspect logs, tests, and artifacts, rerun or cancel workflows, validate configuration, and manage CircleCI resources through CircleCI's official hosted MCP and full CLI MCP.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/CircleCI-Public/circleci-cli` at `1121fafe77b5b2bfa623dda1a244517ff604a823`.

The licensed agent skill, CLI MCP implementation, official release metadata, icon, and MIT license come from CircleCI's pinned CLI repository. The hosted MCP endpoint is operated by CircleCI. Ghast adds routing and safety guidance but does not copy the separate six-skill repository because that repository declares MIT only in its manifest and contains no license text.

## Ghast compatibility

- The hosted MCP is the default for day-to-day run diagnosis. At the audited date it exposes 13 curated tools for runs, workflows, jobs, logs, tests, artifacts, usage exports, reruns, and cancellation.
- The local CircleCI CLI MCP runs `circleci mcp start` and exposes the full installed CLI. Official release 1.0.47993 exported 153 tools in the Ghast smoke test.
- Hosted MCP uses OAuth by default and also accepts a personal API token as a bearer token. CLI MCP uses `circleci auth login` or CIRCLE_TOKEN; credentials remain outside the plugin package.
- CircleCI's former `@circleci/mcp-server-circleci` npm server is explicitly deprecated and is not included.
- The Codex snapshot's build, CLI, config, Chunk, onboarding, and smarter-testing guidance is covered by the current official MCP and CLI surfaces. The unlicensed skill text is not redistributed.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
