---
name: current-datetime
description: Use this skill whenever the user asks "what time/day/date is it", references "now"/"today"/"this week"/"tomorrow" in a way that needs a real timestamp, or asks for the current time in a specific timezone. Provides the exact wall-clock time without guessing from training data.
version: 1.0.0
---

# Current Date & Time

When the user's request requires knowing the current real-world date or time
(e.g. "what's today's date", "what time is it in Tokyo", "is the market open
right now"), use this skill instead of guessing from your training data — your
training cutoff is months behind real time.

## How to use

Run the `Bash` tool with `date` to get the authoritative current time. Two
common patterns:

- System timezone:
  ```bash
  date '+%Y-%m-%d %H:%M:%S %Z (%A)'
  ```
- Specific IANA timezone:
  ```bash
  TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M:%S %Z (%A)'
  ```

For Unix-epoch math, also run:
```bash
date +%s
```

## Presentation

State the time briefly. Never report seconds-precision unless the user asked
for it; "2026-05-14 15:32 CST (Thursday)" is enough. If the user asked a
relative question ("how long until next Friday"), do the math yourself from
the `date` output — don't make up a number.
