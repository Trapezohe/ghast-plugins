# Helicone for Ghast

## 简介 / Overview

通过 Helicone 官方 MCP 查询请求和会话，排查错误、延迟及模型用量。

Query Helicone requests and sessions to investigate errors, latency and model usage with the official MCP server.

## 连接 / Connection

需要 Node.js 和 npx。生成具备读取权限的 Helicone API Key，填入 HELICONE_API_KEY。此版本官方包使用 https://api.helicone.ai，提供 query_requests 和 query_sessions，不包含 AI Gateway 生成工具。需要支持 stdio credentialEnv 的 Ghast 版本。

Requires Node.js and npx. Generate a Helicone API key with read access and enter it in HELICONE_API_KEY. The official package uses https://api.helicone.ai and provides query_requests and query_sessions. It does not expose AI Gateway generation tools in this version. Requires Ghast stdio credentialEnv support.

- MCP: `npx -y @helicone/mcp@0.1.6`
- [官方文档 / Provider documentation](https://docs.helicone.ai/integrations/tools/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.helicone.ai/static/logo.webp
