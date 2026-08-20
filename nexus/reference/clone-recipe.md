# Clone Recipe — Faithful Product Reproduction

> `/nexus clone` — reproduce an existing product **completely and faithfully** by reverse-engineering its observable surface (UI / behavior / features / data shape), synthesizing a reconstruction spec, rebuilding it, and **verifying the copy against the original by differential parity** — not by assertion.

Read this file before executing the `clone` Recipe. Phase contracts, the **Phase 0.1 interactive Stack Dialogue** (§3·0), the Parity Map, capture-strategy selection, and failure escalation are defined here. The **Phase 0.5 web research sweep** that grounds fidelity before capture is specified in `reference/research-grounding.md`.

> **Naming note.** The Recipe subcommand `clone` (alias `replicate`) is distinct from the **`Trace` skill** (session-replay analysis) that this Recipe *spawns* in Phase 1. "Clone the product" = the Recipe; "Trace skill" = one capture tool inside it. Bare `trace` deliberately does **not** route to this Recipe (it reaches the Trace skill) — do not conflate them.

---

## 1. When to Use / Boundaries

Use `clone` to **reproduce a whole product (or a self-contained product area) faithfully** from its observable surface — a legacy product being rebuilt on a new stack, an authorized reference implementation, a design you own, or an internal app whose source is lost. The defining trait: the target is treated as a **black box (or grey box)** — fidelity is *measured* against the original, not assumed.

**Target platforms.** clone is **platform-agnostic on the observable surface** — `target_type` ∈ { **live-web**, **desktop** (macOS / Windows / Linux GUI app), **mobile** (native iOS/Android), **has-source**, **api-backed** }. The four Parity dimensions (visual / behavioral / feature / data) and the fidelity-over-faith principle are identical across platforms; only the **capture mechanism** changes (§2). Web and desktop are first-class peers — a desktop app's windows, menus, dialogs, and keyboard/pointer flows are captured and parity-verified the same way web screens/states are. For a desktop target the "screen" unit is a window/view/dialog state and the navigation graph spans menus, modals, and OS-level interactions.

| Not this | Route to | Why |
|----------|----------|-----|
| Cross-language rewrite of **your own source** (TS→Rust) | `transmute` | White-box; parity oracle extracted *from* the source, not observed externally |
| Same-system arch / framework / middleware / mock→prod sweep | `migrate` | Change-completeness on an existing codebase, no external target to reproduce |
| Web → iOS/Android native reproduction | `PORTING` (Port→Native) | Platform paradigm shift, native parity rules |
| Pixel-accurate **single mockup/screenshot** → code | `pixel` (skill direct) | One image, no product-wide feature/behavior capture or parity loop |
| New product *inspired by* a reference (not a faithful copy) | `feature` / `apex` | Net-new design, no parity baseline to converge against |
| Extract design context from a Figma file | `frame` (skill direct) | Single-source design extraction, no full-product rebuild + verify |

**Three non-negotiable principles:**
0. **Reproduce only what you are entitled to reproduce.** Every run declares an **authorization basis** before capture begins (§3·0b). clone is built for legacy rebuilds, authorized reference implementations, designs you own, and internal apps whose source is lost — the entry condition is a stated basis, not an assumption of one.
1. **Reproduce from evidence, not memory.** Every reproduced screen, flow, and behavior is grounded in a **captured artifact** (screenshot, recorded interaction, observed API response). "Rebuild what I remember of it" is rejected — capture is the entry condition for the spec (Phase 1 → Phase 2 gate).
2. **Fidelity over faith.** The copy's match to the original is *proven* by diffing the rebuild against the Phase 2 parity baseline (visual / behavioral / feature / data), not asserted. A clone that "looks done" but was never diffed against the captured baseline is incomplete.

Scale: 9–27 agents (capture-heavy; desktop/robustness branches add capture agents; +1–2 for the Phase 0.5 research sweep, +1–2 for the Phase 0.2 Rights Gate (Canon[legal]/Cloak), +1 when Performance parity is declared), mid-to-high cost. **Ask First at the Phase 0.2 Rights Gate** (authorization basis — contract-level, AUTORUN cannot skip). **Confirm before launch when strategy = big-bang full clone** (whole product in one cutover).

