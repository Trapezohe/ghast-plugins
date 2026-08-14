# Midpage Litigation — Codex plugin

A suite of litigation skills for [Codex](https://developers.openai.com/codex), built on the
[Midpage](https://www.midpage.ai) MCP. Each skill is a finished-deliverable workflow: the model
researches against Midpage's case-law tools (`search`, `analyzeOpinion`, `findInOpinion`,
`analyzeDocketReport`, `analyzeDocketFiling`) and never asserts law, rules, or record facts
from memory — every citation links to ground truth.

## Skills

| Skill | Deliverable |
|---|---|
| `draft-brief` | A court-ready filing (brief, motion, appellate brief — not complaints), research-led, rule-compliant, every cite linked |
| `draft-long-form-memo` | The classic objective research memorandum — predicts, doesn't advocate |
| `litigation-update-post` | A public firm-style blog post, client alert, or social post, public sources only, with disclaimer |
| `cite-check` | PDF/Word in → a marked-up .docx out: cover page, the document recreated exactly, every finding as a Word comment or redline |

Each skill folder is self-contained: its `SKILL.md`, shared method guides under `references/`
(citations, litigation writing, court rules, Word rendering), and `scripts/legal_docx.js` —
the single Word renderer all skills use (requires the `docx` npm package; the skills install
it with `npm install docx` in the working directory, Node 18+).

## Requirements

- **Midpage MCP** — the skills orchestrate Midpage's legal-research tools and degrade
  honestly without them (they say what they could not verify rather than guessing). A
  [Midpage](https://www.midpage.ai) subscription is required.
- **Code execution with Node 18+** for Word (.docx) deliverables.

## Layout

```
.codex-plugin/plugin.json   plugin manifest
.mcp.json                   Midpage MCP server config
skills/<name>/              one self-contained skill per folder
  SKILL.md
  references/               shared method guides + skill-specific references
  scripts/                  legal_docx.js (+ skill-specific scripts)
```

## Provenance

This repo is the distribution artifact for Codex. The skills are developed and exported from
Midpage's internal repository; edits land there first and are re-exported here.
