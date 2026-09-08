# Dodo Payments for Ghast

## 简介 / Overview

连接 Dodo Payments 官方 MCP，处理支付、订阅、客户与产品目录工作流。

Connect Dodo Payments’ official MCP to work with payments, subscriptions, customers and product catalogs.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Dodo Payments OAuth 授权；受账号权限与服务配额限制。 官方授权网页要求输入 Dodo Payments API Key 并选择测试或生产环境。仅在核实过的服务商授权网页中输入 Key，不要发送到聊天。OAuth 已验证到 S256 PKCE 网页跳转；未提交 Key，未调用账号工具或执行财务操作。

Connect in Ghast and complete Dodo Payments OAuth in the provider browser page. Account permissions and service quotas apply. The official authorization page asks for a Dodo Payments API key and test/live environment. Enter the key only on the verified provider authorization page, never in chat. The OAuth flow reached an S256 PKCE browser redirect; no key was supplied and no account tools or financial operations were executed.

- MCP: `https://mcp.dodopayments.com/sse`
- [官方文档 / Provider documentation](https://docs.dodopayments.com/developer-resources/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/168640166?v=4
