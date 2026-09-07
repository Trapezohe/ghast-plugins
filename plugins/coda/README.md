# Coda for Ghast

## 简介 / Overview

搜索 Coda 文档与表格、读取结构化数据并更新协作工作流。

Search Coda docs and tables, read structured data and update collaborative workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Coda OAuth 授权；受账号权限与服务配额限制。 功能与请求限额取决于 Coda 角色和套餐。OAuth 当前授予服务商 MCP 读写范围，实际可用工具仍受角色权限限制。

Connect in Ghast and complete Coda OAuth in the provider browser page. Account permissions and service quotas apply. Capabilities and request limits depend on your Coda role and plan. OAuth currently grants the provider MCP read/write scope; only tools allowed by your role are usable.

- MCP: `https://coda.io/apis/mcp`
- [官方文档 / Provider documentation](https://help.coda.io/hc/en-us/articles/44722661982989-Connect-to-the-Coda-MCP)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.coda.io/icons/png/color/coda-192.png
