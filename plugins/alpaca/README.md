# Alpaca Trading API

Research stocks, options, crypto, fixed income, indices, news, and corporate actions through Alpaca's official market-data MCP, with separately authorized paper and live trading servers for account, order, position, portfolio, and watchlist workflows.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/alpacahq/agentic` at `a97b49ecdf47b6b46d8fc1027139c475296dc696`.

The three OAuth MCP declarations, public Codex client ID, icon, manifest metadata, and license are copied from Alpaca's pinned official agent-plugin repository. Ghast adds one safety and routing skill; the hosted services remain operated by Alpaca.

## Ghast compatibility

- The Codex private market-data connector is replaced by Alpaca's official public market-data MCP endpoint. The same official repository also supplies distinct paper and live trading endpoints.
- Market-data tools are the default route for quotes, bars, trades, snapshots, option chains, news, indices, fixed income, and corporate actions. The trading endpoints are used only when the user explicitly requests account or order workflows.
- Paper and live accounts remain separate authorization contexts. Live trading requires the user to explicitly say that the action is for a live account and freshly confirm the complete order or portfolio mutation.
- The complete authenticated hosted tool inventory was not enumerated without an Alpaca account. Tool availability, market-data freshness, subscriptions, asset eligibility, and trading permissions remain account-dependent.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
