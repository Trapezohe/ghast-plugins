---
name: stock-quote
description: Use this skill when the user asks for the price of a stock, ETF, index, or crypto ticker (e.g. AAPL, TSLA, ^GSPC, BTC-USD). Returns a delayed quote via Yahoo Finance's public chart endpoint — no API key required.
version: 1.0.0
allowed-tools: [WebFetch, Bash]
---

# Stock Quote (Yahoo Finance)

When the user asks "what's AAPL trading at", "price of TSLA", "S&P 500 today",
"BTC price", use this skill instead of guessing.

## Endpoint

```
https://query1.finance.yahoo.com/v8/finance/chart/<SYMBOL>?range=1d&interval=1m
```

Yahoo accepts:

| Asset | Symbol shape | Example |
| --- | --- | --- |
| US stock | upper-case ticker | `AAPL`, `TSLA`, `NVDA` |
| Index | caret prefix | `^GSPC` (S&P 500), `^DJI`, `^IXIC` |
| Crypto | `<CRYPTO>-<FIAT>` | `BTC-USD`, `ETH-USD` |
| Non-US stock | `<TICKER>.<EXCHANGE>` | `7203.T` (Toyota), `BABA.HK` |

## Fetch

Use `WebFetch` (or `curl` via `Bash` with a real User-Agent — Yahoo blocks
default `curl/*` UAs):

```bash
curl -sS -H 'User-Agent: Mozilla/5.0' \
  'https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=1d&interval=1m'
```

## Extract

The relevant payload is at `chart.result[0].meta`:

- `symbol`, `exchangeName`, `currency`
- `regularMarketPrice` — current price
- `chartPreviousClose` / `previousClose` — prior session close
- `regularMarketDayHigh`, `regularMarketDayLow`, `regularMarketVolume`
- `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`
- `marketState` (`REGULAR`, `CLOSED`, `PRE`, `POST`)
- `regularMarketTime` (unix seconds)

Compute day change: `last - prevClose`, day change %: `(change / prevClose) * 100`.

## Output

> **AAPL** (NASDAQ, USD) — **$189.42** ▲ +1.34 (+0.71%)
> Day range: 187.10 – 189.85 · Vol 38.2M · 52w: 142.10 – 199.62
> Quote delayed ~15 min. Market: regular hours.

## Important: state the delay

Yahoo's free chart endpoint is delayed by ~15 minutes per their terms. Always
tell the user the data isn't real-time when reporting a quote. Do NOT use
this skill for active trading decisions — recommend the user check their
broker for live prices.
