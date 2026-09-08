# Moralis for Ghast

## 简介 / Overview

通过 Moralis 官方 MCP 包查询 EVM 与 Solana 钱包余额、代币和 NFT 数据、价格及链上活动。

Query EVM and Solana wallet balances, token and NFT data, prices and blockchain activity through the official Moralis MCP package.

## 连接 / Connection

需要 Node.js 与 npx，将 Moralis API Key 填入 MORALIS_API_KEY。官方包启动时加载当前 EVM 和 Solana API 结构，在插件自己的数据目录运行，不读取工作区的 .env。需要支持 stdio credentialEnv 的 Ghast 版本。

Requires Node.js and npx. Enter your Moralis API key in MORALIS_API_KEY. The official package loads current EVM and Solana API schemas at startup. It runs in this plugin's data directory so it does not discover a workspace .env file. Requires Ghast stdio credentialEnv support.

- MCP: `npx -y @moralisweb3/api-mcp-server@1.8.2 --transport stdio`
- [官方文档 / Provider documentation](https://moralis.com/cortex/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/80474746?v=4
