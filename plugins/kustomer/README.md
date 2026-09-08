# Kustomer for Ghast

## 简介 / Overview

连接 Kustomer 官方 MCP，检索客户会话、消息、资料与客服工作流信息。

Connect Kustomer’s official MCP to search customer conversations, messages, profiles and support workflow information.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Kustomer OAuth 授权；受账号权限与服务配额限制。 需管理员先在组织的 Kustomer Application Store 中启用并安装 Kustomer MCP server 应用，再通过 OAuth 授权自己的账号。当前官方工具指南主要覆盖检索、读取与诊断，以连接后实际返回的工具为准。已验证到 PKCE 授权跳转，未测试客户记录、账号工具或 Token 交换。

Connect in Ghast and complete Kustomer OAuth in the provider browser page. Account permissions and service quotas apply. An administrator must first enable and install the Kustomer MCP server app from the Kustomer Application Store in the organization. Then authorize your own account through OAuth. The current provider tool guide focuses on search, retrieval and diagnostics; use the tools actually returned after connection. Verification reached a PKCE redirect before consent; customer records, account tools and token exchange were not tested.

- MCP: `https://server.mcp.kustomerapp.com/mcp`
- [官方文档 / Provider documentation](https://help.kustomer.com/kustomer-mcp-server-HJsPzR56ee)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/13696709?v=4
