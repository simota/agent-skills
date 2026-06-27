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

**Three non-negotiable principles:**
1. **Freeze the denominator first.** INVENTORY counts the total change surface *before* any edit. Completeness is undefined without a baseline to be 100% *of*.
2. **Prove residue, do not trust the counter.** A forward "migrated N of M" counter can be wrong because INVENTORY itself can miss sites. Completeness is established by an **independent re-scan that finds zero**, looped until dry — not by the counter reaching M.
3. **Delete only after the proof.** DECOMMISSION is gated on ATTEST passing. Removing old code before residue==0 conflates "migration incomplete" with "deletion bug" and destroys the rollback story.

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
┌─ OUTER LOOP (completeness) — repeat until RESIDUE-GATE passes ──────────────┐
│                                                                            │
│  ┌─ INNER LOOP (per batch: PLAN → EXECUTE → VERIFY) ───────────────┐       │
│  │  PLAN     Ripple[batch-local dependency + ordering]              │       │
│  │  EXECUTE  case agent: Atlas/Shift/Forge → Builder/Artisan        │       │
│  │           (+gateway/schema/stream/native per case)               │       │
│  │  VERIFY   Radar[behavior preserved: build+test+type]             │       │
│  │           drift==0 = value-equality, EXCEPT mock-to-prod where    │       │
│  │           it is contract/shape conformance (§2 oracle), not values│       │
│  │           FAIL → rollback this batch, re-PLAN; do not advance     │       │
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

**Checkpoint-resume:** ≥4 phases → persist the frozen baseline, per-batch VERIFY outputs, and the RESIDUE-GATE scan log at each boundary so an interrupted run resumes from the last completed batch with the denominator intact.

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

- **`case=arch`** — `atlas` owns the target boundary model + ADR before any batch; batches follow module seams. **Residue is structural, not textual**: `atlas` re-scans the dependency/import graph for target-boundary violations (§3a check 2) — RESIDUE-GATE is dry only when violation count is zero, which a grep cannot establish. Whole-system arch change → confirm before launch. Watch for cross-cutting concerns (auth, logging, tx) as their own axis in the coverage check.
- **`case=framework`** — `shift` drives deprecated-API mapping; codemods where available. The old framework's import/annotation is the residue signature. JS/TS UI frameworks pull in `artisan`; test-framework migrations pull in `radar`.
- **`case=middleware`** — protocol/broker/store swap. `gateway` (API contract), `schema` (data store), `stream` (messaging) join EXECUTE. **Strategy defaults to parallel-run**: dual-write / shadow-read and compare until divergence==0 before cutover. Residue includes old client SDK usage + old connection config.
- **`case=mock-to-prod`** — `forge` first maps every mock/stub/in-memory/fixture seam (these are the change sites; they are the denominator). EXECUTE wires real services; `sentinel`/`crypt` join when the real path introduces secrets/credentials. Residue signature = the mock library imports + stub factory calls. **VERIFY uses the contract/shape-conformance oracle, NOT value-equality** (§2): the mock's canned data and the real service's data differ by design, so the gate checks schema / types / error contract / status / SLA conformance and integration health — never `realOutput == mockOutput`. Requiring value parity here never converges and is a defect.
- **`case=lang`** — forwards to `transmute`; the differential-parity oracle subsumes the residue concept. See §7.

---

## 5. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Silent omission** — some sites never migrated, looks done | RESIDUE-GATE independent re-scan, loop-until-dry (2× zero), not the forward counter |
| **Incomplete inventory** — denominator itself missed sites | Re-scan from scratch on the latest tree + `matrix` axis coverage (finds forgotten categories) |
| **Forgotten dimension** — a whole tier/env/platform skipped | Coverage-axis check enumerates dimensions, requires each touched |
| **Arch residue invisible to grep** (boundary still violated, no string to find) | `case=arch` residue = `atlas` dependency/boundary-violation re-scan, not text (§3a check 2) |
| **Behavior drift mid-migration** | Inner-loop Radar VERIFY per batch (build+test+type); fail → rollback batch |
| **mock→prod never converges on value-equality** (real data ≠ canned data) | VERIFY/parallel-run uses contract/shape-conformance oracle, not value parity (§2, §4) |
| **Deleting still-referenced old code** | DECOMMISSION gated on ATTEST + RE-CHECK residual references on latest tree before CUT |
| **parallel-run scaffolding left behind** (dual-write / shadow / comparison harness) | DECOMMISSION DETECT includes the comparison harness as removal scope |
| Destructive deletion run unattended | DECOMMISSION GATE = ATTEST pass AND announce-and-confirm before CUT |
| Deletion entangled with migration, un-revertible | Guardian ships deletion as a separate commit/PR |
| Big-bang risk blindness | Magi risk gate prefers strangler-fig; big-bang needs user confirm; big-bang collapses loops → single VERIFY + full revert |
| Batch ordering breaks dependents | Per-batch Ripple PLAN orders by dependency |

---

## 6. Add-ons

- `+Sentinel`/`+Crypt` — `mock-to-prod` introducing real credentials / secrets at the production boundary.
- `+Siege` — middleware swap motivated by throughput; verify load parity.
- `+Beacon` — production SLO watch during/after a live cutover.
- `+Trail` — regression archaeology when VERIFY catches drift of unknown origin.
- `+Sherpa` — decompose a large surface into atomic per-batch steps (default when total_sites large).
- `+Oath`/`+Cloak` — middleware/data migration crossing compliance or PII boundaries.

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
- **RESIDUE-GATE result**: final residue-scan output (must be the 2× zero proof; for `case=arch`, the `atlas` boundary-violation count), counter completeness, and the `matrix` axis-coverage table (every axis touched + axis-derivation source).
- Per-batch VERIFY summary (value-equality, or — for mock→prod — contract/shape-conformance verdict).
- **DECOMMISSION result**: old code removed, RE-CHECK residual-reference count (==0 before CUT), post-deletion Radar green, and the separate deletion PR reference.
- For strangler-fig runs, each batch + the decommission are separate revertible PRs.
