# Finding Ledger — the shared machinery for external-reviewer-to-zero loops

**Purpose:** The load-bearing machinery every "fix until an external reviewer returns nothing" loop needs, stated once. A raw reviewer is stochastic and adversarial: it re-words findings, surfaces new ones after every fix, and never runs out of nits. Without a ledger, "until zero" is an infinite loop by construction — and without disposition integrity, it is a loop that terminates in one cycle by declaring everything a false positive. This file owns both fixes.

**Read when:** authoring, executing, or extending a recipe whose completion oracle is an **external evaluator's finding set** (`nexus quell`, `nexus burnish`, and any future member). Run `_common/LOOP_PRECONDITIONS.md` first — this protocol assumes that gate passed.

**Provenance:** extracted from `nexus/reference/quell-recipe.md` (code diff) and `nexus/reference/burnish-recipe.md` (rendered UI surface), which now cite it rather than restating it. Loop-cap phrasing and exit-reason vocabulary belong to `nexus/reference/recipe-contract.md` §2; the Generator-Evaluator separation belongs to `nexus/reference/evaluator-loop-protocol.md`. Both are cited here, not re-derived.

---

## 1. When this protocol applies — five conditions

A domain is finding-loop-shaped only if all five hold. Check before authoring; a domain that fails C1 is a different family and routes elsewhere.

| # | Condition | Fails → route to |
|---|-----------|------------------|
| **C1** | The external evaluator emits a **finding set** — not a score, not a metric, not a residue count against a frozen denominator | metric target → `kaizen`/`optimize` · rubric score → `converge`/`restyle` · residue vs a frozen denominator → `lattice`/`migrate` |
| **C2** | Findings carry an identity that is **stable across cycles** (§4 can fingerprint them) | no loop is possible — every cycle reports everything as new |
| **C3** | The fixes have an **invariant they must not break**, expressible as a per-cycle validity gate (§10) | the loop can reach zero on a broken artifact |
| **C4** | The finding space **converges** at the declared floor | still viable, but the member **must** declare a split oracle (§9) |
| **C5** | A dismissal can be **honestly checked** (refute polarity has something to bite on) | integrity (§6) is unenforceable — do not build the loop |

**A domain is rarely all one shape — split it by axis before answering C1.** Twice now the first answer was wrong because the domain was treated as a unit. Documents: the *claim* axis is a finding set (`newsroom`), the *craft* axis is unbounded judgment (a gate). Performance: a *metric target* is not a finding set — that is `optimize`'s single-pass job — but a set of **budget violations** across many targets is one (`optimize mode=to-zero`). The question is never "is performance finding-shaped"; it is "which axis of it is". Ask C1 per axis, and expect the answer to differ.

## 1a. When a finding loop is the wrong shape — even though C1-C5 pass

Five conditions decide whether a domain *can* be looped. One more decides whether it *should*:

**C6 — the fix must close inside the loop.** If closing a finding needs an actor the loop cannot invoke — a human signing a contract, a vendor replying, a 30-day observation window, a deploy waiting on a release train — then iterating is not what the work needs. What it needs is a **tracker**: a durable ledger, owners, due dates, and a scheduled re-check. A loop built over out-of-session closure burns cycles re-reading the same open items and reports `diminishing-returns` on work that was never stalled.

Recorded non-members, so the question is not re-litigated:

| Domain | C1-C5 | Why not a member |
|--------|-------|------------------|
| **Compliance / audit findings** (`canon[regulatory]`) | all pass — control IDs are natural identities, the control set is finite, evidence is checkable | **Fails C6.** Closing a SOC2 / PCI / HIPAA gap runs on days-to-months with human owners and external attestation; `canon[regulatory]` already produces a remediation roadmap with severity-tied timelines and continuous-audit drift flagging. That is the tracker shape, and it is the right one. An in-session loop over it would iterate over items nobody could have closed since the last cycle. |
| **Document craft** (structure, altitude, register, redundancy) | C4 fails (prose critique is unbounded, like taste), so it would need `burnish`'s split oracle and a Charter | Buildable, deliberately not built. `reference/doc-quality-protocol.md` W7-W11 already covers the axis as a **single-pass gate inside every doc-producing recipe**, and `podium` owns package polish. The *claim* axis of documents is a member (`newsroom`); the craft axis stays a gate. **What would flip this:** repeated evidence that a single W7-W11 pass leaves craft defects that only iteration finds — not a preference for symmetry with the other members. |

