# Weights & Biases for Ghast

## 简介 / Overview

通过 Weights & Biases 官方 MCP 分析 W&B 运行记录与制品，以及 Weave 调用追踪和评测。

Analyze W&B runs and artifacts and Weave traces and evaluations through the official Weights & Biases MCP server.

## 连接 / Connection

在 Weights & Biases 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 使用 W&B 官方托管云服务。工具发现本身不会证明 API Key 有效，账号数据查询需要有效的 W&B 密钥。独立部署及私有化实例需要使用服务商支持的专属配置。

Create a Weights & Biases API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. Uses the W&B hosted cloud service. Tool discovery alone does not verify API-key validity; account queries require a valid W&B key. Dedicated and on-premises deployments need their own provider-supported configuration.

- MCP: `https://mcp.withwandb.com/mcp`
- [官方文档 / Provider documentation](https://github.com/wandb/wandb-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/26401354?v=4
