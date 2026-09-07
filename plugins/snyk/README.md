# Snyk for Ghast

## 简介 / Overview

通过 Snyk 官方本地 MCP 扫描代码、依赖与基础设施安全问题。

Scan code, dependencies and infrastructure for security issues through Snyk’s official local MCP.

## 连接 / Connection

需要 Node.js 与 npx。在 Ghast 连接凭据中填写 Snyk API Token，由官方 Snyk CLI 启动本地 MCP。工具和扫描能力受账号权限、组织设置与产品套餐限制；服务会访问选定扫描范围内的本地文件。 需要支持 stdio credentialEnv 的 Ghast 版本。服务商可能读取本地 .env 文件，请避免冲突配置。

Requires Node.js and npx. Enter a Snyk API token in Ghast connection credentials; the official Snyk CLI supplies the local MCP server. Tool availability and scanning depend on account permissions, organization settings and product entitlements. The server can access local files selected for a scan. Requires a Ghast build with stdio credentialEnv support. The provider may load a local .env file; avoid conflicting configuration.

- MCP: `npx -y snyk@1.1307.0 mcp -t stdio`
- [官方文档 / Provider documentation](https://docs.snyk.io/integrations/snyk-studio-agentic-integrations/getting-started-with-snyk-studio)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/12959162?v=4
