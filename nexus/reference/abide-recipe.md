# `abide` — Change-anchored governance audit → a triaged docket of where a change set diverged from the standing decision record

**Purpose:** Full phase contract for the `abide` Recipe — take a **change set** (working tree, commit range, PR, or release window) and audit it against the repository's **standing decision record** (ADRs/RFCs, specs, published contracts, conventions), producing a triaged **Divergence Docket** covering exactly four finding classes: **VIOLATES** (the change contradicts a live decision), **SUPERSEDES-SILENTLY** (the change invalidated a live decision nobody amended), **OBSOLETE-COMPLIANCE** (the change conforms to a retired decision), and **UNGOVERNED** (an architecturally significant change no record governs and no ADR was written for). **Writes no product code and edits no record** — the deliverable is the docket at `docs/audit/abide-<slug>/`, every entry bound to both a change hunk and a rule, quoted, adjudicated for intent, severity-tiered, and routed. The **delta** member of the Comprehend family: `cartograph` maps the system across **space**, `chronicle` across **time**, `verity` audits the **standing** record against reality, `abide` audits **one change** against the record that governs it.

**Read when:** Executing the `abide` Recipe. Authored to `reference/recipe-contract.md` (all 8 elements).

---

## What `abide` is for

A team writes an ADR, agrees on it, and then — over fifty commits — walks away from it without ever saying so. Nobody lied and nobody was careless: each individual change was locally reasonable, the ADR was never in the diff, and no test encodes a decision. Six months later the record says one thing, the system does another, and the only people who could have reconciled them have forgotten which was intended. The expensive part is not the drift; it is that **the moment to catch it cheaply — while the author still remembers why — passed unnoticed.**

`abide` exists because **auditing a change against the record is a different sweep from auditing the record against the code.** `verity` freezes an artifact inventory and sweeps it in both directions at a pinned HEAD; its `since=` form narrows that inventory to *artifacts touched* in a window. But the defining case here is precisely the one that narrowing excludes: **the code changed and the ADR did not**, so the governing ADR is not in the touched set and the divergence is invisible. `abide` inverts the denominator — the **change set** is the trigger, the **standing record** (touched or not) is what it is judged against.

`judge` reviews a diff for bugs and quality; `guardian` shapes commits and PRs; `attest` proves an implementation conforms to *one given spec*; `pdm` reconciles shipped scope against a plan; `atlas` **authors** ADRs. None of them asks the governance question: *for this change, which decisions govern it, does it hold to them, and where it does not — was that intended, and was the record updated to say so?*

**Report-only by contract.** `abide` reads the repo and writes only under `docs/audit/`. It never edits an ADR — **and this is not a stylistic choice**: decision records are append-only by construction, so "fixing" one by editing it destroys the very history the record exists to hold. The correct closure for a `SUPERSEDES-SILENTLY` finding is a *new, superseding* record, and that authoring is `atlas`'s job via the route, not this recipe's.

### Default Mode: `AUTORUN` (announce-and-proceed)

The change set is largely self-resolving (a diff, a PR, a range), so `abide` announces its two denominators and proceeds — unlike `verity`, whose unbounded "check everything" earns a contract-level scope gate. **Confirm before launch when** the change set exceeds **200 changed files**, `since=` spans **≥ 2 releases**, or the governance corpus exceeds **150 records** — each of these turns a merge-time check into a repo audit, and at that size the user should be choosing `verity` or a narrower window deliberately. There is **no destructive-action gate** (read-only; writes confined to `docs/audit/`) — same posture as `cartograph`/`chronicle`/`verity`.

The one *optional* human touchpoint is the Mode-conditional **author-ratification** checkpoint in ADJUDICATE (`GUIDED`/`INTERACTIVE` only). It is worth far more here than the equivalent in `verity`: the author of the change is, by construction, *recent*, and one line from them collapses the `VIOLATES` / `SUPERSEDES-SILENTLY` fork that no amount of artifact reading can settle.

---

## The four finding classes

The charter is **frozen at ANCHOR** and is exactly these four. A candidate that fits none is `OUT-OF-CHARTER` — a bug, a style preference, or a missing test are all real findings and all belong to `bug`/`judge`/`radar`, not here.

