# `optimize` — Measured performance improvement on correct code

**Purpose:** Full phase contract for the `optimize` Recipe — make *correct* code measurably faster against a **quantified target traced to a real budget**, and prove the win with a number. The lightest member of the Improve family: no restructure (`refactor`), no multi-axis polish (`kaizen`), no design sweep (`anneal`).

**Read when:** Executing the `optimize` Recipe, or selecting a tool for a slow-layer complaint. The task-type row + chain-adjustment rules stay in `reference/routing-matrix.md` § OPTIMIZE; this file owns the deep contract.

---

## 1. When to Use / Boundaries

Performance work has one law — **measure, don't guess**. `optimize` exists because the bare `Bolt/Tuner → Radar` chain skips measurement entirely and optimizes the wrong thing.

**Entry condition:** the code is **correct but genuinely too slow**, and there is (or can be derived) a **number** that says so.

| Not this | Route to | Why |
|----------|----------|-----|
| Slowness caused by a **defect** (N+1 from a change, unbounded loop, missing await, accidental quadratic, **memory leak**) | `bug` | Root-cause the defect; do not tune around it |
| Continuous parameter self-tuning (GC / threadpool / connection pool / cache-size loop) | `AUTO_TUNING` | Standing self-measurement loop, not a one-shot fix |
| Multi-axis improvement of one feature (perf **+** UX **+** code quality) | `kaizen` | `optimize` is perf-only |
| Internal restructure with no perf number | `refactor` | Behavior-preserving cleanup, not a measured win |
| Undiagnosed design weaknesses across the codebase | `anneal` | Design sweep, not a measured hotspot |
| "Make it faster" with **no number and no budget to derive one from** | reject → `+Beacon` first | Without a target, optimization is unbounded |

---

## 2. Layer Taxonomy (tool selection follows the measured layer, never the default)

A slow system is slow *somewhere*. Defaulting to Bolt because it is the perf agent is the second-most-common failure after not measuring. Localize the layer, then bind the tool:

| Layer | Symptom | Primary tool | Baseline metric |
|-------|---------|--------------|-----------------|
| **Code / CPU / allocation** | hot function, GC churn, quadratic in-process | `Bolt` | CPU profile, allocation rate, wall time |
| **Render / interaction** | jank, dropped frames, slow re-render | `Bolt` | frame time, INP/TBT, re-render count |
| **Query / plan / index** | slow SQL, bad plan, N+1-by-design | `Tuner` | `EXPLAIN ANALYZE`, rows examined, plan cost |
| **Network / payload** | over-fetch, chatty API, oversized responses | `Bolt` + `Gateway` | request count, transfer size, waterfall depth |
| **Build / bundle** | slow CI, large bundle, slow cold start | `Gear` (+`Bolt` for bundle analysis) | build wall time, bundle bytes, cache hit rate |
| **Infra / runtime** | undersized instance, cold starts, saturation | `Scaffold` + `Beacon` | utilization, queue depth, cold-start p95 |
| **Search / ranking** | slow retrieval, expensive scoring | `Seek` (+`Tuner`) | query latency, index size, recall-at-latency |

**Multi-layer:** when two layers are implicated, run **parallel tracks under hub-spoke, each with its own baseline and its own target** — never one shared number across layers, or a win in one masks a regression in the other.

---

## 3. Phase Contract

```
DEFECT-CHECK → LOCATE → MEASURE → PROFILE-VALIDITY → TARGET-GATE → OPTIMIZE → VERIFY → [ITERATE] → SHIP
```

### DEFECT-CHECK (gate, before anything)
If the slowness is a *defect*, **redirect to `bug`** — root-cause it, don't tune around it. For a perf regression with a known good-past state ("was fast, got slow"), `+Trail`: **bisect the benchmark to the culprit commit first** — the diff names the fix; profiling from scratch is the slow path when the regression window is known.

