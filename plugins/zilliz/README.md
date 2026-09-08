# Zilliz Cloud for Ghast

## 简介 / Overview

通过 Zilliz 官方 MCP 服务管理云端集群、集合和向量搜索。

Manage Zilliz Cloud clusters, collections and vector searches through the official Zilliz MCP server.

## 连接 / Connection

需要 uv／uvx 和 Python 3.12。在连接凭据 ZILLIZ_CLOUD_TOKEN 中填写 Zilliz Cloud API Key，并授予目标项目及集群所需权限。集群 user:password 凭据可能仅支持其对应数据访问。需要支持 stdio credentialEnv 的 Ghast 版本。官方包使用 MCP 1.x 接口，本配置固定 mcp==1.29.1，并直接调用官方模块，避免 CLI 横幅污染 JSON-RPC 输出；没有修改服务商源码。

Requires uv/uvx and Python 3.12. Enter a Zilliz Cloud API key in the ZILLIZ_CLOUD_TOKEN connection field, with permissions for the requested projects and clusters. Cluster user:password credentials may only allow their corresponding data access. Requires Ghast stdio credentialEnv support. The official package uses MCP 1.x APIs; this configuration pins mcp==1.29.1 and invokes its official modules directly to avoid CLI banners on the JSON-RPC output stream. No provider source is modified.

- MCP: `uvx --python 3.12 --with mcp==1.29.1 --from zilliz-mcp-server==1.0.0 python -c from zilliz_mcp_server.app import zilliz_mcp; from zilliz_mcp_server.tools.zilliz import zilliz_tools; from zilliz_mcp_server.tools.milvus import milvus_tools; zilliz_mcp.run(transport="stdio")`
- [官方文档 / Provider documentation](https://docs.zilliz.com/docs/zilliz-mcp-server)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://zilliz.com/favicon.svg