| Class | The finding is | Minimum evidence |
|-------|----------------|------------------|
| **VIOLATES** | the change contradicts a rule from a live (`ACCEPTED`) record | the hunk + the rule quoted verbatim + why they are incompatible |
| **SUPERSEDES-SILENTLY** | the change is deliberate and defensible but invalidates a live rule that was never amended or superseded | the hunk + the invalidated rule + the intent evidence that makes it deliberate |
| **OBSOLETE-COMPLIANCE** | the change conforms to a rule whose record is `SUPERSEDED`/`DEPRECATED` — a retired decision still being obeyed | the hunk + the retired record + the record that replaced it |
| **UNGOVERNED** | the change makes an architecturally significant decision that no record governs and none was written for | the hunk + its significance trigger + the **Governance Search Record** |

**`VIOLATES` and `SUPERSEDES-SILENTLY` are the same observation under two different intents**, and separating them is this recipe's central adjudication (§ Intent adjudication). Filing a genuine regression as "the ADR needs updating" converts a bug into a paperwork task — the mirror of `verity`'s "the code is always right" fallacy, and worse here, because the author is still reachable.

**An `UNGOVERNED` finding is a claim about the record's silence, so it must prove the silence.** Every entry carries a **Governance Search Record** — the sources searched and their misses: the ADR/RFC directory · specs and AC · published contracts · conventions files (`CLAUDE.md`/`AGENTS.md`/`CONTRIBUTING`) · lint/CI policy · the change's own commit message and PR body · linked issues — each marked `searched: miss` or `not-available: <reason>`. An entry without a complete search record is **inadmissible**: "I did not look" and "nobody decided this" are indistinguishable in the output, and only one is a finding. This is `verity`'s Provenance Search Record specialized to governance sources; the discipline is cited, not re-derived.

### Architectural significance (what makes a change owe a record)

`UNGOVERNED` needs a stated trigger, or it degenerates into "every diff should have had an ADR". A hunk is **significant** when it does any of: adds/removes a dependency · crosses or moves a module boundary · changes a published contract (API, schema, event, CLI, config surface) · changes the data model or its persistence · touches a security or privacy control · introduces a new external call or integration · changes a cross-cutting convention (error handling, auth, logging, concurrency model) · sets or moves a consequential constant/budget/threshold. Anything else is `not-significant` and exits before the expensive phases. The trigger list is stated in the anchor sheet and may be project-extended there.

---

## Scope resolution

- **`abide`** — the working tree plus commits ahead of the tracked upstream. The "before I push" form, and the default.
- **`abide <base>..<head>`** / **`abide PR#`** — an explicit range or pull request.
- **`abide since=<tag|date|sha>`** — a release window: "what did this cycle walk away from". The pre-release form.
- **`abide corpus=adr|record|all`** — the governance denominator. `adr` = the ADR/RFC directory only (cheapest, the merge-gate form); `record` (default) = ADR/RFC + specs/AC + published contracts + conventions files; `all` = + prose architecture docs and comments-of-record.
- **`abide classes=<set>`** — narrow the charter (e.g. `classes=violates,ungoverned` for a merge gate; `classes=obsolete-compliance` after a decision reversal).
- **`abide floor=S1|S2|S3|S4`** — severity floor for the README's reported set (default `S3`). Below-floor findings still enter `docket.yaml`, never dropped.
- **`abide depth=scout|standard|deep`** — `scout` = significant hunks only against `ACCEPTED` records; `standard` (default) = all four classes over the resolved corpus; `deep` = + every record status, comments-of-record, and per-finding second-engine grounding.
- **`abide resume`** — re-enter from the last checkpoint.

**File layout:** `docs/audit/abide-<slug>/` — `README.md` (summary-first) · `findings/violates.md` · `findings/superseded.md` · `findings/obsolete.md` · `findings/ungoverned.md` · `docket.yaml` (machine-readable ledger; the artifact a follow-on recipe consumes) · `rejected.md` (refuted-candidate annex). A narrowed `classes=` set ships only its class files.

---

## Intent adjudication — the `VIOLATES` / `SUPERSEDES-SILENTLY` fork

Both classes describe the same physical fact: the change and a live rule cannot both be right. Which one it is depends on **what the author meant**, and that is read off evidence in a fixed order, never off plausibility:

| Evidence | Verdict |
|----------|---------|
| the change's own message/PR body states the decision is being changed | `SUPERSEDES-SILENTLY` — the intent is on record, the *decision record* is not |
| a linked issue or spec authorizes the new behavior | `SUPERSEDES-SILENTLY`, and the authorizing artifact is named in the docket |
| the change's message describes an unrelated goal (a fix, a refactor, a bump) and the divergence is incidental | `VIOLATES` — a side effect, not a decision |
| the rule encodes a security, privacy, or compliance control | `VIOLATES` regardless of stated intent — controls are not silently supersedable; the finding routes to `security` and any reversal needs explicit ratification |
| nothing settles it | **`UNDECIDED`** — routes to an author question |

**`UNDECIDED` is a first-class outcome, never a placeholder for "assume it was deliberate."** Defaulting toward deliberate is what makes a governance audit useless: it launders every regression into an ADR chore. Under headless `AUTORUN` the `UNDECIDED` set ships as the docket's author-question list; it is **never fabricated into a verdict**.

Where a rule and a change conflict but which side *governs* is itself contested (a spec versus a published contract, a convention versus an ADR), authority resolves per `reference/verity-recipe.md` § Authority — cited, not restated, with one specialization: **a record's `status` outranks its recency.** A newer `PROPOSED` ADR does not govern; an older `ACCEPTED` one does.

---

## Phase contract

`ANCHOR → INDEX → BIND → CONFORM → ADJUDICATE → DOCKET → GATE`

Judgment/comprehension throughout — **Claude-owned** (Trail/Guardian/Atlas/Grove/Lens/Attest/Gateway/Schema/Sentinel/Judge/Magi/Rank/Omen/Scribe). No code-gen phase, so no Codex routing for *production*; GATE **may** route to a second engine for prior-diversity on a high-stakes docket — verification is not code generation. **BIND is the distinctive core**: it is a bipartite join of change hunks against governing rules, run in *both* directions, and the reverse direction (hunks with no rule) is the only source of the `UNGOVERNED` class. A one-directional BIND reads as a complete audit while missing an entire class.

### Phase 1 — ANCHOR (freeze both denominators)
Two frozen sets, not one — this is what separates `abide` from every neighbor. Engines: `Trail`[resolve the range, commits, authors, messages], `+Guardian`?[PR body, linked issues, review discussion when a PR is the anchor]. Produce the **anchor sheet**:
- the **change set**: resolved `base` and `head` SHAs + read timestamp, the changed-file/hunk list, per-hunk **significance** verdict against the § Architectural significance trigger list (project extensions stated here);
- the **governance corpus** at `head`: which record classes are in scope per `corpus=`, where they live, and any exclusions with a one-line reason (vendor docs, generated contracts, archived ADRs) — **explicitly independent of what the change touched**;
- the **finding charter** (which of the four classes — frozen here);
- the **severity floor**, the **depth**, and the **caps** that will bound INDEX and BIND (rules per record; candidate rules per hunk) — declared up front so the not-inspected tail is explicit from the start, never implied-complete at the end;
- **announce-and-proceed**: state the two denominators in 4-6 lines (change set size + significant-hunk count · corpus size + record-status breakdown · charter · floor · depth · caps) and continue. **Confirm before launch when** > 200 changed files, `since=` spans ≥ 2 releases, or > 150 records.
- **Draft init:** write `docs/audit/abide-<slug>/README.draft.md` (status `draft`, anchor sheet filled). See **Resume**.

### Phase 2 — INDEX (turn records into bindable rules)
A record is prose; a binding needs a **rule**. `Atlas`[read each ADR/RFC — its Decision, Consequences, and status], `Grove`?[locate the record set when the layout is unfamiliar], `+Gateway`/`Schema`?[published contracts as rules when in scope]. Per rule: `rule_id` · source record + section anchor · **status** (`ACCEPTED` · `PROPOSED` · `SUPERSEDED` · `DEPRECATED` · `REJECTED`) · **scope predicate** (the paths, modules, layers, or subjects it governs — the join key) · the assertion verbatim · authority tier. Cap: **≤ N rules per record (N=8 at `standard`)**, ranked by bindability — a rule with a checkable scope predicate outranks an aspiration.

