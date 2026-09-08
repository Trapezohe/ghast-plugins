# Perplexity for Ghast

## 简介 / Overview

通过 Perplexity 官方工具进行网页搜索、问答、推理与研究，使用独立的 API 账号计费。

Use Perplexity’s official web search, question-answering, reasoning and research tools with your API account.

## 连接 / Connection

需要 Node.js 与 Perplexity API Key。在 Ghast 连接凭据框填写 Key，由 PERPLEXITY_API_KEY 注入。API 计费与配额独立于 Perplexity 面向个人用户的订阅。

Requires Node.js and a Perplexity API key. Enter it in Ghast’s connection credential field; it is passed through PERPLEXITY_API_KEY. API billing and limits are separate from Perplexity consumer subscriptions.

- MCP: `npx -y @perplexity-ai/mcp-server@1.2.1`
- [官方文档 / Provider documentation](https://docs.perplexity.ai/docs/getting-started/integrations/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/185426709?v=4