Symmetry is not a reason to add a member. Each one costs a subcommand, a routing anchor, and a permanent disambiguation burden on its neighbors.

## 2. The five declaration slots

A member recipe declares exactly these and inherits everything else. Anything a member states beyond its slots is either a genuine specialization or drift.

| Slot | `quell` | `burnish` | `whet` | `newsroom` |
|------|---------|-----------|--------|------------|
| **(a) Evaluator** | `codex review` (via `Judge`) over a code diff | multimodal review engine + deterministic scanners over rendered captures | the **mutation engine**, run and classified by `Siege` | separately spawned claim auditor + skeptic panel, never the writer |
| **(b) Frozen scope unit** | the reviewed file diff | `surface × breakpoint × state` matrix + Finding Charter | mutation scope × operator set × **threshold contract** | `newsroom_charter.yaml` — article ref + **claim-tolerance contract** + load-bearing thesis |
| **(c) Identity mechanism** | **derived** — excludes line numbers | **derived** — excludes pixel coordinates, screenshot hashes, DOM indices | **derived** — excludes line/column and the engine's ordinal mutant index | **assigned** — `claim_id` carried through rewrites |
| **(d) Validity gate** | Green Gate (tests / build / typecheck) | Appearance Gate (render / a11y / behavior / `SPILL`) | Suite-Integrity Gate (green · no flake · runtime budget · coverage) | Thesis-Integrity gate |
| **(e) Invariant + profiles** | behavior · `general` · `refactor` | identity-preserving always · `general` · `faithful` | tests assert behavior, not implementation · no profiles | the article still makes its point · no profiles |

**The floor need not be a scalar severity.** It is whatever partitions the finding set into blocking and non-blocking. `quell`/`burnish` use a severity level; `newsroom` uses a claim-tolerance contract keyed to `risk_tier`; `whet` uses a **per-partition threshold contract** (some modules must kill every mutant, others need only a score). All three are the same slot.

