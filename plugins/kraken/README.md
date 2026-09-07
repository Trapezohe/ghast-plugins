# Kraken for Ghast

## 简介 / Overview

通过 Kraken 官方 CLI MCP 服务查询公开价格、订单簿、成交与市场信息。

Query public Kraken prices, order books, trades and market information through the official CLI MCP server.

## 连接 / Connection

从 https://github.com/krakenfx/kraken-cli/releases 安装官方 Kraken CLI，并确保 PATH 中可找到 kraken。已在 macOS Apple Silicon 验证 v0.4.1。Ghast 启动 kraken mcp -s market，仅提供无需 API Key 的公开行情工具；本包未启用实盘交易和私有账号工具。CLI 为实验性软件，服务可用性受地区限制。

Install the official Kraken CLI from https://github.com/krakenfx/kraken-cli/releases and ensure kraken is on PATH. Verified with v0.4.1 on macOS Apple Silicon. Ghast starts kraken mcp -s market, which exposes public market tools without API keys. Live trading and private account tools are not enabled by this package. The CLI is experimental; service availability depends on your region.

- MCP: `kraken mcp -s market`
- [官方文档 / Provider documentation](https://github.com/krakenfx/kraken-cli)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and software, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.kraken.com/_assets/icons/apple-touch-icon.png
