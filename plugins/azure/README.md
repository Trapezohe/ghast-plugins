# Microsoft Azure for Ghast

## 简介 / Overview

通过 Microsoft 官方 Azure MCP Server（Beta）探索与管理 Azure 云资源。

Explore and manage Azure cloud resources with Microsoft’s official Azure MCP Server (Beta).

## 连接 / Connection

需要 Node.js >=22 及 npx，使用官方 @azure/mcp@3.0.0-beta.41 预发布 Beta 包。通过本机 Azure CLI（az login）、Azure PowerShell 或受支持的微软开发环境登录，官方 Azure Identity 库读取开发者凭据，无需在聊天中发送 Token。请选择正确的租户与订阅；使用受 Azure RBAC 权限和服务费用约束。本配置关闭微软 MCP 遥测。

Requires Node.js >=22 and npx. Uses the official @azure/mcp@3.0.0-beta.41 package, a prerelease Beta. Authenticate locally with Azure CLI (az login), Azure PowerShell or a supported Microsoft development environment. The official Azure Identity library resolves local developer credentials. No Ghast-hosted OAuth or pasted chat token is required. Select the intended tenant and subscription; Azure RBAC and service costs apply. Microsoft MCP telemetry is disabled in this configuration.

- MCP: `npx -y @azure/mcp@3.0.0-beta.41 server start`
- [官方文档 / Provider documentation](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/get-started)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/6844498?v=4
