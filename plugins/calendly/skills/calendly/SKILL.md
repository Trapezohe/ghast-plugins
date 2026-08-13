---
name: calendly
description: >-
  Inspect Calendly meetings, invitees, event types, schedules, busy times,
  routing forms, and organization context, or safely create and update
  scheduling resources through Calendly's official hosted MCP server.
---

# Calendly

Use the official Calendly MCP server declared by this plugin.

## Time and identity

- Resolve the authenticated Calendly user and organization before assuming
  ownership, permissions, availability, or the correct event type.
- State exact dates, local times, durations, and IANA time zones. Do not
  silently convert relative phrases such as "next Thursday" or "this week".
- Treat invitee names, email addresses, answers, meeting locations, routing
  submissions, organization membership, and calendar availability as
  sensitive. Retrieve and disclose only what the request requires.
- Distinguish free time, event-type availability, and an actual confirmed
  booking. A suggested slot is not reserved.

## Read workflows

- For upcoming or recent meetings, use an explicit time range and paginate
  deliberately. Preserve cancellation state, attendee status, and returned
  identifiers.
- For availability, resolve the intended user, event type, duration, time
  zone, and date range. Report plan, permission, or calendar-connection gaps.
- For attendee summaries, separate Calendly fields from assistant inferences.
  Do not invent company, role, relationship history, intent, or follow-up.
- Routing forms and organization invitations may expose personal or
  administrative data. Avoid broad exports and unnecessary contact details.

## Changes and confirmation

Obtain explicit confirmation immediately before any state-changing call.

- Creating or updating an event type: show its owner, name, duration,
  location, availability, and resulting public scheduling behavior.
- Updating availability: show the exact schedule, days, time ranges, time
  zone, overrides, and event types affected.
- Booking: show the event type, host, invitee name and email, exact start and
  end time, time zone, location, and any answers or tracking fields.
- Canceling: show the exact scheduled event, host, invitees, start time, and
  cancellation reason. Cancellation is destructive.
- Creating a scheduling link or share: show the source event type,
  customization, expiration or single-use behavior, and intended recipient.
- Marking or clearing no-show status: show the exact invitee and event because
  the change can affect reporting and follow-up.
- Creating or revoking an organization invitation: show the organization,
  email, role or access effect, and exact invitation.

Never turn a request to inspect, summarize, draft, or suggest into an external
change. Do not blindly retry an ambiguous write; read current state first to
avoid duplicate bookings, links, invitations, or conflicting updates.

## Service behavior

- Authentication uses Calendly OAuth Dynamic Client Registration,
  authorization code, and PKCE S256. Never ask for, display, log, or store
  OAuth tokens.
- Calendly currently assigns both `mcp:scheduling:read` and
  `mcp:scheduling:write` to MCP clients. User confirmation remains mandatory
  even when the account has permission to write.
- Direct booking requires an eligible paid plan. Routing-form tools require a
  Teams plan or higher. Other capabilities depend on the user's Calendly
  plan, role, connected calendars, ownership, and organization permissions.
- The public official catalog documents 36 tools. Inspect the authenticated
  live tool list before promising a tool, because the hosted service can
  evolve after this adapter's evidence revision.
- Report authentication, validation, conflict, rate-limit, plan, permission,
  and service errors exactly as returned.
