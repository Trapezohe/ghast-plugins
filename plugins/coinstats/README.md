# CoinStats for Ghast

## 简介 / Overview

通过 CoinStats 官方 OAuth MCP 查询加密货币价格、投资组合表现、钱包活动、交易所数据与资讯。

Read crypto prices, portfolio performance, wallet activity, exchange data and news through CoinStats’ official OAuth MCP.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 CoinStats OAuth 授权；受账号权限与服务配额限制。 通过浏览器 OAuth 使用本人 CoinStats 账号，申请 coinstats 读取权限。MCP 请求受服务商限速与积分规则限制。

Connect in Ghast and complete CoinStats OAuth in the provider browser page. Account permissions and service quotas apply. Uses your own CoinStats account through browser OAuth with the coinstats read scope. MCP requests follow the provider’s rate limits and credit rules.

- MCP: `https://mcp.coinstats.app/mcp`
- [官方文档 / Provider documentation](https://coinstats.app/api-docs/mcp/connecting/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://coinstats.app/icon.svg?icon.35fe5k42kitmv.svg
