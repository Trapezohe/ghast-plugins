# Vonage for Ghast

## 简介 / Overview

通过 Vonage 官方 MCP 查询账户余额、电话号码与通信报表，并处理短信、WhatsApp、RCS 和语音业务。

Use Vonage’s official MCP for account balances, phone numbers, communication reports, SMS, WhatsApp, RCS and voice workflows.

## 连接 / Connection

需要 Node.js 20 或更新版本、npx，以及你自己的 Vonage API Key 和 Secret；仅在 Ghast 连接凭据中填写。应用 ID、Base64 编码的应用私钥、虚拟号码、WhatsApp 号码与 RCS 发送方 ID 为可选配置，使用对应渠道或应用操作时才需要。私钥应在本地编码，不要发到聊天或在线转换网站。需要支持 credentialEnv 与 optionalCredentials 的 Ghast 版本。业务调用、号码购买和通信可能产生服务商费用；MCP App 图表渲染取决于客户端支持。

Requires Node.js 20 or newer, npx, and your own Vonage API key and secret. Enter these only in Ghast connection credentials. The optional application ID, base64-encoded application private key, virtual number, WhatsApp number and RCS sender ID are needed only by the corresponding channel or application operations; configure them when using those features. Encode any private key locally and never paste it into chat or an online converter. Requires Ghast credentialEnv and optionalCredentials support. Usage, number purchases and communications may incur provider charges. MCP App chart rendering depends on host support.

- MCP: `npx -y @vonage/vonage-mcp-server-api-bindings@1.5.1`
- [官方文档 / Provider documentation](https://developer.vonage.com/en/mcp-server/how-to-guides/install-tooling-mcp-server)

## 验证 / Verification

使用无效测试凭据实际启动官方 MCP，发现 15 个工具；只读余额查询返回 HTTP 401。未连接真实账号，未发送消息、拨打电话或购买号码。官方余额工具通过文本返回错误，未设置 isError，调用方必须检查结果内容。

The official MCP started with invalid fixture credentials and exposed 15 tools. A read-only balance query returned HTTP 401. No real account was connected and no message, call or number purchase was performed. The upstream balance tool reports failures in text without isError; inspect the returned content.

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using the provider's official MCP package, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/2683897?v=4
