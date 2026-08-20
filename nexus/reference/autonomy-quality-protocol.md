# Autonomy Quality Protocol — deliverable quality for autonomous runs

**Purpose:** The shared discipline for maximizing deliverable quality when Nexus executes **without a human in the loop** — the autonomous counterpart of `reference/dialogue-protocol.md`. Dialogue recipes elicit intent from the user; autonomous runs must **derive** intent from artifacts, **track** every decision made in the user's absence, **prove** the deliverable against the derived contract with evidence, and **finish** it — every criterion the contract claims is carried to done or accounted for as a typed residual. Quality here is not a final check — it is contracted before execution, guarded during it, and independently verified at the end.

**Read when:** any `AUTORUN`/`AUTORUN_FULL` chain at CLASSIFY (Q1–Q3), AGGREGATE (Q7–Q8), and VERIFY/DELIVER (Q9–Q19); §0 and Q20–Q22 apply throughout; §8 (Q23–Q26) before every spawn and every side-effecting step. Applies to all non-dialogue recipes (`apex`, `enact`, `converge`, `kaizen`, `feature`, `bug`, reproduction family, quality-max family, …) and to the autonomous phases of dialogue recipes (`spec`'s spawned agents, `delve`'s EXCAVATE). Cites — never re-derives — `reference/evaluator-loop-protocol.md`, `reference/handoff-validation.md`, `reference/guardrails.md`, `reference/quality-iteration.md`, `reference/recipe-contract.md` §2.

---

## 0. Stance — the disposition the rules encode

Q1–Q22 are mechanical; the disposition behind them is not, and it is the part that decays first on a long autonomous run. State it once, keep it for the whole run:

> **Do not compromise the goal to make the run easier. Do not abandon a task because the part that is left is the hard part. Do not forget, at step nine of a twelve-step chain, what finishing was supposed to mean.**

Where a rule and this disposition point the same way, follow the rule; where the rules are silent — and on a real run they often are — the disposition decides. It cashes out as three concrete behaviors, specified as Q20–Q22 in §7: the bar is never quietly lowered to meet the output, an alternative is actually tried before `BLOCKED` is claimed, and the difficult core is built before the easy polish.

**What it is not.** Persistence is not stubbornness, and this section never overrides a stop rule:
- Repeating a failing approach is not perseverance — **two identical failures ⇒ stop and diagnose**, then try a *different* approach. Thrash is giving up while looking busy.
- Burning budget past marginal value is Q13's failure mode, not its virtue. Exiting at `diminishing-returns` with an honest residual gap **is** finishing.
- Grinding past an **Ask First** gate, a Q6 escalation, or an L3/L4 guardrail is not determination — it is an unreviewed gamble. The disposition raises effort, never permission.

## 1. Intent Contract (Q1–Q3) — quality is defined before execution

| # | Rule | Discipline |
|---|------|-----------|
| Q1 | **No execution without a contract** | Before EXECUTE, crystallize the intent into: goal (1–3 lines) · acceptance criteria (machine-checkable where possible) · **non-goals** · **prohibited outcomes**. Sources in priority order: a locked spec's L3 ACs → the user's explicit words → derivation from request + repo state. A derived (not user-stated) criterion is itself a `DEC-n` entry (§2). If the request is too vague to derive testable criteria, ask ONE focused question (`reference/intent-clarification.md`) — a wrong contract executed flawlessly is the most expensive failure an autonomous run can produce. |
| Q2 | **Non-goals and prohibited outcomes are load-bearing — and are not the same field** | **Non-goals** bound the *work*: what the run will NOT do. Scope creep is the autonomous analog of dialogue circling — without them, every "while I'm here" improvement dilutes the chain and multiplies unreviewed decisions. **Prohibited outcomes** bound the *consequences*: results that must not occur however the work is done ("no data loss", "no public artifact", "no schema change reaching prod", "no credential in a log"). A run can honor every non-goal, meet every acceptance criterion, and still cause a forbidden result — which is why they are verified on their own axis (§6) and never folded into the AC list. State them explicitly or declare `none`; a blank field is not a declaration. |
| Q3 | **The contract is the single termination oracle** | VERIFY checks against the intent contract — never against "looks done" or the generator's own summary. One oracle per run (`reference/evaluator-loop-protocol.md` — Sprint Contract discipline, applied even outside loops). |