### LOCATE (when the hotspot layer is unknown)
If the request does not name the slow layer, do **not** default to Bolt. Localize with `+Scout` or a broad profile pass, then bind the tool per §2. A misrouted tool produces a confident measurement of the wrong layer.

### MEASURE (quantified baseline — no baseline number → no optimize)
Profile to find the **actual hotspot** and capture the baseline **before** changing anything. The baseline is a **distribution, not a single run**: median + tail (p95/p99) over enough runs that **run-to-run variance < the target delta**, warm state unless cold-start is the metric under test. **A win smaller than measured noise is not a win.**

### PROFILE-VALIDITY (gate — the profile must describe the system you are shipping)
A profile taken on the wrong build or the wrong data measures a system nobody runs. All four must hold, or the profile is re-taken:

| Check | Requirement |
|-------|-------------|
| **Build representativeness** | Production-mode build (optimizations on, dev instrumentation off) — a dev-server profile is not evidence |
| **Data representativeness** | Realistic volume, cardinality, and distribution — a toy fixture hides the plan that matters |
| **Concurrency representativeness** | Measured under representative concurrency when the metric is throughput- or contention-sensitive |
| **Amdahl gate** | The chosen hotspot accounts for a **declared share of the measured metric** (default ≥ 20%); below that, the theoretical ceiling of fixing it is smaller than the effort — re-rank or state the ceiling explicitly |

The Amdahl gate is what stops a technically-real 40% win on 3% of runtime from being reported as a 40% win.

### TARGET-GATE (a number traced to a budget)
Set a **quantified target** (p95 < 200ms, render < 16ms, query < 50ms) **and** a stop condition. The target must trace to a **real budget** — an SLO, a frame/interaction budget, or a stated user-perceptible threshold — not an arbitrary number (`+Beacon` to define one if none exists). Reject "make it faster" with no number.

### OPTIMIZE (fix at the measured hotspot, in leverage order)
1. algorithmic / complexity + **eliminate redundant work**
2. query plan / index
3. batching / concurrency
4. caching
5. micro-tuning

**Prefer removing work over caching it** — caching is added state and an invalidation liability, not a first move. `+Schema` when an index or migration is recommended: a schema index/migration is **DATA blast radius → Ask First** (create/rebuild index, ALTER, backfill), even in AUTORUN.

### VERIFY (independent, evidence-bound — producer ≠ verifier)
The optimizer never scores its own win. `Radar` re-runs the **same benchmark** on a **production-representative environment and dataset**, and all four must hold:

| Check | Pass condition |
|-------|----------------|
| **Speedup** | the metric moved toward target — **proved with a number, never a claim** (Q10, `reference/autonomy-quality-protocol.md`) |
| **Correctness** | behavior unchanged; the correctness suite is green — an optimization that alters output is a bug |
| **No-regression across the explicit metric set** | latency (median **and** tail), throughput, memory/allocations, startup/cold path — any tradeoff taken is **declared in the PR, not hidden** |
| **Cache honesty** (if caching was added) | invalidation correctness proved by a stale-read test on the mutation path, **and** the cold/miss path measured — a cache-hot benchmark measures the cache, not the code |

For prod-facing latency/throughput wins, confirm the target holds under load (`+Siege`) or in prod telemetry (`+Beacon`) before claiming success — **a local-only speedup is unproven**.

### ITERATE
See § Termination Bound.

### SHIP (Guardian)
PR carrying the named **Speedup Report** (§ Output report).

---

## 3a. `optimize mode=to-zero` — the budget sweep

The phases above drive **one target to one number**. `mode=to-zero` drives a **set of budget violations to zero** across many targets: every route against its Core Web Vitals budget, every entrypoint against its bundle budget, every endpoint against its p95 SLO, every query against its plan-cost ceiling. It is a member of `_common/FINDING_LEDGER.md` — **read that file before running this mode** — and **inherits every discipline above rather than restating it**: the baseline is still a distribution, PROFILE-VALIDITY still gates each measurement, the Amdahl gate still applies per target, and no-regression across the explicit metric set still holds.

