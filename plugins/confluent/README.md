# Confluent for Ghast

## 简介 / Overview

通过 Confluent 官方全局 MCP 发现环境与集群、检查连接器、查询指标，并执行已授权的连接器维护。

Use Confluent’s official global MCP to discover environments and clusters, inspect connectors, query metrics and perform authorized connector maintenance.

## 连接 / Connection

使用你自己的凭据连接官方全局接口。 使用 Global 或 Cloud API Key 及对应 Secret。在本地将准确的 key:secret 编码为 Base64，并在 Ghast 填写完整的 Basic <编码结果> 请求头值，Ghast 原样发送。不要填写 Bearer Token 或仅填写 API Key。区域主题、Schema 与消息读取需要专属的服务商／区域／组织 URL，本插件未配置此类地址。无效测试凭据被 HTTP 401 拒绝，未测试真实账号访问。

Connect the official global endpoint using your own credentials. Use a Global or Cloud API key and its secret. Locally Base64-encode the exact key:secret pair and enter the complete Basic <encoded-value> header value in Ghast; Ghast sends it unchanged. Do not enter a Bearer token or only the API key. Regional topics, schemas and message reads require a separate provider-region-organization URL and are not configured by this plugin. Invalid fixture credentials were rejected with HTTP 401; no real account access was tested.

- MCP: `https://api.confluent.cloud/mcp/v1`
- [官方文档 / Provider documentation](https://docs.confluent.io/cloud/current/ai/ai-tools/managed-mcp-server.html)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.confluent.io/icons/apple-touch-icon.png
