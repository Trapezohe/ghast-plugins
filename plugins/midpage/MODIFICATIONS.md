# Modifications

Ghast packages selected files from Midpage's official litigation-skills
repository at `a7900c82da0d76a7efdf0f771f2de55c0ae38357`.

Unmodified upstream files:

- `LICENSE`
- `UPSTREAM_README.md` (renamed from upstream `README.md`)
- `UPSTREAM_MCP.json` (renamed from upstream `.mcp.json`)
- `skills/cite-check/**`
- `skills/draft-brief/**`
- `skills/draft-long-form-memo/**`
- `skills/litigation-update-post/**`

Ghast-authored additions:

- `.ghast-plugin/plugin.json`
- `.mcp.json`, pinned to the documented v3 endpoint `https://app.midpage.ai/mcp/v3`
- `README.md`
- `MODIFICATIONS.md`
- `assets/icon.svg`
- `skills/midpage-safety/SKILL.md`

The renamed files and official skill directories are byte-identical to the
upstream source. The v3 endpoint is an official documented endpoint and is
used to keep a stable seven-tool contract, including the preview docket and
laws tools. All additions are distributed under the included MIT license.
