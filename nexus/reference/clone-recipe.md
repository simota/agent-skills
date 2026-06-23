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

**Two non-negotiable principles:**
1. **Reproduce from evidence, not memory.** Every reproduced screen, flow, and behavior is grounded in a **captured artifact** (screenshot, recorded interaction, observed API response). "Rebuild what I remember of it" is rejected — capture is the entry condition for the spec (Phase 1 → Phase 2 gate).
2. **Fidelity over faith.** The copy's match to the original is *proven* by diffing the rebuild against the Phase 2 parity baseline (visual / behavioral / feature / data), not asserted. A clone that "looks done" but was never diffed against the captured baseline is incomplete.

Scale: 8–24 agents (capture-heavy; desktop/robustness branches add capture agents; +1–2 for the Phase 0.5 research sweep), mid-to-high cost. **Confirm before launch when strategy = big-bang full clone** (whole product in one cutover).

> **Stack-first, then research-grounded capture.** Two front-loaded foundations precede capture. (1) **Stack Dialogue** (Phase 0.1, §3·0) — clone opens with a thorough *interactive* dialogue that locks the **Stack Decision Record** (the target rebuild stack, per layer, with stack-vs-fidelity tradeoffs made explicit) before any capture/build; this is a **contract-level checkpoint AUTORUN cannot skip**. (2) **Research-grounded capture** — a thorough **web evidence sweep** (Phase 0.5, `reference/research-grounding.md`) mines first-party docs, design systems, API references, and changelogs into a cited **Evidence Ledger** that supplies the completeness-gate denominator, exact published values, and version/drift signals. Research raises fidelity **without displacing the oracle** — captured artifacts stay authoritative; a web claim is a lead to confirm, never a substitute (§3a coverage gate, §3b drift). `stack=` pre-supplies the SDR (dialogue confirms rather than explores).

---

## 2. Capture Strategy (selected at Phase 3 gate)

| Strategy | When | Mechanism | Risk |
|----------|------|-----------|------|
| **extract-and-rebuild** (default) | Black box; no source access | Observe surface → neutral spec → rebuild from scratch on the target stack | Low–med — fidelity bounded by capture completeness |
| **scaffold-from-source** | Source available (grey/white box) | Fork structure + assets, re-express on the new stack, parity-verify the seams | Low — structure reused, but still diff-verified |
| **incremental-clone** (screen-by-screen) | Large product, live system | Reproduce one screen/flow at a time, each independently parity-gated | Low — each increment verifiable & shippable |
| **big-bang full clone** | Small/self-contained product | Whole reproduction, single cutover | High — **requires user confirmation** |

Capture-source bindings by `target_type`: **live web** = Vector/Voyager (crawl, screenshot, network observe) + Frame/Pixel (design extraction); **desktop** = Wield (macOS app automation via AppleScript/JXA — drive menus/windows/dialogs, capture per-window screenshots, script non-scriptable apps via System Events) + Pixel (visual diff of captured windows); **has Figma** = Frame (design context); **has source** = Lens (structure map); **mobile** = Snap/Voyager (native UI capture); **API-backed** = Schema (infer data model from observed responses).

