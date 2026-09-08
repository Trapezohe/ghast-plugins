# Webex for Ghast

## 简介 / Overview

连接思科官方 Webex MCP，处理会议、团队消息、Vidcast 视频及工作空间设备洞察。

Connect Cisco’s official Webex MCP services for meetings, team messaging, Vidcast videos and workspace intelligence.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Webex OAuth 授权；受账号权限与服务配额限制。 每个服务都需要组织管理员在 Webex Control Hub 中启用。创建自己的 Webex Integration，将 Ghast 显示的回调地址登记到应用，并在插件 OAuth 应用输入框填写 Client ID、Client Secret 与所需 scope。Webex 不支持自动动态客户端注册。本包采用 OAuth，不采用需要运行时追加授权的 WCIT Token。验证使用测试 Client 凭据为四个端点生成 PKCE 跳转地址，未验证已注册应用、交换 Token、访问账号数据或发送任何内容。

Connect in Ghast and complete Webex OAuth in the provider browser page. Account permissions and service quotas apply. Each service must be enabled by your organization administrator in Webex Control Hub. Create your own Webex Integration and register the callback displayed by Ghast. Enter its Client ID, Client Secret and required scopes in the plugin OAuth application fields. Webex does not support automatic dynamic client registration. This package uses OAuth, not WCIT tokens that need additional runtime consent. Verification used fixture client credentials to generate PKCE redirect URLs for all four endpoints; it did not validate a registered application, exchange tokens, access account data or send anything.

- MCP: `https://mcp.webexapis.com/mcp/webex-meeting`
- [官方文档 / Provider documentation](https://developer.webex.com/mcp/docs/webex-agentic-mcp-servers)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/15900782?v=4

## 服务与权限 / Services and scopes

仅连接需要的服务；下列是完整工具集权限，纯读取任务可按官方工具权限表缩小范围。

Connect only needed services. These scopes cover each full toolset; narrow them using the official tool-scope table for read-only tasks.

### webex

- Endpoint: `https://mcp.webexapis.com/mcp/webex-meeting`
- Scopes: `spark:mcp meeting:schedules_read meeting:schedules_write meeting:participants_read meeting:summaries_read meeting:recordings_read meeting:transcripts_read`

### webex-messaging

- Endpoint: `https://mcp.webexapis.com/mcp/webex-messaging`
- Scopes: `spark:mcp spark:messages_read spark:messages_write spark:rooms_read spark:rooms_write spark:memberships_read spark:memberships_write spark:webhooks_read spark:webhooks_write`

### webex-vidcast

- Endpoint: `https://mcp.webexapis.com/mcp/vidcast`
- Scopes: `spark:mcp Identity:Organization Identity:Config`

### webex-workspaces

- Endpoint: `https://mcp.webexapis.com/mcp/workspaces`
- Scopes: `spark:mcp spark-admin:devices_read spark-admin:workspace_metrics_read spark-admin:workspaces_read spark-admin:workspace_locations_read`

