# Braintrust for Ghast

## 简介 / Overview

查看 Braintrust 调用追踪和实验，管理评测数据集与提示词，并构建经授权的 AI 评测工作流。

Inspect Braintrust traces and experiments, manage evaluation datasets and prompts, and build authorized AI evaluation workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Braintrust OAuth 授权；受账号权限与服务配额限制。 本配置面向美国数据平面。欧盟组织连接前须在本地 MCP 地址配置中改为 https://api-eu.braintrust.dev/mcp。访问权限跟随已授权账号。

Connect in Ghast and complete Braintrust OAuth in the provider browser page. Account permissions and service quotas apply. This configuration targets the US data plane. EU organizations must use https://api-eu.braintrust.dev/mcp in their local MCP URL configuration before connecting. Access follows the authenticated account permissions.

- MCP: `https://api.braintrust.dev/mcp`
- [官方文档 / Provider documentation](https://www.braintrust.dev/docs/integrations/developer-tools/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.braintrust.dev/icon180.png?v=2
