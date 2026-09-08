# Descope for Ghast

## 简介 / Overview

通过 Descope 官方 MCP 管理身份认证项目、用户、租户、访问控制和认证流程。

Manage Descope identity projects, users, tenants, access controls and flows through its official MCP server.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Descope OAuth 授权；受账号权限与服务配额限制。 本配置使用美国端点。欧盟项目可在本地 MCP 地址配置中使用 https://mcp.euc1.descope.com。登录后选择目标项目；会话默认只读，写入需要明确的临时提权。私有云部署需要服务商启用。

Connect in Ghast and complete Descope OAuth in the provider browser page. Account permissions and service quotas apply. This configuration uses the US endpoint. EU projects use https://mcp.euc1.descope.com through local MCP URL configuration. Select the intended project after login. Sessions begin read-only; writes require explicit temporary elevation. Private-cloud deployments require provider enablement.

- MCP: `https://mcp.descope.com`
- [官方文档 / Provider documentation](https://docs.descope.com/mcp/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.descope.com/favicon.ico
