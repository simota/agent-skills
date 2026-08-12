# XCUITest Patterns

Purpose: Author and refactor XCUITest code that survives UI refactors and does not flake. Covers `XCUIApplication` lifecycle, `XCUIElement` / `XCUIElementQuery` query patterns, deterministic wait strategies, gesture APIs, launch-time fixture injection, and the Screen Object / Page Object structure Snap enforces on every suite.

Contents:
- `XCUIApplication` lifecycle and launch configuration
- `XCUIElement` / `XCUIElementQuery` query patterns
- Wait strategies (`XCTNSPredicateExpectation`, never `Thread.sleep`)
- Gesture APIs (tap / swipe / pinch / dragAndDrop)
- Screen Object / Page Object pattern in Swift
- Refactoring Xcode-recorded tests
- Coordinate-based taps (last resort)
- Anti-patterns

## `XCUIApplication` Lifecycle And Launch Configuration

`XCUIApplication` is a proxy for the app-under-test running in a separate process. Each test method should own its own launch so state never bleeds across tests.

```swift
final class LoginFlowTests: XCTestCase {
    var app: XCUIApplication!

    override func setUpWithError() throws {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["-ui-testing", "-disable-animations"]
        app.launchEnvironment = [
            "API_BASE_URL": "https://staging.example.com",
            "SEED_USER": "standard_user",
        ]
        app.launch()
    }

    override func tearDownWithError() throws {
        app = nil
    }
}
```

- `launchArguments` / `launchEnvironment` are read by the app target at boot (`ProcessInfo.processInfo.arguments` / `.environment`). Use them to force a fixture screen, disable animation, and point networking at a stub server — never mutate app state by tapping through onboarding first.
- One `XCUIApplication()` instance per test method (`setUpWithError`), not a shared singleton across the file. Cross-test state bleed is a top flake source.
- `app.terminate()` in `tearDownWithError` only when a test intentionally leaves the app in a broken state (crash repro); normal tests let the next `setUpWithError` launch fresh.
- Multi-app tests (e.g. Safari handoff, share sheet to another app) use a second `XCUIApplication(bundleIdentifier:)` instance — do not assume the queried element belongs to your app once focus leaves it.

## `XCUIElement` / `XCUIElementQuery` Patterns

Queries traverse the accessibility tree, not the view hierarchy. Prefer identifier-based, single-hop queries; deep nested predicate chains are slow and brittle.

```swift
// Preferred: direct identifier lookup
let emailField = app.textFields["login.email.field"]
let submitButton = app.buttons["login.submit.button"]

// Scoped query when the same identifier convention repeats per row
let firstRow = app.cells.matching(identifier: "order.row").element(boundBy: 0)
let firstRowTotal = firstRow.staticTexts["order.row.total"]

// Predicate query — reserve for cases identifiers cannot cover (system alerts, dynamic counts)
let badge = app.staticTexts.matching(
    NSPredicate(format: "label MATCHES %@", #"^\d+ unread$"#)
).firstMatch
```

- `app.descendants(matching: .any)` is a last resort for exploratory debugging only — never leave it in a committed test; it defeats the point of an identifier taxonomy.
- `.firstMatch` short-circuits the query as soon as one match is accessible; use it whenever "any one" is semantically correct — it is materially faster than indexing into a full `XCUIElementQuery`.
- Element existence (`.exists`) and hittability (`.isHittable`) are different facts: an element can exist off-screen or behind a modal and still fail interaction. Assert `isHittable` before `tap()`, not just `exists`.

## Wait Strategies

Never synchronize with `Thread.sleep` / `sleep()`. XCUITest flake is a race-condition problem, not a "wait longer" problem — sleeping a fixed duration either wastes CI time (if generous) or still races (if not).

```swift
func waitAndTap(_ element: XCUIElement, timeout: TimeInterval = 10, file: StaticString = #filePath, line: UInt = #line) {
    let predicate = NSPredicate(format: "exists == true AND isHittable == true")
    let expectation = XCTNSPredicateExpectation(predicate: predicate, object: element)
    let result = XCTWaiter().wait(for: [expectation], timeout: timeout)
    XCTAssertEqual(result, .completed, "Element not hittable after \(timeout)s", file: file, line: line)
    element.tap()
}
```

