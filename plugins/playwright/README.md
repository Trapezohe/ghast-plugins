# Playwright for Ghast

## 简介 / Overview

通过 Microsoft 官方 Playwright MCP 自动化浏览器流程并验证网页界面。

Automate browser workflows and verify web interfaces using Microsoft’s official Playwright MCP.

## 连接 / Connection

需要 npx 和已安装的 Google Chrome。使用独立临时浏览器配置以无头模式运行，无需服务商 API Token；服务关闭后丢弃登录状态。要求 Node.js >=18。本配置不连接已有浏览器会话。

Requires npx and an installed Google Chrome. Runs headlessly in a separate, temporary browser profile; no provider API token is required. Session login state is discarded when the server closes. Requires Node.js >=18. This configuration does not attach to existing browser sessions.

- MCP: `npx -y @playwright/mcp@0.0.80 --isolated --headless --browser chrome`
- [官方文档 / Provider documentation](https://github.com/microsoft/playwright-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://raw.githubusercontent.com/microsoft/playwright/main/packages/web/src/assets/playwright-logo.svg
