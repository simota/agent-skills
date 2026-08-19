# Migrate Recipe — Change-Completeness Migration

> `/nexus migrate` — execute a **wholesale change** (architecture / framework / middleware / mock→production / same-language modernization) across an entire codebase **with a proven-complete guarantee**: every change site migrated, behavior preserved, zero residual old pattern, old code decommissioned. The no-omission property is the deliverable, not a side effect.

Read this file before executing the `migrate` Recipe. The double-loop structure, the RESIDUE-GATE completeness proof, and the gated DECOMMISSION phase are defined here.

---

## 1. When to Use / Boundaries

Use `migrate` when a change must propagate **exhaustively** across a codebase and partial application is a defect, not a milestone. The recipe's reason to exist is the **completeness guarantee** — if a single grep-and-replace would do, you do not need it.

**Cases (set via `case=`):**

| `case=` | Example | Inner-loop primary agent |
|---------|---------|--------------------------|
| `arch` | layered→hexagonal, monolith→modular, sync→event-driven | `atlas` (boundaries/ADR) → `builder` |
| `framework` | Express→Fastify, Vue2→Vue3, Redux→Zustand, JUnit4→5 | `shift` → `builder`/`artisan` |
| `middleware` | REST→gRPC, RabbitMQ→Kafka, Postgres→Cockroach, Redis swap | `shift` +`gateway`/`schema`/`stream` |
| `mock-to-prod` | stub/in-memory/MSW → real service/DB/API | `forge` boundary map → `builder` |
| `lang` | cross-language rewrite | **→ delegates to `transmute`** (see §7) |

| Not this | Route to | Why |
|----------|----------|-----|
| Cross-language rewrite | `transmute` (`migrate case=lang` is an alias that forwards) | Differential-parity oracle is the right backbone there |
| Web → iOS/Android native | `PORTING` (Port→Native) | Platform paradigm shift |
| Internal cleanup, no behavior/dependency change | `refactor` / `kaizen` | No migration surface |
| Single deprecated-API swap, ≤2 sites | `shift detect` directly | Completeness loop is overhead |
| One-off scoped feature | `feature` | Not a sweep |

**Four non-negotiable principles:**
1. **Freeze the denominator first.** INVENTORY counts the total change surface *before* any edit. Completeness is undefined without a baseline to be 100% *of*.
2. **Prove residue, do not trust the counter.** A forward "migrated N of M" counter can be wrong because INVENTORY itself can miss sites. Completeness is established by an **independent re-scan that finds zero**, looped until dry — not by the counter reaching M.
3. **Delete only after the proof.** DECOMMISSION is gated on ATTEST passing. Removing old code before residue==0 conflates "migration incomplete" with "deletion bug" and destroys the rollback story.
4. **Fix the loop, not the file.** When a batch fails VERIFY, the defect usually lives in the translation rule that produced it, not in that one site. Amend the RULEBOOK and regenerate the affected batch; hand-patching individual files leaves the bad rule in place and the same defect reappears in every later batch. Treat compiler errors and test failures as a **self-updating work queue** that refines the rulebook, and act on the *pattern* rather than the instance. [Source: claude.com/blog — *How Anthropic runs large-scale code migrations with Claude Code*, 2026-07-16]

Scale: 6–20 agents (case- and size-dependent), mid-to-high cost. **Confirm policy:** migrate inherently touches 10+ files, so it confirms **once at launch** (not per batch) — and again before the destructive DECOMMISSION CUT (§3 GATE). The generic per-edit "10+ files" Ask-First is satisfied by the launch confirm and does not re-fire each batch. Always confirm before launch when `case=arch` whole-system or strategy=big-bang.

---

## 2. Migration Strategy (selected at the STRATEGY step)

