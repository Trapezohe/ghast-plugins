# Tatum Docs & API for Ghast

## 简介 / Overview

搜索 Tatum 开发文档、查看 OpenAPI 结构，并在配置 Tatum 密钥后执行文档中的 API 请求。

Search Tatum developer documentation, inspect OpenAPI schemas and execute documented API requests with an optional Tatum key.

## 连接 / Connection

在 Tatum Docs & API 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 X-API-Key 请求头。不要在聊天中发送凭据，使用受服务配额限制。 tatum-docs 用于免凭据访问公开文档与 API 结构；tatum 连接需填写 Tatum API Key，用于需要认证的 API 请求。两个连接使用同一官方地址，授权要求分别配置。本插件连接 Tatum Documentation MCP，不安装另一套本地 Blockchain MCP 包。

Create a Tatum Docs & API API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the X-API-Key header; do not paste credentials into chat. Service quotas apply. Use tatum-docs for public documentation and schema discovery without credentials. Use tatum with a Tatum API key for authenticated API requests. The two connections share the official endpoint but have separate authentication requirements. This plugin connects to Tatum Documentation MCP; it does not install the separate local Blockchain MCP package.

- MCP: `https://docs.tatum.io/mcp`
- [官方文档 / Provider documentation](https://docs.tatum.io/oa/docs/tatum-documentation-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/48604299?v=4
