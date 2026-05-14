// defillama — DeFi data lookup via DeFi Llama's free public API
// (api.llama.fi). No auth, no rate limit headers.
//
// Inspired by lobe-chat-plugins' `defillama`. No remote service —
// queries DeFi Llama directly from the host.

const BASE = "https://api.llama.fi";
const COINS = "https://coins.llama.fi";

export function activate(context) {
  const protocolHandle = context.tools.register("get_protocol", {
    description:
      "Return current TVL, market cap, chain breakdown, and project URL for a " +
      "DeFi protocol. Pass `slug` as it appears in the DeFi Llama URL " +
      "(e.g. `aave-v3`, `uniswap-v3`, `lido`). Lower-case, hyphens.",
    parameters: {
      type: "object",
      properties: {
        slug: {
          type: "string",
          description: "DeFi Llama protocol slug.",
        },
      },
      required: ["slug"],
    },
    execute: async (args = {}) => {
      const { slug } = args ?? {};
      if (typeof slug !== "string" || !/^[a-z0-9-]+$/.test(slug)) {
        throw new Error("`slug` must be lowercase letters/digits/hyphens.");
      }
      const data = await fetchJson(`${BASE}/protocol/${slug}`);
      const chainTvls = {};
      for (const [chain, info] of Object.entries(data.currentChainTvls ?? {})) {
        chainTvls[chain] = Math.round(Number(info));
      }
      return {
        name: data.name,
        slug: data.slug,
        symbol: data.symbol ?? null,
        category: data.category,
        description: data.description,
        url: data.url,
        twitter: data.twitter ?? null,
        currentTvlUsd: Math.round(Number(data.tvl?.at?.(-1)?.totalLiquidityUSD ?? data.tvl ?? 0)),
        marketCapUsd: data.mcap ?? null,
        chains: data.chains ?? [],
        chainTvls,
      };
    },
  });

  const topHandle = context.tools.register("list_top_protocols", {
    description:
      "List DeFi protocols sorted by total value locked (TVL). Returns up to " +
      "`limit` entries with their slug, category, chains, and current TVL in USD.",
    parameters: {
      type: "object",
      properties: {
        limit: { type: "integer", minimum: 1, maximum: 30, default: 10 },
        category: {
          type: "string",
          description: "Optional category filter (e.g. `Dexs`, `Lending`, `Yield`).",
        },
      },
    },
    execute: async (args = {}) => {
      const { limit = 10, category } = args ?? {};
      const safeLimit = Math.max(1, Math.min(30, Number(limit) || 10));
      const all = await fetchJson(`${BASE}/protocols`);
      const filtered = category
        ? all.filter((p) => (p.category ?? "").toLowerCase() === category.toLowerCase())
        : all;
      const sorted = filtered
        .filter((p) => typeof p.tvl === "number" && p.tvl > 0)
        .sort((a, b) => b.tvl - a.tvl)
        .slice(0, safeLimit);
      return {
        category: category ?? "all",
        count: sorted.length,
        protocols: sorted.map((p) => ({
          name: p.name,
          slug: p.slug,
          category: p.category,
          chains: p.chains,
          tvlUsd: Math.round(p.tvl),
          change1d: p.change_1d ?? null,
          change7d: p.change_7d ?? null,
          url: p.url,
        })),
      };
    },
  });

  return {
    dispose: () => {
      protocolHandle.dispose();
      topHandle.dispose();
    },
  };
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      "User-Agent":
        "Trapezohe-Ghast/0.1 (+https://ghast.trapezohe.ai) defillama",
    },
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} from ${url}`);
  }
  return response.json();
}

// keep COINS reachable for future use (price queries) without an unused-var warning
void COINS;