| Slot | `optimize mode=to-zero` |
|------|-------------------------|
| **(a) Evaluator** | the measurement harness — Lighthouse CI · bundle-size checker · `EXPLAIN ANALYZE` · k6/Siege thresholds · profiler — run by `Radar`/`Beacon`, **independent of the optimizer**. This mode does **not** inherit `AUTO_TUNING`'s reviewed self-measurement exception: a sweep over dozens of noisy targets is exactly where self-measurement fails |
| **(b) Frozen scope** | the **budget set**: `target × budget × metric`, frozen at BASELINE with the measurement conditions (build, dataset, concurrency, device/network profile, sample count) |
| **(c) Identity** | **derived** — `sha1(budget_id ⊕ target_id ⊕ metric)`. **The measured value and the run timestamp are excluded**: the number changes on every run by construction, so a value-keyed ledger reports the entire budget set as new every cycle |
| **(d) Validity gate** | **Measurement-Integrity Gate**, every cycle: identical declared conditions · measured variance within the declared band · the correctness suite green · **no cross-budget regression** (fixing route A's bundle must not blow route B's) |
| **(e) Invariant** | correctness preserved, and the *user-perceptible* behavior actually improved — not just the number. No profiles |

**Floor** is the budget itself, per target — the same per-partition shape as `whet`'s threshold contract. A target already inside its budget records overruns as `BELOW-FLOOR`.

### Three dishonest ways to reach zero violations

1. **`BUDGET-RAISED` — the self-dismissal analogue.** The cheapest path to zero violations is to move the budget. `TARGET-GATE` already requires a target to trace to a real budget, but that binds at *launch*; in a sweep the temptation is mid-loop. So **budgets are frozen at BASELINE**, and raising one inside the loop is a blocking finding that only the adjudicator may ratify, recording the SLO or user-perceptible threshold that justifies the new number. A budget nobody can trace is not a budget.
2. **`METRIC-GAMED`.** Work deferred past the measured window improves the metric and nothing else — lazy-loading past the LCP mark, moving work off the sampled path, warming the cache before measuring. `VERIFY`'s cache-honesty rule is one instance of this; in a sweep it is a blocking class at any severity, because it falsifies the mode's invariant rather than lowering its quality.
3. **`FLAKE-CLOSED`.** Across dozens of noisy targets, some cross their budget by luck on any given run. A close therefore requires re-measurement over the declared sample count under the declared conditions — never one favorable run. A violation that re-emerges is **not** a new finding: it is evidence the earlier close was noise, and `_common/FINDING_LEDGER.md` §7's oscillation rule freezes it on the second recurrence rather than letting the sweep chase it forever.

`DEFERRED (infrastructure)` covers a violation whose only fix is scale or platform work that cannot close in-session (`FINDING_LEDGER.md` §1a C6), routed out with its owner rather than looped over.

**Not this mode** — one slow endpoint, one target, one number → the single-pass phases above. Continuous parameter self-tuning → `AUTO_TUNING`. A slowdown caused by a defect → `bug`.

---

## 4. Termination Bound

**`loop ≤ N cycles (default N=3)`.** If the target is unmet and the last pass still yielded meaningful gain, **re-profile** (the hotspot moves after each fix) and optimize the new top hotspot; the quantified baseline persists across cycles as the loop's comparison anchor, and each new hotspot re-clears the Amdahl gate.

Exit on `ACCEPT` / `target-met` · `diminishing-returns (Δ < ε)` · `cap-reached` · `BLOCK`. On any non-`ACCEPT` exit, report **best-so-far + residual gap** (baseline → best result vs target) — never silently stop. Loop machinery: `reference/evaluator-loop-protocol.md`; loop preconditions: `_common/LOOP_PRECONDITIONS.md` (the benchmark **is** the completion oracle; Radar ≠ Bolt is the maker≠checker separation).

## 5. Confirm / Safety Gate

