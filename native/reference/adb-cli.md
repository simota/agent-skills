# adb — Android Debug Bridge Reference

Production-grade reference for `adb` (Android Debug Bridge) covering the subcommands a native Android developer or CI script actually uses. Focus: app management, device control, logging, state simulation, and performance tracing.

> Scope: Android development from terminal or CI — installs, instrumentation runs, debugging, demo recording, Doze / network state simulation, Perfetto tracing. Use this alongside `reference/xcrun-cli.md` for iOS / Android symmetric tooling.

---

## 0. Base Mechanics

```bash
adb version                    # Server / client version
adb start-server / kill-server # Restart adb daemon
adb devices -l                 # Connected devices + product / model / transport_id
adb -s <serial> <cmd>          # Target specific device
adb -d <cmd>                   # Prefer USB device
adb -e <cmd>                   # Prefer emulator
```

Active config knobs:
- `ANDROID_HOME` / `ANDROID_SDK_ROOT` — SDK location
- `ADB_VENDOR_KEYS` — additional RSA keys for unattended auth
- `ANDROID_SERIAL` — implicit `-s` target

---

## 1. App Management

| Command | Purpose |
|---------|---------|
| `adb install -r app.apk` | Reinstall (keep data) |
| `adb install -t app.apk` | Allow test-only APKs (debuggable) |
| `adb install -g app.apk` | Grant all runtime permissions on install |
| `adb install --user 0 -r app.apk` | Install for primary user (multi-user devices) |
| `adb install-multiple base.apk split1.apk split2.apk` | App Bundle split APKs |
| `adb uninstall com.example.app` | Uninstall (-k keeps data) |
| `adb shell pm list packages -3` | Third-party packages only (`-s` system / `-d` disabled / `-e` enabled / `-u` includes uninstalled) |
| `adb shell pm path com.example.app` | Resolve APK path on device |
| `adb shell pm clear com.example.app` | Wipe app data (essential for test isolation) |
| `adb shell pm grant com.example.app android.permission.CAMERA` | Pre-grant runtime permission |
| `adb shell pm revoke com.example.app android.permission.CAMERA` | Revoke |
| `adb shell pm reset-permissions` | Reset all runtime permissions |
| `adb shell pm disable-user --user 0 com.example.bloat` | Disable system app without root |
| `adb shell pm dump com.example.app` | Verbose package info (sigs / perms / activities) |

---

## 2. Activity Manager (launching, killing, intents)

| Command | Purpose |
|---------|---------|
| `adb shell am start -n com.example/.MainActivity` | Launch Activity |
| `adb shell am start -a android.intent.action.VIEW -d "myapp://path"` | Deep link / App Link test |
| `adb shell am force-stop com.example.app` | Force-stop (clears process + cached state) |
| `adb shell am kill com.example.app` | Kill background process only (no effect on foreground) |
| `adb shell am start-service com.example/.MyService` | Start Service (Android 12+: use `start-foreground-service`) |
| `adb shell am broadcast -a com.example.ACTION --es key value` | Send Broadcast with string extra |
| `adb shell am instrument -w com.example.app.test/androidx.test.runner.AndroidJUnitRunner` | Run instrumented tests |
| `adb shell am stack list` | Activity stack snapshot (debugging back-stack bugs) |

---

## 3. Logging & Diagnostics

