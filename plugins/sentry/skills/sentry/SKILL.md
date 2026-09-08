---
name: sentry
description: Investigate Sentry issues, events and application performance with the official Sentry MCP. Use for production error triage, release investigation and evidence-backed incident summaries.
---

# Sentry investigation in Ghast

Use the installed Sentry MCP connection. If authorization is needed, direct the
user to the connection in Ghast's Sentry plugin detail page; never request a
secret in chat. Discover actual tool names and schemas from the connected
server rather than relying on a fixed tool inventory.

## Investigation

1. Resolve the organization and project from the user's link or accessible
   records. Clarify only ambiguous targets. Establish the requested environment
   and time window; do not silently assume that production is named `prod`.
2. Find relevant issues, then read representative events and available release
   or performance context. Preserve issue IDs, event times and source links.
3. Distinguish the number of events from affected users and unique issues.
   State filters and pagination limits when reporting totals or rankings.
4. Compare observed symptoms, release timing and available traces. Explain
   which evidence supports a likely cause and which hypotheses remain untested.
5. Return a concise incident summary with impact, first/last observed time,
   relevant release, evidence links and concrete next checks. Empty results or
   permission failures do not establish that the application is healthy.

## Output and changes

Investigation requests authorize reads. Resolving issues, assigning ownership,
changing projects or triggering analysis jobs needs an explicit user request
covering that action. The server can expose write tools; this workflow does not
claim that its transport or OAuth token is technically read-only.

Report only the diagnostic fields needed. Omit authentication headers, cookies,
request bodies containing secrets, raw user data, emails and IP addresses from
chat and artifacts. Prefer short, sanitized excerpts to raw event payloads or
complete traces. The plugin does not provide a deterministic redaction proxy.

For authorized changes, inspect current state and available permissions first.
After an uncertain response, read the target before retrying a mutation. Report
verified results separately from failed, skipped or unobserved operations.