> **Stack-first, then research-grounded capture.** Two front-loaded foundations precede capture. (1) **Stack Dialogue** (Phase 0.1, §3·0) — clone opens with a thorough *interactive* dialogue that locks the **Stack Decision Record** (the target rebuild stack, per layer, with stack-vs-fidelity tradeoffs made explicit) before any capture/build; this is a **contract-level checkpoint AUTORUN cannot skip**. (2) **Research-grounded capture** — a thorough **web evidence sweep** (Phase 0.5, `reference/research-grounding.md`) mines first-party docs, design systems, API references, and changelogs into a cited **Evidence Ledger** that supplies the completeness-gate denominator, exact published values, and version/drift signals. Research raises fidelity **without displacing the oracle** — captured artifacts stay authoritative; a web claim is a lead to confirm, never a substitute (§3a coverage gate, §3b drift). `stack=` pre-supplies the SDR (dialogue confirms rather than explores).

---

## 2. Capture Strategy (selected at Phase 3 gate)

| Strategy | When | Mechanism | Risk |
|----------|------|-----------|------|
| **extract-and-rebuild** (default) | Black box; no source access | Observe surface → neutral spec → rebuild from scratch on the target stack | Low–med — fidelity bounded by capture completeness |
| **scaffold-from-source** | Source available (grey/white box) | Fork structure + assets, re-express on the new stack, parity-verify the seams | Low — structure reused, but still diff-verified |
| **incremental-clone** (screen-by-screen) | Large product, live system | Reproduce one screen/flow at a time, each independently parity-gated | Low — each increment verifiable & shippable |
| **big-bang full clone** | Small/self-contained product | Whole reproduction, single cutover | High — **requires user confirmation** |

Capture-source bindings by `target_type`: **live web** = Vector/Voyager (crawl, screenshot, network observe) + Frame/Pixel (design extraction); **desktop** = Hone `automate` (macOS app automation via AppleScript/JXA — drive menus/windows/dialogs, capture per-window screenshots, script non-scriptable apps via System Events) + Pixel (visual diff of captured windows); **has Figma** = Frame (design context); **has source** = Lens (structure map); **mobile** = Voyager[ios]/Voyager (native UI capture); **API-backed** = Schema (infer data model from observed responses).

> **Desktop capture coverage.** Hone `automate` covers **macOS** GUI automation/screenshot natively. **Windows/Linux** desktop GUI automation has no first-class skill in this roster, so those targets are captured through an **external capture adapter** — the contract below makes that path first-class rather than a caveat. Visual/behavioral parity downstream (Pixel/Voyager/Radar/Attest/judge) is platform-independent and unchanged.

#### Capture-adapter contract (any surface with no first-class capture skill)

An adapter is a script the run shells out to — driving the OS accessibility / UI-automation API (Windows UIA, Linux AT-SPI), a vendor test harness, or assisted manual capture. It is **conformant when it emits the same four artifacts** every first-class capture path emits, so the baseline does not know or care which produced it:

| Artifact | Requirement |
|----------|-------------|
| **State screenshots** | one image per window/view/dialog **state** (not per app), at a declared fixed window size, with the state's identifier |
| **Interaction log** | ordered, replayable steps per flow (target element identity + action + observed result) — enough to re-drive the flow against the clone |
| **State/navigation graph** | which states are reachable from which, so the §3a coverage gate has a denominator |
| **Adapter provenance** | adapter name/version, OS + app build, locale, window size, pinned account/seed — merged into the §3b stamp |

**Gate:** a non-conformant adapter (screenshots but no interaction log, or no state graph) yields a **visual-only baseline** — declare it as such in the Fidelity Report and mark behavioral parity `UNVERIFIED` for that surface. Never let a partial adapter silently narrow what "parity" was proven. Assisted manual capture is a legitimate adapter when it meets the contract.

### 2a. Capture Robustness (live targets resist capture)

A live target — web or desktop — actively impedes complete capture. Plan for these at Phase 0 and handle them in Phase 1; an incompletely captured surface yields a thin baseline (§3a coverage gate), so robustness failures are *capture-coverage* failures, not mere annoyances.

