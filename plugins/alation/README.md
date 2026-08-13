# Alation

Search and browse trusted Alation catalog context, query data products, inspect BI lineage, configure agents and tools, automate workflows, and curate governed metadata through Alation's official Codex skills and CLI.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/Alation/alation-plugins` at `b450039495787ecd6bc16176cca6df6c4a1336c3`.

All seven skills, the pure-Python CLI, wrapper script, icon, and license are copied from Alation's pinned official Codex plugin. Ghast adds only explicit confirmation and secret-handling rules for state-changing workflows.

## Ghast compatibility

- The Codex private app connector is replaced by Alation's newer official portable Codex plugin and its authenticated CLI, which covers the private connector's catalog discovery, governance context, lineage, quality, and documentation workflows plus official query, automation, and curation features.
- The pinned Alation release does not contain a .mcp.json. Ghast does not invent one: users configure their tenant URL and OAuth client through credentials.local and the official setup skill.
- Python 3.10 or newer, an accessible Alation instance, a registered OAuth client or supported legacy credentials, and the user's existing Alation permissions are required.
- Ghast requires explicit confirmation for persistent writes, query or agent executions with material side effects, publishing, scheduling, external email, credential changes, and destructive operations.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
