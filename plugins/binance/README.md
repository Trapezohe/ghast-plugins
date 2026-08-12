# Binance for Ghast

This plugin ports the independently MIT-licensed Binance skills from
`binance/binance-skills-hub` at `2863a186d2bbd8987fa4790d7b81a299a58364ce`.

## Included

- `binance`: Binance CLI coverage for public data and authenticated Spot,
  Futures, Options, Convert, Margin, Earn, Loans, Wallet, sub-account, staking,
  mining, gift card, rebate, and related API families.
- `fiat`: public fiat capabilities, quotes, methods, limits, and authenticated
  fiat order history.
- `p2p`: P2P market discovery plus authenticated order, appeal-evidence, and
  advertisement-management workflows.
- `onchain-pay`: signed merchant Onchain Pay discovery, quote, order, and
  pre-order workflows.

The repository's Web3 Agentic Wallet, payment-assistant, Square posting, and
other skills were not copied because this pinned snapshot does not include a
standalone license file for those directories.

## Safety

Read-only requests are available without transaction confirmation. Every
state-changing request requires a fresh operation summary and the exact reply
`CONFIRM BINANCE`; production is never inferred from an existing profile.
Credentials remain in environment variables or local Binance CLI profiles and
must not be pasted into chat.

The plugin provides procedural skills and does not bundle `binance-cli`,
credentials, an exchange account, or merchant permissions.
