// current-datetime — gives the model an authoritative "what time is it"
// answer. Pure JS, no network, no permissions beyond tools:register.
//
// Inspired by lobe-chat-plugins' `current-datetime-assistant` and
// `clock-time`, but rewritten as a native Ghast plugin: instead of
// pointing at a remote OpenAPI service it runs entirely inside the
// host's main process.

export function activate(context) {
  const handle = context.tools.register("get_current_datetime", {
    description:
      "Return the current date and time, optionally in a specific IANA timezone " +
      "(e.g. \"Asia/Shanghai\", \"America/Los_Angeles\", \"UTC\"). Defaults to the " +
      "user's system timezone. Use this whenever you need to know what \"now\" is " +
      "before answering a time-sensitive question.",
    parameters: {
      type: "object",
      properties: {
        timezone: {
          type: "string",
          description:
            "IANA timezone name. Optional. Omit to use the user's system timezone.",
        },
      },
    },
    execute: async (args = {}) => {
      const { timezone } = args ?? {};
      const now = new Date();
      const tz =
        timezone || Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";

      let formatted;
      let weekday;
      try {
        formatted = new Intl.DateTimeFormat("en-CA", {
          timeZone: tz,
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: false,
          timeZoneName: "short",
        }).format(now);
        weekday = new Intl.DateTimeFormat("en", {
          timeZone: tz,
          weekday: "long",
        }).format(now);
      } catch (err) {
        throw new Error(
          `Unknown timezone "${tz}". Use a valid IANA name like "Asia/Shanghai" or "UTC". (${err.message})`,
        );
      }

      return {
        iso: now.toISOString(),
        unix: Math.floor(now.getTime() / 1000),
        timezone: tz,
        weekday,
        formatted,
      };
    },
  });

  return {
    dispose: () => handle.dispose(),
  };
}
