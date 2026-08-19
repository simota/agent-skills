# fastlane snapshot Pipeline

Purpose: Configure fastlane `snapshot` to generate App Store screenshots across a device and language matrix, reusing the same XCUITest target and Screen Objects Snap already authored — not a parallel test suite. Covers `Snapfile`, `SnapshotHelper.swift`, the dedicated screenshot scheme, the clean-status-bar pre-script, the device/language matrix, and `frameit` for marketing frames.

Contents:
- Pipeline shape and scheme separation
- `Snapfile` configuration
- `SnapshotHelper.swift` integration
- Writing `snapshot()` calls (reusing existing Screen Objects)
- Status-bar override before capture
- Device / language matrix and cost management
- `frameit` for marketing frames
- Output handling and CI notes

## Pipeline Shape And Scheme Separation

fastlane `snapshot` drives the **same** UI test target used for regression tests, but through a **separate scheme** so screenshot generation (10-30× slower, matrix-multiplied by devices × languages) never blocks PR-gating CI.

```
MyApp.xcworkspace
├── MyApp (app target)
├── MyAppUITests (shared XCUITest target — Screen Objects + identifiers)
│   ├── LoginFlowTests.swift        ← regression test (PR-gating scheme)
│   └── ScreenshotTests.swift       ← snapshot() calls (Screenshots scheme only)
├── MyApp.xcscheme                  ← app scheme
├── MyAppUITests.xcscheme           ← PR-gating scheme (excludes ScreenshotTests)
└── Screenshots.xcscheme            ← snapshot scheme (runs ScreenshotTests only)
```

- Reuse Page Objects and identifiers from `reference/xcuitest-patterns.md` and `reference/identifier-strategy.md` inside `ScreenshotTests.swift` — do not duplicate query logic.
- The `Screenshots` scheme's test plan/target membership includes only the screenshot test class(es); the PR-gating scheme excludes them via `-skip-testing:MyAppUITests/ScreenshotTests`.

## `Snapfile` Configuration

```ruby
# fastlane/Snapfile

# Devices to capture (App Store Connect device-size buckets)
devices([
  "iPhone 16 Pro Max",   # 6.9" — required size class
  "iPhone 16",           # 6.1"
  "iPad Pro 13-inch (M4)" # required for iPad-compatible apps
])

languages([
  "en-US",
  "ja-JP",
  "es-ES",
  "de-DE",
])

scheme("Screenshots")
output_directory("./fastlane/screenshots")
clear_previous_screenshots(true)

# Skip slow / irrelevant simulator states
concurrent_simulators(true)
stop_after_first_error(false)

# Launch arguments forwarded to XCUIApplication for deterministic fixture state
launch_arguments(["-ui-testing", "-snapshot-mode", "-disable-animations"])
```

- `devices` should map to App Store Connect's required screenshot size classes for the current submission — verify against Apple's current device-size requirements before finalizing the list; adding a device Apple does not require inflates capture time for no submission benefit.
- `concurrent_simulators(true)` parallelizes across the simulator pool; watch host machine RAM/CPU headroom in CI runners before enabling on a resource-constrained runner.
- `stop_after_first_error(false)` so one locale's failure does not abort the whole matrix run — review all failures in one pass instead of fixing-and-rerunning serially.

## `SnapshotHelper.swift` Integration

fastlane generates `SnapshotHelper.swift` (`fastlane snapshot init`); drop it into the UI test target and call `setupSnapshot(app)` before `app.launch()`:

```swift
import XCTest

final class ScreenshotTests: XCTestCase {
    var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        setupSnapshot(app) // must run BEFORE launch — configures locale + launch args
        app.launch()
    }
}
```

- `setupSnapshot(app)` injects the current language/locale launch arguments fastlane is driving for this matrix cell — calling it after `app.launch()` is a no-op and silently produces screenshots in the wrong locale.
- Re-run `fastlane snapshot init` after any major Xcode upgrade; Apple/fastlane periodically revise the helper for new Swift/Xcode compatibility.

## Writing `snapshot()` Calls

```swift
func testAppStoreScreenshots() throws {
    let login = LoginScreen(app: app)
    let dashboard = login.signIn(email: "demo@example.com", password: "Demo1234!")
    snapshot("01Login")

    dashboard.waitUntilDisplayed()
    snapshot("02Dashboard")

    let checkout = dashboard.openCheckout()
    checkout.applyPromoCode("SAVE10")
    snapshot("03CheckoutPromoApplied")
}
```

