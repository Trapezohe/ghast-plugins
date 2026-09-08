# Braze for Ghast

## 简介 / Overview

通过 Braze 官方远程 MCP 分析营销活动与 Canvas 表现，并管理受支持的内容素材。

Analyze Braze campaign and Canvas performance and manage supported content assets with Braze’s official remote MCP.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Braze OAuth 授权；受账号权限与服务配额限制。 使用官方美国端点，可访问用户已获授权的 Braze 集群。权限跟随控制台用户，调用时选择工作区；不提供用户档案级个人信息工具。Braze 维护客户端域名允许列表，可能需要服务商额外批准；当前不支持启用 IP 允许列表的公司。OAuth 跳转验证不代表账号已授权或客户端已获批准。

Connect in Ghast and complete Braze OAuth in the provider browser page. Account permissions and service quotas apply. Uses the official US endpoint, which can reach all authorized Braze clusters. Access follows dashboard user permissions and each request targets a workspace. User-profile PII tools are not exposed. Braze maintains a client-domain allowlist, so additional provider approval may be required; companies using IP allowlisting are currently unsupported. OAuth redirect testing does not prove account consent or client approval.

- MCP: `https://mcp.braze.com/mcp`
- [官方文档 / Provider documentation](https://www.braze.com/docs/user_guide/brazeai/mcp_server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/32844289?v=4
