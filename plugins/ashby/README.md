# Ashby for Ghast

## 简介 / Overview

通过 Ashby 官方 MCP（Beta）搜索招聘记录、准备面试并管理受支持的候选人流程。

Search recruiting records, prepare interviews and manage supported candidate workflows through Ashby’s official MCP (Beta).

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Ashby OAuth 授权；受账号权限与服务配额限制。 组织管理员需在 Admin > Organization Setup > Opt-in Features 中启用 MCP Server，之后 Elevated Access 用户可分别连接。不支持仅使用 Analytics 的组织。服务为 Beta，工具结构可能变化。

Connect in Ghast and complete Ashby OAuth in the provider browser page. Account permissions and service quotas apply. An Org Admin must enable MCP Server under Admin > Organization Setup > Opt-in Features. Elevated Access users can then connect individually. Analytics-only organizations are unsupported. The service is Beta and tool schemas may change.

- MCP: `https://mcp.ashbyhq.com/mcp/v1`
- [官方文档 / Provider documentation](https://docs.ashbyhq.com/ashby-mcp-server-beta)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.ashbyhq.com/icon.png
