# Agent Visual Loop — AI-Driven Native Screen Implementation, Debugging, and Capture

Reference for running an **agent-in-the-loop** workflow on native screens: the agent writes SwiftUI/Compose, builds, renders or captures the result, compares it against a target with a *numeric* oracle, and iterates under a bounded cap.

> Scope: iOS (SwiftUI/UIKit) and Android (Compose/Views) screen implementation, visual debugging, and screenshot capture **driven by a coding agent**. Use when the task is "build/fix this screen and confirm it actually looks right", not when authoring a test suite (→ `Voyager[ios]` / `Voyager` / `Radar`) or designing the visual direction (→ `Vision` / `Muse`).

---

## 0. The Loop Contract

```
SPECIFY → IMPLEMENT → BUILD → OBSERVE → SCORE → ADJUST ─┐
   ▲                                                     │
   └──────────────── (bounded: ≤ 3 passes) ──────────────┘
                              │
                     escalate to human
```

| Step | Requirement |
|------|-------------|
| `SPECIFY` | Target is a **named artifact**: a reference image, a token set, or an explicit numeric spec (spacing, type scale, colors). "Make it look nice" is not a loop input. |
| `IMPLEMENT` | One screen or one component per pass. Widening scope mid-loop destroys the score's meaning. |
| `BUILD` | Must succeed before OBSERVE. A stale binary silently scores the *previous* implementation. |
| `OBSERVE` | Accessibility tree first, pixels second (§1). |
| `SCORE` | A number, not a judgment (§4). The agent does not get to declare "close enough". |
| `ADJUST` | Change what the score implicates. Record what changed and the score delta. |
| Cap | **≤ 3 passes**, then hand to a human. Beyond that the loop reliably plateaus rather than converges. |

