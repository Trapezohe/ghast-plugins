# fal

Discover, price, run, upload for, monitor, and cancel image, video, audio,
3D, training, editing, and other generative-media workflows through fal's
official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, catalog metadata, documentation, and a generic icon. It does
not copy or redistribute fal's hosted MCP implementation, private Codex
connector, API keys, account data, generated media, branded artwork, or
marketplace icon.

fal's official MCP guide is pinned at SHA-256 `66aa306b5115499a0726440defcab7ae597a73142feef10fa42622decb5d0d7f`. Its ordered
11-tool documentation inventory is pinned at canonical JSON SHA-256
`96fa42823aea87bb940b54659ff8cf109faefd46f91af29ad4692c0576c96b49`. The live official server's ordered tool names
and complete normalized schemas are pinned at `83622c10bdcd3b64d92b6008d4b53a2790d6c8d939d1253a44a1acc940ad8cbb`
and `a56c797a64edfcbd70e03126674294ff1c68cc4d05268cccb4b7963e1b263239`.

The server also publishes 17 guided media prompts. Their ordered names and
complete normalized prompt definitions are pinned at
`05e651f4dcb1b29c5f7e1079aac900b7045fd8e68636c341b5b3b38233a96820` and `7da44a2905f0863901d884b099999e9c88db56178185d15f3fd56a90c99725b7`.

Official authentication, pricing, data-retention, concurrency, and model
access-control guides are pinned at `993de9e066c1edb2279be655bac60b775c859197ed9380268cddd28ab61762d9`,
`18405803581e2cf460e8f36336ee6966e78be9b506762363f26a60532c7e5b87`, `77d6d254a08b1edf7eeda40abe558dcc1d552024e80240738eafcfc2fdd46a09`,
`0e641fdef47e433f8ade3d8ee5da83b9fc31d27861b43e50992342d449f0ed58`, and `c7d1510e67296ab6dc8c21a9d8d211e1e2218071f91fb9d99ed5d11be8510d3c`.
Protected-resource and authorization-server metadata are pinned at canonical
JSON SHA-256 `672d054000bc3f7e331a767b308f6aac4ad25a3cd59f5ca55492c9497030e2e2` and
`ba82881a605265576b39aeed0bf6cc8eec8cd4a39a6be6828637fadf0080d667`.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app identifier or
artwork.

## Ghast compatibility

- Ghast connects directly to `https://mcp.fal.ai/mcp` over Streamable HTTP and sends
  the user-owned API key from the `fal-api-key` vault entry as the documented
  Authorization Bearer header.
- Only an API-scope key is needed. ADMIN keys permit deployment and
  administrative operations beyond this plugin and should not be used.
- The official 11 tools cover live model search and recommendation, schema
  inspection, pricing, synchronous and asynchronous execution, job status,
  result retrieval, cancellation, file upload, and documentation search.
- The 17 official prompts cover image generation and editing, product
  photography, video generation and editing, animation, audio, transcription,
  3D, upscaling, faces, batching, lip sync, training, vision analysis,
  virtual try-on, and restoration.
- This is a functional superset of the Codex app description for image,
  video, audio, 3D, training, editing, model recommendation, schema
  inspection, pricing, asynchronous jobs, file uploads, generation,
  upscaling, and output-parameter summaries.
- `run_model` and `submit_job` are non-idempotent billable operations.
  `upload_file` transfers data to fal's CDN. `cancel_job` is destructive.
  The included skill requires current schema and price lookup, exact input
  review, data-retention review, and explicit confirmation.
- fal documents request JSON storage for 30 days by default, with
  `store_payload=false` available through the live MCP schemas. Generated
  media and uploaded input files use CDN URLs; `expiration_seconds` can bound
  output lifetime, but expiration permanently deletes the file.
- fal's setup guide says MCP OAuth is not yet supported even though the
  endpoint publishes protected-resource and general authorization-server
  metadata. Ghast follows the official API-key setup path.
- On August 13, 2026, missing and invalid Bearer initialize requests returned
  HTTP 401 with fal's protected-resource challenge. A non-billable placeholder
  `Key` header reached protocol initialization, the complete 11-tool live
  catalog, and the complete 17-prompt catalog. No model, upload, training,
  cancellation, account-data, or billed operation was run.
- The hosted MCP implementation has not been published in an official
  licensed source repository. The official endpoint, documentation, live
  protocol catalogs, Codex capability evidence, and public fal API behavior
  are verified without redistributing service code.
- A generic generative-media icon is used because no redistributable catalog
  artwork is included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
fal accounts, credits, hosted service behavior, models, generated media,
provider terms, permissions, trademarks, and terms remain controlled by fal
and the applicable model providers.
