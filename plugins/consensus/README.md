# Consensus for Ghast

## 简介 / Overview

通过 Consensus 官方 MCP 搜索学术研究，整理有文献依据的阅读清单与文献综述。

Search academic research with Consensus’s official MCP and build evidence-backed reading lists and literature reviews.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Consensus OAuth 授权；受账号权限与服务配额限制。 使用 Consensus 账号登录。API 与 MCP 共用月度调用额度，限制和可选超额计费由 API & MCP Dashboard 管理。本包采用 OAuth，无需在聊天中提供 API Key。已验证到 PKCE 授权跳转，未测试用户同意授权、Token 交换或已认证的论文搜索。

Connect in Ghast and complete Consensus OAuth in the provider browser page. Account permissions and service quotas apply. Sign in with your Consensus account. API and MCP usage share a monthly allowance, with limits and optional overages controlled in the API & MCP Dashboard. This package uses OAuth and does not require an API key in chat. Verification reached a PKCE authorization redirect before consent; token exchange and authenticated paper searches were not tested.

- MCP: `https://mcp.consensus.app/mcp`
- [官方文档 / Provider documentation](https://docs.consensus.app/consensus-mcp.md)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://framerusercontent.com/images/tSDlU81XWwAFr3wM0SLlRZp76YY.png
