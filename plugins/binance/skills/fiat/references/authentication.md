# Binance Fiat Authentication

Authenticated fiat SAPI requests require credentials configured outside chat.
Use `BINANCE_API_KEY` with one supported signing method:

- HMAC: `BINANCE_SECRET_KEY`
- RSA or Ed25519: `BINANCE_PRIVATE_KEY_PATH`

Never print these variables, inspect the full environment, or write them to a
workspace file.

## Signing process

1. Build the request query in its required order with a Unix-millisecond
   `timestamp` and optional `recvWindow`.
2. Percent-encode the exact names and values with RFC 3986.
3. Sign the exact encoded query with HMAC SHA256, RSA, or Ed25519.
4. Append `signature` and send `X-MBX-APIKEY`.

## HMAC example

```bash
: "${BINANCE_API_KEY:?Set BINANCE_API_KEY outside chat}"
: "${BINANCE_SECRET_KEY:?Set BINANCE_SECRET_KEY outside chat}"

BASE_URL="https://api.binance.com"
TIMESTAMP=$(($(date +%s) * 1000))
QUERY="transactionType=0&timestamp=${TIMESTAMP}"
SIGNATURE=$(printf '%s' "$QUERY" \
  | openssl dgst -sha256 -hmac "$BINANCE_SECRET_KEY" \
  | cut -d' ' -f2)

curl --silent --show-error --fail-with-body \
  "${BASE_URL}/sapi/v1/fiat/orders?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${BINANCE_API_KEY}" \
  -H "User-Agent: ghast-binance-fiat/1.1.0"
```

Use an IP allowlist and minimum permissions. Follow the Ghast financial
execution policy before any state-changing operation.
