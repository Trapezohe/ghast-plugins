# WeatherAPI.com for Ghast

## 简介 / Overview

通过 WeatherAPI.com 官方 MCP 获取实时天气、预报、历史天气、海洋与天文数据。

Access current weather, forecasts, historical conditions, marine data and astronomy through WeatherAPI.com’s official MCP.

## 连接 / Connection

需要 Node.js 20+ 和 npm。在 WeatherAPI.com 创建 API Key，并填入 Ghast 插件凭据字段；Ghast 通过 WEATHERAPI_KEY 环境变量注入官方本地服务。不要在聊天中发送 Key。功能和配额取决于服务商套餐。 原生启动与发现得到 11 个工具；使用无效测试 Key 读取当前天气返回服务商错误 2006。未测试真实账号天气查询。

Install Node.js 20+ and npm. Create a WeatherAPI.com API key and enter it in Ghast’s plugin credential field. Ghast supplies WEATHERAPI_KEY to the official local server; never paste keys into chat. Provider plans and quotas apply. Native startup and discovery exposed 11 tools. A current-weather read with an invalid fixture key returned provider error 2006. No real account weather query was tested.

- MCP: `npx -y weatherapi-mcp@1.0.0`
- [官方文档 / Provider documentation](https://github.com/weatherapicom/weatherapi-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn.weatherapi.com/v4/images/weatherapi_logo.png
