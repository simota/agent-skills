# Chorus Recipe — Cross-Platform Coherence Proof

> `/nexus chorus "<product or flow>"` — prove that each platform build is **idiomatic to its own platform** *and* **recognizably the same product**, simultaneously. The two halves pull against each other, and every cross-platform failure is a miscategorization of one property as the other: shipping a web layout on iOS (idiom lost), or diverging terminology and task flow per platform (kinship lost). Chorus makes the split explicit as a ratified **Invariant/Variant Contract**, then measures both sides against it.

Read this file before executing the `chorus` Recipe.

---

## 1. Nature / When to Use / Boundaries

**The roster can port and it can implement, but it cannot prove coherence.** `port` designs a web→native porting strategy with a feature-parity matrix. `native` implements one platform well. `rebrand` propagates a brand across touchpoints. None of them ever asks the two questions together: *does each build feel native here?* and *would a user who learned this on one platform succeed on the other?*

Chorus's identity is four things no sibling carries together:

1. **The Invariant/Variant Contract.** Before measurement, every relevant property is classified `invariant` (must be identical across platforms — information architecture, terminology, task flow order, brand tokens, data/state semantics, permissions outcome) or `variant` (must differ — navigation paradigm, gesture vocabulary, system controls, typographic defaults, motion physics, permission *flow*, platform affordances). Almost every cross-platform argument is really a disagreement about which list an item belongs to, and the contract settles it once.
2. **A two-sided gate over one oracle.** The **Idiom Gate** (platform-system conformance) and the **Kinship Gate** (same-product recognition + learned-transfer) are two *measurements of the same contract*, not two competing oracles — the contract arbitrates, so a fix that raises one gate by lowering the other is rejected rather than debated.
3. **Learned transfer as evidence.** Kinship is not "they look similar." A persona that completes the task on platform A must complete it on platform B **first try**, with the friction delta recorded. Recognition without transfer is cosmetic coherence.
4. **Idiom measured against published systems, not taste.** Apple HIG and Material 3 are Tier-2 published-system sources per `_common/PROPORTION_AND_SPACING.md` §1. Conformance claims cite them; "feels native" is never a pass criterion on its own.

### Use `chorus` for

- A product shipped on ≥ 2 platforms (web / iOS / Android / macOS) where the builds have drifted apart or were built by different teams.
- Immediately after a `port` run, to prove the port actually landed on both axes.
- Before a cross-platform launch where inconsistency is a support-cost and trust event.
- Settling a recurring team argument about what must match across platforms — the contract is the durable output even if nothing else changes.

### Not this — route to

| Not this | Route to | Why |
|----------|----------|-----|
| Design the web→native porting **strategy** (parity matrix, architecture, phasing) | `port` (skill) | Chorus verifies a shipped result; port plans one. `port` → `chorus` is a plan→prove pair |
| Implement one platform's UI natively | `native` (skill) | Single-platform build |
| Build a feature on iOS/Android | `MOBILE_NATIVE` task type | Chorus proves coherence, it does not add capability |
| Propagate a settled brand across every touchpoint | `rebrand` | Completeness of a brand change on one system, not cross-platform idiom |
| Prove one system's internal token/component conformance | `lattice` | Inside one platform's system; chorus is *between* platform systems (they compose: run `lattice` per platform, then `chorus` across) |
| Prove tasks complete under hostile conditions | `crucible` | Conditions axis, not platform axis |
| Maximize one flagship screen's design | `runway` | Ceiling on one surface |
| Only one platform ships today | `restyle` / `native` | Chorus's precondition is ≥ 2 platforms with a shared product surface |

**Scale: 14-30 agents × ≤3 cycles, 5-10× `feature` cost.** Per-phase: P0 ≈ 1 · P1 ≈ 2-3 (contract authoring) · P2 ≈ 2 per platform (audit, parallel) · P3 ≈ 4-6 (both gates: idiom scoring per platform + kinship panel + transfer test) · P4 ≈ 3-7 per cycle (reconcile + re-measure both gates) · P5 ≈ 1.

