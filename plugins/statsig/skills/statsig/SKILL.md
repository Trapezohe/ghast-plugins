---
name: statsig
description: Use the Statsig MCP to inspect and manage Statsig entities such as gates, experiments, dynamic configs, segments, metrics, audit logs, and results.
---

# Statsig MCP

## Overview

Use the Statsig MCP server to inspect and manage Statsig entities, review rollout state, check experiment or gate results, inspect audit history, and answer configuration questions.

## Statsig MCP setup

This plugin already declares the official Statsig MCP bridge. It reads
`STATSIG_CONSOLE_API_KEY` from the host environment. Never ask for, print,
log, or write the key. Use a Console API key with only the permissions needed
for the requested read or write workflow. If the MCP is unavailable, ask the
user to set the environment variable and reload the active Ghast profile.

## Workflow

1. Analyze the user's query and determine the task type: discovery, inspection, results analysis, audit/history review, or config changes.
2. Identify the relevant Statsig entity types and names when possible. Common entities include gates, experiments, dynamic configs, segments, metrics, metric sources, and param stores.
3. Use list or search-style MCP tools first when the user does not provide an exact identifier. Use detail tools once you know the target object.
4. For performance or rollout questions, use the appropriate results endpoints or audit logs to understand behavior over time.
5. For create or update requests, confirm the intended object, preserve required fields, and apply the matching write tool carefully.
6. Summarize the key findings or changes clearly, including the object name, current state, important rules or metrics, and any follow-up actions.

## MCP usage

Use the MCP to fetch, inspect, create, and update Statsig objects. For the current capability list and example prompts, read `references/statsig-mcp.md`.

## Resources

- `references/statsig-mcp.md`: setup notes, MCP capabilities, and example prompts for Statsig MCP.
