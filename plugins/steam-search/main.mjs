// steam-search — Steam store search + appdetails lookups. Both are
// undocumented but stable public endpoints used by the Steam web site
// itself. No auth, no API key.
//
// Inspired by lobe-chat-plugins' `steam` and `GameSight`.

const SEARCH_URL = "https://store.steampowered.com/api/storesearch";
const APP_URL = "https://store.steampowered.com/api/appdetails";

export function activate(context) {
  const searchHandle = context.tools.register("search_steam", {
    description:
      "Search the Steam store by keyword. Returns up to `limit` matching " +
      "games with name, AppID, price, and Steam URL. Use this to find a " +
      "game's AppID before calling `get_steam_app`.",
    parameters: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search keyword." },
        limit: { type: "integer", minimum: 1, maximum: 20, default: 5 },
        region: {
          type: "string",
          description: "ISO country code for store region (default `US`).",
          default: "US",
        },
      },
      required: ["query"],
    },
    execute: async (args = {}) => {
      const { query, limit = 5, region = "US" } = args ?? {};
      if (typeof query !== "string" || !query.trim()) {
        throw new Error("`query` is required.");
      }
      const url =
        `${SEARCH_URL}/?term=${encodeURIComponent(query)}` +
        `&l=english&cc=${region.toUpperCase()}`;
      const data = await fetchJson(url);
      const items = (data?.items ?? []).slice(0, Math.min(20, Number(limit) || 5));
      return {
        query,
        count: items.length,
        items: items.map((it) => ({
          appId: it.id,
          name: it.name,
          price: it.price
            ? {
                final: it.price.final / 100,
                currency: it.price.currency,
                discountPercent: it.price.discount_percent ?? 0,
              }
            : null,
          metascore: it.metascore || null,
          platforms: it.platforms,
          tinyImage: it.tiny_image ?? null,
          url: `https://store.steampowered.com/app/${it.id}/`,
        })),
      };
    },
  });

  const appHandle = context.tools.register("get_steam_app", {
    description:
      "Look up a Steam app by its numeric AppID. Returns full description, " +
      "tags, release date, developer, supported platforms, and current price.",
    parameters: {
      type: "object",
      properties: {
        appId: { type: "integer", description: "Numeric Steam AppID." },
        region: {
          type: "string",
          default: "US",
          description: "ISO country code for pricing region.",
        },
      },
      required: ["appId"],
    },
    execute: async (args = {}) => {
      const { appId, region = "US" } = args ?? {};
      if (!Number.isInteger(appId)) {
        throw new Error("`appId` must be an integer.");
      }
      const data = await fetchJson(
        `${APP_URL}/?appids=${appId}&cc=${region.toUpperCase()}&l=english`,
      );
      const entry = data?.[appId];
      if (!entry?.success || !entry.data) {
        throw new Error(`Steam AppID ${appId} not found.`);
      }
      const d = entry.data;
      return {
        appId,
        name: d.name,
        type: d.type,
        shortDescription: d.short_description,
        developers: d.developers ?? [],
        publishers: d.publishers ?? [],
        platforms: d.platforms,
        releaseDate: d.release_date?.date ?? null,
        comingSoon: d.release_date?.coming_soon ?? false,
        price: d.is_free
          ? { free: true }
          : d.price_overview
          ? {
              final: d.price_overview.final / 100,
              initial: d.price_overview.initial / 100,
              currency: d.price_overview.currency,
              discountPercent: d.price_overview.discount_percent,
            }
          : null,
        genres: (d.genres ?? []).map((g) => g.description),
        categories: (d.categories ?? []).map((c) => c.description),
        metacritic: d.metacritic ?? null,
        url: `https://store.steampowered.com/app/${appId}/`,
        headerImage: d.header_image ?? null,
      };
    },
  });

  return {
    dispose: () => {
      searchHandle.dispose();
      appHandle.dispose();
    },
  };
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      "User-Agent":
        "Trapezohe-Ghast/0.1 (+https://ghast.trapezohe.ai) steam-search",
      Accept: "application/json",
    },
  });
  if (!response.ok) {
    throw new Error(`Steam HTTP ${response.status} from ${url}`);
  }
  return response.json();
}