| Obstacle | Handling |
|----------|----------|
| **Auth-gated screens** (login wall, role-gated views, paywalled states) | Capture under each required identity/role; enumerate auth'd-vs-anon and per-role states as distinct baseline entries. Credentials are run inputs, never hardcoded into the spec. |
| **Anti-bot / rate-limiting** | Throttle the crawl to a polite rate, back off on 429/challenge responses, and prefer authenticated session capture over aggressive crawling. If capture is blocked, **degrade to manual/assisted capture for the blocked surface** and record it — do not infer the screen from memory. |
| **CAPTCHA / interactive challenge** | Do not attempt to defeat it. Pause for human-in-the-loop capture of the gated surface, then resume. Mark any surface that could not be reached as a named coverage gap. |
| **Dynamic / lazy-loaded / virtualized content** | Drive scroll/pagination/expansion fully before screenshotting; wait for network-idle and settled layout so the captured state is complete, not mid-load. |
| **Ephemeral / session-scoped state** | Capture with a pinned account/seed so the state is reproducible; record the seed in the provenance stamp (§3b). |

---

## 3. Phase Contract (AUTORUN chain template)

```
Phase 0 FRAMING        Nexus internal: detect (target_type: live-web|desktop|mobile|has-source|api), scope (whole|area),
                       define what "complete copy" covers (visual ∧ behavioral ∧ feature ∧ data ∧ asset),
                       capture feasibility + robustness obstacles (§2a), and record the CAPTURE PROVENANCE STAMP
                       (target version/build, capture date, environment/OS, locale, pinned account/seed) → §3b.
                       Big-bang full clone → confirm with user.
Phase 0.1 STACK    ⟷   INTERACTIVE, contract-level (AUTORUN cannot skip — §3·0). Nail the TARGET REBUILD STACK with the
   DIALOGUE            user FIRST, before any capture/build: quick-probe the original's observable stack fingerprint
                       (headers / JS+CSS bundle signatures / API style) ‖ Lens/Atlas read the user's existing repo +
                       team/infra/license constraints → drive a LAYERED AskUserQuestion dialogue (runtime/lang →
                       frontend → styling/tokens → state → backend → data/ORM → API → build/test → deploy/infra),
                       surfacing every STACK-vs-FIDELITY tradeoff → lock the STACK DECISION RECORD (SDR).
                       `stack=` arg pre-supplied → confirm-not-explore.
Phase 0.2 RIGHTS   ⟷   Ask First, contract-level (AUTORUN cannot skip — §3·0b). Declare the AUTHORIZATION BASIS; Canon[legal] reads the
   GATE                target's ToS/automation posture; Cloak plans PII handling for the capture corpus; asset rights posture
                       set (recreate-never-reuse for marks); no-circumvention rule bound → lock the RIGHTS RECORD.
                       Undeclared/unsupportable basis → STOP (offer feature/apex, or narrow to owned surfaces).
Phase 0.5 RESEARCH  →  deep-research[+Compete?][thorough web EVIDENCE SWEEP: T1 docs/design-system/API-ref/changelog →
   SWEEP                T4 community → cited, verified EVIDENCE LEDGER] → reference/research-grounding.md
                       → Declared inventory = the Capture Completeness Gate denominator (§3a)
                       → Exact-value catalog feeds the fidelity-tolerance contract (§3a) + Phase 4 precision
                       → Version & drift signals sharpen the provenance stamp (§3b)
                       (research-first, capture-authoritative: a web claim is a lead to CONFIRM by capture, never the oracle)
Phase 1 CAPTURE     ∥  Vector/Voyager[live-web: crawl UI, per-screen screenshots, observe network/API traffic]
                       Builder[automate — desktop: drive menus/windows/dialogs, per-window screenshots, script non-scriptable apps]
                       Frame/Pixel[extract design system: tokens, layout, components from screenshots/Figma]
                       Lens?[map current structure + public surface]            (if source available)
                       Schema?[infer data model + API contract from observed responses]  (if API-backed)
                       Echo/Trace?[walk the flows; session-replay behavior if logs exist]
                       PDM/Lens[enumerate the FULL feature inventory in scope]
                       Ink/Pixel?[extract or recreate brand assets — fonts, icons, images — record license posture]
                       → output: capture corpus (screenshots + flow recordings + API shapes + feature list + asset set),
                         each artifact tagged with the provenance stamp
Phase 2 SPEC+BASELINE  Scribe[unified: author reconstruction spec from the capture corpus + acceptance criteria]
                       → establish the PARITY BASELINE = golden reference set (reference screenshots per screen/state,
                         recorded behavior fixtures, API contract, feature checklist, asset manifest) = the fidelity oracle,
                         stamped with its capture provenance (§3b)
                       → CAPTURE COMPLETENESS GATE (§3a) + PROVENANCE & DRIFT GATE (§3b)
Phase 3 ARCHITECT      Magi[arbitrate capture strategy + CAPTURE GATE]
                       Atlas?[clone architecture + module boundaries — DESIGNED WITHIN THE LOCKED SDR (§3·0)]
                       Muse?[design tokens from extracted design, expressed in the SDR's styling system]
                       → confirm Parity Map (visual / behavioral / feature / data / asset) targets for this product
Phase 4 REBUILD        Forge→Artisan/Builder[reproduce screens + logic on the target stack]
                       Pixel[pixel-accurate reproduction from reference screenshots]
                       +gateway?/schema?[API/DB boundaries]   +flow?[animations/interactions]
                       rally[engine COMPETE] for high-fidelity-critical screens → variants, pick closest
Phase 5 PARITY VERIFY ∥ Pixel/Voyager[VISUAL parity: differential diff vs Phase 2 reference set, per screen/state — §3c engine]
                       Radar/Voyager[BEHAVIORAL parity: flow + state-transition + edge-case fixtures, canonicalized]
                       Attest[FEATURE parity: coverage vs the Phase 1 feature inventory]
                       Pixel/Frame[ASSET parity: fonts/icons/images vs the asset manifest; recreate-vs-reuse honored]
                       judge[FIDELITY review: faithful copy vs approximate look-alike?]
                       → DRIFT RE-CHECK (§3b): spot-recapture a sample of target screens; if the live target diverged
                         from the stamped baseline, the baseline is stale → re-capture, do not "fix" the clone to a moved target
                       → loop to Phase 4 on any dimension below its parity threshold (loop ≤ 3 cycles (default 3))
Phase 6 SHIP           Guardian[PR with Fidelity Report + per-screen parity scores + incremental scope]
```

