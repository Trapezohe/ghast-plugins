# Jotform for Ghast

## 简介 / Overview

创建和更新 Jotform 表单，查看与管理表单提交。

Create and update Jotform forms and inspect or manage form submissions.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Jotform OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Jotform OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.jotform.com/`
- [官方文档 / Provider documentation](https://github.com/jotform/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.jotfor.ms/assets/img/favicons/favicon-2021-light.png

需要工作区管理员在 Jotform 中安装并授权 MCP 应用，不支持直接填写普通 API Token。

A workspace admin must install and authorize the Jotform MCP app. Ordinary API tokens are not supported.

验证涵盖官方端点、认证元数据与本地安装/卸载；未使用真实账号验证业务读写。

Validation covers the official endpoint, auth metadata and local install/removal. Business reads and writes with real accounts have not been tested.
