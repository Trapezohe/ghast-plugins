# domotz-preview

Connect directly to Domotz's official `https://mcp.domotz.com/mcp` hosted MCP for network
discovery, monitoring, configuration, alerting, and remediation.

The former preview connector is now covered by Domotz's generally available
remote MCP. Domotz documents roughly 50 account-dependent tools across
Discover, Monitor, Manage, and Alert.

OAuth resource and authorization metadata are pinned at canonical JSON
SHA-256 `95014110a3627248d0924a73605dc09ea599fe482950abcd6c48652e58888a9d` and `711fd29f57aaead116d6946e3c32e7c7c65d77f375b7291742fd8f9e553be943`. The service supports
authorization code, refresh tokens, public clients, dynamic registration, and
PKCE S256. Anonymous initialize returns the official resource challenge.

The hosted implementation and authenticated schemas are not redistributed.
The MIT license covers only the Ghast-authored adapter.
Accounts, data, plans, RBAC, MCP Access, write opt-in, credentials, service
behavior, and trademarks remain controlled by Domotz.

Brand logo source: https://www.domotz.com/assets/img/favicon/apple-touch-icon-152x152.png. Brand names and logos belong to Domotz. 品牌名称与标识归对应服务商所有。