**Contract Lint — run before EXECUTE, not after.** Q1 says what the contract must contain; this is the mechanical check that it does. Seven conditions, all cheap:

1. The goal is non-empty and names an outcome, not an internal action ("expired sessions cannot be reused", not "fix the auth module").
2. Every acceptance criterion has an **oracle** — a command, a file check, a rubric, or a named human reviewer. A criterion with no oracle cannot be auto-verified; either decompose it until it can be, or route it to human review explicitly.
3. Non-goals are stated (Q2), and prohibited outcomes are stated or explicitly `none`.
4. Any high-risk or irreversible step names its rollback, or declares the irreversibility explicitly.
5. Required evidence matches what VERIFY will actually check — no criterion demanding evidence the chain never produces.
6. A budget and a termination condition exist, covering **success, escalate, and abort** — not success alone.
7. In-scope paths and the chain's authorized side effects do not contradict each other.

Lint does not certify that the contract is *right* — only that it is not missing a part. It is the cheapest gate in the protocol; skipping it moves the same failures to DELIVER.

## 2. Decision Ledger (Q4–Q6) — the autonomous Assumption Ledger

Every **load-bearing decision made without the user** — library/API/design picks, trade-off calls, and especially **interpretation decisions** (an ambiguity in the request resolved by choice) — is recorded:

```
| ID | Decision | Alternatives rejected | Why | Reversibility | Class |
|----|----------|----------------------|-----|---------------|-------|
| DEC-1 | retry via exponential backoff | fixed-interval | matches repo's retry conventions | low-cost | design |
| DEC-2 | "notifications" read as in-app only | +email | request silent; email needs infra | medium | interpretation |
```

| # | Rule | Discipline |
|---|------|-----------|
| Q4 | **Record, don't remember** | `DEC-n` entries are written when the decision is made (chains ≥ 4 steps persist them with the checkpoint state), not reconstructed at DELIVER. Ask First tiers are unchanged — the Ledger covers decisions *below* the confirmation threshold; it never substitutes for a required confirmation. |
| Q5 | **Interpretation decisions are flagged** | `class: interpretation` entries are the ones the user is most likely to have wanted differently — they lead the Ledger in the final report and get first claim on any confirmation opportunity. **`class: interpretation` entries additionally carry `invalidation_impact` (what breaks if the reading was wrong) and `validate_before` (the point past which the assumption must be confirmed — typically `merge` or `deliver`).** High impact + low confidence is validated *during* the run, not reported at the end: an assumption surfaced only at DELIVER has already been built on. |
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

**Prohibited outcomes are classified on their own axis, in the same section.** Success criteria and prohibited outcomes fail differently and cannot share a verdict: an AC is met by producing something, a prohibition is held by *nothing having happened*, which no amount of AC evidence demonstrates.

| Class | Meaning | Allowed? |
|-------|---------|----------|
| `held` | checked, with Q10 evidence that the forbidden result did not occur | yes |
| `violated` | it happened — with blast radius, the rollback attempted, and residual state | status `FAILED`; escalate, never deliver over it |
| `unverified` | no evidence either way — the run had no way to observe it | yes, only as a named Risk; never reported as `held` |

A prohibited outcome may never be `dropped`: descoping work is a `DEC-n` (Q4), but descoping a *prohibition* is the user's call, not the run's. `none` declared at Q1 is a valid whole section — an empty one is an incomplete report.

## 7. Completion Integrity (Q16–Q22) — "done" means nothing was quietly left behind

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

### Persistence rules (Q20–Q22) — §0's disposition, made checkable

