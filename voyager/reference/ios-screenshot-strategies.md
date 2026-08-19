# Screenshot Strategies

Purpose: Capture programmatic screenshots during XCUITest runs as regression evidence. Covers `XCUIScreen` / `XCUIElement` / `XCUIScreenshotProviding` capture APIs, `XCTAttachment` lifetime settings, per-failure vs checkpoint capture patterns, and where XCUITest screenshots stop and a real visual-baseline tool starts.

Contents:
- Capture APIs: `XCUIScreen`, `XCUIElement`, `XCUIScreenshotProviding`
- `XCTAttachment` and `.lifetime`
- Per-failure capture (automatic evidence)
- Checkpoint capture (opt-in, key steps)
- Screen vs element vs multi-capture stitching
- `swift-snapshot-testing` distinction
- Anti-patterns

## Capture APIs

Three capture surfaces, each with a different scope:

```swift
// Whole physical screen (includes status bar, all apps' windows in split-screen scenarios)
let screenshot = XCUIScreen.main.screenshot()

// A single element's rendered bounds — tighter, deterministic crop
let elementShot = app.otherElements["checkout.summary.card"].screenshot()

// Custom capture source conforming to XCUIScreenshotProviding — for content
// that needs app-side coordination before a screenshot is meaningful
// (e.g. waiting for an animation-free frame, or capturing off-screen content).
struct StableFrameProvider: XCUIScreenshotProviding {
    var snapshotBounds: CGRect = .zero
    func createScreenshotImage() throws -> UIImage { /* ... */ }
}
```

- `XCUIScreen.main.screenshot()` — use for full-context evidence (what the user actually saw, including system chrome). Default for failure attachments.
- `element.screenshot()` — use when the assertion is about one component's rendered state (a chart, a custom control) and cropping out the rest of the screen makes the diff more legible for a human reviewer.
- `XCUIScreenshotProviding` — reserve for advanced cases: custom rendering surfaces (Metal/SceneKit views) or content that needs an app-side hook to stabilize before capture. Most suites never need this.

## `XCTAttachment` And `.lifetime`

```swift
func attachScreenshot(named name: String, of element: XCUIElement? = nil, keepAlways: Bool = false) {
    let screenshot = element?.screenshot() ?? XCUIScreen.main.screenshot()
    let attachment = XCTAttachment(screenshot: screenshot)
    attachment.name = name
    attachment.lifetime = keepAlways ? .keepAlways : .deleteOnSuccess
    add(attachment)
}
```

| `.lifetime` | Behavior | Use for |
|-------------|----------|---------|
| `.deleteOnSuccess` (default) | Discarded if the test passes; kept only on failure | Routine checkpoint captures — no need to bloat `.xcresult` on green runs |
| `.keepAlways` | Retained regardless of pass/fail | Failure diagnostics you always want archived, and App Store screenshot captures (the artifact *is* the point) |

- Set `.lifetime` explicitly rather than relying on the default — a reviewer scanning `.xcresult` for failure evidence should never wonder whether a missing screenshot means "not captured" or "discarded because it passed."
- Name attachments descriptively and include the step (`"02_after_submit_tap"`), not a bare counter — `xcresulttool` output and CI artifact browsers list attachments by name.

## Per-Failure Capture (Automatic Evidence)

Wire capture into a shared `XCTestObservation` or a `tearDown` hook so every test gets a failure screenshot without per-test boilerplate:

```swift
final class ScreenshotOnFailureObserver: NSObject, XCTestObservation {
    func testCase(_ testCase: XCTestCase, didFailWithDescription description: String, inFile filePath: String?, atLine lineNumber: Int) {
        let screenshot = XCUIScreen.main.screenshot()
        let attachment = XCTAttachment(screenshot: screenshot)
        attachment.name = "failure-\(testCase.name)"
        attachment.lifetime = .keepAlways
        testCase.add(attachment)
    }
}

// Register once, e.g. in a shared test base class's setUp:
XCTestObservationCenter.shared.addTestObserver(ScreenshotOnFailureObserver())
```

- This is evidence for triage, not a test assertion. Never gate `XCTAssert` on the screenshot's pixel content inside this path.
- Always `.keepAlways` for failure captures — a failed run is exactly the case a reviewer needs the artifact preserved.

## Checkpoint Capture (Opt-In)

Capture at specific steps in a long or high-risk flow (checkout, onboarding) to give reviewers a visual trail even on passing runs — used sparingly, since every checkpoint adds `.xcresult` size and capture latency.

