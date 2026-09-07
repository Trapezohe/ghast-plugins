# PayPal for Ghast

## 简介 / Overview

查询 PayPal 交易和发票，并协助完成用户明确授权的支付业务流程。

Review PayPal transactions and invoices and assist with authorized payment workflows.

## 连接 / Connection

在浏览器连接 PayPal 账号。官方远程服务使用 SSE，可用操作取决于账号权限。

Connect your PayPal account in the browser. The official remote service uses SSE; account permissions determine available operations.

- MCP endpoint: `https://mcp.paypal.com/sse`
- [Provider documentation / 官方文档](https://paypal.gitbook.com/agent-toolkit-and-mcp-server/mcp-server/set-up-a-remote-mcp-server)
- 安装后在 Ghast 插件详情连接服务；安装成功不代表账号授权或业务调用成功。
- Install in the Ghast plugin store, then connect in the detail page. Installation does not prove account authorization or task execution.
- 本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 插件、私有连接器 ID 或账号凭据。
- Independently authored for Ghast using the provider's public MCP service. No Codex packages, private connector IDs or credentials are included.
- 如需撤销授权，请同时检查服务商账号的授权设置。To revoke provider access, also review connected applications in your provider account.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Service names and brand assets belong to their respective owners. 品牌标识归相应权利人所有。

Brand logo source: https://cdn.simpleicons.org/paypal/003087
