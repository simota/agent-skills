# CI Integration

Purpose: Wire XCUITest into headless CI — `xcodebuild test` / `test-without-building` invocation, `.xctestrun` packaging, `xcresulttool` result parsing, and platform-specific configuration for Xcode Cloud, GitHub Actions, Bitrise, and self-hosted runners. Covers device-farm handoff for real-device matrices.

Contents:
- `xcodebuild test` invocation (destination matrix, result bundle, parallelism, sharding)
- `test-without-building` + `.xctestrun` packaging
- `xcresulttool` parsing (Xcode 16+ schema, `--legacy` fallback)
- Xcode Cloud
- GitHub Actions (macOS runners)
- Bitrise
- Self-hosted runners (simulator pool + derived data isolation)
- Device-farm handoff

## `xcodebuild test` Invocation

```bash
xcodebuild test \
  -workspace MyApp.xcworkspace \
  -scheme MyAppUITests \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro,OS=18.2' \
  -destination 'platform=iOS Simulator,name=iPad Pro 13-inch (M4),OS=18.2' \
  -resultBundlePath ./build/Result.xcresult \
  -parallel-testing-enabled YES \
  -maximum-concurrent-test-simulator-destinations 4 \
  -only-testing:MyAppUITests/LoginFlowTests \
  -derivedDataPath ./build/DerivedData
```

Call out only the non-default choices when reporting a chosen invocation — do not narrate every flag:
- Multiple `-destination` entries run the same test plan across a device matrix in one invocation.
- `-parallel-testing-enabled YES` + `-maximum-concurrent-test-simulator-destinations N` shard across simulator clones on the same host; tune `N` to the runner's CPU/RAM headroom, not to an arbitrary "more is faster" assumption — oversubscribing a shared CI runner causes simulator boot timeouts.
- `-only-testing:<Target>/<Class>/<method>` and `-skip-testing:<Target>/<Class>` select or exclude specific tests — use `-skip-testing` to exclude the fastlane `Screenshots` scheme's test class from the PR-gating invocation (see `reference/fastlane-snapshot.md`).
- `-resultBundlePath` is mandatory for CI — machine-readable pass/fail, durations, and attachments all live in the resulting `.xcresult`; plain console output is not a reliable parse target.
- `-derivedDataPath` pinned to a per-job path (not the default global location) isolates concurrent CI jobs on a shared self-hosted runner from clobbering each other's build cache.

## `test-without-building` + `.xctestrun` Packaging

Split build and test into separate CI stages (build once, test on multiple destinations/farms) using `build-for-testing` to produce a `.xctestrun`:

```bash
# Stage 1: build once
xcodebuild build-for-testing \
  -workspace MyApp.xcworkspace \
  -scheme MyAppUITests \
  -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath ./build/DerivedData

# Produces: ./build/DerivedData/Build/Products/*.xctestrun + the built .app/.xctest bundles

# Stage 2: test without rebuilding, potentially on a different runner or destination
xcodebuild test-without-building \
  -xctestrun ./build/DerivedData/Build/Products/MyAppUITests_iphonesimulator18.2-arm64.xctestrun \
  -destination 'platform=iOS Simulator,name=iPhone 16 Pro,OS=18.2' \
  -resultBundlePath ./build/Result.xcresult
```

- Use this split when the same build needs to run against multiple destinations, a device farm, or a separate test-execution job — avoids rebuilding per destination.
- The `.xctestrun` bundle is the artifact device farms consume (see Device-Farm Handoff below) — package it together with the built `.app`/`.xctest` products, not just the `.xctestrun` file alone.

## `xcresulttool` Parsing

```bash
# Full result summary as JSON
xcrun xcresulttool get --path ./build/Result.xcresult --format json > result.json

# Follow a nested reference (attachments, sub-tests) — Xcode 16+ schema
xcrun xcresulttool get --path ./build/Result.xcresult --id <refId> --format json

# Extract a specific attachment (e.g. failure screenshot) to a file
xcrun xcresulttool get --path ./build/Result.xcresult --id <attachmentRefId> > failure.png

# Older Xcode / legacy schema fallback
xcrun xcresulttool get --legacy --path ./build/Result.xcresult --format json
```

- Xcode 16 introduced a structurally different result schema (nested under `actions._values` rather than the flat legacy layout). Pin the parser to the Xcode major version used in CI, or fall back to `--legacy` if the toolchain and parsing script are on different Xcode generations.
- For JUnit-consuming dashboards (most CI test-report widgets expect JUnit XML), convert with a shim such as `xcresultparser` or `xcbeautify --report junit` rather than hand-rolling a JSON→JUnit transform per project.
- Archive the raw `.xcresult` bundle as a CI artifact even after JUnit conversion — attachments (failure screenshots) only extract cleanly from the original bundle, not from a converted report.

## Xcode Cloud

```yaml
# ci_scripts/ci_post_clone.sh — Xcode Cloud custom build script hook
#!/bin/sh
echo "Xcode Cloud environment: $CI_XCODEBUILD_ACTION"
```

- Xcode Cloud runs the workflow's configured test action against its own managed macOS/Xcode/simulator matrix — define the destination matrix and parallelism in the Workflow editor (Xcode → Product → Xcode Cloud) rather than a raw `xcodebuild` invocation; Xcode Cloud wraps that call internally.
- Result bundles and attachments surface directly in App Store Connect's Xcode Cloud UI; still archive them as an artifact if a downstream tool (dashboard, Slack notifier) needs to parse `xcresulttool` output outside Apple's UI.
- Use `ci_post_clone.sh` / `ci_pre_xcodebuild.sh` / `ci_post_xcodebuild.sh` script hooks for environment prep (e.g. injecting `launchEnvironment` secrets) — Xcode Cloud has no arbitrary shell step outside these hook points.