The iteration cap and the "agent declares close enough" failure it defends against are both reported from practice, not theory — see §7 and [The Swift Dev](https://www.theswift.dev/posts/give-your-coding-agent-eyes-screenshot-driven-swiftui-iteration/) · [twocentstudios](https://twocentstudios.com/2025/07/13/giving-claude-code-eyes-to-see-your-swiftui-views/).

---

## 1. Structure Before Pixels

**Rule: read the accessibility tree first; fall back to screenshot + coordinates only when the tree is insufficient.**

This is the operating principle of [`mobile-next/mobile-mcp`](https://github.com/mobile-next/mobile-mcp), which drives automation from "the native accessibility tree (no vision model, no image tokens), falling back to screenshots + coordinates only when needed."

| Question the agent is answering | Correct observation channel |
|---------------------------------|-----------------------------|
| "Is the button present / enabled / labeled correctly?" | Accessibility tree |
| "Did navigation land on the right screen?" | Accessibility tree |
| "What is the current state of this control?" | Accessibility tree |
| "Does the spacing / color / type match the design?" | Screenshot + numeric diff (§4) |
| "Why does this render blank?" | Screenshot **and** build log / Logcat |

Why it matters beyond cost: a tree query is deterministic and fails loudly; a coordinate tap derived from a screenshot silently drifts the moment layout shifts. Reserve coordinates for surfaces that expose no usable tree.

Consequence for implementation work: **accessibility identifiers are agent infrastructure, not just test infrastructure.** A screen with a complete identifier taxonomy is drivable by an agent; one without it forces the agent into pixel guessing. Taxonomy and per-framework assignment rules → `voyager/reference/ios-identifier-strategy.md`.

---

## 2. iOS Tool Layer

Pick the lowest-ceremony option that closes the loop for the task at hand.

| Layer | What it gives the agent | Prereq | Best for |
|-------|------------------------|--------|----------|
| **Xcode MCP server** (`xcrun mcpbridge`) | 20 tools incl. `RenderPreview` (returns an actual SwiftUI preview screenshot), `BuildProject`, `GetBuildLog`, `RunSomeTests`, `XcodeListNavigatorIssues`, `ExecuteSnippet` | Xcode **26.3+** running with the project open; enable **Settings → Intelligence → Model Context Protocol → Xcode Tools**; stdio transport | Fastest preview-level iteration when a developer already has Xcode open |
| **XcodeBuildMCP** | Standalone binary driving the `xcodebuild` CLI — build, test, simulator control, LLDB, UI automation, **no running Xcode required** | Node/binary install | Headless and CI-adjacent agent runs |
| **iOS Simulator MCP** | tap / type / swipe / screenshot / record / accessibility inspection against a booted simulator | Booted simulator | Driving a running app, not just previews |
| **`mobile-mcp`** | Unified iOS + Android surface (simulators, emulators, real devices) with a11y-tree-first observation | Node 20+, Xcode CLT, Android platform-tools; real iOS devices need go-ios + WebDriverAgent | Cross-platform parity work in one agent session |
| **Raw CLI** | `xcrun simctl io <UDID> screenshot out.png`, `recordVideo`, `status_bar override`, `ui appearance dark`, `ui content_size …` | Xcode CLT only | Zero-dependency capture, CI, Dynamic Type / dark-mode sweeps |

`RenderPreview` is the piece that changes the economics: it closes the visual feedback loop **without a simulator boot or a developer switching to the canvas**. Agents discover the target window via `XcodeListWindows` before operating. [rudrank.com](https://rudrank.com/exploring-xcode-using-mcp-tools-cursor-external-clients) · [Xcode 26.3 teardown](https://awesomeagents.ai/news/xcode-26-3-agentic-coding-teardown/)

Full `simctl` / `devicectl` / `xctrace` command surface → `reference/xcrun-cli.md`.

---

## 3. Android Tool Layer

| Capability | Where | Notes |
|-----------|-------|-------|
| **Agent Mode** | Android Studio (Otter 3 Feature Drop, 2026-01+) | Tools: deploy to device, take screenshots, inspect screen, read Logcat, interact via `adb shell input`, build + fix build errors, call configured MCP servers. Verifies by building, re-running, screenshotting, and checking Logcat. Some tools are permission-gated; changes require review/approve. |
| **Match UI to Target Image** | Compose Preview → right-click → *AI Actions* | Upload a reference design; the agent proposes code changes to close the gap. This is the built-in equivalent of the §0 loop for a single Composable. |
| **Generate Code From Screenshot** | Preview panel | Design mock → starting Compose implementation. Treat output as a scaffold, not a deliverable. |
| **Preview render-failure debugging** | Gemini in Android Studio | Analyzes the render error + code to find root cause. Faster than reading a stack trace by hand for `@Preview` failures. |
| **Journeys** | Android Studio | XML-defined test steps, run against local or remote devices. The test panel shows **per-step screenshots plus the model's stated reason for each action** — this makes an agent-driven flow auditable rather than opaque. |
| **Raw CLI** | `adb exec-out screencap -p > out.png`, `adb shell screenrecord`, `adb shell input`, `logcat` | Full surface → `reference/adb-cli.md` |

Sources: [Agent Mode docs](https://developer.android.com/studio/gemini/agent-mode) · [Otter 3 Feature Drop release notes](https://developer.android.com/studio/releases/past-releases/as-otter-3-feature-drop-release-notes) · [Generate UI with image attachments](https://developer.android.com/studio/gemini/generate-ui-with-images)

---

## 4. The Numeric Oracle

The agent must not be the judge of "matches the design". Give it a number.

```bash
# Absolute difference metric (lower is closer; 0 = identical)
magick compare -verbose -metric RMSE reference.png candidate.png null:

# Visual diff image for the human reviewer
magick compare reference.png candidate.png diff.png

# Dimension check — catches the whole class of "right pixels, wrong frame" errors
magick identify candidate.png

# Probe one pixel's RGB — resolves color-token disputes exactly
magick image.png -crop 1x1+200+300 txt:
```

Gate rules:

- **Set the threshold before the loop starts**, from the spec, not from whatever the first pass happened to score.
- **Mask dynamic regions** (clock, battery, signal, push banners, animated content) before comparing — otherwise the metric is noise and the threshold gets loosened to compensate.
- A pass that does not move the metric is not an improvement, regardless of how the diff "reads". Revert it.
- Report the metric per pass in the deliverable. A visual claim with no number attached is `UNVERIFIED`.

Technique attribution: [twocentstudios](https://twocentstudios.com/2025/07/13/giving-claude-code-eyes-to-see-your-swiftui-views/).

---

## 5. Screenshot-Test Substrate

The loop is far cheaper when a repeatable render already exists. Reuse the project's snapshot layer instead of booting a simulator per pass.

**iOS** — `pointfreeco/swift-snapshot-testing` in an isolated test target:

```bash
xcodebuild test -only-testing:"ViewSnapshotTests/ViewVerificationTests" -quiet
# → ViewSnapshotTests/__Snapshots__/ViewVerificationTests/<name>.1.png
```

**Android** — three tools, different jobs:

| Tool | Renders | Choose when |
|------|---------|-------------|
| **Paparazzi** (Cash App) | JVM, no device/emulator; single-frame; View system + Compose | Fast layout-level checks in unit-test CI |
| **Roborazzi** | JVM; multi-frame / interaction-driven; supports hardware-accelerated rendering | Elevation shadows, content that clips to bounds, or capturing across an interaction |
| **Compose Preview Screenshot Testing** (Google) | Generates screenshots directly from `@Preview` | Lowest setup: move `@Preview`s into the `screenshotTest` source set; `@Preview` parameters give you the variant matrix for free |
| **ComposablePreviewScanner** | — | Auto-generates screenshot tests from existing `@Preview`s for whichever library above you already use |

Sources: [Paparazzi vs Roborazzi vs Compose Preview comparison](https://medium.com/@natalia.kulbaka/comparing-snapshot-testing-libraries-paparazzi-roborazzi-compose-previews-screenshot-testing-b7c3b47f7f59) · [ComposablePreviewScanner](https://github.com/sergio-sastre/ComposablePreviewScanner)

---

## 6. Authoring for Agent-Readiness

Changes to the *implementation* that make the loop work. These are the highest-leverage edits and they belong in the feature code, not in a test helper.

- **Named previews per state.** `@Preview("Loading")`, `@Preview("Empty")`, `@Preview("Error")`, `@Preview("Long content — ja")`. The agent can only render states that have an entry point.
- **Seeded debug state.** A deterministic fixture behind a debug flag, so pass N and pass N+1 render the same data. Live/network data makes every diff meaningless.
- **Complete accessibility identifiers.** See §1 — this is what lets the agent verify by structure instead of guessing coordinates.
- **Temporary tuning controls.** A debug-only slider/stepper bound to the value under adjustment (padding, corner radius, opacity) lets a human converge in seconds and hand the agent a final number. Remove before merge.
- **Dark mode + Dynamic Type previews** for any screen with a contrast or truncation risk: `xcrun simctl ui <UDID> appearance dark`, `… content_size extra-extra-extra-large`.

---

## 7. Documented Failure Modes

Observed in practice; treat each as a standing guard, not a hypothetical.

| Failure | Shape | Guard |
|---------|-------|-------|
| **Premature satisfaction** | The agent judges its output "close enough" after nearly every pass | Numeric gate (§4) + explicit pass cap. Never let the producer own the accept decision. |
| **System-default drift** | Even given a reference image, the agent falls back to system fonts and system colors unless told otherwise | Front-load the token set (font family, weights, exact hex/token names) in the spec. State it as a constraint, not a hint. |
| **Relative-size blindness** | Padding and sizing deltas are perceived poorly from an image | Express spacing as explicit numbers in the spec; verify with `magick identify` and pixel probes rather than "does it look tighter". |
| **Chrome invisibility** | Snapshot tests cannot capture system UI (status bar, Dynamic Island, home indicator) | Verify anything that interacts with system chrome on a booted simulator/device, not from snapshots. |
| **Suite-granularity trap** | Swift Testing's `-only-testing:` resolves to suites, not individual tests | Isolate the verification test in its own suite so a pass runs one render, not the whole file. |
| **Stale-binary scoring** | OBSERVE runs against the previous build | Make BUILD success a hard precondition for OBSERVE; never score on a cached artifact. |
| **Scope creep mid-loop** | The agent "improves" adjacent views while iterating | One screen per loop; a scope bound on every pass. |

---

## 8. Cross-References

- `reference/xcrun-cli.md` — full `simctl` / `devicectl` / `xctrace` / `xcresulttool` surface, status-bar override, recording recipes.
- `reference/adb-cli.md` — full `adb` surface, screencap / screenrecord / input / Perfetto.
- `reference/patterns.md` — where snapshot tooling sits in the overall per-platform test matrix.
- `voyager/reference/ios-identifier-strategy.md` — accessibility identifier taxonomy (the §1 prerequisite) and per-framework assignment rules.
- `voyager/reference/ios-screenshot-strategies.md` — XCUITest capture APIs, `XCTAttachment` lifetime, App Store screenshot pipelines.
- `voyager/reference/ai-powered-e2e-testing.md` — AI-assisted **test authoring** and self-healing, including the native-mobile tool matrix. This file is about implementation; that file is about the suite.
- `pixel/reference/visual-verification.md` — the equivalent numeric-verification discipline for web mockup reproduction.
