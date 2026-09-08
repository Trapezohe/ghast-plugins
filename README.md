# Ghast Plugins

Extend Ghast with skills, service connections, commands, and lifecycle hooks.

**English** · [简体中文](README.zh-CN.md)

This repository contains Ghast’s public plugin catalog, plugin sources, and downloadable packages. Browse 500+ plugins across developer tools, data, productivity, communication, design, marketing, and finance in the Ghast desktop app.

[Browse plugin sources](plugins/) · [Download catalog](plugin-catalog.json) · [Upstream maintenance](maintenance/README.md)

## Get started

1. Open **Plugins** in Ghast and select **Browse**.
2. Search for a plugin, open its details, and select **Install**.
3. If it connects to a service, complete the setup under **Service connections**. Requirements vary by provider: OAuth, an API key, or a local runtime.
4. Use the plugin in a conversation. Its README describes available capabilities and any prerequisites.

Installing a package does **not** grant access to your accounts. Installation, service authorization, and successful tool execution are separate checks. Manage installed plugins from the **Installed** tab.

Ghast’s default catalog URL is:

```text
https://raw.githubusercontent.com/trapezohe/ghast-plugins/main/plugin-catalog.json
```

Ghast verifies each downloaded package against its catalog SHA-256 digest before installation. These are Ghast-compatible packages; they do not reuse a Codex account, private connector backend, or installed plugin cache.

## What plugins can add

| Capability | Purpose | Example |
| --- | --- | --- |
| Skills | Instructions and workflows for specific tasks | [Binance](plugins/binance/) |
| MCP connections | Tools and data from a service or local server | [GitHub](plugins/github/), [Cloudflare](plugins/cloudflare/), [Supabase](plugins/supabase/) |
| Commands | Explicit entry points for repeatable workflows | See each plugin’s command definitions |
| Lifecycle hooks | Add context when supported conversation events occur | [Ponytail](plugins/ponytail/) |

Plugins can combine capabilities. Available tools, permissions, and runtime requirements depend on the individual plugin and your Ghast version. Hook support currently covers `SessionStart`, `UserPromptSubmit`, and `SubagentStart`; it does not imply support for every hook event from other clients.

Explore [Google Gmail](plugins/google-gmail/), [Google Docs](plugins/google-docs/), [Google Sheets](plugins/google-sheets/), [Microsoft Work IQ](plugins/microsoft-workiq/), [Notion](plugins/notion/), and [Slack](plugins/slack/) for office and collaboration workflows. The catalog includes both account-backed connections and plugins that need no account.

## Sources and store standards

New service connectors must use a provider-published or provider-maintained implementation. A marketplace listing alone does not establish official ownership. Community connectors require an explicit exception and must be identified as such.

A Ghast-authored adapter for an official service is not a provider-authored plugin. Each package must document its actual source, authorship, license, and adaptation details.

Every official store listing must include:

- A real brand logo, bundled locally with its source recorded.
- English and Simplified Chinese introductions. Chinese UI locales display Chinese; all other locales display English. The two are not concatenated.
- Verified upstream documentation or repository provenance, plus the applicable license for redistributed files.
- A usable contribution and documented setup requirements. Private app IDs from another client are not a working connection.
- Local installation, branding, and uninstall verification before publication. Account and tool checks must be reported separately.

Never commit tokens, client secrets, or account credentials. Do not duplicate one connector into multiple listings just to increase the catalog count.

## Repository map

| Path | Contents |
| --- | --- |
| [`plugins/`](plugins/) | Plugin source directories and per-plugin documentation |
| [`packages/`](packages/) | Generated, deterministic ZIP packages |
| [`plugin-catalog.json`](plugin-catalog.json) | Package metadata, URLs, and SHA-256 digests used by Ghast |
| [`mcp-registry.json`](mcp-registry.json) | Separate registry for standalone MCP servers |
| [`scripts/`](scripts/) | Catalog build, validation, import, and audit tools |
| [`maintenance/`](maintenance/) | Upstream inventory, update policy, and maintenance instructions |

## Contribute a plugin

