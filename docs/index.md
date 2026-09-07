# Ghast OAuth client

This site publishes the [OAuth client metadata](oauth-client.json) used by Ghast Desktop to connect to providers that support Client ID Metadata Documents. It contains public application identity only, never user credentials or tokens.

本页面发布 Ghast 桌面客户端的公开 OAuth 身份文档，供支持 Client ID Metadata Documents 的服务商读取；不包含用户凭据或 Token。

Ghast is a native public client using authorization code flow with PKCE. The loopback callback uses the application's local port, as described in RFC 8252 §7.3. Account access requires the user's provider consent.

Ghast 使用原生公开客户端的授权码与 PKCE 流程，回调按 RFC 8252 §7.3 使用应用的本地监听端口；账号访问仍需用户在服务商页面授权。

[Plugin repository](https://github.com/Trapezohe/ghast-plugins)
