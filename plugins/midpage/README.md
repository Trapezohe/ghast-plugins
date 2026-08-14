# midpage

Research US case law, statutes, regulations, and federal dockets, then draft
and cite-check litigation work product with Midpage's official hosted MCP and
MIT-licensed litigation skills.

## Official source

Midpage's public `midpage-ai/litigation-skills` repository is pinned to
revision `a7900c82da0d76a7efdf0f771f2de55c0ae38357` with Git tree `11656b88d900c7c2a484946ab3de62cdb4ba8bb6`. Its complete
30-file inventory has SHA-256
`49d9129118ab412370413da64c92c1eba3f0d7acdb454745106486cfd9b594c2` and includes four skills, their legal-research
guides, and the shared `legal_docx.js` Word renderer under the MIT license.

Ghast preserves `LICENSE`, `UPSTREAM_README.md`, and all four official skill
directories byte-for-byte. The upstream unversioned MCP configuration is
preserved as `UPSTREAM_MCP.json`; Ghast's active `.mcp.json` uses the current
official pinned v3 endpoint `https://app.midpage.ai/mcp/v3`. The repository publishes no reusable
icon, so Ghast adds a generic courthouse-and-search icon rather than copying
private marketplace artwork.

## Portable MCP authentication

- The current official MCP guide is pinned at raw SHA-256
  `f4deb58545d8357404ae43270718cb48cdc2d0e25db634bc4c250e085c2536b2` and documents API-key Bearer authentication plus OAuth.
- Protected-resource metadata is pinned at normalized JSON SHA-256
  `ca090f120f43bac0501e65a3aae92d5c5555fea895603031517cb6c9702424bb`. Clerk authorization and OpenID metadata are
  pinned at `6627f7d4fb4aa8c26815e0b11d673c2d22d89c6cfa00069edabb3e3697a77e9b` and `f28e838f763c580a229cd388bee3f2aaa62397ce0376ea067c346e1ae5a144d0`.
- The OAuth contract publishes dynamic client registration, public clients,
  authorization-code and refresh-token grants, and PKCE S256.
- On August 14, 2026, both missing and deliberately invalid authentication at
  the v3 endpoint returned HTTP 401 with the official protected-resource
  challenge. No account, case, law, docket, filing, credential, or user data
  was accessed.

## Capability comparison

- The Codex snapshot describes case research, opinion review, cited work
  product, statutes and regulations, and research-memo drafting through a
  private app mapping plus the same four litigation skills.
- The current official v3 MCP documents seven tools: `search`,
  `findInOpinion`, `analyzeOpinion`, `analyzeDocketReport`,
  `analyzeDocketFiling`, `searchLaws`, and `analyzeLaw`.
- The four official skills produce court-ready briefs, objective research
  memoranda, public litigation updates, and marked-up Word cite checks.
- The v3 laws tools cover statutes, regulations, constitutions, agency
  guidance, current and historical versions, and official-source links.
- The docket and law tools are preview contracts. Account entitlements,
  coverage, usage, and hosted-service behavior remain controlled by Midpage.
- Ghast adds a separate safety skill for high-stakes review, current primary
  sources, private matter data, docket files, citations, quotations, Word
  output, and authentication hygiene.

Run `scripts/import-midpage-plugin.py` to re-verify the official source,
documentation, OAuth metadata, authentication boundary, and Codex comparison.
