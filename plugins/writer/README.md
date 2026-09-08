# WRITER for Ghast

## 简介 / Overview

连接 WRITER 官方 MCP，进行内容生成、翻译、文件处理和知识图谱工作。

Connect WRITER’s official MCP for content generation, translation, file processing and knowledge graph workflows.

## 连接 / Connection

需要 Node.js 与 npx。在 Ghast 凭据输入框填写 WRITER API Key。本包固定官方 2.3.2 版本，使用直接 API 工具模式。3.0.0 已切换为代码执行工具，本次文档查询返回项目缺失或需要 Stainless Key 的错误。本配置关闭可选远程文档工具，直接 API 工具包含参数定义。使用受 WRITER API 配额与计费限制。未测试真实账号内容生成、文件上传或知识图谱修改。

Requires Node.js and npx. Enter a WRITER API key in Ghast’s credential field. This package pins official version 2.3.2 in direct API-tool mode. Version 3.0.0 switched to code-mode tools; its documentation lookup failed during verification with a missing-project/Stainless-key error. The optional remote docs tool is disabled here; the direct tools include parameter schemas. WRITER API quotas and billing apply. No real account generation, file upload or knowledge graph changes were tested.

- MCP: `npx -y writer-sdk-mcp@2.3.2 --tools=all --no-tools=docs`
- [官方文档 / Provider documentation](https://dev.writer.com/home/mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://writer.com/wp-content/uploads/2021/08/writer-w-logo-1.png?w=192