- Default timeout: `10s`. Justify anything longer inline (e.g. a known-slow server round trip) — do not silently raise the global default to paper over a race.
- Prefer `XCTWaiter().wait(for:timeout:)` over the older `waitForExpectations(timeout:)` API — it returns a `XCTWaiter.Result` you can assert on directly instead of throwing.
- For "element disappears" waits (e.g. spinner dismissal), predicate on `exists == false`, not a fixed delay before the next assertion.
- Network-backed screens: prefer stubbing the response (deterministic, fast) over waiting on real latency. Reserve real-network waits for the smallest possible "it actually talks to the backend" smoke test.

## Gesture APIs

```swift
// Tap
element.tap()
element.doubleTap()
element.press(forDuration: 1.2) // long-press

// Swipe
app.swipeUp()                    // whole-screen swipe, use sparingly
scrollView.swipeLeft()           // scoped to a container — prefer this over whole-screen

// Pinch (zoom)
imageView.pinch(withScale: 2.0, velocity: 1.0)   // zoom in
imageView.pinch(withScale: 0.5, velocity: -1.0)  // zoom out

// Drag and drop
let source = app.cells["reorder.row.3"]
let target = app.cells["reorder.row.1"]
source.press(forDuration: 0.5, thenDragTo: target)
```

- Scope gestures to the smallest containing element (a specific `scrollView` or `table`) rather than `app.swipeUp()` — whole-screen gestures can hit unintended elements when layout shifts.
- `press(forDuration:thenDragTo:)` is the standard reorder / drag interaction; tune `forDuration` to clear the app's own long-press-to-drag threshold (usually `0.4-0.6s`).
- Multi-finger gestures (`pinch`, two-finger scroll) are simulator-supported but sometimes behave differently than physical multi-touch — verify pinch/zoom-heavy flows on a real device before trusting simulator-only coverage.

## Screen Object / Page Object Pattern

One class per screen. The class owns every `XCUIElementQuery` for that screen and exposes user-intent methods — tests read like a spec, not like a query dump.

```swift
protocol BaseScreen {
    var app: XCUIApplication { get }
}

extension BaseScreen {
    func waitForHittable(_ element: XCUIElement, timeout: TimeInterval = 10) -> Bool {
        let predicate = NSPredicate(format: "exists == true AND isHittable == true")
        let expectation = XCTNSPredicateExpectation(predicate: predicate, object: element)
        return XCTWaiter().wait(for: [expectation], timeout: timeout) == .completed
    }
}

struct LoginScreen: BaseScreen {
    let app: XCUIApplication

    private var emailField: XCUIElement { app.textFields["login.email.field"] }
    private var passwordField: XCUIElement { app.secureTextFields["login.password.field"] }
    private var submitButton: XCUIElement { app.buttons["login.submit.button"] }

    @discardableResult
    func signIn(email: String, password: String) -> DashboardScreen {
        _ = waitForHittable(emailField)
        emailField.tap()
        emailField.typeText(email)
        passwordField.tap()
        passwordField.typeText(password)
        submitButton.tap()
        return DashboardScreen(app: app)
    }
}

struct DashboardScreen: BaseScreen {
    let app: XCUIApplication
    var isDisplayed: Bool { app.otherElements["dashboard.root"].waitForExistence(timeout: 10) }
}
```

- Methods return the next Screen Object when the user action navigates (`signIn` returns `DashboardScreen`) so tests chain fluently: `LoginScreen(app: app).signIn(...).isDisplayed`.
- Keep private query properties `private`; only intent methods and read-only state (`isDisplayed`, `errorMessage`) are `public`/`internal`.
- Share cross-cutting waits and helpers via a `BaseScreen` protocol extension, not by subclassing — protocol composition keeps Screen Objects lightweight structs.
- One Screen Object per screen, not per test. Reuse across the whole suite; a screen's query surface should have exactly one source of truth.

## Refactoring Xcode-Recorded Tests

Xcode's UI Recording (red record button in the test editor) is scaffolding, never the final artifact. Recorded code:

```swift
// As recorded — coordinate/index-heavy, brittle
app.tables.cells.element(boundBy: 2).tap()
app.buttons.element(boundBy: 5).tap()
```

Refactor to identifier-based Screen Object calls before merging:

```swift
OrdersListScreen(app: app).selectOrder(named: "Order #1042")
OrderDetailScreen(app: app).tapReorderButton()
```