| Strategy | When | Mechanism | Risk |
|----------|------|-----------|------|
| **strangler-fig** (default) | Live system, seams exist | Old + new coexist behind a seam; migrate one batch at a time | Low — each batch independently verifiable & revertible |
| **parallel-run** | Old + new must agree on the **observable contract** before cutover (mock→prod, middleware swap) | Run old + new side by side, compare on the declared **conformance oracle** (see below), cut over when divergence==0 | Low-Med — needs shadow traffic / dual-write + a comparison harness that is itself DECOMMISSION scope |
| **big-bang** | Small/self-contained, or no seam possible | Whole change, single cutover | High — **requires user confirmation**; **collapses both loops** — no batches, so VERIFY is a single whole-change gate and rollback is a full revert, not per-batch |

`magi` arbitrates strategy at the STRATEGY step and owns the big-bang confirmation.

**parallel-run conformance oracle — what `divergence==0` means.** It is **not blanket value-equality**. Declare per output whether the comparison is:
- **value-equality** — same input must yield byte-identical output (pure transforms, deterministic middleware swaps where data is unchanged).
- **contract/shape-conformance** — same *schema, types, error contract, status, ordering guarantees, and SLA* — **but not the data values**. This is the **mandatory** mode for `mock-to-prod`: the mock returns canned data and production returns real data, so requiring value-equality would never converge. Comparing value-equality on mock→prod is a defect.

The parallel-run comparison harness, dual-write, and shadow-read scaffolding are **temporary** — they are explicit DECOMMISSION scope (§3), not permanent code.

---

## 3. Phase Contract — the double loop (AUTORUN chain template)

```
INVENTORY ── Lens[map all change sites] ‖ Ripple[blast radius] → freeze baseline manifest
              { total_sites, axes[], residue signatures } = the frozen denominator
              residue signature is TEXT (old symbols/APIs/imports) for framework/middleware/mock-to-prod,
              STRUCTURAL (boundary/dependency-rule violations) for case=arch (§3a check 2)
              axes[] are derived mechanically from a repo-structure + env scan, NOT free recall (§3a check 3)
   ▼
STRATEGY ── Magi[strangler-fig | parallel-run | big-bang + RISK GATE]
            Sherpa[split surface into atomic batches]  (when total_sites large / multi-component)
   ▼
RULEBOOK ── Scribe(+Atlas/Shift per case)[author the translation rulebook: per-pattern
            source→target mapping, ambiguity policy, and an explicit "flag, do not guess" list]
            The rulebook is the artifact batches are generated FROM — and the artifact that
            gets amended when a batch fails (§1.4). High-reasoning tier writes and reviews it.
   ▼
PILOT ───── run the full INNER LOOP on a small representative sample (a handful of sites
            spanning the §3a axes) BEFORE scale-out. Every pilot failure amends the RULEBOOK,
            never just the sampled files.
            GATE: pilot batch passes VERIFY with no un-ruled ambiguity → scale out.
   ▼
┌─ OUTER LOOP (completeness) — repeat until RESIDUE-GATE passes ──────────────┐
│                                                                            │
│  ┌─ INNER LOOP (per batch: PLAN → EXECUTE → VERIFY) ───────────────┐       │
│  │  PLAN     Ripple[batch-local dependency + ordering]              │       │
│  │  EXECUTE  case agent: Atlas/Shift/Forge → Builder/Artisan        │       │
│  │           (+gateway/schema/stream/native per case)               │       │
│  │  VERIFY   Radar[behavior preserved: build+test+type]             │       │
│  │           drift==0 = value-equality, EXCEPT mock-to-prod where    │       │
│  │           it is contract/shape conformance (§2 oracle), not values│       │
│  │           FAIL → rollback this batch; if the cause is a rule,     │       │
│  │           amend RULEBOOK and regenerate rather than hand-patching │       │
│  │           (§1.4); re-PLAN; do not advance                         │       │
│  └─────────────────────────────────────────────────────────────────┘       │
│                                                                            │
│  RESIDUE-GATE ★ completeness proof (§3a) — the integrity backbone           │
│     pass → exit OUTER LOOP ; not-dry → schedule remaining sites, loop       │
└────────────────────────────────────────────────────────────────────────────┘
   ▼
ATTEST ── Attest[completeness report: migrated==total, residue==0, drift==0, axes all covered]
   ▼
┌─ DECOMMISSION (old-code removal — GATED on ATTEST, destructive) ───────────┐
│  GATE      ATTEST passed AND announce-and-confirm (destructive, irreversible)│
│  DETECT    Sweep[old impl / mocks / dead adapters / orphans                 │
│            + parallel-run comparison harness / dual-write / shadow scaffolding]│
│  RE-CHECK  Ripple+Lens[residual references on the LATEST tree, == 0]        │
│  CUT       Builder[execute deletion]  +Void[YAGNI final pass]               │
│  VERIFY    Radar[still green after deletion: build+test+type]               │
│  SHIP      Guardian[deletion as a SEPARATE revertible commit/PR]            │
└────────────────────────────────────────────────────────────────────────────┘
```

