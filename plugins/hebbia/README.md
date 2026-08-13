# hebbia

Search authorized institutional knowledge, analyze document sets with
traceable evidence, and support financial research workflows through Hebbia's
official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, metadata, and a generic document-analysis icon.
It does not redistribute Hebbia's hosted implementation, private Codex
connector, OAuth credentials, customer data, service source code, branded
artwork, or marketplace icon.

Hebbia's official product page and homepage are pinned as normalized visible
text with SHA-256 `7f99fc43f3f653685cd64bc5867393facfe6a99ef1991ed645ea52c41c208118` and
`92b907df1539ea06118ae09c2d392f37ee1affe07e67ce652d0674b5483ce5eb`. The product page explicitly publishes the
Matrix API and MCP connector alongside Max, Matrix, Skills & Agents, and
Projects. The homepage documents private documents, public filings, premium
financial data providers, content repositories, and enterprise data
platforms as supported product integrations.

The OAuth protected-resource and authorization-server metadata are pinned at
canonical JSON SHA-256 `78b5d22dd33e918a136b5c5bc66ced1390f609b3c923f135adaae3a3bd34e7db` and
`9b1ae93cc36d7db05e24ff49aeff32ba42f0e89f8a4a7fad3ab3f23b4ffddc0b`. Codex capability evidence is pinned to OpenAI
plugin snapshot `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app ID
or marketplace artwork.

## Ghast compatibility

- Ghast connects directly to `https://api.hebbia.ai/mcp` over Streamable HTTP and uses
  Hebbia browser OAuth. The protected resource advertises `mcp:read` and
  `offline_access`; the authorization server additionally publishes
  `mcp:readwrite`, public clients, dynamic registration, and PKCE S256.
- Hebbia's public product surface covers institutional knowledge search,
  large document-set analysis with traceability, deal and investment
  research, reusable skills and agents, shared projects, and production of
  client-ready spreadsheets, slides, and reports.
- This covers the Codex workflows for searching Hebbia projects, summarizing
  deal documents, extracting risks, obligations, and open questions, and
  returning citation-backed research while flagging evidence gaps.
- The official homepage lists SEC filings, earnings transcripts, FactSet,
  S&P Capital IQ, PitchBook, SharePoint, OneDrive, Box, Dropbox, Egnyte,
  Snowflake, Databricks, and other sources. Availability remains dependent on
  the user's Hebbia organization, plan, connected systems, permissions, and
  source-provider entitlements.
- Hebbia does not publish a public hosted-server source repository, tool
  inventory, tool schemas, annotations, rate limits, or plan matrix. The
  included workflow therefore inspects the authenticated live catalog before
  promising tool-level behavior and does not invent tool names.
- On August 13, 2026, missing and invalid Bearer initialize requests returned
  HTTP 401 with Hebbia's official protected-resource challenge and identical
  body SHA-256 `3ae7ddab16f90209af2f2b5932135d3bc56e8f3cbd44b967535f6c1db5c1bd2e`.
- A disposable loopback public client registered with HTTP 201 and no client
  secret. A PKCE authorization request reached Hebbia's Auth0-hosted,
  Hebbia-branded login endpoint. No user sign-in, authorization code, token,
  account data, or reusable credential was obtained or retained.
- Authenticated tools/list, project search, document retrieval, premium data,
  analysis runs, exports, and state-changing workflows were not exercised
  because no Hebbia account or private institutional data was used.
- The independent skill enforces least privilege, exact project and corpus
  scoping, source traceability, prompt-injection resistance, financial-data
  reconciliation, evidence-gap reporting, and explicit confirmation for any
  state-changing operation exposed by the live server.
- A generic document-analysis icon is used because no licensed Hebbia catalog
  artwork is redistributed.

The MIT license in this package applies only to the Ghast-authored adapter.
Hebbia accounts, subscriptions, hosted service behavior, customer and source
data, permissions, integrations, trademarks, privacy policy, and terms remain
controlled by Hebbia and the applicable data providers.
