# Gorgias for Ghast

## 简介 / Overview

分析客服工单，管理 Gorgias 客服工作流、设置与 AI 指引。

Analyze support tickets and manage customer service workflows, settings and AI guidance in Gorgias.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Gorgias OAuth 授权；受账号权限与服务配额限制。 服务商当前为 Beta，适用于全部 Helpdesk 套餐。在服务商授权页面填写 Gorgias 子域名；工具权限取决于账号角色。需要支持 oauthRequired 的 Ghast 版本，避免将公开工具发现显示为已完成账号授权。

Connect in Ghast and complete Gorgias OAuth in the provider browser page. Account permissions and service quotas apply. The provider service is beta and available on all Helpdesk plans. Enter the Gorgias subdomain on the provider authorization page. Tools inherit your account role. Requires a Ghast build supporting oauthRequired so public tool discovery is not reported as completed account authorization.

- MCP: `https://mcp.gorgias.com/mcp`
- [官方文档 / Provider documentation](https://docs.gorgias.com/en-US/connect-your-ai-assistant-to-the-gorgias-mcp-6310546)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/5e4ff204e7b6f80e402d407a/655f0a311c75248c5ff9756b_Social%20Avatar.png
