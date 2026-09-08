# Infobip for Ghast

## 简介 / Overview

连接 Infobip 官方 SMS、邮件、WhatsApp、语音、客户资料、账号管理及文档工具。

Connect official Infobip tools for SMS, email, WhatsApp, voice, customer profiles, account management and documentation.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Infobip OAuth 授权；受账号权限与服务配额限制。 按需分别授权 SMS、邮件、WhatsApp、语音、People 客户资料和账号管理；公开文档检索无需账号。产品可用性、发件人登记、权限与通信费用取决于账号。试用消息仅可发送给已验证的收件人。

Connect in Ghast and complete Infobip OAuth in the provider browser page. Account permissions and service quotas apply. Connect only the product services you need: SMS, email, WhatsApp, voice, People and account management each have their own OAuth connection. Public documentation search needs no account. Product availability, sender registration, scopes and messaging fees depend on your account. Trial messaging is limited to verified recipients.

- MCP: `https://mcp.infobip.com/sms`
- MCP: `https://mcp.infobip.com/email`
- MCP: `https://mcp.infobip.com/whatsapp`
- MCP: `https://mcp.infobip.com/voice`
- MCP: `https://mcp.infobip.com/people`
- MCP: `https://mcp.infobip.com/account-management`
- MCP: `https://mcp.infobip.com/search`
- [官方文档 / Provider documentation](https://www.infobip.com/docs/mcp/using-mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://cdn-web.infobip.com/uploads/2025/06/cropped-infobip-logo-favicon.png
