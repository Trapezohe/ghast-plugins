# Gate for Ghast

## 简介 / Overview

研究加密市场、新闻与链上数据，并通过 OAuth 连接 Gate 交易所账号。

Research crypto markets, news and on-chain data, and connect a Gate exchange account through OAuth.

## 连接 / Connection

行情、币种信息、新闻与文档服务公开可用；私有交易所工具需要单独连接 gate-exchange 并完成 Gate OAuth，受账号权限及产品可用性限制。DEX 端点在验证中返回与端点不一致的 OAuth 资源元数据，因此本包未包含该端点。

Market, coin information, news and documentation services are public. Connect the separate gate-exchange service through Gate OAuth for private exchange tools; account permissions and product availability apply. The DEX endpoint is not included because its OAuth resource metadata did not match its endpoint during validation.

- MCP: `https://api.gatemcp.ai/mcp`
- MCP: `https://api.gatemcp.ai/mcp/exchange`
- MCP: `https://api.gatemcp.ai/mcp/info`
- MCP: `https://api.gatemcp.ai/mcp/news`
- MCP: `https://api.gatemcp.ai/mcp/docs`
- [官方文档 / Provider documentation](https://github.com/gate/gate-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and software, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/234155391?v=4