Packages use the vendor-neutral Agent Plugins 1.0 format with a root `plugin.json`. Skills live in `skills/` and MCP configuration in `mcp.json`. Ghast-specific metadata belongs under `extensions.ai.trapezohe.ghast`.

Start from a plugin with the same capabilities. Use [GitHub](plugins/github/) for a service connection or [Ponytail](plugins/ponytail/) for a hook plugin. Only include files your plugin needs.

```text
plugins/<name>/
├── plugin.json                  # Manifest and Ghast metadata
├── details.json                 # Localized overview, three examples, and official links
├── assets/                      # Brand logo
├── skills/                      # Optional skills
├── mcp.json                     # Optional MCP configuration
├── ai.trapezohe.ghast/commands/  # Optional Ghast commands
├── hooks/                       # Optional hooks, declared in the Ghast extension
├── README.md                    # Setup, capabilities, provenance, and limitations
└── LICENSE                      # Applicable redistribution license
```

Set `descriptions.en` and `descriptions.zh-CN` in the Ghast extension, and keep the root `description` equal to the English text. Choose a canonical category from [`scripts/plugin_categories.py`](scripts/plugin_categories.py).

Each plugin owns its `details.json`: `overview` and exactly three `starterPrompts` contain `en` and `zh-CN` text. Optional links are `websiteUrl`, `repositoryUrl`, `documentationUrl`, `privacyPolicyUrl`, and `termsOfServiceUrl`; only publish verified official links and retain their evidence in `sources`. Chinese locales show Chinese text; other locales use English. Edit this file in the plugin directory, not a shared descriptions file. Preserve it when importing upstream updates.

The generated catalog contains only a details URL and SHA-256 digest. Ghast loads the full text when opening a plugin, verifies its digest, and reads installed details from the local package without a network request.

From the repository root, prepare the validation environment and rebuild:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-agent-plugins.txt
python scripts/build-ghast-catalog.py
python scripts/validate-ghast-repository.py
```

CI uses Python 3.12 and Node.js 24. Keep Node.js and Bash available for script checks. Validation covers manifests, MCP configuration, skills, icons, script syntax, package layout, hashes, and common embedded-secret patterns; it does not prove a live account connection works.

Install the generated package in Ghast, check its visible presentation and relevant runtime behavior, then uninstall the test installation. Submit the source changes together with regenerated packages and catalog in a pull request. Preserve upstream licenses and record any compatibility changes. Import scripts are for reviewed, pinned upstream sources—not wholesale marketplace mirroring.

## Versions

Plugin versions come from verified upstream manifests or official releases, without a Ghast suffix. The source, packaged revision, and evidence digest are recorded in `maintenance/upstreams.json` under `versionSource`. When no verified upstream package version is available, the manifest omits `version`; an API protocol version or unrelated repository package version is not substituted.

The catalog builder applies this policy to source manifests before packaging, including legacy importer output. When updating an upstream snapshot, refresh its version evidence at the same time. A version for a different packaged revision fails validation. Changes to Ghast adapters, translations, or logos are tracked by Git and the package SHA-256 digest; the client can detect changed content even when the upstream version is unchanged.

## Keeping plugins current

The maintenance workflow is configured to check upstreams daily and collect changes into a single review PR. **PR creation still requires activation:** GitHub Actions must be allowed to create pull requests in the repository settings.

Automatic discovery is broader than automatic rewriting. The current inventory covers GitHub revisions, npm/PyPI releases, and literal HTTPS endpoints; unsupported sources require manual review. Ponytail currently has a guarded file-update mapping. Other detected changes produce review information rather than silently replacing plugin contents.

Updates are not automatically merged. An endpoint response is not a full MCP or account test, and catalog maintenance does not automatically upgrade users’ installed plugins.

See the [maintenance guide](maintenance/README.md) for scheduling, permissions, checks, failure reporting, and current limits.

## Licenses

Licenses are defined per plugin. Check its manifest, README, and bundled license before redistributing it. An adapter’s license does not license the provider’s hosted service, trademarks, or user data; the provider’s terms still apply.