**Parallelism:** Phase 1 capture branches and Phase 5 verifiers run concurrently (hub-spoke, no shared mutable state). Phase 4 screens may parallelize under `isolation: worktree` when incremental-clone splits the rebuild into independent screens/flows.

**Checkpoint-resume:** ≥4 phases → persist the **Phase 0.1 SDR**, the Phase 1 capture corpus, Phase 2 parity baseline, and per-screen Phase 4 outputs at boundaries so an interrupted run resumes from the last completed screen.

### 3·0. Stack Dialogue Gate (Phase 0.1 — interactive, contract-level)

A clone rebuilds the target on a **new stack**, and that stack is the foundation every downstream phase sits on. It is largely the **user's decision** — driven by team skills, an existing codebase to rebuild into, infra, and licensing — not something Nexus may silently assume. So clone opens with a thorough **interactive dialogue** that locks the **Stack Decision Record (SDR)** before any capture-heavy or build work. This is the one place clone is human-in-the-loop; the checkpoint is **contract-level — AUTORUN_FULL cannot skip it** (mirroring `spec`'s contract-level checkpoints), because rebuilding on the wrong stack is expensive and hard to reverse (the "ambiguous + irreversible → ask" rule). The rest of clone proceeds per Mode; only this gate is mandatory-interactive.

**Inputs gathered first (cheap, before asking):**
- **Original stack fingerprint** — observable hints of what the target is built with: response headers, JS framework signatures, bundle analysis, CSS-framework markers, API style. A **lead, not a mandate** — clone reproduces the *observable surface, not the internals* (Parity Map §4), so you need not match the original's stack; the fingerprint just informs the option set and flags where matching vs diverging affects fidelity.
- **Host-side constraints** — when rebuilding into/alongside an existing codebase, Lens/Atlas map the user's current stack, conventions, and team-standard libraries; these bound the viable choices and become defaults the dialogue confirms rather than re-litigates.

**Layered decision checklist** — each a structured `AskUserQuestion`, thorough (every layer resolved, not a single "what stack?" question):

| Layer | Decision locked |
|-------|-----------------|
| Runtime / language | e.g. Node/Deno/Bun, TS/JS, Python, Go, … + version floor |
| Frontend framework | React/Vue/Svelte/Solid/none + SSR/SPA/MPA + meta-framework (Next/Nuxt/…) |
| Styling & design tokens | Tailwind / CSS Modules / CSS-in-JS / vanilla + the token system Muse will target |
| State management | built-in / Redux/Zustand/Pinia/signals / server-state lib |
| Backend framework | the API/server stack (or "static / BaaS / none") |
| Data layer | DB engine + ORM/query layer + migration tool |
| API style | REST / GraphQL / RPC — matched to the observed contract or deliberately re-shaped |
| Build tooling + package manager | Vite/Webpack/Turbopack/…, npm/pnpm/yarn/bun |
| Test stack | unit/component/E2E frameworks (what Radar/Voyager will author against) |
| Deployment target / infra | where the clone runs (constrains runtime, build output, env) |

