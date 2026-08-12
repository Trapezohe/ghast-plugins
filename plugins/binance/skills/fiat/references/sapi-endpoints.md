---
name: fiat
description: Binance Fiat request using the Binance API. Authentication requires API key and secret key. 
metadata:
  version: 1.1.0
  author: Binance
  openclaw:
    requires:
      bins:
        - curl
        - openssl
        - date
    homepage: https://github.com/binance/binance-skills-hub/tree/main/skills/binance/fiat/SKILL.md
license: MIT
---

# Binance Fiat Skill

Fiat request on Binance using authenticated API endpoints. Requires API key and secret key for certain endpoints. Return the result in JSON format.

## Quick Reference

| Endpoint | Description | Required | Optional | Authentication |
|----------|-------------|----------|----------|----------------|
| `/sapi/v1/fiat/deposit` (POST) | Deposit(TRADE) | None | recvWindow | Yes |
| `/sapi/v2/fiat/withdraw` (POST) | Fiat Withdraw(WITHDRAW) | None | recvWindow | Yes |
| `/sapi/v1/fiat/orders` (GET) | Get Fiat Deposit/Withdraw History (USER_DATA) | transactionType | beginTime, endTime, page, rows, recvWindow | Yes |
| `/sapi/v1/fiat/payments` (GET) | Get Fiat Payments History (USER_DATA) | transactionType | beginTime, endTime, page, rows, recvWindow | Yes |
| `/sapi/v1/fiat/get-order-detail` (GET) | Get Order Detail(USER_DATA) | orderNo | recvWindow | Yes |

---

## Parameters

### Common Parameters

* **recvWindow**:  (e.g., 5000)
* **transactionType**: 0-buy,1-sell
* **beginTime**: 
* **endTime**:  (e.g., 1641782889000)
* **page**: default 1 (e.g., 1)
* **rows**: default 100, max 500 (e.g., 100)
* **orderNo**: order id retrieved from the api call of withdrawal


## Authentication

Authenticated endpoints use credentials already present in the process
environment:

- `BINANCE_API_KEY`
- `BINANCE_SECRET_KEY` for HMAC, or `BINANCE_PRIVATE_KEY_PATH` for RSA/Ed25519

Do not search for `.env`, `TOOLS.md`, inline credential files, or raw secrets.
Do not ask the user to paste credentials into chat. If the variables are
missing, stop and ask the user to configure them outside the conversation.

## Security

- Never dump the environment or print a credential.
- Never create or update a credential file.
- Send credentials only to the documented Binance API base URL.
- Use IP allowlists and minimum permissions.
- Apply the Ghast financial execution policy before any write operation.

## Signing Requests

For trading endpoints that require a signature:

1. **Detect key type first**, inspect the secret key format before signing.
2. Build query string with all parameters, including the timestamp (Unix ms).
3. Percent-encode the parameters using UTF-8 according to RFC 3986.
4. Sign query string with secretKey using HMAC SHA256, RSA, or Ed25519 (depending on the account configuration).
5. Append signature to query string.
6. Include `X-MBX-APIKEY` header.

Otherwise, do not perform steps 4–6.

## User Agent Header

Include `User-Agent` header with the following string: `binance-fiat/1.1.0 (Skill)`

See [`references/authentication.md`](./references/authentication.md) for implementation details.
