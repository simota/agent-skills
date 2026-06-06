# xcrun — Xcode / Apple Toolchain CLI Reference

Production-grade reference for the `xcrun` wrapper and its most-used subtools (`simctl`, `devicectl`, `xctrace`, `xcresulttool`, `notarytool`, plus binary-introspection helpers). Focus: commands a native iOS developer or CI script actually runs day-to-day.

> Scope: iOS / macOS / watchOS / tvOS development from terminal or CI. Use this when scripting simulator/device automation, parsing test results, symbolicating crashes, or shipping to App Store Connect from headless environments.

---

## 0. Base Mechanics

- Role: resolves the current `DEVELOPER_DIR` / SDK and runs the appropriate internal tool.
- Switch active Xcode: `sudo xcode-select -s /Applications/Xcode_16.app`
- Locate a tool: `xcrun --find <tool>` (e.g. `xcrun --find swift`)
- Inspect SDK: `xcrun --show-sdk-path` / `xcrun --show-sdk-version`
- Target a specific SDK: `xcrun --sdk iphonesimulator <command>` / `--sdk iphoneos` / `--sdk macosx`
- Environment override: `DEVELOPER_DIR=/Applications/Xcode-beta.app xcrun ...` (no `sudo` needed; per-process)

---

## 1. `simctl` — Simulator Control (most-used)

| Command | Purpose |
|---------|---------|
| `xcrun simctl list` (`devices` / `runtimes` / `device_types`) | Enumerate everything |
| `xcrun simctl list devices booted` | Booted-only |
| `xcrun simctl boot <UDID>` / `shutdown <UDID>` / `shutdown all` | Lifecycle |
| `xcrun simctl create "iPhone 17 Pro" "iPhone 17 Pro" iOS19.0` | Create new device |
| `xcrun simctl erase <UDID>` / `erase all` | Reset device state |
| `xcrun simctl install <UDID> Path.app` / `uninstall <UDID> com.bundle.id` | Deploy app |
| `xcrun simctl launch <UDID> com.bundle.id [--console]` | Launch and stream stdout |
| `xcrun simctl terminate <UDID> com.bundle.id` | Kill app |
| `xcrun simctl openurl <UDID> myapp://path` | Test URL schemes / Universal Links |
| `xcrun simctl push <UDID> com.bundle.id payload.apns` | Simulate APNs push (payload is JSON) |
| `xcrun simctl io <UDID> recordVideo out.mp4` (Ctrl+C to stop) | Screen recording |
| `xcrun simctl io <UDID> screenshot out.png` | Screenshot |
| `xcrun simctl status_bar <UDID> override --time "9:41" --batteryState charged --batteryLevel 100 --wifiBars 3 --cellularBars 4` | Clean status bar for App Store screenshots |
| `xcrun simctl privacy <UDID> grant camera com.bundle.id` | Pre-grant permission (camera / photos / contacts / calendar / location / microphone / all) |
| `xcrun simctl get_app_container booted com.bundle.id data` | Sandbox path (debugging persistence) |
| `xcrun simctl spawn <UDID> log stream --predicate '...'` | Stream iOS unified log inside the simulator |
| `xcrun simctl keychain <UDID> reset` | Wipe Keychain (test isolation) |
| `xcrun simctl pair <watch-UDID> <phone-UDID>` / `pair_activate` | Watch pairing |
| `xcrun simctl ui <UDID> appearance light` / `dark` | Toggle dark mode |
| `xcrun simctl ui <UDID> content_size extra-large` / `extra-extra-extra-large` | Dynamic Type stress test |

### Recipe: automated screen recording

```bash
UDID=$(xcrun simctl list devices booted -j | jq -r '.devices | to_entries[] | .value[0].udid')
xcrun simctl launch "$UDID" com.example.app &
xcrun simctl io "$UDID" recordVideo demo.mp4
```

### Recipe: clean App Store screenshot session

```bash
UDID=...
xcrun simctl status_bar "$UDID" override \
  --time "9:41" --dataNetwork wifi --wifiMode active --wifiBars 3 \
  --cellularMode active --cellularBars 4 --batteryState charged --batteryLevel 100
# ... run UI test that calls xcrun simctl io screenshot per scene
xcrun simctl status_bar "$UDID" clear
```

---

## 2. `devicectl` — Physical Device Control (Xcode 15+, replaces `idevice*` / `ios-deploy`)

| Command | Purpose |
|---------|---------|
| `xcrun devicectl list devices` | Connected devices (USB + Wi-Fi) |
| `xcrun devicectl device info details --device <id>` | Hardware / OS info |
| `xcrun devicectl device install app --device <id> App.ipa` | Install IPA |
| `xcrun devicectl device process launch --device <id> com.bundle.id` | Launch |
| `xcrun devicectl device process list --device <id>` | Running processes |
| `xcrun devicectl device process terminate --device <id> --pid <pid>` | Kill |
| `xcrun devicectl device console --device <id>` | Stream syslog |
| `xcrun devicectl device copy from --device <id> <remote> <local>` / `to` | File transfer |

> Migration note: prefer `devicectl` for new CI. Legacy `ios-deploy` shows instability on M1/M2/M3 Macs with iOS 17+; replace it where possible.

---

## 3. `xctrace` — Instruments as a CLI (performance / leaks)

| Command | Purpose |
|---------|---------|
| `xcrun xctrace list templates` | Available templates (Time Profiler / Allocations / Leaks / etc.) |
| `xcrun xctrace list devices` | Recording targets |
| `xcrun xctrace record --template 'Time Profiler' --launch -- /Path/App.app/App` | Profile a fresh launch |
| `xcrun xctrace record --template 'Time Profiler' --device <UDID> --attach <pid> --time-limit 30s` | Attach to running process |
| `xcrun xctrace export --input out.trace --xpath '...'` | Trace → XML for diffing |

