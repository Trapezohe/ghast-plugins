# Cartesia for Ghast

## 简介 / Overview

通过 Cartesia 官方 MCP 生成语音、转录音频，并管理声音和发音词典。

Generate speech, transcribe audio and manage voices and pronunciation dictionaries through Cartesia’s official MCP server.

## 连接 / Connection

需要 uv/uvx 和 Python 3.13+（uvx 可安装 Python）。在 Cartesia Playground 创建标准 API Key，填入 CARTESIA_API_KEY。普通音频与声音工具使用 cartesia 连接，仅需标准 API Key。可选的 cartesia-admin 连接需要标准 API Key 与独立管理员 Key，用于管理工具。更新连接配置后，请重新填写标准 Key。默认工具覆盖语音生成、转录、声音和发音词典。生成音频保存在该插件的 Ghast 数据目录。需要支持 stdio credentialEnv 的 Ghast 版本。

Requires uv/uvx and Python 3.13+ (uvx can install Python). Create a standard Cartesia API key in the Playground and enter it in CARTESIA_API_KEY. Use the cartesia connection with a standard API key for audio and voice tools. The optional cartesia-admin connection requires both the standard API key and a separate admin key for management tools. Re-enter the standard key after updating this plugin’s connection configuration. Default tools cover speech generation, transcription, voices and pronunciation dictionaries. Generated audio is saved in this plugin’s Ghast data directory. Requires Ghast stdio credentialEnv support.

- MCP: `uvx --python 3.13 cartesia-mcp==0.21.0`
- [官方文档 / Provider documentation](https://docs.cartesia.ai/tools/ai/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cartesia.ai/favicon.svg
