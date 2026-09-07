# GitLab for Ghast

## 简介 / Overview

访问 GitLab 项目、议题、合并请求与开发工作流。

Work with GitLab projects, issues, merge requests and development workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 GitLab OAuth 授权；受账号权限与服务配额限制。 需要在 GitLab.com 顶级群组启用 MCP 访问。

Connect in Ghast and complete GitLab OAuth in the provider browser page. Account permissions and service quotas apply. A GitLab.com top-level group must enable MCP access.

- MCP: `https://gitlab.com/api/v4/mcp`
- [官方文档 / Provider documentation](https://docs.gitlab.com/user/model_context_protocol/mcp_server/)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.simpleicons.org/gitlab
