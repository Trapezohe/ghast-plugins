# Airbyte Agents for Ghast

## 简介 / Overview

查询与使用 Airbyte Agents 账号中已连接的数据源。

Query and work with the data sources connected to your Airbyte Agents account.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Airbyte Agents OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Airbyte Agents OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.airbyte.ai/mcp`
- [官方文档 / Provider documentation](https://docs.airbyte.com/ai-agents/interfaces/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://airbyte.com/favicon-192x192.png?v=20260618

这是 Airbyte 官方平台连接器；下游数据源仍需在 Airbyte 配置各自凭据和权限，不代表每个下游服务的原生官方连接器。

This is the official Airbyte platform connector. Downstream sources require their own credentials and permissions in Airbyte; they are not represented as native official connectors from each downstream provider.

验证包括官方端点认证响应、OAuth 发现和本地安装/卸载；未使用真实账号验证业务调用。

Validation covers official endpoint auth responses, OAuth discovery and local install/removal. Business calls using a real account have not been tested.
