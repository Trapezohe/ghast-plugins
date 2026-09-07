# OKX Market Data for Ghast

通过 OKX 官方 Agent Trade Kit 查询市场价格、订单簿、K 线与衍生品行情。

Read OKX market prices, order books, candles and derivatives market data through the official Agent Trade Kit.

## 连接 / Connection

需要 Node.js 与 npx。使用固定版本的 OKX 官方 npm 包，只启用 market 模块与只读模式，无需 API Key。此包不提供下单、转账或账户管理；不拆分多个交易模块作为独立插件。

Requires Node.js and npx. Runs a pinned official OKX npm package with only the market module and read-only mode. No API key is needed. This package does not expose trading, transfers or account administration. Trading modules are not split into separate plugins.

- Official documentation: https://www.okx.com/docs-v5/agent_en/
- Official source: https://github.com/okx/agent-trade-kit
- Brand logo: https://www.okx.com/cdn/assets/imgs/253/59830BB78B18A776.png

Ghast independently authored this plugin; no Codex private connector is used. Ghast-authored files are MIT licensed. OKX owns its brand and logo.

本插件由 Ghast 独立编写，不使用 Codex 私有连接器。Ghast 编写的文件采用 MIT 许可，品牌与 Logo 归 OKX 所有。