**Stack-vs-fidelity tradeoff rule (the load-bearing reason this is thorough, not a formality):** some stack choices **cap achievable parity** — reproducing a canvas/WebGL-rendered UI with the DOM, choosing a different font-rendering engine, or a different animation runtime can bound visual/behavioral fidelity. The dialogue must **surface each such tradeoff explicitly** so the user chooses knowingly; each accepted tradeoff is recorded in the SDR **with the parity ceiling it imposes**, and that ceiling flows into the Phase 2 fidelity-tolerance contract (§3a) — a stack-imposed parity limit is then a **declared tolerance, not a silent failure** at Phase 5.

**Stack Decision Record (SDR)** — the locked deliverable: chosen stack per layer + rationale + host/infra/license constraints honored + stack-vs-fidelity tradeoffs accepted (each with its parity ceiling) + open stack risks. Stamped alongside the capture provenance (§3b).

**Gate:** Phase 1 capture and Phase 4 rebuild may not begin until the SDR is **locked** (interactively, or supplied via `stack=` and confirmed). Phase 3 ARCHITECT designs strictly within the SDR; Phase 4 builds on it; Radar/Voyager author tests against its test stack. A clone that picked its stack implicitly — or let Phase 4 drift off the SDR — is rejected.

### 3·0b. Authorization & Rights Gate (Phase 0.2 — contract-level, before any capture)

Capture is the first irreversible act of a clone run: it pulls a third party's surface — and often real user data rendered inside it — onto disk. The gate runs **before Phase 1**, is **Ask First** (AUTORUN cannot skip it), and produces the **Rights Record** stamped alongside the SDR and the capture provenance.

| Check | What must be stated | Agent |
|-------|---------------------|-------|
| **Authorization basis** | Which one: *own product* · *licensed / contracted reference* · *legacy system we operate* · *internal app, source lost* · *explicit written authorization from the rights holder*. "It's public, so it's fair" is **not** a basis — a public surface is visible, not licensed. | Nexus (declared by the user) |
| **Automated-capture posture** | The target's Terms of Service and `robots.txt`/automation policy as they bear on crawling, screenshotting, and API observation; rate limits honored per §2a | `Canon[legal]` (+`Compete` for published API terms) |
| **Asset rights** | Per-asset license posture in the manifest — reuse where licensed, **faithfully recreate otherwise** (`+Ink`); trademarks, logos, and brand marks are **recreate-never-reuse** unless owned or licensed | `Canon[legal]` + `Ink` |
| **PII in the capture corpus** | Screenshots and recorded responses of a live product routinely contain real user data. Capture under a **pinned synthetic/seed account** where possible; where not, the corpus is scanned and redacted before it becomes a baseline artifact | `Cloak` |
| **No-circumvention rule** | Technical protection measures are **not** defeated: no CAPTCHA solving, no auth bypass, no DRM/paywall circumvention. A surface reachable only by circumvention is a **named coverage gap**, never captured (this is the §2a rule stated as a rights constraint, not just a robustness one) | contract-level |

**Gate:** Phase 1 capture may not begin until the Rights Record is complete. An **undeclared or unsupportable authorization basis stops the run** — surfaced to the user with the two legitimate alternatives (`feature`/`apex` for a net-new product *inspired by* the reference, or narrowing scope to surfaces the user owns), never worked around. The Rights Record appears in the Fidelity Report (§8) so a shipped clone carries the basis it was built on.

### 3a. Capture Completeness Gate (Phase 2 — the integrity backbone of "fidelity over faith")

Parity is only as strong as the baseline. A green visual diff on three captured screens out of forty is *false confidence*, not a faithful copy. Clone specializes `_common/DIFFERENTIAL_PARITY.md` §3 Gate A (oracle/baseline adequacy) and Gate B (non-determinism canonicalization) — the full state/flow enumeration and the mask/freeze/normalize canonicalization list are owned there, not restated here. Phase 2 must clear both before Phase 5 may trust the baseline:

- **Coverage gate denominator** — the **Phase 0.5 Declared inventory** (`reference/research-grounding.md`) unioned with what navigation-graph crawling (Voyager) discovers is clone's "in scope" denominator for DP Gate A — checked against a researched checklist, not guesswork. If a screen or state was declared or discovered but never captured, it cannot be parity-verified — **expand the corpus before Phase 5**, or mark the gap as out-of-scope in the Fidelity Report (never silently omit it).
- **Fidelity-tolerance contract** — declares, per Phase 3c comparator, what is significant vs incidental for each of clone's five Parity Map dimensions, applying DP Gate B's canonicalization discipline (mask/freeze/normalize/threshold) so a diff neither spuriously fails on incidental variance nor masks real divergence.

**Gate:** Phase 5 parity verification runs against a baseline that has passed both DP gates. A baseline that is landing-page-only OR compares raw against dynamic content is rejected — fix it in Phase 2, do not proceed to trust it.

### 3b. Provenance & Drift Gate (the baseline is a snapshot of a moving target)

The stamp fields, the drift-recheck discipline, and the "never re-tune toward a moved target" rule are owned by `_common/DIFFERENTIAL_PARITY.md` §5 — not restated here. Clone-specific: the stamp is recorded in Phase 0, attached in Phase 1, and gates Phase 2 (a baseline without it is rejected there); the drift re-check runs **before Phase 5 SHIP** and at the start of any resumed run; for incremental-clone, each PR re-stamps per increment so it states the target version it was verified against. Drift status (no-drift / re-captured / deferred) appears in the Fidelity Report (§8).

### 3c. Differential Parity Engine (how parity is actually computed)

"Diff the rebuild against the baseline" is the contract; this is the mechanism. The shared kernel — parity-over-faith, the oracle/baseline-adequacy and non-determinism-canonicalization gates, the comparator/harness discipline, and provenance/drift — is owned by `_common/DIFFERENTIAL_PARITY.md` (§1–§5); clone's specialization is the **captured (black-box) oracle**: a stamped baseline observed from an external product. The per-dimension comparator and pass-condition table lives in § 4 Parity Map (merged there to avoid a second copy of the same six rows).

**Non-determinism canonicalization** applies DP Gate B (`_common/DIFFERENTIAL_PARITY.md` §3) to clone's baseline/clone pair: mask dynamic regions (clocks, feeds, randomized recommendations, ad slots, user-specific data), freeze clock/seed/locale, pin the account, normalize order-incidental collections, and disable or mid-freeze animations for static-frame comparison (verify motion separately via `+Flow`).

**Automated regression** — per `_common/DIFFERENTIAL_PARITY.md` §4, emitted as a screenshot-diff suite + behavior fixtures + feature matrix; each incremental-clone PR accretes into the growing regression suite.

---

## 4. Parity Map

The core knowledge of this recipe. Magi confirms the relevant dimensions in Phase 3; Builder/Pixel reproduce against them in Phase 4; the Phase 5 verifiers audit each dimension independently against the comparator and pass condition below (the §3c Differential Parity Engine mechanism, kept in this one table rather than duplicated).

| Dimension | What "faithful" means | Captured by (Phase 1) | Comparator (Phase 5) | Pass condition (default) |
|-----------|----------------------|------------------------|------------------------|---------------------------|
| **Visual** | Layout, spacing, color, typography, component look, responsive breakpoints / window states match per screen/state | Vector/Voyager screenshots (web); Builder `automate` per-window screenshots (desktop); Frame/Pixel design tokens | Per-screen/state image diff: align → mask declared dynamic regions → normalize fonts/AA → compute SSIM + per-pixel delta against the reference artifact (Pixel/Voyager) | SSIM ≥ declared threshold ∧ pixel-delta ≤ threshold, on the *significant* (unmasked) regions |
| **Behavioral** | Interactions, navigation, state transitions, validation, edge-case responses behave identically | Echo/Trace flow recordings; Voyager (web) / Builder `automate` (desktop) interaction traces | Replay each recorded flow against the clone; assert the canonicalized observable result (DOM/UI state, navigation target, validation message) equals the fixture (Radar/Voyager) | 100% of recorded flows green after canonicalization |
| **Feature** | Every feature in the inventory is present and reachable | PDM/Lens feature inventory | Attest coverage matrix: each inventory feature → present ∧ reachable ∧ exercised in the clone | 100% covered or explicitly deferred (named) |
| **Data / API** | Data model shape, API contract, and field semantics match the observed surface | Schema inference from observed responses | Structural diff of clone responses vs observed-contract shapes (field set, types, nesting); semantics spot-checked on sampled records (gateway/schema) | shape-equivalent; sampled semantics match |
| **Asset** | Fonts, icons, images, and other brand assets match — reused where licensed, faithfully recreated otherwise | Ink/Pixel asset extraction → asset manifest (with license posture) | Per-asset diff vs the asset manifest: fonts (family/metrics), icons/images (perceptual hash within tolerance, or confirmed faithful recreation) (Pixel/Frame) | each asset matches within tolerance, or is a declared faithful recreation |
| **Performance** *(declared per run)* | The copy feels like the original: interaction latency, load/startup, and perceived responsiveness stay within a declared envelope of the captured baseline | Vector/Voyager timing capture during Phase 1 (per-screen load, interaction latency); Builder window/app launch timings (desktop) | Replay the perf-significant flows against the clone on a like-for-like environment and compare the timing distribution (median + p95) to the Phase 1 captured baseline — never a single run, never across dissimilar hardware/network (Bolt/Siege) | within the declared factor (default p95 ≤ 1.5× original); a flow outside it is a named parity gap, not a rounding difference |

