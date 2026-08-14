# razorpay

Read Razorpay payments, orders, refunds, settlements, QR codes, payment links,
payouts, reconciliation, and saved customer payment methods through
Razorpay's official MCP source and official Go SDK.

## Official source

The adapter pins `razorpay/razorpay-mcp-server` revision
`7950d51d118ca164c32b7cf0cfaa14f34f24849f` and Git tree
`feeadae4514cce8fa67651eeae22ba94ffe28dfd`. The complete official 94-file
inventory has SHA-256
`6e74ab32e2e2971fe314e3a19be0e03dc3140c7968cc88d4e02c80e1a0117669`.
The official module and `razorpay-go` SDK are locked by `go.mod` and `go.sum`.

Razorpay's current strict read-only mode excludes `fetch_tokens` because the
official tool also accepts a contact number and may create a customer. Ghast
keeps the official customer-ID behavior but exposes it through a smaller
schema that rejects `contact` and performs only GET requests.

## Tools

The plugin exposes 25 read-only tools:

- 24 unmodified tools registered from seven official Razorpay data toolsets;
- one minimal `fetch_tokens` adapter using the official SDK and requiring an
  existing `cust_...` customer ID.

Every exposed tool reports `readOnlyHint=true` and
`destructiveHint=false`. Checkout integration code generators and every
official write-classified tool are excluded.

## Authentication and runtime

Configure `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` outside chat. Never put
merchant credentials in this repository, MCP arguments, command lines, logs,
or generated files.

The local launcher requires Node.js and Go. It verifies the adapter source,
builds with Go module verification and the pinned sums in a private user cache,
removes Razorpay credentials from the build environment, and then starts the
local stdio MCP process. Set `RAZORPAY_GO_BINARY` only when an absolute Go
executable path is needed.

The first build may download the official Go 1.24.2 toolchain and locked
modules. Account permissions, API availability, pagination, rate limits,
merchant data, test/live mode, and monetary units remain controlled by
Razorpay. No authenticated merchant account was used during the repository
audit.

The generic icon is independently authored because the official source does
not publish reusable catalog artwork. See `MODIFICATIONS.md`, `LICENSE`, and
`UPSTREAM_LICENSE` for the adaptation and licensing boundary.