- **Ask First** — schema index/migration (`+Schema`: create/rebuild index, ALTER, backfill = **DATA blast radius**), infra resizing that changes cost, and any change touching 10+ files. These hold **even in AUTORUN**.
- **announce-and-proceed (no objection window)** — the ordinary measure→fix→verify cycle inside the declared target and cap.
- **Confirm before launch** — when the target can only be met by a change that leaves the perf envelope (rewriting the layer, changing the data model, adding a cache tier): that is an architecture decision, not a tuning pass — surface it and let the user choose `optimize` vs `refactor`/`anneal`/`apex`.

## 6. Resume

**Checkpoint-resume:** the baseline distribution, the Profile-Validity verdict, the target, and each cycle's before/after numbers persist at cycle boundaries, so an interrupted run resumes **without re-profiling** — re-measuring is the expensive part of this recipe, and a re-derived baseline is not comparable to the one the earlier cycles were scored against. A resumed run re-runs the drift check (has the code moved under the baseline?) before trusting persisted numbers.

## 7. Output report — **Speedup Report** (named)

Emitted with `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

| Section | Content |
|---------|---------|
| Layer & tool | measured layer (§2) + tool bound to it + why not the others |
| Baseline | distribution (median + p95/p99), sample count, measured noise floor, environment/dataset provenance |
| Profile validity | build / data / concurrency representativeness + hotspot share vs the Amdahl gate |
| Target | the number + **the budget it traces to** (SLO / frame budget / user-perceptible threshold) |
| Fix | leverage tier applied (1-5) + what work was *removed* vs *cached* |
| Result | baseline → result vs target, per metric in the explicit set; cycles run + exit reason |
| No-regression | the full metric set with verdicts + **declared tradeoffs** |
| Cache honesty | invalidation test + cold/miss path numbers (or `N/A`) |
| Prod confirmation | `+Siege` / `+Beacon` result, or `UNVERIFIED — local only` |

`UNVERIFIED` is a required label, not an omission: a win never exercised under prod-representative conditions is labeled, never quietly presented as shipped-and-proven.

## 8. Scale

**2-4 agents × ≤3 cycles, low cost** — Bolt *or* Tuner (+ a second tool only on a multi-layer track), Radar, Guardian. `+Scout` / `+Trail` / `+Siege` / `+Beacon` add one each. The cheapest recipe that still carries an independent verifier.

## 9. Failure Modes Prevented

| # | Failure | Mitigation |
|---|---------|-----------|
| 1 | Optimizing by guess / the wrong hotspot | MEASURE-FIRST profile |
| 2 | Tuning around a defect instead of fixing it | DEFECT-CHECK → `bug` redirect |
| 3 | Profiling from scratch when the regression window is known | DEFECT-CHECK bisect (`+Trail`) |
| 4 | Defaulting to the code profiler for a DB/network/build problem | LOCATE + § 2 layer taxonomy |
| 5 | Benchmark noise claimed as a win | MEASURE distribution baseline + noise floor |
| 6 | Profiling a dev build or a toy dataset | PROFILE-VALIDITY build/data/concurrency checks |
| 7 | A big win on a negligible slice reported as a big win | PROFILE-VALIDITY Amdahl gate (default ≥ 20%) |
| 8 | Unbounded micro-optimization | TARGET-GATE + `loop ≤ 3` cap |
| 9 | An arbitrary target with no budget behind it | TARGET-GATE budget traceability (`+Beacon`) |
| 10 | Caching as a first move instead of removing work | OPTIMIZE leverage order (1-5) |
| 11 | Claimed-but-unmeasured speedup | VERIFY prove-with-a-number (Q10) |
| 12 | The optimizer grading its own win | VERIFY producer ≠ verifier (Radar ≠ Bolt/Tuner, Q9) |
| 13 | Perf win that silently changes behavior | VERIFY correctness suite green |
| 14 | Perf win that regresses another metric | VERIFY explicit metric set + declared tradeoffs |
| 15 | Cache-hot benchmark measuring the cache, not the code | VERIFY cold/miss path + invalidation test |
| 16 | Local-only win that dies in prod | VERIFY prod-representative + `+Siege`/`+Beacon`, else labeled `UNVERIFIED` |
| 17 | Hotspot moved but the old one kept getting optimized | ITERATE re-profile each cycle |
| 18 | Re-profiling from scratch after an interruption, producing an incomparable baseline | § 6 checkpoint-resume persists the baseline |
| 19 | A tuning pass silently becoming an architecture change | § 5 confirm-before-launch on leaving the perf envelope |

## 10. Boundaries / Decision Tree

```
Something is slow.
  Is it slow because of a DEFECT (leak / N+1 from a change / missing await / accidental quadratic)?
    YES → bug   (known-good past state? → bug +Trail bisect)
  Is the ask a STANDING self-tuning loop (GC / pool / cache-size)?
    YES → AUTO_TUNING
  Is perf only ONE of several axes you want improved on this feature?
    YES → kaizen
  Is there a number (or a budget one can be derived from)?
    NO  → +Beacon to define a budget first; reject "make it faster"
    YES → optimize
          └ target reachable only by leaving the perf envelope? → surface: refactor / anneal / apex
