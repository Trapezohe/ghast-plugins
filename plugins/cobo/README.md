# Cobo Agentic Wallet for Ghast

## 简介 / Overview

通过 Cobo 官方 MCP 查看智能体钱包、授权协议和审计记录，执行钱包所有者授权的操作。

Inspect Cobo agent wallets, pacts and audit records, and perform owner-authorized wallet operations through the official MCP server.

## 连接 / Connection

需要 uv/uvx 支持 Python 3.12。先完成服务商的钱包初始化与所有者配对，再把智能体 API Key 填入 AGENT_WALLET_API_KEY。使用 Cobo 官方 SDK 的 MCP 扩展和生产 API；不要填写钱包原始私钥，钱包操作受所有者批准的授权协议约束。需要支持 stdio credentialEnv 的 Ghast 版本。

Requires uv/uvx with Python 3.12 support. Complete the provider's wallet onboarding and owner pairing, then enter the agent API key in AGENT_WALLET_API_KEY. Uses the official Cobo SDK MCP extra and production API. Do not enter a raw wallet private key. Owner-approved pacts govern wallet operations. Requires Ghast stdio credentialEnv support.

- MCP: `uvx --python 3.12 --from cobo-agentic-wallet[mcp]==0.1.40 python -m cobo_agentic_wallet.mcp`
- [官方文档 / Provider documentation](https://cobo.com/products/agentic-wallet/manual/developer/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/108502427?v=4
