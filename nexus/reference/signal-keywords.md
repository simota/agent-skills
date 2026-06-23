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
| `charter`, `instruction document`, `team charter`, `team operating manual`, `runbook for a team`, `analyze repo and design a team`, `self-driving team charter`, `team design spec`, `comprehensive repo analysis to a plan` | `charter` |
| `enact`, `run the charter`, `execute the charter`, `execute the instruction document`, `build team from charter and run`, `orchestrate the charter`, `run docs/CHARTER.md` | `enact` |
| `goal`, `/goal setup`, `goal recipe`, `long-running goal`, `autonomous loop setup` | `goal` |
| `gedanken`, `thought experiment`, `what if`, `reason through`, `counterfactual`, `limiting case`, `reductio ad absurdum`, `intuition pump`, `steelman scenario`, `hypothetically`, `思考実験`, `もし〜だったら`, `反実仮想` | `gedanken` (structured thought-experiment reasoning — construct a hypothetical → reason from independent lenses → perturb under controlled variation → adversarially refute → conclude with a falsifier; **no code**. Exploratory-reasoning analog of `magi` (which *decides*); orchestrates `flux`/`magi`/`omen`/`matrix`. Trivial one-off "what if" → `flux`/`magi` direct) |
| `spec`, `spec out`, `spec this out`, `flesh out the spec`, `nail down the requirements`, `write the spec with me`, `talk through a feature`, `refine until the spec is locked`, `idea to spec`, `finalize the spec`, `requirements through dialogue`, `機能を相談して仕様にしたい`, `仕様を固める`, `対話で仕様を詰める` | `spec` (interactive feature-proposal → locked spec via deep dialogue; INTERACTIVE default; stops at the spec, no code; hands off to `feature`/`apex`. Distinct from `essential`/`killer` which deliver a *which-feature verdict* with minimal dialogue, and from `feature`/`apex` which *build*) |
| `essential`, `must-have`, `MVP definition`, `core feature`, `minimum viable`, `cut scope`, `bare minimum` | `essential` |
| `killer`, `killer feature`, `differentiator`, `WOW experience`, `decisive feature`, `competitive edge` | `killer` |
| `trim`, `remove feature`, `dead weight`, `dead-weight feature`, `cut unused feature`, `feature sunset`, `retire feature`, `delete what we don't need`, `prune features`, `kill unused feature` | `trim` (inverse of essential/killer — removal via essential×killer 2-axis filter; core engine `void`) |
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
| `attribution`, `multi-touch attribution`, `MTA`, `Shapley value`, `Markov attribution`, `data-driven attribution`, `DDA`, `touchpoint credit` | `ATTRIBUTION_MODELING` (Pulse). Don't confuse with MMM / incrementality (Experiment) |
| `value proposition canvas`, `VPC`, `jobs pains gains`, `pain relievers`, `gain creators`, `problem-solution fit` | `VALUE_PROP_CANVAS` (Spark) |
| `business model canvas`, `BMC`, `lean canvas`, `business model design`, `9 building blocks` | `BUSINESS_MODEL_CANVAS` (Helm) |
| `PQL`, `product-qualified lead`, `PQA`, `product-qualified account`, `PLG conversion signal` | `PQL_MODELING` (Pulse) |
| `Fogg behavior model`, `B=MAP`, `behavior design`, `tiny habits`, `motivation ability prompt` | `BEHAVIOR_DESIGN` (Bond — `habit-formation.md`) |
| `pillar-cluster`, `topic cluster`, `content architecture`, `keyword cannibalization`, `internal linking strategy` | `CONTENT_ARCHITECTURE` (Growth) |
| `Bullseye`, `19 traction channels`, `channel selection`, `See-Think-Do-Care`, `RACE planning`, `lifecycle marketing plan` | `CHANNEL_LIFECYCLE` (Growth) |
| `CBBE`, `brand equity`, `Keller pyramid`, `brand salience`, `brand resonance`, `brand strength` | `BRAND_EQUITY` (Compete — `brand-equity.md`) |
| `pre-mortem`, `premortem`, `FMEA`, `failure modes`, `RPN`, `AP`, `failure scenario enumeration`, `what could go wrong` | `PREMORTEM` (Omen → Ripple) |
| `manual QA`, `TestRail`, `Xray`, `Zephyr`, `Qase`, `BVA`, `equivalence class`, `decision table`, `exploratory charter`, `manual test procedure` | `MANUAL_QA` (Drill) |
| `test pyramid`, `trophy`, `honeycomb`, `coverage heatmap`, `flake dashboard`, `Wilson lower-bound`, `mutation overlay`, `test shape` | `TEST_INTELLIGENCE` (Vista) |
| `feature inventory`, `unimplemented features`, `what's built`, `what's left`, `roadmap status`, `WBS`, `work breakdown`, `delivery status`, `project status`, `is X shipped`, `plan vs code`, `docs-vs-code drift` | `PROJECT_STATUS` (PDM). Don't confuse with PROJECT (Titan lifecycle), PRIORITIZE (Rank), SPEC_VERIFY (Attest), INVESTIGATE (Lens) |
| `positioning`, `positioning statement`, `messaging`, `messaging house`, `value proposition`, `go-to-market`, `GTM`, `launch plan`, `launch marketing`, `sales enablement`, `one-pager`, `ポジショニング`, `メッセージング`, `市場投入`, `ローンチ計画` | `GO_TO_MARKET` (PMM). Markets *shipped* capability; don't confuse with PROJECT_STATUS (PDM what's built), competitive research (Compete), narrative craft (Saga), landing-page build (Funnel), technical release (Launch) |
| `AppleScript`, `osascript`, `JXA`, `JavaScript for Automation`, `Apple Events`, `macOS automation`, `Mac desktop automation`, `app control`, `tell application`, `UI scripting`, `System Events`, `sdef`, `scripting dictionary` | `MACOS_AUTOMATION` (Wield). Note: Automator *workflow* authoring is out of scope; only the "Run AppleScript" action within Automator falls under Wield |

