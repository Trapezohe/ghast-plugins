# DingTalk for Ghast

## 简介 / Overview

通过钉钉官方 MCP 访问通讯录、日历、待办、日志与协作服务。

Access contacts, calendars, tasks, reports and collaboration services through DingTalk’s official MCP.

## 连接 / Connection

需要 Node.js >=16、npx 及你自己的钉钉企业应用。在 Ghast 连接凭据中填写 DINGTALK_Client_ID、DINGTALK_Client_Secret，并在钉钉开放平台申请对应 API 权限。启用全部官方服务分类，但具体操作仍需其对应权限。ROBOT_CODE、ROBOT_ACCESS_TOKEN、DINGTALK_AGENT_ID 为机器人消息或工作通知的可选配置，不是其他接口的必填项。官方包会在包目录缓存访问 Token。需要支持 stdio credentialEnv 与 optionalCredentials 的 Ghast 版本。从 ghast.1 更新后，由于受保护的进程配置已变化，需要重新填写应用凭据。

Requires Node.js >=16, npx and your own DingTalk enterprise application. Enter DINGTALK_Client_ID and DINGTALK_Client_Secret in Ghast connection credentials, then grant the required API permissions in the DingTalk developer console. All official profiles are exposed; individual operations still require their corresponding permissions. ROBOT_CODE, ROBOT_ACCESS_TOKEN and DINGTALK_AGENT_ID are optional settings for robot messages or work notifications, not requirements for unrelated APIs. The official package caches access tokens in its package directory. Requires Ghast stdio credentialEnv and optionalCredentials support. After updating from ghast.1, re-enter the app credentials because the protected process configuration has changed.

- MCP: `npx -y dingtalk-mcp@1.1.21`
- [官方文档 / Provider documentation](https://github.com/open-dingtalk/dingtalk-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商官方 MCP 服务与软件包，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using official provider MCP services and packages, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://avatars.githubusercontent.com/u/31611746?v=4