Q16–Q19 catch work that was left *visibly* undone. Q20–Q22 catch the quieter version: the run that reaches `SUCCESS` by making success cheaper.

| # | Rule | Discipline |
|---|------|-----------|
| Q20 | **The bar does not move to meet the output** | Acceptance criteria are frozen once the intent contract is set (Q1). Rewriting a criterion, relaxing a threshold, weakening an assertion, or narrowing a test so the run can pass is a **goalpost move**: it requires an explicit `DEC-n` (class `interpretation`), lands in Acceptance Provenance as `partial`/`dropped` — never as `verified` — and can never be made by the agent whose output failed the bar (Q9, the same fixer≠adjudicator rule `quell` §4 applies to dispositions). A criterion that quietly changed wording between CLASSIFY and DELIVER is the single hardest self-deception to catch after the fact; re-read the original at each Q8 re-grounding. |
| Q21 | **`BLOCKED` is earned, not declared** | Before a step returns `BLOCKED` — or a residual is classed `blocked-external` (Q17) — at least one *materially different* approach must have been attempted and **named in the report** ("tried X, failed because Y"). "This is difficult", "the API is unclear", "no obvious way" are not blockers; they are the point where the work starts. Bounded by §0: the alternative must be genuinely different, and after two identical failures the step diagnoses instead of retrying. A `BLOCKED` with no named attempt is a defect, and the hub routes it back rather than aggregating it. |
| Q22 | **Hard core before easy polish** | Order the work so the load-bearing, uncertain, or unpleasant part is done **first**, and the cosmetic pass last. Two payoffs: a `budget-exhausted` exit then leaves a working core rather than a polished shell around a hole, and difficulty is discovered while there is still budget to route around it. Where a plan defers the hardest step to the end without a stated reason (a genuine dependency), that ordering is itself the compromise — fix the order, not the report. |

## 8. Authority & effect discipline (Q23–Q26) — what a step may *do* is granted, not derived

Q1–Q22 govern what the run produces. Q23–Q26 govern what it is allowed to *cause*. The distinction matters because a chain widens its effect surface far more quietly than it widens its scope: the platform hands every spawned agent the hub's own tool permissions, so a step that only needed to read three files runs with the authority to write, delete, publish, and spawn.

| # | Rule | Discipline |
|---|------|-----------|
| Q23 | **Authority is granted, never inferred** | *Capability* is what the tools can do; *authority* is what this step may do with them. A step's authority comes from the hub's explicit grant — never from the breadth of its task description, never from "it would be helpful", never from what the platform happens to permit. Three corollaries: (a) the grant is the **narrowest effect set the step's acceptance criteria need**, stated in the spawn prompt's `Authority` field (`reference/hub-authoring.md`); (b) **delegation cannot widen** — a spawned agent may not exceed the grant it received, and may not re-delegate unless re-delegation was granted, so authority is traceable back to the hub at every hop; (c) a step that finds it needs a wider effect set **requests it and returns** — it does not take it. An **Ask First** trigger is unchanged by any grant: authority narrows what a step may do, it never pre-authorizes what the user must confirm. |
| Q24 | **Under unresolved uncertainty, lower the action tier — don't auto-promote** | Effects are tiered (`reference/guardrails.md` § Action Tier Ladder: answer → propose → prepare → execute-reversibly → execute-consequentially). An ambiguous or under-evidenced request is executed at a **lower** tier — deliver the candidate list, the diff, the draft, the dry-run — rather than being either blocked outright or resolved by guessing at the top tier. Promotion to a higher tier requires the uncertainty that blocked it to be *resolved* (evidence found, or the user answered), never merely re-read. This is the graceful middle the binary ask/proceed gate lacks: a run that cannot safely commit can almost always still deliver something reversible. |
| Q25 | **Agreement is not authorization** | Agents concurring is *evidence*, never permission to cause the effect. Three specialists agreeing that a refund is owed does not make the refund authorized — the amount may exceed a limit, the input may be stale, an exception may apply, the effect may already have happened. Separate the two: the chain's aggregated output is a **proposal** (what to do, to what, on what evidence, expected effect, and when the proposal goes stale); causing the effect is a distinct step that runs only when *all* of current state, an explicit policy, a bound approval, an idempotent path, and a stated recovery route are present. Any one missing caps the run at `T2 prepare` and returns the proposal. Unanimity substitutes for none of them — and same-model, same-prompt, same-context reviewers agreeing is correlated error, not independent confirmation. |
| Q26 | **Approval binds to a payload, a scope, and a clock** | An approval is not the word "yes". It attaches to *what was approved*: the proposal it covers, who approved it, what they were shown, and when it expires. Three consequences: (a) **approval does not cascade** — approving a goal does not authorize the specific irreversible actions later derived from it; the effect needs its own approval at its own tier; (b) **an approval goes stale** — if the plan changed after approval, or the world changed under it, the approval no longer describes what is about to happen and is re-obtained, not re-used; (c) **the producer never approves its own effect** for anything irreversible or outside the run's stated scope — approval and production are separate roles, and an agent's own claim that it "confirmed" something is not an approval record. |

