# Glassnode for Ghast

## 简介 / Overview

使用 Glassnode API 权限发现加密货币链上指标并获取市场分析数据。

Discover crypto on-chain metrics and retrieve market analytics using your Glassnode API access.

## 连接 / Connection

在 Glassnode 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 X-Api-Key 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a Glassnode API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the X-Api-Key header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://mcp.glassnode.com`
- [官方文档 / Provider documentation](https://docs.glassnode.com/guides-and-tutorials/glassnode-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://glassnode.com/favicon.png

验证包括端点、工具发现和本地安装/卸载；未验证受保护账号的业务查询。

Validation covers endpoints, tool discovery and local install/removal. Protected-account business queries have not been tested.

本插件使用 X-Api-Key 认证模式，按 API 权限获取数据；请求消耗 API 积分。官方还提供受限的免密公开访问模式。

This plugin uses authenticated X-Api-Key access with account entitlements and API credits. The provider also offers a limited public mode without a key.
