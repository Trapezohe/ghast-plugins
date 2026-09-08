# Hedera for Ghast

## 简介 / Overview

使用 Hedera 官方文档与测试网 MCP，查询网络数据并准备未签名交易。

Use Hedera’s official documentation and Testnet MCP for network queries and unsigned transaction preparation.

## 连接 / Connection

在 Ghast 连接输入框填写你自己的有效 Hedera 测试网 Account ID。这是账号标识，不是 API Key 或私钥；Ghast 将其放入 x-hedera-account-id 请求头以设置会话账号。 托管网络服务仅支持测试网，并以 RETURN_BYTES 模式运行；Ghast 未为它提供钱包签名器。文档服务公开可用。实测发现 43 个网络工具和 3 个文档工具，测试网汇率查询与文档搜索成功，无需钱包签名。未测试账号专属交易、签名或提交。

Enter your Hedera Testnet Account ID in the Ghast connection field. This is an account identifier, not an API key or private key. Ghast supplies the x-hedera-account-id header to scope the session; use your own valid Testnet account. The hosted network service is Testnet-only and runs in RETURN_BYTES mode. Ghast does not provide a wallet signer for it. Documentation is public. Actual checks discovered 43 network tools and 3 documentation tools; a Testnet exchange-rate query and documentation search succeeded without wallet signing. No account-specific transaction, signature or submission was tested.

- Docs MCP: `https://docs.hedera.com/mcp`
- MCP: `https://agentic-testnet-mcp.hedera.com/mcp`
- [官方文档 / Provider documentation](https://hedera.com/mcp-servers/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/31002956?v=4

Network setup: https://docs.hedera.com/solutions/ai/hosted-mcp-server