**What the approver is shown.** An approval request that states only the action buys a click, not a decision.
Show, in this order: the **diff or concrete effect**; the **target** and what else it touches; the **evidence**
it rests on *and what is still unresolved*; the **cost, deadline, and reversibility**; the **alternatives,
including doing nothing**; and the **scope and expiry** of the approval being given. The two most often
omitted — the unresolved part and the do-nothing option — are the two that make an approval a judgment rather
than a formality.

**Approval fatigue is a failure mode, not a user problem.** A gate that fires on every low-risk action trains
the approver to clear it unread, which removes the control while leaving its appearance. When a gate fires
often and is approved nearly always, that is evidence the gate is mis-placed: batch the routine cases under a
stated policy and escalate only the deviations. Volume of approvals is not a safety metric; **approvals that
changed an outcome** is.

**Certainty is the second axis of the gate.** `Ask First` triggers on the *kind* of action. Confidence in the
classification is independent of it, and the two combine:

| | Reversible, low impact | Compensable, medium impact | Irreversible, high impact |
|---|---|---|---|
| **High certainty** | proceed; sample afterwards | proceed on-loop with a stated threshold | approval bound before the effect |
| **Medium certainty** | proceed with a full trace | return a proposal for approval | two approvers, one of them not the producer |
| **Low certainty** | ask one focused question | hand the decision to the user | **do not run the action** — resolve the uncertainty first |

The bottom-right cell is a prohibition, not a stricter gate: an unresolved classification plus an irreversible
effect is not something an approval makes safe, because the approver is being asked to ratify a guess.

**Separation of duties, where it binds.** For an irreversible effect, an effect outside the run's stated
scope, or a change to a control itself, the approver is someone other than the producer — and **an owner does
not unilaterally approve an exception to a control they own**. Self-approval of one's own exception is the
shortest path around every rule above it. Where no second party is available, the run stops at `T2 prepare`
and says so; that is a `PARTIAL` with a named blocker, not a failure.

**Grant dimensions.** "Narrowest grant" (Q23a) is unenforceable until the grant has axes; a per-tool allow/deny list is too coarse, because the *same* tool at different arguments carries different effect. State a grant on the seven axes below, naming only the ones the step's criteria actually need — an unnamed axis is denied, not unlimited.

| Axis | Grants | Typical over-grant |
|------|--------|--------------------|
| `resource` | which repo, path, tenant, record, branch | the whole working tree when three files were needed |
| `action` | read · draft · create · update · delete · send · execute | `update` where `draft` would have sufficed |
| `quantity` | file count, changed lines, item count, **transaction amount**, spend, tokens, API calls | unbounded — the step that edits 40 files instead of 4 |
| `time` | validity window, wall-clock bound, max turns, execution deadline, **maintenance window** | a grant with no expiry outliving the step that earned it |
| `destination` | where output may go: internal · external · published; recipient domain and channel | the outward-facing publish inheriting an internal-edit grant |
| `approval` | before-effect · above-threshold · exception-only · post-audit | an **Ask First** trigger silently absorbed into a broad grant |
| `reversibility` | undo · version · backup · compensation · manual recovery only | irreversible effect granted with no stated recovery route |

