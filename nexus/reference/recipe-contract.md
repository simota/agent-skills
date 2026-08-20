# Recipe Contract — canonical structure & vocabulary for nexus recipes

**Purpose:** The authoring standard every nexus **recipe reference** (`reference/*-recipe.md`, plus inline contracts in `reference/inline-recipes.md`) is held to. A Recipe is a reusable orchestration preset over existing specialist boundaries, not a new Nexus domain capability: it owns chain selection/order, handoffs, termination, and verification, while specialists own methodology and work products. This differs from the lightweight cross-skill Recipe/Subcommand protocol in `_common/RECIPES.md`.

**Read when:** authoring a new recipe, leveling up a thin one, or normalizing phrasing across recipes.

---

## Recipe Admission Gate

This gate applies to every **new** Recipe proposal; existing Recipe contracts are not re-admitted by this gate. Admit only when **all** conditions pass:

1. **Cross-boundary:** the workflow requires at least two distinct specialist boundaries from `_common/BOUNDARIES.md`; multiple agents inside one specialist responsibility do not qualify.
2. **Reusable orchestration value:** cite at least three independent occurrences (completed runs, repeated user requests, or named recurring project workflows) and show that the preset reduces routing, handoff, termination, or verification ambiguity enough to outperform an ad-hoc chain. A one-off or merely plausible future chain is not a Recipe.
3. **No ownership overlap:** no existing specialist, Recipe, or subcommand already owns the request shape. A clearer alias or domain-specific restatement is overlap, not novelty.
4. **Closed execution contract:** name the Recipe owner, each phase's specialist owner, termination bound or explicit non-loop completion condition, independent verification oracle, and residual route. The producer cannot be its sole verifier.

5. **Budgeted:** the proposal declares the four Complexity Budget fields of `_common/HARNESS_DEBT.md` §3b — `failure` · `effect` · `owner` · `removal`. A blank or generic `removal` ("when no longer needed", "on ecosystem review") fails this condition: a Recipe with no removal condition is permanent by default, and the registry's cost is paid by every future routing decision that has to step past it.

Record the evidence and `PASS`/`FAIL` result for all five conditions before cross-index wiring. If any condition fails, reject registry admission and direct-route to the owning specialist or use an ad-hoc minimum viable chain. Nexus MUST NOT register a Recipe that a single specialist can complete end to end, and MUST NOT import that specialist's domain methodology into Nexus to manufacture cross-boundary scope.

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
| 7 | **Scale** | Agent-count range (× cycles for loops) and relative cost. Where a recipe states per-phase agent figures, the stated range **is the sum of those figures**, not an independent estimate: show the floor/ceiling arithmetic under a *Range derivation* line and keep it reconciled whenever a phase figure changes. |
| 8 | **Shared-protocol refs** | Cite the `_common/` protocol instead of re-deriving it (§6). |

The gold-standard exemplars are `reference/spec-recipe.md` and `reference/clone-recipe.md` (both carry all eight).

---

## 2. Termination-bound vocabulary (canonical)