**Superseded and deprecated records are indexed, not skipped** — they are the entire basis of `OBSOLETE-COMPLIANCE`, and dropping them is the cheap mistake that makes this class unreachable. Rules carry **assigned ids** through the run (`_common/FINDING_LEDGER.md` §4's assigned-identity mechanism): remediation rewrites the sentence a rule lives in, so a derived key would lose it. **Output: the Rule Index** + the applied cap + the record-status breakdown.

### Phase 3 — BIND (change × rule join; the cost governor)
Do **not** evaluate every hunk against every rule (O(n·m) and mostly `NOT-APPLICABLE`). Match on scope predicates. `Lens`[resolve each rule's predicate to concrete paths/symbols and each hunk to its module/layer/subject], `+Attest`?[contract-shaped rules bind to their implementing sites natively]. Two mandatory directions:
- **rules → hunks:** for each live rule whose predicate the change set intersects, collect the hunks it governs → the `VIOLATES` / `SUPERSEDES-SILENTLY` candidate surface;
- **hunks → rules:** for each **significant** hunk, collect the governing rules; a significant hunk with **zero** bindings is an `UNGOVERNED` candidate and enters Phase 5's search obligation.

Cap: **≤ K candidate rules per hunk (K=6 at `standard`)**, ranked by predicate specificity. **Output: the Binding Table** (hunk ⇄ rule pairs) + the unbound-significant-hunk list + the uncovered-rule note.

### Phase 4 — CONFORM (verdict per binding; parallel, per binding batch)
Batched hub-spoke, no shared mutable state (`_common/PARALLEL.md`). Engines by rule type: `Lens`[behavioral/structural rules], `Attest`[spec/AC conformance — its native capability], `Gateway`/`Schema`[contract rules], `Gear`/`Gear[gha]`?[tooling, CI, dependency rules], `+Sentinel`?[any rule encoding a security or privacy control — its verdicts are non-supersedable per § Intent adjudication]. Per binding, exactly one verdict:
- `ABIDES` — the change holds to the rule (coverage numerator, not a finding).
- `DIVERGES` — the change and the rule are incompatible → candidate for the `VIOLATES`/`SUPERSEDES-SILENTLY` fork, both sides quoted. **The class is not chosen here** — Phase 5 owns it.
- `OBSOLETE-COMPLIANCE` — the rule is `SUPERSEDED`/`DEPRECATED` and the change conforms to it → candidate, with the replacing record named.
- `NOT-APPLICABLE` — the predicate matched but the rule does not actually reach this hunk (recorded, closes the binding).
**Output: the verdicted Binding Table** + the candidate pool.

### Phase 5 — ADJUDICATE (producer ≠ verifier + intent + silence proof)
The noise filter and the reason this docket is worth reading. **Producer ≠ verifier**: the agent that raised a candidate never confirms it. `Judge`[re-derive each candidate from the artifacts alone — refute polarity per `_common/ADVERSARIAL_REFUTATION.md`, default-to-refuted on evidence claims], `Magi`[the intent fork per § Intent adjudication, plus authority disputes]. Per candidate:
- **Confirmation:** both sides resolve to real text at the pinned SHAs and the incompatibility is re-derivable. A candidate that cannot be re-derived is `REJECTED-REFUTED` → the `rejected.md` annex **with its refutation evidence** — never silently dropped, so the audit itself can be audited.
- **The intent fork:** every confirmed `DIVERGES` becomes `VIOLATES`, `SUPERSEDES-SILENTLY`, or `UNDECIDED` per the evidence-order table. Security/privacy-control rules are `VIOLATES` regardless of stated intent.
- **Silence proof:** every `UNGOVERNED` candidate must carry a complete **Governance Search Record**; an incomplete one is inadmissible and is withdrawn here. Unsearchable sources record `not-available: <reason>` as a **governance-integrity gap**, surfaced in the README — never silently counted as a miss.
- **Dedupe:** fingerprint candidates (`class ⊕ rule_id ⊕ normalized subject`, **excluding line numbers and other locators that move when a fix lands** — `_common/FINDING_LEDGER.md` §4); one rule broken by twelve hunks is **one finding with twelve sites**, not twelve findings.
- **Author-ratification (Mode-conditional checkpoint; not contract-level):** under `GUIDED`/`INTERACTIVE`, present the `UNDECIDED` set and the top `UNGOVERNED` entries (≤ 5-7 lines) to whoever is there. A ratified item is promoted (`UNDECIDED` → adjudicated, or `UNGOVERNED` → `EXPLAINED (author-attested)` with the rationale captured for the docket, which is then the raw material for the ADR the route asks for). Skipped under headless `AUTORUN`, **never fabricated**.
**Output: the confirmed finding set** + the rejected annex + per-finding intent verdict.

### Phase 6 — DOCKET (severity, clusters, routes)
- **Severity** = *governance blast radius* (who binds to this rule: external consumers/operators → contributors → internal-only) × *reversibility of the change* (shipped and depended-on → merged → unpushed). Tiers `S1` blocking · `S2` material · `S3` friction · `S4` cosmetic. `Rank`[score the set], `+Omen`?[downstream failure read on the S1/S2 shortlist]. A `VIOLATES` on a security control floors at `S1`.
- **Clustering:** group findings by the *decision* they trace to, not the file. Most dockets are a handful of decisions quietly abandoned; one cluster route supersedes its members' — **nine findings tracing to one abandoned ADR route to a single superseding ADR**, not nine code corrections.
- **Route** per finding and per cluster:

| Finding | Route |
|---------|-------|
| `VIOLATES`, intent incidental | `bug` — correct the code to the decision |
| `VIOLATES`, security/privacy control | `security` — and any reversal needs explicit owner ratification, never a code-side fix that stands the divergence up |
| `VIOLATES`, deliberate but the rule still holds | owner decision: revert, or an explicit exception recorded against the rule |
| `SUPERSEDES-SILENTLY` | `atlas` — author the **superseding** record and mark the original `SUPERSEDED`; **never edit the original** |
| `OBSOLETE-COMPLIANCE` | `anneal`/`refactor` — bring the code to the live decision; `+quill` for whatever still points at the retired record |
| `UNGOVERNED`, technical | `atlas` — the ADR that was owed, seeded from the author-ratification rationale where one was captured |
| `UNGOVERNED`, product/scope | `spec` — the decision belongs in a specification, not an ADR |
| `UNDECIDED` | author/owner question — first-class outcome, shipped as the docket's question list |
| cluster of `UNGOVERNED` decisions across a long window | `chronicle` → `atlas` — mine the history the per-finding search could not |

### Phase 7 — GATE (grounding + coverage; `loop ≤ 3 cycles (default N=3)`)
`Attest`/`Judge`[independent of every producing agent], `+2nd engine`?[at `depth=deep` or on a release-blocking docket]. Checks: a sampled set of findings re-resolves **verbatim at the pinned base/head SHAs** · every `UNGOVERNED` entry has a complete Governance Search Record · no `DIVERGES` was silently resolved toward "deliberate" · the **coverage statement** is present and honest — *A of B significant hunks bound-or-explicitly-ungoverned; C of D live rules evaluated; the capped tail named*. Exit reasons per `reference/recipe-contract.md` §2; on any non-`ACCEPT` exit the docket ships **best-so-far + the residual gap**.

---

## Termination bound

The GATE loop only: **`loop ≤ 3 cycles (default N=3)`**, exit vocabulary per `reference/recipe-contract.md` §2 (`ACCEPT` · `diminishing-returns (Δ < ε)` · `cap-reached` · `BLOCK` · `denied` · `invalid-state` · `cancelled`). Phases 1-6 are single-pass; the fan-outs in BIND/CONFORM are bounded by the caps declared at ANCHOR, not by a loop. `abide` is a **declared non-member** of `_common/FINDING_LEDGER.md` — it borrows assigned identity (§4) and nothing-silently-dropped (§5) as primitives, but it is a single-pass audit with no fix side and therefore no drive-to-zero oracle.

## Resume

**Checkpoint-resume** — 7 phases, so phase outputs persist at each boundary (anchor sheet → Rule Index → Binding Table → verdicted bindings → confirmed set → docket) and `abide resume` re-enters from the draft's current-phase marker. The pinned base/head SHAs make a resumed run verifiably the same audit; a resume after the head moved **restarts at ANCHOR** rather than mixing two change sets.

## Output report — the **Divergence Docket**

`NEXUS_COMPLETE` with the base `## Nexus Execution Report` (`reference/output-formats.md`) plus:
- **Anchor attestation** — base/head SHAs, read timestamp, change-set size, significant-hunk count, corpus size + record-status breakdown, charter, floor, depth, caps applied.
- **Coverage statement** — significant hunks bound-or-explicitly-ungoverned of total; live rules evaluated of total; **the capped tail named, not implied covered**.
- **Findings by class**, severity-ordered above the floor, each with both sides quoted, its intent verdict, its sites, and its route.
- **Decision clusters**, ranked, each with the cluster route that supersedes its members'.
- **Author-question list** — every `UNDECIDED` finding, phrased as a question someone can answer in one line.
- **Rejected annex** — refuted candidates with refutation evidence; `OUT-OF-CHARTER` items with their owning recipe; governance-integrity gaps.
- **Residual Ledger** — per `reference/autonomy-quality-protocol.md` Q17-Q19, typed, never a free-text follow-up list. **Done is deliverable-relative**: the audit is done when every significant hunk is bound-or-explicitly-ungoverned and every docket entry is adjudicated. **Unfixed divergences are not residuals — they are the deliverable**, and each carries its route. Genuine residuals are of exactly three kinds, each routed: a record class that could not be indexed (`BLOCK`, with the blocker), a governance-integrity gap that made intent unrecoverable (routed to an author question), and the capped tail (routed to a deeper re-run).

## Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **The untouched-ADR blind spot** (a code change violating a record that was never in the diff) | the governance corpus is frozen **independently of the change set** at ANCHOR — the inversion this recipe exists for |
| **Laundering a regression into paperwork** (an unintended violation filed as "the ADR needs updating") | § Intent adjudication's fixed evidence order; `UNDECIDED` is first-class and never defaults to deliberate; security/privacy controls are non-supersedable |
| **"Every diff should have had an ADR"** (UNGOVERNED as an opinion dump) | the § Architectural significance trigger list gates the class; non-significant hunks exit before the expensive phases |
| **"I did not look" reported as "nobody decided"** | the **Governance Search Record** is mandatory for every `UNGOVERNED` entry; ADJUDICATE withdraws incomplete ones |
| **Retired decisions still obeyed, invisibly** | `SUPERSEDED`/`DEPRECATED` records are indexed rather than skipped — the sole basis of `OBSOLETE-COMPLIANCE` |
| **A newer proposal treated as governing** | status outranks recency; `PROPOSED` and `REJECTED` records never bind |
| **One-directional BIND** (rules→hunks alone can never find UNGOVERNED) | both join directions are mandatory and asymmetric; the coverage statement reports each denominator separately |
| **Editing the ADR to make the finding go away** | report-only contract; `SUPERSEDES-SILENTLY` routes to a *new superseding record* via `atlas`, never to an edit of the original |
| **Twelve findings for one broken rule** | fingerprint dedupe on `class ⊕ rule_id ⊕ subject`, excluding volatile locators — one finding, twelve sites |
| **Silently dropped candidates** | `rejected.md` annex with refutation evidence; below-floor entries kept in `docket.yaml` |
| **Unbounded join cost** | scope-predicate matching instead of hunk×rule enumeration; caps on rules-per-record and rules-per-hunk declared at ANCHOR |
| **Fabricated evidence** (a rule that is not in the record, a conflict whose sides do not conflict) | GATE grounding check — verbatim resolution at the pinned SHAs, producer ≠ verifier, optional cross-engine |
| **Charter creep** (bugs, style, missing tests filed as governance findings) | the four-class charter is frozen at ANCHOR; anything else is `OUT-OF-CHARTER` with the recipe that owns it |
| **Stale-on-delivery** | the docket is grounded at pinned base/head SHAs; a resume after the head moved restarts at ANCHOR rather than mixing change sets |

## Boundaries / vs neighbors

- **vs `verity`** — the family sibling on the **delta** axis, and the closest neighbor. `verity` freezes an **artifact inventory** and sweeps the standing record against reality at a pinned HEAD; `abide` freezes a **change set** and judges it against the standing record, *including records the change never touched*. `verity since=<tag>` narrows verity's inventory to touched artifacts and therefore **cannot see the core case here** — code moved, the ADR did not. Use `verity` for "where does our record disagree with our code" (repo-wide, all record types, 7-24 agents); `abide` for "did this change walk away from a decision" (change-anchored, governance corpus, 5-16 agents, merge-time cadence). A large `abide` docket clustering into repo-wide rot is the standard escalation to `verity`.
- **vs `judge` (agent)** — judge reviews a **diff** for correctness and quality. `abide` reviews the same diff for **conformance to decisions** and files nothing about code quality. Run both on a PR; they share no findings.
- **vs `guardian` (agent)** — guardian shapes *how a change is packaged* (granularity, naming, commit strategy). `abide` audits *what the change decided*.
- **vs `attest` (agent)** — attest proves an implementation conforms to **one given spec's ACs**, with the spec as privileged authority. `abide` resolves *which* records govern a change (that binding is its own phase), spans the whole governance corpus, and adds the intent fork and the ungoverned class attest has no shape for. One spec to verify against → `attest` direct; `attest` is also an `abide` engine.
- **vs `atlas` (agent)** — atlas **authors** ADRs and RFCs. `abide` never authors one; every `SUPERSEDES-SILENTLY` and `UNGOVERNED` finding routes *to* atlas. `abide` → `atlas` is the audit→author pair.
- **vs `pdm` (agent)** — pdm answers *what is built vs what was planned* against a roadmap/PRD. `abide` has no plan and no scope question; it asks whether a change held to decisions already made.
- **vs `chronicle`** — chronicle reconstructs *how the repo got here* and infers a decision log from history. `abide` takes the decision record as given and tests one change against it. A cluster of `UNGOVERNED` findings over a long window routes `abide` → `chronicle` → `atlas`.
- **vs `acceptance`** — acceptance is a **proof-carrying merge gate** producing evidence that a change meets its ACs (G1-G10). `abide` is a governance audit producing a docket; it blocks nothing by itself. They compose: `abide` as an `acceptance` input on a Tier-S change.
- **vs `canon` (agent)** — canon audits against **external named standards** (OWASP/WCAG/OpenAPI/ISO 25010). `abide` audits against the project's **own** decisions.
- **vs `lattice`** — lattice proves design-system token conformance (visual, steady-state). `abide` audits textual governance conformance of a change.
- **vs `migrate`** — migrate *executes* a change to completeness. `abide` reports on a change already made.

**Decision tree:**
```
Want to know whether a CHANGE held to the decisions that govern it (no fixes)?
  NO  → where the standing record and the code disagree, repo-wide?  → verity
        how the system is built now (structure)?                     → cartograph
        how it got here / infer the decision log?                    → chronicle
        the diff's bugs and quality?                                 → judge direct
        commit/PR packaging?                                         → guardian direct
        conformance to ONE given spec?                               → attest direct
        built vs planned (delivery status)?                          → pdm direct
        an external named standard?                                  → canon direct
        write the ADR itself?                                        → atlas direct
  YES → one rule, one file, one question?                            → attest / lens direct
        the whole change set vs the governance record, triaged?
              → abide
                    abide                       → working tree + unpushed, "before I push"
                    abide <base>..<head> | PR#  → an explicit range or PR
                    abide since=<tag>           → what this cycle walked away from
                    abide corpus=adr            → ADR/RFC only, cheapest merge-gate form
                    abide classes=violates,ungoverned → merge-gate charter
                    abide depth=deep            → all record statuses + cross-engine grounding
                    then close                  → abide → atlas / bug / security / anneal (per route)
                    docket sprawls repo-wide    → abide → verity
                    ungoverned cluster          → abide → chronicle → atlas
```

## Scale

**5-16 agents × the GATE loop (≤ 3 cycles).** *Range derivation:* floor = ANCHOR 1 (Trail) + INDEX 1 (Atlas) + BIND 1 (Lens) + CONFORM 1 (Lens) + ADJUDICATE 1 (Judge) + DOCKET 1 (Rank) + GATE 1 (Attest) = **7**, less 2 where `depth=scout corpus=adr` merges ANCHOR into INDEX and BIND into CONFORM = **5**. Ceiling = ANCHOR 2 (Trail + Guardian) + INDEX 2 (Atlas + Grove/Gateway) + BIND 2 (Lens + Attest) + CONFORM 4 (Lens + Attest + Gateway/Schema + Sentinel) + ADJUDICATE 2 (Judge + Magi) + DOCKET 2 (Rank + Omen) + GATE 2 (Attest + a second-engine verifier) = **16**. The low end is `abide corpus=adr depth=scout` on an unpushed branch; the high end is a `since=<release>` window at `depth=deep` with contracts and security controls in the corpus.

**Cost scales with (significant hunks × bound rules) — not with diff line count or repo size.** ANCHOR and INDEX are cheap enumeration bounded by the record directory (tens of records, not the whole doc set); BIND prunes on scope predicates *before* the expensive fan-out; CONFORM and ADJUDICATE are bounded by the caps BIND already applied. A 10,000-line refactor touching one module costs less than a 200-line change crossing five governed boundaries — which is the correct incentive. The cost governors are **`corpus`** (the single biggest lever: `adr` versus `all`), **`depth`**, **`classes`** (dropping `ungoverned` removes the reverse join and the search obligation entirely), the **severity floor**, and the ANCHOR caps. **Materially cheaper than `verity` at equal repo size**, and cheap enough to run per-PR at `corpus=adr depth=scout`.

## Shared protocols & Add-ons

- **Shared:** Authority resolution when records conflict → `reference/verity-recipe.md` § Authority (cited, with the one specialization that status outranks recency). Silence-proof discipline → the same file's Provenance Search Record, specialized here to governance sources. Adversarial confirmation, refute polarity, default-to-refuted → `_common/ADVERSARIAL_REFUTATION.md` (ADJUDICATE; also the prior-diversity basis for GATE's optional cross-engine check). Assigned identity + nothing-silently-dropped → `_common/FINDING_LEDGER.md` §§4-5 **as borrowed primitives only** (declared non-member — see § Termination bound). Per-batch parallel isolation → `_common/PARALLEL.md` (hub-spoke, no shared mutable state across binding batches). Docket authoring, freshness metadata, per-file length envelope → `reference/doc-quality-protocol.md` (W1-W3, W7-W9, W12). Evidence-bound claims, producer ≠ verifier, typed residuals and the completion sweep → `reference/autonomy-quality-protocol.md` (Q9-Q11, Q15-Q19). Loop cap phrasing, confirm tiers, resume vocabulary → `reference/recipe-contract.md` §§2-4. Author-ratification checkpoint presentation → `reference/dialogue-protocol.md` (the Mode-conditional checkpoint only — `abide` is a comprehension recipe, not a dialogue recipe).
- **Add-ons:** +`Gateway`/`Schema` (published API, GraphQL, or DB-schema contracts as rules), +`Sentinel` (any rule encoding a security or privacy control — its findings are non-supersedable and route to `security`), +`Cloak` (privacy/data-governance records), +`Canon[regulatory]` (regulatory-control records, where a divergence is a compliance event rather than a design one), +`Gear`/`Gear[gha]` (dependency, tooling, and CI-policy rules), +`Guardian` (PR body, review discussion, and linked issues as intent evidence), +`Omen` (downstream failure read on the S1/S2 shortlist), +`Canvas` (a decision-cluster map when the docket is large), +`Sherpa` (decompose a `since=<release>`-scale window into independent per-module sub-runs).

## Chain template

`ANCHOR (Trail +Guardian?) → announce + draft-init → INDEX (Atlas +Grove? +Gateway/Schema?) → BIND (Lens +Attest?) [both directions] → CONFORM ∥per-binding-batch (Lens + Attest +Gateway/Schema? +Gear/Gear[gha]? +Sentinel?) → ADJUDICATE (Judge[refute-polarity] + Magi[intent fork], ✓author-ratification) → DOCKET (Rank +Omen? +Canvas?) → ⟲GATE (Attest/Judge, +2nd engine?) → promote docs/audit/abide-<slug>/ + pinned-SHA attestation` [NO CODE]

Each phase's inputs, caps, engine bindings, discipline rules, and outputs are canonical in § Phase contract; `∥` marks the parallel fan-out (per binding batch, hub-spoke per `_common/PARALLEL.md`). The `✓` marker is the **author-ratification** checkpoint (Phase 5 — Mode-conditional); the launch gate is **announce-and-proceed**, escalating to confirm-before-launch at the § Default Mode thresholds. `⟲` is the **grounding/coverage loop** (Phase 7 — `loop ≤ 3 cycles (default N=3)`). Resumable via `abide resume` from the draft's current-phase marker. Hands off per finding and cluster route (§ DOCKET) — `atlas` / `bug` / `security` / `anneal` / `refactor` / `quill` / `spec` / `chronicle` → `atlas` / `verity`.
