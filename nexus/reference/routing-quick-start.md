# Routing Quick Start — Extended

Extends the inline Routing Quick Start in `SKILL.md`. Canonical matrix: `reference/routing-matrix.md`.

## Standard Task-Type Chains (legacy `classify` flow)

| Task Type | Default Chain | Add When |
|-----------|---------------|----------|
| `BUG` | Scout[RCA] → Sherpa? → Radar[failing repro] → Builder[root-cause] → Radar[verify] → Guardian | `+Sentinel` for security, `+Trail` when a past commit introduced it, `+Ripple` for wide blast radius. Sherpa skip when files ≤ 2 or single-component fix. Phase contract ↓ |
| `FEATURE` | Lens?[reuse] → Sherpa[spec+AC] → Forge? → Builder → Radar[+verify gate] → Guardian | Lens reuse-scan on existing codebases (skip greenfield). Forge only when approach unproven (spike, not shipped). `+Muse`/`+Palette` for UI (skip on backend/CLI), `+Artisan` for frontend production. Phase contract ↓ |
| `SECURITY` | Sentinel[triage] → Probe?[confirm-exploit] → Builder[root-cause] → Probe/Radar[verify-closed] → Vigil? → Guardian | Confirm-exploit before & verify-closed after the fix. `+Breach` red-team, `+Shift` dep-CVE upgrade, `+Crypt` crypto. Phase contract ↓ |
| `REFACTOR` | Radar?[safety-net] → Zen → Radar[verify-equivalence] → Guardian | Green-before / same-suite-same-result-after. Safety-net skip for tool-assisted pure rename/extract. `+Sherpa` multi-file, `+Atlas` architecture, `+Grove` structure. Phase contract ↓ |
| `OPTIMIZE` | Bolt/Tuner[measure→target→optimize] → Radar[verify-speedup] → Guardian | Measure-first / prove-with-a-number / no-regression. `+Schema` DB index, `+Siege` load-test, `+Beacon` prod SLO. Phase contract ↓ |
| `DESIGN_SYSTEM_DOCS` | Muse → Vitrine + Canvas → Quill | `+Vision` for direction, `+Artisan` for live examples |
| `DESIGN_WORKFLOW` | Atelier (orchestrates: Vision → Muse/Frame → Forge → Artisan → Vitrine → Canvas) | Full design→code loop with design-system persistence. When request spans direction + tokens + prototype + implementation + catalog |
| `MOBILE_NATIVE` | **Native** → Radar → Vitrine → Launch | iOS Swift/SwiftUI or Android Kotlin/Compose. Pure-native only (RN/Flutter/KMP/CMP → Forge). Add-ons + full row → `reference/routing-matrix.md` MOBILE_NATIVE |
| `IOS_UI_TEST` | **Snap** → Gear → Launch | XCUITest authoring, accessibilityIdentifier audit, App Store screenshot pipeline (fastlane snapshot). Pure XCUITest scope (Appium/Detox/Maestro → Voyager). Add-ons → `reference/routing-matrix.md` IOS_UI_TEST |
| `PORTING` | Lens/Atlas → **Port → Native** → Voyager → Launch | Web → iOS/Android porting design + implementation. Add-ons (Fossil/Field/Scaffold/Polyglot/Cloak/Crypt) → `reference/routing-matrix.md` PORTING. Cross-platform UI component-name lookup → `port/reference/ui-terminology-matrix.md` |

## FEATURE Phase Contract

`feature` is the highest-traffic Recipe; its chain row is a summary. Phase semantics (read before executing a non-trivial feature):

