#!/usr/bin/env node

import {
  chmodSync,
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  renameSync,
  rmSync,
} from "node:fs";
import { createHash } from "node:crypto";
import { homedir } from "node:os";
import { dirname, isAbsolute, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawn, spawnSync } from "node:child_process";

const pluginRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const sourceFiles = {
  "go.mod": "f9bd7e4e71c698035dff2e8083bc87589b04b311368d8b419f2e76719c949b87",
  "go.sum": "9963007111c3f94736197b97d172d66ae2e53cb2bdf166c740a6944ceb42d97d",
  "cmd/razorpay-readonly/main.go":
    "d1d67f17cf3b81946967c80c3563db9369c16c63bc3978be73dcddb8e0d59c12",
};
const sourceRevision = "7950d51d118ca164c32b7cf0cfaa14f34f24849f";

function fail(message) {
  console.error(`razorpay: ${message}`);
  process.exit(1);
}

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function verifyDirectory(path, label, privateDirectory = false) {
  const stat = lstatSync(path);
  if (!stat.isDirectory() || stat.isSymbolicLink()) {
    fail(`${label} must be a real directory`);
  }
  if ((stat.mode & 0o022) !== 0) {
    fail(`${label} must not be group- or world-writable`);
  }
  if (privateDirectory && (stat.mode & 0o077) !== 0) {
    chmodSync(path, 0o700);
  }
}

function verifyRegularPrivateSource(relative, expected) {
  const path = join(pluginRoot, relative);
  const stat = lstatSync(path);
  if (!stat.isFile() || stat.isSymbolicLink()) {
    fail(`${relative} must be a regular file`);
  }
  if ((stat.mode & 0o022) !== 0) {
    fail(`${relative} must not be group- or world-writable`);
  }
  if (sha256(path) !== expected) {
    fail(`${relative} differs from the audited adapter source`);
  }
}

verifyDirectory(pluginRoot, "plugin root");
verifyDirectory(join(pluginRoot, "cmd"), "adapter source directory");
verifyDirectory(
  join(pluginRoot, "cmd", "razorpay-readonly"),
  "adapter command directory",
);
for (const [relative, expected] of Object.entries(sourceFiles)) {
  verifyRegularPrivateSource(relative, expected);
}

for (const name of ["RAZORPAY_KEY_ID", "RAZORPAY_KEY_SECRET"]) {
  const value = process.env[name];
  if (!value) {
    fail(`set ${name} outside chat before starting`);
  }
  if (/[\u0000-\u001f\u007f]/u.test(value)) {
    fail(`${name} contains a control character`);
  }
}

let goBinary = process.env.RAZORPAY_GO_BINARY || "go";
if (process.env.RAZORPAY_GO_BINARY && !isAbsolute(goBinary)) {
  fail("RAZORPAY_GO_BINARY must be an absolute path");
}
const buildEnv = { ...process.env };
delete buildEnv.RAZORPAY_KEY_ID;
delete buildEnv.RAZORPAY_KEY_SECRET;
Object.assign(buildEnv, {
  CGO_ENABLED: "0",
  GONOPROXY: "",
  GONOSUMDB: "",
  GOPRIVATE: "",
  GOPROXY: "https://proxy.golang.org,direct",
  GOSUMDB: "sum.golang.org",
  GOTOOLCHAIN: "go1.24.2+auto",
  GOWORK: "off",
});
const goCheck = spawnSync(goBinary, ["version"], {
  env: buildEnv,
  encoding: "utf8",
});
if (goCheck.status !== 0) {
  fail(
    "Go is required. Install Go 1.24.2 or newer, or set " +
      "RAZORPAY_GO_BINARY to an absolute Go executable",
  );
}

const cacheBase =
  process.env.XDG_CACHE_HOME || join(homedir(), ".cache");
mkdirSync(cacheBase, { recursive: true, mode: 0o700 });
verifyDirectory(cacheBase, "cache base");
let cacheDir = cacheBase;
for (const segment of ["ghast-plugins", "razorpay", sourceRevision]) {
  cacheDir = join(cacheDir, segment);
  if (!existsSync(cacheDir)) {
    mkdirSync(cacheDir, { mode: 0o700 });
  }
  verifyDirectory(cacheDir, "Razorpay build cache", true);
}

const binary = join(cacheDir, "razorpay-readonly");
if (!existsSync(binary)) {
  const temporary = join(
    cacheDir,
    `.razorpay-readonly-${process.pid}-${Date.now()}`,
  );
  const build = spawnSync(
    goBinary,
    [
      "build",
      "-mod=readonly",
      "-trimpath",
      "-o",
      temporary,
      "./cmd/razorpay-readonly",
    ],
    {
      cwd: pluginRoot,
      env: buildEnv,
      encoding: "utf8",
      stdio: ["ignore", "ignore", "pipe"],
    },
  );
  if (build.status !== 0) {
    rmSync(temporary, { force: true });
    fail(`build failed: ${(build.stderr || "").trim()}`);
  }
  chmodSync(temporary, 0o700);
  renameSync(temporary, binary);
}

const binaryStat = lstatSync(binary);
if (!binaryStat.isFile() || binaryStat.isSymbolicLink()) {
  fail("cached Razorpay adapter must be a regular file");
}
if ((binaryStat.mode & 0o077) !== 0) {
  chmodSync(binary, 0o700);
}

const child = spawn(binary, [], {
  cwd: pluginRoot,
  env: process.env,
  stdio: "inherit",
});
for (const signal of ["SIGINT", "SIGTERM", "SIGHUP"]) {
  process.on(signal, () => child.kill(signal));
}
child.on("error", (error) => fail(`failed to start adapter: ${error.message}`));
child.on("exit", (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
  } else {
    process.exit(code ?? 1);
  }
});
