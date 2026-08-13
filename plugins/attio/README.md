# attio

Search, read, create, and update Attio CRM records, lists, comments, notes,
tasks, meetings, calls, emails, and reports through Attio's official hosted
MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute Attio's hosted MCP implementation, private Codex connector,
service source code, datasets, or marketplace artwork.

The adapter is pinned to Attio's official MCP documentation with SHA-256
`2e2e355662ddd53bf33aa2a8ab89831690cd135cf60280486484f43bd2a53158`. The official OAuth protected-resource metadata is
pinned at canonical JSON SHA-256 `f4f72e8681550a7212d184d58209cab18a235a85a224798b32f75921eb6c1cda`. The OAuth
authorization-server metadata is pinned at canonical JSON SHA-256
`0ea2dac5158a6b1790c6ee311c7fcb7cf76743527cf76b1d54287908bd801f0a`.

## Ghast compatibility

- Ghast connects directly to `https://mcp.attio.com/mcp` using Streamable HTTP and Attio
  OAuth. The service declares dynamic client registration, authorization-code
  and refresh-token grants, public clients, and PKCE S256.
- Attio documents 39 tools for records and objects, lists, comments, notes,
  tasks, meetings, call recordings, emails, workspace identity, reporting,
  and plan-dependent read-only SQL.
- This covers the Codex app's contact, company, deal, list, note, task,
  meeting-preparation, prospect-research, and pipeline-update workflows, with
  additional official comments, merge, email, call, reporting, and SQL tools.
- Read operations are auto-approved by Attio while write operations request
  confirmation. The Ghast skill also requires explicit confirmation before
  every mutation and stronger fresh confirmation for merges and deletions.
- Endpoint discovery and the complete OAuth protocol were verified without an
  account. Authenticated tool listing and workspace operations were not run.
- A generic CRM data icon is used because no licensed catalog icon is included
  in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Attio accounts, subscriptions, hosted service behavior, CRM data, permissions,
trademarks, and terms remain controlled by Attio.
