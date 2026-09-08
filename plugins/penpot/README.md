# Penpot for Ghast

## 简介 / Overview

连接 Penpot 官方本地 MCP，检查设计、处理组件与设计令牌，并导入或导出设计素材。

Connect Penpot’s official local MCP to inspect designs, work with components and tokens, and import or export design assets.

## 连接 / Connection

本地 MCP 服务，需要配对你的 Penpot 浏览器会话。 本包连接官方本地服务，不是托管的 Token 认证服务。安装 Node.js（服务商测试使用 v22），运行 npx -y @penpot/mcp@2.15.4 并保持终端运行。在 Penpot 中打开目标设计文件，通过 Plugins > Load from URL 加载 http://localhost:4400/manifest.json，运行插件并选择 Connect to MCP server，保持插件窗口打开。Ghast 连接 http://localhost:4401/mcp。访问使用当前 Penpot 浏览器会话与焦点页面；本地模式无需单独 MCP API Key。使用结束后停止终端服务并断开 Penpot 插件。安装或卸载 Ghast 包不会启动或停止外部服务。

Local MCP service paired with your Penpot browser session. This package connects to the official LOCAL service, not the hosted token-based service. Install Node.js (provider tested v22), run npx -y @penpot/mcp@2.15.4 and keep the terminal running. In Penpot, open the intended design file, use Plugins > Load from URL with http://localhost:4400/manifest.json, run the plugin and choose Connect to MCP server. Keep its window open. Ghast connects to http://localhost:4401/mcp. Access follows the active Penpot browser session and focused page; there is no separate MCP API key in local mode. Stop the terminal service and disconnect the Penpot plugin when finished. Installing or uninstalling the Ghast package does not start or stop the external service.

- MCP: `http://localhost:4401/mcp`
- [官方文档 / Provider documentation](https://help.penpot.app/mcp/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/30179644?v=4

## Verification / 验证

The official local package started, exposed 5 tools and returned usage guidance from high_level_overview. Ghast installation, logo, localized descriptions, registration and uninstall passed. No Penpot browser session was connected and no design file was read or edited. The test server was stopped after verification.

官方本地包成功启动、列出 5 个工具，high_level_overview 返回使用指南。Ghast 安装、Logo、本地化介绍、注册与卸载检查通过。未连接 Penpot 浏览器会话，未读取或编辑设计文件。验证后停止测试服务。
