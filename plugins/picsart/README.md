# Picsart Gen-AI

Generate and edit images, video, audio, and motion graphics through Picsart's official skills, CLI workflows, and hosted MCP servers.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/PicsArt/gen-ai-skills` at `b52ed0d07fa8f7e94b29f194ab3eea99bb95b650`.

The 21 current shared skills, two hosted MCP declarations, manifest metadata, icon, and primary license come from Picsart's pinned gen-ai-skills repository. The batch and end-to-end workflow skills come from the matching official gen-ai CLI v2.61.0 source revision and retain that repository's MIT license.

## Ghast compatibility

- The Codex private app connector is replaced by Picsart's official public Gen-AI OAuth MCP and Creative API-key MCP endpoints.
- Ghast fixes four demonstrably broken relative-link groups in nested official references and redirects the retired @picsart/gen-ai-mcp installation link to the current gen-ai-use installation section.
- Every packaged skill receives the same Ghast safety boundary for paid generations, external uploads, durable Drive writes, permanent deletes, secrets, and ambiguous retries.
- The official Picsart icon is copied from the MIT-licensed gen-ai-skills repository.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
