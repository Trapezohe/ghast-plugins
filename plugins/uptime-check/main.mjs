// uptime-check — single-shot uptime probe. Sends a HEAD first (cheap),
// falls back to GET if the host doesn't allow HEAD. Returns status code,
// status text, and round-trip latency in ms.
//
// Inspired by lobe-chat-plugins' `uptime` — same idea, no remote service.

const TIMEOUT_MS = 10_000;

export function activate(context) {
  const handle = context.tools.register("check_uptime", {
    description:
      "Send an HTTP request to a URL and report back the status code and the " +
      "round-trip time in milliseconds. Tries HEAD first, falls back to GET. " +
      "Use this when the user asks whether a site / API is up, or how fast it " +
      "responds.",
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

      let attempted = "HEAD";
      let { ok, status, statusText, latencyMs, error } = await probe(
        url,
        "HEAD",
      );
      if (!ok && (status === 405 || status === 0)) {
        // Many servers reject HEAD outright. Retry with GET.
        attempted = "GET";
        ({ ok, status, statusText, latencyMs, error } = await probe(
          url,
          "GET",
        ));
      }

      return {
        url,
        method: attempted,
        ok,
        status,
        statusText,
        latencyMs,
        error: error ?? null,
      };
    },
  });

  return { dispose: () => handle.dispose() };
}

async function probe(url, method) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  const startedAt = Date.now();
  try {
    const response = await fetch(url, {
      method,
      redirect: "follow",
      signal: controller.signal,
      headers: {
        "User-Agent":
          "Trapezohe-Ghast/0.1 (+https://ghast.trapezohe.ai) uptime-check",
      },
    });
    return {
      ok: response.ok,
      status: response.status,
      statusText: response.statusText,
      latencyMs: Date.now() - startedAt,
      error: null,
    };
  } catch (err) {
    return {
      ok: false,
      status: 0,
      statusText: "",
      latencyMs: Date.now() - startedAt,
      error: err?.name === "AbortError" ? "timeout" : err?.message ?? String(err),
    };
  } finally {
    clearTimeout(timer);
  }
}
