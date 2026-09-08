# Timing for Ghast

## 简介 / Overview

通过 Timing 官方 MCP 查看跟踪活动、管理项目与工时记录，并控制计时器。

Use Timing’s official MCP to review tracked activity, manage projects and time entries, and control timers.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Timing OAuth 授权；受账号权限与服务配额限制。 需要 Timing Sync 账号与 Timing Connect 订阅。OAuth 自动注册客户端，无需自行配置 Client ID 或 Secret。官方 MCP 当前支持活动、项目、工时与计时器，不支持规则管理、报表生成/导出或团队管理。已验证到 PKCE 授权跳转，未测试跟踪活动、计时器修改或 Token 交换。

Connect in Ghast and complete Timing OAuth in the provider browser page. Account permissions and service quotas apply. Requires a Timing Sync account and Timing Connect subscription. OAuth registers the client automatically; no custom Client ID or Secret is required. The official MCP currently supports activity, projects, time entries and timers, but not rule management, report generation/export or team management. Verification reached a PKCE redirect before consent; tracked activity, timer changes and token exchange were not tested.

- MCP: `https://web.timingapp.com/mcp`
- [官方文档 / Provider documentation](https://timingapp.com/help/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://web.timingapp.com/media/favicons/apple-touch-icon-512x512.png.pagespeed.ce.Km7-uCgI6H.png
