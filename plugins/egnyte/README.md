# egnyte

Search, read, analyze, upload, share, and administer Egnyte content through
Egnyte's official hosted MCP and optional official agent CLI.

## Official source

The plugin is derived from `egnyte/egnyte-for-ai` revision
`b2f1d26aa81a09cc729dc22040004c8064ec3495` (tree `4951b8b36ef0012247c3a61059d247e028f045c5`), licensed under Apache-2.0. The
official skill source, nine detailed reference documents, safety rules, and
logo are preserved, with host-specific setup and safety text adapted.
Claude Desktop terminal-bridge installation and configuration mutation
instructions are replaced with Ghast-compatible MCP and shell guidance.

The MCP declaration is normalized from `transport: "http"` to Ghast's
equivalent `type: "http"` field and points directly to `https://mcp-server.egnyte.com/mcp`.

## Capability comparison

- Codex directory snapshot: private app connector for searching folders,
  retrieving files, extracting information, and producing grounded summaries.
- Ghast: the same official hosted search, retrieval, document Q&A, summaries,
  and multi-file workflows, plus Egnyte's current file management, knowledge
  bases, metadata, links, comments, and collaboration tools.
- Optional official CLI `@egnyte/agentic-cli@1.0.1`: 64 discoverable operations
  for binary and large transfers, bulk work, users, groups, permissions,
  events, notes, locks, trash, projects, profiles, and API fallback.

The CLI source is pinned to `5ce270db377c7989ce00553f46eb5062bdd69350` (tree `dc0c6d8aac87ac72d52494669a97721357404e83`). Its canonical
64-operation schema has SHA-256 `02c674e8fcc464131c9e18679cb53e7a8a6e2dc206eed645883969f4b0b55508`.

## Authentication and safety

Remote MCP authentication uses Egnyte browser OAuth. Canonical protected
resource and authorization metadata SHA-256 values are `138f605b123ac6b6cfdca57cbb6b9dfad0aede4cc46610acfec54344a5115776` and
`fdb09e25d1caeab1655a9d920c257e4807bcdf851696d165d59f172dc5577f62`. Anonymous MCP initialization returns the expected Bearer
challenge.

An Egnyte account, domain access, RBAC, content permissions, feature
entitlements, OAuth approval, Node.js for CLI use, and service limits remain
user-managed. Every CLI mutation requires dry-run and explicit confirmation.
Deletes, shares, comments, permissions, uploads to externally shared folders,
and other visible writes require exact-target confirmation and read-after-write
verification.

The Apache-2.0 license covers the copied and adapted official plugin materials
and icon. Egnyte's hosted service, accounts, customer content, trademarks, and
service terms remain controlled by Egnyte.
