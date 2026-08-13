# mixpanel-headless

Query and analyze Mixpanel data with Python. Provides the mixpanel_headless auth surface (Account → Project → Workspace hierarchy), API (5 query engines, discovery, entity CRUD), and Business Context read/write (the markdown documentation that grounds AI assistants, at org and project scopes), with a live documentation system (help.py) for method signatures, type lookup, fuzzy search, and hosted docs.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/mixpanel/mixpanel-headless` at `6c2c2f975d51628bdbc75802fb879d4f6cb66f69`.

Skills, references, scripts, commands, and public MCP declarations remain sourced from the pinned official repository. Unsupported client metadata is omitted.

## Ghast compatibility

- Skill-local helper paths use Ghast's host-resolved <SKILL_DIR> placeholder instead of Claude-only variables.
- The auth slash command routes through the official mp CLI, so it remains runnable without a plugin-root environment variable.
- The setup dependency list explicitly includes click>=8.1 because the pinned official CLI imports click directly but does not declare it as a direct package dependency.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