| Command | Purpose |
|---------|---------|
| `adb logcat` | All logs |
| `adb logcat -c` | Clear buffer |
| `adb logcat *:E` | Error and above |
| `adb logcat -s MyTag:V` | One tag, verbose level |
| `adb logcat --pid=$(adb shell pidof com.example.app)` | App-scoped log (Android 7+) |
| `adb logcat -v threadtime` | Recommended format (date + pid + tid + level + tag) |
| `adb logcat -b crash -b events` | Specific buffers (default + crash + events + system + main + radio) |
| `adb bugreport bugreport.zip` | Full system report (includes perfetto trace, logs, dumpsys) |
| `adb shell dumpsys activity activities` | Activity state across all tasks |
| `adb shell dumpsys window \| grep -E "mCurrentFocus\|mFocusedApp"` | Currently focused Activity |
| `adb shell dumpsys gfxinfo com.example.app` | Frame-render stats (jank detection) |
| `adb shell dumpsys gfxinfo com.example.app framestats` | Per-frame timing (debugging dropped frames) |
| `adb shell dumpsys meminfo com.example.app` | Memory breakdown |
| `adb shell dumpsys batterystats com.example.app` | Battery usage attribution |
| `adb shell dumpsys battery` | Battery state |
| `adb shell dumpsys power` | Power / wakelock state |
| `adb shell top -m 10` | Top processes by CPU |
| `adb shell ps -A | grep com.example` | Process listing |

---

## 4. File Transfer

| Command | Purpose |
|---------|---------|
| `adb push local /sdcard/remote` | Push to device |
| `adb pull /sdcard/remote local` | Pull from device |
| `adb shell run-as com.example.app cat databases/app.db > app.db` | Read debuggable app's private storage (no root) |
| `adb shell run-as com.example.app tar -cf - .` | Tar entire app sandbox (debuggable apps) |
| `adb backup -f backup.ab -apk com.example.app` | Legacy backup (heavily restricted on Android 12+) |

---

## 5. Network & Wi-Fi ADB (Android 11+ requires `pair`)

```bash
# USB → Wi-Fi switchover (legacy, still works for rooted / debug devices)
adb tcpip 5555
adb connect 192.168.1.10:5555

# Android 11+ Wireless Debugging (developer options must enable "Wireless debugging")
# Tap "Pair device with pairing code" on device → shows IP:port and 6-digit code
adb pair 192.168.1.10:37123          # Then enter pairing code at prompt
adb connect 192.168.1.10:43215       # IP:port shown under "IP address & Port"

# Port forwarding
adb forward tcp:8080 tcp:8080        # PC localhost:8080 → device localhost:8080
adb reverse tcp:3000 tcp:3000        # device localhost:3000 → PC localhost:3000 (REQUIRED for Metro / Vite dev server)
adb forward --list                    # Current forwards
adb forward --remove tcp:8080         # Remove single
adb forward --remove-all              # Reset
```

---

## 6. Screen & Input

| Command | Purpose |
|---------|---------|
| `adb shell screencap -p /sdcard/s.png && adb pull /sdcard/s.png` | Screenshot (use `-p` for PNG; raw without it) |
| `adb exec-out screencap -p > s.png` | Screenshot without intermediate file (fast) |
| `adb shell screenrecord --time-limit 30 --bit-rate 8M /sdcard/rec.mp4` | Record (max 3 min, no audio, no 4K) |
| `adb shell screenrecord --size 720x1280 --bit-rate 4M /sdcard/rec.mp4` | Constrained for smaller files |
| `adb shell input tap 500 1000` | Tap at (x, y) |
| `adb shell input swipe 100 1000 100 200 300` | Swipe with last arg = duration ms |
| `adb shell input text "hello"` | Type text (space = `%s`) |
| `adb shell input keyevent KEYCODE_HOME` | Key event (3=HOME, 4=BACK, 82=MENU, 26=POWER, 24=VOL_UP, 25=VOL_DOWN, 187=APP_SWITCH) |
| `adb shell input keyevent --longpress KEYCODE_POWER` | Long press |

→ Pairs well with `director` skill for automated demo recording.

---

## 7. Device State Simulation (test edge cases)

