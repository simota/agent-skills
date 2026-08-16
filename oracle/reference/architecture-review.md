Purpose: Use this file when you are reviewing the design of a system that embeds AI — before implementation, before raising a feature's authority, or when re-reviewing after a change. Reviews the *architecture*, not the model choice.

## Contents
- What the review is not
- Review input package
- The twelve lenses
- Risk tiers and review depth
- Conditional approval
- Re-review triggers
- Oracle gates

# AI Architecture Review

## What The Review Is Not

A review that opens with "which model", "RAG or fine-tuning", or "which agent framework" has put the reversible question first and the irreversible ones last. Purpose, determinism boundary, authority, evaluation, degradation, and ownership decide the structure; the model is a swappable dependency inside it. Safety added after those are fixed cannot change the structure they created.

The output of a review is never just approve/reject. It is: **conditions · residual risks · owner · required evidence · rollback · re-review trigger**.

## Review Input Package

Assembled before the meeting, 1–3 pages is fine for a small feature. The rule is not length — it is that no listed topic gets deferred to "we'll work it out in implementation". Evaluation, authority, and fallback are the three that cannot be retrofitted without changing the architecture.

- Problem statement **and the non-AI alternative that was compared**
- System context / container view — AI decomposed into retrieval, generation, policy, action, evaluation, human decision (never one "AI Service" box)
- Data flow and trust boundary
- Deterministic / probabilistic boundary
- Interface, data, and evaluation contracts
- Agent authority matrix or tool inventory
- Failure modes and degradation plan
- SLO, latency budget, cost budget
- Threat model
- Change / migration / rollback plan
- Ownership and incident runbook
- Candidate ADRs

## The Twelve Lenses

| # | Question | Evidence | Issue when |
|---|----------|----------|------------|
| 1 | Where is it probabilistic? | data flow, output types, sampling config, sources of variance | **High** — a probabilistic output is implicitly converted into a command. "The LLM part" is not an answer: rerankers, safety filters, and human judgment vary too |
| 2 | What must stay deterministic? | invariants, policy decision points, domain validators | **Critical** — a security or monetary invariant is entrusted to a prompt |
| 3 | What changes most often? | change-rate map per model / prompt / retrieval data / policy / tool / eval set / code, with owners | **High** — changes owned by different people are coupled into one deploy |
| 4 | How far does a change propagate? | change impact matrix, dependency graph (`_common/EVIDENCE_LADDER.md` §3) | **High** — the blast radius of a model change cannot be enumerated |
| 5 | What counts as correct? | golden set, rubric, thresholds, owner — i.e. the Evaluation Contract | **Critical** — a high-risk effect has no acceptance condition. **High** — only a mean, no critical slice |
| 6 | Can failure be observed? | telemetry schema separating transport / syntax / semantic / authority / cost, plus retention, sampling, privacy | **High** — after an incident, the model, prompt, context, and tool calls cannot be reconstructed |
| 7 | Can it be stopped? | runbook, who holds the switch, game-day result | **Critical** — an agent with external effects cannot be halted immediately |
| 8 | Can it degrade? | degradation matrix with triggers and exit criteria | **High** — a critical function depends wholly on one provider with no alternative |
| 9 | Can it be reverted? | rollback bundle, retained prior versions, compensation | **Critical** — irreversible effects rolled out without a canary |
| 10 | Can blast radius be bounded? | authority matrix, quota, sandbox, bulkhead — by tenant, data, tool, amount, count, time, region, cohort | **High** — one credential can write to every tenant |
| 11 | Who is responsible? | named request / decision / system / incident owners, on-call, escalation | **High** — only collective nouns ("the AI team", "the business") |
| 12 | **Can the core structure be explained with the AI removed?** | domain model, non-AI fallback, process view | **High** — the prompt *is* the only business specification |

Lens 12 is the one most often skipped and the most diagnostic. If removing the AI makes the purpose and the state transitions unexplainable, business rules have been absorbed into the model, where they cannot be reviewed, tested, or owned.

**Four owners, kept distinct** (lens 11) — one person may hold several roles in a small system; the roles still separate:

| Owner | Holds |
|-------|-------|
| Request | what is to be achieved, whether the input is valid, what the expected result is |
| Decision | exceptions, irreversible effects, value judgments — with real authority to reject, amend, escalate. Not necessarily the operator clicking the button |
| System | architecture, SLO, evaluation contract, change process, operating budget |
| Incident | containment, evidence preservation, recovery, explanation — authority explicitly named for incident time |

**Human-in-the-loop is not a boolean.** A review point exists only when the reviewer has the evidence, the time, the authority to refuse, and accountability for the outcome. Approval screens defaulting to "approve", with rationale folded away and a queue that punishes refusal, convert human review into a signature on automation. Send to a human what is a value conflict, irreversible, externally consequential, contextually invisible to the system, or organizationally privileged — and do not push back work that could have been decided deterministically.

## Risk Tiers And Review Depth

One process for every feature slows the harmless experiments and buries the dangerous questions in paperwork. Tier by **effect and reversibility**, not by model size:

| Tier | Example | Required review |
|------|---------|-----------------|
| `R0` | personal drafting, no external send | purpose, data boundary, basic eval |
| `R1` | internal search, summarization, recommendation | citations, ACL, observability, fallback |
| `R2` | workflow branching, customer-facing output, limited writes | authority, canary, SLO, incident plan, security |
| `R3` | money, permissions, legal effect, broadly-scoped agent | independent security review, strong approval, game day, staged rollout, executive owner |

**Severity does not fall because the model got better.** "That is unlikely with the current model" is a hypothesis, not a mitigation.

## Conditional Approval

A review is not a hold-until-perfect gate. For a reversible, small-scope change, approve **with measurable exit criteria** — dated, owned, and falsifiable:

- collect 500+ critical-slice cases over two weeks of shadow running
- confirm citation-mismatch rate below threshold on a human sample
- start with write tools disabled
- degrade intake if p95 review-queue age exceeds 30 minutes
- run a security game day and operate the kill switch within 10 minutes

## Re-review Triggers

Approval is scoped to the design that was reviewed. Re-review when:

- **an output's downstream use changes from proposal to command** — the same model and the same prompt become a different system the moment a suggestion starts driving an API call. No model change is required for the risk to change
- authority widens (new tool, wider scope, higher budget, new destination)
- the model, provider, or retrieval index changes (`_common/EVIDENCE_LADDER.md` `R15`/`R17`)
- a new data class enters context (personal data, another tenant, external content)
- a semantic-failure class appears that the failure taxonomy did not have
- degradation or rollback is exercised for real and behaves differently than designed

## Oracle Gates

- review agenda opening with model selection -> reorder to purpose → boundary → contract → authority → failure → operations
- no non-AI alternative in the package -> block; capability is not a reason for adoption
- lens 5 or lens 7 unanswered at `R2`+ -> block
- lens 12 answered only by pointing at the prompt -> block; extract the business rules
- approval recorded as "approved the AI feature" -> rewrite as allowed effects, required evaluation, residual risk, stop and re-review triggers
- `R3` without a named incident owner and a rehearsed kill switch -> block