*Range derivation (keep reconciled when a phase figure changes):* floor = 2 platforms, one flow, ACCEPT on cycle 1 → 1+2+4+4+2+1 = **14**; ceiling = 3 platforms, multiple flows, 3 cycles → 1+3+6+6+(7+4+2)+1 = **30**. The stated range is the sum of the per-phase figures, not an independent estimate. **Confirm-before-launch always** (intentional parity with `runway`/`silhouette`).

**Model selection (Plan-and-Execute):** the Phase 1 Invariant/Variant Contract and the Phase 4 conflict adjudication are judgment-heavy → plan-tier (opus / Fable 5). Platform audits, gate measurement, and implementation → Sonnet 5 default. The kinship panel is engine-diverse where the hub allows.

---

## 2. Termination Bound

Reconciliation **`loop ≤ 3 cycles (default N=3)`**. Exit reasons use the canonical vocabulary:

| Exit reason | Chorus-specific meaning |
|-------------|------------------------|
| `ACCEPT` / `target-met` | **both** gates pass on their pre-declared thresholds: zero open Idiom violations on ratified `variant` properties, **and** the Kinship measurement (same-product attribution + first-try learned transfer) meets threshold — with no `invariant` property differing across platforms |
| `diminishing-returns (Δ < ε)` | a cycle moved neither gate — report the open violations on each side and the contract items they trace to |
| `cap-reached` | 3 cycles with one gate open → deliver the contract + both measurements + the named residual per platform |
| `BLOCK` | **`contract-conflict`** — an item cannot be satisfied as classified: honoring the platform idiom necessarily breaks the invariant (or vice versa). One user-ratified **contract amendment** is permitted (§6); a second conflict exits `BLOCK` with the finding, because at that point the product's cross-platform premise is the problem, not its implementation |

On any non-`ACCEPT` exit, both gate results are reported per platform, never aggregated into one score. "83% coherent" hides which platform is the outlier, which is the only actionable fact.

## 3. Confirm / Safety Gate

- **Phase 0 framing: Confirm before launch — always** (unconditional; intentional parity with `runway`/`silhouette`, not drift). Surfaces: the platform set, the shared flow(s) in scope, both gate thresholds, and the cost envelope — plus a cheaper-path recommendation (`port` when the ask is really a porting *plan*, `native`/`restyle` when only one platform is in question).
  **Precondition:** ≥ 2 platforms with a shared product surface, each shipped or specced. One platform → the run stops and routes to `native`/`restyle`.
- **Phase 1 Invariant/Variant Contract: contract-level checkpoint; AUTORUN cannot skip.** This classification *is* the oracle; a contract the user does not recognize as theirs produces a coherence proof about the wrong product. Every item lands on exactly one list — an unclassified property is a gap, not a default.
- **Contract amendment (§6): contract-level, at most once.** Re-classifying an item mid-run requires user ratification and a re-measurement of both gates so the trajectory stays comparable.
- **Phase 4 implementation: standard Ask First tiers** (10+ files, brand-level token changes) apply unchanged, per platform.
- On a Fable 5 hub the Phase 0 gate subsumes the F8 cost gate — one confirmation, not two.

## 4. Resume

**Checkpoint-resume** (≥ 4 phases; `chorus resume`): persist the ratified Invariant/Variant Contract + both thresholds at Phase 1 exit; persist the per-platform audit at Phase 2 exit; persist both gate measurements per cycle at each Phase 4 boundary, including the panel composition (a resumed kinship measurement with a stale panel measures memory, not recognition — §5 requires a fresh panel each round).

---

## 5. Phase Contract (AUTORUN chain template)

