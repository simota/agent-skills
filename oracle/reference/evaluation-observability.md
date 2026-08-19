Purpose: Use this file when you are designing evaluation suites, CI gates, rollout checks, tracing, or production monitoring for AI systems.

## Contents
- Test / Eval layer separation
- Evaluation Contract (the versioned artifact)
- Eval dataset stratification and slices
- Scenario generation (how cases are produced)
- Release gate as conjunction
- Two-layer evaluation model
- LLM-as-judge anti-patterns
- Task metrics
- CI/CD and rollout gates
- Observability pillars
- Monitoring thresholds
- Oracle gates

# Evaluation And Observability

## Test / Eval Layer Separation

Decide this before designing any eval. Two failure modes sit on either side of the line: pinning everything with exact-match assertions (brittle, breaks on every acceptable rewording), or handing everything to a model judge (loses the boundaries that were deterministically enforceable).

| | Deterministic Test | Probabilistic Eval |
|---|---|---|
| Input → | expected value | dataset + rubric |
| Output | pass / fail | score / distribution |
| Subject | types, contracts, state transitions | quality of open-ended output |
| Grader | code | human and/or model, calibrated |
| Regression | reproducible | sampling with confidence intervals |

Split the system, not the test suite:

```
Deterministic control plane      Probabilistic component
├─ type / schema / contract      ├─ relevance
├─ authorization / policy        ├─ groundedness
├─ state transition              ├─ completeness
├─ tool argument validation      ├─ style / usefulness
└─ timeout / retry / budget      └─ unsafe or misleading behavior
```

**"We have evals, so we don't need tests" is the expensive version of this mistake.** In an AI product, authn, billing, permissions, schema, tool arguments, state transitions, timeout, retry, and audit are ordinary software and stay deterministic. Conversely, HTTP 200 + schema validity says nothing about answer quality. They are layers, not alternatives.

Concrete deterministic checks for a RAG/tool answer path: output satisfies the JSON schema · every citation ID is a member of the retrieved source set · no personal-data field is emitted without authorization · tool calls satisfy allowlist and argument schema · cost / timeout / retry ceilings hold · actions requiring human approval never auto-execute.

## Evaluation Contract

Evaluation is not a scoreboard for comparing models — it is the architecture element that decides what may ship, what must roll back, and which authority a feature is allowed to hold. "As accurate as possible" and "human-level" are goals; neither can stop a release. Write the contract **at design time, alongside the architecture decision**, and version it with the feature.

```yaml
feature: contract_clause_assistant
business_goal: cut first-pass review time without increasing missed critical clauses
input_domain: JP/EN master service agreements, listed template families
expected_behavior:
  - list candidate deviations from the standard canon set
  - attach an evidence span from the source for each candidate
prohibited_behavior:
  - state a legal conclusion as settled
  - reference a contract outside the caller's permissions
success_metric: [critical_clause_recall, evidence_support_rate]
quality_threshold:
  critical_clause_recall: ">= 0.97 on critical slice"
  evidence_support_rate: ">= 0.95"
latency_budget: "p95 <= 8s to verified result"
cost_budget: "<= 0.18 USD per document (internal budget, at time of writing)"
safety_constraint:
  - cross_tenant_leakage == 0 in adversarial suite
  - external_send == disabled
evaluation_dataset: contract-eval-v12
human_review_policy: reviewer confirms every result; high-risk clauses surfaced first
online_monitoring: [override_rate, missed_clause_reports, no_evidence_rate]
rollback_condition:
  - critical_clause_recall < 0.95
  - cross_tenant_leakage > 0
owner: Legal Engineering / Contract Platform
```

Numbers are illustrative — derive them from the feature's risk, base rate, and reviewer capacity. What is not optional is the *shape*: quality, **prohibited behavior**, latency, cost, dataset identity, human policy, online signals, rollback condition, and a named owner in one versioned artifact. Thresholds scattered across a dashboard, a PR comment, and someone's memory are not a contract.