> **Desktop capture coverage.** Wield covers **macOS** GUI automation/screenshot natively. **Windows/Linux** desktop GUI automation has no first-class skill in this roster — capture those via an external automation harness (e.g. the OS's accessibility/UI-automation API driven through a script the run shells out to) and feed the resulting screenshots/interaction logs into the same parity baseline; **mark the capture mechanism in the Fidelity Report provenance stamp** so the gap in tooling is explicit, never silent. Visual/behavioral parity downstream (Pixel/Voyager/Radar/Attest/judge) is platform-independent and unchanged.

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
Phase 0.5 RESEARCH  →  deep-research[+Compete?][thorough web EVIDENCE SWEEP: T1 docs/design-system/API-ref/changelog →
   SWEEP                T4 community → cited, verified EVIDENCE LEDGER] → reference/research-grounding.md
                       → Declared inventory = the Capture Completeness Gate denominator (§3a)
                       → Exact-value catalog feeds the fidelity-tolerance contract (§3a) + Phase 4 precision
                       → Version & drift signals sharpen the provenance stamp (§3b)
                       (research-first, capture-authoritative: a web claim is a lead to CONFIRM by capture, never the oracle)
Phase 1 CAPTURE     ∥  Vector/Voyager[live-web: crawl UI, per-screen screenshots, observe network/API traffic]
                       Wield[desktop: drive menus/windows/dialogs, per-window screenshots, script non-scriptable apps]
                       Frame/Pixel[extract design system: tokens, layout, components from screenshots/Figma]
                       Lens?[map current structure + public surface]            (if source available)
                       Schema?[infer data model + API contract from observed responses]  (if API-backed)
                       Echo/Trace?[walk the flows; session-replay behavior if logs exist]
                       PDM/Lens[enumerate the FULL feature inventory in scope]
                       Ink/Pixel?[extract or recreate brand assets — fonts, icons, images — record license posture]
                       → output: capture corpus (screenshots + flow recordings + API shapes + feature list + asset set),
                         each artifact tagged with the provenance stamp
Phase 2 SPEC+BASELINE  Scribe/Accord[author reconstruction spec from the capture corpus + acceptance criteria]
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

### 3a. Capture Completeness Gate (Phase 2 — the integrity backbone of "fidelity over faith")

Parity is only as strong as the baseline. A green visual diff on three captured screens out of forty is *false confidence*, not a faithful copy. Phase 2 must clear two gates before Phase 5 may trust the baseline:

- **Coverage gate** — the capture corpus must cover **every screen, every reachable state (empty / loading / error / populated / auth'd-vs-anon), and every flow** in scope, not just the landing page and the happy path. The **denominator of "in scope" is the Phase 0.5 Declared inventory** (the researched feature/flow/state list from `reference/research-grounding.md`) unioned with what navigation-graph crawling (Voyager) discovers — so coverage is checked against a researched checklist, not guesswork. Require the parity baseline to hold a reference artifact for each. If a screen or state was declared (by research) or discovered (by crawl) but never captured, it cannot be parity-verified — **expand the corpus before Phase 5**, or mark the gap as out-of-scope in the Fidelity Report (never silently omit it).
- **Fidelity-tolerance contract** — pixel-exact equality is the wrong bar for **incidental rendering variance**: anti-aliasing, font-hinting across platforms, dynamic/timestamped content, randomized feeds, A/B-varied layouts, animation mid-frames. For each dimension, declare what is **semantically significant vs incidental**, and set per-screen diff tolerances (mask dynamic regions, normalize fonts, freeze clock/seed, compare at a declared SSIM/pixel-delta threshold). Otherwise visual parity either **spuriously fails** on incidental variance or **masks real divergence** under a too-loose threshold.

**Gate:** Phase 5 parity verification runs against a baseline that has passed both gates. A baseline that is landing-page-only OR compares raw against dynamic content is rejected — fix it in Phase 2, do not proceed to trust it.

### 3b. Provenance & Drift Gate (the baseline is a snapshot of a moving target)

A live target is not frozen — it ships new versions, A/B-rotates layouts, and refreshes content while the clone is being built. A baseline captured on day 1 and trusted on day 30 silently compares the clone against a target that no longer exists. Two controls keep the baseline honest:

- **Provenance stamp** — every capture artifact and the parity baseline as a whole carry a stamp: **target version/build identifier (or capture date if unversioned), capture environment/OS, browser or app version, locale, viewport/window size, and the pinned account/seed** used. The stamp is the answer to "what exactly did we copy, and from when." It is recorded in Phase 0, attached in Phase 1, and surfaced in the Fidelity Report (§8). A baseline without a provenance stamp is rejected at the Phase 2 gate.
- **Drift re-check** — before SHIP (Phase 5) and at the start of any resumed run, **spot-recapture a sample of baseline screens/flows from the live target and diff them against the stamped baseline**. If the target has drifted beyond the fidelity tolerance, the baseline is stale: **re-capture the drifted surface and re-establish the baseline — never silently re-tune the clone toward a target that moved**, because that produces a copy that matches neither the captured baseline nor the current target. For long incremental-clone runs, re-stamp per increment so each shippable PR states the target version it was verified against.

**Gate:** a baseline with no provenance stamp, or a SHIP whose drift re-check was skipped, is rejected. Drift status (no-drift / re-captured / deferred) appears in the Fidelity Report.

### 3c. Differential Parity Engine (how parity is actually computed)

"Diff the rebuild against the baseline" is the contract; this is the mechanism. The shared kernel — parity-over-faith, the oracle/baseline-adequacy and non-determinism-canonicalization gates, the comparator/harness discipline, and provenance/drift — is owned by `_common/DIFFERENTIAL_PARITY.md` (§1–§5); clone's specialization is the **captured (black-box) oracle**: a stamped baseline observed from an external product. Each dimension is computed by an explicit, reproducible comparator, not eyeballed:

| Dimension | Comparator | Pass condition |
|-----------|-----------|----------------|
| **Visual** | Per-screen/state image diff: align → mask declared dynamic regions → normalize fonts/AA → compute SSIM + per-pixel delta against the reference artifact | SSIM ≥ declared threshold ∧ pixel-delta ≤ threshold, on the *significant* (unmasked) regions |
| **Behavioral** | Replay each recorded flow against the clone; assert the canonicalized observable result (DOM/UI state, navigation target, validation message) equals the fixture | 100% of recorded flows green after canonicalization |
| **Feature** | Attest coverage matrix: each inventory feature → present ∧ reachable ∧ exercised in the clone | 100% covered or explicitly deferred (named) |
| **Data / API** | Structural diff of clone responses vs observed-contract shapes (field set, types, nesting); semantics spot-checked on sampled records | shape-equivalent; sampled semantics match |
| **Asset** | Per-asset diff vs the asset manifest: fonts (family/metrics), icons/images (perceptual hash within tolerance, or confirmed faithful recreation) | each asset matches within tolerance, or is a declared faithful recreation |

**Non-determinism canonicalization (both sides, before comparing).** A faithful clone of a *dynamic* product must not be failed by the product's own variance. For each dimension declare significant-vs-incidental and canonicalize the incidental on both baseline and clone before diffing: **mask dynamic regions** (clocks, feeds, randomized recommendations, ad slots, user-specific data), **freeze clock/seed/locale**, **pin the account**, **normalize ordering** of order-incidental collections, and **disable or mid-freeze animations** for static-frame comparison (verify motion separately via `+Flow`). A clone of a randomized feed is faithful when its *feed mechanism* reproduces the original's behavior, not when a single frame matches byte-for-byte — compare the mechanism, not a frozen sample of its output. The "without canonicalization → spuriously-fails / masks-divergence" failure pair this prevents is owned by `_common/DIFFERENTIAL_PARITY.md` §3 (Gate B).

**Automated regression.** The Phase 5 comparators are emitted as a re-runnable parity harness (screenshot-diff suite + behavior fixtures + feature matrix), so a later change to the clone — or a later target re-capture — re-verifies parity without re-deriving the baseline. For incremental-clone, each increment's harness accretes into a growing regression suite.

---

## 4. Parity Map

The core knowledge of this recipe. Magi confirms the relevant dimensions in Phase 3; Builder/Pixel reproduce against them in Phase 4; the Phase 5 verifiers audit each dimension independently.

| Dimension | What "faithful" means | Captured by (Phase 1) | Verified by (Phase 5) | Threshold (default) |
|-----------|----------------------|------------------------|------------------------|---------------------|
| **Visual** | Layout, spacing, color, typography, component look, responsive breakpoints / window states match per screen/state | Vector/Voyager screenshots (web); Wield per-window screenshots (desktop); Frame/Pixel design tokens | Pixel/Voyager screenshot diff (masked, normalized) — §3c | ≥ declared SSIM / ≤ pixel-delta per screen |
| **Behavioral** | Interactions, navigation, state transitions, validation, edge-case responses behave identically | Echo/Trace flow recordings; Voyager (web) / Wield (desktop) interaction traces | Radar/Voyager behavior fixtures (canonicalized) | 100% of recorded flows green |
| **Feature** | Every feature in the inventory is present and reachable | PDM/Lens feature inventory | Attest coverage vs inventory | 100% covered or explicitly deferred |
| **Data / API** | Data model shape, API contract, and field semantics match the observed surface | Schema inference from observed responses | contract/shape diff (gateway/schema) | shape-equivalent; semantics spot-checked |
| **Asset** | Fonts, icons, images, and other brand assets match — reused where licensed, faithfully recreated otherwise | Ink/Pixel asset extraction → asset manifest (with license posture) | Pixel/Frame per-asset diff (perceptual hash / font metrics) — §3c | each asset within tolerance or a declared faithful recreation |

> Reproduce *idiomatically on the target stack* — a faithful copy is faithful in **observable result**, not in internal implementation. Re-expressing the original's UI in the target framework's idioms is correct; transliterating its internal code (when source exists) is not the goal — `judge` Phase 5 distinguishes faithful-result from cargo-cult-internals.

---

## 5. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Wrong-stack rebuild** (clone built on an assumed stack the team can't maintain / that doesn't fit the existing codebase or infra) | Phase 0.1 Stack Dialogue Gate (§3·0): interactive, contract-level SDR locked before capture/build; AUTORUN cannot skip |
| **Stack silently caps fidelity** (a rendering/animation/font-engine choice bounds parity, discovered only at Phase 5) | §3·0 stack-vs-fidelity tradeoff rule: each accepted tradeoff recorded with its parity ceiling → flows into the Phase 2 fidelity-tolerance contract as a *declared* tolerance |
| **Memory-based rebuild** (reproduced from impression, not artifacts) | Phase 1 capture corpus is a mandatory entry condition for Phase 2 |
| **Stumbled-onto capture / pixel-estimated values** (captured only the easy-to-reach surface; guessed values that are actually published) | Phase 0.5 research sweep (`reference/research-grounding.md`): Declared inventory = completeness-gate denominator; Exact-value catalog (T1 tokens/specs) confirmed into the baseline; capture stays authoritative |
| **Doc-as-truth corruption** (rebuilt from an aspirational/stale doc never confirmed against the live surface) | research-first/capture-authoritative rule + per-claim verification status; a claim contradicted by capture flags stale/drift, capture wins |
| **Thin baseline → false fidelity** (3 screens captured, 40 exist) | Phase 2 coverage gate: corpus must hold an artifact per screen/state/flow; expand or explicitly defer before Phase 5 trusts it |
| **Spurious visual-diff failure on incidental variance** (AA, fonts, timestamps, A/B) | Phase 2 fidelity-tolerance contract: declare significant-vs-incidental, mask dynamic regions, normalize fonts, freeze clock/seed, compare at declared threshold |
| **Approximate look-alike accepted as a copy** | `judge` fidelity review (Phase 5) + per-dimension thresholds block "close enough" |
| **Happy-path-only behavior** (error/empty/loading states missing) | Phase 1 explicit state enumeration + Phase 2 coverage gate require every reachable state |
| **Feature drop-out** (a screen built, a feature silently lost) | Attest feature-parity coverage vs the Phase 1 inventory (Phase 5) |
| **"Reproduce everything at once" risk blindness** | Magi capture-strategy gate (Phase 3) prefers incremental-clone; big-bang needs user confirm |
| **Internal transliteration instead of idiomatic re-expression** | Parity Map "observable result, not internals" + judge review |
| **Stale baseline** (target shipped a new version mid-clone; clone verified against a target that no longer exists) | §3b provenance stamp + pre-SHIP drift re-check; re-capture on drift, never re-tune toward a moved target |
| **Capture blocked** (auth wall / anti-bot / CAPTCHA → surface never captured, inferred from memory) | §2a robustness handling: per-role/auth capture, polite throttle + backoff, human-in-the-loop for challenges; blocked surface named as a coverage gap, never reconstructed from memory |
| **Spurious diff on dynamic content** (feeds, recommendations, timestamps, A/B, ad slots fail an exact diff) | §3c non-determinism canonicalization: mask dynamic regions, freeze clock/seed/locale, compare the mechanism not a frozen sample |
| **Asset infidelity** (placeholder fonts/icons, wrong logo, or unlicensed reuse of copyrighted assets) | Asset Parity dimension + asset manifest with license posture; reuse where licensed, faithfully recreate otherwise |
| **Desktop surface treated as second-class** (only web capture wired, native windows/menus/dialogs missed) | `target_type: desktop` first-class: Wield capture (macOS) / external UI-automation harness (Win/Linux) into the same baseline; coverage gate spans windows/menus/modals/OS interactions |

## 6. Add-ons

- `+Snap` — native iOS UI capture/verification when the target is a mobile app.
- `+Wield` — macOS desktop-app capture/automation when `target_type = desktop`.
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
              target_type = desktop? → Wield capture (macOS) / external UI-automation harness (Win/Linux), same Parity Map
```

## 8. Output

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus a **Fidelity Report**: the **Stack Decision Record** (locked stack per layer + rationale + constraints honored + stack-vs-fidelity tradeoffs accepted with their parity ceilings — §3·0), a **Research Grounding** subsection (Evidence Ledger size + per-tier source count, declared-vs-captured coverage delta, exact-values adopted, version/drift signals — per `reference/research-grounding.md` §6), **provenance stamp (target version/build, capture date, environment/OS, app/browser version, locale, pinned account/seed) + capture mechanism per surface (e.g. Wield/macOS, external harness/Win)**, **drift status (no-drift / re-captured / deferred)**, per-screen visual parity scores (SSIM/pixel-delta vs threshold), behavioral-fixture pass rate, **capture coverage (screens/states/flows/windows captured vs enumerated, with any deferred or capture-blocked gaps named)**, **fidelity-tolerance + non-determinism canonicalization contract (which regions/aspects were masked/frozen vs compared raw)**, feature-parity coverage vs inventory, **asset-parity results (per-asset match/recreation + license posture)**, fidelity-review verdict, and incremental scope (which screens reproduced this PR, which remain — each increment re-stamped with the target version it was verified against). For incremental-clone runs, each increment is a separate shippable PR carrying its own provenance stamp + accreted parity-regression harness.
