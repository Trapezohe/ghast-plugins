#!/usr/bin/env node
import readline from "node:readline";
import process from "node:process";

const AUTH_URL = "https://data.policynote.com/v1/auth/token";
const MCP_URL = "https://data.policynote.com/v0/mcp";
const REMOTE_METHODS = new Set(["tools/list", "tools/call"]);
const SERVER_NAME = "ghast-policynote";
const SERVER_VERSION = "1.0.3-ghast.1";

let cachedToken = null;
let tokenExpiresAt = 0;

function jsonRpcError(id, code, message) {
  return { jsonrpc: "2.0", id: id ?? null, error: { code, message } };
}

function apiKey() {
  const value = process.env.POLICYNOTE_API_KEY;
  if (
    typeof value !== "string" ||
    !value.trim() ||
    /[\0\r\n]/.test(value)
  ) {
    throw new Error(
      "Set POLICYNOTE_API_KEY in the Ghast host environment.",
    );
  }
  return value.trim();
}

function resetToken() {
  cachedToken = null;
  tokenExpiresAt = 0;
}

async function accessToken() {
  if (cachedToken && Date.now() < tokenExpiresAt) return cachedToken;
  const response = await fetch(AUTH_URL, {
    method: "POST",
    headers: {
      accept: "application/json",
      "x-api-key": apiKey(),
    },
  });
  if (!response.ok) {
    throw new Error(`PolicyNote authentication failed (HTTP ${response.status}).`);
  }
  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error("PolicyNote authentication returned invalid JSON.");
  }
  if (
    typeof payload.access_token !== "string" ||
    !payload.access_token ||
    String(payload.token_type || "").toLowerCase() !== "bearer"
  ) {
    throw new Error("PolicyNote authentication response is incomplete.");
  }
  const expiresIn = Number(payload.expires_in);
  const usableSeconds = Number.isFinite(expiresIn)
    ? Math.max(1, expiresIn - 60)
    : 60;
  cachedToken = payload.access_token;
  tokenExpiresAt = Date.now() + usableSeconds * 1000;
  return cachedToken;
}

async function parseRemoteResponse(response) {
  const text = await response.text();
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("text/event-stream")) {
    for (const line of text.split(/\r?\n/)) {
      if (!line.startsWith("data:")) continue;
      const data = line.slice(5).trim();
      if (!data || data === "[DONE]") continue;
      return JSON.parse(data);
    }
    throw new Error("PolicyNote MCP returned an empty event stream.");
  }
  return JSON.parse(text);
}

async function callRemote(request, mayRefresh = true) {
  const token = await accessToken();
  const response = await fetch(MCP_URL, {
    method: "POST",
    headers: {
      accept: "application/json, text/event-stream",
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
    body: JSON.stringify(request),
  });
  if (response.status === 401 && mayRefresh) {
    resetToken();
    return callRemote(request, false);
  }
  if (!response.ok) {
    throw new Error(`PolicyNote MCP request failed (HTTP ${response.status}).`);
  }
  try {
    return await parseRemoteResponse(response);
  } catch {
    throw new Error("PolicyNote MCP returned an invalid response.");
  }
}

async function handle(request) {
  if (!request || request.jsonrpc !== "2.0" || typeof request.method !== "string") {
    return jsonRpcError(request?.id, -32600, "Invalid Request");
  }
  if (request.method.startsWith("notifications/")) return null;
  if (request.method === "initialize") {
    return {
      jsonrpc: "2.0",
      id: request.id ?? null,
      result: {
        protocolVersion: request.params?.protocolVersion || "2025-06-18",
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: SERVER_NAME, version: SERVER_VERSION },
      },
    };
  }
  if (request.method === "ping") {
    return { jsonrpc: "2.0", id: request.id ?? null, result: {} };
  }
  if (!REMOTE_METHODS.has(request.method)) {
    return jsonRpcError(request.id, -32601, "Method not found");
  }
  try {
    return await callRemote(request);
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "PolicyNote request failed.";
    return jsonRpcError(request.id, -32000, message);
  }
}

