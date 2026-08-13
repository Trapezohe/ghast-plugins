# DigitalOcean

Provision a DigitalOcean Droplet as a remote SSH workspace and inspect or explicitly manage Droplets, images, sizes, regions, account billing, actions, and SSH keys through DigitalOcean's official hosted MCP services.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/digitalocean-labs/mcp-digitalocean` at `acbe39190b822268192d02ffd77b50319bb3d071`.

The MCP endpoints and 54 account, Droplet, image, size, region, billing, action, and SSH-key tools come from DigitalOcean's pinned MIT-licensed official MCP repository. The workflow and two local SSH helper scripts are independently written by Ghast. DigitalOcean's separate CodexPlugin repository is pinned only as capability evidence because it publishes no license; none of its code, text, templates, or artwork is copied.

## Ghast compatibility

- The Codex private app mapping is replaced by DigitalOcean's official accounts and droplets Streamable HTTP MCP services. Both advertise read/write scopes, browser OAuth, public dynamic clients, refresh tokens, and PKCE S256.
- The generated provision-droplet skill preserves the Codex workflow's SSH-key upload, region and size selection, image verification, Droplet creation, bounded status checks, SSH configuration, remote-workspace handoff, and cleanup.
- The official MCP surface is a strict superset of the six private app tools used by the Codex workflow: 11 account tools, 42 Droplet/image/size tools, and the common region-list tool.
- Creation, rebuild, restore, reset, power, resize, image, SSH-key, and deletion operations follow DigitalOcean's official safety annotations and require exact-target review and explicit confirmation.
- The helpers never scan and trust a host key blindly. The generated SSH config uses accept-new for the first connection; users may instead verify and pin a fingerprint through their normal OpenSSH workflow.
- A generic cloud-server icon is used because the licensed MCP source does not grant redistribution rights for DigitalOcean marketplace artwork.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
