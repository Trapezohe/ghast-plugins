# Honeycomb for Ghast

## 简介 / Overview

分析 Honeycomb 链路追踪、请求延迟与服务健康状况。

Explore traces, latency and service health with Honeycomb.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Honeycomb OAuth 授权；受账号权限与服务配额限制。 默认使用美国端点，EU 区账号应改用官方 EU 端点；按任务选择环境和权限。

Connect in Ghast and complete Honeycomb OAuth in the provider browser page. Account permissions and service quotas apply. Uses the US endpoint. EU accounts must use the documented EU endpoint instead. Select the intended environment and read-only scopes when sufficient.

- MCP: `https://mcp.honeycomb.io/mcp`
- [官方文档 / Provider documentation](https://docs.honeycomb.io/integrations/mcp/configuration-guide)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.honeycomb.io/favicon-32x32.png