| Command | Purpose |
|---------|---------|
| `adb shell svc wifi disable` / `enable` | Wi-Fi toggle |
| `adb shell svc data disable` / `enable` | Mobile data toggle |
| `adb shell cmd connectivity airplane-mode enable` / `disable` | Airplane mode |
| `adb shell dumpsys battery set level 10 && adb shell dumpsys battery set status 1` | Fake low battery (status 1=unknown, 2=charging, 3=discharging, 4=not charging, 5=full) |
| `adb shell dumpsys battery unplug` | Simulate unplugged (for Doze testing) |
| `adb shell dumpsys battery reset` | Restore real readings |
| `adb shell dumpsys deviceidle force-idle` | Force Doze mode |
| `adb shell dumpsys deviceidle step` | Advance Doze state machine one step |
| `adb shell dumpsys deviceidle unforce` | Exit forced Doze |
| `adb shell cmd appops set com.example.app RUN_IN_BACKGROUND ignore` | Restrict background |
| `adb shell settings put global window_animation_scale 0` | Disable window animation (test speedup) |
| `adb shell settings put global transition_animation_scale 0` | Same for transitions |
| `adb shell settings put global animator_duration_scale 0` | Same for animators |
| `adb shell setprop persist.sys.locale ja-JP` (requires reboot) | Change locale (debug builds) |
| `adb emu battery 20` | Emulator-only: battery level |
| `adb emu geo fix 139.6917 35.6895` | Emulator GPS fix (Tokyo Station lon lat) |
| `adb emu sms send +15551234567 "test"` | Emulator: simulate incoming SMS |

---

## 8. Properties & Settings (low-level config)

| Command | Purpose |
|---------|---------|
| `adb shell getprop` | All system properties |
| `adb shell getprop ro.build.version.release` | Single property |
| `adb shell setprop log.tag.MyTag VERBOSE` | Dynamic log level (debug builds) |
| `adb shell settings get global hidden_api_policy` | Read setting (namespaces: global / system / secure) |
| `adb shell settings put global hidden_api_policy 1` | Relax hidden API (debug builds; restore: `settings delete global hidden_api_policy`) |
| `adb shell cmd package install-existing com.example.app` | Re-enable a system package |

---

## 9. Perfetto Tracing (system-wide profiling)

```bash
# Trigger Perfetto trace with inline config (5-second sched trace)
adb shell perfetto -c - --txt -o /data/misc/perfetto-traces/trace.pftrace <<EOF
buffers { size_kb: 65536 }
data_sources {
  config {
    name: "linux.ftrace"
    ftrace_config { ftrace_events: "sched/sched_switch" }
  }
}
duration_ms: 5000
EOF
adb pull /data/misc/perfetto-traces/trace.pftrace
# Open at https://ui.perfetto.dev
```

For app-specific frame / startup tracing, use Macrobenchmark library + `androidx.tracing` annotations; results land in `bugreport` Perfetto trace.

---

## 10. Stress / Fuzz Testing

| Command | Purpose |
|---------|---------|
| `adb shell monkey -p com.example.app -v 500` | 500-event UI fuzz |
| `adb shell monkey -p com.example.app --pct-touch 50 --pct-motion 30 --throttle 100 -v 1000` | Tunable event mix |
| `adb shell monkey --kill-process-after-error -v 1000` | Stop on first crash |

---

## 11. Crash Symbolication

```bash
# Native (NDK)
adb logcat | ndk-stack -sym ./obj/local/arm64-v8a

# Kotlin / Java with R8
# Use proguard mapping file (build/outputs/mapping/release/mapping.txt) with:
java -jar retrace.jar mapping.txt obfuscated-stacktrace.txt > readable.txt
```

---

## 12. Practical One-Liners

```bash
# Currently focused package
adb shell dumpsys window | awk '/mCurrentFocus/{print $NF}' | sed 's/}//'

# All installed third-party apps with version
for pkg in $(adb shell pm list packages -3 | sed 's/package://'); do
  v=$(adb shell dumpsys package "$pkg" | awk '/versionName=/{print $1; exit}')
  echo "$pkg $v"
done

# CPU/MEM top 5, refresh every 1s
adb shell top -d 1 -m 5 -s cpu

# Cold-start time (am start prints TotalTime)
adb shell am force-stop com.example.app
adb shell am start -W -n com.example/.MainActivity | grep -E "TotalTime|WaitTime"

# Auto-grant all runtime permissions on install
adb install -g app.apk

# Tail logs for one app and color CRITICAL keywords
adb logcat --pid=$(adb shell pidof com.example.app) -v color
```

