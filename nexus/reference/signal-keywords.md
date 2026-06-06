# Signal Keywords → Recipe (full table)

**Purpose:** Natural-language keyword → Recipe mapping for CLASSIFY when no explicit subcommand is provided. SKILL.md keeps only the most-used recipes inline; this file is the canonical full table.

**Read when:** Classifying ambiguous user input that did not match a known subcommand and may need keyword-based routing.

**Disambiguation rule:** Subcommand match (first token of user input) ALWAYS wins over keyword match.

**Language rule:** Keywords are **English canonical anchors**, not a literal allowlist. Nexus absorbs language and phrasing at CLASSIFY — input in any language (Japanese, etc.) or paraphrased wording is semantically mapped to the matching Recipe by intent, not string match. Translate the user's request to its English intent first, then match. The output-language config still governs the user-facing response.

---

## Core Recipe Anchors

| Keywords | Recipe |
|----------|--------|
| `bug`, `error`, `broken` | `bug` |
| `feature`, `implement`, `build` | `feature` |
| `security`, `vulnerability`, `CVE` | `security` |
| `refactor`, `clean up`, `code smell` | `refactor` |
| `optimize`, `slow`, `performance` | `optimize` |
| `kaizen`, `improve`, `polish`, `enhance existing`, `incremental improvement`, `refine`, `continuous improvement` | `kaizen` |
| `review`, `check`, `audit` | (legacy quality review via `routing-matrix.md`) |
| `design system docs`, `token docs`, `component catalog` | `DESIGN_SYSTEM_DOCS` (see Routing Quick Start) |
| `brainstorm`, `bounce ideas`, `riff`, `ideate`, `sounding board` | (Riff direct — single-agent) |
| `apex`, `auto-impl`, `full implementation`, `discovery to launch`, `end-to-end feature`, `ultimate` | `apex` |
| `goal`, `/goal setup`, `goal recipe`, `long-running goal`, `autonomous loop setup` | `goal` |
| `essential`, `must-have`, `MVP definition`, `core feature`, `minimum viable`, `cut scope`, `bare minimum` | `essential` |
| `killer`, `killer feature`, `differentiator`, `WOW experience`, `decisive feature`, `competitive edge` | `killer` |
| `acceptance`, `proof-carrying PR`, `acceptance gate`, `machine-adjudicated merge`, `tier-s merge`, `payment merge`, `auth merge`, `auto-merge with evidence` | `acceptance` |
| `growth-acceptance`, `lifecycle gate`, `market proof`, `research proof`, `brand proof`, `insight ledger`, `incrementality gate`, `brand compiler`, `growth-brand contract`, `post-launch measurement` | `growth-acceptance` |
| `summit`, `tri-engine`, `all engines`, `claude+codex+agy`, `quality maximization`, `strategic decision`, `release-critical`, `design-critical launch` | `summit` |
| `podium`, `slide deck`, `keynote`, `conference talk`, `presentation`, `talk deck`, `speaker deck`, `onboarding kit (doc + deck)`, `learning material with companion deck`, `doc + slide`, `unified content package`, `article + slides`, `retrospective (doc + exec deck)`, `launch package (announcement + sales deck)` | `podium` |
| `/Nexus` (no arguments) | `proactive` |

---

## Specialist Skill Anchors

| Keywords | Recipe / Skill |
|----------|----------------|
| `skill audit`, `MCP supply chain`, `plugin intake`, `.claude config audit`, `Unicode Tag injection`, `curl-pipe scan`, `third-party intake` | `SUPPLY_CHAIN_AUDIT` (Chain) |
| `Shai-Hulud`, `npm worm`, `PyPI worm`, `lottie-player`, `S1ngularity`, `infected lockfile`, `C2 traffic`, `credential rotation order`, `infected` | `MALWARE_RESPONSE` (Cull → Triage → Crypt) |
| `auto-tune`, `continuous tuning`, `GC tuning`, `threadpool`, `connection pool`, `worker count`, `cache size auto-adjust` | `AUTO_TUNING` (Dial) |
| `tech debt visualization`, `debt mascot`, `debt character`, `gamified retro`, `quarterly debt review` | `DEBT_VISUALIZATION` (Hex → Sketch) |
| `audio analysis`, `LUFS`, `True Peak`, `BPM detect`, `key detect`, `mastering QC`, `EBU R128`, `librosa`, `pyloudnorm` | `AUDIO_ANALYSIS` (Sonar) |
| `ToS`, `Terms of Service`, `Privacy Policy`, `Tokushoho`, `Specified Commercial Transactions Act`, `terms review`, `policy gap` | `LEGAL_REVIEW` (Clause → Scribe) |
| `ICE`, `RICE`, `WSJF`, `MoSCoW`, `Kano`, `Cost of Delay`, `priority`, `prioritize`, `ranking` | `PRIORITIZE` (Rank → Magi) |
| `pre-mortem`, `premortem`, `FMEA`, `failure modes`, `RPN`, `AP`, `failure scenario enumeration`, `what could go wrong` | `PREMORTEM` (Omen → Ripple) |
| `manual QA`, `TestRail`, `Xray`, `Zephyr`, `Qase`, `BVA`, `equivalence class`, `decision table`, `exploratory charter`, `manual test procedure` | `MANUAL_QA` (Drill) |
| `test pyramid`, `trophy`, `honeycomb`, `coverage heatmap`, `flake dashboard`, `Wilson lower-bound`, `mutation overlay`, `test shape` | `TEST_INTELLIGENCE` (Vista) |