async function runSelfTest() {
  const originalFetch = globalThis.fetch;
  const originalKey = process.env.POLICYNOTE_API_KEY;
  const secret = "kid.self-test-secret";
  process.env.POLICYNOTE_API_KEY = secret;
  resetToken();
  let authCalls = 0;
  let listCalls = 0;
  const seen = [];
  globalThis.fetch = async (url, options = {}) => {
    seen.push({ url, headers: { ...(options.headers || {}) } });
    if (url === AUTH_URL) {
      authCalls += 1;
      if (options.headers["x-api-key"] !== secret) {
        return new Response("bad key", { status: 500 });
      }
      return new Response(
        JSON.stringify({
          access_token: `token-${authCalls}`,
          token_type: "Bearer",
          expires_in: 3600,
        }),
        { status: 200, headers: { "content-type": "application/json" } },
      );
    }
    const request = JSON.parse(options.body);
    if (request.method === "tools/list") {
      listCalls += 1;
      if (listCalls === 2) return new Response("", { status: 401 });
      return new Response(
        JSON.stringify({
          jsonrpc: "2.0",
          id: request.id,
          result: { tools: [{ name: "search_legislation" }] },
        }),
        { status: 200, headers: { "content-type": "application/json" } },
      );
    }
    return new Response(
      `event: message\ndata: ${JSON.stringify({
        jsonrpc: "2.0",
        id: request.id,
        result: { content: [{ type: "text", text: "ok" }] },
      })}\n\n`,
      { status: 200, headers: { "content-type": "text/event-stream" } },
    );
  };
  try {
    const initialized = await handle({
      jsonrpc: "2.0",
      id: 1,
      method: "initialize",
      params: { protocolVersion: "2025-06-18" },
    });
    const ping = await handle({ jsonrpc: "2.0", id: 2, method: "ping" });
    const listed = await handle({ jsonrpc: "2.0", id: 3, method: "tools/list" });
    const called = await handle({
      jsonrpc: "2.0",
      id: 4,
      method: "tools/call",
      params: { name: "search_legislation", arguments: {} },
    });
    const refreshed = await handle({
      jsonrpc: "2.0",
      id: 5,
      method: "tools/list",
    });
    const unsupported = await handle({
      jsonrpc: "2.0",
      id: 6,
      method: "resources/list",
    });
    const transcript = JSON.stringify({
      initialized,
      ping,
      listed,
      called,
      refreshed,
      unsupported,
    });
    const remoteHeaders = seen
      .filter((entry) => entry.url === MCP_URL)
      .map((entry) => JSON.stringify(entry.headers))
      .join("\n");
    if (
      initialized?.result?.serverInfo?.name !== SERVER_NAME ||
      ping?.result == null ||
      listed?.result?.tools?.[0]?.name !== "search_legislation" ||
      called?.result?.content?.[0]?.text !== "ok" ||
      refreshed?.result?.tools?.[0]?.name !== "search_legislation" ||
      unsupported?.error?.code !== -32601 ||
      authCalls !== 2 ||
      transcript.includes(secret) ||
      remoteHeaders.includes(secret)
    ) {
      throw new Error("PolicyNote bridge self-test assertion failed.");
    }
    process.stdout.write("PolicyNote bridge self-test passed\n");
  } finally {
    globalThis.fetch = originalFetch;
    resetToken();
    if (originalKey === undefined) delete process.env.POLICYNOTE_API_KEY;
    else process.env.POLICYNOTE_API_KEY = originalKey;
  }
}

async function runStdio() {
  const input = readline.createInterface({
    input: process.stdin,
    crlfDelay: Infinity,
    terminal: false,
  });
  for await (const line of input) {
    if (!line.trim()) continue;
    let response;
    try {
      response = await handle(JSON.parse(line));
    } catch {
      response = jsonRpcError(null, -32700, "Parse error");
    }
    if (response) process.stdout.write(`${JSON.stringify(response)}\n`);
  }
}

if (process.argv.includes("--self-test")) await runSelfTest();
else await runStdio();
