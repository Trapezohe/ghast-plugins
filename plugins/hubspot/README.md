# hubspot

Operate HubSpot CRM records, pipelines, activities, workflows, reports, data quality, sales execution, support, retention, ownership, and quote-to-cash through all 15 official Agent CLI skills.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/HubSpot/agent-cli-skills` at `71f2bdefcc0247b1f378cb98186800dc57b6f6b1`.

Skills, references, scripts, commands, and public MCP declarations remain sourced from the pinned official repository. Unsupported client metadata is omitted.

## Ghast compatibility

- The Codex private app mapping is replaced by HubSpot's official Agent CLI, which authenticates through browser OAuth or a supported HUBSPOT_ACCESS_TOKEN service key.
- The beta CLI binary is installed separately from HubSpot's official distribution and is not redistributed in this Apache-2.0 skills package; this port was verified against hubspot 0.11.0.
- A generic CRM icon is used because the licensed skills repository does not publish a catalog icon and the CLI public-home repository does not grant redistribution rights for its social-preview asset.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
