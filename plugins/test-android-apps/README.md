# Android App Testing

Ghast-authored Android test workflows using Google's official Android SDK
Platform Tools. This package includes one local CLI skill and no MCP server.

Official sources:
- https://developer.android.com/tools/adb
- https://developer.android.com/studio/run/emulator-commandline

The user supplies an Android SDK, authorized emulator and target app/project.
No SDK binary, device credentials, copied Codex workflow or third-party UI
control wrapper is bundled. This version replaces the previous OpenAI-derived
skill and Python helpers with Ghast-maintained instructions.

The workflow covers launch, UI hierarchy inspection, screenshots, input and
scoped logs. It does not claim performance profiling coverage. Local plugin
installation does not prove an app ran successfully on a device.

English and Chinese introductions are separate manifest fields selected by UI
language. Brand icon source:
https://www.gstatic.com/devrel-devsite/prod/v5e941f15ff6710591bee254538202655020220785b40a3f4d932e94adb9f6037/android/images/touchicon-180.png
This asset is linked by https://developer.android.com/. Android branding remains
Google's property; the MIT license covers Ghast-authored instructions and
configuration only.