**Freeze the whole target, not the model.** A result is reproducible only against the bundle that
produced it: `product · model_name · model_version · system_prompt_hash · behavior_policy_version ·
memory_schema_version · retrieval_version · tool_schema_versions · permission_policy_version ·
interface_version · locale · evaluation_date`. Behavior moves with any of them, so "we did not change
the prompt" is not an explanation for a behavior change — and where a hosted model updates underneath
you, record the version information you can obtain plus the evaluation timestamp, and file the
irreproducibility as a known limitation rather than leaving it implied.

**Promotion gate.** If the team cannot build the evaluation dataset, cannot decide whether a prohibited behavior occurred, or cannot state a rollback condition — do not raise the feature's production authority. Ship it one action tier lower (read → propose → prepare → execute) until those three exist.

**Do not wire the business goal straight to one metric.** Split it: `Outcome` (task completion time, misses, rework, user trust) → `System Behavior` (evidence-backed candidates, ordered by importance, explicit unknowns, permission compliance) → `Component Metric` (retrieval recall, extraction recall, citation support, latency, cost). Component metrics are diagnostic; they are never a substitute for the outcome, and their correlation to it is confirmed in production, not assumed.

**Evaluate at the right unit.** A single mean over instances hides most agent and RAG failures. Score per `instance` · `turn/step` · `trajectory` · `task` · `session/workflow` · `population slice`. Final task success alone conceals wasted loops, dangerous tool calls, and cost blowouts; final answer quality alone conceals retrieval failure.

## Eval Dataset Stratification

Random sampling of past logs under-represents rare-but-severe failure. Build and version five distinct sets:

| Set | Contents | Purpose |
|-----|----------|---------|
| Representative | approximates normal traffic | detects average regression |
| Critical | low-frequency, high-damage tasks | never averaged into the headline score |
| Counterexample | error-prone boundaries, contradictory context, stale documents, out-of-permission requests | catches confident wrongness |
| Regression | past incidents and known failures, frozen | prevents recurrence |
| Adversarial | prompt injection, tool misuse, data-exfiltration probes | security surface |

Record per case: input, **expected evidence**, tolerance, prohibited outcomes, slice labels, reason for inclusion, last-updated, rights, and personal-data handling. A dataset built only from successful demo runs overstates quality by construction.

Sourcing from production logs is a privacy decision, not just a data decision — confirm consent, purpose, retention, and redaction, and treat "anonymized" as an assertion to verify, since re-identification risk survives naive scrubbing.

**Slices to analyze separately** (overall score can improve while a slice degrades): use case / intent · risk level · tenant or plan · language · input length and context size · retrieval hit vs miss · tool success / partial failure / timeout · model, prompt, and index version · whether a human escalation occurred. Choose slices by business impact and known failures; display uncertainty where a slice is under-sampled rather than reporting a point estimate.

## Scenario Generation

The five sets above say **which cases to hold**; this says **how cases are produced**. The two axes are
orthogonal — an adversarial *set* can still be built entirely from single-turn canonical cases, which
is the usual reason a suite passes and production does not.

| Method | Produces | What only this method catches |
|---|---|---|
| **Canonical** | cases written straight from the spec | spec/implementation mismatch — and overfits fastest, since the team wrote both sides |
| **Metamorphic** | meaning-preserving rewrites: word order, language, register, emotion, stated title, length, framing | the expectation is not the same *text* but the same *decision*; catches answers that move with phrasing |
| **Counterfactual pair** | one attribute varied, everything else held: age, gender, seniority, tone, purchasing power | unjustified response differences — the fairness failure an aggregate score never shows |
| **Adversarial** | injection, identity spoofing, memory poisoning, permission pressure, conflict of interest | whether the trust boundary actually holds, not whether the model refuses politely |
| **Longitudinal** | tens to hundreds of turns across sessions, with corrections, setting changes, and a model/policy update mid-run | accumulation: memory decay, drift, and independence *after* the user has pushed back repeatedly |
| **Field replay** | real usage under rights, privacy, and purpose limits | language, repetition, environment, and workaround behavior offline sets never contain |

**Single-turn evaluation is structurally blind to the third and fifth rows.** Long-horizon memory
benchmarks report large gaps precisely where extraction is easy but cross-session reasoning, temporal
ordering, knowledge update, and correct abstention are not — LongMemEval (Wu et al., 2025), LoCoMo
(Maharana et al., 2024). If a feature holds state across sessions, a suite without a longitudinal
method has not tested the feature.

