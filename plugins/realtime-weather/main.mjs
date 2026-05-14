// realtime-weather — geocode a place name with Open-Meteo's free
// geocoding API, then pull current + 24h hourly forecast from their
// free forecast endpoint. No API key needed.
//
// Inspired by lobe-chat-plugins' `realtime-weather` and `WeatherGPT`,
// but uses Open-Meteo so users don't have to register anywhere.

const GEOCODE_BASE = "https://geocoding-api.open-meteo.com/v1/search";
const FORECAST_BASE = "https://api.open-meteo.com/v1/forecast";

// Open-Meteo WMO weather code → human label
// https://open-meteo.com/en/docs#api_form
const WMO_LABELS = {
  0: "Clear sky",
  1: "Mainly clear",
  2: "Partly cloudy",
  3: "Overcast",
  45: "Fog",
  48: "Depositing rime fog",
  51: "Light drizzle",
  53: "Moderate drizzle",
  55: "Dense drizzle",
  56: "Light freezing drizzle",
  57: "Dense freezing drizzle",
  61: "Slight rain",
  63: "Moderate rain",
  65: "Heavy rain",
  66: "Light freezing rain",
  67: "Heavy freezing rain",
  71: "Slight snow",
  73: "Moderate snow",
  75: "Heavy snow",
  77: "Snow grains",
  80: "Slight rain showers",
  81: "Moderate rain showers",
  82: "Violent rain showers",
  85: "Slight snow showers",
  86: "Heavy snow showers",
  95: "Thunderstorm",
  96: "Thunderstorm with slight hail",
  99: "Thunderstorm with heavy hail",
};

export function activate(context) {
  const handle = context.tools.register("get_weather", {
    description:
      "Look up a place name and return current weather (temperature, " +
      "humidity, wind, condition) plus a 24h hourly forecast. Powered by " +
      "Open-Meteo — no API key required. Use this when the user asks about " +
      "weather, temperature, or forecast in any city.",
    parameters: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "City or place name, e.g. `Shanghai`, `San Francisco, CA`.",
        },
        units: {
          type: "string",
          enum: ["metric", "imperial"],
          default: "metric",
          description:
            "`metric` returns °C and km/h; `imperial` returns °F and mph.",
        },
      },
      required: ["location"],
    },
    execute: async (args = {}) => {
      const { location, units = "metric" } = args ?? {};
      if (typeof location !== "string" || !location.trim()) {
        throw new Error("`location` is required.");
      }

      const geocode = await fetchJson(
        `${GEOCODE_BASE}?name=${encodeURIComponent(location)}&count=1&language=en&format=json`,
      );
      const place = geocode?.results?.[0];
      if (!place) {
        throw new Error(`No location found for "${location}".`);
      }

      const tempUnit = units === "imperial" ? "fahrenheit" : "celsius";
      const windUnit = units === "imperial" ? "mph" : "kmh";
      const forecast = await fetchJson(
        `${FORECAST_BASE}?latitude=${place.latitude}&longitude=${place.longitude}` +
          `&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m` +
          `&hourly=temperature_2m,precipitation_probability,weather_code` +
          `&temperature_unit=${tempUnit}&wind_speed_unit=${windUnit}` +
          `&forecast_hours=24&timezone=auto`,
      );

      const current = forecast.current ?? {};
      const hourly = forecast.hourly ?? {};
      const upcoming = (hourly.time ?? []).slice(0, 24).map((t, i) => ({
        time: t,
        temperature: hourly.temperature_2m?.[i],
        precipProbability: hourly.precipitation_probability?.[i] ?? null,
        condition: WMO_LABELS[hourly.weather_code?.[i]] ?? "Unknown",
      }));

      return {
        location: {
          name: place.name,
          country: place.country,
          admin1: place.admin1,
          latitude: place.latitude,
          longitude: place.longitude,
          timezone: forecast.timezone,
        },
        current: {
          time: current.time,
          temperature: current.temperature_2m,
          feelsLike: current.apparent_temperature,
          humidity: current.relative_humidity_2m,
          windSpeed: current.wind_speed_10m,
          windDirection: current.wind_direction_10m,
          precipitation: current.precipitation,
          condition: WMO_LABELS[current.weather_code] ?? "Unknown",
          isDay: current.is_day === 1,
        },
        units: {
          temperature: tempUnit === "fahrenheit" ? "°F" : "°C",
          wind: windUnit,
        },
        forecast: upcoming,
        attribution: "Weather data by Open-Meteo (open-meteo.com)",
      };
    },
  });

  return { dispose: () => handle.dispose() };
}

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      "User-Agent":
        "Trapezohe-Ghast/0.1 (+https://ghast.trapezohe.ai) realtime-weather",
    },
  });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} from ${url}`);
  }
  return response.json();
}
