# Helius for Ghast

## 简介 / Overview

通过 Helius 官方 MCP 的无签名凭据模式查询 Solana 资产、钱包数据、交易与网络信息。

Query Solana assets, wallet data, transactions and network information through Helius’s official MCP in its non-signing credential mode.

## 连接 / Connection

需要 Node.js 与 npx，已使用 Node.js 24.16.0 验证。Helius API Key 仅填写在 Ghast 凭据字段。本包选择上游 HELIUS_MCP_SHARED_CREDENTIAL=1 模式：使用传入 API Key，不加载签名密钥，并拒绝钱包签名、账号开通及运行时凭据修改。默认网络为 mainnet-beta，切换网络需修改本地 MCP 配置中的 HELIUS_NETWORK。仍受 Helius 套餐限制。上游包会在 ~/.helius 写入匿名遥测标识，并要求路由调用携带反馈元数据，勿在其中包含私人信息。 验证发现 10 个路由工具，并成功返回文档主题。使用无效模拟 API Key 查询网络状态返回 HTTP 401，未验证真实认证链上查询或签名。

Requires Node.js and npx; verified with Node.js 24.16.0. Enter a Helius API key only in Ghast credentials. This package selects the upstream HELIUS_MCP_SHARED_CREDENTIAL=1 mode: it uses the supplied API key, does not load a signing key, and refuses wallet signing, account provisioning and runtime credential changes. The network is mainnet-beta; changing network requires editing HELIUS_NETWORK in local MCP configuration. Helius plan limits still apply. The upstream package writes an anonymous telemetry ID under ~/.helius and requires feedback metadata on routed calls; keep that metadata free of private information. Verification discovered 10 routed tools and returned documentation topics. A network-status call with an invalid fixture API key returned HTTP 401; real authenticated chain queries and signing were not tested.

- MCP: `npx -y helius-mcp@2.2.0`
- [官方文档 / Provider documentation](https://www.helius.dev/docs/agents/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/107892413?v=4
