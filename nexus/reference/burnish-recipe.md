# Burnish Recipe — Design Review-to-Zero Loop

> `/nexus burnish [<surface>]` — capture the **rendered** UI, run an **external multimodal review engine** over the same frozen surface set, fix, re-capture, and repeat until the reviewer returns **zero open hard findings at or above the severity floor** and every declared soft axis reaches its bar. The loop runs **uninterrupted** — no per-cycle confirmation — and is bounded externally, never by the fixer's own taste.

Read this file before executing the `burnish` Recipe. The **split oracle** (§2), the **Finding Charter** (§3), the **Design Finding Ledger** (§4), and the disposition-integrity rules (§5) are what make "until zero" a reachable, honest state for design work instead of an unbounded taste argument.

**Named report:** **Burnish Ledger**. **Resume:** checkpoint-resume (`burnish resume`). **Confirm tier:** announce-and-proceed (no objection window) after a single launch-time blast-radius acknowledgement (§6).

---

## 1. Nature / When to Use / Boundaries

Burnish is the **Loop**-family member whose completion oracle is an *external reviewer's finding set over a rendered artifact*. The reviewer is a separate multimodal engine (`codex` / `agy` via `Judge`) plus deterministic scanners, so **maker ≠ checker holds structurally** — the agent that writes the style change never decides whether the finding is closed.

It is `quell` with the object swapped from a code diff to a rendered surface, and with the one change that swap forces: a **split oracle**, because design findings do not all reduce to a defect count (§2).

Use `burnish` when: a surface has a settled design direction and must be driven to a clean external review before ship · a design review produced a long list you want worked to zero unattended · you want CI-grade craft discipline on UI in-session.

**Invocation:**

| Arg | Default | Meaning |
|-----|---------|---------|
| `<surface>` | current UI scope | Surface set to burnish: routes, screens, or components. **Frozen at BASELINE** together with the breakpoint × state matrix — the loop never widens it. |
| `floor=` | `medium` | Severity floor for **hard** findings. Below-floor findings are recorded but do not block ZERO. `floor=info` rarely converges. |
| `engines=` | `codex` | Review roster, delegated to `Judge`: `codex` \| `codex+agy` \| `tri`. Multi-engine raises finding volume and cost; concurrence labels feed triage. |
| `profile=` | `general` | Loop profile (§7): `general` \| `faithful`. A profile swaps the gate, the fixer roster, and the out-of-bounds rule — never the termination contract. |
| `max_cycles=` | `4` | Hard ceiling (§8). Lower than `quell`'s 6 — every cycle re-captures the full matrix, so cycles cost more. |
| `resume` | — | Resume from the persisted Ledger. |

| Not this | Route to | Why |
|----------|----------|-----|
| Set the design **direction** (what should it look like?) | `restyle` | burnish executes against a settled direction; it never invents one. Natural pair: `restyle` → `burnish` |
| Iterate a surface to a **rubric** bar with internal evaluators | `restyle` / `converge` | burnish's blocking oracle is an *external* finding set; the rubric is only its soft floor |
| Prove every critical task still **completes** under degraded conditions | `crucible` | Operability floor (binary per condition cell), not craft findings |
| Prove the surface is **recognizably ours** | `silhouette` | Distinction, not defect closure |
| Prove every surface **derives from the design system** | `lattice` | Conformance residue with a frozen denominator; burnish consumes token residue as *one* hard class, it does not own the system proof |
| Maximize the **ceiling** of a flagship surface | `runway` | Tournament + rubric ceiling; burnish closes a floor of findings |
| Design weaknesses in **code** structure | `anneal` | Code design, not the rendered surface |
| Review a **code diff** to zero | `quell` | Same machinery, different object |
| Loop must survive session end / run for hours | `orbit` skill | burnish is attended-but-uninterrupted, in-session |
| Just want one design review, no fixing | `palette` / `echo` direct | Minimum viable chain |

**Scale:** 5-13 agents per cycle × ≤ 4 cycles, plus 4 at BASELINE. Medium-to-high cost (multiplied by cycle count; the surface × breakpoint × state matrix and the finding volume are the governors, not repo size).
*Range derivation:* TRIAGE 1-2 (adjudicator + `Magi` on dispute) + FIX 1-5 (one per finding class, file-partitioned) + GATE-A 2 (`Vector` re-capture + gate) + REVIEW 1-3 (`Judge` + per-engine review subagents) + ARBITRATE 0-1 → floor 1+1+2+1+0 = **5**, ceiling 2+5+2+3+1 = **13**. BASELINE adds `Vector` + `Radar` + `Palette` + `Judge` = **4**, once.

