# dow-jones-factiva

Search licensed Factiva news for company, industry, market, and event research
through Dow Jones's official Factiva Retrieval API.

## Official API adapter

Dow Jones publishes Retrieval API 1.0 at `https://api.dowjones.com/content/gen-ai/retrieve` for contextual news
search, metadata-rich licensed chunks, summarization, question answering, and
RAG. The official developer demo is pinned to `231615fb3369ccafd4afb6fea4d817080922e772` with tree
`fb75da2d4ecbc4297ecd81aabb88fac0b9d852e2` and an MIT license.

Ghast packages no private Codex app mapping, Dow Jones credential, bearer
token, licensed article, sample content, official logo, or hosted service
implementation. The included standard-library adapter has SHA-256
`2d5e8610ed0f72d3fdaca9495753c9470883a0c901d9fece5e1a776de35ee117` and performs the documented two-step service-account exchange,
Retrieval request, current Factiva deep-link construction, and Token Usage
request without writing content or tokens to disk.

Official developer-document raw content hashes are pinned for Retrieval
overview, access, usage rules, endpoint 1.0, viewing options, direct links,
Article Fetch, deprecated Usage Metrics, Token Usage, and authentication.
OpenAI capability evidence is pinned to plugin snapshot `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9`
without redistributing its private connector or marketplace artwork.

## Capability comparison

- Codex: search Factiva's licensed global archive, research companies,
  industries, and markets, and ground answers with citations and direct
  article links through a private app connector.
- Ghast: the same current official semantic Retrieval API for licensed RAG
  context, supported Factiva taxonomy filters, date ranges, source metadata,
  compliant citations, and direct links to the secure Factiva article view.
- Ghast additionally exposes the current Token Usage endpoint for account
  consumption review.

## Contract and content boundary

A project-scoped Factiva GenAI Machine Use subscription and Dow Jones-issued
service-account credentials are required. Retrieved chunks are licensed for
transient generative use. They may not be shown as article text, persisted,
cached, redistributed, or used for model training. Every derived claim must be
attributed, and full reading should occur through an entitled Factiva link.

The MIT license in this package covers the Ghast-authored adapter, metadata,
workflow, documentation, and generic news-research icon. Factiva content,
accounts, API access, metering, rights, terms, trademarks, and service behavior
remain controlled by Dow Jones and applicable publishers.
