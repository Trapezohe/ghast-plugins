# Binance P2P Authentication

Authenticated P2P SAPI requests require HMAC SHA256 credentials already present
in `BINANCE_API_KEY` and `BINANCE_SECRET_KEY`.

## Base URL

`https://api.binance.com`

## SAPI-specific behavior

- Keep parameters in their original insertion order; do not sort them.
- Percent-encode names and values with RFC 3986 before signing.
- Add `timestamp` in Unix milliseconds and optionally `recvWindow`.
- Use the exact encoded query string for both the signature and request.

## Secure example

```bash
: "${BINANCE_API_KEY:?Set BINANCE_API_KEY outside chat}"
: "${BINANCE_SECRET_KEY:?Set BINANCE_SECRET_KEY outside chat}"

BASE_URL="https://api.binance.com"
TIMESTAMP=$(($(date +%s) * 1000))
QUERY="page=1&rows=20&recvWindow=60000&timestamp=${TIMESTAMP}"
SIGNATURE=$(printf '%s' "$QUERY" \
  | openssl dgst -sha256 -hmac "$BINANCE_SECRET_KEY" \
  | cut -d' ' -f2)

curl --silent --show-error --fail-with-body \
  "${BASE_URL}/sapi/v1/c2c/orderMatch/listUserOrderHistory?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${BINANCE_API_KEY}" \
  -H "User-Agent: ghast-binance-p2p/1.1.0"
```

Never print either variable or store it in a generated file. Use an IP
allowlist and the minimum API permissions required for the requested endpoint.