---

## Mobile Native Anchors

| Keywords | Recipe |
|----------|--------|
| `iOS`, `iOS implementation`, `iPhone`, `iPad`, `Swift`, `SwiftUI`, `Swift 6.2`, `Liquid Glass`, `iOS 26`, `@Observable`, `SwiftData`, `Xcode`, `App Store`, `TestFlight`, `xcrun`, `simctl`, `devicectl`, `xctrace`, `WidgetKit`, `Live Activities`, `App Intents`, `ASAuthorizationController`, `Apple Intelligence`, `Foundation Models` | `MOBILE_NATIVE` (Native) — iOS path |
| `Android`, `Android implementation`, `Kotlin`, `Jetpack Compose`, `Material 3 Expressive`, `M3 Expressive`, `Compose Multiplatform`, `Strong Skipping`, `Type-safe Navigation`, `Gradle`, `KSP`, `Android Gradle Plugin`, `AGP`, `Play Store`, `Play Console`, `adb`, `logcat`, `dumpsys`, `WorkManager`, `Credential Manager`, `Jetpack Glance`, `Gemini Nano`, `AICore` | `MOBILE_NATIVE` (Native) — Android path |
| `native app`, `native implementation`, `mobile app implementation`, `both iOS and Android`, `mobile native`, `pure native`, `Passkey mobile`, `Privacy Manifest`, `Data Safety form`, `Universal Links`, `App Links`, `App Bundle`, `staged rollout`, `phased release` | `MOBILE_NATIVE` (Native) — cross-platform / shared mobile |
| `XCUITest`, `XCUIApplication`, `XCUIElement`, `XCUIElementQuery`, `accessibilityIdentifier`, `fastlane snapshot`, `Snapfile`, `SnapshotHelper`, `App Store screenshot`, `frameit`, `xcresulttool`, `xcodebuild test`, `.xctestrun`, `iOS UI test`, `swift ui test`, `status bar override`, `simctl status_bar` | `IOS_UI_TEST` (Snap) |
| `Web to iOS`, `Web to Android`, `Web to native`, `port to iOS`, `port to Android`, `feature parity matrix`, `nativize`, `porting design`, `Strangler Fig mobile` | `PORTING` (Port → Native) |
| `UI terminology mapping`, `Web vs iOS vs Android UI`, `cross-platform UI naming`, `what is this component called on iOS/Android`, `HIG Material equivalent`, `compare UI parts across platforms`, `equivalent component`, `UI parity implementation` | `PORTING` (Port) — read `port/reference/ui-terminology-matrix.md` for the Web ↔ iOS (HIG) ↔ Android (Material 3) component-name matrix before per-screen specs / handoff |