## GitHub Actions (macOS Runners)

```yaml
# .github/workflows/ios-ui-tests.yml
name: iOS UI Tests

on:
  pull_request:
    branches: [main]

jobs:
  xcuitest:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.2.app

      - name: Run XCUITest
        run: |
          xcodebuild test \
            -workspace MyApp.xcworkspace \
            -scheme MyAppUITests \
            -destination 'platform=iOS Simulator,name=iPhone 16 Pro,OS=18.2' \
            -resultBundlePath ./build/Result.xcresult \
            -parallel-testing-enabled YES \
            -skip-testing:MyAppUITests/ScreenshotTests

      - name: Convert to JUnit
        if: always()
        run: xcbeautify --report junit --report-path ./build/junit < ./build/Result.xcresult

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: xcresult
          path: build/Result.xcresult
```

- `macos-15`/`macos-14` GitHub-hosted runners ship a pinned Xcode set; verify the runner image's available Xcode versions before pinning `-s /Applications/Xcode_X.Y.app` — GitHub rotates default/available Xcode versions on a regular cadence.
- `if: always()` on the artifact-upload and JUnit-conversion steps so a **test failure** still produces the `.xcresult` artifact — the default step behavior skips subsequent steps on failure otherwise.
- Simulator boot time dominates cold-runner latency; a `macos` runner with `xcrun simctl list` cached/warm devices boots meaningfully faster than a fully cold image — factor this into timeout budgets, not just test count.

## Bitrise

```yaml
# bitrise.yml (excerpt)
workflows:
  ui_test:
    steps:
      - xcode-test@5:
          inputs:
            - scheme: MyAppUITests
              destination: "platform=iOS Simulator,name=iPhone 16 Pro,OS=18.2"
            - is_clean_build: "no"
      - deploy-to-bitrise-io@2:
          inputs:
            - notify_user_groups: none
```

- Bitrise's `xcode-test` step wraps `xcodebuild test` and auto-archives the `.xcresult`/test report to the Bitrise dashboard — same non-default-flag-only reporting principle applies when documenting a chosen configuration (parallel simulators, device matrix, sharding).
- `deploy-to-bitrise-io@2` (or the dedicated artifact-deploy step) is the mechanism for surfacing the result bundle and screenshots to reviewers off the Bitrise build page.

## Self-Hosted Runners (Simulator Pool + Derived Data Isolation)

Self-hosted macOS runners (Mac minis, cloud Mac instances) need explicit isolation that hosted runners provide implicitly per-job:

- **Simulator pool management**: pre-provision a fixed pool of named simulators (`xcrun simctl create`) rather than letting each CI job create-and-destroy ephemeral devices — device creation/deletion churn is a common source of `xcodebuild` destination-resolution flake on busy self-hosted fleets.
- **Derived data isolation**: pass a per-job `-derivedDataPath` (e.g. keyed by CI job ID) so concurrent jobs on the same host do not race on the shared default DerivedData location.
- **Simulator reset between jobs**: `xcrun simctl erase <UDID>` (or `erase all` if the pool is exclusive to CI) before each job claims a device — leftover Keychain/UserDefaults state from a prior job's failed teardown is a real flake source on long-lived self-hosted runners.
- **Xcode version pinning**: self-hosted runners often carry multiple Xcode installs side by side (via `xcodes`); require `DEVELOPER_DIR=/Applications/Xcode_16.2.app` set explicitly per job rather than relying on whatever `xcode-select -p` happens to point to at job start.

## Device-Farm Handoff

Route `.xctestrun` bundles to a real-device farm when local simulator coverage is insufficient (hardware-specific bugs, camera/biometric flows, performance under real thermal/battery constraints):

```bash
# Package the built products + .xctestrun for upload
zip -r MyAppUITests.zip \
  ./build/DerivedData/Build/Products/Debug-iphoneos \
  ./build/DerivedData/Build/Products/MyAppUITests_iphoneos18.2-arm64.xctestrun
```

| Vendor | Notes |
|--------|-------|
| BrowserStack App Automate | Broadest real-device matrix; upload `.xctestrun` + app bundle via API or dashboard; parallel session cost scales with device count — confirm budget before wiring |
| Sauce Labs Real Device Cloud | Similar upload flow; strong enterprise SSO / detailed device logs |
| AWS Device Farm | Pay-per-minute; integrates with CodeBuild/CodePipeline for teams already on AWS CI infrastructure |

- Confirm the device-farm vendor and parallel-session budget before wiring upload (Ask First boundary) — real-device minutes are materially more expensive than simulator CI time.
- Tier the matrix: simulator on every PR → one farm device on merge to main → full real-device matrix on release gate. Never run the full farm matrix as the PR-blocking check.

## Cross-References

- `reference/fastlane-snapshot.md` — the separate, non-PR-blocking scheme this file's CI patterns must isolate from the regression-test invocation.
- `reference/screenshot-strategies.md` — the `XCTAttachment` content that `xcresulttool` extracts from the result bundle.
- Native's `reference/xcrun-cli.md` — `simctl` / `devicectl` command reference underlying the simulator-pool and device-lifecycle steps above.