---

## 2. The Split Oracle — why "zero design findings" needs two halves

A code reviewer's finding set is finite: a defect either exists or it does not. A design reviewer's is not — taste generates findings forever, so a naive review-to-zero loop on UI never terminates. Burnish splits the finding space and gives each half the oracle it can actually satisfy.

| Class | Examples | Oracle |
|-------|----------|--------|
| **HARD** — machine-checkable, has a right answer | WCAG AA violations · contrast ratio · touch-target size · focus order / keyboard trap · overflow, clipping or truncation at a declared breakpoint · missing empty/loading/error state on a declared component · token residue (raw hex/px where a token exists) · a declared perf budget (LCP/CLS) | **`open(≥floor) == 0`** |
| **SOFT** — judgment, no ground truth | hierarchy · spacing rhythm · typographic scale · motion appropriateness · density · copy tone · brand fit | **every declared axis ≥ 2** on the 0-3 scale of `reference/evaluator-loop-protocol.md` (cited, not a new scale) |

**ZERO (ACCEPT)** ⟺ `hard_open(≥floor) == 0` **∧** every declared soft axis ≥ 2 **∧** the Appearance Gate is green **∧** the final review output is attached verbatim as evidence.

Reaching for literal zero on the soft half is the recipe's defining failure mode, and §3 is what prevents it.

---

## 3. The Finding Charter — pre-committed, so taste cannot expand the run

At BASELINE, before the first review, the run **freezes a Charter**: the hard finding classes in scope, the soft axes that will be scored with their target bars, and the surface × breakpoint × state matrix. The same pre-commitment discipline `silhouette` uses for its Sameness Ledger and `crucible` for its declared denominator.

A finding that lands outside the Charter is `OUT-OF-CHARTER`: recorded with its evidence, **non-blocking**, and reported as a follow-up. It is never silently dropped and never allowed to consume a fix cycle. Widening the Charter mid-run is a new run, not a cycle.

**Grounding requirement.** Every finding carries a **locus** — `surface@breakpoint@state / component-or-role / (screenshot region | code ref | WCAG SC id | heuristic id)` — plus **expected vs observed**. A finding with no locus is `NEEDS-INFO` and stays `OPEN`; the adjudicator must either ground it or refute it with evidence (§5.2). "Feels cluttered" is not a finding until it names what and where.

---

## 4. The Design Finding Ledger — why zero is reachable

The Ledger is the loop's persistent memory (`_common/LOOP_PRECONDITIONS.md` #4) and the state a resume restores.

**Fingerprint** (identity across cycles): `sha1(surface_id ⊕ breakpoint ⊕ state ⊕ component_or_role ⊕ finding_class ⊕ normalized_message)`. **Pixel coordinates, screenshot hashes, and DOM indices are excluded** — they change on every fix, and a coordinate-keyed ledger reports every finding as new forever. This is `quell`'s line-number exclusion, transposed.

**Per-finding record:** `fingerprint · surface@breakpoint@state · component · class (HARD/SOFT) · severity · locus · expected/observed · engine(s) + concurrence · first_seen_cycle · disposition · disposition_evidence · closed_in_cycle`.

**Disposition vocabulary** (every finding carries exactly one; nothing is silently dropped):

| Disposition | Meaning | Counts toward ZERO? |
|-------------|---------|---------------------|
| `OPEN` | actionable, not yet fixed | **blocks** (hard, if severity ≥ floor) |
| `FIXED-VERIFIED` | fix landed **and** the finding is absent from a subsequent review of the same frozen matrix | closed |
| `FALSE-POSITIVE-RATIFIED` | independently checked against the rendered artifact and refuted | closed |
| `WONTFIX-RATIFIED` | real but deliberately not fixed; justification recorded | closed |
| `DEFERRED` | real, fix is outside the frozen surface set | closed **for this run**, reported as residual + follow-up |
| `DEFERRED (identity-changing)` | fix would change IA, copy meaning, or brand-level tokens (§5.3) | closed **for this run**, routed out |
| `OUT-OF-CHARTER` | outside the frozen Charter (§3) | recorded, does not block |
| `BELOW-FLOOR` | hard finding below `floor` | recorded, does not block |
| `FROZEN` | oscillating (§ below) — excluded from further fix cycles, escalated | does not block; reported as a `BLOCK`-class residual |

