# marcopolo

Work with governed company data in MarcoPolo's secure, persistent remote
workspace using Immersa's official MCP server and Apache-2.0 workflow skills.

## Official source

The official `immersa-co/marcopolo-plugin` repository is pinned to signed
revision `113b842f35c875a2d8ab5b31eb00675e65cd307c` with Git tree `d44fb347a54152f11ed93bec337eed54a3b98db4`. Its complete
22-file inventory has SHA-256 `226698da44cea71be4d6b2922251390623a80282b100a5f04c3bbe94465b2230` and is licensed
Apache-2.0.

This package preserves the official `.mcp.json`, four released skills, eight
connection-CLI references, icon, license, and upstream README without
modifying their contents. Ghast adds only its native manifest, this README,
`MODIFICATIONS.md`, and the separately named `marcopolo-safety` skill. The
official Claude-only agent and release workflow are verified as evidence but
are not packaged.

The released official skills are `using-marcopolo-workspace`,
`using-connection-cli`, `setup-connection`, and `query-and-analyze`. Current
MarcoPolo documentation also names `build-dashboard` and `setup-automation`,
but those files are not present in signed release v3.3.1. The official agent
explains that editable dashboard and scheduled-pipeline skills may be managed
inside the user's MarcoPolo workspace. Ghast does not invent or mislabel
unreleased files as upstream source.

## Portable MCP authentication

- Ghast connects directly to `https://mcp.marcopolo.dev` over HTTP and uses MarcoPolo OAuth.
- Protected-resource metadata is pinned at canonical JSON SHA-256
  `b3f86c27fd393a96e5c0ee415fddb8cd3d15e9fad6277a83a039549e101ed358` and identifies Bearer-header authentication.
- Authorization metadata is pinned at canonical JSON SHA-256
  `a8a8dd096445cc1068689c57f176c1d38e4042ecd14096a45dbb8377af288bca` and publishes authorization-code,
  refresh-token, and device-code grants, PKCE S256, dynamic client
  registration, and public clients.
- On August 14, 2026, missing and invalid Bearer initialize requests returned
  HTTP 401 with the exact official authentication responses. A disposable
  loopback public client registered with HTTP 201, no client secret, then
  reached the WorkOS AuthKit sign-in page with Google, GitHub, Microsoft, and
  email options. No user login, authorization code, token, reusable
  credential, or registration-management credential was obtained or retained.

## Capability comparison

- The official MCP gives the assistant an isolated persistent Linux workspace
  with shell, Python, DuckDB, files, scripts, git state, dashboards, and
  schedules.
- The official `connection` CLI lists and tests connections, writes metadata
  snapshots, runs file-based queries, materializes results into DuckDB, browses
  provider storage, downloads files, and uploads files when the live
  capability list permits.
- `connection_setup` opens a user-completed credential flow, while
  `install_demo_connection` provides no-credential evaluation datasets.
  Credentials remain outside model context.
- Results from databases, warehouses, SaaS systems, APIs, storage, and logs
  can be joined locally through DuckDB, exported for the user, turned into
  dashboards, or used by bounded scheduled workflows.
- This is a functional superset of the audited Codex marketplace description:
  secure scoped credentials, persistent workspace, DuckDB, Python, shell,
  cross-system exploration, querying, transformation, analysis, reporting,
  debugging, and recent-metric review.

## Verification and limits

MarcoPolo's current Codex, MCP tools, connection and cron CLI, and security
documentation are pinned as normalized visible text by
`scripts/import-marcopolo-plugin.py`. The current public tools page documents
`workspace_shell`, `connection_setup`, `install_demo_connection`, and
`preview_dashboard`; released skills also describe optional session-dependent
`connections_list` and `data_query` surfaces. Authenticated live `tools/list`
and workspace guidance remain authoritative.

No MarcoPolo account, private workspace, company connection, source-system
credential, query result, file, dashboard, or schedule was accessed during the
audit. Real capabilities depend on the user's account, company, plan,
workspace, connection types, source-system permissions, network reachability,
provider rate limits, and current service behavior.

The official icon is copied from the Apache-2.0 source revision and has
SHA-256 `eb91862502c864f97f258912a9289cd3e13b5ab56b38e7076a7e060345b06bab`. OpenAI's private app ID and
marketplace artwork are verified only as capability evidence and are not
included.
