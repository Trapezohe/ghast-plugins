# Hygraph for Ghast

## 简介 / Overview

连接 Hygraph 官方全局 MCP，发现账号可访问的项目与环境、查看模型并处理结构化内容。

Connect Hygraph’s official global MCP to discover your projects and environments, inspect schemas and work with structured content.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Hygraph OAuth 授权；受账号权限与服务配额限制。 本插件采用官方全局端点和 Hygraph 账号登录，可发现账号有权访问的所有项目与环境，请明确选择目标。按项目配置的 PAT 端点属于另一种官方模式，本包未配置该模式。已验证到 PKCE 授权跳转，未测试 Token 交换、账号模型与内容操作。

Connect in Ghast and complete Hygraph OAuth in the provider browser page. Account permissions and service quotas apply. This plugin uses the official global endpoint with Hygraph account login. It can discover every project and environment your account can access, so select the intended target explicitly. Project-specific PAT endpoints are a separate provider mode and are not configured here. Verification reached a PKCE redirect before consent; token exchange, account schemas and content operations were not tested.

- MCP: `https://mcp.hygraph.com/mcp`
- [官方文档 / Provider documentation](https://hygraph.com/docs/hygraph-ai/mcp-server-setup)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://hygraph.com/icons/icon-512x512.png
