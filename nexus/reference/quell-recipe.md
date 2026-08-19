# Quell Recipe — Review-to-Zero Fix Loop

> `/nexus quell [<scope>]` — fix code, run an **external review engine** (Codex by default) over the same scope, and repeat until the reviewer returns **zero open findings at or above the severity floor**. The loop runs **uninterrupted** — no per-cycle confirmation — and is bounded externally, never by the fixer's own judgment.

Read this file **and `_common/FINDING_LEDGER.md`** before executing the `quell` Recipe. The ledger machinery that makes "until zero" reachable and honest lives in that shared protocol; this file declares quell's five slots against it (§3-§4), plus the termination contract (§2) and the `refactor` profile (§5a).

**Named report:** **Quell Ledger**. **Resume:** checkpoint-resume (`quell resume`). **Confirm tier:** announce-and-proceed (no objection window) after a single launch-time blast-radius acknowledgement (§5).

---

## 1. Nature / When to Use / Boundaries

Quell is the **Loop**-family member whose completion oracle is an *external reviewer's finding set*, not a rubric score and not a metric target. The reviewer is a separate engine (`codex review` via `Judge`), so **maker ≠ checker holds structurally** — the agent that writes the fix never decides whether the finding is closed.

Use `quell` when: a change set must be driven to a clean review before merge · a review pass produced a long finding list and you want it worked to zero unattended · you want CI-grade review discipline in-session.

**Invocation:**

| Arg | Default | Meaning |
|-----|---------|---------|
| `<scope>` | `--uncommitted` | Review scope, passed through to `codex review`: `--uncommitted` \| `base=<branch>` \| `commit=<sha>`. **Frozen at BASELINE** — the loop never widens it. |
| `floor=` | `medium` | Severity floor. Findings below it are recorded in the Ledger but do not block ZERO. `floor=info` means literal zero findings (expensive; nit-storms rarely converge). |
| `engines=` | `codex` | Review roster, delegated to `Judge`: `codex` \| `codex+claude` \| `tri`. Multi-engine raises finding volume and cost; the concurrence labels (CONFIRMED/LIKELY/CANDIDATE) feed triage. |
| `profile=` | `general` | Loop profile (§5a): `general` \| `refactor`. A profile swaps the green gate, the fixer roster, and the out-of-bounds rule — never the termination contract. `quell refactor` is the alias. |
| `max_cycles=` | `6` | Hard ceiling (§2). |
| `resume` | — | Resume from the persisted Ledger. |

| Not this | Route to | Why |
|----------|----------|-----|
| Iterate to a **rubric** bar (subjective quality dimensions) | `converge` | quell's oracle is a finding *count*, converge's is a score per dimension |
| One-shot **merge decision** with proof obligations | `acceptance` | acceptance judges whether to merge; quell makes the diff reviewable first. Natural pair: `quell → acceptance` |
| Walk findings **conversationally**, human decides each | `judge pair` | quell is autonomous and batch; pair mode is one finding at a time |
| One known defect, root cause unknown | `bug` | quell consumes a reviewer's list, it does not do RCA on a single symptom |
| Discover **design** weaknesses by internal audit | `anneal` | anneal generates its own slate from six design dimensions; quell's slate comes from an external reviewer on a diff |
| Drive a **rendered UI surface** to a clean external review | `burnish` | same machinery, different object — burnish reviews screenshots of the running UI and splits its oracle (hard findings to zero, soft axes to `≥ 2`) because taste never reaches zero |
| A *known* restructure, shipped once, no reviewer loop | `refactor` | quell adds a loop and an external oracle; a single rename/extract does not need either. Drive an already-made refactor to a clean review → `quell profile=refactor` (§5a) |
| Loop must survive session end / run for hours | project-local `orbit` when available; otherwise `goal` or `apex` | quell is attended-but-uninterrupted, in-session; apply `_common/PROJECT_LOCAL_SKILLS.md` before an unattended-runner handoff |
| Just want one review, no fixing | `judge` direct | minimum viable chain |

**Scale:** 4-11 agents per cycle × ≤ 6 cycles. Medium-to-high cost (multiplied by cycle count; finding volume is the governor, not repo size).
*Range derivation:* TRIAGE 1-2 (Judge + independent adjudicator when dispositions are claimed) + FIX 1-4 (one per finding class, file-partitioned) + GREEN 1 (Radar) + REVIEW 1-3 (Judge + per-engine review subagents) + ARBITRATE 0-1 (Magi on oscillation/dispute) → floor 1+1+1+1+0 = **4**, ceiling 2+4+1+3+1 = **11**.