Refactor checklist:
1. Replace every `.element(boundBy:)` / coordinate tap with an identifier query — add the identifier to the app if it is missing (file to Native).
2. Extract queries into the screen's Screen Object; delete inline queries from the test body.
3. Replace `sleep`/fixed delays the recorder sometimes inserts with `XCTNSPredicateExpectation` waits.
4. Re-run the refactored test 5-10× locally to confirm no residual race before committing.

## Coordinate-Based Taps (Last Resort)

```swift
// Only for canvases / system UI Snap cannot annotate with identifiers
let canvas = app.otherElements["drawing.canvas"]
let point = canvas.coordinate(withNormalizedOffset: CGVector(dx: 0.5, dy: 0.5))
point.tap()
```

Reserve `coordinate(withNormalizedOffset:)` for drawing canvases, maps, and system alerts/permission sheets that expose no stable identifier. Comment the exception inline explaining why an identifier query was not possible.

## Anti-Patterns

- `Thread.sleep` / `sleep()` anywhere in a test or Screen Object — always a `XCTNSPredicateExpectation`.
- Mutating app state through the UI to set up a test (navigating through onboarding to reach a fixture screen) instead of `launchArguments` / `launchEnvironment`.
- Deep `XCUIElementQuery` predicate chains against the full tree (`app.descendants(matching: .any).matching(...)`) when a scoped identifier query would do.
- Recorded coordinate/index-based code left uncommitted-to-refactor — recordings are a starting point, not a deliverable.
- One shared `XCUIApplication` instance reused across test methods without a fresh launch — carries state and timing artifacts between tests.

## Cross-References

- `reference/identifier-strategy.md` — designing the identifier taxonomy these queries depend on.
- `reference/screenshot-strategies.md` — attaching evidence when a Screen Object assertion fails.
- `reference/ci-integration.md` — running the resulting suite under `xcodebuild test` with sharding and parallelism.


---

## Per-Recipe Behavior Notes (SKILL.md excerpt)

- `xcuitest`: end-to-end XCUITest target authoring. Establish identifier convention first; Screen Object structure; `XCTNSPredicateExpectation` waits; launch arguments for state. Default timeout 10s; justify longer.
- `identifier`: audit-only Recipe. Produce a taxonomy doc (`screen.section.element`), a gap list (which views lack identifiers), and a handoff to Native for retrofit. Verify findings with Accessibility Inspector and recorded UI hierarchy.
- `screenshot`: in-test capture via `XCTAttachment.screenshot(...)` with `.lifetime = .keepAlways`. Capture on failure (default) and at key checkpoints (opt-in). Do not introduce pixel-diff assertions inside XCUITest — refer that to `swift-snapshot-testing` or visual-AI vendor.
- `appstore`: fastlane snapshot wiring. Produces `Snapfile` (devices / languages), `SnapshotHelper.swift` (drops into test target), a dedicated `Screenshots` scheme, and a status-bar override pre-script. Combine with frameit for marketing frames. Output goes to artifact store, never committed to main.
- `page-object`: refactor existing or recorded XCUITest code into Swift Screen Object classes. One class per screen; expose user-intent methods; isolate query chains; share helpers via a `BaseScreen` protocol or class.
- `ci`: wire `xcodebuild test -workspace <ws> -scheme <scheme> -destination "<dest>" -resultBundlePath Result.xcresult -parallel-testing-enabled YES` into CI; archive `.xcresult`; convert via `xcresulttool get --format json` and optional JUnit shim. Cover Xcode Cloud, GitHub Actions (`macos-14`+), Bitrise.
- `farm`: build `.xctestrun` via `xcodebuild build-for-testing`, package the resulting `.app` + `.xctestrun`, upload to BrowserStack App Automate / Sauce Labs Real Device Cloud / AWS Device Farm. Tier the matrix: simulator on PR → 1 farm device on merge → multi-device on release gate.
- `xcresult`: parse-only Recipe. Extract attachments (`xcrun xcresulttool get --path Result.xcresult --id <ref> > out.png`), pass/fail counts, durations. Pin parser to Xcode major or use `--legacy`.

### Signal Keywords → Recipe

