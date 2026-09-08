# Adobe Workfront for Ghast

## 简介 / Overview

使用服务凭据连接 Adobe Workfront 官方 MCP，搜索工作内容、检查项目并执行已授权的项目操作。

Connect Adobe Workfront’s official MCP using service credentials to search work, inspect projects and perform authorized project operations.

## 连接 / Connection

获取下文说明的 Adobe IMS 服务到服务 Access Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。 本包采用 Adobe 正式支持的服务到服务 Access Token 流程。在 Adobe Developer Console 创建 OAuth server-to-server 凭据并获取 Access Token，将 Token 填入 Ghast，wf-url 填写准确的 Workfront 实例主机名，例如 yoursubdomain.my.workfront.com。本包始终要求指定实例，避免凭据可访问多个实例时路由不明确。Token 过期后需重新生成并更新连接设置；本包不会自动使用 Client Secret 换取 Token。实例必须使用 Adobe IMS，管理员需开启所需 MCP 读写权限。服务商说明自定义 OAuth 尚不支持自助接入；已观察到授权跳转不等于完成受支持的自定义登录。未测试真实账号授权或工作记录。

Obtain the Adobe IMS service-to-service access token described below and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply. This package uses Adobe’s supported service-to-service access-token flow. Create an OAuth server-to-server credential in Adobe Developer Console and obtain its access token. Enter that token in Ghast and set wf-url to the exact Workfront instance hostname (for example, yoursubdomain.my.workfront.com). This package always asks for the instance to avoid ambiguous routing when credentials cover multiple instances. Tokens expire: generate a new token and replace it in connection settings when required; this package does not automatically exchange Client Secrets. The instance must use Adobe IMS, and an administrator must enable the needed MCP read/write access. Self-service custom OAuth integration is not available according to the provider; the observed OAuth redirect is not a completed supported custom login. No real account authorization or work items were tested.

- MCP: `https://mcp.workfront.adobe.com/mcp/v1/workfront`
- [官方文档 / Provider documentation](https://experienceleague.adobe.com/en/docs/workfront/using/basics/workfront-mcp-server/configure-workfront-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/36018178?v=4

Verification: the official endpoint rejected fixture credentials at initialization with invalid_token / signature_verification_failed. Authenticated tool discovery and account operations were not tested.

验证：官方端点在初始化时以 invalid_token / signature_verification_failed 拒绝测试凭据，未测试已认证工具发现或账号操作。
