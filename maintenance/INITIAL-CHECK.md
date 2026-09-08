# Initial online validation — 2026-09-08

Read-only official-source checks completed for the 502-plugin inventory. A follow-up
check of 13 plugins verified corrected uvx package parsing, including the Google Ads
pinned GitHub source. These are two batches, not an atomic snapshot of every provider.

- 495 plugins now have machine-checkable monitors; 7 remain explicit source-review items.
- 44 plugins have a newer/different upstream revision or package version than the recorded package baseline. This is an update candidate, not compatibility approval.
- 13 distinct hosted endpoints returned HTTP 404 or timed out on unauthenticated GET. They need protocol-aware follow-up; this does not prove the authenticated MCP service is broken.
- Ponytail's upstream HEAD currently matches the packaged revision; no artificial update was published.
- Local full build/validation: 502 plugins, 1384 skills, 502 packages passed. Updater regressions and isolated hook smoke passed.
- PR CI performs a fresh independent validation on Ubuntu. Its Actions status is authoritative for the current PR head.

## Upstream update candidates

aiera, alpaca, amplitude, atlassian-rovo, base44, binance, boltz-api-cli, bybit, carta-crm, catalyst-by-zoho, chrome-devtools, circleci, cloudflare, convex, datadog, deepnote, digitalocean, expo, glean, hostinger, hugging-face, hyperframes, mixpanel, mixpanel-headless, neon-postgres, netlify, nvidia, picsart, posthog, remotion, shopify, singlestore, snyk, starrocks, statsig, stripe, temporal, toggl, vantage, vercel, wix, writer, zilliz, zoom

## Endpoint observations

- `https://ai.chronograph.pe/mcp`: HTTP Error 404: Not Found
- `https://api.letsdeel.com/mcp`: HTTP Error 404: Not Found
- `https://api.picsart.com/gen-ai/mcp`: HTTP Error 404: Not Found
- `https://api.sunsama.com/mcp`: The read operation timed out
- `https://api.telnyx.com/v2/mcp`: HTTP Error 404: Not Found
- `https://mandrillapp.com/mcp`: HTTP Error 404: Not Found
- `https://mcp.api.coingecko.com/mcp`: HTTP Error 404: Not Found
- `https://mcp.channel99.com/mcp`: HTTP Error 404: Not Found
- `https://mcp.meteomatics.com/mcp`: HTTP Error 404: Not Found
- `https://mcp.picsart.io/v1`: The read operation timed out
- `https://mcp.socket.dev/`: HTTP Error 404: Not Found
- `https://mcp.vapi.ai/mcp`: HTTP Error 404: Not Found
- `https://mcp.withwandb.com/mcp`: The read operation timed out

## Activation still required

The implementation is on the review branch. The daily schedule is not live until the
workflow is merged to main. Repository Actions permission to create PRs must also be
enabled. Direct main publication was rejected by automatic approval review; this change
is delivered through a PR, with no self-approval or automatic merge.
