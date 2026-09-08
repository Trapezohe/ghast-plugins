# Ankr for Ghast

## 简介 / Overview

连接 Ankr 官方只读区块链 MCP 与 OAuth 账号管理 MCP，查询链上数据并管理 RPC 服务。

Connect Ankr’s official read-only blockchain MCP and OAuth account-management MCP for chain data and RPC operations.

## 连接 / Connection

在 Ankr 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 x-ankr-api-key 请求头。不要在聊天中发送凭据，使用受服务配额限制。 数据 MCP 需 Ankr 项目 API Key，遵循原套餐限制；管理 MCP 单独通过浏览器 OAuth 连接。数据入口已发现 17 个工具，但测试凭据的区块读取返回上游 404，未证明有效凭据下的链查询。管理 OAuth 已验证到 S256 PKCE 跳转；未测试 Token 交换或账号操作。更换 Key 后需重新连接数据服务。

Create a Ankr API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the x-ankr-api-key header; do not paste credentials into chat. Service quotas apply. Data MCP requires an Ankr project API key; normal plan limits apply. Management MCP connects separately through browser OAuth. Data discovery returned 17 tools, but a block read with a fixture key failed with an upstream 404; no authenticated chain query was proven. Management OAuth reached an S256 PKCE redirect; token exchange and account operations were not tested. Reconnect the data service after changing its key.

- Management MCP (OAuth): `https://mcp.ankr.com/mcp`
- MCP: `https://mcp.ankr.com/rpc`
- [官方文档 / Provider documentation](https://www.ankr.com/docs/agentic-rpc/overview/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.ankr.com/static/favicon/apple-touch-icon.png

Management documentation: https://www.ankr.com/docs/rpc-service/getting-started/management-mcp/
