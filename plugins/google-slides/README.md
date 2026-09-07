# Google Slides for Ghast

## 简介 / Overview

通过 Google 官方 Workspace MCP 服务阅读与更新演示文稿。

Read and update presentations through Google’s official Workspace MCP service.

## 连接 / Connection

需要 Google Workspace 开发者预览访问权限、已配置的 Google Cloud 项目与自有 OAuth 应用。在 Ghast 中展开使用自有 OAuth 登录应用，将显示的回调地址注册到 Google；启用对应产品及 MCP API，配置授权同意屏幕与测试用户，在连接表单填写 Client ID、Secret 与所需权限范围，不要在聊天中发送凭据。需要支持 OAuth 应用配置的 Ghast 版本。

Requires Google Workspace Developer Preview access, a configured Google Cloud project and your own OAuth client. Open Use your own OAuth application in Ghast and register the displayed callback URL with Google. Enable the product and MCP APIs and configure consent/test users. Enter the client ID, secret and required scopes in the connection form, never in chat. Requires a Ghast build with OAuth application configuration support.

- MCP: `https://slidesmcp.googleapis.com/mcp/v1`
- [官方文档 / Provider documentation](https://developers.google.com/workspace/guides/configure-mcp-servers)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.gstatic.com/images/branding/productlogos/slides_2026/v2/web/192px.svg

## OAuth scopes / 权限范围

在 Google 同意屏幕与 Ghast 权限范围输入框配置所需权限。以下为起点；按实际任务缩减，日历写入另需 calendar.events，邮件标签修改另需 gmail.modify。权限范围不会让未开放的工具自动出现。Google Chat 还需要在项目中配置 Chat 应用。

Configure the scopes in both Google consent settings and the Ghast scopes field. Start with the following and reduce them to the task requirements. Calendar writes additionally need calendar.events; Gmail label changes need gmail.modify. Scopes do not create unavailable tools. Google Chat also requires a Chat app configured in the project.

```text
https://www.googleapis.com/auth/presentations.readonly https://www.googleapis.com/auth/presentations
```

验证范围：端点初始化、工具发现、OAuth 元数据与本地安装/卸载。未使用真实 Google 账号验证数据读写；授权与预览资格由 Google 决定。

Validation covers endpoint initialization, tool discovery, OAuth metadata and local install/uninstall. Google account data access has not been tested; Google determines authorization and preview eligibility.
