# Chrome DevTools for Ghast

## 简介 / Overview

通过 Google 官方 Chrome DevTools MCP 检查网页、排查网络与控制台问题，并分析页面性能。

Inspect browser pages, debug network and console issues, and analyze performance with Google’s official Chrome DevTools MCP.

## 连接 / Connection

需要 npx 和已安装的 Google Chrome。使用独立临时浏览器配置以无头模式运行，无需服务商 API Token；服务关闭后丢弃登录状态。要求 Node.js ^20.19.0、^22.12.0 或 >=23。本配置不连接已有浏览器会话。Chrome DevTools 已关闭使用统计与 CrUX URL 共享。

Requires npx and an installed Google Chrome. Runs headlessly in a separate, temporary browser profile; no provider API token is required. Session login state is discarded when the server closes. Requires Node.js ^20.19.0, ^22.12.0 or >=23. This configuration does not attach to existing browser sessions. Chrome DevTools usage statistics and CrUX URL sharing are disabled.

- MCP: `npx -y chrome-devtools-mcp@1.8.0 --isolated --headless --no-usage-statistics --no-performance-crux`
- [官方文档 / Provider documentation](https://github.com/ChromeDevTools/chrome-devtools-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.gstatic.com/devrel-devsite/prod/v5e941f15ff6710591bee254538202655020220785b40a3f4d932e94adb9f6037/chrome/images/touchicon-180.png
