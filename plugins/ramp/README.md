# Ramp for Ghast

## 简介 / Overview

连接 Ramp 官方账号、开发文档和基准数据服务，支持企业支出与财务办公流程。

Connect Ramp’s official account, developer documentation and benchmark data services for spend and finance workflows.

## 连接 / Connection

在 Ghast 中连接，通过服务商网页完成 Ramp OAuth 授权；受账号权限与服务配额限制。 账号连接：使用具有相应角色并已开启 MCP 权限的 Ramp 账号登录。自定义客户端回调 URI 可能需要 Ramp 加入允许名单；能够跳转 OAuth 不代表回调地址已获批准。开发文档：无需账号，已成功读取公开文档。Ramp Data：需向 Ramp Data Partner Program 申请访问权限，并在单独连接输入框填写其 API Key。已发现 9 个数据工具，但测试 Key 被上游 API 拒绝。公开基准数据不等于企业账号的私有数据。未测试真实账号操作、审批、付款或已认证的基准数据调用。

Connect in Ghast and complete Ramp OAuth in the provider browser page. Account permissions and service quotas apply. Account connection: sign in to Ramp with the appropriate role and enabled MCP access. Custom client callback URIs may require Ramp allowlisting; reaching an OAuth redirect does not establish that the callback is approved. Developer docs: no account required; public docs retrieval succeeded. Ramp Data: request provisioned access from the Ramp Data Partner Program and enter its API key in the separate connection field. Nine data tools were discovered, but the fixture key was rejected by the upstream API. These public benchmarks are not private company account data. No real account actions, approvals, payments or authenticated benchmark calls were tested.

- Account MCP: `https://mcp.ramp.com/mcp`
- Developer MCP: `https://mcp.ramp.com/developer/mcp`
- Data MCP: `https://mcp.ramp.com/ramp-data/mcp`
- [Developer MCP](https://docs.ramp.com/developer-api/v1/developer-mcp)
- [Ramp Data MCP](https://docs.ramp.com/developer-api/v1/ramp-data-mcp)
- [官方文档 / Provider documentation](https://docs.ramp.com/developer-api/v1/mcp)

安装后在插件详情连接服务。安装成功不代表账号授权或业务调用成功。

Install the plugin, then connect in its detail page. Installation does not prove account authorization or business task execution.

本包由 Ghast 独立编写，使用服务商公开 MCP，不包含 Codex 私有连接器或账号凭据。

Independently authored for Ghast using public provider MCP services, without Codex private connectors or credentials.

## License / 许可

Ghast-authored manifests and skill text are MIT licensed. Brand names and logos belong to their respective owners. 品牌名称与标识归相应权利人所有。

Brand logo source: https://agents.ramp.com/icon.svg?icon.3fh2nsuef-sof.svg?dpl=dpl_AVYHX3qHmX8khAHL6vaW1u8Ysune
