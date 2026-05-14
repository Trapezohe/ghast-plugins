---
description: Show the current date and time, optionally in a specific IANA timezone
argument-hint: "[IANA-timezone, e.g. Asia/Shanghai]"
allowed-tools: [Bash]
---

# Current Date & Time

The user invoked `/now` with arguments: $ARGUMENTS

## Instructions

1. Treat `$ARGUMENTS` (trimmed) as an optional IANA timezone name such as
   `Asia/Shanghai`, `America/Los_Angeles`, or `UTC`. If empty, omit the
   `TZ=` prefix to use the system timezone.

2. Use the `Bash` tool to run **exactly one** of these commands (don't add
   any extra flags):

   - With timezone: `TZ="<arg>" date '+%Y-%m-%d %H:%M:%S %Z (%A, week %V)'`
   - Without timezone: `date '+%Y-%m-%d %H:%M:%S %Z (%A, week %V)'`

3. Report the result as a single short line — date, time, timezone, weekday,
   ISO week number. Do not add any commentary unless the user asked for it.

4. If `date` rejects the timezone (e.g. typo'd name), report the error verbatim
   and suggest the user pass an IANA name like `Asia/Shanghai`.
