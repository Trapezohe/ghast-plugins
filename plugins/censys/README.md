# Censys for Ghast

## 简介 / Overview

连接 Censys 官方 Platform MCP，研究互联网资产、主机历史、证书和暴露面。

Connect Censys’s official Platform MCP for internet asset research, host history, certificates and exposure investigation.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Censys OAuth 授权；受账号权限与服务配额限制。 需要 Censys Platform API 访问权限；使用组织权益需要 API Access 角色。OAuth 授权时选择目标组织。调用会消耗 Censys API 积分。已验证到 oauth2.censys.io 的 OAuth PKCE 跳转，未测试用户同意授权、Token 交换、账号工具发现、资产搜索或集合修改。

Connect in Ghast and complete Censys OAuth in the provider browser page. Account permissions and service quotas apply. Requires Censys Platform API access; organization entitlements require the API Access role. Select the intended organization during OAuth consent. Calls consume Censys API credits. Verification reached the OAuth PKCE redirect at oauth2.censys.io before consent; token exchange, account tool discovery, asset searches and collection changes were not tested.

- MCP: `https://mcp.platform.censys.io/platform/mcp/`
- [官方文档 / Provider documentation](https://docs.censys.com/docs/platform-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/14364260?v=4