Use **one** phrasing for the loop cap: **`loop ≤ N cycles (default N=3)`** (podium's default is 2). Do not introduce `cap 3` / `max 3` / `capped at 3 iterations` as separate **prose** phrasings for the same thing — they read as different rules. **Exempt: machine-readable config keys.** A YAML/JSON value handed to an executor (`max_loops: 3`, `max_cycles: 3`) is a machine value, not a restatement of the rule — keep the key its executor expects and state the canonical phrasing in the surrounding prose. Only prose is normalized.

Every loop states its **exit reason** from this fixed vocabulary:

| Exit reason | Meaning |
|-------------|---------|
| `ACCEPT` / `target-met` | the quality bar / quantified target was reached |
| `diminishing-returns (Δ < ε)` | marginal gain fell below threshold |
| `cap-reached` | hit `N` cycles without acceptance |
| `budget-reached` | a declared budget envelope's ceiling was hit mid-run (budget-enveloped recipes: wish/marquee, eureka) |
| `BLOCK` | a hard blocker needs escalation |
| `denied` | a required approval was refused — **no side effect landed**; return the request and the refusal reason, not a partial attempt |
| `invalid-state` | an invariant broke mid-run — return the last valid checkpoint **plus a corruption report**; never continue from the violating state |
| `cancelled` | the user or the system stopped the run — return a safe-stop confirmation: what landed, what was rolled back, what is still in flight |

The last three used to be reported as `BLOCK`, and they are not interchangeable: `denied` leaves the world
untouched, `invalid-state` leaves it *suspect*, and `cancelled` leaves it partially changed. What the caller
must do next differs in each case, so the exit reason has to say which one it was.

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

**Shorthand rule:** after one full "contract-level checkpoint; AUTORUN cannot skip" statement in a file, later gates may abbreviate to **"contract-level"** (e.g. a ratification checkpoint). The abbreviation names the *same* tier — AUTORUN can never skip any gate labeled contract-level; there is no weaker unnamed variant.

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

Every recipe emits `NEXUS_COMPLETE` with the base `## Nexus Execution Report` (`reference/output-formats.md`) **plus a named recipe report**. The name is stable and recipe-specific: **Parity** (transmute), **Fidelity** (clone), **Fusion** (fuse), **Graft** (graft), **Completeness** (migrate), **Convergence** (converge), **Before/After** (kaizen), **Fulfillment Report** (wish), **Invention Dossier** (eureka). A heavyweight recipe that emits only an unnamed `NEXUS_COMPLETE` (apex, enact) is missing element #4 — give it a named report (e.g. apex **Delivery Report**, enact **Execution Report**).

---

## 6. Shared protocols (cite, don't re-derive)

| Protocol | Owns | Recipes that must cite it |
|----------|------|---------------------------|
| `_common/DIFFERENTIAL_PARITY.md` | parity-over-faith, oracle adequacy + non-determinism gates, comparator/harness, provenance/drift | transmute, clone, fuse, graft, migrate |
| `reference/verdict-gate.md` | verdict card, Yes/No/Modify branches, flag+KPI+kill | essential, killer, trim, graft (flag clause), eureka (Phase 8 product-bet handoff) |
| `reference/research-grounding.md` | tiered sources, per-claim verification, cited Evidence Ledger | clone, fuse, graft (Phase 0.5), eureka (Phase 1.5, inverted polarity), wish/marquee (Phase 1.5 exemplar anchoring), newsroom (ledger schema + trust tiers) |
| `_common/ADVERSARIAL_REFUTATION.md` | skeptic panel, evidence-vs-novelty, polarity, exclusions | killer, trim, graft, wish, newsroom, eureka |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, single termination oracle, flatten rule | converge, kaizen, apex, summit, podium, wish, newsroom, eureka |
| `_common/FINDING_LEDGER.md` | scope freeze, fingerprint discipline, disposition vocabulary + integrity, oscillation → `FROZEN`, ledger diff, ZERO predicate, split-oracle rule, validity-gate requirement — everything an external-reviewer-to-zero loop needs. Members fill its **five declaration slots** and add nothing else | quell, burnish, whet, newsroom, `security mode=to-zero`, `optimize mode=to-zero`, and any future member — §1a there records the domains deliberately **not** made members, and warns to split a domain by axis before answering C1 |
| `_common/TRACEABILITY.md` | canonical AC/REQ IDs | spec, accord-driven recipes, attest gates |
| `reference/dialogue-protocol.md` | question craft, answer processing, Assumption Ledger, checkpoint presentation, Provenance Gate for contract-level dialogue | spec, delve, wish Crystallization, eureka Phase 1 Contradiction Crystallization (mandatory); gedanken INTERACTIVE, clone Stack Dialogue, verdict cards (D1–D4/D10–D11 only) |
| `reference/autonomy-quality-protocol.md` | intent contract, Decision Ledger, drift control, producer≠verifier, evidence-bound claims, Acceptance Provenance, **completion integrity (Q16–Q19: artifact-level Done, typed deferral, Residual Ledger, completion sweep) + persistence (Q20–Q22: frozen bar, earned `BLOCKED`, hard-core-first)** | all autonomous (non-dialogue) recipes + ad-hoc chains; recipes cite it and add only specializations (parity oracles satisfy Q3/Q10; acceptance G1–G10 subsume Q11) |
| `reference/doc-quality-protocol.md` | reader contract, universal grounding / UNKNOWN-over-fabrication, cross-doc single source of truth, summary-first readability, Doc Quality Gate (W12 = Q11 for documents) | package, charter, layer, podium, spec/delve artifacts, gedanken reports, wish (W12 as a rubric dimension), eureka Disclosure Package, any doc-authoring step; native gates (podium Verification Team, Spec Quality Gate, package Phase 5) subsume W12 and add only missing dimensions |
| `_common/PROOF_CARRYING.md` | G1-G10 proof-carrying merge | acceptance, growth-acceptance |

A recipe re-describing a primitive a `_common/` protocol already owns is drift — replace the prose with a citation + the recipe-specific specialization only.

---

## 6.5 Completion policy (inherited, not per-recipe)

Every recipe finishes what its contract covers, and finishes it at the bar it set. The rule is **inherited** from `reference/autonomy-quality-protocol.md` §0 (stance) + §7 (Q16–Q22 — artifact-level Done, typed deferral, Residual Ledger, sweep, frozen bar, earned `BLOCKED`, hard-core-first ordering) — a recipe cites it and does **not** restate it (§6's cite-don't-re-derive rule). What a recipe *does* own:

- **Its Done definition**, stated in deliverable terms in element #4's named report. Done is deliverable-type relative: a design recipe (`spec`, `layer`, `charter`, `cartograph`) is done when the design is complete — that is a Q2 non-goal, not a residual. A build recipe is done when the code runs, not when it compiles around a stub.
- **Its residual route**: where a `RES-n` goes next (`quell` routes behavior-changing findings to `bug`/`feature`/`security`; `apex` routes to a follow-on `feature`; `migrate` routes to the next tranche). A recipe that produces residuals with no named route is missing element #4.
- **Recipe-specific residue markers** beyond the Q19 default probe, when its artifact type has them (`package`'s `#TODO(agent): promote <domain>` gap note is the existing exemplar).

A recipe whose report has a free-text "Recommended follow-ups" list instead of a typed Residual Ledger is out of contract — that list is where unfinished in-scope work hides.

`_common/FINDING_LEDGER.md` is the reference implementation: its disposition vocabulary (§5) and disposition integrity (§6, the fixer never disposes) are Q17–Q18 specialized to a review loop, and other recipes should follow that shape rather than invent a parallel one. `quell` and `burnish` are its two members.

## 7. Authoring checklist

Before a recipe reference is "done": all eight §1 elements present (or `N/A` + reason) · loop phrasing matches §2 · confirm tier named per §3 · resume mechanism named per §4 · report named per §5 · every reused primitive cites its §6 protocol · **completion policy per §6.5 — the named report carries a typed Residual Ledger (never a free-text follow-up list), Done is stated in deliverable terms, every residual class has a route, and no phase reorders the hard core behind the polish (Q22)** · Failure Modes Prevented is a consolidated section, not scattered notes.

## 8. Cross-index wiring checklist (adding a NEW recipe)

A recipe is not "live" until it appears — consistently — in **every** index, not just its own reference file. Omitting one is how a recipe becomes unroutable or mis-grouped (e.g. the signal-keywords mis-filing that put loop/reproduction recipes under "Mobile Native"). Wire all seven:

1. `reference/<name>-recipe.md` — the deep contract (this file's §1-§7).
2. `reference/recipes-index.md` — one row (Recipe · Subcommand · When to Use · Chain Template · Read), **and** the subcommand added to the `SKILL.md` `### Recipe Registry` allowlist. The full table lives in the index file; SKILL.md carries only the dispatch allowlist.
3. `SKILL.md` `### Recipe Families` — add to the right family (create one only if no family fits); state the within-family distinguishing axis.
4. *(retired)* — SKILL.md no longer carries an inline Signal Keywords table; anchors live only in #6 (`reference/signal-keywords.md`).
5. `SKILL.md` `## Reference Map` — one row pointing at the new reference file.
6. `reference/signal-keywords.md` — the **canonical full** anchor row, under the **correct section header** (Core / Specialist / Loop-Migration-Reproduction / Package), with English anchors + key non-English paraphrases.
7. `reference/recipes-detail.md` — ensure the recipe's **family row** covers it (within-family axis); add a per-recipe identity/disambiguation section **only when** the axis needs more than the recipes-index row states. Not every recipe has a section here. **No chain template here** — phase contracts and chain templates live solely in `reference/<name>-recipe.md` (or `inline-recipes.md` for lightweight recipes); `recipes-detail.md` must point there, never duplicate it.

Consistency rule: the recipe's name, one-line purpose, and confirm tier must read **consistently** across #2 (`recipes-index.md`) and #6 (`signal-keywords.md`) (no drift between the index row and the keyword entries); agent count and cost figures are canonical in `<name>-recipe.md` §1 element 7 (Scale) only — index/keyword rows omit them. A `recipes-detail.md` section (#7), when present, must state the same purpose but carries no chain template to keep in sync.
