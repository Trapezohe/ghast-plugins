# Binance Authentication

Credentials must be configured outside chat before an authenticated request.

## Environment variables

- `BINANCE_API_KEY`: Binance API key
- `BINANCE_SECRET_KEY`: HMAC secret, private-key path, or private-key content
- `BINANCE_API_ENV`: `prod`, `testnet`, or `demo`

The agent may reference these specific variables inside one command, but must
never print them, dump the environment, or copy them into another file.

## Existing CLI profiles

```bash
binance-cli profile list
binance-cli profile view
binance-cli profile select --name <name>
```

Use `--profile <name>` to override the active profile. Do not create or update
profiles from credentials supplied in chat. Users who need a new profile should
configure it themselves in a trusted terminal with
`binance-cli profile create -i`, then ask the agent to use the profile name.

## Security rules

- Never run `printenv`, `env`, or an unscoped `export`.
- Never read `.env`, `TOOLS.md`, or arbitrary secret files.
- Never echo or log raw credentials or private-key paths.
- Use testnet or demo for state-changing examples unless production is explicit.
- Follow the Ghast financial execution policy before every write operation.
