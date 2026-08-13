# chronograph-lp

Analyze private-capital LP portfolios with cashflow forecasts, commitment pacing, look-through exposure, and GP-meeting preparation through Chronograph's official skills and OAuth MCP.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/chronograph-pe/chronograph-lp-claude-plugin` at `6c18b66e882c44db26d88afabc52853ba39dcd98`.

All four workflow skills, their references, the analyst routing content, manifest metadata, and license come from Chronograph's pinned official LP repository. Ghast converts the Claude sub-agent into a portable routing skill and declares the developer-operated MCP endpoint directly.

## Ghast compatibility

- The Codex private app connector is replaced by Chronograph's official hosted MCP endpoint with browser OAuth, public-client authentication, refresh tokens, and PKCE.
- The current official LP release retains and updates cashflow forecasting and GP-meeting prep, and adds commitment pacing plus look-through concentration analysis.
- The portfolio-company one-pager included in the older Codex LP snapshot is now explicitly GP-side in Chronograph's official split release and requires GP-only company financials and gross per-investment returns. Ghast keeps it in the GP package instead of misrepresenting LP permissions.
- A generic private-capital analytics icon is used because the Apache-2.0 repository does not publish separately licensed catalog artwork.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
