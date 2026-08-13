---
name: mixpanel:install
description: Configure or repair the official Mixpanel MCP, mixpanel-headless SDK, region, or authentication mode.
argument-hint: [mcp|headless|custom] [us|eu|in] [oauth|service-account]
---

# Mixpanel Install

Use the `install` skill from this plugin. Treat `$ARGUMENTS` only as the
user's preferred engine, region, or authentication mode; still run every
verification and credential-safety check in the skill. Never request or echo
a Mixpanel secret or token.
