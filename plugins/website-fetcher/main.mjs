// website-fetcher — download a URL and reduce it to plain text the model
// can read. No external dependencies; ships its own tiny HTML cleaner so
// we don't pull a tree-shake-resistant library like cheerio just to grab
// a <title> tag.
//
// Inspired by lobe-chat-plugins' `web` and `website-crawler`, but does
// the parsing locally instead of bouncing off a remote service.

const MAX_BYTES = 1_500_000; // hard cap on download size to stay sane
const MAX_TEXT = 8_000; // model-visible text cap

export function activate(context) {
  const handle = context.tools.register("fetch_url", {
    description:
      "Download an HTTP(S) page and return its title, meta description, " +
      "canonical URL and main text content. Strips script/style/nav/footer. " +
      "Caps output at ~8000 characters; longer pages get truncated with an " +
      "ellipsis marker. Use this when the user shares a link and you need " +
      "to read it before answering.",
    parameters: {
      type: "object",
      properties: {
        url: {
          type: "string",
          description: "Full HTTP or HTTPS URL.",
        },
      },
      required: ["url"],
    },
    execute: async (args = {}) => {
      const { url } = args ?? {};
      if (typeof url !== "string" || !/^https?:\/\//i.test(url)) {
        throw new Error("`url` must start with http:// or https://");
      }

      const response = await fetch(url, {
        redirect: "follow",
        headers: {
          "User-Agent":
            "Trapezohe-Ghast/0.1 (+https://ghast.trapezohe.ai) website-fetcher",
          Accept: "text/html,application/xhtml+xml",
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status} ${response.statusText}`);
      }
      const contentType = response.headers.get("content-type") ?? "";
      if (!/text\/html|application\/xhtml/i.test(contentType)) {
        throw new Error(
          `Unsupported content-type: ${contentType || "unknown"} (only HTML pages are supported)`,
        );
      }

      const html = await readBoundedText(response, MAX_BYTES);
      const parsed = extract(html);
      const truncated = parsed.text.length > MAX_TEXT;
      return {
        url: response.url,
        title: parsed.title,
        description: parsed.description,
        canonical: parsed.canonical,
        text: truncated ? `${parsed.text.slice(0, MAX_TEXT)}…` : parsed.text,
        truncated,
      };
    },
  });

  return { dispose: () => handle.dispose() };
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
        // ignore cancel errors
      }
      break;
    }
  }
  buffer += decoder.decode();
  return buffer;
}

function extract(html) {
  const title = pickTag(html, "title");
  const description = pickMeta(html, "description") || pickMeta(html, "og:description");
  const canonical = pickAttr(
    html,
    /<link[^>]+rel=["']canonical["'][^>]*>/i,
    /href=["']([^"']+)["']/i,
  );
  const cleaned = html
    // drop entire script/style/noscript/svg blocks
    .replace(/<(script|style|noscript|svg|template)[\s\S]*?<\/\1>/gi, " ")
    // drop nav/footer/aside/header for noise reduction
    .replace(/<(nav|footer|aside|header)[\s\S]*?<\/\1>/gi, " ")
    // strip tags
    .replace(/<[^>]+>/g, " ")
    // decode common entities
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")
    .replace(/&#(\d+);/g, (_m, n) => String.fromCharCode(Number(n)))
    .replace(/\s+/g, " ")
    .trim();
  return {
    title: title ?? null,
    description: description ?? null,
    canonical: canonical ?? null,
    text: cleaned,
  };
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

function pickAttr(html, tagRe, attrRe) {
  const tagMatch = tagRe.exec(html);
  if (!tagMatch) return null;
  const attrMatch = attrRe.exec(tagMatch[0]);
  return attrMatch ? attrMatch[1] : null;
}
