# Prismic for Ghast

## 简介 / Overview

通过 Prismic 官方 MCP 检索内容、准备本地化草稿与素材，并在明确授权后管理发布版本。

Use Prismic’s official MCP to search content, prepare localized drafts and assets, and manage releases with explicit publishing control.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Prismic OAuth 授权；受账号权限与服务配额限制。 先在每个目标仓库的 Settings > Prismic MCP 中启用服务，再授权账号；启用可能需要几分钟。内容修改暂存在 release 中，publish_release 额外要求 Publisher（Manager）角色与明确发布请求。迁移 release 不能通过 MCP 发布。本包采用当前托管内容 MCP，不采用已弃用的切片编码 MCP 包。已验证到 PKCE 授权跳转，未测试账号内容、Token 交换与发布。

Connect in Ghast and complete Prismic OAuth in the provider browser page. Account permissions and service quotas apply. Activate Prismic MCP under Settings > Prismic MCP in every repository you want to use, then authorize your account. Activation can take a few minutes. Content writes are staged in releases; publish_release additionally requires a Publisher (Manager) role and an explicit publishing request. Migration releases cannot be published via MCP. This uses the current hosted content MCP, not the deprecated slice-coding MCP package. Verification reached a PKCE redirect before consent; account content, token exchange and publishing were not tested.

- MCP: `https://mcp.prismic.io/mcp`
- [官方文档 / Provider documentation](https://prismic.io/docs/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/4621061?v=4
