# cube

Query governed Cube data, analyze financial performance, build dashboards,
edit semantic models on protected development branches, and inspect or build
pre-aggregations through Cube's official hosted MCP.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, metadata, and a generic governed-analytics icon.
It does not redistribute Cube's hosted implementation, private Codex
connector, OAuth credentials, tenant data, deprecated local server code,
branded artwork, or marketplace icons.

Cube's official hosted MCP guide is pinned as normalized visible text at
SHA-256 `fd816d469e8d330ee88a23d953dec174fd3df0d7732203c32ea071f6b235bec9`. The documented ordered 20-tool inventory
is pinned at canonical JSON SHA-256 `9fd46d5d21aa9477690935b50be79bf893ec95aa55beb3bfccab2c2cd205185e`. The 12 read,
four ordinary write, and four destructive tool sets are pinned at
`09bc0fb14751bd24d59d7973e066698c184929be49c71fecf9b5fdd25b6a00c1`, `04be8319b229ba71b35e7ffe1c9bbfd602e3a541a64626792db39b379ea444c0`, and
`5d1cce1b17be7bba683878f63906bb0e33ece8c955dfe3a486ce29f7f2961575`.

The OAuth protected-resource and authorization-server metadata are pinned at
canonical JSON SHA-256 `f88522816f071a795c6c20d756370fe9fd194a5d96bc9ae29f7b46c01efb6c4f` and
`8e4f1585bcd901bd05d2b98fe18700367212787cccd9f18b08a8f3235f48dcc0`.

Cube's public `cubedevinc/cube-mcp-server` repository is pinned to
`81c55225caaa8ab814e050a5e48ddede3a535a27` with Git tree
`6d63406872e6ba950f408b8f1b5b593d781f943c`. Its README explicitly deprecates the
one-tool local server in favor of the remote MCP. The repository declares MIT
in package metadata but has no LICENSE, LICENSE.md, LICENSE.txt, COPYING, or
NOTICE file, so no source file is redistributed.

The matching deprecated npm package `@cube-dev/mcp-server`
`1.3.0` is pinned at tarball SHA-256
`fa68d51dbc52add4b32df9877473fe3b76aaf5678dc91f8603179b5b6634c1ad`. It contains only `index.js`, `package.json`,
and `README.md`; it also contains no license text and exposes only `chat`, so
it is not treated as the current complete Cube plugin.

Codex capability evidence is pinned to OpenAI plugin snapshot
`11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` without copying its private app ID or marketplace
artwork.

## Ghast compatibility

- Ghast connects directly to `https://cubecloud.dev/mcp` over Streamable HTTP. Cube
  documents one endpoint for all accounts and regions, with tenant,
  deployment, and agent selection resolved through OAuth and request context.
- OAuth uses the fixed `cube-mcp-client`, `mcp-agent-access` scope,
  authorization-code and refresh-token grants, public-client authentication,
  and PKCE S256.
- The current hosted server exposes 20 tools for deployments and agent chat,
  result pagination, semantic-model search, Cube SQL queries, workbook and
  dashboard authoring, semantic-model source inspection and editing,
  redacted environment inspection, branch diffs, and pre-aggregation status
  and builds.
- The 12 read-oriented tools are `listDeployments`, `chat`,
  `loadQueryResults`, `searchDataModel`, `runQuery`, `readWorkbook`,
  `listDataModelFiles`, `readDataModelFile`, `getDataModelChanges`,
  `getBranchDiff`, `getDeploymentEnv`, and `getPreAggregationStatus`.
- The four ordinary writes are `createWorkbook`, `createReport`,
  `startDataModelEdit`, and `buildPreAggregation`. The included skill treats
  all four as state-changing and requires explicit confirmation.
- Cube labels `updateDashboard`, `publishDashboard`, `writeDataModelFile`,
  and `deleteDataModelFile` destructive. The skill requires exact before and
  after review, current-conversation confirmation, and readback after any
  ambiguous response.
- This covers and extends the Codex workflows for actual, budget, forecast,
  and variance analysis, transaction and dimension drill-down, board
  summaries, and role-governed access. The official public MCP additionally
  supports dashboard creation, semantic-model development, and
  pre-aggregation operations.
- Cube documents the hosted MCP for Premium and Enterprise plans, with Viewer
  or higher required for access, Explorer or higher for workbooks, and
  semantic-model edit permission for model and pre-aggregation tools.
- Model writes are restricted to a personal `dev-<user>-<hash>` branch,
  whole-file writes recompile and return validation errors, and Cube exposes
  no commit tool. Only a person can promote changes through the Cube UI.
- `updateDashboard` changes only the complete draft widget set and
  `publishDashboard` separately makes that draft live. The workflow never
  treats an edited draft as a published dashboard.
- `getDeploymentEnv` replaces secret-looking values with `[ENCRYPTED]`.
  `buildPreAggregation` can run real warehouse queries, write through an
  external export bucket, and incur warehouse cost.
- On August 13, 2026, the registration endpoint returned the fixed public
  client ID `cube-mcp-client` with no secret, and a PKCE request reached
  Cube's official login page. Missing and invalid Bearer initialize requests
  returned HTTP 401 with the official protected-resource challenge and
  identical body SHA-256 `b4f3b22267ec57be5480c46714960dc3eff6c506bcb684fd228befeabc5d68ff`.
- Authenticated tools/list, tenant data, financial queries, dashboard writes,
  model edits, and pre-aggregation builds were not exercised because no Cube
  tenant or business data was used.
- A generic governed-analytics icon is used because no licensed Cube
  marketplace artwork is redistributed.

The MIT license in this package applies only to the Ghast-authored adapter.
Cube accounts, plans, hosted service behavior, tenant and warehouse data,
semantic models, permissions, query cost, external storage, trademarks,
privacy policy, and terms remain controlled by Cube and the applicable data
providers.
