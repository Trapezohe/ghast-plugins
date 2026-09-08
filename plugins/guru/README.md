# Guru for Ghast

## 简介 / Overview

通过 Guru 官方 MCP 服务检索工作区知识、向知识代理提问并准备知识卡片草稿。

Find trusted workspace knowledge, ask Knowledge Agents and prepare Card drafts using Guru’s official MCP service.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Guru OAuth 授权；受账号权限与服务配额限制。 已验证 OAuth 发现及 S256 授权跳转；未完成账号登录或私有数据操作。 部分应用可能需要 Guru 支持团队加入允许名单。

Connect in Ghast and complete Guru OAuth in the provider browser page. Account permissions and service quotas apply. OAuth discovery and the S256 authorization redirect were verified; no account sign-in or private data operations were performed. Guru may require application allowlisting by its support team.

- MCP: `https://mcp.api.getguru.com/mcp`
- [官方文档 / Provider documentation](https://help.getguru.com/docs/connecting-gurus-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/5d8d029013ffd80bbb91320d/6216a21ee8829c7531435bc8_Guru_G_Black%202256.png
