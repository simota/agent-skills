# Harness Debt — the decay axis of an agent ecosystem

**Purpose:** Track and pay down the *degradation* of the control system agents work through — instructions, references, routing, verification — as distinct from duplication (`prune`) and inactivity (`darwin` Activity). A skill can be unique, actively used, and still be debt: if its Architecture Map is stale, every invocation pays interest in retries and human corrections.

**Read when:** running a `darwin` ecosystem review, a `prune` roster audit, a `gauge` compliance sweep, whenever a skill fails the same way twice and the cause is not the model, or when a restated fact (a count, a list, a summary) disagrees with the source it came from (§2b).

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

## 2b. Derived Register — freshness for the assets nobody authors

`HD-DRIFT` and `HD-DOC` are found by *reading* a file. A **derived** asset — one restated or generated from a source elsewhere in the corpus — decays without anyone touching it: the source moves, the restatement does not. Nobody is editing the wrong file, so no sweep that looks for bad edits will find it. The fix is to name the derivation, not to read harder.

**Four staleness classes, four different repairs.** Collapsing them into "it's out of date" is why regenerating more often does not help.

| Class | What happened | Repair |
|-------|---------------|--------|
| **Source stale** | The derivation ran, but against an already-outdated source | Fix the source; the derived asset was never the problem |
| **Generation stale** | Source changed; the derived asset was never re-derived | Bind a regeneration trigger to the source change |
| **Publication stale** | Re-derived, but the new value never reached the file that states it | Include every consumer in the same change, not a follow-up |
| **Consumption stale** | Corpus is correct; an agent or session is running on a cached or remembered older value | Invalidate the cache and re-read the source; a stored memory entry restating a count is itself a derived asset |

**Register entry.** One per derived asset. `source`, `check`, and `delete_route` are required — a derivation whose freshness cannot be tested is `HD-ORACLE`, not a derived asset, and one whose *removal* cannot be tested is the same defect on the other axis.

```yaml
derived: compass/reference/recipes-directory.md
source: every <skill>/SKILL.md `## Recipes` table
rule: _common/scripts/generate-recipes-directory.py   # or "manual restatement"
check: re-run the generator; a non-empty diff is generation-stale
trigger: any Recipe/Subcommand change
consumers: [compass]
delete_route: re-run the generator after the source row is gone; the entry must not reappear
```

### `delete_route` — a derived asset that cannot be removed must not be created

Freshness answers "did the new value arrive". It does not answer "did the old value leave". Those fail
separately: a register that only tests regeneration will pass a corpus where a retired skill still appears
in half its consumers, because every one of them was regenerated — from a source list that still named it.

**Admission rule.** Adding a derived asset requires stating how it is removed, not only how it is refreshed.
A derivation with no `delete_route` is not registered and not created; if it already exists, it is an
`HD-DRIFT` entry with an owner, not an accepted state.

**`delete_route` states the removal path and its test**, in the same form `check` uses: the action that
removes the derived value when the source row disappears, and the observation that proves it is gone. For a
generated file that is "re-run the rule and confirm the entry is absent"; for a manual restatement it is the
grep that must return zero hits.

**Removal is verified by absence, not by intent.** A removal is complete when a search for the retired
identifier returns nothing across every consumer named in the register — not when the removal steps were
performed. Report the search that was run and its result; "updated the references" is not the same claim as
"zero references remain", and only the second one is checkable.

**Scope creeps downstream, so enumerate before removing.** The consumers of a derived asset are the reach of
its deletion. For a retired skill that set is larger than the skill's own directory: pack membership,
profile lists, routing and recipe tables, signal keywords, disambiguation entries, boundary definitions, the
`COLLABORATION_PATTERNS` and `BIDIRECTIONAL_PARTNERS` blocks of every skill that names it, and any memory
entry restating a count that included it. Missing one leaves a reference to something that no longer exists
— the same `HD-DRIFT` the register exists to prevent, created by the cleanup itself.

**Records are exempt** (see "A Record is not a derived asset" below). Changelog entries, archive notes, and journal history are supposed to
name things that no longer exist. Removal applies to assets that assert a *current* state, never to records
of a past one.

**Standing register for this corpus.** Anything listed here is not hand-maintained truth; the `source` column is.

| Derived asset | Source (authoritative) | Rule | Freshness check |
|---------------|------------------------|------|-----------------|
| `compass/reference/recipes-directory.md` | each `SKILL.md` `## Recipes` table | `_common/scripts/generate-recipes-directory.py` | re-run; diff must be empty |
| Every skill-count claim (`README.md`, `CLAUDE.md`, `AGENTS.md`, `_common/SKILL_PACKS.md`, `_common/RECIPES.md`, `compass/SKILL.md`, `compass/reference/cache-format.md`, `nexus/reference/task-battery.md`) | the skill directory listing | manual restatement | `ls -d */ \| grep -v '^_' \| wc -l` equals every stated number |
| `nexus/SKILL.md` Recipe Registry allowlist | `nexus/reference/recipes-index.md` Subcommand column | manual restatement | the two token sets are equal |
| `CAPABILITIES_SUMMARY` block in each `SKILL.md` | that skill's own body | manual restatement | every summarized capability is still claimed in the body |
| `.claude/compass-cache.md` | `compass/reference/catalog.md` | `/compass refresh` | regenerate rather than hand-edit |
| Per-spawn grants in the Delegation record (`nexus/reference/autonomy-quality-protocol.md` §8) | that task type's current Autonomy Ledger tier (`nexus/reference/routing-learning.md` § Autonomy Ledger) | manual restatement | no spawn's grant exceeds what its task type's tier allows; a **demotion invalidates grants issued under the old tier**, so grants outliving a demotion are generation-stale |