```swift
func testCheckoutFlow() throws {
    let checkout = CheckoutScreen(app: app)
    attachScreenshot(named: "01_cart_summary")

    checkout.applyPromoCode("SAVE10")
    attachScreenshot(named: "02_promo_applied")

    checkout.confirmPurchase()
    attachScreenshot(named: "03_confirmation", keepAlways: true)
}
```

- Reserve checkpoint captures for flows where a human regularly reviews the visual trail (release-gate smoke tests, App Store submission dry-runs) — not for every PR-blocking unit-of-flow test.
- Default checkpoint attachments to `.deleteOnSuccess`; reserve `.keepAlways` for the final/critical step reviewers always want.

## Screen Vs Element Vs Multi-Capture Stitching

For a single evidence bundle that shows device chrome, the specific failing region, and a targeted element together:

```swift
func attachDiagnosticBundle(for element: XCUIElement, testCase: XCTestCase) {
    let device = XCTAttachment(screenshot: XCUIScreen.main.screenshot())
    device.name = "device-full"
    device.lifetime = .keepAlways
    testCase.add(device)

    let component = XCTAttachment(screenshot: element.screenshot())
    component.name = "element-\(element.identifier)"
    component.lifetime = .keepAlways
    testCase.add(component)
}
```

Both attachments land in the same `.xcresult` under the same test — `xcresulttool` extracts them independently by attachment reference (see `reference/ci-integration.md`).

## `swift-snapshot-testing` Distinction

XCUITest screenshots are **evidence**, not **baselines**. They confirm "here is what the screen looked like when this assertion failed" — they do not gate a test on pixel-perfect comparison against a golden image.

| Concern | XCUITest `XCTAttachment` | `pointfreeco/swift-snapshot-testing` |
|---------|---------------------------|----------------------------------------|
| Scope | Full end-to-end flow, real simulator/device | Single view/component in isolation (unit-of-UI) |
| Assertion | None — attachment is diagnostic only | Pixel/reference-image diff is the assertion |
| Speed | Slower (full app boot, real navigation) | Fast (renders a view controller/SwiftUI view directly) |
| Baseline storage | N/A | Reference images committed to the repo (or LFS) |
| Failure signal | Test fails for a behavioral reason; screenshot explains why | Test fails *because* the rendered output changed |

- If the ask is "assert this view didn't visually regress," that is `swift-snapshot-testing` (or a downstream visual-AI vendor like Applitools/Percy) — not a `XCTAttachment` pixel-diff bolted onto XCUITest.
- If the ask is "prove this end-to-end flow reached the expected state, with visual evidence for a human reviewer," that is the `XCTAttachment` pattern in this file.
- Both can coexist in the same app: `swift-snapshot-testing` at the unit-test tier for component baselines, XCUITest `XCTAttachment` at the UI-test tier for flow evidence.

## Anti-Patterns

- Asserting on screenshot pixel data inside an XCUITest (`XCTAssertEqual(screenshot.pngData(), goldenData)`) — flaky across simulator OS versions, font rendering, and Dynamic Type settings. Route real pixel-diff needs to `swift-snapshot-testing`.
- `.keepAlways` on every checkpoint in every test — bloats `.xcresult` size and CI artifact upload time for no reviewer benefit on green runs.
- Capturing only on failure and never at checkpoints for a release-gate smoke suite that a human is expected to visually spot-check — checkpoint captures are the intended trail there.
- Committing screenshot output (`Voyager[ios]shot.images/`, ad-hoc `.png` dumps) to the main branch — route to an artifact store or a dedicated screenshot branch (see `reference/fastlane-snapshot.md`).

## Agent-Driven Capture (Distinct Third Mode)

A coding agent iterating on a screen is a third consumer of screenshots, and it wants neither of the two modes above: not flow evidence, not a committed baseline, but a **throwaway render scored against a target**.

- Do not route agent iteration through this file's `XCTAttachment` pattern — the capture is not diagnostic evidence of a failing assertion, and it should never land in `.xcresult`.
- Preferred substrates are `swift-snapshot-testing` (fast, no boot), `xcrun simctl io <UDID> screenshot`, or an MCP tool that renders the SwiftUI preview directly (Xcode 26.3+ `RenderPreview`).
- The agent's accept decision must come from a numeric diff, not its own reading of the image.

Full loop contract, tool-layer selection, and documented failure modes → `native/reference/agent-visual-loop.md`.

## Cross-References

- `reference/fastlane-snapshot.md` — the App Store screenshot pipeline that reuses this file's capture APIs inside dedicated `snapshot()` calls.
- `reference/ci-integration.md` — extracting attached screenshots from `.xcresult` via `xcresulttool` in CI.
- `native/reference/agent-visual-loop.md` — agent-in-the-loop screen implementation and visual debugging; consumes this skill's identifier taxonomy as its structural observation channel.