**Parallelism:** INVENTORY branches (Lens ‖ Ripple) run concurrently. Independent batches in the OUTER loop may parallelize under `isolation: worktree` when strangler-fig gives non-overlapping seams (hub-spoke ownership, no shared mutable state).

**Model tiering across the loop.** Spend the high-reasoning tier where it changes the outcome — RULEBOOK authoring, PILOT failure diagnosis, and adversarial review of a batch — and run the high-volume translation itself on the balanced tier. This is the Plan-and-Execute split (`hub-authoring.md` § Model Selection) applied to a sweep, and it is what keeps a large migration's token cost proportionate; Anthropic's own million-line runs are budgeted this way.

**Checkpoint-resume:** ≥4 phases → persist the frozen baseline, the current RULEBOOK revision, per-batch VERIFY outputs, and the RESIDUE-GATE scan log at each boundary so an interrupted run resumes from the last completed batch with the denominator intact.

### 3a. RESIDUE-GATE — the completeness proof

A forward counter is necessary but **not sufficient**: it only knows about sites INVENTORY found. The gate establishes completeness through three independent checks, all of which must hold:

1. **Forward counter** — `migrated == total_sites` from the frozen baseline. Necessary, not sufficient.
2. **Independent residue re-scan (loop-until-dry)** — re-derive the residue from the *latest tree from scratch*, **by signature type**:
   - **Text-signature cases** (framework / middleware / mock-to-prod) — re-search for old symbols, old APIs, mock/stub boundaries, deprecated config keys, old framework imports.
   - **Structural-signature case** (`case=arch`) — text grep is **insufficient**: an architecture migration's residue is *boundary/dependency-rule violations*, not a string. Re-scan with `atlas` (dependency-direction / import-graph / layer-boundary lint) and count violations of the target boundary model as residue. Treating arch residue as a text pattern is the recipe's easiest false-"complete".
   Require **two consecutive scans returning zero** before declaring "dry" — catches dynamic/indirect references and sites INVENTORY never knew about. This, not the counter, is what proves no omission.
3. **Coverage-axis check** — `matrix` enumerates the change *dimensions* (layer, environment, platform/OS, file-type, service) and confirms **every axis was touched at least once**. Text search only finds *visible* sites; this catches a whole category silently forgotten (e.g. the staging config, the worker tier, the mobile build). **The axis list is itself a fallible denominator** — a forgotten axis cannot be checked. Mitigate by **deriving axes mechanically** from a repo-structure + environment/config + build-target scan (not from free recall), the same discipline transmute applies to oracle adequacy. Record the derivation source in the Completeness Report.

Plus `sweep` flags newly-orphaned code as an early DECOMMISSION signal.

