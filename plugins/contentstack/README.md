# Contentstack for Ghast

## 简介 / Overview

通过 Contentstack 官方 MCP 管理内容条目、素材、内容模型与发布流程。

Manage content entries, assets, models and publishing in Contentstack through its official MCP.

## 连接 / Connection

需要 Node.js 与 npx。在 Ghast 连接凭据中填写 Stack API Key、Management Token 与区域（NA、EU、AU、AZURE_NA、AZURE_EU、GCP_NA、GCP_EU）。本包启用 CMA；Analytics、BrandKit、Launch 等仅支持 OAuth 的工具组未配置。官方 --auth 会话由服务商另行保存，已有会话可能影响配置。 需要支持 stdio credentialEnv 的 Ghast 版本。服务商可能读取本地 .env 文件，请避免冲突配置。

Requires Node.js and npx. Enter your Stack API Key, Management Token and region in Ghast connection credentials. Regions include NA, EU, AU, AZURE_NA, AZURE_EU, GCP_NA and GCP_EU. This package enables CMA; Analytics, BrandKit, Launch and other OAuth-only groups are not configured. Official --auth sessions are stored separately by the provider, and may affect configuration if already present. Requires a Ghast build with stdio credentialEnv support. The provider may load a local .env file; avoid conflicting configuration.

- MCP: `npx -y @contentstack/mcp@0.9.0 --groups cma`
- [官方文档 / Provider documentation](https://developers.contentstack.com/contentstack-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.contentstack.com/apple-icon.png?apple-icon.01-ytjr51qiss.png
