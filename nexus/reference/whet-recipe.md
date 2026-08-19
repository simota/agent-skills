# Whet Recipe — Mutation-Survivor Loop

> `/nexus whet [<scope>]` — run a **mutation engine** over the frozen scope, drive the surviving mutants down until every declared partition meets its threshold contract, and prove the kills are real tests rather than assertions pinned to the implementation. The loop runs **uninterrupted** and is bounded externally, never by the test author's own judgment.

Read this file **and `_common/FINDING_LEDGER.md`** before executing the `whet` Recipe. The ledger machinery lives in that shared protocol; this file declares whet's five slots (§3), the threshold contract that serves as its floor (§2), and the three ways a survivor can be closed dishonestly (§4).

**Named report:** **Whet Ledger**. **Resume:** checkpoint-resume (`whet resume`). **Confirm tier:** announce-and-proceed (no objection window) after a single launch-time acknowledgement (§5).

---

## 1. Nature / When to Use / Boundaries

Whet is the **Loop**-family member whose completion oracle is a **mutation engine's surviving-mutant set**. The engine is a deterministic external tool that generates the findings mechanically, so **maker ≠ checker holds structurally** — `Siege` runs and classifies, `Radar` writes the tests, and the agent that wrote a test never decides whether its mutant is killed.

It exists because the loop had no owner. `siege`'s `MUTATE` Recipe runs mutations, classifies survivors, and **recommends fixes**; `radar` authors tests. Nobody drives the survivor set to a threshold and proves the kills honest. Whet is that loop and nothing else — the mutation craft itself (operators, equivalent-mutant patterns, risk-based thresholds, CI tiering) is `siege/reference/mutation-testing-advanced.md`, cited throughout and never re-derived here.

Use `whet` when: a suite's *coverage* is high but its *strength* is unknown · a critical module must be proven genuinely tested before a release · a mutation report produced a long survivor list you want worked down unattended.

**Invocation:**

| Arg | Default | Meaning |
|-----|---------|---------|
| `<scope>` | changed modules | The mutation scope: module / package / path set. **Frozen at BASELINE** together with the operator set — the loop never widens either. |
| `tier=` | `2` | CI tier from `siege/reference/mutation-testing-advanced.md` — `1` PR-scoped incremental (`< 5 min`) · `2` changed module (`< 30 min`) · `3` full codebase (no strict limit). Sets the run budget, and a cycle that blows it fails the gate. |
| `threshold=` | risk-based | The **threshold contract** (§2). A single number applies it to every partition; the risk-based default reads per-module thresholds from the siege reference. |
| `max_cycles=` | `3` | Hard ceiling (§6). Lower than `quell`'s 6 — every cycle re-runs the engine, which is the cost driver. |
| `resume` | — | Resume from the persisted Ledger. |

| Not this | Route to | Why |
|----------|----------|-----|
| Run mutations once and get a report | `siege` (skill) | Whet loops siege's `MUTATE`; one measurement does not need a loop |
| Add tests for a known gap, no mutation oracle | `radar` (skill) | Minimum viable chain — whet's value is the oracle, not the authoring |
| Raise line/branch **coverage** | `radar` | Coverage counts execution; mutation counts detection. A 100%-covered suite can kill nothing |
| Drive a code **review** to zero | `quell` | Same machinery, different evaluator |
| The suite is flaky, not weak | `radar` (flaky repair) | A flaky suite cannot host a mutation run at all — whet `BLOCK`s on it at BASELINE |
| Load / chaos / contract resilience | `siege` (skill) | Whet owns only the mutation axis |
| Loop must survive session end | project-local `orbit` when available; otherwise `goal` or `apex` | Whet is attended-but-uninterrupted, in-session; apply `_common/PROJECT_LOCAL_SKILLS.md` |

**Scale:** 4-8 agents per cycle × ≤ 3 cycles, plus 2 at BASELINE. Medium-to-high cost — the governor is the **engine runtime**, not the agent count, so `tier=3` on a large repo dominates everything else.
*Range derivation:* TRIAGE 1-2 (`Siege` + `Magi` on dispute) + FIX 1-3 (`Radar` · `Void`/`Sweep` · `Zen`) + GATE-S 1 (`Radar`) + RE-MUTATE 1 (`Siege`) → floor 1+1+1+1 = **4**, ceiling 2+3+1+1 = **8** (the dispute arbitrator is counted inside TRIAGE). BASELINE adds `Radar` + `Siege` = **2**, once.

