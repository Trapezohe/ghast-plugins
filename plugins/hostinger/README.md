# Hostinger

Create Hostinger Horizons websites from natural-language briefs and build, connect, deploy, verify, and operate websites, domains, DNS, VPS, ecommerce, WordPress, mail, campaigns, and billing through Hostinger's official MCP and Headless skill.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/hostinger/api-mcp-server` at `cc04bafbeae9362a35af1b6443d3c3833f9f30d5`.

The complete Hostinger Headless skill tree and MIT license are copied from Hostinger's pinned official repository. Ghast connects directly to Hostinger's official hosted OAuth MCP service; the separately published 314-tool server source and npm package remain available from the same repository but are not duplicated inside this plugin.

## Ghast compatibility

- The Codex private app mapping is replaced by Hostinger's official hosted Streamable HTTP MCP endpoint with browser OAuth and the mcp:use scope.
- The official all-tool server exposes 314 tools. Its Horizons group exposes horizons_createWebsiteV1 for natural-language website creation and horizons_getWebsiteV1 for the resulting edit URL, matching the Codex snapshot's declared build-and-launch surface.
- Hostinger's official Headless skill adds create, connect, and iterate workflows for static or Node.js sites, custom storefronts, and WordPress-backed content, including live deployment verification and project-local site metadata.
- The official MCP publishes no safety annotations. Ghast therefore requires explicit review and confirmation for deployments, overwrites, purchases, provisioning, DNS, billing, email, store, WordPress, VPS, credential, and other state-changing operations.
- A generic hosting-and-deployment icon is used because the official MIT repository does not publish licensed catalog artwork.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
