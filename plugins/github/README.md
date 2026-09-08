# GitHub for Ghast

## 简介 / Overview

读取仓库、审查 PR、管理 Issue 与排查 CI；优先浏览器授权，Token 作为高级备选。

Read repositories, review pull requests, manage issues and diagnose GitHub Actions. Prefer browser authorization; personal tokens are an advanced alternative.


A Ghast-authored workflow bundle using GitHub's official hosted MCP server.
It does not redistribute OpenAI's private connector or claim GitHub authorship.

## Connect

Install this plugin and open its details. Browser authorization requires Ghast’s registered OAuth application; until configured the interface explicitly shows setup pending. To use a personal token instead, expand **Advanced: use an API key or token**, enter `github-token`, then select **Save and connect**. Ghast stores the value
in the active profile's encrypted vault, scoped to this server URL. It never
belongs in this package or a chat message. Use a token limited to the repositories
and operations you need. Organization policy or SSO may require additional
approval. Select **Disconnect** to remove the locally saved credential; revoke
the token in GitHub if it should no longer work elsewhere.

Ask Ghast to summarize a PR or inspect a failing Actions run. The package exposes
repos, issues, pull requests, actions and users toolsets; the actual tools and
access depend on the hosted server and token permissions. Write actions still
require a user request and Ghast's normal execution permissions.

## OAuth alternative

GitHub also distributes a native `github-mcp-server stdio` binary whose official
build includes its own OAuth app on github.com. This can be configured as a local
MCP server after installing the official binary. It is not automatically bundled
or installed by this hosted-MCP plugin. Enterprise hosts require separate setup.

OpenAI's `.app.json` only references a connection in OpenAI's backend. Those IDs
are not endpoints and cannot authenticate Ghast. This package therefore uses a
publicly documented, independently accessible server.

## Sources and verification

- https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md
- https://github.com/github/github-mcp-server/blob/main/docs/host-integration.md
- https://github.com/github/github-mcp-server/blob/main/docs/oauth-login.md

Account-backed PR/CI reads and writes require real account acceptance; package
validation alone does not establish that these operations passed.

## Browser authorization

GitHub remote MCP supports OAuth but does not support dynamic client registration. Ghast must register and configure its own GitHub App or OAuth App before the managed browser-login experience can be enabled. Until then the client displays an explicit setup-pending state. Personal tokens remain optional under advanced settings, and existing saved tokens continue to work. Never embed a client secret in a distributed plugin.

GitHub 远程 MCP 支持 OAuth，但不支持动态客户端注册。Ghast 必须先注册并配置自己的 GitHub App 或 OAuth App。尚未完成时显示明确的待配置状态；个人 Token 作为高级可选方式保留，已保存的 Token 仍可使用。不要将 Client Secret 打包进插件。

Source: https://github.com/github/github-mcp-server/blob/main/docs/host-integration.md
