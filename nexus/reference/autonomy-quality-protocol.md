# Autonomy Quality Protocol — deliverable quality for autonomous runs

**Purpose:** The shared discipline for maximizing deliverable quality when Nexus executes **without a human in the loop** — the autonomous counterpart of `reference/dialogue-protocol.md`. Dialogue recipes elicit intent from the user; autonomous runs must **derive** intent from artifacts, **track** every decision made in the user's absence, **prove** the deliverable against the derived contract with evidence, and **finish** it — every criterion the contract claims is carried to done or accounted for as a typed residual. Quality here is not a final check — it is contracted before execution, guarded during it, and independently verified at the end.

**Read when:** any `AUTORUN`/`AUTORUN_FULL` chain at CLASSIFY (Q1–Q3), AGGREGATE (Q7–Q8), and VERIFY/DELIVER (Q9–Q19). Applies to all non-dialogue recipes (`apex`, `enact`, `converge`, `kaizen`, `feature`, `bug`, reproduction family, quality-max family, …) and to the autonomous phases of dialogue recipes (`spec`'s spawned agents, `delve`'s EXCAVATE). Cites — never re-derives — `reference/evaluator-loop-protocol.md`, `reference/handoff-validation.md`, `reference/guardrails.md`, `reference/quality-iteration.md`, `reference/recipe-contract.md` §2.

---

## 1. Intent Contract (Q1–Q3) — quality is defined before execution

| # | Rule | Discipline |
|---|------|-----------|
| Q1 | **No execution without a contract** | Before EXECUTE, crystallize the intent into: goal (1–3 lines) · acceptance criteria (machine-checkable where possible) · **non-goals**. Sources in priority order: a locked spec's L3 ACs → the user's explicit words → derivation from request + repo state. A derived (not user-stated) criterion is itself a `DEC-n` entry (§2). If the request is too vague to derive testable criteria, ask ONE focused question (`reference/intent-clarification.md`) — a wrong contract executed flawlessly is the most expensive failure an autonomous run can produce. |
| Q2 | **Non-goals are load-bearing** | State what the run will NOT do. Scope creep is the autonomous analog of dialogue circling: without explicit non-goals, every "while I'm here" improvement dilutes the chain and multiplies unreviewed decisions. |
| Q3 | **The contract is the single termination oracle** | VERIFY checks against the intent contract — never against "looks done" or the generator's own summary. One oracle per run (`reference/evaluator-loop-protocol.md` — Sprint Contract discipline, applied even outside loops). |

## 2. Decision Ledger (Q4–Q6) — the autonomous Assumption Ledger

Every **load-bearing decision made without the user** — library/API/design picks, trade-off calls, and especially **interpretation decisions** (an ambiguity in the request resolved by choice) — is recorded:

```
| ID | Decision | Alternatives rejected | Why | Reversibility | Class |
|----|----------|----------------------|-----|---------------|-------|
| DEC-1 | retry via exponential backoff | fixed-interval | matches repo's tempo patterns | low-cost | design |
| DEC-2 | "notifications" read as in-app only | +email | request silent; email needs infra | medium | interpretation |
```

| # | Rule | Discipline |
|---|------|-----------|
| Q4 | **Record, don't remember** | `DEC-n` entries are written when the decision is made (chains ≥ 4 steps persist them with the checkpoint state), not reconstructed at DELIVER. Ask First tiers are unchanged — the Ledger covers decisions *below* the confirmation threshold; it never substitutes for a required confirmation. |
| Q5 | **Interpretation decisions are flagged** | `class: interpretation` entries are the ones the user is most likely to have wanted differently — they lead the Ledger in the final report and get first claim on any confirmation opportunity. |
| Q6 | **Irreversible + uncertain → escalate** | A decision that is hard to reverse AND low-confidence is not a Ledger entry — it is a pause point (guardrail L3 posture / `pending_confirmations`). The Ledger is for judgment calls, not for gambling with irreversibility. |

## 3. Drift control (Q7–Q8) — quality guarded mid-run