**Gate verdict:** PASS only when (1) counter complete **and** (2) residue scan dry (2× zero) **and** (3) all axes covered. Any miss → schedule the uncovered sites/axes as a new batch and re-enter the OUTER loop. Record the achieved counts and the final residue-scan output in the Completeness Report.

---

## 4. Per-case detail

- **`case=arch`** — `atlas` owns the target boundary model + ADR before any batch; batches follow module seams. **Residue is structural, not textual** — `atlas` re-scans the dependency/import graph for target-boundary violations (§3a check 2), which a grep cannot establish. Whole-system arch change → confirm before launch. Watch for cross-cutting concerns (auth, logging, tx) as their own axis in the coverage check.
- **`case=framework`** — `shift` drives deprecated-API mapping; codemods where available. The old framework's import/annotation is the residue signature. JS/TS UI frameworks pull in `artisan`; test-framework migrations pull in `radar`.
- **`case=middleware`** — protocol/broker/store swap. `gateway` (API contract), `schema` (data store), `stream` (messaging) join EXECUTE. **Strategy defaults to parallel-run**: dual-write / shadow-read and compare until divergence==0 before cutover. Residue includes old client SDK usage + old connection config.
- **`case=mock-to-prod`** — `forge` first maps every mock/stub/in-memory/fixture seam (these are the change sites; they are the denominator). EXECUTE wires real services; `sentinel`/`crypt` join when the real path introduces secrets/credentials. Residue signature = the mock library imports + stub factory calls. **VERIFY uses the contract/shape-conformance oracle, not value-equality — mandatory for this case (§2)**, plus integration health.
- **`case=lang`** — forwards to `transmute`; the differential-parity oracle subsumes the residue concept. See §7.

---

## 4a. Termination Bound

Double loop, each separately bounded:

| Loop | Bound | Exit reasons |
|------|-------|--------------|
| **Inner** (per batch: PLAN → EXECUTE → VERIFY) | one pass per batch; a batch failing VERIFY is re-planned **`loop ≤ 3 cycles (default N=3)`** before escalating | `ACCEPT` (batch verified) · `cap-reached` → escalate the batch · `BLOCK` |
| **Outer** (completeness) | repeats until **RESIDUE-GATE** passes; bounded by the change-site denominator fixed at INVENTORY — the gate is the single termination oracle and cannot pass while residue > 0 | `ACCEPT` / `target-met` (residue = 0) · `BLOCK` (a site cannot be migrated — reported with the residual set) |

On any non-`ACCEPT` exit the recipe reports migrated-vs-residual sites explicitly and **DECOMMISSION stays gated** — old code is never removed on an unproven-complete run.

## 5. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Silent omission** — some sites never migrated, looks done | RESIDUE-GATE §3a check 2 (independent loop-until-dry re-scan), which is what proves completeness — not the forward counter of check 1 |
| **Incomplete inventory** — denominator itself missed sites | §3a checks 2 + 3 together: the re-scan starts from the latest tree, not the baseline, and axis coverage finds forgotten categories |
| **Forgotten dimension** — a whole tier/env/platform skipped | §3a check 3 (`matrix` coverage-axis), with axes derived mechanically rather than recalled |
| **Arch residue invisible to grep** (boundary still violated, no string to find) | §3a check 2's structural-signature branch — `atlas` boundary-violation re-scan for `case=arch` |
| **Same defect re-emerges in every batch** — fixed per-file instead of in the rule that produced it | RULEBOOK amend-and-regenerate loop (§1.4); hand-patching a generated site is the anti-pattern |
| **Systemic rule error discovered only at full scale** — the whole sweep has to be redone | PILOT gate: run the complete inner loop on a small cross-axis sample before scale-out |
| **Behavior drift mid-migration** | Inner-loop Radar VERIFY per batch (build+test+type); fail → rollback batch |
| **mock→prod never converges on value-equality** (real data ≠ canned data) | VERIFY/parallel-run uses the contract/shape-conformance oracle (§2) |
| **Deleting still-referenced old code** | DECOMMISSION gated on ATTEST + RE-CHECK residual references on latest tree before CUT |
| **parallel-run scaffolding left behind** (dual-write / shadow / comparison harness) | DECOMMISSION DETECT includes the comparison harness as removal scope |
| Destructive deletion run unattended | DECOMMISSION GATE = ATTEST pass AND announce-and-confirm before CUT |
| Deletion entangled with migration, un-revertible | Guardian ships deletion as a separate commit/PR |
| Big-bang risk blindness | Magi risk gate prefers strangler-fig; big-bang needs user confirm; big-bang collapses loops → single VERIFY + full revert |
| Batch ordering breaks dependents | Per-batch Ripple PLAN orders by dependency |

