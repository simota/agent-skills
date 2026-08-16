# Harness Debt — the decay axis of an agent ecosystem

**Purpose:** Track and pay down the *degradation* of the control system agents work through — instructions, references, routing, verification — as distinct from duplication (`prune`) and inactivity (`darwin` Activity). A skill can be unique, actively used, and still be debt: if its Architecture Map is stale, every invocation pays interest in retries and human corrections.

**Read when:** running a `darwin` ecosystem review, a `prune` roster audit, a `gauge` compliance sweep, or whenever a skill fails the same way twice and the cause is not the model.

**Boundary.** Technical Debt is the future cost of *code*. Harness Debt is the future cost of *the system agents reason and act through*. They overlap and are not the same: a tangled legacy module is technical debt; an architecture map that makes every agent pick the wrong entry point is harness debt. Adapted for this repository, where the harness is the SKILL.md corpus, `_common/` protocols, routing matrix, and lint scripts.

---

## 1. Debt Catalog

Sixteen categories. Each is a *mechanism of decay*, not a style complaint.

| ID | Category | What it looks like here |
|----|----------|-------------------------|
| `HD-DOC` | Stale Documentation | A `reference/` file describing a workflow, CLI flag, or file path that no longer exists |
| `HD-ORACLE` | Missing Test Oracle | A skill whose Core Contract cannot be checked by any script, fixture, or reviewer rubric |
| `HD-FLAKE` | Flaky Eval | `task-battery.md` / `routing-oracle.py` cases whose pass/fail flips without a corpus change |
| `HD-OPAQUE` | Opaque Tool | A skill whose `description` does not let the router decide *when not to* use it |
| `HD-ERR` | Unstructured Error | A failure mode reported as prose with no code, location, or next safe action |
| `HD-PERM` | Excessive Permission | A skill or recipe authorized for a side effect broader than its contract needs |
| `HD-TACIT` | Hidden Human Knowledge | A step that only works because the operator remembers something undocumented |
| `HD-VER` | Unversioned Prompt | Instruction text changed without a trace of what changed or why |
| `HD-MODEL` | Undocumented Model Dependency | Behavior that silently assumes a specific engine, tier, or context window |
| `HD-TRACE` | Trace Gap | A chain step whose outcome cannot be reconstructed from `.agents/` journals |
| `HD-STATE` | State Ambiguity | Handoff fields that do not distinguish claimed state from verified state |
| `HD-REPRO` | Irreproducible Environment | A documented command that does not run clean on a fresh checkout |
| `HD-ENTROPY` | Agent-generated Complexity | Near-duplicate references, adapter layers, and conditional branches accumulated by prior agent runs |
| `HD-DRIFT` | Architecture Drift | Declared structure (`CLAUDE.md`, routing matrix) diverging from the actual corpus |
| `HD-GAME` | Eval Gaming | A check that passes by construction — the metric moved, the property did not |
| `HD-LOOP` | Broken Feedback Loop | Findings that never reach the file that would prevent recurrence |

**Rule:** `HD-GAME` and `HD-LOOP` are the two that hide the other fourteen. Audit them first.

---

## 2. Debt Register

One entry per confirmed debt. Symptom and interest are **required** — a category with neither is an opinion, not debt.

```yaml
debt_id: HD-0042
category: stale-documentation      # from the catalog above
asset: nexus/reference/routing-matrix.md
symptom:
  - router selects a deprecated recipe for migration tasks
interest:
  human_corrections_per_month: 4
  failed_or_reworked_runs_per_month: 2
risk: high                          # low | medium | high | critical
owner: nexus
introduced: 2026-04-12              # or "unknown" — do not guess
paydown:
  - update the recipe table
  - add a routing-oracle case pinning the correct selection
status: planned                     # planned | in-progress | paid | accepted
review_by: 2026-09-30
```

**Interest need not be money.** Record it as whatever the debt actually costs: repeated corrections, reruns, clarifying questions, review minutes, escaped defects. An entry that cannot name a recurring cost is closed as `accepted`, not carried.

**`accepted` is a legitimate terminal state.** Not every debt is worth paying. Accepting it with a named risk and an owner is honest; leaving it `planned` for a year is the register decaying into its own `HD-LOOP`.

---

## 3. Gardening — the three recurring sweeps

Debt is found by sweeps, not by inspiration. Each sweep has a trigger and a disposal rule.

### Documentation Gardening

Signals: stale link · missing `owner` / `last_verified` · zero usage · search miss · repeated agent clarification on the same point · superseded chain.

Disposal: **update, archive, or delete — never leave an unread file in place.** An unread reference costs context budget on every progressive-disclosure scan and teaches nothing.

### Skill Gardening (the "Tool Registry" sweep)

Signals: duplicate capability · low selection with high correction rate · deprecated workflow · authority broader than the contract · oversized output · missing or drifted `description` trigger words · no owner.

Disposal: merge, narrow, or sunset via `prune`'s sunset protocol. When retiring a skill, keep an alias and a deprecation window, and update every routing reference in the same change — a retired skill still named in `routing-matrix.md` is a fresh `HD-DRIFT`.

### Eval Gardening

Signals: fixture drift from real usage · flaky or infra-caused failures · leakage between fixture and corpus · rubric drift · cases too expensive to keep running · cases no longer decision-relevant · a failure class with no case at all.

Disposal: split the suite into **Core** (every run), **Extended** (per review cycle), and **Audit** (on demand). Growing one undifferentiated suite raises cost and lowers signal at the same time.

---

## 4. Ownership and cadence

| Sweep | Owner | Cadence |
|-------|-------|---------|
| Documentation Gardening | `gauge` | 30-day review cycle |
| Skill Gardening | `prune` | 30-day review cycle |
| Eval Gardening | `darwin` | 30-day review cycle, plus after any harness regression |
| Register triage | `darwin` | same cycle — the register is an input to the ecosystem review, not a separate ritual |

Register location: `.agents/HARNESS_DEBT.md` (journal-side, gitignored). Confirmed structural debt that requires a corpus change is promoted to an `EVOLUTION_SIGNAL` (`_common/EVOLUTION.md`).

---

## 5. Anti-patterns

- **Cataloguing without interest.** A list of every imperfection is not a register; it is a second `HD-DOC`.
- **Paying the cheap debt first.** Order by interest × risk, not by how easy the fix looks.
- **Counting files as coverage.** More references is not less debt — `HD-ENTROPY` is measured by near-duplication and branch count, not volume.
- **Letting the debtor grade the debt.** The skill that owns an asset does not decide alone whether its own debt is `accepted` (see `_common/SELF_EVOLUTION.md` § Change Class — this is a `C4` judgment).
