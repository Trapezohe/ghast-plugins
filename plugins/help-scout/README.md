# Help Scout for Ghast

## 简介 / Overview

搜索 Help Scout 对话、客户与知识库文章，并读取客服报表。

Search Help Scout conversations, customers and knowledge articles, and retrieve support reports.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Help Scout OAuth 授权；受账号权限与服务配额限制。 需要包含 API 访问权限的 Standard、Plus 或 Pro 套餐。新连接只读，报表需要 Plus 或 Pro。知识库功能需要在 Help Scout 授权页面另填 Docs API Key。MCP 客户端自动注册，不要在 Ghast OAuth 客户端字段中填写 Help Scout App ID。

Connect in Ghast and complete Help Scout OAuth in the provider browser page. Account permissions and service quotas apply. Requires Standard, Plus or Pro with API access. New connections are read-only; reports require Plus or Pro. To enable Docs, enter a separate Docs API key on the Help Scout authorization page. Do not enter Help Scout App IDs in Ghast OAuth client fields; the MCP client registers automatically.

- MCP: `https://mcp.helpscout.net/mcp`
- [官方文档 / Provider documentation](https://docs.helpscout.com/article/1779-connect-your-ai-agent-with-help-scout-to-search-conversations-and-pull-reports)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.helpscout.com/images/favicon/favicon.svg
