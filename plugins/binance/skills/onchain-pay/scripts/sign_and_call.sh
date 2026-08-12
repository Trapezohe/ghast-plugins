#!/usr/bin/env bash
set -euo pipefail

# Binance Onchain-Pay Open API - Sign & Call
# Credentials are read from the environment so they do not appear in process args.
# Usage: sign_and_call.sh <api_path> [json_body]

: "${BINANCE_ONCHAIN_PAY_BASE_URL:?Set BINANCE_ONCHAIN_PAY_BASE_URL}"
: "${BINANCE_ONCHAIN_PAY_CLIENT_ID:?Set BINANCE_ONCHAIN_PAY_CLIENT_ID}"
: "${BINANCE_ONCHAIN_PAY_API_KEY:?Set BINANCE_ONCHAIN_PAY_API_KEY}"
: "${BINANCE_ONCHAIN_PAY_PEM_PATH:?Set BINANCE_ONCHAIN_PAY_PEM_PATH}"

API_PATH="${1:?API path is required}"
JSON_BODY="${2:-}"
timestamp=$(($(date +%s) * 1000))
payload="${JSON_BODY}${timestamp}"

signature=$(printf '%s' "$payload" \
  | openssl dgst -sha256 -sign "$BINANCE_ONCHAIN_PAY_PEM_PATH" \
  | openssl enc -base64 -A)

curl_args=(
  --silent
  --show-error
  --fail-with-body
  --location
  --request POST "${BINANCE_ONCHAIN_PAY_BASE_URL%/}/${API_PATH#/}"
  --header "X-Tesla-ClientId: ${BINANCE_ONCHAIN_PAY_CLIENT_ID}"
  --header "X-Tesla-SignAccessToken: ${BINANCE_ONCHAIN_PAY_API_KEY}"
  --header "X-Tesla-Signature: ${signature}"
  --header "X-Tesla-Timestamp: ${timestamp}"
  --header "Content-Type: application/json"
  --header "x-trace-id: ghast_skill_${timestamp}"
  --header "User-Agent: ghast-binance-onchain-pay/0.1.2"
)

if [ -n "$JSON_BODY" ]; then
  curl_args+=(--data-raw "$JSON_BODY")
fi

response=$(curl "${curl_args[@]}")
printf '%s' "$response" | python3 -m json.tool 2>/dev/null || printf '%s\n' "$response"
