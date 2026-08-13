---
name: ddtoolsets
description: Inspect and configure Datadog MCP toolsets in Ghast while keeping the active tool surface narrow and reviewable.
---

# Datadog MCP Toolsets

Toolsets group Datadog tools by product. Keeping only the needed groups enabled
reduces tool-selection ambiguity and context usage.

## Inspect

Read `datadog://mcp/toolsets` from the `datadog` MCP server. Present every
available toolset, whether it is enabled, whether it is a server default, and
its live description. If the resource is unavailable, diagnose the connection
with `ddconfig`; do not guess that a product toolset exists.

The plugin uses `core,widgets` when `DD_MCP_TOOLSETS` is unset. Current
documented groups include core observability plus APM, alerting, audit trail,
cases, cost, dashboards, data observability, database monitoring, DDSQL, error
tracking, experiments, feature flags, forms, Kubernetes, networks, onboarding,
product analytics, profiling, reference tables, RUM, security, session replay,
software delivery, synthetics, widgets, and workflows. Availability can depend
on the organization and product plan.

## Change

1. Understand whether the user wants to add, remove, replace, or reset groups.
2. Show the exact resulting comma-separated list before changing anything.
3. Warn before removing `core`, because most incident and telemetry workflows
   depend on it.
4. Ask the user to set `DD_MCP_TOOLSETS` to the confirmed list. Use `all` only
   when the user explicitly wants every generally available group. Use
   `default` to defer to Datadog's current server defaults.
5. Reload the active Ghast profile and read `datadog://mcp/toolsets` again to
   verify the result.

Toolset selection changes which tools are exposed; it does not grant new
Datadog permissions or product entitlements.
