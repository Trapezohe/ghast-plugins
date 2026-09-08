# Rootly for Ghast

## 简介 / Overview

通过 Rootly 官方 Code Mode MCP 连接查询事故响应信息并处理值班工作流程。

Explore incident response and on-call workflows using Rootly’s official Code Mode MCP connection.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Rootly OAuth 授权；受账号权限与服务配额限制。 使用服务商推荐的 /mcp-codemode 端点。验证到 Rootly OAuth 授权页面跳转，未完成授权或执行账号 API 操作。

Connect in Ghast and complete Rootly OAuth in the provider browser page. Account permissions and service quotas apply. This uses the recommended /mcp-codemode endpoint. Verification reached Rootly’s OAuth redirect before consent; no account API operations were tested.

- MCP: `https://mcp.rootly.com/mcp-codemode`
- [官方文档 / Provider documentation](https://docs.rootly.com/integrations/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/65eb28a668c15a253c5417a6/6914d3cdf2b405d3d668acfc_rootly-favicon.svg