---

## Loop, Migration & Reproduction Anchors

Loop-control, change-completeness, cross-language, and product-reproduction/synthesis recipes (previously misfiled under Mobile Native).

| Keywords | Recipe |
|----------|--------|
| `converge`, `iterate to rubric`, `generator-evaluator`, `evaluator loop`, `quality loop`, `iterate until accept`, `loop until it passes`, `converge to a quality bar` | `converge` (standalone, or `converge <recipe>` wrapping a generator; flatten rule for loop-recipes) |
| `migrate`, `migrate everything`, `change without omission`, `もれなく`, `architecture change`, `framework migration`, `framework change`, `middleware swap`, `middleware change`, `mock to production`, `mock to prod`, `stub to real`, `change completeness`, `migrate the whole codebase` | `migrate` (case = arch \| framework \| middleware \| mock-to-prod; `case=lang` → `transmute`) |
| `transmute`, `rewrite in`, `port to Rust`, `TS to Rust`, `Go to Rust`, `Python to Go`, `JS to TS`, `language rewrite`, `cross-language`, `rewrite in another language`, `idiomatic rewrite`, `differential parity` | `transmute` |
| `clone`, `replicate`, `copy this product`, `clone this product`, `faithful copy`, `complete copy`, `reproduce the product`, `rebuild like <product>`, `make a copy of <product>`, `pixel-perfect clone`, `1:1 copy`, `clone this desktop app`, `copy this desktop application`, `reproduce this app` | `clone` (faithful reproduction of an external product, parity-verified; black-box analog of `transmute`. Platform-agnostic — `target_type` web \| **desktop** (macOS/Win/Linux GUI) \| mobile \| has-source \| api. `replicate` is an alias. **Bare `trace` deliberately excluded** — it routes to the `Trace` session-replay skill, not here; use `clone`/`replicate` for product copying) |
| `fuse`, `synthesize`, `combine two products`, `combine A and B`, `merge A and B into one`, `mashup of <X> and <Y>`, `blend products`, `hybrid of X and Y`, `take A's <feature> and B's <feature>`, `best of both products`, `make one product out of two`, `fuse these apps` | `fuse` (multi-source synthesis — clone's extension. Capture **≥2** products and synthesize into **one new** product: adopt/merge/net-new per element via a **Fusion Map**, verified by a **dual oracle** (adopted→parity-vs-source ‖ merged/net-new→spec-AC) + **Coherence Gate**. `sources=2..N`, mixed `target_type`. **Single source / faithful copy → `clone`; net-new only inspired → `feature`/`apex`.** Confirm big-bang or sources ≥ 3) |
| `graft`, `mix in a concept`, `mixin <X>'s concept`, `bring <X>'s concept into our product`, `apply <X>'s paradigm to our app`, `innovate by borrowing from <X>`, `transplant a concept`, `inject <X>'s idea into our product`, `make our product innovative with <X>'s approach`, `borrow the principle behind <X>` | `graft` (concept transplant for innovation — fuse's extension, clone's fidelity-inverse. Owned **host** + **donor**; transplant the donor's **concept** (principle/mechanism, **not** surface) onto the host → **innovation**. Triple oracle: concept-fidelity ∧ host-integrity (regression net) ∧ **Innovation Gate** (emergence + refutation + felt-novelty). `host=1, donors=1..N`. **Rejects surface copying — faithful surface reproduction → `clone`; peer-source surface synthesis → `fuse`; net-new feature, no donor concept → `feature`.** Confirm if invasive to host core / no flag) |

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
