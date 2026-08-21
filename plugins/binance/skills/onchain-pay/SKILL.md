---
name: onchain-pay
description: 'Binance Onchain Pay enables users to buy cryptocurrency with fiat (e.g., EUR, USD) or send existing crypto from their Binance account directly to any external on-chain wallet address in a single flow—no manual withdrawal needed.


  Enables partners to integrate crypto buying services:

  - payment-method-list: Get available payment methods (Card, P2P, Google Pay, Apple Pay, etc.) with limits for a fiat/crypto pair

  - trading-pairs: List all supported fiat currencies and cryptocurrencies

  - estimated-quote: Get real-time price quote including exchange rate, fees, and estimated crypto amount

  - pre-order: Create a buy order and get redirect URL to Binance payment flow

  - order: Query order status and details (processing, completed, failed, etc.)

  - crypto-network: Get supported blockchain networks with withdraw fees and limits

  - p2p/trading-pairs: List P2P-specific trading pairs'
license: MIT
metadata:
  version: 0.1.2
  author: onchain-pay-team
---
## Ghast financial execution policy

These rules override less restrictive confirmation examples elsewhere in this skill:

- Never ask the user to paste API secrets, private keys, seed phrases, or PEM contents into chat.
- Use environment variables or an existing local Binance CLI profile for credentials. Never place a secret directly in a command argument, log, or generated file.
- Public market-data and authenticated read-only requests may run after the user asks for them.
- Before any order, cancellation, transfer, withdrawal, conversion, subscription, redemption, loan, staking action, advertisement change, appeal mutation, payment, pre-order, or other state-changing request, show the exact environment/profile, action, asset, amount, price or slippage, destination, and known irreversible effects.
- Execute a state-changing request only after the user replies with the exact text `CONFIRM BINANCE`. A confirmation authorizes one displayed action and expires immediately after that action.
- Never infer production intent. Use testnet or demo for state-changing examples unless the user explicitly chooses production and then provides the required confirmation.
- Prefer quote, test, preview, or dry-run endpoints when available. After execution, query status and report whether the action is pending, filled, completed, rejected, or failed.

# Binance Onchain-Pay Open API Skill

Call Binance Onchain-Pay Open API endpoints with automatic RSA SHA256 request signing.

## Use Cases & Scenarios

This skill is designed for the following scenarios:

### 1. 💳 Fiat-to-Crypto Purchase & Send
**When to use**: User wants to buy crypto with fiat currency and send directly to an external on-chain wallet address
- Buy USDT with USD/EUR/TWD using credit card → Send to MetaMask address on BSC
- Purchase BTC with Google Pay → Transfer to hardware wallet
- Buy USDC with P2P → Send to DeFi protocol contract address

**Key APIs**: `trading-pairs` → `payment-method-list` → `estimated-quote` → `pre-order`

### 2. 🔄 Direct Crypto Transfer (Send Primary)
**When to use**: User has crypto in Binance account and wants to send to external address
- Send existing USDT from Binance Spot to friend's wallet address
- Transfer ETH to Uniswap contract for trading
- Move crypto from Binance to self-custodial wallet (Trust Wallet, Ledger, etc.)

**Key APIs**: `pre-order` with `SEND_PRIMARY` customization

### 3. 🔗 Cross-Chain Bridge Operations
**When to use**: User needs to buy crypto on one chain and transfer to another network
- Buy USDC on Ethereum → Bridge to Polygon for lower fees
- Purchase tokens on BSC → Transfer to Base network
- Fiat to crypto on Solana → Send to Arbitrum for DeFi

**Key APIs**: `crypto-network` → `pre-order` with network selection

### 4. 🏪 Merchant Payment Integration
**When to use**: Integrate crypto payment gateway for e-commerce or services
- Accept fiat payments and auto-convert to crypto
- Enable "Pay with Crypto" checkout flow
- Process subscription payments with crypto

**Key APIs**: `pre-order` with `externalOrderId` tracking

### 5. 🤖 Smart Contract Interaction (Onchain-Pay Easy)
**When to use**: Buy crypto and execute smart contract in one transaction
- Buy USDT and deposit to lending protocol
- Purchase tokens and stake in DeFi pool
- Fiat on-ramp directly to GameFi or NFT marketplace

