---
name: uptime-check
description: Use this skill when the user asks whether a website or API endpoint is up, reachable, or how fast it responds. Probes the URL with curl (timing) or WebFetch and reports HTTP status + latency.
version: 1.0.0
allowed-tools: [Bash, WebFetch]
---

# Uptime Check

When the user asks "is <site> up", "can you reach <url>", "how fast does
<api> respond", or similar reachability/latency questions, run a single
probe and report back.

## Preferred approach: `curl` via Bash

`curl` with format options gives you status + latency in one call:

```bash
curl -sS -o /dev/null -w 'status=%{http_code}\nlatency_ms=%{time_total}\nfinal_url=%{url_effective}\n' \
     --max-time 10 'https://example.com'
```

Multiply `time_total` (seconds) by 1000 to get milliseconds.

## Fallback: `WebFetch`

If `Bash` is not available in this conversation, call `WebFetch(url=...)`.
You won't get latency from WebFetch, but you'll know whether the page came
back. Report "reachable, content received" or the error WebFetch raised.

## Output

A single short line per probe:

> `https://example.com` — **200 OK**, 312 ms (final URL: `https://example.com/`)

For probe failures: report the curl error verbatim and don't speculate
("DNS resolution failed" is useful; "the site is probably down" is not).

## Caveats

- `curl` from the user's machine can succeed even when the public site is
  down (mirror, cache, captive portal). Mention this if the user is trying
  to debug an outage with a global audience.
- 4xx / 5xx codes are "reachable but error", not "down" — explain the
  distinction in your reply.
