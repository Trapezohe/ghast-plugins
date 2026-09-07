# Nansen for Ghast

## 简介 / Overview

通过 Nansen 分析链上活动、代币流向、钱包与聪明钱数据。

Analyze blockchain activity, token flows, wallets and smart-money data with Nansen.

## 连接 / Connection

在 Nansen 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 NANSEN-API-KEY 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a Nansen API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the NANSEN-API-KEY header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://mcp.nansen.ai/ra/mcp`
- [官方文档 / Provider documentation](https://docs.nansen.ai/mcp/connecting)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://framerusercontent.com/images/X6PAJXo4BDwSFLJcxI2JZNWsQ.png

验证包括端点、工具发现和本地安装/卸载；未验证受保护账号的业务查询。

Validation covers endpoints, tool discovery and local install/removal. Protected-account business queries have not been tested.
