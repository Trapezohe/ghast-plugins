# Harness for Ghast

## 简介 / Overview

通过 Harness 官方 MCP 集成查询流水线、部署、基础设施与功能管理信息。

Explore pipelines, deployments, infrastructure and feature management using Harness’s official MCP integrations.

## 连接 / Connection

harness 连接需要 Node.js >=20、npx，以及在 Ghast 凭据中填写 Harness PAT 或服务账号 Token。能从 Token 推导账号 ID 时该字段可选，否则必须填写；FME API Key 可选，使用 FME 功能时需要。需要 Ghast 支持 credentialEnv 和 optionalCredentials。独立的 harness-hosted 连接使用 OAuth：按 Harness 官方文档将公共 Client ID 填为 mcp-client，Client Secret 留空。需要 Harness 支持团队为 SaaS 账号启用托管 OAuth；SAML/OIDC 可能需要服务商指定的 MCP 身份提供商配置。自动客户端注册受到限制，未开启审批绕过。 原生服务发现 11 个工具；使用无效模拟 Token 查询组织列表返回 HTTP 401。使用官方公开 Client ID 生成了 OAuth 授权跳转，未验证用户授权、Token 交换或真实账号操作。

The harness connection requires Node.js >=20, npx and a Harness PAT or Service Account token in Ghast credentials. Account ID is optional when inferable from the token; otherwise provide it. FME API key is optional and required for FME features. Requires Ghast credentialEnv and optionalCredentials support. The separate harness-hosted connection uses OAuth: set the public Client ID to mcp-client as specified by Harness, leaving Client Secret blank. Harness Support must enable hosted OAuth for your SaaS account; SAML/OIDC may need the provider’s MCP-specific IdP configuration. Automatic client registration is restricted. No approval bypass is enabled. The native server exposed 11 tools; a read-only organization list with an invalid fixture token returned HTTP 401. The documented public Client ID generated an OAuth redirect; provider consent, token exchange and account operations were not tested.

- MCP: `npx -y harness-mcp-v2@3.2.24`
- MCP: `https://mcp.harness.io/mcp`
- [官方原生服务器 / Official native server](https://github.com/harness/mcp-server)
- [原生客户端配置 / Native client setup](https://developer.harness.io/3k-docs/ai/configure-ai-clients/)
- [官方文档 / Provider documentation](https://developer.harness.io/docs/platform/harness-ai/connect-with-ai/harness-mcp-server/hosted-mcp/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/34780278?v=4
