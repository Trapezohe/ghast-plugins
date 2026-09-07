# CoinGlass for Ghast

## 简介 / Overview

通过 CoinGlass 分析加密衍生品、资金费率、持仓量、清算与 ETF 资金流。

Analyze crypto derivatives, funding rates, open interest, liquidations and ETF flows with CoinGlass.

## 连接 / Connection

在 CoinGlass 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 CG-API-KEY 请求头。不要在聊天中发送凭据，使用受服务配额限制。 CoinGlass MCP 当前为 Beta，API Key 套餐决定可访问的数据集与请求限额。

Create a CoinGlass API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the CG-API-KEY header; do not paste credentials into chat. Service quotas apply. CoinGlass MCP is Beta; the API key plan determines accessible datasets and request limits.

- MCP: `https://api-mcp.coinglass.com/mcp`
- [官方文档 / Provider documentation](https://docs.coinglass.com/reference/mcp-service)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and software, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.coinglasscdn.com/static/icon_200.png