| # | Rule | Discipline |
|---|------|-----------|
| Q7 | **Goal-alignment check at AGGREGATE** | On top of schema/confidence validation (`reference/handoff-validation.md`), each step output is checked semantically: *does this still serve the intent contract?* Valid-schema-wrong-meaning is the failure that amplifies downstream — catch it at the boundary, not at VERIFY. |
| Q8 | **Re-ground long chains** | Chains ≥ 4 steps re-read the intent contract (goal + non-goals) at each checkpoint boundary before dispatching the next step. Long-chain goal dilution is gradual and invisible from inside any single step; re-grounding is the cheap antidote. |

## 4. Independent verification (Q9–Q11) — self-review is not review

| # | Rule | Discipline |
|---|------|-----------|
| Q9 | **Producer ≠ sole verifier** | The agent that produced a deliverable never solely verifies it (the Generator-Evaluator separation of `reference/evaluator-loop-protocol.md`, generalized beyond loops). VERIFY runs an independent check — a fresh spawn or a different specialist — against the intent contract. **Not in tension with `OPUS_5_AUTHORING.md` P9:** P9 removes *prompt-level self-check instructions* from a producer's own prompt (Opus 5 already self-verifies, so "double-check your work" only buys over-verification). Q9 is a *chain-level* control implemented by a different agent. Delete the wording, keep the step. |
| Q10 | **Evidence-bound claims** | Every claim in the Verification section is tied to observed evidence: a command that was run and its output, a diff, a measurement. "Should work" / "likely passes" is forbidden vocabulary. Anything not actually exercised is labeled `UNVERIFIED` and listed under Risks — an honest gap outranks a confident guess. |
| Q11 | **Deliverable Quality Gate (heavyweight runs)** | Before DELIVER on heavyweight runs (chain ≥ 4 agents, or any Quality-Max / reproduction recipe), the deliverable is adversarially reviewed **as an artifact** against the intent contract — Judge[artifact review] + AC-coverage check (Attest posture). Findings are fixed, or deferred through the Q17 gate (typed class + a `RES-n` row); never silently passed and never downgraded to an untyped "follow-up". This is the autonomous analog of spec's Spec Quality Gate. |

## 5. Quality budget & completion honesty (Q12a, Q12–Q14)

