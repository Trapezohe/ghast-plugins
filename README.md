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
├── assets/icon.svg           # required; PNG/JPEG/WebP also supported
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
  "icon": "./assets/icon.svg",
  "skills": "./skills/",
  "commands": "./commands/",
  "mcpServers": "./.mcp.json"
}
```

Every plugin must declare one icon under `./assets/`; the catalog exposes that
asset before installation and the package includes the same file. Only declare
paths that exist. Ghast currently hosts skills, slash commands, and MCP
servers. Open remote MCP plugins can use Ghast's OAuth flow; private connector
IDs tied to another vendor's backend cannot be published as working Ghast
plugins.

## Build the catalog

```bash
python3 scripts/build-ghast-catalog.py
```

The script reads only `.ghast-plugin/plugin.json` sources, creates stable ZIPs,
computes their SHA-256 digests, and rewrites `plugin-catalog.json`.

## Validate the repository

```bash
python3 scripts/validate-ghast-repository.py
```

The validator checks plugin manifests, declared paths, icons, skill
frontmatter, JSON, Python, JavaScript, shell scripts, package layout and
SHA-256 hashes, audit summaries, and common embedded-secret patterns.

## Import connector-free OpenAI plugins

The audited importer handles the OpenAI marketplace snapshot pinned in the
script. It imports only classified plugins without `.app.json`, requires real
license files, strips Codex store metadata, and writes
`openai-portability.json` with the complete decision record.

```bash
python3 scripts/import-openai-portable-plugins.py \
  --source ../openai-plugins \
  --external-root ../upstreams
python3 scripts/sync-plugin-icons.py --openai-source ../openai-plugins
python3 scripts/build-ghast-catalog.py
```

Canonical checkouts used for external license files must be at the exact
revisions declared by the importer. An unfamiliar connector-free plugin causes
the import to fail until it has been reviewed and classified.

## Import audited official plugins

Plugins with a public, developer-owned source repository are regenerated
directly from that repository instead of treating the OpenAI marketplace copy
as canonical.

```bash
python3 scripts/import-official-third-party-plugins.py \
  --source-root ../upstreams
python3 scripts/sync-plugin-icons.py --openai-source ../openai-plugins
python3 scripts/build-ghast-catalog.py
```

Every source checkout must match the exact revision pinned in the importer.
The generated plugin README and audit record preserve provenance, capability
differences, transport substitutions, and any client-specific compatibility
changes for each imported developer-owned source.

## Import audited official hosted MCP adapters

Some developers operate a public hosted MCP server without publishing its
server source. The hosted adapter importer verifies pinned official
documentation and OAuth metadata before generating only Ghast-authored
configuration and safety instructions.

```bash
python3 scripts/import-official-hosted-plugins.py
python3 scripts/sync-plugin-icons.py --openai-source ../openai-plugins
python3 scripts/build-ghast-catalog.py
```

The adapter license applies only to Ghast-authored files. Hosted services,
accounts, data, trademarks, permissions, and service terms remain controlled
by their operators.

## Import the Binance plugin

The Binance importer pins the official Skills Hub revision and copies the four
skill directories that contain standalone MIT license files. It also adds a
Ghast financial-execution policy and changes the Onchain Pay helper so secrets
come from environment variables instead of process arguments.

```bash
python3 scripts/import-binance-plugin.py \
  --source ../upstreams/binance-skills-hub
python3 scripts/sync-plugin-icons.py --openai-source ../openai-plugins
python3 scripts/build-ghast-catalog.py
```

## Import the BrightHire plugin

The BrightHire importer verifies the official developer-owned plugin source,
public hosted MCP endpoint, OAuth metadata, anonymous authentication boundary,
and the pinned OpenAI capability evidence. It generates only independently
authored Ghast adapter files and generic artwork because the official source
declares MIT in its manifest but does not contain an actual license text.

```bash
python3 scripts/import-brighthire-plugin.py \
  --openai-source ../openai-plugins \
  --official-source ../upstreams/brighthire-codex-plugin
```

For a deliberate one-time public OAuth registration test, add
`--verify-registration`. The returned client value is not retained.

## Import the Morningstar plugin

The Morningstar importer verifies the official developer-owned plugin source,
hosted MCP endpoint, OAuth metadata, anonymous authentication boundary, five
official workflow categories, and the pinned OpenAI capability evidence. It
generates independently authored adapter materials because the official source
declares MIT in its manifest without including license text.

```bash
python3 scripts/import-morningstar-plugin.py \
  --openai-source ../openai-plugins \
  --official-source ../upstreams/morningstar-plugins
```

Add `--verify-registration` only for a deliberate one-time confidential OAuth
client registration check. The returned client ID and secret are not retained.

## Audit third-party Codex plugins

`third-party-plugin-audit.json` tracks every marketplace plugin whose declared
developer is not OpenAI. A plugin is marked complete only after its official
developer source, exact revision, license, Codex capability set, Ghast
capability set, and runnable verification have been recorded in
`third-party-plugin-reviews.json`.

```bash
python3 scripts/audit-third-party-plugins.py \
  --source ../openai-plugins
```

The generated `THIRD_PARTY_PLUGIN_AUDIT.md` is the readable inventory. A
developer name or an MIT string in the Codex manifest is not sufficient
evidence that the connector implementation itself can be redistributed.

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
