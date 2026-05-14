# Ghast Plugins & MCP Registry

[![Sync Anthropic plugins](https://github.com/Trapezohe/ghast-plugins/actions/workflows/sync-anthropic-plugins.yml/badge.svg)](https://github.com/Trapezohe/ghast-plugins/actions/workflows/sync-anthropic-plugins.yml)

Public plugin & MCP directory for the
[Ghast desktop client](https://ghast.trapezohe.ai).

This repo follows the **Anthropic plugin format** used by
[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official),
so plugins authored for Claude Code's plugin system can be hosted here (and
vice versa). Ghast also exposes its own MCP server registry alongside.

| File | Purpose | Consumed by |
| --- | --- | --- |
| `.claude-plugin/marketplace.json` | Plugin directory (Anthropic schema) | Ghast → Settings → Plugins |
| `mcp-registry.json` | MCP server directory (self-contained) | Ghast → Settings → MCP → Marketplace |
| `plugins/<name>/` | Plugin source trees | Resolved via marketplace `source` |

The Ghast client fetches these files directly from `raw.githubusercontent.com`
on the `main` branch. Push to `main` → marketplace updates on the next refresh.

---

## Plugin directory: `.claude-plugin/marketplace.json`

Schema declared by `$schema: "https://anthropic.com/claude-code/marketplace.schema.json"`.

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "ghast-plugins",
  "description": "...",
  "owner": { "name": "Ghast AI", "url": "https://ghast.trapezohe.ai" },
  "plugins": [
    {
      "name": "<plugin-id>",
      "description": "...",
      "author": { "name": "...", "email": "..." },
      "category": "utility | web | development | finance | gaming | media | news | information | productivity",
      "source": "./plugins/<plugin-id>",
      "homepage": "..."
    }
  ]
}
```

`source` can be:

- **`"./plugins/<name>"`** — plugin lives inside this repo under the given path.
- **`{ "source": "git-subdir", "url": "...", "path": "...", "ref": "main", "sha": "<commit>" }`** — plugin lives in another repo. The optional `sha` pins the install to a specific commit for reproducibility.
- **`{ "source": "url", "url": "https://github.com/...", "sha": "..." }`** — whole repo is the plugin (no subdir).

---

## Plugin layout

Each plugin lives at `plugins/<plugin-name>/` and follows the Anthropic
convention. Anything beyond `plugin.json` is optional — pick only the
contribution kinds your plugin actually provides.

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json          # required — name / description / author
├── commands/                # optional — slash commands
│   └── <command>.md
├── skills/                  # optional — model-invoked skills
│   └── <skill>/SKILL.md
├── agents/                  # optional — subagent definitions
│   └── <agent>.md
├── hooks/                   # optional — Claude lifecycle hooks
├── .mcp.json                # optional — MCP server config to register
├── README.md
└── LICENSE
```

### `.claude-plugin/plugin.json`

The only required file. Keep it minimal:

```json
{
  "name": "your-plugin",
  "description": "One-line summary of what this plugin does.",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  }
}
```

`name` must match both the directory name (`plugins/<name>/`) and the
`name` field in `marketplace.json`.

### `commands/<command>.md`

User-invoked slash commands. Body becomes the prompt that runs when the
user types `/<command>` in chat. Frontmatter:

```markdown
---
description: One-liner shown in /help and the slash-command picker
argument-hint: "<required-arg> [optional-arg]"
allowed-tools: [Read, Bash, WebFetch]
---

# Command Title

The user invoked this with: $ARGUMENTS

Instructions:
...
```

`$ARGUMENTS` is substituted with whatever the user typed after the command
name. `allowed-tools` pre-approves tools so the command runs without
permission prompts. Optional `model: haiku | sonnet | opus` overrides the
chat model for this invocation.

### `skills/<name>/SKILL.md`

Model-invoked capabilities. The model autonomously decides when to inject a
skill based on its `description` and the task context. Frontmatter:

```markdown
---
name: skill-name
description: When this skill should activate. Be specific — this is what the model reads to decide.
version: 1.0.0
allowed-tools: [WebFetch, Bash]
---

# Skill Title

Body becomes the system-prompt fragment injected when the skill activates.
Tell the model:
- When this skill applies
- What tools to use (and how)
- How to format the output
```

### `.mcp.json`

Standard MCP servers config — Claude Code / Ghast wire these into the
session when the plugin is installed.

```json
{
  "example-server": {
    "type": "http",
    "url": "https://mcp.example.com/api"
  },
  "another": {
    "command": "npx",
    "args": ["-y", "@example/mcp"],
    "env": { "API_KEY": "${API_KEY}" }
  }
}
```

---

## Starter set

The marketplace currently lists **184 plugins**:

- **12 Ghast-original starters** (the table below) inspired by
  [lobehub/lobe-chat-plugins](https://github.com/lobehub/lobe-chat-plugins)
  and re-implemented as Anthropic-format skill bundles. None require an
  API key; all use builtin `WebFetch` / `Bash` for network access.
- **172 entries inherited from
  [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)**.
  Anthropic's directory is curated and includes both Anthropic-authored
  internal plugins (agent-sdk-dev, code-review, frontend-design,
  language-server plugins for ~10 languages, etc.) plus third-party
  plugins from partners (Adobe, HashiCorp, 42Crunch, GitHub, GitLab,
  Linear, Playwright, Firebase, etc.). Entries that originally used a
  `./plugins/foo` relative path are rewritten as `git-subdir` pointing
  at `anthropics/claude-plugins-official` — we don't fork their code,
  we just surface their directory.

Ghast-originals:

| Plugin | Kind | What it does |
| --- | --- | --- |
| `current-datetime` | command + skill | `/now [tz]` and a skill that tells the model the wall-clock time |
| `mermaid-mindmap` | command | `/mindmap <topic>` outputs a Mermaid mindmap block |
| `website-fetcher` | skill | Fetch a URL and read its readable text |
| `uptime-check` | skill | HEAD/GET probe with latency |
| `realtime-weather` | skill | Open-Meteo current weather + 24h forecast |
| `github-stats` | skill | Public GitHub REST API repo / user lookups |
| `hacker-news` | skill | HN Firebase API — top / new / best stories + threads |
| `defillama` | skill | api.llama.fi — TVL, top protocols, chain breakdown |
| `stock-quote` | skill | Yahoo Finance v8 chart — delayed quotes |
| `steam-search` | skill | Steam storesearch + appdetails |
| `bilibili-search` | skill | Bilibili public web search + ranking |
| `seo-meta` | skill | Meta / OG / Twitter / canonical extractor |

### Keeping the Anthropic mirror fresh

The merge is automated via
[`.github/workflows/sync-anthropic-plugins.yml`](.github/workflows/sync-anthropic-plugins.yml) —
a GitHub Actions workflow that runs daily at 02:00 UTC, fetches
Anthropic's current marketplace, re-runs the merge, and commits any
diff back to `main` with a message recording Anthropic's HEAD sha.
You can also trigger it manually from the Actions tab (with a
`dry_run` toggle that reports the diff without pushing).

The underlying merge logic lives in
[`scripts/merge-anthropic-plugins.py`](scripts/merge-anthropic-plugins.py)
and is idempotent — re-runs drop the prior Anthropic-imported set and
recompute it, so duplicates never accumulate. Run it locally with:

```bash
python3 scripts/merge-anthropic-plugins.py
```

Our 12 Ghast-original entries are always preserved; name collisions
keep our copy and skip the Anthropic version.

---

## MCP server directory: `mcp-registry.json`

Self-contained registry of MCP servers, distinct from plugins (an MCP
server alone has no commands/skills/hooks). Shape:

```json
{
  "generatedAt": "2026-05-14T...",
  "servers": [
    {
      "id": "example",
      "name": "Example",
      "description": { "en": "...", "zh-CN": "..." },
      "author": "...",
      "url": "https://github.com/...",
      "license": "MIT",
      "category": "tools",
      "tags": ["..."],
      "featured": false,
      "verified": false,
      "installations": [
        {
          "name": "npx",
          "description": { "en": "...", "zh-CN": "..." },
          "config": {
            "command": "npx",
            "args": ["-y", "@your/example-mcp"],
            "env": { "API_KEY": "${API_KEY}" }
          },
          "parameters": [
            {
              "name": "API_KEY",
              "description": { "en": "...", "zh-CN": "..." },
              "placeholder": "your_api_key",
              "required": true
            }
          ],
          "prerequisites": ["Node.js 18+"],
          "transports": ["stdio"]
        }
      ],
      "detectionHints": ["@your/example-mcp"]
    }
  ]
}
```

Field semantics:

- **`description`** etc. accept either a plain string or a BCP-47-keyed object (`{ en, zh-CN, zh-TW, ja, ... }`). Client falls back through exact → base lang → en → first non-empty.
- **`config`** is a real JSON object (not a stringified blob), matching the shape Ghast persists in its mcpServers settings entry.
- **`${PARAM}`** placeholders inside any string value get substituted with what the user enters during install (`parameters[].name` is the key).
- **`transports`**: `stdio` · `sse` · `streamable-http`.
- **`detectionHints`**: substrings checked against the user's Claude Desktop / Codex CLI / Cursor MCP configs (`command + args + url` haystack). If any hint hits, the marketplace card swaps **Install** → **Import from <client>** which copies the existing config (including tokens) straight into Ghast.

---

## Validation

Before pushing:

```bash
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null
python3 -m json.tool mcp-registry.json > /dev/null
for f in plugins/*/.claude-plugin/plugin.json; do
  python3 -m json.tool "$f" > /dev/null || echo "FAIL: $f"
done
```

Skill / command markdown frontmatter is validated client-side at install
time. Bad entries are dropped from the listing with a console error — they
don't break the whole registry.

---

## Contributing

1. Fork.
2. For a plugin: add a folder under `plugins/<name>/` with at minimum
   `.claude-plugin/plugin.json` + one of `commands/` / `skills/` / `agents/` / `hooks/` / `.mcp.json`. Add the index entry to `.claude-plugin/marketplace.json`.
3. For an MCP server: add an entry under `mcp-registry.json:servers`.
4. Open a PR. CI (forthcoming) will lint the JSON; a maintainer reviews.

To request a third-party listing without forking, open an issue with the
`registry-request` label (and `plugin` or `mcp` for the type).

---

## License

This registry repository is published under the MIT License. Each plugin
under `plugins/` may declare its own license; see each plugin's
`LICENSE` file for details.

The starter plugin set was inspired by the MIT-licensed
[lobehub/lobe-chat-plugins](https://github.com/lobehub/lobe-chat-plugins)
catalog — content and intent rewritten as Anthropic-format skill bundles
for the Ghast / Claude Code plugin runtime.
