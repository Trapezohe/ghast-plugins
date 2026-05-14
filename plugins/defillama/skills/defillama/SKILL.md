---
name: defillama
description: Use this skill when the user asks about DeFi protocols, TVL (total value locked), chain-by-chain breakdowns, top DeFi protocols, or specific protocols like Aave, Uniswap, Lido, etc. Hits the free DeFi Llama public API (no key).
version: 1.0.0
allowed-tools: [WebFetch]
---

# DeFi Llama

When the user asks about DeFi data — "what's the TVL of Aave", "show me the
top 10 DeFi protocols", "how much value is on Arbitrum" — use this skill.

## Endpoints (no auth)

Base: `https://api.llama.fi`

| What | URL |
| --- | --- |
| All protocols (sorted by TVL) | `/protocols` |
| Single protocol detail | `/protocol/<slug>` |
| Chains summary | `/chains` |
| Historical TVL for a protocol | `/protocol/<slug>` (look at the `tvl` time series) |

Slugs are lowercase + hyphens (`aave-v3`, `uniswap-v3`, `lido`,
`makerdao`, `curve-dex`).

## Use patterns

### "Top 10 DeFi protocols"

`WebFetch https://api.llama.fi/protocols`, sort by `tvl` desc, take top 10,
present name/category/chains/TVL ($X.XB) in a numbered list.

### "TVL of Aave"

`WebFetch https://api.llama.fi/protocol/aave-v3`. Extract `name`,
`currentChainTvls` (per-chain $), `chains`, `category`, `url`, `twitter`.
Show the current total + top 3 chains by TVL.

### "Top protocols by category"

Filter `/protocols` by `category == "Dexs"` or `"Lending"` or `"Yield"`
before sorting.

## Output

Use compact USD formatting: `$12.4B`, `$890M`, `$45K`. Always link to
`https://defillama.com/protocol/<slug>` so the user can drill in.

## Caveats

- TVL numbers are snapshot — DeFi Llama updates roughly hourly.
- Cross-chain protocols sum across chains; per-chain breakdown is in
  `currentChainTvls`.
- "Stablecoins" and "Bridges" are separate categories with their own
  endpoints (`/stablecoins`, `/bridges`). Mention if the user asks
  about either.
