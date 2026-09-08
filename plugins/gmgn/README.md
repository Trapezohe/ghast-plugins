# GMGN

Ghast adaptation of [GMGN's official skills](https://github.com/GMGNAI/gmgn-skills/tree/aa4d29a9b7d1aaaac3d6acd72c13f17575605348), licensed under MIT. All 13 upstream skills and their referenced workflow documents are included.

## Setup / 配置

Install Node.js 22 or newer, then run `npm install -g gmgn-cli@1.6.1`. Configure your own GMGN API key locally through the official CLI and https://gmgn.ai/ai. Do not paste credentials into chat. Installation of this skill package does not install the CLI or connect an account.

安装 Node.js 22 或更新版本，再运行 `npm install -g gmgn-cli@1.6.1`。通过官方 CLI 与 https://gmgn.ai/ai 在本地配置凭据；不要向对话发送密钥。安装技能包不会自动安装 CLI 或连接账号。

## Scope / 能力

Market rankings, token research, holder analysis, wallet analysis, chart patterns and authorized order workflows. State-changing orders require explicit user authorization for the target chain, asset and amount; a research request is not trading authorization.

支持市场排名、代币研究、持仓结构、钱包分析、图表形态与已授权订单流程。实际下单必须获得针对链、资产和金额的明确授权，研究请求不等于交易授权。

## Provenance / 来源

Upstream commit: `aa4d29a9b7d1aaaac3d6acd72c13f17575605348`. The plugin version follows `.claude-plugin/plugin.json` (1.0.0); the separate CLI dependency is 1.6.1. Ghast normalizes skill frontmatter, pins the CLI setup version, and replaces chat-based secret collection instructions with local configuration guidance. The official organization avatar supplies the logo. Upstream workflow documentation and license are retained.

插件版本采用上游插件清单的 1.0.0，CLI 依赖版本另为 1.6.1。Ghast 仅规范技能元数据、固定 CLI 配置版本，并将对话收集密钥改为本地配置。保留上游文档及许可证。
