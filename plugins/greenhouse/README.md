# Greenhouse for Ghast

## 简介 / Overview

通过 Greenhouse 官方 MCP（公开测试版）探索招聘数据并执行受支持的招聘流程。

Explore recruiting data and perform supported hiring workflows with Greenhouse’s official MCP (Open Beta).

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Greenhouse OAuth 授权；受账号权限与服务配额限制。 公开测试版，适用于符合条件的 Core、Plus、Pro 套餐。Site Admin 需要配置 MCP Access 权限范围，并添加 Ghast 显示的回调地址。启用后用户仍受原有 Greenhouse 权限限制。本包使用官方文档中的美国服务入口。

Connect in Ghast and complete Greenhouse OAuth in the provider browser page. Account permissions and service quotas apply. Open Beta on eligible Core, Plus and Pro tiers. A Site Admin must configure MCP Access scopes and add the redirect URL shown by Ghast for this client. After setup, users remain limited by their existing Greenhouse permissions. This package uses the documented US endpoint.

- MCP: `https://mcp.us.greenhouse.io/mcp`
- [官方文档 / Provider documentation](https://support.greenhouse.io/hc/en-us/articles/52096319906971-Set-up-Greenhouse-MCP-with-supported-AI-tools)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/6668a687e71e2722fccb8357/679a83f9b21b5caab0c682c9_GH-logo-web.png
