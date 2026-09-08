# Heptabase for Ghast

## 简介 / Overview

连接 Heptabase 官方 MCP，搜索知识、阅读笔记与日记，并整理卡片、标签和白板。

Connect Heptabase’s official MCP to search knowledge, read notes and journals, and organize cards, tags and whiteboards.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Heptabase OAuth 授权；受账号权限与服务配额限制。 通过服务商网页授权连接 Heptabase 账号。访问范围取决于云同步内容与授予的账号权限。已验证到 OAuth PKCE 授权跳转，未测试用户同意授权、Token 交换或已认证的笔记读写。

Connect in Ghast and complete Heptabase OAuth in the provider browser page. Account permissions and service quotas apply. Connect your Heptabase account through the provider browser authorization page. Access applies to cloud-synced content and the granted account permissions. Verification reached an OAuth PKCE redirect before consent; token exchange and authenticated note reads or writes were not tested.

- MCP: `https://api.heptabase.com/mcp`
- [官方文档 / Provider documentation](https://support.heptabase.com/en/articles/12679581-how-to-use-heptabase-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/94618218?v=4
