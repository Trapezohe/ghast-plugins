# Ghast Plugins & MCP Registry

Public registry powering the **Plugins** and **MCP** marketplaces inside the
[Ghast desktop client](https://ghast.trapezohe.ai).

This repo hosts two independent indexes plus the actual plugin sources.

| File | Purpose | Consumed by |
| --- | --- | --- |
| `registry.json` | Plugin index | Ghast → Settings → Plugins |
| `mcp-registry.json` | MCP server index | Ghast → Settings → MCP → Marketplace |
| `plugins/<id>/` | Plugin source tree | Resolved via `registry.json[].path` |

The Ghast client fetches these files directly from `raw.githubusercontent.com`
on the `main` branch. There is no build step — push to `main` and the
marketplace updates on the next refresh.

---

## Layout

```
ghast-plugins/
├── README.md
├── registry.json                  # plugin index
├── mcp-registry.json              # MCP server registry (self-contained)
└── plugins/
    └── <plugin-id>/
        ├── manifest.json          # required, zod-validated by the client
        ├── main.js                # entry point (whatever `manifest.main` points at)
        ├── icon.png               # optional
        └── README.md              # optional
```

---

## Adding a plugin

### 1. Drop the plugin into `plugins/<plugin-id>/`

It must contain a `manifest.json` and the file referenced by `manifest.main`.

### 2. `manifest.json` schema

Validated client-side with [zod](https://github.com/colinhacks/zod). See
`src/main/plugins/plugin-manifest-schema.ts` in the Ghast repo for the
authoritative definition.

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
  "homepage": "https://github.com/Trapezohe/ghast-plugins",
  "repository": "https://github.com/Trapezohe/ghast-plugins",
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

**Required**: `id` · `name` · `version` · `description` · `author` · `main` · `engines.ghast` · `type`

**Constraints**:

| Field | Constraint |
| --- | --- |
| `id` | matches `[@a-z0-9-_./]+`, globally unique |
| `version` | semver `\d+\.\d+\.\d+` |
| `author` | string **or** `{ name, email?, url? }` |
| `type` | one of `tool` · `ui` · `theme` · `provider` · `transform` · `integration` · `composite`, or an array of those |
| `engines.ghast` | semver range, e.g. `^0.1.0` |

### 3. Add the registry entry

Append to `registry.json`:

```json
{
  "plugins": [
    {
      "id": "your-plugin-id",
      "version": "0.1.0",
      "repository": "https://github.com/Trapezohe/ghast-plugins",
      "path": "plugins/your-plugin-id"
    }
  ]
}
```

The client composes the manifest URL as

```
https://raw.githubusercontent.com/<owner>/<repo>/main/<path>/manifest.json
```

and compares `manifest.version` against the installed version to trigger update
notifications. **Bump both** `manifest.json:version` **and** `registry.json:plugins[].version`
when releasing.

Plugins can also live in a third-party repo — set `repository` to point there
and `path` to the subdirectory inside it. They don't have to be hosted in this
monorepo.

---

## Adding an MCP server

Append to `mcp-registry.json` under `servers`. The registry is **self-contained**:
the client reads the config directly from this file, so there's nothing to host
elsewhere.

```json
{
  "id": "example",
  "name": "Example",
  "description": {
    "en": "What this server does.",
    "zh-CN": "这个 server 是干什么的。"
  },
  "author": "Your Name",
  "url": "https://github.com/your/example-mcp",
  "license": "MIT",
  "category": "tools",
  "tags": ["example"],
  "featured": false,
  "verified": false,
  "installations": [
    {
      "name": "npx",
      "description": {
        "en": "Run via npx.",
        "zh-CN": "通过 npx 运行。"
      },
      "config": {
        "command": "npx",
        "args": ["-y", "@your/example-mcp"],
        "env": { "API_KEY": "${API_KEY}" }
      },
      "parameters": [
        {
          "name": "API_KEY",
          "description": { "en": "API key.", "zh-CN": "API 密钥。" },
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
```

After adding, bump `generatedAt` at the top of `mcp-registry.json` to the
current ISO timestamp.

### Localisation

`description`, `installations[].description`, `parameters[].description`, and
`prerequisites[]` accept either a plain string (legacy, treated as `en`) or a
BCP-47 keyed object (`en`, `zh-CN`, `zh-TW`, `ja`, `ko`, `fr`, …). The client
falls back through: exact match → base language (`zh-TW` → `zh`) → `en` →
first non-empty value.

Prefer the object form for new entries. Aim to ship at least `en` and `zh-CN`.

### `config` shape

`config` is a **real JSON object**, not a stringified blob. It is the same
shape the client persists in its mcpServers settings entry:

- **stdio**: `{ "command", "args"?, "env"? }`
- **http / sse**: `{ "url", "headers"? }`

`${PARAM}` placeholders inside string values get substituted with what the user
enters during install (parameter `name` field is the key).

### `detectionHints`

Substring matches checked against the user's installed Claude Desktop / Codex
CLI / Cursor MCP configs (`command + args + url` haystack). If any hint hits,
the marketplace card swaps its primary CTA from **Install** to
**Import from <Client>**, which copies the config including tokens straight
into Ghast — no re-typing.

Hints should be the npm package name (or whatever identifying token shows up
in the `args` array). Two hints per server is usually enough:

```json
"detectionHints": ["@modelcontextprotocol/server-filesystem", "mcp-server-filesystem"]
```

### `transports`

Currently understood: `stdio` · `sse` · `streamable-http`.

---

## Validation

Before pushing:

```bash
# JSON syntax
python3 -m json.tool registry.json > /dev/null
python3 -m json.tool mcp-registry.json > /dev/null
python3 -m json.tool plugins/your-plugin-id/manifest.json > /dev/null
```

Full zod validation runs client-side when the marketplace fetches. Bad entries
simply disappear from the listing with an error in the client console — they
don't break the whole registry.

---

## Versioning

- Bumping a plugin's `version` (in both `manifest.json` and the `registry.json`
  entry) triggers an update notification in installed clients.
- Use semver: patch for fixes, minor for additions, major for breaking changes.
- Removing a plugin from `registry.json` does **not** uninstall it from
  existing clients — it just stops appearing in the marketplace.
- MCP entries don't have versions; they're identified by `id`. Changing
  `installations[].config` rolls out to all marketplace viewers on the next
  refresh.

---

## Contributing

1. Fork.
2. For a plugin: add a directory under `plugins/<id>/` with a valid manifest,
   then add the index entry to `registry.json`.
3. For an MCP server: add an entry under `mcp-registry.json:servers`.
4. Open a PR. CI (forthcoming) will lint the JSON; a maintainer reviews.

Substantial changes — new plugin types, schema fields, registry-level shape —
should start as an issue against the [Ghast client repo](https://github.com/Trapezohe/ghast_desktop)
so the contract stays in sync with what the client actually parses.

---

## License

This registry repository is published under the MIT License. Each plugin under
`plugins/` may declare its own license inside its `manifest.json`; users are
responsible for reading and complying.