```
Phase 0   FRAMING ★Confirm-before-launch (always)
          precondition: ≥2 platforms with a shared surface → else route to native / restyle
          Nexus[platform set + flows in scope + both thresholds + envelope
               + cheaper-path recommendation → port (planning) / native (single platform)]
   ▼
Phase 1   CONTRACT ★contract-level checkpoint (AUTORUN cannot skip; plan-tier)
          Magi ‖ Port? ‖ Vision — classify every relevant property, exactly one list each:
          ┌ INVARIANT (must be IDENTICAL): information architecture · terminology and labels ·
          │            task flow order and step count · brand tokens (colour/type intent) ·
          │            data & state semantics · the OUTCOME of permission/auth flows ·
          │            error meanings · pricing/plan presentation
          └ VARIANT  (must DIFFER): navigation paradigm (tab bar / drawer / sidebar) ·
                     gesture vocabulary · system controls (pickers, sheets, dialogs) ·
                     typographic defaults and dynamic type · motion physics · the FLOW of
                     permission prompts · platform affordances (share sheet, back gesture,
                     widgets, keyboard shortcuts)
          → both GATE THRESHOLDS declared here (idiom: zero open violations on cited
            Tier-1/2 requirements; kinship: attribution + first-try transfer rate)
          → ✓user ratifies → the contract FREEZES (one amendment permitted, §6)
   ▼
Phase 2   AUDIT ‖ per platform (parallel; one branch per platform, no shared mutable state)
          Native/Port?[platform context] ‖ Canon[HIG / Material 3 conformance, cited]
          ‖ Palette[platform a11y: Dynamic Type / TalkBack / VoiceOver]
          ‖ Echo[platform-native persona walkthrough] ‖ Lens[implementation reality]
          → per-platform current state against BOTH lists
   ▼
Phase 3   MEASURE — the two-sided gate (one oracle: the frozen contract)
          (a) IDIOM GATE — per platform, each `variant` property scored against its platform's
              PUBLISHED SYSTEM with a citation (Apple HIG / Material 3 / platform a11y specs;
              Tier 1-2 per _common/PROPORTION_AND_SPACING.md §1). "Feels native" is never a
              pass criterion; a violation names the guideline it violates
          (b) KINSHIP GATE — two measurements, both required:
              · SAME-PRODUCT ATTRIBUTION: a fresh, engine-diverse panel sees the platform
                builds with branding stripped and must judge them one product, not several
              · LEARNED TRANSFER: Echo personas complete the task on platform A, then meet
                platform B COLD → first-try completion + friction delta recorded
          (c) INVARIANT DIFF: every `invariant` property compared literally across platforms
              (terminology table, step count, IA tree) → any difference is an open violation
   ▼
Phase 4   RECONCILE loop ⟲ {
          fix per platform (Native ‖ Artisan ‖ Prose[terminology alignment] ‖ Muse[shared
          tokens] ‖ Flow[platform-appropriate motion]) → RE-MEASURE BOTH GATES
          → CONFLICT RULE: a fix that raises one gate and lowers the other is REJECTED and
            escalated to the contract as a candidate amendment (§6) — never resolved by
            preferring whichever gate the fixer happened to be optimizing
          → per-platform regression: Radar + Voyager/Voyager[ios]?[platform E2E] + Palette[a11y ≥ baseline]
          }⟲  loop ≤ 3 cycles (default 3)
   ▼
Phase 5   DELIVER — Chorus Attestation + Guardian (per platform)
```

## 6. Contract amendment (at most once, user-ratified)

A frozen contract that misclassifies an item will make the loop chase an impossible target. Amendment is permitted when **all four** hold: (a) a Phase 4 conflict is reproducible — the item cannot satisfy both gates as classified; (b) reclassifying it is a genuine product decision, not a convenience (moving "terminology" to `variant` because translating is hard is a convenience, and is refused); (c) the user ratifies; (d) **both gates are re-measured** on the amended contract so the trajectory stays comparable. A second amendment request is refused — two irreconcilable items mean the cross-platform premise itself needs a decision, and the honest exit is `BLOCK (contract-conflict)` with the finding.

## 7. Output Report — **Chorus Attestation** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Invariant/Variant Contract** — the full ratified classification, with any amendment (trigger, change, re-measured delta) or the section omitted when none
- **Platform × property matrix** — every `invariant` property across every platform with `MATCH`/`DIFFER`, and every `variant` property with its per-platform idiom verdict
- **Idiom Gate** — per platform: violations with the **cited guideline** for each, resolved and open
- **Kinship Gate** — same-product attribution result (with panel composition and the stripping method) + learned-transfer results per persona per direction (A→B and B→A), with friction deltas
- **Conflicts** — every fix rejected by the conflict rule, and where it went
- **Per-platform regression** — a11y and E2E results after each cycle
- **Exit reason** (§2 vocabulary) + **both gate results reported per platform, never aggregated**
- **Handoff** — platform capability gaps → `native`/`MOBILE_NATIVE`; a needed re-port → `port`; system-level drift inside one platform → `lattice`