---

## 13. Gotchas

1. **`pidof` requires Android 7+** — pre-N use `ps | grep com.example.app | awk '{print $2}'`.
2. **`adb shell screencap` raw mode** — without `-p`, output is raw RGBA pixels; always pass `-p` for PNG.
3. **`screenrecord` limits** — 3-min cap, no audio, no 4K, MP4 container only. For longer or audio-included recordings use `scrcpy --record file.mp4` on the host.
4. **`am force-stop` vs `kill`** — `force-stop` clears alarms, jobs, and cached processes; `kill` only kills background. Use `force-stop` for clean test isolation.
5. **Wireless ADB pairing token expires** — Android 11+ pairing codes are single-use and time-bound; re-pair if `adb connect` fails after a long idle.
6. **`dumpsys battery set ...` requires `unplug` first** on Android 14+ — the simulated values are ignored while a real charger is connected; call `adb shell dumpsys battery unplug` first.
7. **`dumpsys deviceidle force-idle` only works while unplugged** — combine with `battery unplug` to test Doze paths.
8. **`run-as` requires debuggable app** — release / store builds reject `run-as`; for prod-build debugging take a `bugreport` instead.
9. **`hidden_api_policy` reset** — always `settings delete global hidden_api_policy` after debugging; leaving relaxed policy on a device skews compliance test results.
10. **`adb forward` does NOT survive `adb kill-server`** — restart breaks all forwards silently; CI scripts should re-establish forwards after any server restart.

---

## Cross-References

- `reference/mobile-ci-cd.md` — Gradle / fastlane / GitHub Actions integration with `adb install` and `connectedAndroidTest`
- `reference/bg-execution.md` — Doze / WorkManager scenarios that `dumpsys deviceidle` exercises
- `reference/release-rollout.md` — Play staged rollout that consumes `bundletool` + signed AAB
- `reference/xcrun-cli.md` — iOS counterpart

### iOS ↔ Android command map (cross-platform quick reference)

| Task | iOS (xcrun) | Android (adb) |
|------|-------------|---------------|
| Boot simulator/emulator | `simctl boot <UDID>` | `emulator -avd <name>` |
| Install on simulator/device | `simctl install booted App.app` / `devicectl device install app` | `adb install -r app.apk` |
| Launch app | `simctl launch booted com.bundle.id` | `adb shell am start -n com.example/.Main` |
| Force-stop | `simctl terminate booted com.bundle.id` | `adb shell am force-stop com.example` |
| Stream logs (app-scoped) | `simctl spawn booted log stream --predicate 'subsystem == "com.example"'` | `adb logcat --pid=$(adb shell pidof com.example)` |
| Screenshot | `simctl io booted screenshot s.png` | `adb exec-out screencap -p > s.png` |
| Screen record | `simctl io booted recordVideo r.mp4` | `adb shell screenrecord /sdcard/r.mp4` |
| Deep link | `simctl openurl booted "scheme://path"` | `adb shell am start -a VIEW -d "scheme://path"` |
| Push notification test | `simctl push booted com.bundle.id payload.apns` | `adb shell am broadcast` or FCM SDK direct |
| Performance trace | `xctrace record --template 'Time Profiler' ...` | `adb shell perfetto -c ...` + ui.perfetto.dev |
| Crash symbolication | `atos -o App.dSYM/.../App -arch arm64 -l <baseAddr> <addr>` | `ndk-stack -sym <obj-dir>` (native) or `retrace.jar mapping.txt` (R8) |
| Fake device state | `simctl status_bar override ...` (limited) | `dumpsys battery/deviceidle/settings` (broad) |
