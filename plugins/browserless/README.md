# Browserless for Ghast

## 简介 / Overview

使用 Browserless 自动化云端浏览器、提取网页内容、截图并执行网站审计。

Automate cloud browser sessions, extract web content, capture pages and run website audits with Browserless.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Browserless OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Browserless OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.browserless.io/mcp`
- [官方文档 / Provider documentation](https://docs.browserless.io/mcp/browserless-mcp-server/setup)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/65cb4923a3a6b08fe1124094/6890bf5c78666f8d84f1a584_favicon%20(1).svg

验证包括官方端点认证响应、OAuth 发现和本地安装/卸载；未使用真实账号验证业务调用。

Validation covers official endpoint auth responses, OAuth discovery and local install/removal. Business calls using a real account have not been tested.
