# Linear

Ghast-maintained workflows for Linear issues, projects and team collaboration.

## Official connection

Connect directly to Linear's official Streamable HTTP service at
`https://mcp.linear.app/mcp`. Linear documents OAuth 2.1 with dynamic client
registration. Ghast handles the connection through its native MCP client.
The plugin does not use Codex plugin packages, private connector IDs or OAuth
credentials from another host.

Source: https://linear.app/docs/mcp

## Language and branding

The manifest provides separate English and Simplified Chinese introductions;
Ghast selects Chinese for Chinese UI languages and English otherwise.

Logo source: https://linear.app/static/apple-touch-icon.png?v=2
The brand asset remains Linear's property. The MIT license covers only
Ghast-authored configuration and workflow text, not Linear's logo or service.

Installing the plugin does not authorize account access. Connect a Linear
account separately; workspace permissions determine the available records and
operations. Authenticated business operations require the user's account and
are not claimed as tested by local installation checks.