**Key APIs**: `pre-order` with `ON_CHAIN_PROXY_MODE` customization

### 6. 📊 Query & Monitoring
**When to use**: Check order status, available networks, or payment methods
- Monitor order processing status (pending, completed, failed)
- List supported fiat currencies and cryptocurrencies
- Check available payment methods for specific country/amount
- Verify network fees and limits

**Key APIs**: `order`, `crypto-network`, `trading-pairs`, `payment-method-list`

---

## Quick Reference

| Endpoint | API Path | Required Params | Optional Params |
|----------|----------|-----------------|-----------------|
| Payment Method List (v1) | `papi/v1/ramp/connect/buy/payment-method-list` | fiatCurrency, cryptoCurrency, totalAmount, amountType | network, contractAddress |
| Payment Method List (v2) | `papi/v2/ramp/connect/buy/payment-method-list` | (none) | lang |
| Trading Pairs | `papi/v1/ramp/connect/buy/trading-pairs` | (none) | (none) |
| Estimated Quote | `papi/v1/ramp/connect/buy/estimated-quote` | fiatCurrency, requestedAmount, payMethodCode, amountType | cryptoCurrency, contractAddress, address, network |
| Pre-order | `papi/v1/ramp/connect/buy/pre-order` | externalOrderId, merchantCode, merchantName, ts | fiatCurrency, fiatAmount, cryptoCurrency, requestedAmount, amountType, address, network, payMethodCode, payMethodSubCode, redirectUrl, failRedirectUrl, redirectDeepLink, failRedirectDeepLink, customization, destContractAddress, destContractABI, destContractParams, affiliateCode, gtrTemplateCode, contractAddress |
| Get Order | `papi/v1/ramp/connect/order` | externalOrderId | (none) |
| Crypto Network | `papi/v1/ramp/connect/crypto-network` | (none) | (none) |
| P2P Trading Pairs | `papi/v1/ramp/connect/buy/p2p/trading-pairs` | (none) | fiatCurrency |

---

## How to Execute a Request

### Step 1: Gather credentials

Credentials must already be configured outside chat:

- `BINANCE_ONCHAIN_PAY_BASE_URL`: API base URL
- `BINANCE_ONCHAIN_PAY_CLIENT_ID`: Client identifier
- `BINANCE_ONCHAIN_PAY_API_KEY`: Sign access token
- `BINANCE_ONCHAIN_PAY_PEM_PATH`: Absolute path to the RSA private key PEM file

Do not create or read `.local.md`, and do not place these values in command arguments.

### Step 2: Build the JSON body

Build a compact JSON body from user-specified parameters. Remove any parameters the user did not provide.

**IMPORTANT: Address and Network Validation**
- `address` (destination wallet address) and `network` (blockchain network) are REQUIRED for all pre-order requests
- Require the user to provide `address` and `network` for the displayed operation summary
- Never load a default destination from a credential file

### Step 3: Sign and call using the bundled script

```bash
bash <skill_path>/scripts/sign_and_call.sh \
  "<API_PATH>" \
  '<JSON_BODY>'
```

### Step 4: Return results

Display the JSON response to the user in a readable format.

---

## Authentication

See [`references/authentication.md`](./references/authentication.md) for full signing details.

Summary:
1. Payload = `JSON_BODY` + `TIMESTAMP` (milliseconds)
2. Sign payload with RSA SHA256 using PEM private key
3. Base64 encode the signature (single line)
4. Send as POST with headers: `X-Tesla-ClientId`, `X-Tesla-SignAccessToken`, `X-Tesla-Signature`, `X-Tesla-Timestamp`, `Content-Type: application/json`

---

## Parameters Reference

### Payment Method List v1 (`buy/payment-method-list`)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| fiatCurrency | string | Yes | Fiat currency code (e.g., `USD`, `EUR`, `BRL`, `UGX`) |
| cryptoCurrency | string | Yes | Crypto currency code (e.g., `BTC`, `USDT`, `USDC`, `SEI`) |
| totalAmount | number | Yes | Amount value |
| amountType | number | Yes | `1` = fiat amount, `2` = crypto amount |
| network | string | No | Blockchain network (e.g., `BSC`, `ETH`, `SOL`, `BASE`, `SEI`) |
| contractAddress | string | No | Token contract address (required for non-native tokens) |

