# Knowify for Ghast

## 简介 / Overview

通过 Knowify 官方只读 AI 连接器分析施工项目、利润与开票数据。

Analyze construction jobs, profitability and invoicing with Knowify’s official read-only AI connector.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Knowify OAuth 授权；受账号权限与服务配额限制。 需要管理员账号。此连接器仅支持读取，不能创建、修改或删除记录。

Connect in Ghast and complete Knowify OAuth in the provider browser page. Account permissions and service quotas apply. Requires an administrator account. Read-only; records cannot be created, changed or deleted.

- MCP: `https://assistant.knowify.com/api/v2/mcp`
- [官方文档 / Provider documentation](https://knowify.zendesk.com/hc/en-us/articles/49623682048660-Getting-started-with-the-Knowify-AI-Connector)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/ca/cd/2c/cacd2cca-33e1-ee68-a77c-17e3ec402b2e/AppIcon-0-0-1x_U007epad-0-1-85-220.png/512x512bb.jpg
