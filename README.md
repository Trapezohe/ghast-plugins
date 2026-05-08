# Ghast Skills & MCP Store

Public registry for [Ghast](https://ghast.trapezohe.ai) — discovers and installs **plugins**, **skills** (bundled inside plugins), and **MCP servers**.

This repository hosts two registry files plus the actual plugin sources:

| File | Purpose | Consumed by |
| --- | --- | --- |
| `registry.json` | Plugin & skill index | Ghast Settings → Plugins / Skills marketplace |
| `mcp-registry.json` | MCP server index | Ghast Settings → MCP marketplace |
| `plugins/<id>/` | Plugin source (with optional `skills/` subdir) | Resolved via `registry.json[].path` |

Skills are not a separate store category — they ship inside plugins under `plugins/<id>/skills/<skill-name>/SKILL.md` and are scanned automatically when the host plugin is installed.

---

## Repo layout

```
skills_store/
├── README.md
├── registry.json                  # plugin / skill registry
├── mcp-registry.json              # MCP server registry
├── plugins/
│   └── <plugin-id>/
│       ├── manifest.json          # required, validated by zod schema
│       ├── main.js                # entry point referenced by manifest.main
│       ├── icon.png               # optional
│       ├── skills/                # optional; bundled skills
│       │   └── <skill-name>/
│       │       └── SKILL.md
│       └── README.md
└── .github/
    └── workflows/                 # (optional) CI to validate registry & manifests
```

---

## Adding a plugin

### 1. Drop your plugin into `plugins/<plugin-id>/`

Required: `manifest.json` and the file referenced by `manifest.main`.

### 2. `manifest.json` schema (zod-validated by Ghast)

```json
{
  "id": "your-plugin-id",
  "name": "Your Plugin",
  "version": "0.1.0",
  "description": "What this plugin does in one line.",
  "author": "Your Name",
  "main": "main.js",
  "engines": { "ghast": "^0.1.0" },
  "type": "tool",

  "icon": "icon.png",
  "homepage": "https://github.com/Trapezohe/skills_store",
  "repository": "https://github.com/Trapezohe/skills_store",
  "license": "MIT",
  "keywords": ["example"],
  "permissions": [],
  "activationEvents": ["onStartup"],

  "contributes": {
    "tools": [],
    "commands": [],
    "themes": [],
    "providers": [],
    "keybindings": [],
    "components": {
      "sidebar": [],
      "settingsPanels": [],
      "toolbar": [],
      "contextMenus": [],
      "artifactRenderers": [],
      "statusBar": []
    },
    "configuration": null,
    "locales": []
  }
}
```

**Required fields**: `id` · `name` · `version` · `description` · `author` · `main` · `engines.ghast` · `type`

**Field constraints**:

| Field | Constraint |
| --- | --- |
| `id` | matches `[@a-z0-9-_./]+`, must be globally unique |
| `version` | semver `\d+\.\d+\.\d+` |
| `author` | string, **or** `{ name, email?, url? }` |
| `type` | one of `tool` · `ui` · `theme` · `provider` · `transform` · `integration` · `composite`, or array of those |
| `engines.ghast` | semver range string, e.g. `^0.1.0` |

### 3. Add an entry to `registry.json`

```json
{
  "plugins": [
    {
      "id": "your-plugin-id",
      "version": "0.1.0",
      "repository": "https://github.com/Trapezohe/skills_store",
      "path": "plugins/your-plugin-id"
    }
  ]
}
```

The Ghast client composes `${repository}/tree/main/${path}` to fetch the plugin and runs version compares against the manifest's `version` field for update notifications.

### 4. (Optional) bundle skills

Drop one or more skill directories under `plugins/<plugin-id>/skills/`. Each skill is a folder containing a `SKILL.md`:

```markdown
---
name: skill-name
description: One-line description shown in the skill picker.
type: feedback
---

# Skill Name

Body content (markdown). Becomes the system prompt injected when the
skill is selected.
```

Skills are auto-discovered when their host plugin is installed — they don't need a separate registry entry.

---

## Adding an MCP server

Append to `mcp-registry.json`:

```json
{
  "id": "example-mcp",
  "name": "Example MCP Server",
  "description": "What this server does.",
  "author": "Your Name",
  "url": "https://github.com/your/example-mcp-server",
  "category": "tools",
  "tags": ["productivity"],
  "installations": [
    {
      "name": "NPX",
      "config": "{\n  \"command\": \"npx\",\n  \"args\": [\"-y\", \"@your/example-mcp\"],\n  \"env\": {\"API_KEY\": \"${API_KEY}\"}\n}",
      "prerequisites": ["Node.js"],
      "parameters": [
        {
          "name": "API Key",
          "key": "API_KEY",
          "placeholder": "your_api_key",
          "required": true
        }
      ],
      "transports": ["stdio"]
    }
  ]
}
```

After adding, also bump `totalServers` and `generatedAt` at the top of `mcp-registry.json`.

**Notes**:

- `installations[].config` is a **JSON-stringified** mcpServers entry — it is _not_ a nested object. Mind the escaping.
- `transports` values: `stdio` · `sse` · `streamable-http`.
- Parameter keys (e.g. `API_KEY`) are substituted into the config string at install time via `${KEY}` placeholders.

---

## Validation

Before pushing a plugin or MCP entry, validate locally:

```bash
# JSON syntax
python3 -m json.tool registry.json > /dev/null
python3 -m json.tool mcp-registry.json > /dev/null
python3 -m json.tool plugins/your-plugin-id/manifest.json > /dev/null

# Manifest fields (full zod check happens on the Ghast client side)
node -e 'JSON.parse(require("fs").readFileSync("plugins/your-plugin-id/manifest.json"))' \
  && echo "manifest ok"
```

CI workflows under `.github/workflows/` (to be added) will run the same checks on PRs.

---

## Versioning

- Bumping a plugin's `version` in both its `manifest.json` and the `registry.json` entry triggers an update notification in installed Ghast clients.
- Use semver: bump patch for fixes, minor for additions, major for breaking changes.
- Removing a plugin from `registry.json` does **not** uninstall it from existing clients — it just stops appearing in the marketplace.

---

## Contributing

1. Fork this repository.
2. Add your plugin under `plugins/<id>/` with a valid `manifest.json`.
3. Add the registry entry to `registry.json` (and `mcp-registry.json` if applicable).
4. Open a PR. CI will validate; a maintainer will review.

For substantial changes (new plugin types, schema updates, API contracts), open an issue first to discuss.

---

## License

This registry repository is published under the MIT License. Each plugin under `plugins/` may carry its own license declared in its `manifest.json` — installers are responsible for reading and complying.