**Field replay is not a licence to experiment on users.** High-risk changes go to sandbox, synthetic
data, staged rollout, and human supervision first; production is where you confirm, not where you find
out. Sourcing constraints are the same as for datasets above.

**Compare distributions, not means.** A drift check that reports only an average difference misses the
shape change that matters. Compare quantiles and failure rates per layer, attribute a significant
difference to a specific bundle component, and record intended changes in the release note and
unintended ones as issues.

## Release Gate: Conjunction, Not Average

A single composite score hides the failures that matter — a mean groundedness of `0.92` is not a release signal if one case exposed personal data. Gate on a conjunction:

```
Release = deterministic tests PASS
      AND critical failures = 0
      AND no-regression slices PASS
      AND latency / cost within budget
      AND human calibration completed
```

Declare `hard_failures` explicitly (unauthorized action, unsupported policy claim, personal-data exposure); a hard failure blocks release regardless of aggregate score. Routing:

```
if deterministic_fail:            reject
elif safety_score == fail:        reject
elif judge_confidence < threshold: human_review
elif score_regression > budget:   block_release
else:                             accept_for_canary
```

**Statistical discipline:** 80/100 vs 84/100 is not "4 points better". Compare pre/post on the *same frozen dataset*, separate critical failures from the mean, do not over-read small-sample differences, distinguish tasks needing multiple samples per input, and calibrate offline eval against production outcome. `temperature=0` does not guarantee reproducibility — provider-side implementation, model updates, and distributed execution still vary.

**Change one variable at a time.** Model, prompt, and retrieval index moved together cannot be attributed when quality shifts.

## Two-Layer Safety Net

- Layer 1: automated metrics for fast regression detection
- Layer 2: human review for nuance, bias, and domain correctness

Use both. Automated metrics catch scale problems; humans catch subtle failures.

## LLM-as-Judge Anti-Patterns

| ID | Anti-pattern | Mitigation |
|----|--------------|------------|
| `EV-01` | self-evaluation | different judge model or human review |
| `EV-02` | position bias | randomize order and repeat |
| `EV-03` | verbosity bias | score conciseness explicitly |
| `EV-04` | no rubric | use anchored scoring rubrics |
| `EV-05` | single judge | use `3+` judges or mixed review |
| `EV-06` | no ground truth | provide reference answers |
| `EV-07` | regenerated test sets | keep a stable test set |
| `EV-08` | monolithic evaluation | split Retrieval / Generation / Task |

Judge prompt essentials:
- task
- rubric anchors
- question
- ground truth
- response under test
- JSON output format

## Task-Specific Metrics

| Task | Primary metrics |
|------|-----------------|
| classification | accuracy, F1, precision, recall |
| extraction | exact match, partial match, F1 |
| summarization | ROUGE-L, BERTScore, faithfulness |
| generation | human preference, judge score |
| RAG | faithfulness, relevancy, Recall@K |
| code generation | Pass@K, execution success |
| agentic systems | task completion, step efficiency, tool-call accuracy, cost |

**When a human decides whether to accept the output, these metrics are incomplete on their own.** A
model that scores well and is systematically over-accepted has a worse net outcome than a weaker
one that is checked. Pair the task metrics with the calibration set in `reference/human-ai-trust.md`
§2 — `correct_acceptance` / `correct_rejection` / `overreliance` / `underreliance` — sliced by task
consequence and user population. Acceptance rate alone is not a calibration measurement.

## Path Evaluation — grade the route, not only the answer

Scoring the final output alone cannot separate a run that reached the right answer *safely* from one that
reached it by luck — nor can it credit the run that stopped short correctly, refused a dangerous effect, and
reported the evidence gap. Both matter more than the answer in a system with side effects.

Score the path against a rubric that a trace can be checked against mechanically:

| Criterion | Passes when |
|-----------|-------------|
| Termination | ended on an allowed stop reason, not by running out |
| Budget | within declared step / tool / token / cost ceilings |
| Routing | never entered a forbidden node; no route the task did not warrant |
| Approval | every high-risk effect was bound to an approval *before* it fired |
| Retry | only retryable classes retried, within limit, with a changed action or changed evidence |
| Idempotency | every external effect carried an identity key; no duplicate landed |
| Evidence | every major claim has a supporting path, not just a plausible sentence |
| Recovery | after an injected failure, the run reached a safe state |

**Node evaluation is separate from path evaluation.** Grade the individual decision points on their own
datasets — router (accuracy / abstain rate / *dangerous* misroute), validator (contradiction detection vs
false reject), memory admission (harmful admit vs useful reject), capability decision (allow/deny correctness,
stale policy). High per-node scores still compose into failure, so scenario tests stay.

**Coverage is measured over the graph, not the corpus.** A suite that exercises every happy node and no
failure edge reports high coverage and tests almost nothing that matters:

`node` · `edge` · `condition-outcome` · **`cycle-exit`** (every loop's exit reason taken at least once) ·
**`failure-edge`** · **`capability-deny`** (denial paths actually exercised) · `compensation-path` ·
`schema-version`.

**Rule: an evaluation that cannot fail on a path violation is an output test wearing an eval's name.**
Report path and output results separately — a configuration can improve one while regressing the other.

## CI/CD And Rollout

Development:
1. run evals on every prompt change
2. block if regression is `>= 5%`
3. add failure traces to the stable test set

Deployment:
1. shadow mode until the observed traffic covers the Critical, Counterexample, and Adversarial strata (§ Eval Dataset Stratification) at the declared case count — `24h` is a floor, not the exit condition. "Three quiet days" can mean zero risky slices were ever observed
2. canary `5% -> 25% -> 50% -> 100%`
3. validate quality, latency, cost, and safety at each stage

Production:
1. sample evaluation on `5%` of requests
2. drift alerts
3. periodic human review
4. feed findings back into the eval set

## Observability: 7 Pillars

| Pillar | Required fields |
|--------|-----------------|
| semantic instrumentation | `trace_id`, `span_id`, `session_id` |
| request/response capture | query, response, tool calls, retrieved docs — **structured metadata always; raw content opt-in, sampled, and redacted** (`beacon/reference/llm-observability.md`) |
| continuous metrics | tokens, cost, `latency_p95`, eval score |
| integrated evaluation | auto score, human score, agreement rate |
| real-time alerting | threshold and incident count |
| data export | export format and destination |
| enterprise security | access control and compliance status |

### Observability Anti-Patterns

| ID | Anti-pattern | Mitigation |
|----|--------------|------------|
| `OB-01` | siloed data | unify traces, evals, and alerts |
| `OB-02` | request-only view | add session-level tracing |
| `OB-03` | engineer-only evaluation | expose eval workflows to PM/QA/domain experts |
| `OB-04` | black-box inference | log rationale, tool calls, and checkpoints |
| `OB-05` | no multi-step tracing | trace Retrieval, Reranking, Generation, Tool Call separately |
| `OB-06` | monitoring platform becomes the largest uncontrolled PII store | prompt/response content is never a default span attribute — capture it as opt-in sampled span events with a stated purpose, retention window, and role-scoped access |

## Monitoring Dashboard

| Category | Alert threshold |
|----------|-----------------|
| p95 latency | `> 2x` baseline |
| sampled quality score | `< 90%` of baseline |
| daily spend | `> 120%` budget |
| error rate | `> 1%` |
| guardrail trigger rate | `> 5%` |
| user satisfaction | `< 80%` |

Deployment checklist:
- eval metrics meet or exceed baseline
- no regression in stable test suite
- safety guardrails tested
- latency within SLO
- cost per query within budget
- rollback plan documented

## Tools

- `DeepEval` for general LLM evaluation
- `RAGAS` for RAG-specific metrics
- `Langfuse` for tracing and observability
- `Braintrust` for eval plus prompt versioning
- custom suites for domain-specific acceptance

## Oracle Gates

- LLM judges itself -> require different judge
- test set is not fixed -> require stable set creation
- observability means logs only -> require tracing + eval integration
- evaluation is engineer-only -> recommend accessible eval workflows
- no deployment checklist -> require pre/post-deploy validation
