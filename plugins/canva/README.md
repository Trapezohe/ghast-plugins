# Canva

Create, edit, review, resize, bulk-generate, and brand-check Canva designs through Canva's official skills and hosted MCP server.

## Official Ghast port

This package is generated directly from the developer-owned repository `https://github.com/canva-sdks/canva-skills` at `b56291ea0a36d0a941e1478b47959be5f1771dee`.

All six packaged skills, the MCP declaration, manifest metadata, and license come from Canva's pinned official multi-host plugin repository. The four workflows under inactive-skills are deliberately excluded because Canva says supported hosts do not register them.

## Ghast compatibility

- The Codex private app connector is replaced by Canva's official public Streamable HTTP endpoint with browser OAuth, Dynamic Client Registration, refresh tokens, and PKCE S256.
- A disposable localhost public client registered successfully during the audit, and its authorization request reached Canva's official login page in a real browser. No account login, token exchange, or design operation was performed.
- Canva's current active package supersedes the older Codex snapshot: it adds brand checking, bulk creation, safe design editing, structured review, and comment-driven feedback implementation, while older branded-presentation and translation skills are now inactive upstream.
- Generation, Brand Kit, copy, resize, export, content-read, and transactional editing primitives remain available in the official hosted MCP. Ghast does not silently reactivate Canva's inactive workflow files.
- A generic design-workspace icon is used because the Apache-2.0 source license does not grant Canva trademark rights and the main branch publishes no separately licensed catalog artwork.

External CLIs, accounts, credentials, paid services, and platform permissions remain user-managed dependencies.