**Oscillation detection:** a fingerprint that returns to `OPEN` after having been `FIXED-VERIFIED` is `re-emerged`. First re-emergence → one more fix attempt with the prior fix diff and the prior/current screenshots attached as context. Second re-emergence → `FROZEN` + `BLOCK` escalation showing both attempts. A ledger diff per cycle (`closed / persisting / net-new / re-emerged`) plus the soft-axis score delta is the loop's progress signal and the input to the diminishing-returns bound.

---

## 5. Disposition Integrity — the rule that keeps zero honest

The cheapest path to zero design findings is to call every one of them a matter of taste. Four rules make that impossible:

1. **The fixer never disposes.** An agent that produced a style change in cycle N cannot set `FALSE-POSITIVE-RATIFIED`, `WONTFIX-RATIFIED`, or `OUT-OF-CHARTER` for any finding in cycle N. Dispositions are set by an independent adjudicator (`Palette` for heuristic/a11y grounding, `Echo` for persona relevance; `Magi` on dispute) — the Generator-Evaluator separation of `reference/evaluator-loop-protocol.md`, applied to triage.
2. **Refute-polarity dismissal.** To mark a finding `FALSE-POSITIVE-RATIFIED`, the adjudicator must attempt to **confirm** it against the rendered artifact and fail, recording the evidence (`_common/ADVERSARIAL_REFUTATION.md` polarity rule). For hard classes the confirmation attempt is the deterministic scanner's own output, not an opinion. `NEEDS-INFO` stays `OPEN`.
3. **Identity is out of bounds, always.** A fix that changes information architecture, the *meaning* of copy, or a brand-level token is `DEFERRED (identity-changing)` with an explicit route (`restyle direction=` / `rebrand` / `hallmark` / `prose`), never applied inside the loop. This holds in **both** profiles: `Vision` is deliberately absent from every roster, because a polish loop that can re-direct the design is no longer bounded by anything.
4. **`WONTFIX` is a written argument, not a shrug.** It records why the current behavior is intended, what constraint makes the finding inapplicable, and the blast radius of fixing it anyway. `WONTFIX` on a CRITICAL/HIGH **hard** finding is **Ask First**, never auto-ratified — an a11y violation is not a taste call.

`FIXED-VERIFIED` is likewise never self-declared: it requires the finding's *absence* from a fresh review of the same frozen matrix. A fix with no confirming re-capture and re-review is `OPEN`.

---

## 6. Appearance Gate — the design analogue of `quell`'s Green Gate

Runs every cycle. A red gate injects a synthetic **blocking** finding into the Ledger, which the next cycle fixes first — the loop can never reach zero on a surface that does not render.

1. **Render** — every declared surface × breakpoint × state captures successfully (`Vector`). A capture failure is a build failure, not a missing screenshot.
2. **A11y non-regression** — `Palette` re-checks against the BASELINE a11y result; a prettier-but-less-accessible cycle fails the gate (inherited from `restyle` Phase 4).
3. **Behavior non-regression** — `Radar`: same suite, same result.
4. **SPILL** — any visual diff on a surface **outside** the frozen set is a `SPILL` finding and **blocks at any severity**, because it falsifies the recipe's scope invariant rather than lowering its quality. Appearance parity is judged per `_common/DIFFERENTIAL_PARITY.md` (oracle origin: the run's own BASELINE capture, one forward baseline).

**Confirm gate — one acknowledgement, then uninterrupted.** BASELINE announces the frozen surface set, the Charter, the finding counts by class and severity, and the declared bounds. If that blast radius trips an Ask First line (10+ files, brand-token reach, an L4 finding), that is the **one** confirmation for the whole run — `Confirm-before-launch`. Approving it approves the loop, not one cycle. After launch the loop stops only on §8's bounds, or on a new Ask First trigger the acknowledgement did not cover.

---

## 7. Profiles

A profile specializes **three** things — the gate, the fixer roster, and what "out of bounds" means — and **nothing else**. The termination contract (§8), the Charter (§3), the Ledger (§4), and disposition integrity (§5) are profile-invariant: a profile can never buy a cheaper exit.

