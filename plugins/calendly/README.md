# calendly

Inspect Calendly meetings, invitees, event types, schedules, busy times,
routing forms, and organization context, or safely create and update
scheduling resources through Calendly's official hosted MCP server.

## Official hosted MCP adapter

This package contains only Ghast-authored MCP configuration, safety
instructions, documentation, and catalog metadata. It does not copy or
redistribute Calendly's hosted MCP implementation, private Codex connector,
service source code, account data, or marketplace artwork.

The adapter is pinned to normalized visible text from Calendly's official MCP
overview with SHA-256 `9cc165e39526a0a4ee8d59e71ca88561b16b7f01b2599542afb2bc7d911af62f` and its complete
36-tool catalog with SHA-256 `62c1741ac3df3a3e5f216c5b9772c7bfe2a243869c2e398dcf62f9349215e773`. The
order-normalized OAuth protected-resource metadata is pinned at canonical JSON
SHA-256 `379eb5537223aadaaf138327e9bc293b71639d2a3c3ae3e8ebc4b26c23171f06`, and the authorization-server
metadata at `512f41277070a17997c1df424133f687337437528bd9e090359a37b8bbb2c5ef`.

## Ghast compatibility

- Ghast connects directly to `https://mcp.calendly.com` using Streamable HTTP and
  Calendly OAuth. The service requires Dynamic Client Registration, a public
  client, authorization code, and PKCE S256; a disposable localhost client
  registration was verified with HTTP 201.
- Calendly's official catalog exposes 36 tools for event types, event-type
  and user availability, busy times, meeting locations, scheduled events,
  invitees, booking, cancellation, no-show state, scheduling links, shares,
  routing forms, users, organizations, memberships, invitations, and
  server-provided skills.
- This covers the Codex app's event-type creation and update, scheduling-link
  generation, availability adjustment, meeting booking and cancellation,
  upcoming-meeting review, attendee detail, and follow-up context.
- The official hosted service is not open source and is not redistributed.
  Endpoint discovery, OAuth metadata, unauthenticated protocol behavior, DCR,
  and the published tool catalog were verified without a Calendly account.
  Authenticated tools/list and account-data operations were not run.
- Calendly currently assigns both read and write MCP scopes. The included
  skill requires exact target review and explicit confirmation for every
  booking, cancellation, schedule change, event-type change, no-show change,
  scheduling-link creation, and organization invitation change.
- Direct booking requires an eligible paid plan, and routing-form tools
  require a Teams plan or higher. Other behavior remains subject to account
  role, connected calendars, ownership, permissions, limits, and service
  changes.
- A generic calendar icon is used because no licensed catalog artwork is
  included in a public official MCP source repository.

The MIT license in this package applies only to the Ghast-authored adapter.
Calendly accounts, subscriptions, hosted service behavior, scheduling data,
permissions, trademarks, and terms remain controlled by Calendly.