---

## 2. The Threshold Contract — whet's floor is a per-partition contract

**C4 holds** (`_common/FINDING_LEDGER.md` §1): the mutant set is finite and mechanically enumerable, and each mutant has a right answer (killed / survived / equivalent). Whet therefore needs **no split oracle**. What it does need is a floor that is not a scalar.

100% mutation score is the wrong target — `siege`'s `MA-02 Score Obsession` names it, and low-risk modules do not repay the tests it would take. So whet's floor is a **threshold contract**: a declared partition set (module / package / risk band), each with its own bar, frozen at BASELINE:

- partitions marked **`must-kill-all`** (typically the risk-critical modules): zero surviving mutants, no exceptions
- every other partition: **corrected mutation score ≥ its threshold**, where corrected score is siege's `Killed / (Total − Equivalent) × 100`

**ZERO (ACCEPT)** ⟺ every `must-kill-all` partition has no `OPEN` survivor **∧** every other partition meets its threshold **∧** the Suite-Integrity Gate is green **∧** the final mutation run's output is attached verbatim as evidence.

A survivor in a partition already at its threshold is `BELOW-FLOOR`: recorded, not blocking. This is the ordinary severity floor, expressed per partition instead of per finding.

---

## 3. Declaration Slots

| Slot | whet |
|------|------|
| **(a) Evaluator** | the **mutation engine** (Stryker / mutmut / PIT / cargo-mutants) run and classified by `Siege`. Deterministic and independent of the test author by construction |
| **(b) Frozen scope unit** | the mutation scope × the operator set × the **threshold contract** (§2 — the floor) |
| **(c) Identity mechanism** | **derived** — `sha1(file ⊕ enclosing_symbol ⊕ mutation_operator ⊕ normalized_mutated_expression)`. **Line/column and the engine's ordinal mutant index are excluded**: mutants are regenerated from scratch every run, so ordinals mean nothing across cycles and a line-keyed ledger reports the whole set as new after the first test lands |
| **(d) Validity gate** | **Suite-Integrity Gate** (§5) |
| **(e) Invariant + profiles** | tests assert **behavior**, not implementation. No profiles — `tier=` is a run budget and `threshold=` is the floor |