---

## 2. Termination Contract

"Until findings are zero" is only a *success* exit. Every run declares all bounds up front; **none is waivable by AUTORUN** (`_common/LOOP_PRECONDITIONS.md` #2 is contract-level).

| Bound | Default | Stop behavior |
|-------|---------|---------------|
| **ZERO (ACCEPT)** | — | Open findings ≥ `floor` == 0 **and** the Green Gate is green → `ACCEPT`. The success exit. |
| `max_cycles` | `loop ≤ N cycles (default N=6)` | `cap-reached` — stop, report best-so-far + residual open findings + `quell resume` command. |
| `token_budget` | run-level | `budget-reached` — stop + report (shared pool, not per-cycle). |
| diminishing-returns | **net open-finding count fails to decrease for 2 consecutive cycles** (ε = 1 closed finding/cycle) | `diminishing-returns (Δ < ε)` — stop + report. This is the anti-oscillation stop: a fix cycle that closes 3 and opens 3 has made no progress. |
| `BLOCK` | — | Oscillation (§3), a finding whose fix is out of scope, or Agent Tennis (fixer vs reviewer disagreeing 3+ turns without progress — Nexus circuit-breaker) → stop + escalate. |

**"Never stops" is implemented as: no confirmation pauses, not as an unbounded loop.** The run never stops to ask permission mid-loop (§5); it stops only on one of the five bounds above, and every non-`ACCEPT` exit ships best-so-far with the residual gap named.

---

## 3. The Finding Ledger — quell's declaration slots

The Ledger machinery — scope freeze, fingerprint discipline, the disposition vocabulary, oscillation → `FROZEN`, the per-cycle ledger diff, the ZERO predicate, and the confirm/resume posture — is **`_common/FINDING_LEDGER.md`. Read it before executing this recipe.** Quell fills its five declaration slots (§2 there) and adds nothing else:

| Slot | quell |
|------|-------|
| **(a) Oracle source** | `codex review` via `Judge`; `engines=codex \| codex+claude \| tri` |
| **(b) Frozen scope unit** | the reviewed file diff (`--uncommitted` \| `base=<branch>` \| `commit=<sha>`) |
| **(c) Fingerprint basis** | `sha1(normalized_path ⊕ enclosing_symbol ⊕ finding_class ⊕ normalized_message)` — **line numbers excluded**, they shift with every fix |
| **(d) Validity gate** | **Green Gate** — tests + build + typecheck, every cycle (`profile=refactor` swaps it, §5a) |
| **(e) Invariant + profiles** | `general` (scope only) · `refactor` (behavior preservation, §5a) |

**C4 holds** (`FINDING_LEDGER.md` §1): a code reviewer's finding space is bounded by the diff, so quell needs **no split oracle and no charter**. `floor=info` means literal zero findings — expensive, and nit-storms rarely converge.

**Disposition added by this recipe:** `DEFERRED (behavior-changing)` under `profile=refactor` (§5a.3) — real, but the fix changes external behavior, so it routes to `bug`/`feature`/`security` rather than being applied.

---

## 4. Disposition Integrity — what quell binds to agents

The four integrity rules are `_common/FINDING_LEDGER.md` §6 (the fixer never disposes · refute-polarity dismissal · `WONTFIX` is a written argument and is **Ask First** on CRITICAL/HIGH · `FIXED-VERIFIED` requires absence from a fresh review). Quell binds them to concrete agents:

- Dispositions are set by **`Judge` grounding** — verdicts VERIFIED / REJECTED / NEEDS-INFO per `judge/reference/tri-engine-review.md` — with `Magi` on dispute. `NEEDS-INFO` stays `OPEN`.
- The confirmation attempt behind a `FALSE-POSITIVE-RATIFIED` is a read of the **actual code**, not of the review text.
- **The self-dismissal analogue** (`FINDING_LEDGER.md` §6 closing rule) is `TEST-EDITED` under `profile=refactor`: editing a test to make the gate green is this loop's version of dismissing a finding, and only the adjudicator can ratify it (§5a.2).

---

## 5. Confirm Gate — one acknowledgement, then uninterrupted

**announce-and-proceed (no objection window)** for the loop body, per the front-loading rule in `_common/FINDING_LEDGER.md` §11. What quell announces and what re-opens the gate:

- BASELINE announces the frozen scope: the file set, the finding count by severity, and the declared bounds.
- If that blast radius trips an Ask First line (10+ files, `PUBLIC_API`/`DATA` reach, an L4 security finding), that is the **one** confirmation for the whole run — `Confirm-before-launch`. Approving it approves the loop, not one cycle.
- After launch the loop stops only on §2's bounds, or if a *new* L4 security finding appears that the launch acknowledgement did not cover.

---

## 5a. Profiles

A profile specializes **three** things — the green gate, the fixer roster, and what "out of bounds" means — and **nothing else**. The termination contract (§2), the Ledger (§3), and disposition integrity (§4) are profile-invariant: a profile can never buy a cheaper exit.

| | `profile=general` (default) | `profile=refactor` |
|---|---|---|
| Green gate | Green Gate — tests + build + typecheck pass | **Equivalence Gate** — the *same* suite passes *identically* (no changed expectations), build/lint green, public surface unchanged |
| Fixer roster | Builder · Sentinel · Zen · Radar | **Zen** (primary) · +Atlas (module boundaries) · +Grove/+Grove[llm] (structure) · +Sweep (dead code). Builder/Sentinel are **not** in the roster |
| Out of bounds → `DEFERRED` | outside the frozen file set | outside the frozen file set **or** the fix changes external behavior |
| Extra blocking class | — | **behavior-drift findings** (see below) |

### `profile=refactor` — behavior-preserving review-to-zero

Refactoring's invariant is *no external behavior change*, so a review-to-zero loop over a refactor diff has a second way to fail that `general` does not: it can reach zero findings by quietly changing behavior. Four rules close it. The underlying discipline is **not re-derived here** — it is `routing-matrix.md` § REFACTOR Phase Contract (SAFETY-NET / SCOPE-GUARD / VERIFY-EQUIVALENCE / behavior-neutral SHIP) plus `_common/DIFFERENTIAL_PARITY.md` (oracle origin: **own pre-change behavior**, one forward baseline — the same origin as `migrate`).

1. **SAFETY-NET is a launch precondition, not a phase.** Cycle 1 does not start until the frozen scope has a green suite that *pins current behavior*; untested scope gets characterization tests first (`Radar`), and if it cannot be pinned the run is `BLOCK`, never "refactor carefully and hope". A green diff on a thin oracle is false confidence (`_common/DIFFERENTIAL_PARITY.md` §1), so the pin's adequacy is stated at BASELINE and carried in the Ledger.
2. **Test files are frozen.** Editing a test to make the gate green is the refactor loop's version of dismissing a finding — the same integrity problem §4 solves for dispositions. Any change to a test file inside the loop raises a `TEST-EDITED` blocking finding that only the independent adjudicator can ratify (with the reason the expectation was wrong *before* the refactor). The fixer can never ratify its own test edit.
3. **SCOPE-GUARD as a disposition rule.** A finding whose only fix changes external behavior — API signature, output contract, error semantics, a real security fix — is `DEFERRED (behavior-changing)` with an explicit route (`bug` / `feature` / `security`). It is never applied inside the loop, and never silently dropped: it ships in the Quell Ledger as a follow-up. This is why Builder and Sentinel are off the roster; their presence *is* the scope leak.
4. **Behavior-drift findings block at any severity.** The review pass asks the engine for two things: ordinary findings, and whether the diff observably changes behavior. A drift finding ignores `floor` entirely — it is CRITICAL by construction, because it falsifies the recipe's invariant rather than lowering its quality.

**ZERO under `profile=refactor`** ⟺ no `OPEN` at severity ≥ `floor` **∧** no open behavior-drift finding at *any* severity **∧** the Equivalence Gate is green **∧** no unratified `TEST-EDITED` **∧** the final review output is attached.

**Pairing:** `refactor` (make the change) → `quell profile=refactor` (drive it to a clean review) → `acceptance` (merge proof). Invoking `quell profile=refactor` on an un-refactored scope is legitimate — the reviewer's findings then *become* the refactor slate, which is the cheap way to run "review-driven refactoring" without `anneal`'s six-dimension audit.

---

## 6. Phase Contract (AUTORUN chain template)

```
GATE ──── _common/LOOP_PRECONDITIONS.md (5-point) + engine preflight
          Judge[availability: codex binary + fallback paths per
                judge/reference/codex-review-usage.md]  ★ no -m / no API key
   ▼
BASELINE  Radar[Green Gate: tests + build + typecheck]  →  must be green to start
          ★ profile=refactor: SAFETY-NET first — pin behavior with
            characterization tests; un-pinnable scope ⇒ BLOCK (§5a.1)
          Judge[review @frozen scope] → Finding Ledger v0
          ANNOUNCE scope + counts + bounds + profile → §5 single acknowledgement
   ▼
┌─ LOOP (until ZERO | bound hit per §2) ──────────────────────────────────────┐
│  TRIAGE     Judge[ground each finding: VERIFIED/REJECTED/NEEDS-INFO,         │
│             dedupe by fingerprint, severity vs floor] → Fix Slate            │
│             ★ dispositions by adjudicator only, never by cycle-N fixer (§4)  │
│  FIX ∥      per finding class, file-ownership partitioned (no shared files): │
│             logic/API → Builder · security → Sentinel · waste/smell → Zen    │
│             · missing tests → Radar                                          │
│             ★ profile=refactor: Zen-led roster; behavior-changing fix ⇒      │
│               DEFERRED, never applied (§5a.3)                                │
│  GREEN      Radar[tests + build + typecheck] — red ⇒ synthetic BLOCKING      │
│             finding injected into the Ledger, next cycle fixes it first      │
│             ★ profile=refactor: Equivalence Gate — SAME suite, identical     │
│               results; any test-file change ⇒ TEST-EDITED blocker (§5a.2)    │
│  REVIEW     Judge[re-review @same frozen scope, same engines]                │
│             ★ profile=refactor: + behavior-drift question; a drift finding   │
│               blocks at any severity (§5a.4)                                 │
│  DIFF       Ledger diff: closed / persisting / net-new / re-emerged (§3)     │
│  GATE       open(≥floor) == 0 ∧ green      → ACCEPT (ZERO)                   │
│             re-emerged ×2                  → FROZEN + BLOCK                  │
│             Δopen ≥ 0 for 2 cycles         → diminishing-returns → stop      │
│             cycle N / budget               → cap-reached / budget-reached    │
│             else                           → carry Ledger into next cycle    │
└──────────────────────────────────────────────────────────────────────────────┘
   ▼
DELIVER ── Quell Ledger (§8) + handoff: Guardian[commit/PR] ; acceptance? [merge gate]
```

**Checkpoint-resume:** the Finding Ledger + frozen scope + per-cycle diff are persisted at every `GATE` boundary, so `quell resume` restarts mid-convergence with dispositions and trajectory intact. The Ledger file **is** the loop's state — precondition #4 is satisfied by it, not by conversation context.

**Loop Precondition Gate verdict** (report all five in §8): #1 completion oracle — **met** (open-count == 0 at floor is machine-checkable, given §3's ledger); #2 hard-stop — **met** (`max_cycles` + budget + diminishing-returns, external to the fixer); #3 maker ≠ checker — **met structurally** (external review engine + §4 disposition integrity); #4 persistent memory — **met** (Ledger file); #5 drift awareness — **run risk**: cycles of narrow fixes erode structure even while the finding count falls, so the Green Gate is mandatory each cycle and a sampled read of the accumulated diff is reported at DELIVER. Never assert quality improvement from the finding count alone.

---

## 7. Failure Modes Prevented

Generic finding-loop failures — unreachable zero, dishonest zero, phantom progress, oscillation, churn with no net gain, volatile-locator fingerprints, scope creep, confirmation storm, unbounded spend — and their mitigations are **`_common/FINDING_LEDGER.md` §12**. Below: what `quell` adds on top.

| Failure | Mitigation |
|---------|-----------|
| **Zero findings on broken code** | Green Gate every cycle (slot (d), §3); a red build injects a blocking finding rather than passing |
| **Nit-storm never converges** | `floor=medium` default; below-floor findings recorded, not blocking. C4 holds, so no split oracle is needed (§3) |
| **Structural erosion masked by a falling finding count** | Precondition #5 reported as a run risk + sampled diff read at DELIVER (§6) |
| **`refactor`: green reached by editing the tests** | Test files frozen; a test edit is a `TEST-EDITED` blocker only the adjudicator can ratify (§5a.2) |
| **`refactor`: silent behavior change reaching zero findings** | Equivalence Gate (same suite, identical results) + behavior-drift findings block at any severity (§5a.1, §5a.4) |
| **`refactor`: loop drifts into a rewrite via "just fix it properly"** | SCOPE-GUARD disposition rule — behavior-changing fixes are `DEFERRED` with a route, and Builder/Sentinel are off the roster (§5a.3) |
| **`refactor`: refactoring untested code with no proof of preservation** | SAFETY-NET is a launch precondition; un-pinnable scope is `BLOCK`, not best-effort (§5a.1) |

---

## 8. Output

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus the **Quell Ledger**:

- **Exit reason**: `ACCEPT (ZERO)` | `diminishing-returns (Δ < ε)` | `cap-reached` | `budget-reached` | `BLOCK`.
- Frozen scope + **profile** + review engines + `floor` + declared bounds. Under `profile=refactor`: the SAFETY-NET pin (what pins behavior, and its adequacy), every `DEFERRED (behavior-changing)` finding with its route, and any ratified `TEST-EDITED` with the ratifying agent's reason.
- **Per-cycle trajectory**: open(≥floor) at cycle entry → closed / net-new / re-emerged → open at exit.
- **Full finding table**: fingerprint (short), path:symbol, severity, disposition, and for every `FALSE-POSITIVE-RATIFIED` / `WONTFIX-RATIFIED` / `DEFERRED` / `FROZEN` record, the ratifying agent + evidence. No finding appears without a disposition.
- **Evidence**: the final review invocation and its verbatim output (evidence-bound claims, `reference/autonomy-quality-protocol.md` Q10). A ZERO claimed without an attached final review is `UNVERIFIED`.
- Green Gate result per cycle (tests / build / typecheck).
- Loop Precondition Gate verdict, five entries (§6).
- Residual gap + `quell resume` command on any non-`ACCEPT` exit; follow-up handoff (`Guardian` commit/PR, `acceptance` merge gate) on `ACCEPT`.

---

## 9. Decision Tree vs Neighbors

```
Driving code to a clean state?
  Oracle is an EXTERNAL REVIEWER's finding list → quell
    └ the object is a RENDERED UI SURFACE, not a diff → burnish
    └ the diff must preserve behavior (a refactor) → quell profile=refactor
    └ must survive session end / run unattended for hours → project-local orbit, else goal/apex
    └ want to decide each finding yourself, conversationally → judge pair
  Oracle is a RUBRIC score on a deliverable → converge
  Oracle is a METRIC on one shipped feature → kaizen
  Oracle is a MERGE decision with proof obligations → acceptance
  No oracle yet — "the design drifted, clean it up" → anneal
  A single known restructure, shipped once → refactor
  One known defect → bug
```

`quell` = external-reviewer-to-zero loop with a disposition ledger · `converge` = rubric Generator-Evaluator loop · `acceptance` = proof-carrying merge gate · `judge` = the review itself (quell's evaluator, called once).

---

## 10. Shared Protocols (cited, not re-derived)

| Protocol | What quell takes from it |
|----------|--------------------------|
| **`_common/FINDING_LEDGER.md`** | **The entire ledger machinery** — scope freeze, fingerprint discipline, disposition vocabulary + integrity, oscillation, ledger diff, ZERO predicate, bounds/confirm/resume posture, generic failure modes. quell fills its five declaration slots (§3) and adds only `profile=refactor`'s specializations |
| `_common/LOOP_PRECONDITIONS.md` | The five-point gate; run before cycle 1, verdict reported in §8 |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, single termination oracle, flatten rule (`converge quell` is **redundant** — quell already owns a loop and an oracle; wrap only by flattening to quell's fix agents) |
| `judge/reference/codex-review-usage.md` | How to invoke `codex review` — scope flags, robust binary detection, **never** `-m`/`--model`/`OPENAI_API_KEY` |
| `judge/reference/codex-integration.md`, `judge/reference/tri-engine-review.md` | Severity mapping, false-positive filtering, concurrence labels, grounding verdicts |
| `_common/ADVERSARIAL_REFUTATION.md` | Refute-polarity discipline for dismissals (§4.2) |
| `reference/routing-matrix.md` § REFACTOR Phase Contract | `profile=refactor`'s SAFETY-NET / SCOPE-GUARD / VERIFY-EQUIVALENCE / behavior-neutral SHIP discipline — cited, never re-derived (§5a) |
| `_common/DIFFERENTIAL_PARITY.md` | `profile=refactor`'s parity posture: oracle origin = own pre-change behavior (one forward baseline, as in `migrate`); oracle-adequacy gate on the SAFETY-NET pin (§5a.1) |
| `reference/autonomy-quality-protocol.md` | Decision Ledger for every judgment made without the user, evidence-bound claims, Acceptance Provenance |
| `_common/PROOF_CARRYING.md` | Only when handing off to `acceptance` — quell produces the clean diff, acceptance carries the merge proof |
