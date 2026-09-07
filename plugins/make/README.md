# Make for Ghast

## 简介 / Overview

通过 Make 官方 MCP 服务构建、查看、管理与运行自动化场景。

Build, inspect, manage and run automation scenarios through Make’s official MCP server.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Make OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Make OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.make.com`
- [官方文档 / Provider documentation](https://developers.make.com/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://372892049-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/organizations%2F8lUfdal5k5WEadMGCIer%2Fsites%2Fsite_ipZgk%2Ficon%2FgBbkE4PN3kFt9GtaLZ7j%2Ffavicon%20-%20Make%20light%20mode.png?alt=media&token=c63fbb15-858a-4868-9b7b-7b7c1f6215fd

场景调用超时不代表执行取消；先检查原执行状态与结果，避免重复触发。

A scenario call timeout does not mean execution stopped. Inspect the original run and its output before retrying to avoid duplicate effects.

验证涵盖官方端点、认证元数据与本地安装/卸载；未使用真实账号验证业务读写。

Validation covers the official endpoint, auth metadata and local install/removal. Business reads and writes with real accounts have not been tested.