Four consequences worth stating explicitly:

- **Budget is a safety control, not a cost control.** Caps bound loops, tool abuse, injected-instruction blast radius, and cascading failure — the same caps that bound the bill. Tier them, because a cap at one level does not bound the level above it: **per step · per job/run · per tool · per session · per user or tenant · per day/month · one emergency global cap**. The last is the only backstop that crosses sessions, and it is the one most often missing. On exhaustion, return partial output, the unfinished steps, and the resume condition (Q17 typed residual) rather than failing bare.
- **Shrink the tool, not just the grant.** A narrow capability (`get_open_invoices(customer_id, limit)`) enforces authorization, range, audit, and idempotency at the tool boundary; a general one (`execute_sql`, `http_request`, bare shell) pushes all of that into a prompt, where it is a request rather than a control. Prefer granting a narrow tool over constraining a broad one.
- **A secret is a credential the task needs, not knowledge the model should see.** The failing path is `secret value → prompt → model → tool argument → log`, and every hop after the first is permanent: traces, summaries, and downstream calls all retain it. The tool resolves the credential internally and the model holds only an opaque reference — `charge_card(payment_method_id)`, never `charge_card(card_number, cvv)`. A redaction placeholder must not be reversible to the original.
- **Read-only is not automatically safe.** Read grants still aggregate, infer, and exfiltrate across sources — individually-permitted facts compose into sensitive relationships. A read grant carries `destination`, `quantity`, purpose, field, row, tenant, and retention like any other, and secrets pulled into context live in the trace, the summary, and any downstream spawn.

