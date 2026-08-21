---
name: mixpanel-headless:auth
description: Manage Mixpanel authentication, accounts, projects, workspaces, targets, and bridge status through the official mp CLI.
argument-hint: [session|login|account|project|workspace|target|bridge] [...]
---

# Mixpanel Authentication Management

Use the official `mp` CLI installed by `mixpanel-headless`. Parse
`$ARGUMENTS`, run the matching command below, and present the result
conversationally. Never invent an account, project, workspace, or target ID.

## Security rules

- Never ask for passwords, API secrets, or bearer tokens in conversation.
- Never pass a secret as a CLI argument.
- Prefer `mp login` for interactive OAuth.
- For service accounts, instruct the user to run `mp account add` themselves;
  it prompts with hidden input or accepts `--secret-stdin`.
- Use environment variables for non-interactive credentials.

## Routing

With no arguments or `session`, run:

```bash
mp session --format json
```

For `login`, tell the user the browser flow may open, then run:

```bash
mp login
```

Useful login flags are `--name`, `--region us|eu|in`, `--project`,
`--service-account`, `--token-env`, `--secret-stdin`, and `--no-browser`.

### Accounts

```bash
mp account list --format json
mp account show <NAME>
mp account use <NAME>
mp account test <NAME>
mp account login <NAME>
mp account logout <NAME>
```

For account creation, guide the user to one of these official flows:

```bash
mp login --name <NAME> --region <REGION>
mp account add <NAME> --type service_account --username <USERNAME> --project <PROJECT_ID> --region <REGION>
mp account add <NAME> --type oauth_token --token-env <ENV_VAR> --project <PROJECT_ID> --region <REGION>
```

Do not run `account add` on the user's behalf when it would require handling a
secret. After the user completes it, verify with `mp account test <NAME>`.

### Projects

```bash
mp project list --format json
mp project show
mp project use <PROJECT_ID>
```

If `project use` has no ID, list projects first and ask the user to choose.

### Workspaces

```bash
mp workspace list --format json
mp workspace show
mp workspace use <WORKSPACE_ID>
```

If `workspace use` has no ID, list workspaces first and ask the user to choose.

### Targets

```bash
mp target list --format json
mp target show <NAME> --format json
mp target add <NAME> --account <ACCOUNT> --project <PROJECT_ID> [--workspace <WORKSPACE_ID>]
mp target use <NAME>
```

Before adding a target, collect its name, account, project, and optional
workspace. These are identifiers, not secrets.

### Bridge

For bridge status, run:

```bash
mp session --bridge --format json
```

To create a bridge at an explicit path, guide the user to:

```bash
mp account export-bridge [<ACCOUNT>] --to <PATH> [--project <PROJECT_ID>] [--workspace <WORKSPACE_ID>]
```

## Non-interactive authentication

Supported environment combinations include:

```text
MP_USERNAME + MP_SECRET + MP_PROJECT_ID + MP_REGION
MP_OAUTH_TOKEN + MP_PROJECT_ID + MP_REGION
```

Never print their values. When a command fails, report the CLI's concrete error
and suggest the smallest matching recovery command.