```

## 11. Shared protocols

- `reference/evaluator-loop-protocol.md` — ITERATE loop machinery (single termination oracle = the benchmark).
- `_common/LOOP_PRECONDITIONS.md` — the five-point gate; the benchmark is the completion oracle, `loop ≤ 3` the hard-stop bound, Radar ≠ Bolt the maker≠checker separation.
- `reference/autonomy-quality-protocol.md` — Q9 (producer ≠ verifier), Q10 (evidence-bound claims, `UNVERIFIED` labeling), Q15 (Acceptance Provenance).
- `reference/routing-matrix.md` § OPTIMIZE — task-type row, chain adjustment, Sherpa-skip.

## 12. Handoffs

| Direction | Contract |
|-----------|----------|
| `apex` / `acceptance` → `optimize` | a perf **AC** with its budget becomes this recipe's TARGET-GATE input; the Speedup Report is the AC's evidence |
| `optimize` → `kaizen` | target met but the feature needs UX / code-quality work too — hand off with the baseline + result so kaizen does not re-measure |
| `optimize` → `AUTO_TUNING` | the win requires a standing parameter loop rather than a one-shot fix |
| `optimize` → `beacon` (skill) | the target should become a monitored SLO so the win does not silently decay |
| `optimize` → `bug` | DEFECT-CHECK fired mid-run (the "slow" behavior turned out to be incorrect) |

## 13. Add-ons

`+Trail` (bisect a perf regression to the offending commit) · `+Scout` (localize an unknown hotspot layer) · `+Schema` (DB index/migration — **Ask First**) · `+Gear` (build/bundle/CI layer) · `+Scaffold` (infra/runtime sizing) · `+Gateway` (network/payload contract) · `+Seek` (search/ranking latency) · `+Siege` (load-test the speedup under realistic traffic) · `+Beacon` (define the budget / confirm the target in production) · `+Flux` (first-principles reframe when stuck) · `+Matrix` (target combination coverage).

## 14. Chain template

```
DEFECT-CHECK (bug? → redirect | +Trail bisect if known-good past) → LOCATE (+Scout? → bind tool per §2)
  → MEASURE (Bolt | Tuner | Gear | Scaffold — distribution baseline, noise floor)
  → ✓PROFILE-VALIDITY (build / data / concurrency / Amdahl ≥ 20%)
  → ✓TARGET-GATE (number + budget it traces to; +Beacon? to define)
  → OPTIMIZE (leverage order 1-5; +Schema? = Ask First)
  → VERIFY (Radar — speedup ∧ correctness ∧ no-regression ∧ cache honesty; +Siege?/+Beacon? prod)
  → [ITERATE loop ≤ 3 cycles — re-profile, re-clear Amdahl]
  → SHIP (Guardian — PR + Speedup Report)
```
