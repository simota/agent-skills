# Autonomy Quality Protocol — deliverable quality for autonomous runs

**Purpose:** The shared discipline for maximizing deliverable quality when Nexus executes **without a human in the loop** — the autonomous counterpart of `reference/dialogue-protocol.md`. Dialogue recipes elicit intent from the user; autonomous runs must **derive** intent from artifacts, **track** every decision made in the user's absence, and **prove** the deliverable against the derived contract with evidence. Quality here is not a final check — it is contracted before execution, guarded during it, and independently verified at the end.

**Read when:** any `AUTORUN`/`AUTORUN_FULL` chain at CLASSIFY (Q1–Q3), AGGREGATE (Q7–Q8), and VERIFY/DELIVER (Q9–Q15). Applies to all non-dialogue recipes (`apex`, `enact`, `converge`, `kaizen`, `feature`, `bug`, reproduction family, quality-max family, …) and to the autonomous phases of dialogue recipes (`spec`'s spawned agents, `delve`'s EXCAVATE). Cites — never re-derives — `reference/evaluator-loop-protocol.md`, `reference/handoff-validation.md`, `reference/guardrails.md`, `reference/quality-iteration.md`, `reference/recipe-contract.md` §2.

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
| Q9 | **Producer ≠ sole verifier** | The agent that produced a deliverable never solely verifies it (the Generator-Evaluator separation of `reference/evaluator-loop-protocol.md`, generalized beyond loops). VERIFY runs an independent check — a fresh spawn or a different specialist — against the intent contract. |
| Q10 | **Evidence-bound claims** | Every claim in the Verification section is tied to observed evidence: a command that was run and its output, a diff, a measurement. "Should work" / "likely passes" is forbidden vocabulary. Anything not actually exercised is labeled `UNVERIFIED` and listed under Risks — an honest gap outranks a confident guess. |
| Q11 | **Deliverable Quality Gate (heavyweight runs)** | Before DELIVER on heavyweight runs (chain ≥ 4 agents, or any Quality-Max / reproduction recipe), the deliverable is adversarially reviewed **as an artifact** against the intent contract — Judge[artifact review] + AC-coverage check (Attest posture). Findings are fixed or explicitly downgraded to Risks/Follow-ups; never silently passed. This is the autonomous analog of spec's Spec Quality Gate. |

## 5. Quality budget & completion honesty (Q12–Q14)

| # | Rule | Discipline |
|---|------|-----------|
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

## Wiring

- **All autonomous chains** (recipe or ad-hoc `classify` output): Q1–Q3 at CLASSIFY/PLAN, Q4–Q6 during EXECUTE, Q7–Q8 at AGGREGATE, Q9–Q15 at VERIFY/DELIVER. Enforced at the Workflow level — individual recipe references cite this protocol instead of re-deriving it, adding only recipe-specific specializations (e.g. reproduction recipes' parity oracles already satisfy Q3/Q10 via `_common/DIFFERENTIAL_PARITY.md`; `acceptance`'s G1–G10 subsume Q11).
- **`NEXUS_COMPLETE` / `NEXUS_COMPLETE_FULL`** (`reference/output-formats.md`): the Decision Ledger (interpretation entries first) and the per-criterion Acceptance Provenance table are part of the final report — omit each section only when genuinely empty.
- **Dialogue recipes** (`spec`, `delve`): the dialogue itself follows `reference/dialogue-protocol.md`; their spawned autonomous work (EXPAND fan-outs, EXCAVATE lenses, Quality-Gate reviews) follows this protocol. The two ledgers are siblings: ASSUME-n tracks what the *user* didn't decide; DEC-n tracks what the *run* decided alone.

This protocol governs the **hub's conduct of the run** — spawn prompts inherit only the pieces a step needs (its slice of the contract, Q10 evidence duty in the output envelope), never the whole protocol.
