# ConfigCat for Ghast

## 简介 / Overview

通过 ConfigCat 官方 MCP 服务管理功能开关、定向规则、产品与环境。

Manage feature flags, targeting rules, products and environments through ConfigCat’s official MCP server.

## 连接 / Connection

需要 Node.js >=20 和 npx。在 ConfigCat 创建 Management API 凭据，将 API 用户名和密码填入 Ghast 连接字段，不要发送到聊天。服务通过 Basic 认证访问 api.configcat.com，权限取决于凭据所属账号。 验证发现 95 个工具，使用无效模拟凭据执行只读 list-products 返回认证错误；未验证真实账号访问。

Requires Node.js >=20 and npx. Create Management API credentials in ConfigCat and enter the API user and password in Ghast connection fields, not chat. The server uses Basic authentication against api.configcat.com. Permissions apply to the credential owner. Verification discovered 95 tools. A read-only list-products call with invalid fixture credentials returned an authentication error; actual account access was not tested.

- MCP: `npx -y @configcat/mcp-server@0.1.9`
- [官方文档 / Provider documentation](https://configcat.com/docs/advanced/mcp-server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/37753260?v=4
