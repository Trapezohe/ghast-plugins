---
name: steam-search
description: Use this skill when the user asks to search Steam for games, look up a specific game's price/release-date/genres/reviews, or browse what's currently selling on Steam. Uses Steam's public store endpoints — no API key.
version: 1.0.0
allowed-tools: [WebFetch]
---

# Steam Store Search

When the user wants to find a game on Steam ("is <game> on Steam", "how much
does <game> cost", "what genre is <game>"), use this skill.

## Endpoints

Both are undocumented but stable — used by the Steam website itself.

### Search

```
https://store.steampowered.com/api/storesearch/?term=<URL-encoded query>&l=english&cc=<COUNTRY>
```

Returns `items[]` with `id` (AppID), `name`, `price.final` (cents),
`price.currency`, `metascore`, `platforms`, `tiny_image`. Sort order is
relevance.

### App details (after you know the AppID)

```
https://store.steampowered.com/api/appdetails/?appids=<APPID>&cc=<COUNTRY>&l=english
```

Returns `<APPID>.success` (boolean) and `<APPID>.data` with full info:
`name`, `type` (game/dlc/demo), `short_description`, `developers`,
`publishers`, `platforms`, `release_date.date` & `coming_soon`,
`price_overview` (final cents, currency, discount %), `is_free`,
`genres[]`, `categories[]`, `metacritic`, `header_image`.

## Country code

`cc` controls regional pricing. Default `US`; use `CN` for China store,
`JP` for Japan, etc. The user may give you a hint ("how much in CNY").

## Output

For search results:

> 1. **Hades II** — $29.99 USD · AppID 1145350 · Action / Roguelike
>    <https://store.steampowered.com/app/1145350/>
> 2. **Hades** — $24.99 USD · AppID 1145360 ...

For single-game detail: pull a 3-4 line summary covering price, release date,
developer/publisher, genres, platforms, Metacritic score (if present),
and the store URL.

## Notes

- Prices come in cents — divide by 100 to display.
- "Free to play" games have `is_free: true` and no `price_overview`.
- Unreleased games have `coming_soon: true` and `price_overview` may be
  absent. Show the release date prominently.