**"External" means external to the producer, not to the vendor.** The load-bearing property is maker ≠ checker (`_common/LOOP_PRECONDITIONS.md` #3). A different *engine* (quell, burnish) buys it most strongly — an independent model cannot inherit the fixer's blind spots — but a separately spawned adjudicator plus adversarial refutation (newsroom) also satisfies it. What is never acceptable is the producing agent evaluating its own output.

## 3. Scope freeze

The scope is frozen at BASELINE and **never widened by the loop**. A fix that requires touching outside it becomes `DEFERRED`, never a silent expansion. Widening is a new run, not a cycle.

Members whose finding space does not converge on its own (C4) additionally freeze a **charter** — the finding classes and scored axes admitted this run — so that a class invented after seeing the artifact cannot consume a fix cycle. `burnish` §3 is the reference implementation; `quell` does not need one because a code reviewer's classes are already bounded by the diff.

## 4. Identity across cycles

A finding must keep the same identity from the cycle that opens it to the cycle that closes it. **Two mechanisms are legitimate; a member declares which one it uses in slot (c).**

**Derived (fingerprint)** — when a stateless evaluator re-emits the whole finding set each cycle and nothing carries an ID:

`fingerprint = sha1(<stable locators> ⊕ <finding class> ⊕ <normalized message>)`

**The rule that matters is the exclusion.** Every locator that *moves when a fix lands* is excluded: line numbers, pixel coordinates, screenshot hashes, DOM indices, byte offsets. A ledger keyed on a volatile locator reports the same finding as new forever, and the loop can never close anything.

**Assigned (carried ID)** — when the fix **rewrites the artifact** and the evaluator re-derives its findings from the rewritten text, no locator survives and no message normalization is reliable. Then the ID is assigned at first evaluation and the **fixer states which ID it acted on**, so the re-evaluation re-attaches the verdict history instead of re-discovering the item as new. `newsroom`'s `claim_id` is the reference case: remediation legitimately rewrites the sentence a claim lives in, so a derived key would lose the claim on the first fix.

**Choosing:** if a fix moves a finding, derive and exclude the mover. If a fix *replaces the thing the finding is about*, assign. Getting this wrong is silent — it looks like a loop that keeps finding new work.

**Per-finding record:** `id · location · class · severity · engine(s) + concurrence · first_seen_cycle · disposition · disposition_evidence · closed_in_cycle`. Members extend the record with domain fields (`burnish` adds `locus` and `expected/observed`); they never drop one.

## 5. Disposition vocabulary

Every finding carries **exactly one** disposition. Nothing is silently dropped.

| Disposition | Meaning | Counts toward ZERO? |
|-------------|---------|---------------------|
| `OPEN` | actionable, not yet fixed | **blocks** (if severity ≥ floor) |
| `FIXED-VERIFIED` | fix landed **and** the finding is absent from a subsequent evaluation of the same frozen scope | closed |
| `FALSE-POSITIVE-RATIFIED` | independently checked against the artifact and refuted | closed |
| `WONTFIX-RATIFIED` | real but deliberately not fixed; justification recorded | closed |
| `DEFERRED` | real, fix is outside the frozen scope | closed **for this run**, reported as residual + follow-up |
| `BELOW-FLOOR` | severity < the declared floor | recorded, does not block |
| `FROZEN` | oscillating (§7) — excluded from further fix cycles, escalated | does not block; reported as a `BLOCK`-class residual |

**Extension rule:** a member may add a disposition only when its domain has a genuinely distinct *closure reason*, and must state whether it blocks. Existing extensions: `DEFERRED (behavior-changing)` (`quell profile=refactor`), `DEFERRED (identity-changing)` and `OUT-OF-CHARTER` (`burnish`), `EQUIVALENT-RATIFIED` and `CLOSED-BY-REMOVAL` (`whet` — a mutant no test can distinguish, and one whose host code was deleted as genuinely dead; neither counts as a kill), `DOWNGRADED` and `DELETED (logged)` (`newsroom` — a claim closed by weakening it to labeled opinion or by removing it, both logged and re-audited, never silent), `RISK-ACCEPTED (owner, expiry)` (`security mode=to-zero` — invalid without both, and re-opens when the expiry lapses), `DEFERRED (infrastructure)` (`optimize mode=to-zero` — the fix is scale or platform work that cannot close in-session, per §1a C6). A member may **not** redefine a disposition above.

**Domain vocabularies map onto this table; they do not replace it.** A member whose evaluator emits its own verdict names (`newsroom`'s `grounded` / `miscited` / `unsupported` / `contradicted` / `stale` / `mislabeled`) states the mapping in its own contract. Verdict and disposition are different levels: a verdict is *what the evaluation found*, a disposition is *why the item is closed*.

## 6. Disposition integrity — the rules that keep zero honest

The cheapest path to zero is to dismiss everything. Four rules make that impossible:

1. **The fixer never disposes.** An agent that produced a fix in cycle N cannot set `FALSE-POSITIVE-RATIFIED`, `WONTFIX-RATIFIED`, or any member-added dismissal for any finding in cycle N. Dispositions are set by an independent adjudicator (`Magi` on dispute) — the Generator-Evaluator separation of `nexus/reference/evaluator-loop-protocol.md`, applied to triage rather than scoring.
2. **Refute-polarity dismissal.** To mark a finding `FALSE-POSITIVE-RATIFIED`, the adjudicator must attempt to **confirm** it against the actual artifact and fail, recording the evidence (`_common/ADVERSARIAL_REFUTATION.md` polarity rule). A `NEEDS-INFO` verdict stays `OPEN`.
3. **`WONTFIX` is a written argument, not a shrug.** It records why the current behavior is intended, what invariant makes the finding inapplicable, and the blast radius of fixing it anyway. `WONTFIX` on a CRITICAL/HIGH finding is **Ask First**, never auto-ratified.
4. **`FIXED-VERIFIED` is never self-declared.** It requires the finding's *absence* from a fresh evaluation of the same frozen scope. A fix with no confirming re-evaluation is `OPEN`.

**The self-dismissal analogue.** Every domain has a second cheap exit that looks like work: editing the test that would have failed (`quell profile=refactor`'s `TEST-EDITED`), "improving on" the reference instead of matching it (`burnish profile=faithful`'s `REFERENCE-DRIFT`), killing a mutant by asserting on the mutated expression itself (`whet`'s `TAUTOLOGICAL-KILL`), weakening a claim into vacuity or deleting the inconvenient paragraph (`newsroom`'s `DOWNGRADED` / `DELETED (logged)`), accepting every risk without an owner (`security mode=to-zero`'s `RISK-ACCEPTED`), **raising the budget the run is measured against** (`optimize mode=to-zero`'s `BUDGET-RAISED`). All of them are the same move — *close the finding by shifting the standard rather than meeting it* — so a member whose domain has one **must name it as a blocking class only the adjudicator can ratify**. It is rule 1 applied to the artifact instead of to the ledger.

**Watch for the arithmetically-rewarded variant.** In most domains a dishonest dismissal merely removes a blocker. In some it *improves the reported number*: `whet`'s corrected mutation score is `Killed / (Total − Equivalent)`, so declaring a survivor equivalent raises the score with no test written. Where a dismissal moves the denominator, the member must report the dismissal count alongside the metric, so a number that rose by shrinking its base is visible rather than flattering.

## 7. Oscillation → `FROZEN`

A fingerprint that returns to `OPEN` after having been `FIXED-VERIFIED` is `re-emerged`. First re-emergence → one more fix attempt with the prior fix diff attached as context. Second re-emergence → `FROZEN` + `BLOCK` escalation showing both attempts. This is what stops "fix A opens B, fix B re-opens A" from consuming the cycle budget.

## 8. Ledger diff — the progress signal

Each cycle emits `closed / persisting / net-new / re-emerged`. This diff, not the raw finding count, is the input to the diminishing-returns bound: a cycle that closes 3 and opens 3 has made no progress. Members with a split oracle (§9) pair the diff with their soft-half delta.

## 9. The ZERO predicate — and the split-oracle rule

**Base form:** `ZERO` ⟺ no record is `OPEN` at severity ≥ floor **∧** the validity gate (§10) is green **∧** the last evaluation output is attached verbatim as evidence. A ZERO claimed without an attached final evaluation is `UNVERIFIED` (`nexus/reference/autonomy-quality-protocol.md` Q10).

**When C4 fails** — the domain generates findings without bound because part of its finding space is judgment rather than defect — the member **must** split the space and give each half the oracle it can satisfy:

- **hard half** (machine-checkable, has a right answer) → `open(≥floor) == 0`
- **soft half** (judgment, no ground truth) → every declared axis `≥ 2` on the 0-3 scale of `nexus/reference/evaluator-loop-protocol.md` — **the existing scale, never a new one**

Reaching for literal zero on a soft half is not rigour; it is a loop that cannot terminate. `burnish` §2 is the reference implementation.

## 10. Validity gate — the anti-"zero findings on a broken artifact" rule

Every member runs a per-cycle gate proving the artifact is still valid under its C3 invariant. **A red gate injects a synthetic blocking finding into the ledger**, which the next cycle fixes first — it never merely warns. Members declare the gate's contents in slot (d).

## 11. Bounds, confirm posture, resume

- **Bounds are contract-level; AUTORUN cannot waive them.** Cap phrasing and exit vocabulary come from `nexus/reference/recipe-contract.md` §2 (`ACCEPT` · `diminishing-returns (Δ < ε)` · `cap-reached` · `budget-reached` · `BLOCK`). Every non-`ACCEPT` exit ships best-so-far with the residual gap named and a `resume` command.
- **"Never stops" means no confirmation pauses, not no ceiling.** Members front-load their blast radius into a **single launch-time acknowledgement** at BASELINE rather than letting Ask First fire per cycle; approving it approves the loop, not one cycle. A *new* Ask First trigger the acknowledgement did not cover still stops the run.
- **The ledger file is the loop's state.** Persist ledger + frozen scope + per-cycle diff at every gate boundary, so `resume` restarts mid-convergence with dispositions and trajectory intact. This satisfies `_common/LOOP_PRECONDITIONS.md` #4 — conversation context does not.

## 12. Failure modes this protocol prevents

| Failure | Mitigation |
|---------|-----------|
| **Unreachable zero** (the reviewer always finds something new) | Ledger + dispositions (§5): ZERO is "no `OPEN` ≥ floor", not "the reviewer said nothing" |
| **Non-terminating soft half** (taste generates findings forever) | Split-oracle rule (§9): the soft half targets `≥ 2`, never zero |
| **Dishonest zero** (everything dismissed) | Disposition integrity (§6): fixer ≠ adjudicator, refute polarity, `WONTFIX` on CRITICAL/HIGH is Ask First |
| **The self-dismissal analogue** (editing the test / drifting from the reference to make the gate green) | §6's closing rule — a blocking class only the adjudicator can ratify |
| **Phantom progress** (fix declared done, never re-evaluated) | `FIXED-VERIFIED` requires absence from a fresh evaluation (§6.4) |
| **Every finding reported as new after a trivial edit** | Derived identity excludes volatile locators; a domain whose fixes *rewrite* the artifact uses assigned identity instead (§4) |
| **Oscillation** (fix A re-opens B) | Re-emergence → `FROZEN` + `BLOCK` on the second recurrence (§7) |
| **Infinite churn with no net gain** | Diminishing-returns computed on the ledger diff, not on cycles attempted (§8) |
| **Zero findings on a broken artifact** | Validity gate injects a blocking finding rather than warning (§10) |
| **Scope creep** (fixes wander outside the reviewed scope) | Scope frozen at BASELINE; out-of-scope fixes become `DEFERRED` (§3) |
| **Charter creep** (new finding classes invented mid-run) | Charter frozen alongside scope for C4-failing domains (§3) |
| **Confirmation storm** (Ask First fires every cycle) | Blast radius front-loaded into one launch-time acknowledgement (§11) |
| **Unbounded spend under "don't stop"** | §11: bounds are contract-level; "don't stop" is about pauses, never ceilings |

## 13. Member registry

| Member | Object | Identity | Split oracle | Contract |
|--------|--------|----------|--------------|----------|
| `nexus quell` | code diff | derived | no (C4 holds at `floor=medium`) | `nexus/reference/quell-recipe.md` |
| `nexus burnish` | rendered UI surface | derived | **yes** (hard → 0, soft → `≥ 2`) | `nexus/reference/burnish-recipe.md` |
| `nexus whet` | a mutation engine's surviving mutants | derived | no (C4 holds — the mutant set is finite and each has a right answer; the floor is a per-partition threshold contract) | `nexus/reference/whet-recipe.md` |
| `nexus newsroom` | an article's factual claims | **assigned** (`claim_id`) | no (C4 holds — the claim set is the article's own assertions, and each has a right answer) | `nexus/reference/newsroom-recipe.md` |

**Mode members** — an existing recipe's single-pass phases wrapped in a sweep, rather than a new recipe. Reach for this shape when the domain already owns its triage and verification discipline and duplicating it would be the defect:

| Mode | Object | Floor | Contract |
|------|--------|-------|----------|
| `security mode=to-zero` | a scanner's findings over a repo | CVSS level | `nexus/reference/routing-matrix.md` § SECURITY |
| `optimize mode=to-zero` | budget violations across a target set | the budget itself, per target | `nexus/reference/optimize-recipe.md` §3a |

`newsroom` was authored independently and **arrived at this machinery on its own** — an audit table where no claim may be absent, citation-support-over-citation-existence as refute polarity, producer ≠ verifier, and a `BLOCK` exit for an article corrected into meaninglessness. It joined the registry by declaring its slots, not by being rewritten. Two of this file's rules exist because registering it surfaced them: the assigned-identity mechanism (§4) and the "external means external to the producer" clarification (§2).

`whet` contributed the two rules about metrics: the floor may be a per-partition contract rather than a scalar (§2), and a dismissal that moves a metric's denominator must be reported alongside the metric (§6).

**Non-members are recorded in §1a**, not left as open questions — compliance findings (fails C6) and document craft (a deliberate single-pass gate).

A new member fills §2's five slots, declares its identity mechanism and whether C4 holds, passes C6, and adds nothing else that this file already owns.
