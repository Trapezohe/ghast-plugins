# Airwallex for Ghast

## 简介 / Overview

连接 Airwallex 官方生产、沙箱开发与公开文档 MCP 服务，支持财务和集成开发工作流。

Connect Airwallex’s official production, sandbox developer and public documentation MCP services for finance and integration workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Airwallex OAuth 授权；受账号权限与服务配额限制。 生产 AgentOS 使用生产 Airwallex 账号，Developer MCP 单独使用沙箱账号连接。Docs MCP 是公开文档服务，不能读取账号余额或执行付款。生产和沙箱授权已验证到 S256 PKCE 网页跳转，未测试 Token 交换或账号操作。已发现两个公开文档工具。遵循账号权限及服务商对资金转出的限制。

Connect in Ghast and complete Airwallex OAuth in the provider browser page. Account permissions and service quotas apply. Connect production AgentOS with your production Airwallex account, and Developer MCP separately with a sandbox account. Docs MCP is public and does not access account balances or execute payments. Production and sandbox authorization reached S256 PKCE browser redirects; token exchange and account operations were not tested. The two public documentation tools were discovered. Follow account permissions and the provider’s money-out restrictions.

- MCP: `https://mcp.airwallex.com/mcp`
- Developer MCP: `https://mcp.sandbox.airwallex.com/developer`
- Docs MCP: `https://mcp.sandbox.airwallex.com/docs`
- [Developer and docs setup](https://www.airwallex.com/docs/developer-tools/ai/developer-mcp)
- [官方文档 / Provider documentation](https://www.airwallex.com/docs/developer-tools/ai/agentos)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/15722888?v=4
