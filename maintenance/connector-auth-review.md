# Connector authentication review

Checked 2026-09-08 against all 503 plugin packages: **538 MCP services**, including 452 remote entries (450 unique URLs) and 86 local runtimes. Public OAuth metadata was advertised by 376 remote entries; 76 need further documentation/network review. The JSON records the discovery snapshot before these corrections, with applied actions annotated. These counts do not represent authenticated connections.

## Applied changes

27 services across 26 plugins now prefer OAuth and keep their one existing credential as an optional advanced alternative. Dropbox additionally uses its advertised dynamic registration instead of forcing a user-provided OAuth app (28 services / 27 plugins changed). Existing saved credentials are retained.

| Plugin | Service | Registration requirement |
| --- | --- | --- |
| apify | apify | Advertised dynamic registration / client metadata document |
| appsflyer | appsflyer | Advertised dynamic registration / client metadata document |
| brevo | brevo | Advertised dynamic registration / client metadata document |
| bright-data | bright-data | Advertised dynamic registration / client metadata document |
| checkly | checkly | Advertised dynamic registration / client metadata document |
| coinmarketcap | coinmarketcap | Advertised dynamic registration / client metadata document |
| crowdin | crowdin | Advertised dynamic registration / client metadata document |
| cryptohopper | cryptohopper | Advertised dynamic registration / client metadata document |
| deel | deel | Advertised dynamic registration / client metadata document |
| deepnote | deepnote | Advertised dynamic registration / client metadata document |
| dovetail | dovetail | Advertised dynamic registration / client metadata document |
| dropbox | dropbox | Advertised dynamic registration / client metadata document |
| dune | dune | Advertised dynamic registration / client metadata document |
| everhour | everhour | Advertised dynamic registration / client metadata document |
| fal | fal | Advertised dynamic registration / client metadata document |
| fiscal-ai | fiscal | Advertised dynamic registration / client metadata document |
| github | github | Ghast registered application required |
| govtribe | govtribe | Advertised dynamic registration / client metadata document |
| instantly | instantly | Advertised dynamic registration / client metadata document |
| lokalise | lokalise | Advertised dynamic registration / client metadata document |
| lokalise | lokalise-development | Advertised dynamic registration / client metadata document |
| ref | ref | Advertised dynamic registration / client metadata document |
| render | render | Ghast registered application required |
| teamwork | teamwork | Advertised dynamic registration / client metadata document |
| telnyx | telnyx | Advertised dynamic registration / client metadata document |
| tomtom | tomtom | Advertised dynamic registration / client metadata document |
| wrike | wrike | Ghast registered application required |

## Unresolved manual-credential candidates

These 10 entries advertise some OAuth metadata but were deliberately not migrated: supplementary headers or incomplete resource discovery need provider-specific review. Existing configuration remains usable.

- **ankr / ankr**: resource or authorization discovery incomplete.
- **bitly / bitly**: resource or authorization discovery incomplete.
- **cockroachdb / cockroachdb**: supplementary instance, cluster or app credential.
- **hg-insights / hg-insights**: resource or authorization discovery incomplete.
- **justcall / justcall**: resource or authorization discovery incomplete.
- **kong-konnect / kong-konnect**: resource or authorization discovery incomplete.
- **pumble / pumble**: supplementary instance, cluster or app credential.
- **ramp / ramp-data**: resource or authorization discovery incomplete.
- **workfront / workfront**: supplementary instance, cluster or app credential.
- **yepcode / yepcode**: resource or authorization discovery incomplete.

## Validation boundary

- No private credentials, login, token exchange, account changes or provider tool calls in this scan.
- Each changed service has provider-hosted protected-resource and authorization metadata saved in [the JSON evidence](connector-auth-audit.json); GitHub also has the official host integration guide linked in its README.
- GitHub, Render, Smartsheet and Wrike require registered client configuration; this change does not supply a managed OAuth application or client secret.
- All 86 local runtimes were inventoried, not executed or logged in. The 76 remote entries without positive discovery remain unresolved, not classified as API-key-only.
- 中文：本次完成全量配置与公开元数据审查，修正 27 个插件的 28 个服务；不等于全部连接器已完成真实登录测试。10 个含额外参数或发现信息不足的手动凭据条目，以及 76 个未确认 OAuth 的远程条目仍需复核。
