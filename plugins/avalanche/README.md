# Avalanche for Ghast

## 简介 / Overview

通过 Avalanche 官方托管 MCP 检索开发文档，并查询公开网络、P 链及区块链数据。

Search Avalanche developer documentation and inspect public network, P-Chain and blockchain data through its official hosted MCP.

## 连接 / Connection

公开 MCP 服务，无需账号或 API Key。 托管端点无需账号。验证发现 48 个工具，实际返回文档搜索结果并读取主网 P 链高度。本包连接托管服务，不安装独立的 AvaCloud 或 Chainkit CLI MCP 服务。

Public MCP service; no account or API key required. The hosted endpoint requires no account. Verification discovered 48 tools, returned documentation search results and read mainnet P-Chain height. This package connects the hosted service; the separate AvaCloud and Chainkit CLI MCP servers are not installed.

- MCP: `https://build.avax.network/api/mcp`
- [官方文档 / Provider documentation](https://build.avax.network/docs/tooling/ai-llm/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://build.avax.network/common-images/Avalanche_Logomark_Red.svg
