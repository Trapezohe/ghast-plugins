# Enterpret for Ghast

## 简介 / Overview

通过 Enterpret 官方 MCP 分析客户反馈、主题、情绪与账号背景，并获取带来源引用的答案。

Analyze customer feedback, themes, sentiment and account context with cited answers from Enterpret’s official MCP.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Enterpret OAuth 授权；受账号权限与服务配额限制。 使用帮助中心当前记载的 wisdom-api 入口。已验证 OAuth 发现及 S256 跳转，未测试账号登录与私有反馈查询。

Connect in Ghast and complete Enterpret OAuth in the provider browser page. Account permissions and service quotas apply. Uses the current wisdom-api endpoint documented in the help center. OAuth discovery and S256 redirect were verified; account sign-in and private feedback queries were not tested.

- MCP: `https://wisdom-api.enterpret.com/server/mcp`
- [官方文档 / Provider documentation](https://helpcenter.enterpret.com/en/articles/12665166-enterpret-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.prod.website-files.com/69e6b779dbc68d6b76294ae1/69e6b779dbc68d6b76294e61_Final%20icon%20256.png
