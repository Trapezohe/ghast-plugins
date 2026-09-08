# Gainium for Ghast

## 简介 / Overview

通过 Gainium 官方 OAuth 连接查看加密交易机器人、余额、筛选器与回测，并可单独连接交易服务。

Review crypto bots, balances, screeners and backtests with Gainium’s official OAuth connections, with a separate trading connection.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Gainium OAuth 授权；受账号权限与服务配额限制。 需要已启用双重认证的 Gainium 账号。gainium 连接使用 /read 提供查看权限；独立的 gainium-trading 连接使用 /mcp，在服务商授权页面选择读取或交易权限，以及仅模拟交易或单机器人限制。可在 Gainium Settings > Connected apps 撤销授权。两个端点均通过 Ghast OAuth 发现并生成 PKCE 授权跳转；未验证用户授权、Token 交换、账号数据或交易。

Connect in Ghast and complete Gainium OAuth in the provider browser page. Account permissions and service quotas apply. A Gainium account with 2FA is required. The gainium connection uses /read for view access. The separate gainium-trading connection uses /mcp; choose read or trading scope and any paper-only or single-bot restriction on the provider consent page. Revoke access in Gainium Settings > Connected apps. Both endpoints passed Ghast OAuth discovery and generated PKCE authorization redirects. Consent, token exchange, account data and trades were not tested.

- MCP: `https://mcp.gainium.io/read`
- MCP: `https://mcp.gainium.io/mcp`
- [官方文档 / Provider documentation](https://gainium.io/help/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/101028747?v=4
