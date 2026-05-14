// seo-meta — fetch a URL and pull out the tags a human SEO auditor
// would check first: title, description, OG, Twitter, canonical, h1s,
// robots, viewport. Returns a structured snapshot so the model can
// critique what's missing.
//
// Inspired by lobe-chat-plugins' `SEO` and `seo_assistant`. The
// extraction is regex-based — purposely simple, won't parse JS-rendered
// SPAs (no JSDOM dependency by design).

const MAX_BYTES = 800_000;
const FETCH_TIMEOUT_MS = 12_000;

export function activate(context) {
  const handle = context.tools.register("analyze_seo", {
    description:
      "Download a URL and extract its SEO-relevant head tags: <title>, " +
      "<meta description>, canonical link, robots, OpenGraph, Twitter Card, " +
      "first three H1s, viewport, lang. Use this when the user wants to " +
      "audit how a page is presenting itself to search engines or social " +
      "scrapers. Does NOT execute JavaScript — JS-rendered SPAs will look " +
      "empty.",
    parameters: {
      type: "object",
      properties: {
        url: { type: "string", description: "Full HTTP or HTTPS URL." },
      },
      required: ["url"],
    },
    execute: async (args = {}) => {
      const { url } = args ?? {};
      if (typeof url !== "string" || !/^https?:\/\//i.test(url)) {
        throw new Error("`url` must start with http:// or https://");
      }

      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
      let response;
      try {
        response = await fetch(url, {
          redirect: "follow",
          signal: controller.signal,
          headers: {
            "User-Agent":
              "Trapezohe-Ghast/0.1 (+https://ghast.trapezohe.ai) seo-meta",
            Accept: "text/html,application/xhtml+xml",
          },
        });
      } finally {
        clearTimeout(timer);
      }
      if (!response.ok) {
        throw new Error(`HTTP ${response.status} ${response.statusText}`);
      }
      const ctype = response.headers.get("content-type") ?? "";
      if (!/text\/html|application\/xhtml/i.test(ctype)) {
        throw new Error(`Unsupported content-type: ${ctype || "unknown"}`);
      }
      const html = await readBoundedText(response, MAX_BYTES);

      const langMatch = /<html[^>]*\blang=["']([^"']+)["']/i.exec(html);
      const og = collectMetaPrefix(html, "og:");
      const tw = collectMetaPrefix(html, "twitter:");
      const h1Matches = [...html.matchAll(/<h1[^>]*>([\s\S]*?)<\/h1>/gi)]
        .slice(0, 3)
        .map((m) => stripTags(m[1]).slice(0, 200));

      return {
        url: response.url,
        lang: langMatch ? langMatch[1] : null,
        title: pickTag(html, "title"),
        description: pickMeta(html, "description"),
        robots: pickMeta(html, "robots"),
        viewport: pickMeta(html, "viewport"),
        canonical: pickAttr(
          html,
          /<link[^>]+rel=["']canonical["'][^>]*>/i,
          /href=["']([^"']+)["']/i,
        ),
        openGraph: og,
        twitter: tw,
        h1: h1Matches,
        issues: diagnose({
          title: pickTag(html, "title"),
          description: pickMeta(html, "description"),
          og,
          h1: h1Matches,
        }),
      };
    },
  });

  return { dispose: () => handle.dispose() };
}

function diagnose({ title, description, og, h1 }) {
  const issues = [];
  if (!title) issues.push("Missing <title>");
  else if (title.length > 70) issues.push(`Title is ${title.length} chars — search snippets typically truncate after 60-70`);
  if (!description) issues.push("Missing meta description");
  else if (description.length > 160) issues.push(`Description is ${description.length} chars — Google typically truncates after ~160`);
  if (!og["og:title"]) issues.push("No og:title — social cards may fall back to <title>");
  if (!og["og:image"]) issues.push("No og:image — links will share without a preview image");
  if (h1.length === 0) issues.push("No <h1> on the page");
  if (h1.length > 1) issues.push(`Multiple H1s (${h1.length}) — pick one primary heading`);
  return issues;
}

async function readBoundedText(response, maxBytes) {
  const reader = response.body?.getReader();
  if (!reader) return await response.text();
  const decoder = new TextDecoder("utf-8", { fatal: false });
  let total = 0;
  let buffer = "";
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    total += value.byteLength;
    buffer += decoder.decode(value, { stream: true });
    if (total >= maxBytes) {
      try {
        await reader.cancel();
      } catch {
        /* ignore */
      }
      break;
    }
  }
  buffer += decoder.decode();
  return buffer;
}

function pickTag(html, tag) {
  const match = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)</${tag}>`, "i").exec(html);
  return match ? match[1].replace(/\s+/g, " ").trim() : null;
}

function pickMeta(html, name) {
  const re = new RegExp(
    `<meta[^>]+(?:name|property)=["']${name}["'][^>]*content=["']([^"']*)["']`,
    "i",
  );
  const match = re.exec(html);
  return match ? match[1].trim() : null;
}

function collectMetaPrefix(html, prefix) {
  const out = {};
  const re = new RegExp(
    `<meta[^>]+(?:name|property)=["'](${prefix.replace(":", "\\:")}[^"']+)["'][^>]*content=["']([^"']*)["']`,
    "gi",
  );
  let match;
  while ((match = re.exec(html)) !== null) {
    out[match[1]] = match[2].trim();
  }
  return out;
}

function pickAttr(html, tagRe, attrRe) {
  const tagMatch = tagRe.exec(html);
  if (!tagMatch) return null;
  const attrMatch = attrRe.exec(tagMatch[0]);
  return attrMatch ? attrMatch[1] : null;
}

function stripTags(input) {
  return String(input).replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
}
