# AB Tasty Feature Experimentation for Ghast

## 简介 / Overview

通过 AB Tasty 官方 Feature Experimentation MCP 查看访客功能开关与实验活动配置。

Inspect visitor feature flags and campaign configuration with AB Tasty’s official Feature Experimentation MCP.

## 连接 / Connection

需要 Node.js 18+ 和 npm，在 Ghast 填写 Feature Experimentation 环境 ID 与 API Key。Resource Loader 凭据按需填写：Feature Experimentation 需要账号 ID、账号环境 ID 和 RCA Token；Web Experimentation 需要账号 ID 与 Token。不使用的组留空。代码扫描另需官方 @abtasty/codebase-analyzer-typescript 包，本插件未捆绑该分析器。 本地启动发现 7 个工具；无效测试凭据读取返回认证错误。未测试真实账号操作。

Install Node.js 18+ and npm. Enter the Feature Experimentation environment ID and API key in Ghast. Optional Resource Loader fields are needed only for the corresponding features: Feature Experimentation requires account ID, account environment ID and RCA token; Web Experimentation requires account ID and token. Leave unused groups blank. Codebase analysis requires the separate official @abtasty/codebase-analyzer-typescript package and is not bundled here. Local startup exposed 7 tools; a read with invalid fixture credentials returned an authentication error. Real account operations were not tested.

- MCP: `npx -y @abtasty/mcp-server@0.3.0`
- [官方文档 / Provider documentation](https://github.com/flagship-io/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/8311305?v=4
