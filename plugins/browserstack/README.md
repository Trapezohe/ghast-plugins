# BrowserStack for Ghast

## 简介 / Overview

通过 BrowserStack 访问真机测试、测试管理、无障碍检查与测试报告。

Access real-device testing, test management, accessibility and test reporting through BrowserStack.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 BrowserStack OAuth 授权；受账号权限与服务配额限制。

Connect in Ghast and complete BrowserStack OAuth in the provider browser page. Account permissions and service quotas apply.

- MCP: `https://mcp.browserstack.com/mcp`
- [官方文档 / Provider documentation](https://www.browserstack.com/docs/browserstack-mcp-server/get-started/remote-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://bstackprod.kinsta.cloud/wp-content/themes/browserstack/img/favicons/apple-touch-icon.png



验证包括公开端点响应、认证发现和本地安装/卸载；未验证真实账号的业务读写。

Validation covers public endpoint responses, auth discovery and local install/removal. Business reads and writes using a real account have not been tested.
