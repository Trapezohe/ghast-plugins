# Productive for Ghast

## 简介 / Overview

连接 Productive 官方 MCP，在已授权组织中管理项目、任务、工时、CRM 与业务报表。

Connect Productive’s official MCP to manage projects, tasks, time tracking, CRM and business reports in your authorized organization.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Productive OAuth 授权；受账号权限与服务配额限制。 需要 Ultimate 订阅并启用 Productive AI。每位用户单独授权自己的账号，每个连接选择一个组织；切换组织需断开后重新连接。productive 对应正式环境，productive-sandbox 对应具有独立数据的官方沙箱，仅连接目标环境。两个端点均通过 OAuth 发现并生成 PKCE 授权跳转，未测试 Token 交换、账号工具与业务操作。

Connect in Ghast and complete Productive OAuth in the provider browser page. Account permissions and service quotas apply. Requires the Ultimate subscription plan and enabled Productive AI. Each user authorizes their own account and selects one organization per connection. Disconnect and reconnect to switch organizations. The productive connection uses production; productive-sandbox is the official separate sandbox with its own data. Connect only the intended environment. Both endpoints passed OAuth discovery and generated PKCE redirects before consent; token exchange, account tools and business operations were not tested.

- MCP: `https://mcp.productive.io/mcp`
- MCP: `https://mcp-sandbox.productive.io`
- [官方文档 / Provider documentation](https://help.productive.io/en/articles/14817386-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/20676694?v=4
