---
name: asana-usage
description: Best practices for using Asana MCP tools in Ghast. Use when working with tasks, projects, or portfolios.
---

# Asana Usage Best Practices

## Before using Asana tools

Always verify the MCP connection is active. If tools are unavailable, run the `asana-setup` skill first.

## Working with tasks

- When creating tasks, always confirm the target project with the user before creating
- When searching, prefer specific project or section filters over broad workspace searches
- Always show the user a summary of what will be created or modified before taking action
- For bulk operations (creating multiple tasks), list them all first and ask for confirmation

## Working with projects

- Never delete a project without explicit user confirmation
- When duplicating a project, confirm the new name before proceeding
- Section names matter — confirm with the user before moving tasks between sections

## Handling ambiguity

- If the user references "my project" or "the team" without being specific, ask which project they mean before taking action
- If multiple workspaces exist, ask the user which one to use before searching or creating

## Error handling

- If an MCP tool call fails with an auth error, run the `asana-setup` skill
- If a task or project GID is not found, do not guess — ask the user to verify the resource exists
- Rate limit errors: wait 10 seconds and retry once before reporting the error to the user

## Ghast and Asana V2 rules

- Never expose raw Asana GIDs in conversational responses when a human-readable
  name is available.
- Prefer the most specific tool. Use `search_objects` only to resolve unknown
  identifiers, and use `get_my_tasks` for "what is on my plate" requests.
- Read current state before changing tasks, dependencies, project membership,
  followers, custom fields, completion, dates, assignees, or parent links.
- Obtain explicit confirmation before every create, update, comment, project
  status update, archive, or delete operation. Show the target names and exact
  proposed values first.
- `delete_task` is permanent and can also remove subtasks that are not members
  of another project. Require a fresh, explicit confirmation immediately
  before calling it.
- For up to 50-task batch creates or updates, list every affected task and
  field change before confirmation. Split vague "do everything" requests into
  reviewable steps.
- Use comments only for discussion or context, not for events Asana already
  records automatically. Show the full proposed comment before posting it.
- Interactive preview tools may be unavailable outside Claude and ChatGPT.
  In Ghast, perform the equivalent preview in conversation and call standard
  write tools only after confirmation.
- Do not blindly retry a failed write. Read current state first to avoid
  duplicate tasks, comments, projects, or status updates.
- Advanced `search_tasks` requires an eligible Premium workspace. Fall back to
  filtered `get_tasks` when the service reports that limitation.
- Access is limited to the authorized user's existing permissions and the
  workspace selected during OAuth. Never claim broader visibility.
