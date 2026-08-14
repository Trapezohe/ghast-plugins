# Modifications

Ghast builds this plugin from two official Windsor.ai MIT sources:

- `https://github.com/windsor-ai/windsor_mcp` at `f1632eefcae4c135fe4e6ec7f4454660f339eee0`
- `https://github.com/windsor-ai/claude-windsor-ai-plugin` at `d7ba1cb036c7ca765536355fb85f13a3237ea3f9`

Unmodified official files:

- `LICENSE` from the official Claude Code plugin
- `UPSTREAM_MCP_LICENSE.md`
- `UPSTREAM_MCP_README.md`
- `UPSTREAM_CLAUDE_README.md`
- `UPSTREAM_CLAUDE_MCP.json`
- `UPSTREAM_BUSINESS_DATA_SKILL.md`
- `UPSTREAM_BUSINESS_DATA_ANALYST.md`
- `commands/campaign-report.md`
- `commands/windsor-sources.md`
- `commands/windsor-types.md`

Ghast-authored additions:

- `.ghast-plugin/plugin.json`
- active `.mcp.json`, normalized to the protected resource URL with a trailing
  slash
- `README.md`
- `MODIFICATIONS.md`
- `assets/icon.svg`
- `skills/windsor-ai/SKILL.md`

The original Claude skill is preserved but not activated because it documents
only four read tools. Windsor.ai's current hosted reference documents 16 tools,
including connection, write-action, destination, subscription, login, and
support workflows. The active Ghast skill follows that live official contract
and adds safety constraints; it is not represented as byte-identical upstream
content.
