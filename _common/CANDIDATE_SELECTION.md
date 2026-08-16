# Candidate Selection Protocol

Cross-skill discipline for **narrowing many generated candidates down to one defensible choice**. When generation is cheap, the scarce resource is not ideas — it is the reviewer attention needed to tell candidates apart and the reasoning needed to justify keeping one. This file governs that half of the work.

**Read when:** you are about to generate more than one candidate; you have a pile of variants and no stated basis for choosing; a review is drifting into preference voting; a skill's output is "here are 12 options" with no narrowing.

**Audience:** `vision`, `forge`, `pixel`, `bazaar`, `funnel`, `atelier`, `muse`, `ink`, `spark`, `riff`, `magi`, `rank`, `nexus`.

**Prerequisites:** none.
**Composes with:** `_common/parametric-output.md` (**orthogonal** — parametric output presents a *range along one axis* for a human to tune; this file *reduces a set of whole candidates* to one), `_common/EVIDENCE_LADDER.md` (how much evidence a Gate check must carry), `_common/ADVERSARIAL_REFUTATION.md` (stress-testing the surviving candidate), `_common/FINDING_LEDGER.md` (identity/disposition vocabulary when candidates persist across cycles).

---

## 1. Design the axes before the count

A candidate count is not a plan. Before generating, name the axes being varied and fix everything else.

| Axis | Varies | Example |
|------|--------|---------|
| **Semantic** | the meaning or stance the artifact takes | reassuring vs. challenging; expert-to-expert vs. guided |
| **Structural** | order, hierarchy, branching, what comes first | explain-then-act vs. act-then-explain vs. compare-first |
| **Surface** | color, type, texture, spacing, motion feel | palette, typeface, corner radius, easing |

**The failure this prevents:** models vary the Surface axis fastest and most willingly. A batch that holds Semantic and Structural fixed produces many candidates that differ only in finish — they look like exploration and function like duplication, and they converge on the highest-frequency pattern in the training distribution. If every candidate answers the same question the same way, the batch has one candidate.

**Rule:** vary one axis at a time within a batch. A candidate that moves two axes at once cannot be attributed when it wins.

### Reference discipline

Classify every reference by the *function* it serves, and state what is **not** being borrowed from it:

`principle` · `structural` · `material` · `counter-reference` (what to move away from) · `domain` · `distant analogy`

A single reference carried at full fidelity is imitation, not exploration. Always pair with at least one counter-reference. Rights consequences of reference use → `_common/ASSET_PROVENANCE.md` §5.

---

## 2. Stop conditions — declare them before generating

Four admissible stop conditions. State which one applies before the first candidate exists.

| Stop | Fires when |
|------|-----------|
| `coverage` | every declared axis has been explored at least once |
| `learning` | new candidates differ only along already-understood dimensions |
| `risk` | the verification budget for this decision is spent |
| `decision` | a candidate meets the success criteria **and** its advantage over the runner-up can be stated |

**"There might be a better one" is not a stop condition.** Neither is "the user has not reacted yet." An open-ended generation loop transfers cost from generation (cheap) to evaluation (expensive) without bounding it — this is the mechanism behind review fatigue in §7.

---

## 3. The three-stage funnel

Never rank a full batch on overall quality. Narrow in three passes, in this order.

### Stage 1 — Disqualify (no aesthetic ranking)

Remove candidates that fail a Gate (§4) or that duplicate another candidate in substance. **Assign no quality ordering at this stage.** Mixing "is it allowed" with "is it good" is what lets a strong-looking candidate carry a disqualifying defect into the final round.

### Stage 2 — Cluster into families

Group survivors by the *decision they embody*, not by appearance. Pick one representative per family; the rest are that family's surface variance and are set aside, not deleted.

Families make the real question visible: the choice is between approaches, and only afterwards between finishes.

### Stage 3 — Pairwise comparison

Compare representatives two at a time against explicit lenses:

`user goal fit` · `information hierarchy` · `brand fit` · `accessibility` · `technical feasibility` · `rights and safety` · `distinctiveness` · `reversibility` · `unknowns`

**Do not compute a total score and take the maximum.** A composite average hides exactly the trade-off the decision is about, and lets strength on a cosmetic lens outweigh weakness on a structural one.

---

## 4. Criterion classes: Gate / Trade-off / Preference

Every criterion is exactly one of these. Confusing them is the single most common defect in an evaluation rubric.

