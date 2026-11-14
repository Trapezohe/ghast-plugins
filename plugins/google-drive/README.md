# Google Drive for Ghast

## 简介 / Overview

通过 Google 官方 Drive API 与已连接的 Google 账号检索、阅读与整理云端硬盘文件。

Search, read and organize Drive files through Google’s official Drive API with your Google account.

## 连接 / Connection

安装后在插件详情选择“连接”，使用 Google 账号授权 Ghast。所有已安装的 Google 插件共用一次账号连接，授权请求只包含已安装服务所需的权限；断开连接会同时断开全部 Google 插件。无需 Google Cloud 项目、自有 OAuth 应用或开发者预览资格。需要支持 Google 共享账号连接的 Ghast 版本。

Install the plugin, then select Connect in its detail page and authorize Ghast with your Google account. All installed Google plugins share one account connection; the request covers only the installed services. Disconnecting removes access for every Google plugin. No Google Cloud project, own OAuth client or Developer Preview access is needed. Requires a Ghast build with shared Google account support.

- API: `https://www.googleapis.com/drive/v3/`
- [官方文档 / Provider documentation](https://developers.google.com/workspace/drive/api/reference/rest/v3)

安装成功不代表账号授权或业务调用成功。

Installation does not prove account authorization or business task execution.

## 工具 / Tools

Ghast 内置适配器读取 Google 官方 Discovery 文档，提供 `search_operations`、`describe_operation`、`read_operation`（GET）与 `write_operation`（POST/PUT/PATCH/DELETE）。只显示已授予权限可用的操作；支持 JSON 请求体，不支持二进制或 multipart 上传。

Ghast's built-in adapter reads Google's official Discovery document and provides `search_operations`, `describe_operation`, `read_operation` (GET) and `write_operation` (POST/PUT/PATCH/DELETE). Only operations allowed by the granted permissions are listed. JSON bodies are supported; binary and multipart uploads are not.

本包由 Ghast 独立编写，调用 Google 公开 REST API，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using Google's public REST APIs, without Codex private connectors or credentials.

## OAuth scopes / 权限范围

```text
https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/drive.file
```

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://www.gstatic.com/images/branding/productlogos/drive_2026/v2/web/192px.svg
