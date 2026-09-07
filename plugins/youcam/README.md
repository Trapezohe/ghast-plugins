# YouCam for Ghast

## 简介 / Overview

使用玩美移动 YouCam 进行图片与视频编辑、美妆效果预览和虚拟试穿。

Use Perfect Corp’s YouCam tools for image and video editing, beauty visualization and virtual try-on.

## 连接 / Connection

在 YouCam 账号中创建 API Token，填入 Ghast 连接凭据输入框；由 Ghast 注入 Authorization 请求头。不要在聊天中发送凭据，使用受服务配额限制。

Create a YouCam API token in your provider account and enter it in the Ghast connection credential field. Ghast supplies the Authorization header; do not paste credentials into chat. Service quotas apply.

- MCP: `https://mcp-api-01.makeupar.com/mcp/creators`
- [官方文档 / Provider documentation](https://docs.perfectcorp.com/develop/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://yce.perfectcorp.com/apple-touch-icon.png

- MCP: `https://mcp-api-01.makeupar.com/mcp/beauty`
- MCP: `https://mcp-api-01.makeupar.com/mcp/fashion`



验证包括公开端点响应、认证发现和本地安装/卸载；未验证真实账号的业务读写。

Validation covers public endpoint responses, auth discovery and local install/removal. Business reads and writes using a real account have not been tested.