| Keywords | Recipe |
|----------|--------|
| `xcuitest`, `XCUIApplication`, `XCUIElement`, `XCUIElementQuery`, `ios ui test`, `swift ui test` | `xcuitest` |
| `accessibility identifier`, `accessibilityIdentifier`, `identifier taxonomy`, `swiftui identifier`, `uikit isAccessibilityElement` | `identifier` |
| `screenshot`, `XCTAttachment`, `failure screenshot`, `regression screenshot`, `ios screenshot test` | `screenshot` |
| `fastlane snapshot`, `Snapfile`, `SnapshotHelper`, `App Store screenshot`, `frameit`, `marketing screenshot` | `appstore` |
| `page object`, `screen object`, `XCUITest refactor`, `recorded test cleanup` | `page-object` |
| `xcodebuild test`, `xcodebuild test-without-building`, `xctestrun`, `Xcode Cloud xcuitest`, `github actions ios test`, `bitrise ios` | `ci` |
| `browserstack ios`, `sauce labs ios`, `aws device farm ios`, `real device ios`, `.xctestrun upload` | `farm` |
| `xcresult`, `xcresulttool`, `result bundle`, `junit ios`, `test attachment extract` | `xcresult` |
| `status bar override`, `simctl status_bar`, `clean status bar`, `9:41 screenshot` | `appstore` (status-bar branch) |
| `swift snapshot testing`, `pointfree snapshot`, `view snapshot baseline` | `screenshot` (baseline branch — clarify whether XCUITest or unit-snapshot scope) |
| unclear iOS test request | `xcuitest` (default) |



## Capability Detail (SKILL.md excerpt)

- xcuitest_authoring: Author XCUITest targets using XCUIApplication / XCUIElement / XCUIElementQuery, async waits via expectations and XCTNSPredicateExpectation, gesture APIs (tap / swipe / pinch / dragAndDrop), and launch arguments / environment for deterministic state
- accessibility_identifier_strategy: Design Swift-side accessibilityIdentifier taxonomy (screen.section.element), enforce via SwiftUI .accessibilityIdentifier() / UIKit isAccessibilityElement + accessibilityIdentifier, and verify with Accessibility Inspector and recorded UI hierarchy
- swift_page_object: Implement Page Object / Screen Object patterns in Swift around XCUIApplication, expose user-intent methods, isolate XCUIElementQuery chains, and reuse via test helpers and BaseScreen abstractions
- programmatic_screenshot: Capture screenshots via XCUIScreen.main.screenshot() / XCUIElement.screenshot() / XCUIScreenshotProviding, attach via XCTAttachment.lifetime = .keepAlways, and stitch device + screen + element captures for regression evidence
- fastlane_snapshot_pipeline: Configure fastlane snapshot (Snapfile, SnapshotHelper.swift, snapshot() calls in UI tests) for App Store screenshots across device matrix, languages, and orientations; combine with frameit for marketing frames
- status_bar_clean_capture: Use xcrun simctl status_bar override (time 9:41, full battery, wifi/cellular bars) before App Store captures to satisfy Apple's clean status-bar requirement
- xcodebuild_test_runner: Drive headless runs via xcodebuild test / test-without-building with -destination matrix, -resultBundlePath, -parallel-testing-enabled, and -only-testing / -skip-testing for sharding
- xcresult_parsing: Parse .xcresult bundles with xcresulttool (Xcode 16+ schema awareness, --legacy fallback), extract attachments / failure screenshots, and emit JUnit / CI-friendly reports
- ui_test_recording: Use Xcode UI Recording to bootstrap queries, then refactor recorded code into Page Objects and identifier-based locators (recordings are scaffolding, not the final test)
- ci_device_matrix: Wire XCUITest into Xcode Cloud, GitHub Actions (macos runners), Bitrise, or self-hosted runners with simulator pool management, derived data isolation, and result-bundle archiving
- device_farm_handoff: Route XCUITest .xctestrun bundles to BrowserStack App Automate / Sauce Labs Real Device Cloud / AWS Device Farm for real-device matrices when local simulator coverage is insufficient
- snapshot_testing_libraries: Optional integration with pointfreeco/swift-snapshot-testing for view-snapshot baselines distinct from XCUITest end-to-end screenshots; choose by scope (unit-of-UI vs full flow)
- privacy_manifest_for_test_targets: Declare PrivacyInfo.xcprivacy on the test target itself when it bundles SDKs with required-reason APIs; Apple aggregates app + SDK manifests and a missing test-bundle entry can block TestFlight builds

