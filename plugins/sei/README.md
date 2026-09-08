# Sei for Ghast

## 简介 / Overview

通过 Sei 官方 MCP 查询区块、余额、代币、NFT 与合约，并通过独立可选的钱包连接执行已授权的交易。

Use Sei’s official MCP to inspect blocks, balances, tokens, NFTs and contracts, with a separate optional wallet connection for authorized transactions.

## 连接 / Connection

需要 Node.js >=20 和 npx。sei 连接使用服务商公开 RPC，并禁用钱包模式；独立的 sei-wallet 连接需要专用钱包私钥，仅在 Ghast 加密凭据字段中填写，0x 前缀可选。钱包模式使用 stdio。主网和测试网均可用，每次操作应明确网络。安装或连接不代表授权签名、转账或付费交易。

Requires Node.js >=20 and npx. The sei connection uses the provider’s public RPC endpoints with wallet mode disabled. The separate sei-wallet connection requires a dedicated wallet private key entered only in the encrypted Ghast credential field; its 0x prefix is optional. Wallet mode stays on stdio. Both mainnet and testnet are available, so specify the network for each operation. Installing or connecting does not authorize signing, transfers or paid transactions.

- MCP: `npx -y @sei-js/mcp-server@1.0.0`
- MCP: `npx -y @sei-js/mcp-server@1.0.0`
- [官方文档 / Provider documentation](https://docs.sei.io/ai/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/101956417?v=4