**Delegation record.** On chains that fan out ≥ 3 spawns or nest a feature-lead layer (Core Rule #9), the grant per spawn is journaled with the step: `from · to · allowed · denied · redelegation · expires_with`. It costs one line and is the only way an aggregated `SUCCESS` can be audited back to who was allowed to do what. Where the platform distinguishes them, record the acting identities separately — `actor_user · actor_agent · purpose · session · policy` in the token claims or policy context — so an audit can tell *who* an effect was caused for from *what* caused it. **Agent identity is not user identity**: running an agent on the end user's credential inherits the user's full permission set, which is always wider than the task and is the widest grant in the system. Use a dedicated identity with delegated short-lived tokens, audience restriction, and resource scoping.

**Budget is divided, not lent.** A parent that spawns three children and passes each the *same* ceiling has
authorized three times its own limit, and a feature-lead layer multiplies it again per level. Allocate a
share to each child, keep a reserve at the parent, and record the split alongside the grant. State the
ceiling on every dimension that can run away, not just tokens: `wall_time · model_calls · tool_calls ·
side_effects · monetary · human_interrupts` — a run bounded on tokens alone can still burn an hour, fire
forty tool calls, or interrupt the user six times.

**Three properties travel with a delegation.**

1. **Capability does not inherit.** A child receives what it was explicitly granted, never what the parent
   holds. `redelegation: false` is the default, and a child cannot grant onward what it was not given.
2. **Cancellation propagates downward.** Cancelling or aborting a parent cancels its children; a child that
   keeps running after its parent stopped is producing effects nobody is waiting for and nobody will check.
3. **Ownership transfers explicitly.** After a handoff, exactly one party owns the final answer, the
   cancellation, and the approval. Record the transfer — an unowned in-flight task is the state where every
   party assumes another is watching it.

## Failure Modes Prevented

| Failure | Mitigation |
|---------|------------|
| **Concurring agents treated as permission to cause the effect** | Q25 agreement is evidence, not authorization — the aggregate is a proposal; commit needs state + policy + bound approval + idempotency + recovery |
| **An upstream goal approval reused to authorize a downstream irreversible action** | Q26(a) approval does not cascade — the effect needs its own approval at its own tier |
| **An approval reused after the plan or the world changed under it** | Q26(b) approval binds to the payload and expires; re-obtain rather than re-use |
| **A gate that fires so often it is cleared unread** | Q26 approval fatigue — batch the routine under a stated policy, escalate deviations; count approvals that changed an outcome, not approvals issued |
| **An owner approving an exception to the control they own** | Q26 separation of duties — for irreversible or out-of-scope effects the approver is not the producer; no second party ⇒ stop at `T2 prepare` |
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
| **The bar quietly lowered so the run can pass** (criterion reworded, threshold relaxed, assertion weakened) | Q20 frozen criteria — a goalpost move needs a `DEC-n`, can never be `verified`, and is never made by the failing producer |
| `BLOCKED` / `blocked-external` used as a synonym for "hard" | Q21 — at least one materially different attempt, named in the report, or the hub routes it back |
| Budget exit leaving a polished shell around an unbuilt core | Q22 hard-core-first ordering |
| "Never give up" degenerating into thrash or budget burn | §0 — two identical failures ⇒ diagnose; `diminishing-returns` exit is finishing, not quitting |
| **Every AC met and a forbidden result caused anyway** (data lost, artifact published, credential logged) | Q2 prohibited outcomes as a separate field + §6 `held`/`violated`/`unverified` on its own axis |
| A step causing side effects far beyond what its task needed, because the platform allowed it | Q23 narrowest-grant authority, stated per spawn and non-wideable through delegation |
| An ambiguous request resolved by guessing at full effect, or blocked with nothing delivered | Q24 tier degradation — deliver the reversible form instead |

## Wiring

- **All autonomous chains** (Recipe or ad-hoc CLASSIFY output): §0 for the whole run, Q1–Q3 at CLASSIFY/PLAN, Q4–Q6 + Q21–Q24 during EXECUTE, Q7–Q8 + Q20 at AGGREGATE, Q9–Q19 at VERIFY/DELIVER. Enforced at the Workflow level — individual recipe references cite this protocol instead of re-deriving it, adding only recipe-specific specializations (e.g. reproduction recipes' parity oracles already satisfy Q3/Q10 via `_common/DIFFERENTIAL_PARITY.md`; `acceptance`'s G1–G10 subsume Q11).
- **`NEXUS_COMPLETE` / `NEXUS_COMPLETE_FULL`** (`reference/output-formats.md`): the Decision Ledger (interpretation entries first), the per-criterion Acceptance Provenance table, and the **Residual Ledger** (Q18, with the Q19 sweep line) are part of the final report — omit each section only when genuinely empty, and an empty Residual Ledger still reports the sweep as `scanned, 0 hits`.
- **Spawn prompts** inherit Q16–Q17 as the `Completion bound` field of the Agent Spawn Template (`reference/hub-authoring.md`): a spawned agent finishes its slice or returns `PARTIAL` with a typed residual — it never returns a stub as `SUCCESS`. Q23 rides the same template as the `Authority` field (narrowest grant, `redelegation: false` by default) and Q1's prohibited outcomes as `Prohibited outcomes`. The hub owns Q18–Q19; a step never self-certifies its own completion sweep (Q9).
- **Dialogue recipes** (`spec`, `delve`): the dialogue itself follows `reference/dialogue-protocol.md`; their spawned autonomous work (EXPAND fan-outs, EXCAVATE lenses, Quality-Gate reviews) follows this protocol. The two ledgers are siblings: ASSUME-n tracks what the *user* didn't decide; DEC-n tracks what the *run* decided alone.

This protocol governs the **hub's conduct of the run** — spawn prompts inherit only the pieces a step needs (its slice of the contract, Q10 evidence duty in the output envelope), never the whole protocol.