| Class | Definition | Handling |
|-------|-----------|----------|
| **Gate** | failing it disqualifies, regardless of other strengths — legal, rights, confidentiality, minimum accessibility, technical viability | apply **first**, as a boolean. Never weighted, never averaged, never offset |
| **Trade-off** | raising one lowers another — density vs. speed, distinctiveness vs. operability, precision vs. update cost | compared only among Gate survivors, and only pairwise |
| **Preference** | direction between candidates that are otherwise equivalent | resolved last, and labeled as preference in the record |

> A scoring table in which a candidate with a severe keyboard-navigation defect ranks first on visual strength is not a close call — **the table is built wrong.** The defect was a Gate and was scored as a lens.

**Applying this to an agent's own output:** when a skill scores its own candidates, Gates must be checked by something other than the generator's judgment wherever a mechanical check exists (contrast computation, token lookup, type check, link check, license field presence). A model asserting "this passes AA" is `E0` evidence — see `_common/EVIDENCE_LADDER.md`.

---

## 5. Record the comparison, not the verdict

A selection record whose content is "we chose A" is unusable later — it cannot be re-examined when conditions change, and it teaches nothing.

Record instead, per decision:

```yaml
decision: <id>
candidates: [<ids>]           # including family representatives set aside
gates_failed: {<id>: <gate>}
comparison: |                 # conditional, not absolute
  A is stronger on first-time comprehension.
  B is stronger on repeat-use scanning.
selected: A
because: single-exposure campaign; first-time comprehension dominates
reversal_condition: if this becomes a recurring surface, re-open and prefer B
unknowns: [<what was not verified>]
owner: <who decided>
```

`reversal_condition` is the field that makes the record worth keeping. A rejection without a stated condition under which it would have been accepted is not a decision — it is a preference with a timestamp.

---

## 6. Measure useful options, not option count

The productive metric is **useful options per unit of evaluation cost**:

- **Numerator** — candidates that gave the decision *new information*: tested a different hypothesis, surfaced a constraint, refuted an existing candidate, earned a place in user testing, or proved integrable with the system.
- **Denominator** — the cost of generating, organizing, comparing, and verifying the batch.

Near-duplicates raise the denominator and leave the numerator flat. **Never report candidate count as a productivity signal**; report how many candidates changed the decision.

---

## 7. Bound reviewer attention

Reviewer accuracy degrades within a single session, and the degradation is not visible to the reviewer. Bound it structurally:

- 3-5 candidates per comparison round; 1-3 lenses per round
- Apply Stage 1 disqualification *before* any human sees the batch
- Compare family representatives, never raw batches
- Re-check the anchor candidate after any break
- Where the stakes justify it, hide authorship and tool origin during comparison

Automated scoring does not remove this load — it relocates it to scoring design and exception review.

---

## 8. When not to use this

| Situation | Instead |
|-----------|---------|
| One correct answer exists (contrast ratio, spec conformance) | emit the value; there is nothing to select |
| A hard constraint fixes the outcome (brand primary, platform requirement) | emit the constraint |
| A single tunable parameter along one axis | `_common/parametric-output.md` |
| Prioritizing a backlog of unlike items | `rank` (ICE/RICE/WSJF) — that is scoring, not selection |
| Arbitrating one decision across viewpoints | `magi` |

---

## 9. Failure modes

| Mode | Symptom | Mechanism | Response |
|------|---------|-----------|----------|
| `prompt fixation` | the first output anchors everything; only wording is edited afterwards | the task, the context, and the evaluation are collapsed into one instruction | stop editing the prompt; separate intent / axes / gates and explore the opposing hypothesis in a fresh context |
| `surface-only exploration` | many candidates, one idea | Semantic and Structural axes held fixed | re-declare axes (§1) and regenerate |
| `over-generation` | nobody can hold the batch in mind; near-duplicates accumulate | cheap generation with the evaluation cost externalized to the reviewer | set batch size and stop condition **before** generating |
| `gate averaged away` | a disqualified candidate wins | Gate scored as a weighted lens | reclassify per §4 and re-run Stage 1 |
| `preference voting` | "I like B" with no stated basis | no rubric fixed before the batch was seen | write the rubric before viewing candidates |
| `automation bias` | the model's ranking is adopted without checking | fluency and speed used as a proxy for correctness | separate model critique from human critique and record where they disagree |
| `review fatigue` | later candidates get less scrutiny; the first or the loudest one wins | attention spent on volume rather than difference | §7 bounds |
| `unrecorded rejection` | the same rejected direction returns next cycle | no reversal condition captured | §5 record |