| # | Rule | Discipline |
|---|------|-----------|
| Q12a | **Spend effort where it changes the verdict, not uniformly** | Opus 5's `low`/`medium` effort are materially stronger than prior Opus generations', and **review accuracy in particular holds at low effort**. So a wide finding/coverage pass (P10's finding stage, `anneal` MAP, `acceptance` gate sweeps, `summit` team passes, verdict-recipe evidence gathering) runs at `low`/`medium`, and `xhigh` is reserved for the steps whose output *is* the judgment — adjudication, tournament scoring, ceiling convergence, the Q11 artifact review. Two consequences: (a) raising effort is **not** a lever for shorter output — effort governs thinking, not visible length (use the P2 envelope); (b) `effort` shapes the rendered prompt, so **varying it step-to-step inside one cached conversation drops the prompt cache** — vary it across spawns, not within a session that depends on cache hits. **When a single cached conversation genuinely needs different depth per step, steer per-message instead of re-setting `effort`:** appending "Please think hard before responding." / "Answer directly without deliberating." to the newest user turn moves thinking depth while leaving earlier cache breakpoints intact. That is the cache-safe form of a per-step depth nudge — an orchestrator can raise depth on planning steps and suppress it on routine confirmations without changing a single request parameter. Setting `effort` explicitly *to the model's default* is equivalent to omitting it and does **not** break the cache. Prefer the calibrated `effort` control when you are free to change it; reach for wording only inside a cache-dependent conversation, and measure — wording-based steering is sensitive to exact phrasing and can cost quality on tasks that needed the reasoning. |
| Q12 | **Bar unmet + budget remains → iterate** | A first draft below the contract's bar routes into an improvement loop (`reference/evaluator-loop-protocol.md` for contract-scored work; `reference/quality-iteration.md` PDCA for post-hoc polish) — delivering a known-substandard draft with budget left is a protocol violation, not a style choice. |
| Q13 | **Bar unmet + budget exhausted → best-so-far + residual gap** | Use the canonical exit vocabulary (`reference/recipe-contract.md` §2): report best-so-far and the precise residual gap. Never silently stop; never burn cycles past marginal value. Generalized to non-loop runs. |
| Q14 | **No status inflation** | `PARTIAL` with a precise gap beats `SUCCESS` with hidden holes. The acceptance line never says "all criteria met" as a blanket — it maps each criterion individually (§6). Downstream automation routes on status; inflated status corrupts routing *and* trust. |

## 6. Acceptance Provenance (Q15) — D16's autonomous analog

At DELIVER, classify **every intent-contract criterion**:

| Class | Meaning | Allowed? |
|-------|---------|----------|
| `verified` | met, with Q10 evidence attached | yes |
| `partial` | partly met — the gap stated precisely | yes (status ≤ PARTIAL) |
| `missed` | not met — with why + best-so-far | yes (status ≤ PARTIAL) |
| `dropped` | descoped mid-run — with the `DEC-n` that dropped it | yes, only if the DEC is in the Ledger |
| *(silent)* | a criterion the report never mentions | **no — the report is incomplete** |

A criterion that vanishes between the intent contract and the final report is the autonomous equivalent of a `silent` assumption — the report must account for all of them, and `dropped` without a Ledger entry is scope creep in reverse.

## 7. Completion Integrity (Q16–Q19) — "done" means nothing was quietly left behind

Q13's best-so-far exit and Q11's deferral branch are honest **only** when the deferral itself is disciplined. Without that discipline the Follow-ups section becomes the run's disposal chute: in-scope work reclassified as "future work", artifacts shipped with `TODO` markers and stub bodies, and a `SUCCESS` status over a skeleton. `quell` already solves this for one recipe with its disposition ledger (`reference/quell-recipe.md` §3–§4, "nothing is silently dropped"); Q16–Q19 generalize that mechanism to **every** autonomous run and every recipe.

| # | Rule | Discipline |
|---|------|-----------|
| Q16 | **The artifact is part of Done** | A deliverable is complete when the *artifact* is complete, not when the plan for it is. **Code:** every path the contract claims is implemented — no `TODO`/`FIXME`/`XXX`, no placeholder body, no `NotImplementedError` / `throw new Error("not implemented")`, no hard-coded mock standing in for the real path, no elided `// ... same for the others` presented as finished code. **Documents:** no `TBD`, no `[fill in]`, no empty heading, no section whose body is a promise to write it. Done-ness is **deliverable-type relative**: a design-only recipe (`spec`, `layer`, `charter`, `cartograph`) is done when the *design* is complete — "we didn't write the code" is a non-goal (Q2), not residue. Q16 never licenses work outside the contract: finishing ≠ widening, Q2 still binds. |
| Q17 | **Deferral is a typed decision, not a convenience** | Anything the intent contract covers may be deferred only under exactly one class below, and the class must be **true and named**. A residual with no class is a **defect**, not a follow-up: fix it, or the run's status is at most `PARTIAL` — never `SUCCESS`. |
| Q18 | **Residual Ledger — every leftover has a row, every marker has an anchor** | Each residual becomes a `RES-n` row: `id · what · class (Q17) · blocker/owner · marker location · route (recipe or agent that finishes it)`. Binding is **bidirectional**: every `#TODO(agent):` marker the run leaves in a file has a `RES-n`, and every `RES-n` living in an artifact names its marker. An orphan marker (residue no report mentions) and an orphan row (a follow-up with no anchor) are both incomplete reports. Q15's `dropped` needs a `DEC-n`; Q18's residual needs a `RES-n` — the same rule on a different axis (criteria vs work). |
| Q19 | **Completion sweep before DELIVER** | Scan the files the run actually touched for residue markers and report the result as Q10 evidence — the command, the hit count, and the `RES-n` accounting for each hit. Suggested probe: `TODO\|FIXME\|XXX\|HACK\|TBD\|not implemented\|placeholder\|<stub>`. Residue the run did **not** introduce is reported `pre-existing` and left alone (touching it is Q2 scope creep). Zero is stated as a *scanned* zero, never asserted — "there are no TODOs" without a sweep is a Q10 violation. |

**Q17 deferral classes** (the complete set):

| Class | Legitimate because | Must state |
|-------|--------------------|-----------|
| `blocked-external` | a dependency outside the run's reach — missing credential, upstream API, another team's merge | the blocker, by name |
| `gate-pending` | the work needs an **Ask First** confirmation the run cannot self-grant | which gate |
| `out-of-contract` | genuinely outside goal + ACs | the non-goal or the `DEC-n` that scoped it out |
| `budget-exhausted` | a Q13 exit | the residual gap, quantified |
| `user-declined` | the user was asked and said no | the turn where they declined |

**Not classes** — these are the phrasings that hide unfinished work, and each one means "go finish it": *for brevity · left as an exercise · can be added later · beyond the scope of this response · the pattern is the same for the rest · wire this up when convenient · similar changes needed in the other N files*.

## Failure Modes Prevented

| Failure | Mitigation |
|---------|------------|
| Flawless execution of the wrong goal | Q1 intent contract before EXECUTE, one clarifying question when underivable |
| "While I'm here" scope creep diluting the chain | Q2 explicit non-goals, Q8 re-grounding |
| Verifying against "looks done" instead of the contract | Q3 single termination oracle |
| **Judgment calls invisible to the user** (library picks, ambiguity resolutions) | Q4–Q5 Decision Ledger with flagged interpretations |
| Gambling on an irreversible low-confidence call | Q6 escalate instead of decide |
| Valid-schema-wrong-meaning outputs amplifying downstream | Q7 goal-alignment at AGGREGATE |
| Generator grading its own work | Q9 producer ≠ sole verifier |
| "Should work" reports / untested paths presented as verified | Q10 evidence-bound claims + `UNVERIFIED` labeling |
| Heavyweight deliverable shipped without artifact-level review | Q11 Deliverable Quality Gate |
| First draft delivered with budget left / cycles burned past value | Q12–Q13 quality budget rules |
| Status inflation corrupting routing and trust | Q14 + Q15 per-criterion accounting |
| Criteria silently vanishing between contract and report | Q15 Acceptance Provenance (`dropped` requires a `DEC-n`) |
| **In-scope work reclassified as "future work" to close the run** | Q17 typed deferral classes; an unclassed residual caps status at `PARTIAL` |
| Artifacts shipped with `TODO`/stub/placeholder bodies under a `SUCCESS` status | Q16 artifact-level Done + Q19 completion sweep |
| The Follow-ups section used as a disposal chute for the hard 20% | Q18 Residual Ledger — every row carries class + blocker + route |
| Residue in files the report never mentions / follow-ups with no anchor in the code | Q18 bidirectional marker binding (no orphan markers, no orphan rows) |
| "No TODOs left" claimed without looking | Q19 scanned zero as Q10 evidence |

## Wiring

- **All autonomous chains** (recipe or ad-hoc `classify` output): Q1–Q3 at CLASSIFY/PLAN, Q4–Q6 during EXECUTE, Q7–Q8 at AGGREGATE, Q9–Q19 at VERIFY/DELIVER. Enforced at the Workflow level — individual recipe references cite this protocol instead of re-deriving it, adding only recipe-specific specializations (e.g. reproduction recipes' parity oracles already satisfy Q3/Q10 via `_common/DIFFERENTIAL_PARITY.md`; `acceptance`'s G1–G10 subsume Q11).
- **`NEXUS_COMPLETE` / `NEXUS_COMPLETE_FULL`** (`reference/output-formats.md`): the Decision Ledger (interpretation entries first), the per-criterion Acceptance Provenance table, and the **Residual Ledger** (Q18, with the Q19 sweep line) are part of the final report — omit each section only when genuinely empty, and an empty Residual Ledger still reports the sweep as `scanned, 0 hits`.
- **Spawn prompts** inherit Q16–Q17 as the `Completion bound` field of the Agent Spawn Template (`reference/hub-authoring.md`): a spawned agent finishes its slice or returns `PARTIAL` with a typed residual — it never returns a stub as `SUCCESS`. The hub owns Q18–Q19; a step never self-certifies its own completion sweep (Q9).
- **Dialogue recipes** (`spec`, `delve`): the dialogue itself follows `reference/dialogue-protocol.md`; their spawned autonomous work (EXPAND fan-outs, EXCAVATE lenses, Quality-Gate reviews) follows this protocol. The two ledgers are siblings: ASSUME-n tracks what the *user* didn't decide; DEC-n tracks what the *run* decided alone.

This protocol governs the **hub's conduct of the run** — spawn prompts inherit only the pieces a step needs (its slice of the contract, Q10 evidence duty in the output envelope), never the whole protocol.
