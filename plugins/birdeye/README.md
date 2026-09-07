# Birdeye for Ghast

## 简介 / Overview

通过 Birdeye 官方 MCP（Beta）探索代币市场、DEX 流动性、热点与历史价格。

Explore token markets, DEX liquidity, trends and historical prices through Birdeye’s official MCP (Beta).

## 连接 / Connection

在 Birdeye 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 x-api-key 请求头。不要在聊天中发送凭据，使用受服务配额限制。 服务为 Beta。在 Birdeye Data Services 的用量／安全设置中生成 API Key，可用数据集与请求限制取决于套餐。本包使用需鉴权的托管服务入口。

Create a Birdeye API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the x-api-key header; do not paste credentials into chat. Service quotas apply. The service is Beta. Generate an API key in Birdeye Data Services under Usage / Security. Available datasets and request limits follow your plan. This package uses the authenticated hosted endpoint.

- MCP: `https://mcp.birdeye.so/mcp`
- [官方文档 / Provider documentation](https://docs.birdeye.so/docs/birdeye-ai)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://mintcdn.com/birdeye/avRdMljk5iuSQU-x/images/verticalBlacklogotransparent.png
