# Zep for Ghast

## 简介 / Overview

查询 Zep 记忆、获取用户上下文，并向已连接的知识图谱添加经授权的信息。

Search Zep memory, retrieve user context and add authorized information to connected knowledge graphs.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Zep OAuth 授权；受账号权限与服务配额限制。 管理员须配置并启用项目 MCP 连接，且账号有可用 MCP 席位。使用获准的工作身份登录；Google Workspace 登录与企业版自定义 OIDC 的适用条件不同。所选项目在会话中固定，更换项目需重新连接。读写及独立图谱权限受管理员策略约束。OAuth 跳转验证不代表账号已获准接入。

Connect in Ghast and complete Zep OAuth in the provider browser page. Account permissions and service quotas apply. An administrator must configure and enable the project MCP connection and provide available MCP seats. Sign in with an admitted work identity. Google Workspace sign-in and Enterprise Custom OIDC have different eligibility requirements. Your selected project is fixed for the session; reconnect to change it. Read/write and standalone-graph permissions follow administrator policy. OAuth redirect verification does not prove account admission.

- MCP: `https://api.getzep.com/mcp`
- [官方文档 / Provider documentation](https://help.getzep.com/memory-mcp-server/connect)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.getzep.com/apple-touch-icon.png
