# GitBook for Ghast

## 简介 / Overview

通过 GitBook 官方账号 MCP 服务创建和维护文档、页面、变更请求与空间。

Create and maintain documentation, pages, change requests and spaces through GitBook’s official account MCP server.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 GitBook OAuth 授权；受账号权限与服务配额限制。 已验证 OAuth 发现及 S256 授权跳转；账号授权和文档操作需要用户完成登录，本次未测试。

Connect in Ghast and complete GitBook OAuth in the provider browser page. Account permissions and service quotas apply. OAuth discovery and the S256 authorization redirect were verified. Account authorization and document operations require the user to complete sign-in and were not tested.

- MCP: `https://mcp.gitbook.com/mcp`
- [官方文档 / Provider documentation](https://www.gitbook.com/blog/create-documentation-with-ai-and-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://github.com/GitbookIO.png?size=460
