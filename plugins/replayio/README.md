# Replay.io Pro

Record and inspect Replay browser runs, create verified MP4 evidence, debug uploaded recordings through Replay MCP, and run Replay QA project, bug, journey, and exploration workflows.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/replayio/plugins` at `c6cd28ff3d47f4e8e8b23040c69925ec2a820695`.

Skills, references, scripts, commands, and public MCP declarations remain sourced from the pinned official repository. Unsupported client metadata is omitted.

## Ghast compatibility

- Ghast does not execute Codex PostToolUse or Stop hooks, so browser recording and cleanup use the same official browser-open.js and browser-close.js scripts explicitly.
- The official Replay.io Pro and Replay QA packages are combined so Ghast retains both recording/debugging and hosted QA workflows.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