---

## Mobile Native Anchors

| Keywords | Recipe |
|----------|--------|
| `iOS`, `iOS implementation`, `iPhone`, `iPad`, `Swift`, `SwiftUI`, `Swift 6.2`, `Liquid Glass`, `iOS 26`, `@Observable`, `SwiftData`, `Xcode`, `App Store`, `TestFlight`, `xcrun`, `simctl`, `devicectl`, `xctrace`, `WidgetKit`, `Live Activities`, `App Intents`, `ASAuthorizationController`, `Apple Intelligence`, `Foundation Models` | `MOBILE_NATIVE` (Native) — iOS path |
| `Android`, `Android implementation`, `Kotlin`, `Jetpack Compose`, `Material 3 Expressive`, `M3 Expressive`, `Compose Multiplatform`, `Strong Skipping`, `Type-safe Navigation`, `Gradle`, `KSP`, `Android Gradle Plugin`, `AGP`, `Play Store`, `Play Console`, `adb`, `logcat`, `dumpsys`, `WorkManager`, `Credential Manager`, `Jetpack Glance`, `Gemini Nano`, `AICore` | `MOBILE_NATIVE` (Native) — Android path |
| `native app`, `native implementation`, `mobile app implementation`, `both iOS and Android`, `mobile native`, `pure native`, `Passkey mobile`, `Privacy Manifest`, `Data Safety form`, `Universal Links`, `App Links`, `App Bundle`, `staged rollout`, `phased release` | `MOBILE_NATIVE` (Native) — cross-platform / shared mobile |
| `XCUITest`, `XCUIApplication`, `XCUIElement`, `XCUIElementQuery`, `accessibilityIdentifier`, `fastlane snapshot`, `Snapfile`, `SnapshotHelper`, `App Store screenshot`, `frameit`, `xcresulttool`, `xcodebuild test`, `.xctestrun`, `iOS UI test`, `swift ui test`, `status bar override`, `simctl status_bar` | `IOS_UI_TEST` (Snap) |
| `Web to iOS`, `Web to Android`, `Web to native`, `port to iOS`, `port to Android`, `feature parity matrix`, `nativize`, `porting design`, `Strangler Fig mobile` | `PORTING` (Port → Native) |
| `transmute`, `rewrite in`, `port to Rust`, `TS to Rust`, `Go to Rust`, `Python to Go`, `JS to TS`, `language rewrite`, `cross-language`, `rewrite in another language`, `idiomatic rewrite`, `differential parity` | `transmute` |

---

## Package / Domain Anchors

| Keywords | Recipe |
|----------|--------|
| `venture`, `business plan`, `business documentation package`, `MVP dossier`, `startup dossier`, `pitch package`, `business-prep package`, `investor material bundle`, `business idea to docs`, `comprehensive product docs` | `venture` (= `package domain=startup`) |
| `package`, `document package`, `documentation package`, `generate a full package`, `project package`, `generic project docs` | `package` (auto-detect preset) |
| `research package`, `research plan package`, `literature review package`, `study design`, `methodology + analysis plan` | `package domain=research` |
| `AI adoption package`, `AI rollout plan`, `RAG plan`, `prompt library`, `AI governance package`, `internal AI enablement` | `package domain=ai-adoption` |
| `legal package`, `compliance package`, `policy pack`, `ToS + privacy + AI policy drafts`, `legal risk register` | `package domain=legal` |
| `SaaS package`, `SaaS productization docs`, `AI product platform docs` | `package domain=saas` |
| `media package`, `content operations kit`, `editorial calendar package`, `channel + monetization plan` | `package domain=media` |
| `growth package`, `growth experiment plan`, `funnel + A/B plan package`, `growth hypotheses package` | `package domain=growth` (planning-only; execution → `kaizen`) |
| `career package`, `job-change plan`, `career strategy package`, `portfolio + interview + negotiation kit` | `package domain=career` (owner skill `ascent`) |
| `learning package`, `curriculum package`, `course design package`, `training program docs` | `package domain=learning` (owner skill `agora`) |
| `hiring package`, `recruitment package`, `JD + interview + onboarding kit`, `org design docs` | `package domain=hiring` (owner skill `guild`) |

---

## Fallback

| Keywords | Recipe |
|----------|--------|
| unclear or multi-domain request | `classify` → `reference/intent-clarification.md` |