- Number-prefix snapshot names (`01`, `02`, ...) so App Store Connect Media Manager and local review both sort them in narrative order.
- Every `snapshot()` call implicitly captures `XCUIScreen.main.screenshot()` — no additional `XCTAttachment` wiring needed for App Store output; that pattern (`reference/screenshot-strategies.md`) is for regression evidence, a separate concern.
- Drive the app to each state through the same Screen Object methods used elsewhere in the suite — a screenshot test is a thin script on top of the existing Page Object layer, not a new query surface.

## Status-Bar Override Before Capture

Apple requires a clean status bar (no third-party app badges, static time, full battery/signal) for submitted screenshots. Run the override before the screenshot test executes, not per-`snapshot()` call:

```bash
#!/bin/bash
# fastlane/scripts/clean_status_bar.sh — run as a fastlane `before_each` or pre-action
UDID=$(xcrun simctl list devices booted -j | jq -r '.devices | to_entries[] | .value[0].udid')
xcrun simctl status_bar "$UDID" override \
  --time "9:41" \
  --dataNetwork wifi --wifiMode active --wifiBars 3 \
  --cellularMode active --cellularBars 4 \
  --batteryState charged --batteryLevel 100
```

```ruby
# fastlane/Fastfile
lane :screenshots do
  run_tests(scheme: "Screenshots", skip_slack: true) # snapshot lane wraps this
  # or invoke directly:
  snapshot
end

before_each do |lane, options|
  sh("bash ./fastlane/scripts/clean_status_bar.sh") if lane == :screenshots
end
```

- The override must run per-booted-simulator-session before the screenshot scheme launches; if fastlane spins fresh simulators per device in the matrix, the script needs to target the currently-booting UDID rather than a hardcoded one.
- `xcrun simctl status_bar <UDID> clear` restores default behavior after the capture session — include it in a post-action or CI teardown so leftover overrides do not leak into other jobs sharing the runner.

## Device / Language Matrix And Cost Management

Every additional device × language multiplies capture time and CI minutes linearly. Ask First (per Snap's Boundaries) once the matrix exceeds **3 devices × 3 languages**.

| Matrix size | Approx. wall time (per screenshot count `n`) | When appropriate |
|-------------|-----------------------------------------------|-------------------|
| 1 device × 1 language | `n × ~5-10s` | Local dev iteration, smoke-checking a new screenshot script |
| 3 devices × 3 languages | `9n × ~5-10s`, parallelizable with `concurrent_simulators` | Typical pre-submission review pass |
| Full required size classes × full supported languages | Scales past 15-20× | Final submission run only — schedule off the PR-gating pipeline (nightly or manual release job) |

- Parallelize with `concurrent_simulators(true)` before adding CI runner count — most of the cost is wall time, not CI minutes, until the matrix is large.
- Stage the matrix: iterate locally on 1×1, review on 3×3, run the full submission matrix once right before release.

## `frameit` For Marketing Frames

```ruby
# fastlane/Fastfile
lane :frame_screenshots do
  frameit(white: true) # wraps raw screenshots in device bezels + optional title text
end
```

```yaml
# fastlane/screenshots/en-US/framefile.json — per-locale title/keyword text overlay
{
  "default": {
    "title": {
      "color": "#000000",
      "font": "./fonts/Inter-Bold.ttf"
    },
    "background": "./background/gradient.png"
  },
  "01Login.png": { "keyword": { "string": "Sign In" }, "title": { "string": "Access your account instantly" } }
}
```

- `frameit` operates on the raw `snapshot()` output — run it as a separate lane/step after `snapshot`, never in place of it.
- Marketing frame text (`framefile.json`) is a Vision/Launch concern for copy; Snap's responsibility ends at producing clean, correctly-matrixed raw screenshots for `frameit` to consume.

## Output Handling And CI Notes

- Raw screenshots (`fastlane/screenshots/`) and `frameit` output are **artifacts, not commits** — upload to an artifact store (CI build artifacts, S3, or a dedicated screenshot branch) and hand the bundle to Launch for App Store Connect submission. Never commit to `main`.
- Run the `Screenshots` scheme in a separate, non-PR-blocking CI job (nightly, manual dispatch, or pre-release job) — see `reference/ci-integration.md` for the workflow shape and simulator pool considerations.
- Pin the fastlane and Xcode versions used to generate a submission's screenshots in the release notes/journal; a later Xcode upgrade can shift status-bar rendering or simulator chrome subtly enough to require a re-capture.

## Cross-References

- `reference/screenshot-strategies.md` — the underlying `XCTAttachment` / capture API concepts this pipeline builds on.
- `reference/xcuitest-patterns.md` — Screen Objects and identifiers reused inside `ScreenshotTests.swift`.
- `reference/ci-integration.md` — wiring the `Screenshots` scheme into a non-blocking CI job.
