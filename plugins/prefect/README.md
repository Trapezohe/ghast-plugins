# Prefect for Ghast

## 简介 / Overview

以只读方式查看 Prefect Cloud 工作流、部署、运行记录、日志与基础设施。

Inspect Prefect Cloud workflows, deployments, runs, logs and infrastructure with read-only diagnostics.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Prefect OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete Prefect OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://prefect.fastmcp.app/mcp`
- [官方文档 / Provider documentation](https://github.com/PrefectHQ/prefect-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.prefect.io/favicon.ico?favicon.2_tzich_gaey5.ico

此实验性托管服务通过 Prefect Cloud OAuth 授权，仅访问授权时选择的工作区，不读取本地 Prefect 配置。MCP 工具提供只读诊断。

This experimental hosted service uses Prefect Cloud OAuth for the workspaces selected during consent. It does not read local Prefect configuration. MCP tools provide read-only diagnostics.

验证包括官方端点认证响应、OAuth 发现和本地安装/卸载；未使用真实账号验证业务调用。

Validation covers official endpoint auth responses, OAuth discovery and local install/removal. Business calls using a real account have not been tested.
