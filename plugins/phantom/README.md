# Phantom for Ghast

## 简介 / Overview

连接 Phantom 官方代理钱包与开发文档 MCP 服务，支持加密资产和钱包集成工作流。

Connect Phantom’s official agent wallet and developer documentation MCP services for crypto and wallet integration workflows.

## 连接 / Connection

安装 Node.js 后，在 Ghast 中连接钱包服务。钱包操作通过服务商网页登录或设备授权使用专用代理钱包。官方包在 ~/.phantom-mcp 管理本地会话；Ghast 不会将其导入自身凭据库。断开或卸载本插件不会撤销或删除该服务商会话。不要在聊天中分享会话文件或私钥。开发文档是单独的公开连接，无需钱包登录。

Install Node.js and connect the wallet server in Ghast. Wallet actions use the provider’s browser sign-in/device authorization and a dedicated agent wallet. The official package manages a local session in ~/.phantom-mcp; Ghast does not import it into its credential vault. Disconnecting or uninstalling this plugin does not revoke or delete that provider session. Never share session files or secret keys in chat. Developer documentation is a separate public connection requiring no wallet login.

- MCP: `npx -y @phantom/mcp-server@1.2.7`
- MCP docs: `https://docs.phantom.com/mcp`
- [Developer documentation service](https://docs.phantom.com/resources/mcp-server)
- [官方文档 / Provider documentation](https://docs.phantom.com/phantom-mcp-server/setup)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/124594793?v=4

## Verification / 验证

Official wallet package startup and discovery succeeded with 30 tools; public developer documentation exposed 3 tools and a search returned official documentation. No wallet tool was invoked, existing wallet sessions were not read, and login, signing or transactions were not tested. Tool names differ from older provider documentation; discover the installed schemas.

官方钱包包启动并发现 30 个工具；公开开发文档服务列出 3 个工具，搜索返回官方文档。未调用钱包工具、读取已有钱包会话或测试登录、签名和交易。工具名称与旧版文档有差异，应以已安装服务的实际结构为准。
