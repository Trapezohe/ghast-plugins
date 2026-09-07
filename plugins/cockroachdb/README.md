# CockroachDB Cloud for Ghast

## 简介 / Overview

通过 CockroachDB Cloud 官方托管 MCP 服务探索数据库并执行 SQL。

Explore CockroachDB Cloud databases and run SQL using the official managed MCP service.

## 连接 / Connection

在 CockroachDB Cloud 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a CockroachDB Cloud API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://cockroachlabs.cloud/mcp`
- [官方文档 / Provider documentation](https://www.cockroachlabs.com/blog/cockroachdb-ai-agents-managed-mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://raw.githubusercontent.com/cockroachdb/claude-plugin/main/assets/logo.svg

在凭据表单中，Authorization 填服务账号 API Key，mcp-cluster-id 填 Cloud 控制台的目标集群 ID。访问受 Cloud RBAC、集群权限与读写同意控制。

In the credential form, enter the service-account API key under Authorization and the target cluster ID under mcp-cluster-id. Cloud RBAC, cluster permissions and read/write consent apply.

Additional official configuration reference: https://github.com/cockroachdb/claude-plugin#alternative-mcp-backends