**Delete routes for the rows above**, in the same order, plus whole-skill removal — which is not a row in the
register because it retires every row at once. Each states what removes the value and what proves it left.

| Derived asset | Delete route (action → proof) |
|---------------|------------------------------|
| `compass/reference/recipes-directory.md` | re-run the generator after the `## Recipes` row is gone → the recipe token is absent from the output |
| Every skill-count claim | re-count and restate in the same change → `ls -d */ \| grep -v '^_' \| wc -l` equals every stated number again |
| `nexus/SKILL.md` Recipe Registry allowlist | drop the token from `recipes-index.md` first, then the allowlist → the two token sets are equal and neither contains it |
| `CAPABILITIES_SUMMARY` block | remove the entry when the body stops claiming it → no summarized capability lacks a body claim |
| `.claude/compass-cache.md` | `/compass refresh` after the catalog entry is gone → regenerated cache does not name it |
| Per-spawn grants in the Delegation record | revoke on tier demotion → no live grant exceeds its task type's current tier |
| **A retired skill's name** (whole-skill removal) | `prune`'s sunset protocol across every consumer above → a repo-wide search for the skill name returns zero hits outside `.archive/` and records |

**Authority registers drift against each other, not against a file.** The row above is the one derivation in
this register whose staleness is a *safety* property rather than a documentation one: three authority records
exist (the Autonomy Ledger, the per-spawn Delegation record, and any grant a running chain still holds), and
nothing re-reads the first when the second was written. Demotion is automatic and instant; a grant issued
minutes earlier is not withdrawn by it. Treat the tier as the `source` and every live grant as derived from
it — an unrevoked grant under a demoted tier is the same class of defect as a regenerated file nobody
republished, and it is found the same way: by testing the derivation, never by reading either record alone.

**A Record is not a derived asset.** `CHANGELOG.md` entries, calibration notes ("calibrated against a 132-skill corpus"), and journal history state what was true at a past moment. They are not stale and must not be "corrected" to today's value — rewriting them destroys the only evidence of when the corpus changed.

**Manual edits to a derived asset.** Permitted only as an **overlay**: a section the rule does not generate, preserved across regeneration and marked as such. A hand-edit inside generated territory is repaid by fixing the source and re-deriving — patching the output leaves the rule that produced the wrong value in place, so the next regeneration reintroduces it.

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

## 3b. Complexity Budget — the prevention side of `HD-ENTROPY`

Sweeps find debt after it accrues. A Complexity Budget stops the accrual at the point of addition: **every new control must state what it costs and when it leaves.** Each added guardrail, gate, routing branch, protocol file, or validation layer declares four fields before it lands:

| Field | Question |
|-------|----------|
| `failure` | Which specific failure does this control catch? Name it, not a category |
| `effect` | What evidence shows it catches it — and what it does *not* catch |
| `owner` | Who maintains it when the surrounding harness moves |
| `removal` | The condition under which it should be deleted |

A control with no `removal` condition is permanent by default, and permanence is how a harness accumulates layers no one can justify or safely remove. The most common miss is `effect`: a control added on intuition, never measured, and then defended by the effort it took to build.

**Where the budget is enforced.** A budget declared in one file and required by none is itself `HD-LOOP`. These are the admission points that MUST collect the four fields before the addition lands; each rejects rather than accepts a blank `removal`:

| Addition | Gate | Enforced in |
|----------|------|-------------|
| A new ecosystem skill | Architect's gap-fill proposal, before Nexus pre-registration | `architect/SKILL.md` → `## Complexity Budget Gate` |
| A new Nexus Recipe | Recipe Admission Gate condition 5 | `nexus/reference/recipe-contract.md` |
| A new project-local skill / rule / workflow | Sigil's operating-layer authoring | `sigil/SKILL.md` |
| A new `_common/` protocol, gate, or routing branch | The proposing agent, in the change itself | this section |

The fields live in the artifact they govern (`## Lifecycle` in `_templates/SKILL_TEMPLATE.md`), not in a separate register — a register of removal conditions decays faster than the controls it tracks. Existing controls are **not** retro-fitted on a sweep: an unbudgeted control that has never cost anything is not debt, and cataloguing all of them is the § 5 anti-pattern. It acquires the four fields the next time it is edited for another reason.

**Centralization has the same asymmetry.** Shared control reduces duplication and *widens the failure domain* — a routing rule, a common gate, a `_common/` protocol becomes a single blast radius for every skill downstream. Apply the same discipline to the shared layer that the shared layer imposes: canary it, budget it, own it, and be able to roll it back. Consolidate only when three or more skills hit the same cross-cutting problem and a common owner exists; where consolidation raises coordination cost instead of lowering it, move the boundary back.

---

## 4. Ownership and cadence

| Sweep | Owner | Cadence |
|-------|-------|---------|
| Documentation Gardening | `gauge` | 30-day review cycle |
| Skill Gardening | `prune` | 30-day review cycle |
| Eval Gardening | `darwin` | 30-day review cycle, plus after any harness regression |
| Near-duplication sweep (`HD-ENTROPY`) | `prune` | 30-day review cycle. Scope is the roster **and one level down** — `_common/` protocols and `*/reference/` files. A near-duplicate reference is roster overlap that never reached the roster, which is why the corpus can pass a Skill Gardening sweep and still accrue `HD-ENTROPY`. Candidates are confirmed by **merging**, not by heading or token similarity: a pair is duplication only if the merged text loses no claim and the net line count falls. Similarity alone has measured a false-positive rate near half. |
| Derived Register freshness (§2b) | `gauge` | same cycle, plus before any release-shaped change — run every `check` column; a failure names its staleness class |
| Register triage | `darwin` | same cycle — the register is an input to the ecosystem review, not a separate ritual |

Register location: `.agents/HARNESS_DEBT.md` (journal-side, gitignored). Confirmed structural debt that requires a corpus change is promoted to an `EVOLUTION_SIGNAL` (`_common/EVOLUTION.md`).

---

## 5. Anti-patterns

- **Cataloguing without interest.** A list of every imperfection is not a register; it is a second `HD-DOC`.
- **Paying the cheap debt first.** Order by interest × risk, not by how easy the fix looks.
- **One repair for all staleness.** Re-deriving fixes generation-stale only. A value that is right in the corpus and wrong in a session's memory is consumption-stale, and regenerating it a third time changes nothing.
- **Counting files as coverage.** More references is not less debt — `HD-ENTROPY` is measured by near-duplication and branch count, not volume.
- **Letting the debtor grade the debt.** The skill that owns an asset does not decide alone whether its own debt is `accepted` (see `_common/SELF_EVOLUTION.md` § Change Class — this is a `C4` judgment).