### Payment Method List v2 (`v2/buy/payment-method-list`)

Get all available payment methods without specifying fiat/crypto parameters. Simplified version of v1.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| lang | string | No | Language code for localized payment method names (e.g., `en`, `cn`, `es`) |

**Differences from v1**:
- **Simpler**: No need to specify fiatCurrency, cryptoCurrency, or amount
- **Comprehensive**: Returns all available payment methods for the merchant
- **Use case**: Useful for displaying all options before user input

**Response Format**: Same as v1, returns list of payment methods with their limits and properties.

### Estimated Quote (`buy/estimated-quote`)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| fiatCurrency | string | Yes | Fiat currency code |
| cryptoCurrency | string | No | Crypto currency code (optional if contractAddress provided) |
| requestedAmount | number | Yes | Amount value |
| payMethodCode | string | Yes | Payment method (e.g., `BUY_CARD`, `BUY_GOOGLE_PAY`, `BUY_P2P`, `BUY_WALLET`) |
| amountType | number | Yes | `1` = fiat amount, `2` = crypto amount |
| network | string | **Yes*** | Blockchain network selected by the user |
| contractAddress | string | No | Token contract address |
| address | string | **Yes*** | Destination wallet address for receiving crypto |

\* Required by Ghast policy: ask the user when either value is missing.

### Pre-order (`buy/pre-order`)

Create a buy pre-order and return the redirect link for payment.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| externalOrderId | string | Yes | Partner's unique order ID (must be unique) |
| merchantCode | string | Yes | Merchant code assigned to you by Binance (provided by user) |
| merchantName | string | Yes | Merchant display name (provided by user) |
| ts | number | Yes | Current timestamp in milliseconds |
| fiatCurrency | string | No* | Fiat currency code (e.g., `TWD`, `USD`, `EUR`) |
| fiatAmount | number | No* | Fiat amount to spend |
| cryptoCurrency | string | No* | Crypto currency to buy (e.g., `USDT`, `BTC`, `ETH`) |
| requestedAmount | number | No* | Amount value (fiat or crypto based on amountType) |
| amountType | number | No* | `1` = fiat amount, `2` = crypto amount |
| address | string | No | Destination wallet address for receiving crypto |
| network | string | No | Blockchain network (e.g., `BSC`, `ETH`, `SOL`) |
| payMethodCode | string | No | Payment method code (e.g., `BUY_CARD`, `BUY_P2P`, `BUY_GOOGLE_PAY`, `BUY_APPLE_PAY`, `BUY_PAYPAL`, `BUY_WALLET`, `BUY_REVOLUT`) |
| payMethodSubCode | string | No | Payment method sub-code (e.g., `card`, `GOOGLE_PAY`, `WECHAT`) |
| redirectUrl | string | No | Success redirect URL |
| failRedirectUrl | string | No | Failure redirect URL |
| redirectDeepLink | string | No | Deep link for success (mobile apps) |
| failRedirectDeepLink | string | No | Deep link for failure (mobile apps) |
| customization | object | No | Custom configuration object (see Customization section below) |
| destContractAddress | string | No | Destination contract address (for Onchain-Pay Easy mode) |
| destContractABI | string | No | Contract ABI name (for Onchain-Pay Easy mode) |
| destContractParams | object | No | Contract parameters (for Onchain-Pay Easy mode) |
| affiliateCode | string | No | Affiliate code for commission tracking |
| gtrTemplateCode | string | No | GTR template code (e.g., `OTHERS`) |
| contractAddress | string | No | Token contract address (for non-native tokens) |

\* Either `fiatAmount` or (`requestedAmount` + `amountType`) should be provided. If `fiatCurrency` is not provided, the system will auto-select available fiat currencies.

**Response Example**:
```json
{
  "code": "000000",
  "message": "success",
  "data": {
    "link": "https://app.binance.com/uni-qr/ccnt?...",
    "linkExpireTime": 1772852565045
  },
  "success": true
}
```