---

## 5a. Shared-Protocol References

`migrate` is a member of the Reproduce & Synthesize family and inherits its shared discipline rather than re-deriving it:

| Protocol | What migrate takes from it | Migrate-specific specialization |
|----------|---------------------------|--------------------------------|
| `_common/DIFFERENTIAL_PARITY.md` | Parity-over-faith, oracle adequacy, comparator/harness discipline, non-determinism gates | The parity claim here is **behavior preservation across the change**, not source-vs-target reproduction: the pre-migration build is the reference and each inner-loop VERIFY is a parity check against it. `case=lang` forwards to `transmute`, where the family's full differential-parity oracle applies unchanged |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, single termination oracle | RESIDUE-GATE is the outer loop's termination oracle; the inner loop's is per-site VERIFY |
| `reference/autonomy-quality-protocol.md` | Intent contract (Q1-Q3), producer ≠ verifier (Q9), Acceptance Provenance (Q15) | The change-site denominator *is* the intent contract; residual sites are reported per Q15, never silently dropped |

## 6. Add-ons

- `+Sentinel`/`+Crypt` — `mock-to-prod` introducing real credentials / secrets at the production boundary.
- `+Siege` — middleware swap motivated by throughput; verify load parity.
- `+Beacon` — production SLO watch during/after a live cutover.
- `+Trail` — regression archaeology when VERIFY catches drift of unknown origin.
- `+Sherpa` — decompose a large surface into atomic per-batch steps (default when total_sites large).
- `+Canon[regulatory]`/`+Cloak` — middleware/data migration crossing compliance or PII boundaries.

---

## 7. Decision Tree vs Neighbors

```
Change must propagate exhaustively across the codebase (omission = defect)?
  NO  → scoped feature? feature  | internal cleanup? refactor/kaizen  | ≤2-site API swap? shift detect
  YES → crossing a language boundary?
          YES → migrate case=lang  ==  transmute (differential parity oracle)
          NO  → target is mobile-native from Web? PORTING
                otherwise → migrate (case = arch | framework | middleware | mock-to-prod)
```

`migrate` is the completeness-guaranteed sweep; `transmute` is its language-pair specialization (parity oracle replaces the residue scan); `shift` is the agent that executes framework/dependency steps *inside* migrate's EXECUTE; `refactor` changes no external behavior and needs no residue proof.

---

## 8. Output

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus a **Completeness Report**:
- `case`, strategy, and total_sites (frozen baseline) vs migrated.
- **RULEBOOK trail**: the pilot's verdict and each subsequent rulebook amendment with the batch failure that prompted it — this is the audit trail showing defects were fixed in the rule rather than per file (§1.4).
- **RESIDUE-GATE result**: the §3a three-check verdict with its evidence — final residue-scan output, counter completeness, and the `matrix` axis-coverage table (every axis touched + axis-derivation source).
- Per-batch VERIFY summary, naming the oracle applied per §2.
- **DECOMMISSION result**: old code removed, RE-CHECK residual-reference count (==0 before CUT), post-deletion Radar green, and the separate deletion PR reference.
- For strangler-fig runs, each batch + the decommission are separate revertible PRs.
