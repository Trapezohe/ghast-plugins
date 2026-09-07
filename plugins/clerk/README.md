# Clerk for Ghast

## 简介 / Overview

查询 Clerk 官方 SDK 示例与身份认证实现方案。

Find official Clerk SDK snippets and authentication implementation patterns.

## 连接 / Connection

公开 MCP 服务，无需账号或 API Key。

Public MCP service; no account or API key required.

- MCP: `https://mcp.clerk.com/mcp`
- [官方文档 / Provider documentation](https://clerk.com/docs/guides/ai/mcp/clerk-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://clerk.com/v2/favicon.ico