- **SURVEY (Lens, conditional) — reuse before you build** — for any feature added to an **existing** codebase, scan for reusable implementations BEFORE decomposing: does the function / component / hook / pattern already exist? Extend or compose the existing one instead of reinventing it. Skip only for greenfield. The most common feature-implementation waste is re-deriving code that already ships — this step is the guard (repo rule: don't re-implement what already exists).
- **SPEC (Sherpa)** — decompose into atomic steps AND **lock acceptance criteria + scope boundary before any code** (front-loaded ACs become Radar's test targets and the VERIFY gate). Fold SURVEY's reuse findings into the plan (build-on-existing vs build-new, stated per step). Skip Sherpa only when the change is single-file atomic, but still state the ACs inline.
- **PROTOTYPE (Forge, conditional)** — run **only when the approach is unproven** (new UI pattern, uncertain API shape, integration risk). Forge output is a **throwaway spike to validate feasibility, NOT the shipped artifact**. Skip for well-understood CRUD/backend additions — Builder goes straight to production. Prevents both "rebuild from scratch, lose the spike's learnings" and "ship the prototype as production".
- **BUILD (Builder; +Artisan for frontend production)** — production implementation carrying forward the spike's validated decisions and SURVEY's reuse plan. UI surface routing: **+Muse** when introducing new design tokens/visual primitives, **+Palette** when interaction-heavy, **Artisan** owns frontend production code. Backend/CLI features skip all three.
- **VERIFY (Radar + gate)** — Radar adds edge-case/regression tests; THEN the **VERIFY gate requires existing build + test + lint/typecheck green** against the locked ACs. Not "new tests pass" — the whole check suite. Additionally confirm **each locked AC is actually satisfied** (covered by a test or demonstrated behavior), not merely that the suite is green — convergence on green ≠ the feature does what the spec required. A feature is not done until the gate passes (repo quality rule).
- **SHIP (Guardian)** — PR-prep: commit granularity, PR title/description, ACs linked to evidence.

**Anti-patterns prevented**: (1) prototype-shipped-as-production (PROTOTYPE spike discipline), (2) feature-without-acceptance-criteria (SPEC front-loads ACs), (3) "new tests green but build broken" (VERIFY runs the full suite, not just Radar's additions), (4) feature lands with no PR discipline (SHIP/Guardian — previously absent from the chain), (5) **reinventing code that already ships** (SURVEY reuse scan), (6) **green suite that doesn't meet the spec** (VERIFY's per-AC satisfaction check).

## BUG Phase Contract

Bug-fixing has a best-practice order the default chain must honor — **reproduce before you fix**:

- **RCA (Scout)** — root-cause analysis: why the bug occurs, where to fix, reproduction steps, impact/blast radius. **Confirm it IS a defect** (not expected behavior / misconfig / user error) before proceeding — a misread "bug" exits here with an explanation, no code.
- **DECOMPOSE (Sherpa, conditional)** — only when the fix touches 3+ files or spans components. Skip for single-component atomic fixes.
- **REPRODUCE-FIRST (Radar)** — encode Scout's reproduction steps as a **failing automated test BEFORE any fix**. The failing test is the acceptance criterion: red now, green after the fix. A regression test written *after* the fix can't prove it actually addresses the reported bug — it never failed.
- **FIX (Builder)** — fix the **root cause** Scout identified, not the symptom. Symptom-only patches (swallowing the error, masking the output, broad `try/except`) are rejected — repo rule: fix root causes, don't silence.
- **VERIFY (Radar + gate)** — the repro test now **passes** (bug gone), the existing build + test suite stays green (no new regression), and Scout's blast-radius areas are spot-checked. `+Sentinel` when the bug has a security dimension.
- **SHIP (Guardian)** — PR carrying the repro test + root-cause explanation, so the fix is auditable and the regression is permanently guarded.

**Anti-patterns prevented**: (1) regression test written after the fix that never actually failed (REPRODUCE-FIRST red→green), (2) symptom patch leaving the cause live (FIX root-cause discipline), (3) fix that breaks something else (VERIFY suite + blast-radius), (4) "fix" for a non-bug (RCA defect-confirmation gate), (5) fix lands with no PR/regression guard (SHIP — previously absent from the chain).

## SECURITY Phase Contract

A security fix is only real when the exploit is **confirmed closed** — static detection alone is faith-based. Order:

- **TRIAGE (Sentinel + severity)** — classify the finding: severity (CVSS), exploitability, and scope (**own code** vs **dependency CVE** vs **config/secret**). Severity sets urgency; scope sets the route — a dependency CVE routes to `Shift` (upgrade path), not a code patch. **Confirm it is a real vulnerability, not a SAST false positive**, before mobilizing.
- **CONFIRM-EXPLOIT (Probe / Breach, conditional)** — for dynamically-reachable vulns, **prove it is actually exploitable** (DAST / red-team) before fixing: don't burn effort on a false positive, and capture the working exploit as the verification oracle (the security analogue of bug's failing repro test). Skip for self-evident static issues (hardcoded secret, obvious injection sink).
- **FIX (Builder)** — fix the **root cause at the right layer** (parameterize the query, validate/encode at the boundary, rotate-and-vault the secret) — not a surface filter the next payload bypasses. Repo rule: defense at the boundary, don't silence.
- **VERIFY-CLOSED (Probe / Radar + gate)** — **re-run the exploit/DAST: the vuln no longer reproduces.** Radar encodes the attack as a regression test; the existing suite stays green. For secrets: confirm rotation AND removal from git history (a fix that leaves the secret in history is not closed).
- **DETECT (Vigil, conditional)** — add a detection rule (Sigma / Detection-as-Code) so reintroduction or in-the-wild exploitation is caught. Recommended for high-severity or recurring vuln classes.
- **SHIP (Guardian)** — **security-aware PR**: do NOT disclose exploit details in a public commit before the patch is deployed; link to the advisory/CVE; coordinate disclosure timing.

**Add-ons**: `+Crypt` (cryptographic design fix), `+Shift` (dependency CVE → upgrade), `+Cloak`/`+Oath` (privacy/compliance dimension), `+Sentinel` re-scan after fix.

**Anti-patterns prevented**: (1) "fixing" a SAST false positive (TRIAGE + CONFIRM-EXPLOIT), (2) band-aid filter the next payload bypasses (FIX root-cause/right-layer), (3) faith-based fix never validated against the actual exploit (VERIFY-CLOSED re-run), (4) same vuln class silently reintroduced (DETECT rule), (5) premature exploit disclosure in a public commit (SHIP security-aware PR), (6) secret "removed" but still in git history (VERIFY-CLOSED history check).

## REFACTOR Phase Contract

Refactoring's invariant is **no external behavior change** — and the only proof of that is a test suite that passes identically before and after. The order matters:

- **SAFETY-NET (Radar, first — green before you refactor)** — refactoring is safe **only under a passing suite**; the tests are what prove behavior is preserved. Confirm the code under refactor has green coverage; if it's untested, add **characterization tests that pin current behavior FIRST**. You cannot preserve behavior you never captured. (This is the Fowler precondition the default `Zen → Radar` order inverts.) **Skip only** for tool-assisted pure rename/extract where the compiler/type-system guarantees equivalence.
- **SCOPE-GUARD** — confirm this is **internal-only**: no public API / signature / output-contract change. If external behavior must change, it is a `feature` or `bug`, not a refactor — redirect. Keeps the invariant honest.
- **REFACTOR (Zen)** — rename / extract / constant-ify / dead-code removal in **small reversible steps**. `+Atlas` when module boundaries move, `+Grove`/`+Nest` for structure, `+Sherpa` for multi-file.
- **VERIFY-EQUIVALENCE (Radar + gate)** — re-run the **SAME suite**: identical pass results (no behavior delta), build/lint green, public surface unchanged. Not just "tests pass" — *the same tests pass the same way*. A refactor that changes a test's expected value is a behavior change masquerading as a refactor.
- **SHIP (Guardian)** — **behavior-neutral** PR/commit, reviewable as a pure refactor, kept separate from any behavior-changing work.

**Anti-patterns prevented**: (1) refactoring untested code with no behavior proof (SAFETY-NET green-first), (2) "refactor" that changes external behavior (SCOPE-GUARD), (3) silent behavior drift hidden inside a refactor (VERIFY-EQUIVALENCE same-suite-same-result), (4) refactor + behavior change mixed into one unreviewable commit (SHIP behavior-neutral).

## OPTIMIZE Phase Contract

Performance work has one law — **measure, don't guess** — and the default `Bolt/Tuner → Radar` chain skips the measurement entirely. Order:

- **MEASURE-FIRST (Bolt / Tuner profile)** — profile to find the **actual hotspot** and capture a **quantified baseline** BEFORE changing anything. Bolt profiles code-side (render / CPU / allocation), Tuner runs `EXPLAIN ANALYZE` on queries. Optimizing without a profile optimizes the wrong thing — the #1 perf anti-pattern. **No baseline number → no optimize.**
- **TARGET-GATE** — set a **quantified target** (e.g. p95 < 200ms, render < 16ms, query < 50ms) and a stop condition. Without a target, optimization is unbounded — micro-tuning past the point of user-perceptible value. Reject "make it faster" with no number.
- **OPTIMIZE (Bolt / Tuner)** — apply the fix **at the measured hotspot**: Bolt → re-render reduction / memoization / lazy-load / caching / async; Tuner → query plan / index. `+Schema` when an index or migration is recommended.
- **VERIFY-SPEEDUP + NO-REGRESSION (Radar + gate)** — re-run the **same benchmark**: the metric actually moved toward target (**prove the speedup with a number, never a claim**), behavior is unchanged (correctness suite green — an optimization that alters output is a bug), and **no other metric regressed** (a latency win that blows up memory or breaks the cold path is not a win).
- **ITERATE (bounded)** — if the target is unmet and the last pass still yielded meaningful gain, **re-profile** (the hotspot moves after each fix) and optimize the new top hotspot; stop at target-met or diminishing returns. Hand off to `kaizen` for multi-axis continuous improvement.
- **SHIP (Guardian)** — PR with **before/after numbers** embedded (baseline → result vs target) so the win is auditable.

**Add-ons**: `+Schema` (DB index/migration), `+Siege` (load-test the speedup under realistic traffic), `+Beacon` (SLO/observability to confirm the target in production), `+Flux` (first-principles reframe when stuck).

**Anti-patterns prevented**: (1) optimizing by guess / wrong hotspot (MEASURE-FIRST profile), (2) unbounded micro-optimization (TARGET-GATE), (3) claimed-but-unmeasured speedup (VERIFY prove-with-number), (4) perf win that silently changes behavior (VERIFY correctness suite), (5) perf win that regresses another metric (VERIFY no-regression), (6) hotspot moved but kept optimizing the old one (ITERATE re-profile).

## Sherpa Skip Conditions

Skip Sherpa from the default chain only when ALL apply:
- Task touches ≤ 2 files
- No implicit intermediate steps
- Single atomic operation completable in one focused step

## Chain Adjustment Rules

- `3+` files touched → add Sherpa (if not already in chain).
- Ambiguous or multi-step requirements → add Sherpa.
- `3+` test failures → add Sherpa for re-decomposition.
- Security-sensitive changes → add Sentinel or Probe.
- UI changes → add Muse or Palette.
- Slow database path → add Tuner.
- `2+` independent implementation tracks → consider Rally.
- `<10` changed lines with existing tests → Radar may be skipped.
- Pure documentation work → skip Radar and Sentinel unless the change affects executable behavior.

## Clarification and Decision Rules

- If context is clear, proceed.
- If unclear, inspect git state and `.agents/PROJECT.md`.
- If confidence remains low, ask the user one focused question.
- If the action is risky or irreversible, confirm before execution.
- Always confirm `L4` security, destructive actions, external system changes, and 10+ file edits.

## Anti-Pattern References

Before expanding a chain, consult the anti-pattern references when the plan starts looking expensive, overly dynamic, or hard to verify:
- Orchestration design risk → `reference/orchestration-anti-patterns.md`
- Decomposition or routing quality risk → `reference/task-routing-anti-patterns.md`
- Production reliability risk → `reference/production-reliability-anti-patterns.md`
- Handoff and schema risk → `reference/agent-communication-anti-patterns.md`
