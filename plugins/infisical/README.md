# Infisical for Ghast

## 简介 / Overview

连接 Infisical 官方 MCP，管理项目环境、文件夹、授权范围内的密钥和项目成员。

Connect Infisical’s official MCP to manage project environments, folders, scoped secrets and project membership.

## 连接 / Connection

需要 Node.js 与 npx。在 Ghast 连接输入框填写已限定权限范围的个人或机器身份访问 Token，以及 Infisical 服务 URL。默认云端地址为 https://app.infisical.com；区域部署或自托管部署请填写对应地址。本配置使用服务商支持的 access-token 模式，官方包固定为 0.0.23。启动和 10 个工具发现成功；测试 Token 列出项目返回 403 错误文本，未设置 isError。未测试真实密钥、账号数据或写入操作。

Requires Node.js and npx. Enter a scoped personal or machine identity access token and your Infisical service URL in Ghast’s connection fields. The default cloud URL is https://app.infisical.com; use your own region or self-hosted URL when applicable. This configuration uses the provider-supported access-token mode, with the official package pinned to 0.0.23. Startup and discovery of 10 tools succeeded; fixture-token project listing returned 403 as error text without isError. No real secrets, account data or write operations were tested.

- MCP: `npx -y @infisical/mcp@0.0.23`
- [官方文档 / Provider documentation](https://github.com/Infisical/infisical-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/107880645?v=4
