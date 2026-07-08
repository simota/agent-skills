# Recipe Contract — canonical structure & vocabulary for nexus recipes

**Purpose:** The authoring standard every nexus **recipe reference** (`reference/*-recipe.md`, plus the inline contracts in `reference/inline-recipes.md`) is held to. nexus recipes are heavyweight multi-agent orchestrations — distinct from the lightweight cross-skill Recipe/Subcommand protocol in `_common/RECIPES.md`, which governs the SKILL.md `## Recipes` table and naming. This file is the **measuring stick** for consistency audits and the source of the canonical phrasings that prevent drift.

**Read when:** authoring a new recipe, leveling up a thin one, or normalizing phrasing across recipes.

---

## 1. The eight required elements

A complete recipe reference carries all eight (mark `N/A` with a one-line reason where a shape genuinely lacks one — e.g. a non-looping recipe has no loop cap):

| # | Element | What it must state |
|---|---------|--------------------|
| 1 | **Termination bound** | For any loop: the cap + the exit-reason vocabulary (§2). Non-loop recipes: `N/A`. |
| 2 | **Confirm / safety gate** | Which actions stop for confirmation and at which tier (§3). |
| 3 | **Resume** | The checkpoint/draft/run-log mechanism, or `N/A` with reason (§4). |
| 4 | **Output report** | A *named* report on top of `## Nexus Execution Report` (§5). |
| 5 | **Failure Modes Prevented** | A consolidated section (canonical heading `## Failure Modes Prevented`), not only phase-scoped notes. |
| 6 | **Boundaries / vs neighbors** | A "vs <neighbor recipe>" block + a Decision Tree where ≥1 sibling exists. |
| 7 | **Scale** | Agent-count range (× cycles for loops) and relative cost. |
| 8 | **Shared-protocol refs** | Cite the `_common/` protocol instead of re-deriving it (§6). |

The gold-standard exemplars are `reference/spec-recipe.md` and `reference/clone-recipe.md` (both carry all eight).

---

## 2. Termination-bound vocabulary (canonical)