→ One of the few ways to gate Time Profiler / Allocations regressions in CI.

---

## 4. `xcresulttool` — Test Result Parsing

| Command | Purpose |
|---------|---------|
| `xcrun xcresulttool get --path Result.xcresult --format json` | Test result JSON |
| `xcrun xcresulttool get --path Result.xcresult --id <ref> --format json` | Follow nested references |
| `xcrun xcresulttool get --path Result.xcresult --id <attachmentRef> > out.png` | Extract attachment (failure screenshot) |

→ Pair with `xcodebuild test ... -resultBundlePath Result.xcresult` to parse pass/fail counts, durations, and attachments in CI.

---

## 5. `altool` / `notarytool` — App Store Submission + macOS Notarization

| Command | Purpose | Status |
|---------|---------|--------|
| `xcrun altool --upload-app -f App.ipa -t ios --apiKey <id> --apiIssuer <iss>` | Upload to App Store Connect | Working but **deprecation-track**; prefer App Store Connect API direct or `xcrun notarytool` for macOS |
| `xcrun altool --notarize-app ...` | (legacy) macOS notarization | **deprecated → use `notarytool`** |
| `xcrun notarytool submit App.zip --apple-id ... --team-id ... --password <app-specific> --wait` | macOS notarization (current) | |
| `xcrun notarytool history` / `info <submission-id>` / `log <submission-id>` | Status / failure logs | |
| `xcrun stapler staple App.app` | Staple notarization ticket to bundle | |

---

## 6. Binary Introspection (debugging / forensics)

| Command | Purpose |
|---------|---------|
| `xcrun lipo -info App.app/App` | Architecture inventory (arm64 / x86_64) |
| `xcrun lipo -create -output universal a.dylib b.dylib` | Build fat binary |
| `xcrun lipo -thin arm64 -output App-arm64 App` | Extract single arch |
| `xcrun strip -x App.app/App` | Strip non-global symbols (size reduction) |
| `xcrun atos -o App.app.dSYM/Contents/Resources/DWARF/App -arch arm64 -l <baseAddr> <addr>` | Symbolicate crash address |
| `xcrun dwarfdump --uuid App.app.dSYM` | dSYM UUID (must match crashed binary) |
| `xcrun otool -L App.app/App` | Linked dynamic libraries |
| `xcrun otool -hv App.app/App` | Mach-O header (load commands) |
| `xcrun codesign -d --entitlements - App.app` | Entitlements |
| `xcrun codesign -dvvv App.app` | Verbose signing info |
| `xcrun security find-identity -p codesigning -v` | Available signing identities |
| `xcrun security cms -D -i embedded.mobileprovision` | Decode provisioning profile |

---

## 7. xcodebuild (not via xcrun, but always co-used)

```bash
# Build for simulator
xcodebuild -workspace App.xcworkspace -scheme App \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro,OS=latest' \
  -configuration Debug build

# Test with result bundle (machine-readable)
xcodebuild test -workspace App.xcworkspace -scheme AppTests \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro,OS=latest' \
  -resultBundlePath TestResults.xcresult -enableCodeCoverage YES

# Archive + export
xcodebuild archive -workspace App.xcworkspace -scheme App \
  -configuration Release -archivePath build/App.xcarchive
xcodebuild -exportArchive -archivePath build/App.xcarchive \
  -exportOptionsPlist exportOptions.plist -exportPath build/export

# Export App Store Connect localization XLIFF (handoff to Polyglot)
xcodebuild -exportLocalizations -project App.xcodeproj -localizationPath ./l10n -includeScreenshots
```

---

## 8. Gotchas

1. **`xcrun` looks up tools in active Xcode only** — `xcode-select -p` to verify. CI runners with multiple Xcodes installed (via `xcodes`) require explicit `DEVELOPER_DIR=...` per build.
2. **`simctl push` payload format** — must be a top-level `aps` dict; if you copy a server payload that's already wrapped, strip the wrapper. Bundle ID arg is mandatory.
3. **Booted device disambiguation** — `simctl io booted screenshot` works when exactly one device is booted; with multiple, use explicit UDID.
4. **`devicectl` vs `idb`** — Apple's `devicectl` covers basic install/launch/console, but Facebook's `idb` is still richer for UI automation (touch / swipe / record events). Pick `devicectl` for CI signing/install paths, `idb` for E2E test orchestration.
5. **`xctrace record --launch`** vs `--attach` — `--launch` requires the .app bundle path, not the bundle ID. `--attach` accepts pid only on a known device.
6. **`xcresulttool` schema breaking changes** — Xcode 16 introduced a new structure under `actions._values`; pin your parser to the Xcode version or use `xcresulttool get --legacy` for the older shape.
7. **`notarytool` keychain profile** — `xcrun notarytool store-credentials "AC_KEY"` once saves Apple ID + app-specific password to Keychain; subsequent calls use `--keychain-profile AC_KEY` instead of inline credentials.
8. **`atos` requires the matching dSYM UUID** — `dwarfdump --uuid` on the dSYM must equal the crash report's binary UUID. Mismatch produces nonsensical symbols silently.

---

## Cross-References

- `reference/mobile-ci-cd.md` — Xcode Cloud / fastlane / GitHub Actions pipeline integration
- `reference/release-rollout.md` — TestFlight phased release that consumes `notarytool` / `altool` output
- `reference/adb-cli.md` — Android counterpart (side-by-side iOS ↔ Android command mapping at bottom of that file)
- Apple official: <https://developer.apple.com/documentation/xcode-release-notes>
