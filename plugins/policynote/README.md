# policynote

Research legislation, regulation, officials, elections, transcripts, local
government activity, CQ news, and organization policy work through
FiscalNote's official PolicyNote API and MCP server.

## Official service

PolicyNote publishes a Streamable HTTP MCP endpoint at `https://data.policynote.com/v0/mcp` and a
public OpenAPI 3.1 schema. The schema currently documents 41 REST operations
and 33 unique MCP tools across organization app data, legislation, people,
organizations, elections, VoterVoice, Curate, presidential transcripts, CQ
documents, CQ news, and full-text retrieval.

The service supports browser OAuth for compatible clients and a documented
machine flow that exchanges a customer API key at `https://data.policynote.com/v1/auth/token` for a
short-lived bearer token. This package uses the machine flow because it can be
configured independently without reusing a private Codex OAuth client.

## Capability comparison

- Codex: structured worldwide policy and regulatory intelligence, legislation,
  government activity, policy updates, alerts, research, dashboards, and
  internal workflow integration through a private app connector.
- Ghast: the complete currently documented official 33-tool MCP surface,
  subject to the user's scopes and plan, through an independent local
  API-key-to-bearer bridge.
- The official surface includes organization Issues, Projects, Actions,
  legislation and regulation; global legislation; officials and organizations;
  elections and districts; local-government documents; presidential and CQ
  transcripts; CQ news; predictive bill analytics; votes; events; and source
  document retrieval.

## Authentication and licensing

Set `POLICYNOTE_API_KEY` in the local host environment. API access, scopes,
quotas, subscription terms, data rights, and key issuance remain controlled by
FiscalNote. The bridge keeps the key and bearer token out of command arguments
and stores tokens only in memory.

The bundled bridge SHA-256 is `54f167e50adeff5126885bda4cf3d6558f3caa0f57e193add8fe1ec171417a99`. The MIT license covers only the
Ghast-authored bridge, workflow, metadata, documentation, and generic policy
research icon. It does not license or redistribute FiscalNote's hosted server,
PolicyNote data, Provider Content, private connector, credentials,
documentation, logos, or trademarks.
