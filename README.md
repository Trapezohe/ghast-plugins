# Ghast Plugins & MCP Registry

Ghast's public plugin catalog. The desktop client downloads
`plugin-catalog.json`, verifies each package's SHA-256 digest, and installs the
selected bundle into the active profile.

## Repository layout

| Path | Purpose |
| --- | --- |
| `plugins/<name>/` | Ghast-native plugin sources |
| `packages/<name>.zip` | Deterministic downloadable packages |
| `plugin-catalog.json` | Package metadata consumed by Ghast |
| `mcp-registry.json` | Standalone MCP marketplace |

## Plugin format

Every plugin uses Ghast's native declarative format:

```text
plugins/<name>/
├── .ghast-plugin/plugin.json
├── commands/                  # optional slash commands
├── skills/                    # optional model-invoked skills
├── .mcp.json                  # optional MCP servers
├── README.md                  # optional
└── LICENSE                    # required for third-party ports
```

Minimal manifest:

```json
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "What the plugin adds.",
  "author": { "name": "Your Name" },
  "skills": "./skills/",
  "commands": "./commands/",
  "mcpServers": "./.mcp.json"
}
```

Only declare paths that exist. Ghast currently hosts skills, slash commands,
and MCP servers. Connector apps need a Ghast connector implementation before
they can be published.

## Build the catalog

```bash
python3 scripts/build-ghast-catalog.py
```

The script reads only `.ghast-plugin/plugin.json` sources, creates stable ZIPs,
computes their SHA-256 digests, and rewrites `plugin-catalog.json`.

## Porting an external plugin

External Codex, Claude, and Agent Plugin bundles are source material, not a
runtime dependency:

1. Verify the upstream repository, exact revision, and redistribution license.
2. Copy only contributions Ghast actually supports.
3. Replace the source manifest with `.ghast-plugin/plugin.json`.
4. Remove connector-app declarations unless a Ghast connector exists.
5. Include the upstream license and provenance in the plugin directory.
6. Build the catalog and install the generated package through Ghast before
   publishing it.

Users may also install an external Ghast plugin directory directly from
Settings. Third-party catalogs can be loaded by URL; their packages must use
HTTPS and provide a valid SHA-256 digest.

## Contribution policy

Add the plugin source under `plugins/<name>/`, run the catalog builder, and
commit both the source and generated package/catalog changes. Do not mirror an
external marketplace wholesale: each plugin must be licensed, reviewed, and
verified against Ghast's real runtime.
