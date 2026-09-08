# Trust Wallet for Ghast

## 简介 / Overview

通过 Trust Wallet 官方 API Gateway MCP 查询代币数据、兑换报价、支持网络与地址安全信息。

Query token data, swap quotes, supported networks and address security with Trust Wallet’s official API Gateway MCP.

## 连接 / Connection

在 portal.trustwallet.com 申请 Access ID 和 HMAC Secret Key，将两者填入 Ghast 凭据字段，由官方 HTTPS 网关签名上游请求。这是 API 网关凭据，不是助记词或钱包私钥。使用模拟请求头验证发现 13 个工具，get_swap_domains 因无效凭据返回 HTTP 403，未验证真实账号调用。

Register at portal.trustwallet.com for an Access ID and HMAC Secret Key, then enter both in Ghast credential fields. The official HTTPS gateway signs upstream requests. These are API gateway credentials, never a seed phrase or wallet private key. Verification discovered 13 tools with fixture headers; get_swap_domains returned HTTP 403 for invalid credentials. Real account calls were not tested.

- MCP: `https://mcp.trustwallet.com/tws`
- [官方文档 / Provider documentation](https://github.com/trustwallet/developer/blob/master/mcp/api-gateway.md)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/32179889?v=4
