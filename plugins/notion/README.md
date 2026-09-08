# Notion

Four Ghast-authored workflows cover knowledge capture, meeting preparation,
research documentation and specification-to-task planning. They connect to
Notion's official hosted MCP through Ghast's native client.

Official connection documentation:
https://developers.notion.com/guides/mcp/get-started-with-mcp

Endpoint: `https://mcp.notion.com/mcp` (Streamable HTTP, OAuth).
Install the plugin, then connect the intended workspace from its detail page.
Workspace access and available tools remain controlled by Notion. Installation
and OAuth redirect checks do not establish authenticated page access.

This version replaces the OpenAI-derived workflow text and bundled examples
with Ghast-maintained instructions. It retains all four workflow entry points,
uses current tool schemas, and does not load Codex plugin packages or credentials.
English and Chinese introductions are separate fields selected by UI language.

Logo source: https://avatars.githubusercontent.com/u/4792552?v=4
The official `makenotion` organization identifies itself as Notion and links
to its website. Notion retains ownership of the brand asset; the MIT license
covers Ghast-authored text and configuration only.
