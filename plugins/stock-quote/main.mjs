// stock-quote — Yahoo Finance v8 chart endpoint. Public, no auth.
// Returns latest close + previous close, computes intraday change.
// Data is delayed 15 minutes per Yahoo's terms.
//
// Inspired by lobe-chat-plugins' `StockData` and `savvy_trader_ai`. We
// hit Yahoo directly so it doesn't matter when those CDNs disappear.

const CHART_BASE = "https://query1.finance.yahoo.com/v8/finance/chart";

export function activate(context) {
  const handle = context.tools.register("get_quote", {
    description:
      "Return the latest price for a stock or index ticker (Yahoo Finance " +
      "symbol). Includes regular-market price, previous close, day change " +
      "%, volume, and 52-week high/low. Data is delayed ~15 minutes per " +
      "Yahoo's terms — clearly state that to the user.",
    parameters: {
      type: "object",
      properties: {
        symbol: {
          type: "string",
          description:
            "Yahoo Finance ticker, e.g. `AAPL`, `TSLA`, `^GSPC` (S&P 500), `BTC-USD`.",
        },
      },
      required: ["symbol"],
    },
    execute: async (args = {}) => {
      const { symbol } = args ?? {};
      if (typeof symbol !== "string" || !symbol.trim()) {
        throw new Error("`symbol` is required.");
      }
      const url = `${CHART_BASE}/${encodeURIComponent(symbol)}?range=1d&interval=1m`;
      const response = await fetch(url, {
        headers: {
          "User-Agent":
            "Mozilla/5.0 (Trapezohe-Ghast/0.1) stock-quote",
          Accept: "application/json",
        },
      });
      if (!response.ok) {
        throw new Error(`Yahoo Finance HTTP ${response.status}`);
      }
      const payload = await response.json();
      const result = payload?.chart?.result?.[0];
      if (!result) {
        const err = payload?.chart?.error?.description ?? "no data";
        throw new Error(`No data for ${symbol}: ${err}`);
      }
      const meta = result.meta ?? {};
      const last = meta.regularMarketPrice;
      const prev = meta.chartPreviousClose ?? meta.previousClose;
      const change = typeof last === "number" && typeof prev === "number"
        ? last - prev
        : null;
      const changePct = change != null && prev ? (change / prev) * 100 : null;
      return {
        symbol: meta.symbol,
        exchange: meta.exchangeName,
        currency: meta.currency,
        price: last,
        previousClose: prev,
        change,
        changePercent: changePct,
        dayHigh: meta.regularMarketDayHigh ?? null,
        dayLow: meta.regularMarketDayLow ?? null,
        volume: meta.regularMarketVolume ?? null,
        fiftyTwoWeekHigh: meta.fiftyTwoWeekHigh ?? null,
        fiftyTwoWeekLow: meta.fiftyTwoWeekLow ?? null,
        marketState: meta.marketState ?? null,
        regularMarketTime: meta.regularMarketTime
          ? new Date(meta.regularMarketTime * 1000).toISOString()
          : null,
        attribution: "Quote data delayed ~15 min via Yahoo Finance.",
      };
    },
  });

  return { dispose: () => handle.dispose() };
}