## 8. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Native-looking builds that behave like different products** | Kinship Gate: same-product attribution + first-try learned transfer (Phase 3b) |
| **Identical builds that feel foreign on every platform** | Idiom Gate: per-platform conformance to the published system, cited (Phase 3a) |
| Endless argument about what must match | The Invariant/Variant Contract classifies every property once, user-ratified (Phase 1) |
| Dueling oracles between the two gates | Both gates measure **one** contract; conflicts escalate to the contract, never resolved by fixer preference (§1.2, Phase 4 conflict rule) |
| "Feels native" as a pass criterion | Idiom verdicts cite Tier 1-2 published-system sources; taste is not evidence (§1.4) |
| Cosmetic coherence mistaken for real coherence | Transfer test: recognition alone never passes the Kinship Gate (§1.3) |
| An outlier platform hidden in an average | Both gates reported **per platform**, aggregation forbidden (§2, §7) |
| A contract that made the goal impossible | One user-ratified amendment with both gates re-measured; a second conflict exits `BLOCK` (§6) |
| Amendment used to dodge hard work | Amendment condition (b) refuses convenience reclassification (§6) |
| Parallel platform branches corrupting each other | One branch per platform, hub-spoke ownership, no shared mutable state (`_common/PARALLEL.md`) |
| Panel measuring memory instead of recognition | Fresh, engine-diverse panel per measurement round (§4, §5) |
| Running with a single shipped platform | Phase 0 precondition routes to `native`/`restyle` |
| Confusing this with the porting plan | `port` plans, `chorus` proves — a plan→prove pair (§1 routing table) |

## 9. Shared-Protocol References

| Protocol | What chorus takes from it | Chorus-specific specialization |
|----------|--------------------------|-------------------------------|
| `_common/PROPORTION_AND_SPACING.md` | §1 evidence tiers; platform margin/target conventions | Apple HIG / Material 3 are Tier-2 requirements for the Idiom Gate; Tier 4 folklore may never be a verdict |
| `_common/PARALLEL.md` | Branch definitions, file ownership, merge, rollback | One branch per platform in Phase 2 and Phase 4; ownership is per-platform by construction |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, cycle cap, flatten rule | Two measurements, one oracle (the contract); the loop owns the single termination decision |
| `reference/autonomy-quality-protocol.md` | Q1-Q3 intent contract, Q9 producer ≠ verifier, Q10 evidence-bound claims, Q15 | Q9: the kinship panel and the idiom scorers are independent of the fixers; Q10: every idiom violation carries its cited guideline |
| `_common/DIFFERENTIAL_PARITY.md` | Parity discipline, comparator adequacy | The `invariant` list is a parity oracle across platforms: terminology, step count, and IA are compared literally, not judged |
| `reference/dialogue-protocol.md` | Question craft, Assumption Ledger, checkpoint presentation | Phase 1 contract ratification and the §6 amendment |
| `reference/doc-quality-protocol.md` | W1-W12 | Applies to the Chorus Attestation |
| `reference/verdict-gate.md` | — | `N/A` — chorus proves a property; it delivers no which-feature verdict |

## 10. Decision Tree vs Neighbors

```
How many platforms ship a shared product surface today?
  ONE → native / restyle (chorus has nothing to compare)
  ≥ TWO ↓
Is the ask a PLAN (how to port / what to build) or a PROOF (is what shipped coherent)?
  PLAN → port skill (parity matrix, architecture, phasing) — then chorus to prove it
  PROOF ↓
Is the drift WITHIN one platform's design system, or BETWEEN platforms?
  WITHIN → lattice (per platform; compose: lattice ×N, then chorus across)
  BETWEEN ↓
Is the failure "doesn't feel native" or "doesn't feel like the same product"?
  EITHER, OR BOTH → chorus — contract → audit → two-sided gate → reconcile ⟲ → attest
                    (both are the same contract; that is the point)
```
