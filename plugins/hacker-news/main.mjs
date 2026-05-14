// hacker-news — read HN via the public Firebase API. No auth, no
// rate-limit headers, ~stable since 2014.
//
// Inspired by lobe-chat-plugins' news plugins. Reimplemented locally.

const BASE = "https://hacker-news.firebaseio.com/v0";
const FETCH_TIMEOUT_MS = 12_000;

export function activate(context) {
  const listHandle = context.tools.register("list_top_stories", {
    description:
      "Return Hacker News stories from the requested list (`top`, `new`, " +
      "`best`, `ask`, `show`, `job`). Returns up to `limit` items with " +
      "title, url, score, author, and discussion link.",
    parameters: {
      type: "object",
      properties: {
        list: {
          type: "string",
          enum: ["top", "new", "best", "ask", "show", "job"],
          default: "top",
        },
        limit: {
          type: "integer",
          minimum: 1,
          maximum: 30,
          default: 10,
        },
      },
    },
    execute: async (args = {}) => {
      const { list = "top", limit = 10 } = args ?? {};
      const safeLimit = Math.max(1, Math.min(30, Number(limit) || 10));
      const ids = await fetchJson(`${BASE}/${list}stories.json`);
      const trimmedIds = ids.slice(0, safeLimit);
      const items = await Promise.all(
        trimmedIds.map((id) => fetchJson(`${BASE}/item/${id}.json`)),
      );
      return {
        list,
        count: items.length,
        items: items
          .filter(Boolean)
          .map((item) => ({
            id: item.id,
            title: item.title,
            by: item.by,
            score: item.score,
            url: item.url ?? null,
            discussion: `https://news.ycombinator.com/item?id=${item.id}`,
            comments: item.descendants ?? 0,
            time: item.time ? new Date(item.time * 1000).toISOString() : null,
          })),
      };
    },
  });

  const storyHandle = context.tools.register("get_story", {
    description:
      "Fetch a single Hacker News story by its numeric ID. Returns the " +
      "story plus up to `commentLimit` top-level comments (each truncated " +
      "to 600 chars).",
    parameters: {
      type: "object",
      properties: {
        id: { type: "integer", description: "Hacker News story ID." },
        commentLimit: {
          type: "integer",
          minimum: 0,
          maximum: 20,
          default: 5,
        },
      },
      required: ["id"],
    },
    execute: async (args = {}) => {
      const { id, commentLimit = 5 } = args ?? {};
      if (!Number.isInteger(id)) {
        throw new Error("`id` must be an integer story ID.");
      }
      const story = await fetchJson(`${BASE}/item/${id}.json`);
      if (!story) throw new Error(`Story ${id} not found.`);

      const kids = Array.isArray(story.kids) ? story.kids.slice(0, commentLimit) : [];
      const comments = await Promise.all(
        kids.map(async (kid) => {
          const c = await fetchJson(`${BASE}/item/${kid}.json`);
          if (!c || c.deleted || c.dead) return null;
          return {
            by: c.by,
            time: c.time ? new Date(c.time * 1000).toISOString() : null,
            text: stripHtml(c.text ?? "").slice(0, 600),
          };
        }),
      );

      return {
        id: story.id,
        title: story.title,
        by: story.by,
        score: story.score,
        url: story.url ?? null,
        text: story.text ? stripHtml(story.text).slice(0, 1200) : null,
        discussion: `https://news.ycombinator.com/item?id=${story.id}`,
        commentCount: story.descendants ?? 0,
        topComments: comments.filter(Boolean),
      };
    },
  });

  return {
    dispose: () => {
      listHandle.dispose();
      storyHandle.dispose();
    },
  };
}

async function fetchJson(url) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} from ${url}`);
    }
    return await response.json();
  } finally {
    clearTimeout(timer);
  }
}

function stripHtml(input) {
  return String(input)
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#(\d+);/g, (_m, n) => String.fromCharCode(Number(n)))
    .trim();
}
