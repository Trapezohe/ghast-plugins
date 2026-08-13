# chronograph-gp

Analyze private-capital GP portfolios, operating performance, valuations, fund reviews, company reports, and TVPI attribution through Chronograph's official skills and hosted OAuth MCP.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/chronograph-pe/chronograph-gp-claude-plugin` at `88a4290f29009e1cfe4341e0b9518d23c537d853`.

All five workflow skills, their references, the analyst routing content, manifest metadata, and license come from Chronograph's pinned official GP repository. Ghast converts the Claude sub-agent into a portable routing skill and declares the developer-operated MCP endpoint directly.

## Ghast compatibility

- The Codex private app connector is replaced by Chronograph's official hosted MCP endpoint with browser OAuth, public-client authentication, refresh tokens, and PKCE.
- The current official GP release expands the older Codex one-pager package with budget-versus-actuals, quarterly review packs, markup/markdown briefs, and company-level TVPI attribution.
- GP-authenticated access is mandatory for company financials and gross per-investment returns. Ghast does not substitute LP net figures or present an LP login as GP capability.
- A generic private-capital analytics icon is used because the Apache-2.0 repository does not publish separately licensed catalog artwork.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