Use **one** phrasing for the loop cap: **`loop ≤ N cycles (default N=3)`** (podium's default is 2). Do not introduce `cap 3` / `max 3` / `capped at 3 iterations` / `max_loops: 3` as separate phrasings for the same thing — they read as different rules.

Every loop states its **exit reason** from this fixed vocabulary:

| Exit reason | Meaning |
|-------------|---------|
| `ACCEPT` / `target-met` | the quality bar / quantified target was reached |
| `diminishing-returns (Δ < ε)` | marginal gain fell below threshold |
| `cap-reached` | hit `N` cycles without acceptance |
| `BLOCK` | a hard blocker needs escalation |

On any non-`ACCEPT` exit the recipe **reports best-so-far + the residual gap** — never silently stops, never burns cycles past marginal value. The rich loop machinery (Generator-Evaluator separation, single termination oracle, flatten rule) lives in `reference/evaluator-loop-protocol.md`; loop recipes reference it rather than re-specifying it.

---

## 3. Confirm / safety-gate tiers (canonical)

Four tiers — use the exact tier name so the strength is unambiguous:

| Tier | Phrasing | When |
|------|----------|------|
| **AUTORUN-cannot-skip** | "contract-level checkpoint; AUTORUN cannot skip" | the checkpoint *is* the deliverable (spec dialogue, clone Stack Dialogue, verdict card) |
| **Confirm-before-launch** | "Confirm before launch when `<condition>`" | expensive/destructive launch (big-bang, sources ≥ 3, Tier-S) |
| **Ask First** | "Ask First" | L4 security, destructive data, `PUBLIC_API`/`DATA` blast radius, 10+ files |
| **announce-and-proceed** | "announce-and-proceed (no objection window)" | runs-to-completion recipes (enact) where only §8 red lines stop |

When two sibling recipes deliberately differ (summit = unconditional confirm vs podium = conditional), **say it is intentional** so it doesn't read as drift.

---

## 4. Resume mechanisms (canonical)

State the rule as **"Checkpoint-resume: recipes with ≥ 4 phases persist phase outputs at each boundary so an interrupted run resumes from the last checkpoint."** (Do not phrase the same rule as "4+ step chains" elsewhere.) Four mechanisms, each legitimate for its shape — name which one applies:
- **checkpoint-resume** (default; apex/clone/fuse/graft/migrate/transmute/converge/summit/podium)
- **draft-resume** (`spec resume` — the dialogue draft is the state)
- **run-log-tail** (`enact resume` — the append-only run log is the state)
- **schedule-resume** (growth-acceptance — +14/+30/+90d cadence)

A recipe with ≥ 4 phases and none of these is a gap, not a style choice.

---

## 5. Output-report naming (canonical)

Every recipe emits `NEXUS_COMPLETE` with the base `## Nexus Execution Report` (`reference/output-formats.md`) **plus a named recipe report**. The name is stable and recipe-specific: **Parity** (transmute), **Fidelity** (clone), **Fusion** (fuse), **Graft** (graft), **Completeness** (migrate), **Convergence** (converge), **Before/After** (kaizen). A heavyweight recipe that emits only an unnamed `NEXUS_COMPLETE` (apex, enact) is missing element #4 — give it a named report (e.g. apex **Delivery Report**, enact **Execution Report**).

---

## 6. Shared protocols (cite, don't re-derive)

| Protocol | Owns | Recipes that must cite it |
|----------|------|---------------------------|
| `_common/DIFFERENTIAL_PARITY.md` | parity-over-faith, oracle adequacy + non-determinism gates, comparator/harness, provenance/drift | transmute, clone, fuse, graft, migrate |
| `reference/verdict-gate.md` | verdict card, Yes/No/Modify branches, flag+KPI+kill | essential, killer, trim, graft (flag clause) |
| `_common/ADVERSARIAL_REFUTATION.md` | skeptic panel, evidence-vs-novelty, polarity, exclusions | killer, trim, graft |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, single termination oracle, flatten rule | converge, kaizen, apex, summit, podium |
| `_common/TRACEABILITY.md` | canonical AC/REQ IDs | spec, accord-driven recipes, attest gates |
| `reference/dialogue-protocol.md` | question craft, answer processing, Assumption Ledger, checkpoint presentation, Provenance Gate for contract-level dialogue | spec, delve (mandatory); gedanken INTERACTIVE, clone Stack Dialogue, verdict cards (D1–D4/D10–D11 only) |
| `reference/autonomy-quality-protocol.md` | intent contract, Decision Ledger, drift control, producer≠verifier, evidence-bound claims, Acceptance Provenance | all autonomous (non-dialogue) recipes + ad-hoc chains; recipes cite it and add only specializations (parity oracles satisfy Q3/Q10; acceptance G1–G10 subsume Q11) |
| `reference/doc-quality-protocol.md` | reader contract, universal grounding / UNKNOWN-over-fabrication, cross-doc single source of truth, summary-first readability, Doc Quality Gate (W12 = Q11 for documents) | package, charter, layer, podium, spec/delve artifacts, gedanken reports, any doc-authoring step; native gates (podium Verification Team, Spec Quality Gate, package Phase 5) subsume W12 and add only missing dimensions |
| `_common/PROOF_CARRYING.md` | G1-G10 proof-carrying merge | acceptance, growth-acceptance |

A recipe re-describing a primitive a `_common/` protocol already owns is drift — replace the prose with a citation + the recipe-specific specialization only.

---

## 7. Authoring checklist

Before a recipe reference is "done": all eight §1 elements present (or `N/A` + reason) · loop phrasing matches §2 · confirm tier named per §3 · resume mechanism named per §4 · report named per §5 · every reused primitive cites its §6 protocol · Failure Modes Prevented is a consolidated section, not scattered notes.

## 8. Cross-index wiring checklist (adding a NEW recipe)

A recipe is not "live" until it appears — consistently — in **every** index, not just its own reference file. Omitting one is how a recipe becomes unroutable or mis-grouped (e.g. the signal-keywords mis-filing that put loop/reproduction recipes under "Mobile Native"). Wire all six:

1. `reference/<name>-recipe.md` — the deep contract (this file's §1-§7).
2. `SKILL.md` `## Recipes` table — one row (Recipe · Subcommand · When to Use · Chain Template · Read).
3. `SKILL.md` `### Recipe Families` — add to the right family (create one only if no family fits); state the within-family distinguishing axis.
4. `SKILL.md` `### Signal Keywords` inline table — add the most-used anchors (subset of #6).
5. `SKILL.md` `## Reference Map` — one row pointing at the new reference file.
6. `reference/signal-keywords.md` — the **canonical full** anchor row, under the **correct section header** (Core / Specialist / Loop-Migration-Reproduction / Package), with English anchors + key non-English paraphrases.
7. `reference/recipes-detail.md` — the extended description + chain template (the catalog every recipe appears in).

Consistency rule: the recipe's name, one-line purpose, agent count, and confirm tier must read **identically** across #2/#6/#7 (no drift between the SKILL.md row and the detail/keyword entries).
