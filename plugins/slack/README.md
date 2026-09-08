# Slack for Ghast

## 简介 / Overview

通过 Slack 官方 MCP 搜索会话与文件、阅读讨论串，并管理消息、画布和列表。

Search Slack conversations and files, read threads, and manage messages, canvases and lists through the official Slack MCP.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Slack OAuth 授权；受账号权限与服务配额限制。 需要自有的 Slack 内部应用或已在 Slack Marketplace 发布的应用，未上架的公开分发应用不能使用此服务。Slack 不支持动态客户端注册。请在 Ghast 中配置该应用的 Client ID 与 Client Secret，在 Slack 中登记 Ghast 显示的准确回调地址，启用所需用户权限，并按工作区规则取得管理员批准。本插件不包含共享客户端身份，需要 Ghast 支持静态 OAuth 应用配置。

Connect in Ghast and complete Slack OAuth in the provider browser page. Account permissions and service quotas apply. Requires your own registered internal or Slack Marketplace-published Slack app; unlisted apps cannot use this service. Slack does not support dynamic client registration. Configure that app's Client ID and Client Secret in Ghast, register the exact callback URL shown there in Slack, enable the required user scopes, and obtain workspace admin approval where needed. No shared client identity is bundled. Requires Ghast static OAuth client configuration support.

- MCP: `https://mcp.slack.com/mcp`
- [官方文档 / Provider documentation](https://docs.slack.dev/ai/slack-mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/6962987?v=4
