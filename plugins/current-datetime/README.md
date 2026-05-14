# current-datetime

Slash command and skill that tells the model what time it is — kills the
"I don't actually know today's date" problem.

## What it provides

- **`/now [timezone]`** — slash command, user-invoked. Optionally pass an
  IANA timezone (e.g. `/now Asia/Shanghai`).
- **`current-datetime` skill** — model-invoked. Activates whenever a request
  needs an authoritative timestamp.

Both use the local `date` command via the `Bash` builtin; no network call.

## License

MIT
