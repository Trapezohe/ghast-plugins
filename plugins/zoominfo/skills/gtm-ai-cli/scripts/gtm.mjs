#!/usr/bin/env node
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import path from "node:path";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const cli = path.resolve(
  scriptDir,
  "../../../vendor/gtm-ai-cli/gtm.bundle.mjs",
);
const child = spawn(process.execPath, [cli, ...process.argv.slice(2)], {
  stdio: "inherit",
  env: process.env,
});
child.on("error", (error) => {
  console.error(`Unable to start ZoomInfo GTM AI CLI: ${error.message}`);
  process.exit(1);
});
for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => child.kill(signal));
}
child.on("exit", (code, signal) => {
  if (signal) process.kill(process.pid, signal);
  else process.exit(code === null ? 1 : code);
});
