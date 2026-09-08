---
name: linear
description: Search and manage Linear issues, projects, comments and team workflows through Linear's official MCP. Use for triage, planning, progress reports and authorized updates.
---

# Linear work in Ghast

Use the installed Linear connection and its current tool catalog. Tool names,
fields and available operations come from the connected service; do not assume
that a remembered tool name or an unavailable operation exists.

## Connection and scope

If the connection requires login, direct the user to the Linear connection in
Ghast's plugin detail page. Resume the requested work when tools become
available. Never ask for credentials in chat or clear browser cookies.

Identify the relevant workspace, team and issue or project from the request and
accessible records. Ask only when multiple matches affect the intended action.
Use record IDs returned by Linear, not guessed identifiers.

## Read and act

- For triage, read issue details and current team workflow states. Separate
  reported symptoms, verified evidence and proposed priority or assignment.
- For planning, inspect existing projects, cycles, labels and dependencies.
  Turn the supplied scope into concrete issues without inventing owners,
  deadlines or dependencies. Reuse existing records to avoid duplicate work.
- For workload or cycle summaries, apply the requested team and date filters,
  follow pagination and distinguish completed work from pending work.
- For documentation review, search relevant documents and issues, link source
  records and identify gaps before proposing new tracking issues.
- For authorized creates or updates, read current values first and change only
  the requested fields. Use existing authorization; clarify materially ambiguous
  targets or scope before writes. Publish comments only when explicitly asked.
- For bulk edits, keep a record of each result. After uncertain network outcomes,
  inspect the target before retrying a create or comment to avoid duplicates.

Read back changed records when the response does not establish the final state.
Report what changed with Linear links and distinguish failed, skipped and
unverified operations. Account permissions, rate limits and missing tools are
concrete limits, not evidence that a record or capability does not exist.
