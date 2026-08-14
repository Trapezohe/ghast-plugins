# Modifications

Primary official source: `https://github.com/Zoominfo/gtm-ai-cli` at `f63a6d86bcd732c63f731c858e312d631f31b9a5`.

Additional official source for the icon and MCP comparison:
`https://github.com/Zoominfo/zoominfo-mcp-plugin` at `3ec997a1ffaaa8d5d98d81b6b9d8c3fdafab6420`.

Unmodified upstream files:

- `LICENSE` from the official CLI repository
- `UPSTREAM_SKILL.md` from `.claude/skills/gtm-ai-cli/SKILL.md`
- `UPSTREAM_CLI_README.md` from the npm package
- `UPSTREAM_CLI_PACKAGE.json` from the npm package
- `UPSTREAM_MCP_PLUGIN_LICENSE.md` from the official MCP plugin repository
- `assets/icon.svg` from `assets/zoominfo-logomark-red.svg`

Ghast-authored or adapted files:

- `.ghast-plugin/plugin.json`
- `README.md`
- `MODIFICATIONS.md`
- `skills/gtm-ai-cli/SKILL.md`, mechanically adapted from the official skill
  to call the bundled launcher, avoid direct credential-file deletion, and
  require confirmation for external writes
- `skills/gtm-ai-cli/scripts/gtm.mjs`, a path-resolving launcher for the
  security-rebuilt official executable
- `vendor/gtm-ai-cli/gtm.bundle.mjs`, built from unmodified official v1.0.1
  TypeScript source after applying only compatible dependency resolutions in
  a build-only lockfile
- `SECURITY_BUILD.json`, the exact source, npm evidence, lockfile, bundle,
  production-audit, and bundled-package hashes
- `THIRD_PARTY_NOTICES.md`, generated from the license files of every package
  identified by Bun's build metafile as included in the executable

The official npm bundle is retained only as pinned verification evidence and
is not included as the runtime. The adapted files are distributed under the
included MIT license. No hosted MCP implementation, OpenAI connector, account
data, credential, token, or ZoomInfo customer record is included.
