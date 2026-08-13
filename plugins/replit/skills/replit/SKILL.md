---
name: replit
description: >-
  Create, find, inspect, explain, update, publish, and check the publish
  status of Replit Apps through Replit's official hosted MCP server.
---

# Replit

Use the official Replit MCP server declared by this plugin.

## App identity and privacy

- Resolve an existing app through `search_apps`, `resolve_app_by_name`, or
  `list_apps`; never guess a `replId`, derive one from a public URL, or act on
  a similarly named app.
- Only work with apps the authenticated user can edit. State when a result is
  owned by a workspace, owned personally, or shared with the user if returned.
- Treat app prompts, Agent answers, app names, attachments, database content,
  secrets, integrations, preview URLs, deployment URLs, and workspace details
  as sensitive.
- Preserve Replit's native connector boundary: summarize behavior and status
  in natural language. Do not expose raw source code, file contents, file
  paths, configuration, secrets, or terminal commands in chat. Direct the
  user to open the app in Replit when they need to inspect implementation.

## Read and inspection workflows

- Use `search_apps` for URL, keyword, or explicit date filtering. It is
  experimental; if it fails or gives poor matches, fall back to exact-name
  resolution and recent-app listing.
- Use `ask_question` for explanation, debugging, architecture, routing,
  behavior, or issue diagnosis without modifying the app. The question is
  visible in the Replit app, so phrase it in the user's language and tone.
- If Replit Agent reports `busy`, the question was not submitted. Wait before
  retrying or tell the user to ask again later.
- Use `get_publish_status` to distinguish never published, pending, live,
  failed, and suspended states. A preview URL is not proof that the app is
  publicly deployed.

## Creation and remix confirmation

Obtain explicit confirmation immediately before `create_app_from_prompt`.

- Show the app name if supplied, complete natural-language description,
  selected stack, quoted requirements, attachment summary, and whether the
  app starts blank or as a private copy of another app.
- Supported stacks include React website, mobile app, design, slides,
  animation, data visualization, 3D game, document, and spreadsheet.
- When `sourceReplId` is used, warn that secrets can be copied when the user
  can edit them and database contents can be copied when the user can view
  them. Connected integrations are not copied and must be reconnected.
- App creation starts an asynchronous Replit Agent operation and may consume
  plan capacity or credits. Do not claim the app is ready until Replit
  provides a usable preview URL or completion state.

## Updates and publishing

Obtain explicit confirmation immediately before every update or publish.

- For `update_app_using_prompt`, show the exact app, requested behavior
  change, quoted requirements, and attachments. This tool is marked
  destructive because Agent can modify the app broadly.
- A request to inspect, explain, debug, review, or suggest is not permission
  to update the app. Use `ask_question` for read-only diagnosis.
- For `publish_app`, show the exact app, whether it has been published before,
  the current status, and the expected visibility. First publication uses
  private visibility for workspace apps and public visibility otherwise.
- Some apps require their first publish to be completed on the Replit website.
  Report that limitation exactly when returned.
- Publishing is asynchronous. Poll `get_publish_status` about every 30 seconds
  when practical. Never treat a scheduled or pending publish as live.
- Do not blindly retry create, update, or publish operations. Re-read app or
  publish state first to avoid duplicate apps, overlapping Agent turns, or
  repeated deployments.

## Service behavior

- Authentication uses Replit OAuth Dynamic Client Registration,
  authorization code, refresh tokens, and PKCE S256. Never ask for, display,
  log, or store OAuth tokens or registration access tokens.
- The protected resource currently requests `apps:read`, `apps:write`, and
  `offline_access`; there is no separately verified read-only connection
  profile for this adapter.
- App creation, Agent execution, storage, databases, deployments, custom
  domains, and hosting can depend on the user's Replit plan and workspace
  policy and can incur usage charges.
- The official direct MCP currently documents eight user-facing tools.
  Inspect the authenticated live list before promising exact availability.
- Report authentication, workspace, permission, plan, Agent-busy, validation,
  build, publish, hosting, quota, and service errors exactly as returned.