| | `profile=general` (default) | `profile=faithful` |
|---|---|---|
| Gate | Appearance Gate (§6) | Appearance Gate **+ reference conformance** against the declared source of truth (Figma frame / Design Brief / design system) |
| Fixer roster | `Artisan` · `Flow` · `Muse` · `Prose` · `Ink` | **`Muse`** (token-first) · `Frame` (reference context) · `Artisan`. `Prose`/`Ink` are **not** in the roster |
| Out of bounds → `DEFERRED` | outside the frozen surface set | outside the frozen surface set **or** the fix diverges from the reference |
| Extra blocking class | — | **`REFERENCE-DRIFT` — blocks at any severity** |

`profile=faithful` is for "make it match the design file / the system", where divergence from the reference is the defect being closed, and inventing a better-looking alternative is out of scope by construction. Its `REFERENCE-DRIFT` class is the exact analogue of `quell profile=refactor`'s behavior-drift finding: it falsifies the invariant, so `floor` does not apply to it. A run with no declared reference cannot use this profile — it is `BLOCK (no reference of record)`, never a silent fall-back to `general`.

---

## 8. Termination Contract

"Until findings are zero" is only a *success* exit. Every run declares all bounds up front; **none is waivable by AUTORUN** (`_common/LOOP_PRECONDITIONS.md` #2 is contract-level).

| Bound | Default | Stop behavior |
|-------|---------|---------------|
| **ZERO (ACCEPT)** | — | The §2 conjunction holds → `ACCEPT`. The success exit. |
| `max_cycles` | `loop ≤ N cycles (default N=4)` | `cap-reached` — stop, report best-so-far + residual open findings + `burnish resume`. |
| `token_budget` | run-level | `budget-reached` — stop + report (shared pool, not per-cycle). |
| diminishing-returns | **net open hard-finding count fails to decrease AND the aggregate soft score improves by < 0.2 for 2 consecutive cycles** | `diminishing-returns (Δ < ε)` — stop + report. Both halves of the oracle must stall; progress on either one continues the loop. |
| `BLOCK` | — | Oscillation (§4), a fix whose only form is out of scope, `profile=faithful` with no reference of record, or Agent Tennis (fixer vs reviewer disagreeing 3+ turns without progress — Nexus circuit-breaker) → stop + escalate. |

**"Never stops" is implemented as: no confirmation pauses, not as an unbounded loop.** Every non-`ACCEPT` exit ships best-so-far with the residual gap named.

---

## 9. Phase Contract (AUTORUN chain template)

```
GATE ──── _common/LOOP_PRECONDITIONS.md (5-point) + engine preflight
          Judge[availability: multimodal review engine — codex, or agy per
                _common/CLI_COMPATIBILITY.md §9.2; image input per
                _common/IMAGE_INPUT.md]
   ▼
BASELINE  Vector[capture the frozen surface × breakpoint × state matrix]
          Radar[behavior green] + Palette[a11y baseline]  →  Appearance Gate v0
          FREEZE Charter: hard classes · soft axes + bars · the matrix (§3)
          ★ profile=faithful: declare the reference of record; none ⇒ BLOCK (§7)
          Judge[external multimodal review @frozen matrix] → Ledger v0
          ANNOUNCE surfaces + counts + bounds + profile → §6 single acknowledgement
   ▼
┌─ LOOP (until ZERO | bound hit per §8) ──────────────────────────────────────┐
│  TRIAGE     Palette/Echo[ground each finding: VERIFIED/REJECTED/NEEDS-INFO,  │
│             dedupe by fingerprint, classify HARD/SOFT/OUT-OF-CHARTER,        │
│             severity vs floor] → Fix Slate                                   │
│             ★ dispositions by adjudicator only, never by cycle-N fixer (§5)  │
│  FIX ∥      per finding class, file-ownership partitioned (_common/PARALLEL) │
│             layout/structure → Artisan · motion → Flow · raw values → Muse   │
│             (token-first) · microcopy → Prose · assets → Ink                 │
│             ★ identity-changing ⇒ DEFERRED, never applied (§5.3)             │
│             ★ profile=faithful: Muse-led; reference divergence ⇒ DEFERRED    │
│  GATE-A     Vector[re-capture] → Appearance Gate (render / a11y / behavior / │
│             SPILL) — red ⇒ synthetic BLOCKING finding into the Ledger (§6)   │
│  REVIEW     Judge[re-review @same frozen matrix, same engines]               │
│             ★ profile=faithful: + reference-conformance question;            │
│               a REFERENCE-DRIFT finding blocks at any severity (§7)          │
│  DIFF       Ledger diff: closed / persisting / net-new / re-emerged          │
│             + soft-axis score delta (§4)                                     │
│  GATE       §2 conjunction holds            → ACCEPT (ZERO)                  │
│             re-emerged ×2                   → FROZEN + BLOCK                 │
│             hard Δ ≥ 0 ∧ soft Δ < 0.2 ×2    → diminishing-returns → stop     │
│             cycle N / budget                → cap-reached / budget-reached   │
│             else                            → carry Ledger into next cycle   │
└──────────────────────────────────────────────────────────────────────────────┘
   ▼
DELIVER ── Burnish Ledger (§11) + handoff: Guardian[commit/PR] ;
           crucible? [operability floor] ; acceptance? [merge gate]
```

**Checkpoint-resume:** the Ledger + Charter + frozen matrix + BASELINE captures + per-cycle diff are persisted at every `GATE` boundary, so `burnish resume` restarts mid-convergence with dispositions, baselines, and trajectory intact. The Ledger file **is** the loop's state.

**Loop Precondition Gate verdict** (report all five in §11): #1 completion oracle — **converted** (the raw ask "improve the design" is unverifiable; the §2 split oracle converts it to `hard_open == 0 ∧ every declared soft axis ≥ 2`, both machine-checkable given §3's Charter); #2 hard-stop — **met** (`max_cycles` + budget + diminishing-returns, external to the fixer); #3 maker ≠ checker — **met structurally** (external review engine + deterministic scanners + §5); #4 persistent memory — **met** (Ledger + baseline captures); #5 drift awareness — **run risk**: many small local fixes can erode a surface's coherence even while the finding count falls, so the Appearance Gate is mandatory each cycle and a side-by-side BASELINE-vs-final capture is reported at DELIVER. Never assert design improvement from the finding count alone.

---

## 10. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Nit-storm never converges** (taste generates findings forever) | Split oracle (§2): the soft half targets `≥ 2` per axis, never zero; `floor=medium` on the hard half |
| **Charter creep** (new "issues" invented after seeing the surface) | Finding Charter frozen at BASELINE (§3); anything outside is `OUT-OF-CHARTER`, non-blocking |
| **Ungrounded findings** ("feels cluttered") | Locus + expected/observed mandatory (§3); no locus ⇒ `NEEDS-INFO`, stays `OPEN` |
| **Every finding reported as new after a 1px change** | Fingerprint excludes coordinates, screenshot hashes, and DOM indices (§4) |
| **Dishonest zero** (fixer dismisses everything as taste) | Disposition integrity (§5): fixer ≠ adjudicator, refute polarity, `WONTFIX` on a CRITICAL/HIGH hard finding is Ask First |
| **Phantom progress** (fix declared done, never re-captured) | `FIXED-VERIFIED` requires absence from a fresh review of the same frozen matrix (§5) |
| **Prettier but less usable** | A11y non-regression is a gate condition, not a finding class (§6.2) |
| **The polish loop becomes a redesign** | Identity changes are always `DEFERRED` with a route; `Vision` is on no roster (§5.3) |
| **Fixing one screen breaks another** | `SPILL` — visual diff outside the frozen set blocks at any severity (§6.4) |
| **Zero findings on a surface that does not render** | Render gate: a capture failure injects a blocking finding (§6.1) |
| **Oscillation** (fix A re-opens B) | Fingerprint re-emergence → `FROZEN` + `BLOCK` on the second recurrence (§4) |
| **Infinite churn with no net gain** | diminishing-returns on *both* halves of the oracle (§8) |
| **Unbounded spend under "don't stop"** | §8 bounds are contract-level; "don't stop" means no confirmation pauses, never no ceiling |
| **Confirmation storm** (Ask First fires every cycle on a wide surface set) | Blast radius front-loaded into one launch-time acknowledgement (§6) |
| **Coherence erosion masked by a falling finding count** | Precondition #5 as a run risk + BASELINE-vs-final side-by-side at DELIVER (§9) |
| **`faithful`: "improving on" the reference instead of matching it** | `REFERENCE-DRIFT` blocks at any severity; divergent fixes are `DEFERRED` (§7) |

---

## 11. Output

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus the **Burnish Ledger**:

- **Exit reason**: `ACCEPT (ZERO)` | `diminishing-returns (Δ < ε)` | `cap-reached` | `budget-reached` | `BLOCK`.
- Frozen surface × breakpoint × state matrix + **Charter** (hard classes, soft axes + bars) + **profile** + review engines + `floor` + declared bounds. Under `profile=faithful`: the reference of record and its version.
- **Per-cycle trajectory**: hard `open(≥floor)` at cycle entry → closed / net-new / re-emerged → open at exit, alongside the per-axis soft scores.
- **Full finding table**: fingerprint (short), `surface@breakpoint@state / component`, class, severity, disposition, and for every `FALSE-POSITIVE-RATIFIED` / `WONTFIX-RATIFIED` / `DEFERRED*` / `OUT-OF-CHARTER` / `FROZEN` record, the ratifying agent + evidence. No finding appears without a disposition.
- **Evidence**: the final review invocation and its verbatim output, plus the final capture set. A ZERO claimed without an attached final review is `UNVERIFIED` (`reference/autonomy-quality-protocol.md` Q10).
- **BASELINE vs final captures**, side by side, per surface — the drift-awareness artifact (§9).
- Appearance Gate result per cycle (render / a11y / behavior / SPILL).
- Loop Precondition Gate verdict, five entries (§9).
- **Residual Ledger** (typed, never a free-text follow-up list): each `DEFERRED (identity-changing)` with its route (`restyle direction=` / `rebrand` / `hallmark` / `prose`), each `OUT-OF-CHARTER` cluster as a candidate next Charter, each `FROZEN` item as a `BLOCK`-class residual, plus the completion-sweep line. `burnish resume` command on any non-`ACCEPT` exit.
- Follow-up handoff on `ACCEPT`: `Guardian` (commit/PR), then `crucible` (operability floor) or `acceptance` (merge gate).

**Done** is deliverable-relative: the surfaces in the frozen set render, pass the Appearance Gate, and carry zero open hard findings at or above the floor with every declared soft axis at its bar. Surfaces outside the frozen set are a Q2 non-goal, not a residual.

---

## 12. Decision Tree vs Neighbors

```
Driving a UI surface to a clean state?
  Oracle is an EXTERNAL REVIEWER's finding list over the rendered surface → burnish
    └ the surface must match a design file / system reference → burnish profile=faithful
    └ the direction itself is unsettled → restyle first, then burnish
    └ must survive session end / run unattended → orbit skill
  Oracle is a RUBRIC score set by an internal evaluator      → restyle (or converge)
  Oracle is TASK COMPLETION under degraded conditions        → crucible
  Oracle is BLIND ATTRIBUTION vs competitors                 → silhouette
  Oracle is SYSTEM CONFORMANCE with a frozen denominator     → lattice
  Oracle is a TOURNAMENT for the best possible surface       → runway
  Object is a CODE DIFF, not a rendered surface              → quell
```

`burnish` = external-reviewer-to-zero loop on rendered UI with a split oracle · `quell` = the same loop on a code diff · `restyle` = direction + rubric-scored improvement · `crucible`/`silhouette`/`lattice` = design proofs with their own single oracles.

Natural sequence: `restyle` (decide and implement the direction) → `burnish` (drive it to a clean external review) → `crucible` (prove the floor) → `acceptance` (merge proof).

---

## 13. Shared Protocols (cited, not re-derived)

| Protocol | What burnish takes from it |
|----------|----------------------------|
| `_common/LOOP_PRECONDITIONS.md` | The five-point gate; run before cycle 1, verdict reported in §11 |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, the 0-3 soft scale and its `≥ 2` bar, single termination oracle, flatten rule (`converge burnish` is **redundant** — burnish already owns a loop and an oracle) |
| `reference/quell-recipe.md` | The Ledger/disposition/oscillation machinery this recipe transposes; the code-diff sibling |
| `reference/restyle-recipe.md` | The design direction and Design Brief burnish executes against; the a11y-non-regression gate condition |
| `_common/ADVERSARIAL_REFUTATION.md` | Refute-polarity discipline for dismissals (§5.2) |
| `_common/DIFFERENTIAL_PARITY.md` | Appearance-parity posture for `SPILL`: oracle origin = the run's own BASELINE capture, one forward baseline |
| `_common/IMAGE_INPUT.md`, `_common/CLI_COMPATIBILITY.md` §9.2 | Screenshot input handling; agy headless capture (pty allocation, artifact-not-stdout) |
| `_common/PARALLEL.md` | File-ownership partitioning for concurrent fixers |
| `reference/autonomy-quality-protocol.md` | Decision Ledger for every judgment made without the user, evidence-bound claims, Acceptance Provenance, completion integrity (Q16-Q22) |
| `_common/PROOF_CARRYING.md` | Only when handing off to `acceptance` — burnish produces the clean surface, acceptance carries the merge proof |
