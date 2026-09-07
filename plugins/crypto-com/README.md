# Crypto.com Market Data for Ghast

## 简介 / Overview

通过 Crypto.com 公开行情服务查询加密货币价格、市场趋势与交易量。

Look up cryptocurrency prices, market trends and trading volumes through Crypto.com’s public market-data service.

## 连接 / Connection

公开 MCP 服务，无需账号或 API Key。

Public MCP service; no account or API key required.

- MCP: `https://mcp.crypto.com/market-data/mcp`
- [官方文档 / Provider documentation](https://mcp.crypto.com/docs/getting-started)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://mcp.crypto.com/docs/favicon.ico

验证包括端点、工具发现和本地安装/卸载；未验证受保护账号的业务查询。

Validation covers endpoints, tool discovery and local install/removal. Protected-account business queries have not been tested.

已实际调用 get_ticker 获取 BTC_USDT 行情。

Verified a live BTC_USDT ticker through get_ticker.
