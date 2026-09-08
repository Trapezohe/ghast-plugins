# Missive for Ghast

## 简介 / Overview

通过 Missive 官方 MCP 检索共享收件箱会话，并在所选权限内处理联系人、日历与草稿。

Use Missive’s official MCP to search shared inbox conversations and work with contacts, calendars and drafts under your chosen permissions.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Missive OAuth 授权；受账号权限与服务配额限制。 授权前，需管理员在你所属的每个组织中启用 MCP。无需 MCP API Key 或 Client Secret。请在服务商页面选择所需权限并核对回调地址；发送邮件与创建草稿属于不同权限。修改已授予权限需撤销后重新连接。已验证到 PKCE 授权跳转，未测试账号数据、日历或发送操作。

Connect in Ghast and complete Missive OAuth in the provider browser page. Account permissions and service quotas apply. An administrator must enable MCP in every organization you belong to before authorization. No MCP API key or client secret is required. Choose only the needed permissions on the provider page and verify the redirect URL. Sending email is a separate permission from creating drafts. To change granted permissions, revoke and reconnect. Verification reached a PKCE redirect before consent; account data, calendars and sending were not tested.

- MCP: `https://mcp.missiveapp.com`
- [官方文档 / Provider documentation](https://missiveapp.com/docs/ai/mcp/server/connect)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/6352330?v=4
