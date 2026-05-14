---
name: realtime-weather
description: Use this skill when the user asks about current weather, temperature, conditions, or forecast for any city or place name. Provides current conditions and a 24h hourly forecast via the free Open-Meteo API — no API key, no signup required.
version: 1.0.0
allowed-tools: [WebFetch, Bash]
---

# Realtime Weather (Open-Meteo)

When the user asks "what's the weather in <place>", "is it raining in <city>",
"what's the forecast", etc., use this skill to fetch real weather data instead
of guessing.

## Two-step API call

### Step 1: Geocode the place name

Call `WebFetch` (or `curl` via `Bash`) on:

```
https://geocoding-api.open-meteo.com/v1/search?name=<URL-encoded place>&count=1&language=en&format=json
```

The response has `results[0].latitude`, `.longitude`, `.name`, `.country`,
`.admin1`. If `results` is empty, tell the user the place wasn't found.

### Step 2: Fetch current + 24h forecast

```
https://api.open-meteo.com/v1/forecast?latitude=<lat>&longitude=<lon>
  &current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m
  &hourly=temperature_2m,precipitation_probability,weather_code
  &forecast_hours=24
  &temperature_unit=celsius
  &wind_speed_unit=kmh
  &timezone=auto
```

(Use `temperature_unit=fahrenheit` & `wind_speed_unit=mph` if the user is in
the US or asked for imperial units.)

## Decoding `weather_code` (WMO)

| Code | Condition |
| --- | --- |
| 0 | Clear sky |
| 1-3 | Mainly clear → overcast |
| 45, 48 | Fog |
| 51-57 | Drizzle |
| 61-67 | Rain |
| 71-77 | Snow |
| 80-82 | Rain showers |
| 85-86 | Snow showers |
| 95-99 | Thunderstorm |

## Output

Short, useful summary. Example:

> **Shanghai, CN (now):** 24 °C (feels 26), partly cloudy, humidity 68%, wind
> 12 km/h SE.
>
> **Next 12h:** rain starting ~18:00, low ~21 °C overnight.
>
> _Source: Open-Meteo (open-meteo.com)._

Always cite Open-Meteo per their attribution requirement.
