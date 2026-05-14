// bilibili-search — public Bilibili web search + ranking endpoints.
//
// Bilibili rate-limits anonymous traffic aggressively and recently
// started requiring a `wbi` signature for some search endpoints. The
// `/x/web-interface/search/all/v2` endpoint still works without a
// signature for basic queries (verified late 2024), but the host may
// return `-412` on rapid repeat calls — we surface that error clearly
// instead of throwing a generic HTTP failure.
//
// Inspired by lobe-chat-plugins' `bilibili`.

const SEARCH_URL = "https://api.bilibili.com/x/web-interface/search/all/v2";
const RANKING_URL = "https://api.bilibili.com/x/web-interface/ranking/v2";

export function activate(context) {
  const searchHandle = context.tools.register("search_videos", {
    description:
      "Search Bilibili by keyword and return up to `limit` matching videos " +
      "with title, BVID, uploader name, view count, and direct URL. Bilibili " +
      "may rate-limit aggressively — if a call returns an error, wait a few " +
      "seconds before retrying.",
    parameters: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search keyword (any language)." },
        limit: { type: "integer", minimum: 1, maximum: 20, default: 8 },
      },
      required: ["query"],
    },
    execute: async (args = {}) => {
      const { query, limit = 8 } = args ?? {};
      if (typeof query !== "string" || !query.trim()) {
        throw new Error("`query` is required.");
      }
      const url = `${SEARCH_URL}?keyword=${encodeURIComponent(query)}&search_type=video`;
      const data = await biliFetch(url);
      const videoResults =
        (data?.result ?? []).find((entry) => entry.result_type === "video")?.data ?? [];
      const trimmed = videoResults.slice(
        0,
        Math.max(1, Math.min(20, Number(limit) || 8)),
      );
      return {
        query,
        count: trimmed.length,
        items: trimmed.map((video) => ({
          bvid: video.bvid,
          aid: video.aid,
          title: stripTags(video.title ?? ""),
          author: video.author,
          mid: video.mid,
          duration: video.duration,
          play: video.play,
          danmaku: video.video_review ?? video.danmaku ?? null,
          favorites: video.favorites ?? null,
          uploaded: video.pubdate
            ? new Date(video.pubdate * 1000).toISOString()
            : null,
          description: video.description,
          url: `https://www.bilibili.com/video/${video.bvid}`,
          cover: video.pic
            ? video.pic.startsWith("//")
              ? `https:${video.pic}`
              : video.pic
            : null,
        })),
      };
    },
  });

  const trendingHandle = context.tools.register("list_trending", {
    description:
      "Return the current Bilibili daily ranking (top videos site-wide). " +
      "Use this when the user asks what's trending on Bilibili today.",
    parameters: {
      type: "object",
      properties: {
        limit: { type: "integer", minimum: 1, maximum: 30, default: 10 },
      },
    },
    execute: async (args = {}) => {
      const { limit = 10 } = args ?? {};
      const data = await biliFetch(`${RANKING_URL}?rid=0&type=all`);
      const items = (data?.list ?? []).slice(
        0,
        Math.max(1, Math.min(30, Number(limit) || 10)),
      );
      return {
        count: items.length,
        items: items.map((v) => ({
          bvid: v.bvid,
          title: v.title,
          author: v.owner?.name ?? null,
          score: v.score ?? null,
          play: v.stat?.view ?? null,
          danmaku: v.stat?.danmaku ?? null,
          uploaded: v.pubdate
            ? new Date(v.pubdate * 1000).toISOString()
            : null,
          url: `https://www.bilibili.com/video/${v.bvid}`,
          cover: v.pic ?? null,
        })),
      };
    },
  });

  return {
    dispose: () => {
      searchHandle.dispose();
      trendingHandle.dispose();
    },
  };
}

async function biliFetch(url) {
  const response = await fetch(url, {
    headers: {
      "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " +
        "(KHTML, like Gecko) Chrome/120 Safari/537.36 Trapezohe-Ghast/0.1",
      Accept: "application/json",
      Referer: "https://www.bilibili.com/",
    },
  });
  if (!response.ok) {
    throw new Error(`Bilibili HTTP ${response.status}`);
  }
  const payload = await response.json();
  if (payload.code && payload.code !== 0) {
    const msg = payload.message ?? "unknown error";
    if (payload.code === -412) {
      throw new Error(
        `Bilibili rate-limited this request (code -412). Wait a few seconds and retry.`,
      );
    }
    throw new Error(`Bilibili API error ${payload.code}: ${msg}`);
  }
  return payload.data;
}

function stripTags(text) {
  return String(text).replace(/<\/?em[^>]*>/g, "");
}