### Get Order (`order`)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| externalOrderId | string | Yes | The external order ID to query |

---

## Customization Options

The `customization` field in pre-order API accepts various flags to customize the buy flow behavior. Each merchant must have the corresponding permission configured in `db.merchant_info` table.

### Available Customization Flags

| Flag | Code | Type | Availability | Description | Use Case |
|------|------|------|--------------|-------------|----------|
| `LOCK_ORDER_ATTRIBUTES` | 1 | array | Open API ✓ | Lock specific order attributes so users cannot modify them. Values: `1`=fiat currency, `2`=crypto currency, `3`=amount, `4`=payment method, `5`=network, `6`=address, `7`=fiat amount, `8`=crypto amount | Fixed-parameter orders |
| `SKIP_CASHIER` | 2 | boolean | Open API ✓ | Skip the cashier page and proceed directly to payment. Reduces user friction in the checkout flow. | Streamlined payment experience |
| `AUTO_REDIRECTION` | 3 | boolean | Open API ✓ | Automatically redirect to `redirectUrl` after order completion without showing success page. | Seamless user experience |
| `HIDE_SEND` | 6 | boolean | Open API ✓ | Hide the "Send" tab in the UI. Useful when only buy flow is needed. | Buy-only integration |
| `SEND_PRIMARY` | 7 | boolean | Open API ✓ | Enable Send Crypto feature. If user's Binance balance is insufficient, auto-trigger buy flow first. | Send crypto to external address |
| `MERCHANT_DISPLAY_NAME` | 8 | string | Open API ✓ | Override the display name shown to users in the UI. | Custom branding |
| `NET_RECEIVE` | 9 | boolean | Open API ✓ | User receives net amount after deducting all fees. Total cost is more transparent. | Better UX for showing final received amount |
| `P2P_EXPRESS` | 10 | boolean | Open API ✓ | Enable P2P Express mode for faster P2P order matching. | Quick P2P transactions |
| `OPEN_NETWORK` | 11 | boolean | Web3 only | Allow users to select different networks. Default is locked to pre-selected network. **Note**: Currently only available for Web3 entrance, not available for Open API. | Multi-network support (Web3 only) |
| `ON_CHAIN_PROXY_MODE` | 12 | boolean | Open API ✓ | Enable Onchain-Pay Easy mode. After buying crypto, Onchain-Pay will execute smart contract interaction instead of direct withdrawal to user wallet. Requires `destContractAddress`, `destContractABI`, and `destContractParams`. | Fiat to Smart Contract integration |
| `SEND_PRIMARY_FLEXIBLE` | 13 | boolean | Open API ✓ | Flexible Send Primary mode with more options. | Advanced send crypto scenarios |

### Customization Examples

**Example 1: Basic Card Payment**
```json
{
  "customization": {}
}
```

**Example 2: Onchain-Pay Easy (On-Chain Proxy)**
```json
{
  "customization": {
    "ON_CHAIN_PROXY_MODE": true,
    "NET_RECEIVE": true,
    "SEND_PRIMARY": true
  },
  "destContractAddress": "0x128...974",
  "destContractABI": "depositFor",
  "destContractParams": {
    "accountType": 2
  }
}
```

**Example 3: Send Crypto**
```json
{
  "customization": {
    "SEND_PRIMARY_FLEXIBLE": true,
    "SEND_PRIMARY": true
  }
}
```

**Example 4: P2P with Auto Redirection**
```json
{
  "customization": {
    "AUTO_REDIRECTION": true,
    "P2P_EXPRESS": true
  }
}
```

**Example 5: Lock Order Attributes**
```json
{
  "customization": {
    "LOCK_ORDER_ATTRIBUTES": [2, 3, 6, 7, 8],
    "MERCHANT_DISPLAY_NAME": "My Custom Brand"
  }
}
```
Lock attribute codes:
- `2` = Crypto currency
- `3` = Amount
- `6` = Address
- `7` = Fiat amount
- `8` = Crypto amount

**Example 6: Net Receive Mode**
```json
{
  "customization": {
    "NET_RECEIVE": true,
    "SEND_PRIMARY": true
  }
}
```

**Example 7: Hide Send Tab**
```json
{
  "customization": {
    "HIDE_SEND": true
  }
}
```

