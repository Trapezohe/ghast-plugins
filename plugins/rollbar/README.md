# Rollbar for Ghast

## 简介 / Overview

在 Rollbar 中查看生产错误、发生记录、部署与会话回放。

Inspect production errors, occurrences, deployments and session replays in Rollbar.

## 连接 / Connection

需要 Node.js 20 或更高版本及 npx。Ghast 启动官方 @rollbar/mcp-server@0.6.0 包。在 Rollbar 账号设置创建 Account Access Token，排查使用 read 权限，更新错误条目需要 read 与 write 权限，然后填入 Ghast 连接凭据。官方服务优先读取工作目录或用户目录的 .rollbar-mcp.json；若显示错误账号，请清理冲突配置。需要支持 stdio credentialEnv 的 Ghast 版本。

Requires Node.js 20 or later and npx. Ghast launches the official @rollbar/mcp-server@0.6.0 package. Create an Account Access Token in Rollbar account settings with read scope for investigations, or read and write for item updates, and enter it in Ghast connection credentials. Existing .rollbar-mcp.json files in the working or home directory take precedence in the official server; remove conflicting configuration if the wrong account appears. Requires a Ghast build with stdio credentialEnv support.

- MCP: `npx -y @rollbar/mcp-server@0.6.0`
- [官方文档 / Provider documentation](https://docs.rollbar.com/docs/mcp-server-setup)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://framerusercontent.com/images/pPKEABOv0Xd4KgtEqnJLwPG6HY.png