**Disposition added by this recipe:** `EQUIVALENT-RATIFIED` — the mutant is real and survived, but **no possible test can distinguish it** (siege's equivalence pattern table). Distinct from `FALSE-POSITIVE-RATIFIED` (the finding was not real) and from `WONTFIX-RATIFIED` (real, killable, deliberately not killed), and unique in that it **moves the denominator**: see §4. Also `CLOSED-BY-REMOVAL` — the survivor's host code was deleted as genuinely dead (§4.3).

---

## 4. Disposition Integrity — three dishonest ways to close a survivor

The four base rules are `_common/FINDING_LEDGER.md` §6. Whet's domain has an unusually strong pull toward each of them, because **two of its three cheats improve the number arithmetically rather than merely hiding a problem.**

### 4.1 `EQUIVALENT` is a proof obligation, not a label — and it is the strongest cheat in the family

Corrected score is `Killed / (Total − Equivalent) × 100`. Declaring a survivor equivalent **shrinks the denominator, so it raises the score without a single test being written.** Every other member's false-positive dismissal merely removes a blocker; this one is directly rewarded.

Three rules, and none is waivable:

1. **The test author never ratifies equivalence** for a mutant in their own scope — `_common/FINDING_LEDGER.md` §6.1 applied where it bites hardest. `Siege` adjudicates; `Magi` on dispute.
2. **Refute polarity** (§6.2): the adjudicator must attempt to **construct a distinguishing test** and fail, recording *why* no observable difference exists, citing the matching pattern in `siege/reference/mutation-testing-advanced.md` § Equivalent Mutants. "Looks equivalent" is `NEEDS-INFO`, and `NEEDS-INFO` stays `OPEN`.
3. **The equivalence rate is reported, per cycle, in the Ledger.** A run whose score rose mainly through a growing `Equivalent` count did not strengthen the suite, and the Whet Ledger must make that visible rather than reporting the corrected score alone.

### 4.2 `TAUTOLOGICAL-KILL` — the self-dismissal analogue

A survivor can always be killed by asserting on the mutated expression itself. The mutant dies, the score rises, and nothing about the system's behavior is now tested — this is `quell profile=refactor`'s `TEST-EDITED` transposed, and `siege`'s `MA-07` in ledger form.

A test added inside the loop that pins an implementation detail — asserting a private intermediate, mirroring the production expression, or asserting only that a function was called — raises a **`TAUTOLOGICAL-KILL` blocking finding at any severity**. Only the adjudicator may ratify a contested case, and the kill does not count until it does. The rule of thumb the adjudicator applies: *would this test still pass if the implementation were rewritten to the same contract?* If not, it is a mirror, not a test.

### 4.3 `CLOSED-BY-REMOVAL` — legitimate, but never silent

`siege`'s `MA-07` is right that survivors often reveal structure rather than test gaps: an unreachable branch, an over-built abstraction, a defensive path that cannot fire. Deleting the host code is a **real** closure — the mutant is gone because the code is gone.

It is also the third cheat if unchecked. So: removal requires `Void`/`Sweep` evidence that the code is genuinely dead, ratified by the adjudicator, and it is recorded as `CLOSED-BY-REMOVAL` rather than as a kill — it never counts toward `Killed`. A removal that changes externally observable behavior is `DEFERRED (behavior-changing)` with a route to `bug`/`feature`, never applied inside the loop.

---

## 5. Suite-Integrity Gate and the Confirm Gate

**Suite-Integrity Gate** — whet's validity gate (`_common/FINDING_LEDGER.md` §10), run every cycle. A red gate injects a synthetic blocking finding into the Ledger for the next cycle; it never merely warns.

1. **Green on unmutated code** — the suite passes against the real implementation. A red suite makes every mutant "killed" for the wrong reason.
2. **No flake** — a test that passes and fails across the cycle's runs invalidates the mutation result, because a flaky failure is indistinguishable from a kill. Un-stabilizable flake at BASELINE is `BLOCK`, not a best-effort run.
3. **Runtime within the `tier=` budget** — a cycle that blows its tier budget fails the gate rather than silently becoming a nightly job.
4. **Coverage non-regression** — killing mutants must not come with deleted or skipped tests.

**Confirm Gate — one acknowledgement, then uninterrupted**, per the front-loading rule in `_common/FINDING_LEDGER.md` §11. BASELINE announces the frozen scope, the operator set, the threshold contract, the survivor count per partition, the measured engine runtime, and the declared bounds. If that trips an Ask First line (10+ files, a `tier=3` full-codebase run), that is the **one** confirmation for the whole run.

---

## 6. Termination Contract

| Bound | Default | Stop behavior |
|-------|---------|---------------|
| **ZERO (ACCEPT)** | — | §2's conjunction holds → `ACCEPT`. |
| `max_cycles` | `loop ≤ N cycles (default N=3)` | `cap-reached` — stop, report best-so-far + the residual survivor set + `whet resume`. |
| `token_budget` | run-level | `budget-reached` — stop + report. |
| diminishing-returns | **net open survivor count fails to decrease for 2 consecutive cycles** (ε = 1 killed survivor/cycle) | `diminishing-returns (Δ < ε)` — stop + report. |
| `BLOCK` | — | Un-stabilizable flake or a red suite at BASELINE · oscillation (§`FINDING_LEDGER.md` §7) · an unratified `TAUTOLOGICAL-KILL` the fixer will not replace · Agent Tennis → stop + escalate. |

Bounds are contract-level; `AUTORUN` cannot waive them.

---

## 7. Phase Contract (AUTORUN chain template)

```
GATE ──── _common/LOOP_PRECONDITIONS.md (5-point) + engine preflight
          Siege[mutation engine available for the stack; operator set resolved]
   ▼
BASELINE  Radar[suite green + flake check]  →  un-stabilizable flake ⇒ BLOCK (§5.2)
          Siege[run mutations @frozen scope] → Survivor Ledger v0
          FREEZE threshold contract: partitions + per-partition bars (§2)
          ANNOUNCE scope + operators + survivors/partition + runtime + bounds
          → §5 single acknowledgement
   ▼
┌─ LOOP (until ZERO | bound hit per §6) ──────────────────────────────────────┐
│  TRIAGE     Siege[classify each survivor: killable | equivalent-candidate    │
│             | dead-code-candidate; dedupe by fingerprint; partition vs bar]  │
│             ★ equivalence ratified by Siege only, never by the test author,  │
│               with a failed distinguishing-test attempt recorded (§4.1)      │
│  FIX ∥      per class, file-ownership partitioned (_common/PARALLEL.md):     │
│             killable       → Radar[behavior test]                            │
│             dead-code      → Void[justify] + Sweep[remove]  ⇒ CLOSED-BY-     │
│                              REMOVAL, never counted as a kill (§4.3)         │
│             structural     → Zen[extract so the branch becomes testable]     │
│             ★ behavior-changing removal ⇒ DEFERRED, never applied            │
│  GATE-S     Radar[Suite-Integrity: green · no flake · tier budget ·          │
│             coverage non-regression] — red ⇒ synthetic BLOCKING finding      │
│             ★ implementation-coupled test ⇒ TAUTOLOGICAL-KILL blocker (§4.2) │
│  RE-MUTATE  Siege[re-run @same frozen scope, same operators]                 │
│  DIFF       Ledger diff: killed / persisting / net-new / re-emerged          │
│             + per-partition corrected score + the equivalence rate (§4.1.3)  │
│  GATE       §2 conjunction holds            → ACCEPT (ZERO)                  │
│             re-emerged ×2                   → FROZEN + BLOCK                 │
│             Δopen ≥ 0 for 2 cycles          → diminishing-returns → stop      │
│             cycle N / budget                → cap-reached / budget-reached   │
│             else                            → carry Ledger into next cycle   │
└──────────────────────────────────────────────────────────────────────────────┘
   ▼
DELIVER ── Whet Ledger (§9) + handoff: Guardian[commit/PR] ; acceptance? [merge gate]
```

**Loop Precondition Gate verdict** (report all five in §9): #1 completion oracle — **met** (§2's conjunction is machine-checkable); #2 hard-stop — **met** (`max_cycles` + budget + diminishing-returns, external to the fixer); #3 maker ≠ checker — **met structurally** (a deterministic engine generates the findings; `Siege` adjudicates, `Radar` fixes); #4 persistent memory — **met** (Ledger file); #5 drift awareness — **run risk**: a suite can gain mutants-killed while losing readability and speed, so the Suite-Integrity Gate is mandatory each cycle and the added tests' total runtime delta is reported at DELIVER. Never assert suite quality from the score alone.

---

## 8. Failure Modes Prevented

Generic finding-loop failures and their mitigations are **`_common/FINDING_LEDGER.md` §12**. Below: what the mutation domain adds.

| Failure | Mitigation |
|---------|-----------|
| **Score raised by declaring survivors equivalent** (the denominator cheat) | `EQUIVALENT-RATIFIED` needs a failed distinguishing-test attempt + a cited pattern; the test author may not ratify; the **equivalence rate is reported per cycle** (§4.1) |
| **Mutants killed by tests that mirror the implementation** | `TAUTOLOGICAL-KILL` blocks at any severity; the kill does not count until the adjudicator ratifies (§4.2) |
| **Code deleted to make the survivor disappear** | `CLOSED-BY-REMOVAL` needs Void/Sweep dead-code evidence and never counts as a kill; behavior-changing removal is `DEFERRED` (§4.3) |
| **Chasing 100%** (`MA-02` Score Obsession) | The floor is a per-partition threshold contract, not a single number; below-threshold partitions record survivors as `BELOW-FLOOR` (§2) |
| **Mutation run on a flaky or red suite** | Suite-Integrity Gate §5.1-5.2; un-stabilizable flake at BASELINE is `BLOCK`, not a best-effort run |
| **The loop silently becomes a nightly job** | `tier=` runtime budget is a gate condition, not a guideline (§5.3) |
| **Every mutant reported as new after the first test lands** | Identity excludes line/column and the engine's ordinal index (§3) |
| **A faster score at the cost of a slower suite** | Precondition #5 as a run risk + the added tests' runtime delta reported at DELIVER (§7) |

---

## 9. Output

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus the **Whet Ledger**:

- **Exit reason**: `ACCEPT (ZERO)` | `diminishing-returns (Δ < ε)` | `cap-reached` | `budget-reached` | `BLOCK`.
- Frozen scope + operator set + **threshold contract** (partitions, bars, which are `must-kill-all`) + `tier` + declared bounds.
- **Per-cycle trajectory**, per partition: survivors at entry → killed / net-new / re-emerged → survivors at exit, with the corrected score **and the equivalence count shown separately** — a score that moved because the denominator shrank is reported as such, never folded into the headline number.
- **Full survivor table**: fingerprint (short), `file:symbol`, operator, partition, disposition, and for every `EQUIVALENT-RATIFIED` / `CLOSED-BY-REMOVAL` / `WONTFIX-RATIFIED` / `DEFERRED` / `FROZEN` record, the ratifying agent + evidence. No survivor appears without a disposition.
- **Evidence**: the final mutation run's invocation and verbatim output. A threshold claimed without an attached final run is `UNVERIFIED` (`reference/autonomy-quality-protocol.md` Q10).
- Suite-Integrity Gate result per cycle, plus the **suite runtime delta** introduced by the added tests.
- Loop Precondition Gate verdict, five entries (§7).
- **Residual Ledger** (typed): each `DEFERRED (behavior-changing)` with its route, each below-threshold partition as a candidate next scope, each `FROZEN` survivor as a `BLOCK`-class residual, plus the completion-sweep line. `whet resume` on any non-`ACCEPT` exit.

**Done** is deliverable-relative: every `must-kill-all` partition has no surviving mutant, every other partition meets its threshold, and the added tests are behavior assertions that survived the adjudicator. Partitions outside the frozen scope are a Q2 non-goal, not a residual.

---

## 10. Decision Tree vs Neighbors

```
Driving test quality to a bar?
  Oracle is a MUTATION ENGINE's surviving-mutant set → whet
    └ one measurement, no loop → siege (skill) MUTATE
    └ must survive session end → project-local orbit, else goal/apex
  Oracle is line/branch COVERAGE → radar (skill)
  Oracle is an external REVIEWER's finding list → quell (code) / burnish (UI)
  Oracle is load / chaos / contract resilience → siege (skill)
  The suite is flaky rather than weak → radar (flaky repair) — whet BLOCKs on it
```

---

## 11. Shared Protocols (cited, not re-derived)

| Protocol | What whet takes from it |
|----------|-------------------------|
| **`_common/FINDING_LEDGER.md`** | **The entire ledger machinery** — scope freeze, identity, disposition vocabulary + integrity, oscillation, ledger diff, ZERO predicate, bounds/confirm/resume, generic failure modes. whet fills its five slots (§3) and adds only `EQUIVALENT-RATIFIED`, `CLOSED-BY-REMOVAL`, and `TAUTOLOGICAL-KILL` |
| **`siege/reference/mutation-testing-advanced.md`** | **The mutation craft** — equivalent-mutant patterns and the corrected-score formula, risk-based thresholds, CI tiering (`tier=`), and the `MA-01`..`MA-07` anti-patterns. Whet supplies the loop and the integrity rules; it never re-derives the technique |
| `siege/reference/mutation-testing-guide.md` | Operator selection and scoping for the BASELINE run |
| `_common/LOOP_PRECONDITIONS.md` | The five-point gate; run before cycle 1, verdict reported in §9 |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation (`converge whet` is **redundant** — whet already owns a loop and an oracle) |
| `_common/ADVERSARIAL_REFUTATION.md` | Refute-polarity discipline for equivalence claims (§4.1.2) |
| `_common/PARALLEL.md` | File-ownership partitioning for concurrent fixers |
| `reference/autonomy-quality-protocol.md` | Decision Ledger, evidence-bound claims, Acceptance Provenance, completion integrity (Q16-Q22) |
