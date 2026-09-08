---
name: android-emulator-qa
description: Validate Android app flows with official Android SDK tools, including emulator selection, launch, UI inspection, screenshots, input and scoped diagnostic logs.
---

# Android testing in Ghast

Use the project's existing Android build tooling and the official SDK's `adb`.
This is a local CLI workflow, not a hosted MCP service. Follow any active host
restrictions on computer interaction; do not use adb to bypass those restrictions.

## Establish the target

Check `adb version` and `adb devices -l`. Select the user-authorized emulator
serial explicitly with `adb -s SERIAL` for every device operation. An offline or
unauthorized device is not usable; do not bypass device consent or connect to
another device just because it is reachable. If no emulator is available, report
that fact. Do not wipe, reset or silently start a different device.

Read the repository's build instructions and identify the requested variant,
application ID and existing Gradle task. Build/install only the requested test
application. For an already supplied APK, `adb -s SERIAL install -r APK` replaces
that app while retaining data; do not downgrade, uninstall, clear data or install
unrelated packages without explicit scope.

Resolve the launch component with
`adb -s SERIAL shell cmd package resolve-activity --brief PACKAGE` and use the
returned component with `adb -s SERIAL shell am start -n COMPONENT`. A successful
launch command does not prove that the intended screen rendered.

## Observe and exercise

Capture a fresh screenshot with
`adb -s SERIAL exec-out screencap -p > LOCAL_SCREENSHOT.png` and inspect it using
the available image viewer. Use a task-specific output path.

For semantic inspection, dump the UI hierarchy to a task-specific device path
with `adb -s SERIAL shell uiautomator dump DEVICE_XML_PATH`, then pull that file
with `adb -s SERIAL pull DEVICE_XML_PATH LOCAL_XML_PATH`. Read node text,
content descriptions, resource IDs, visibility/state and bounds. Canvas or
WebView content can be absent from the hierarchy; do not equate missing nodes
with an empty screen. Use fresh visual evidence when semantic data is incomplete.

Resolve a unique visible target before each action. For bounds
`[left,top][right,bottom]`, the center is `((left+right)/2,(top+bottom)/2)`.
Do not reuse coordinates after navigation, scrolling or rotation. Use
`adb -s SERIAL shell input tap X Y`, bounded swipes, or a relevant key event
only for actions covered by the test. Capture new evidence after each step.
Text input must contain test data, not credentials or personal information.
For duplicate labels, use the surrounding UI and resource ID to disambiguate.

## Diagnostics and results

Resolve the app process with `adb -s SERIAL shell pidof -s PACKAGE`. Capture
bounded logs with `adb -s SERIAL logcat -d --pid PID`, using an observed PID.
For a crash, inspect `adb -s SERIAL logcat -d -b crash` and retain only entries
relevant to the test. Do not clear shared log buffers. Sanitize secrets and
personal data before including excerpts in an artifact.

Record the build/variant, emulator serial, reproduction steps, expected result,
observed result and evidence files. Separate passed, failed, blocked and
unobserved checks. Screenshots prove appearance; logs and assertions provide
additional evidence for behavior. Remove only temporary files created by this
test; preserve application data and existing device state.
