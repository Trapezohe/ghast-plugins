# ONLYOFFICE DocSpace for Ghast

## 简介 / Overview

连接 ONLYOFFICE 官方 DocSpace MCP，处理文件、文件夹、协作空间与文档工作流。

Connect ONLYOFFICE’s official DocSpace MCP to work with files, folders, collaboration rooms and document workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 ONLYOFFICE DocSpace OAuth 授权；受账号权限与服务配额限制。 通过服务商托管的 OAuth 流程选择并授权自己的 DocSpace。服务商代理按 OAuth 应用权限授权，客户端请求的 scope 不会进一步缩小权限，请核对服务商授权页面。已验证到 PKCE 授权跳转，未测试 Token 交换、账号工具与文档操作。

Connect in Ghast and complete ONLYOFFICE DocSpace OAuth in the provider browser page. Account permissions and service quotas apply. Use the provider-hosted OAuth flow to select and authorize your own DocSpace. The provider proxy determines the OAuth application permissions; requested client scopes do not narrow those permissions. Review the provider consent carefully. Verification reached a PKCE redirect before consent; token exchange, account tools and document operations were not tested.

- MCP: `https://mcp.onlyoffice.com/mcp`
- [官方文档 / Provider documentation](https://www.onlyoffice.com/blog/2026/01/remote-onlyoffice-docspace-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/1426033?v=4
