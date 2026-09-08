# Reclaim.ai for Ghast

## 简介 / Overview

连接 Reclaim 官方 MCP，分析工作负载、寻找会议时间，并在 Reclaim 2.0 中暂存日历变更供审阅。

Connect Reclaim’s official MCP to analyze workload, find meeting time and stage calendar changes for review in Reclaim 2.0.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Reclaim.ai OAuth 授权；受账号权限与服务配额限制。 需要 Reclaim 2.0 及已连接的 Google 日历或 Microsoft Outlook 日历，通过服务商 OAuth 页面授权。官方文档说明 MCP 变更会暂存在 Preview Mode 中，需要在 Reclaim 审阅后应用。已验证到 PKCE 授权跳转，未测试日历访问、暂存或应用变更。

Connect in Ghast and complete Reclaim.ai OAuth in the provider browser page. Account permissions and service quotas apply. Requires Reclaim 2.0 and a connected Google Calendar or Microsoft Outlook calendar. Connect through the provider OAuth page. Official documentation states MCP changes are staged in Preview Mode for review in Reclaim before applying. Verification reached a PKCE redirect before consent; calendar access, staged changes and applying changes were not tested.

- MCP: `https://mcp.reclaim.ai`
- [官方文档 / Provider documentation](https://help.reclaim.ai/en/articles/15280604-reclaim-2-0-faq)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/67859049c02d67b2cfcceebf/67859049c02d67b2cfccf4f1_logomark256maskable.png