**Example 8: Skip Cashier (Direct Payment)**
```json
{
  "customization": {
    "SKIP_CASHIER": true
  }
}
```

### Important Notes

1. **Permission Required**: Each customization flag requires merchant permission. Check with admin if a flag is not working.
2. **Onchain-Pay Easy**: Only supported on BSC network currently. Requires contract integration.
3. **Validation**: Invalid customization values (e.g., `null` for `MERCHANT_DISPLAY_NAME`) will return `ILLEGAL_CUSTOMIZATION_VALUE` error.
4. **Combinations**: Some flags work together (e.g., `NET_RECEIVE` + `SEND_PRIMARY`), while others are independent.
5. **Testing**: Use a dedicated test merchant account (provided by Binance) to verify customization flags before production.
6. **Internal Flags**: `OPERATION` (code 4) and `SKIP_WITHDRAW` (code 5) are internal use only and should NOT be passed from merchant side.
7. **OPEN_NETWORK**: Currently only available for Web3 entrance, not available for Open API. Do not use this flag in Open API pre-order requests.
8. **Flag Order**: Flags are ordered by their internal code (1-13). The code number is used internally for identification.

---

## Security

- Read credentials only from `BINANCE_ONCHAIN_PAY_BASE_URL`,
  `BINANCE_ONCHAIN_PAY_CLIENT_ID`, `BINANCE_ONCHAIN_PAY_API_KEY`, and
  `BINANCE_ONCHAIN_PAY_PEM_PATH`.
- Never read or create `.local.md`, `.env`, `TOOLS.md`, or another credential
  file.
- Never show the API key, private-key content, or private-key path.
- Never send credentials to a URL other than
  `BINANCE_ONCHAIN_PAY_BASE_URL`.
- Apply the Ghast financial execution policy before `pre-order` or another
  state-changing request.

## User Agent Header

Include `User-Agent` header with the following string: `onchain-pay-open-api/0.1.2 (Skill)`

---

## Agent Behavior

1. If the user asks to call an Onchain-Pay API endpoint, identify which endpoint from the Quick Reference table
2. Ask for any missing required parameters
3. Verify the required environment variables exist; never ask for their values
4. Execute the request using the bundled `scripts/sign_and_call.sh`
5. Display the response in a readable format
6. If the request fails, show the error and suggest fixes

---

## Important Notes for Pre-order API

### Timestamp Generation (Cross-platform)

When generating timestamps for the `ts` parameter and `externalOrderId`, use the following approach for cross-platform compatibility:

```bash
# Generate millisecond timestamp (works on macOS, Linux, BSD)
TIMESTAMP=$(($(date +%s) * 1000))

# Generate unique order ID
ORDER_ID="order$(date +%s)"
```

**DO NOT USE** `date +%s%3N` or `date +%s000` as these are not portable:
- `date +%s%3N` doesn't work on macOS (outputs literal 'N')
- `date +%s000` just appends '000' without actual millisecond precision

### Order ID Format

The `externalOrderId` must be a valid string without special characters. Recommended formats:
- `order1773744500` (simple numeric suffix)
- `order_1773744500` (with underscore separator)
- `txn-abc123` (custom prefix with alphanumeric)

**Avoid**: `order_${TIMESTAMP}` where TIMESTAMP contains shell variable syntax errors

### Example Pre-order Request

After displaying the complete operation summary and receiving the exact reply
`CONFIRM BINANCE`:

```bash
TIMESTAMP=$(($(date +%s) * 1000))
ORDER_ID="order$(date +%s)"

bash /path/to/scripts/sign_and_call.sh   "papi/v1/ramp/connect/buy/pre-order"   "{\"externalOrderId\":\"$ORDER_ID\",\"merchantCode\":\"<MERCHANT_CODE>\",\"merchantName\":\"<MERCHANT_NAME>\",\"ts\":$TIMESTAMP,\"fiatCurrency\":\"USD\",\"requestedAmount\":100,\"cryptoCurrency\":\"BNB\",\"amountType\":1,\"address\":\"0x...\",\"network\":\"BSC\",\"payMethodCode\":\"BUY_CARD\"}"
```