> Reproduce *idiomatically on the target stack* — a faithful copy is faithful in **observable result**, not in internal implementation. Re-expressing the original's UI in the target framework's idioms is correct; transliterating its internal code (when source exists) is not the goal — `judge` Phase 5 distinguishes faithful-result from cargo-cult-internals.

---

## 5. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Wrong-stack rebuild / stack silently caps fidelity** (built on an assumed stack the team can't maintain, or a rendering/font/animation choice bounds parity — discovered only at Phase 5) | §3·0 Stack Dialogue Gate, feeding each accepted tradeoff's parity ceiling into §3a as a *declared* tolerance |
| **Memory-based / doc-as-truth rebuild** (reproduced from impression, or from an aspirational/stale doc never confirmed against the live surface) | §1 principle 1 (the capture corpus is the Phase 1 → 2 entry condition) + the research-first / capture-authoritative rule (§1, §3b) |
| **Thin baseline / happy-path-only coverage** (3 screens captured of 40; error/empty/loading states missing) | §3a Capture Completeness Gate — expand the corpus or explicitly defer the gap before Phase 5 may trust the baseline |
| **Stumbled-onto capture / pixel-estimated values** (captured only the easy-to-reach surface; guessed a value that is actually published) | Phase 0.5 research sweep (`reference/research-grounding.md`), consumed by §3a as the coverage denominator and the exact-value source |
| **Spurious/masked diff on incidental variance** (AA, fonts, timestamps, feeds, A/B, ad slots) | §3a / §3c DP Gate B canonicalization — applied on both sides, before comparing |
| **Approximate/cargo-cult copy accepted** (looks done but isn't faithful, or transliterates internals over idiomatic re-expression) | `judge` fidelity review (Phase 5) + the §4 Parity Map's per-dimension pass conditions, which judge observable result rather than internals |
| **Feature drop-out** (a screen built, a feature silently lost) | Attest feature-parity coverage vs the Phase 1 inventory (§4, Feature row) |
| **"Reproduce everything at once" risk blindness** | §2 capture-strategy selection at the Phase 3 Magi gate — incremental-clone preferred, big-bang requires user confirmation |
| **Stale baseline** (target shipped a new version mid-clone; clone verified against a target that no longer exists) | §3b Provenance & Drift Gate |
| **Capture blocked** (auth wall / anti-bot / CAPTCHA → surface never captured, inferred from memory) | §2a robustness handling; a blocked surface is named as a §3a coverage gap, never reconstructed from memory |
| **Rights/authorization failure** (unauthorized reproduction with no stated basis; capture that violates ToS or defeats a protection measure; real user data/PII baked into the baseline; trademark reuse mistaken for asset fidelity) | §3·0b Authorization & Rights Gate — all four checks plus the no-circumvention rule; an unsupportable basis stops the run |
| **Desktop surface treated as second-class** (only web capture wired, native windows/menus/dialogs missed) | §2 capture-source bindings + capture-adapter contract, into the same baseline; the §3a coverage gate spans windows/menus/modals/OS interactions |
| **A faithful-looking clone that is unusably slower** (visual/behavioral parity green, interaction latency 5× the original) | §4 Performance parity dimension (declared per run) |
| **Partial capture adapter silently narrowing "parity"** (screenshots only → behavioral parity never actually proven for that surface) | §2 capture-adapter contract — a non-conformant adapter yields a declared visual-only baseline, behavioral parity `UNVERIFIED` |

## 6. Add-ons

- `+Voyager[ios]` — native iOS UI capture/verification when the target is a mobile app.
- `+Hone[automate]` — macOS desktop-app capture/automation when `target_type = desktop`.
- `+Ink` — recreate brand assets (icons/illustrations) when the original's assets cannot be licensed for reuse.
- `+Flow` — when motion/animation fidelity is part of "complete copy".
- `+Schema` / `+Tuner` — when the data layer and query behavior must be reproduced, not just the UI.
- `+Seek` — when search/ranking behavior is a reproduced feature.
- `+Sherpa` — decompose a large incremental-clone into atomic per-screen steps.
- `+Polyglot` — when the original ships multiple locales that must be reproduced.
- `+Siege` — load/throughput parity when the clone must match the original's performance envelope.

## 7. Decision Tree vs Neighbors

```
Reproducing an EXISTING product faithfully (parity-verified)?
  NO  → cross-language rewrite of your own source? → transmute | arch/framework/mock→prod sweep? → migrate
        | net-new design inspired by a reference? → feature/apex | single mockup→code? → pixel
  YES → target is mobile-native from a Web app? → PORTING (Port→Native)
        single Figma source, no full rebuild? → frame
        otherwise (whole product, fidelity-verified — web | desktop | mobile | api) → clone
              target_type = desktop? → Hone `automate` capture (macOS) / external UI-automation harness (Win/Linux), same Parity Map
```

## 7a. Handoff contract (what downstream receives)

A finished clone is rarely the end — it is the starting point for the product that replaces the original. The **Clone Handoff Packet** carries the state so downstream recipes do not re-derive it:

| Field | Content | Consumed by |
|-------|---------|-------------|
| `sdr` | the locked Stack Decision Record incl. accepted stack-vs-fidelity tradeoffs **and their parity ceilings** | `feature`/`apex` (every new feature is built on this stack, and a ceiling is a standing constraint, not a bug) |
| `parity_harness` | the re-runnable comparator suite (screenshot diffs + behavior fixtures + feature matrix + perf flows) | `migrate`/`refactor`/`optimize` — the harness becomes the regression net for any later change to the clone |
| `rights_record` | authorization basis + asset license posture + PII handling | `launch` (ship-time review), `canon[legal]` (any later distribution question) |
| `provenance_stamp` | target version/build, capture date, environment, locale, seed | a later re-capture / drift re-check compares against this, not a fresh guess |
| `coverage_gaps` | deferred, capture-blocked, and `UNVERIFIED` surfaces, each named | `feature` backlog — the honest list of what the clone does **not** yet reproduce |
| `parity_ceilings` | per-dimension limits imposed by the stack choice | `optimize` (a perf ceiling that is stack-imposed is not an optimization target), `restyle` (a visual ceiling is not a design defect) |

**Contract rule:** a downstream recipe that changes the clone **re-runs the parity harness** before shipping. A change that breaks parity is either a deliberate divergence — recorded as such, moving the clone off the baseline by intent — or a regression. Silent parity loss is the failure this field exists to prevent.

## 8. Output

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus a **Fidelity Report**, carrying these artifacts — each defined in the section named, not restated here:

- **Rights Record** (§3·0b) · **Stack Decision Record** (§3·0) · **provenance stamp + drift status** (§3b) · **capture mechanism and capture-adapter conformance, per surface** (§2, incl. any `visual-only` → behavioral `UNVERIFIED`).
- **Research Grounding** — Evidence Ledger size + per-tier source count, declared-vs-captured coverage delta, exact values adopted, version/drift signals (`reference/research-grounding.md` §6).
- **Capture coverage** — screens/states/flows/windows captured vs enumerated, with every deferred or capture-blocked gap named (§3a) — plus the **fidelity-tolerance + non-determinism canonicalization contract** it was cleared against (§3a/§3c: what was masked/frozen vs compared raw).
- **Per-dimension parity results**, each scored against its §4 Parity Map pass condition: visual (per screen/state), behavioral (fixture pass rate), feature (coverage vs inventory), data/API, asset (per-asset match or declared recreation + license posture), performance (baseline vs clone p95 vs the declared envelope, or `N/A — not declared`).
- **Fidelity-review verdict** (Phase 5 `judge`) and **incremental scope** — which screens this PR reproduced and which remain.

For incremental-clone runs, each increment is a separate shippable PR carrying its own provenance stamp (the target version *that* increment was verified against) + the accreted parity-regression harness.
