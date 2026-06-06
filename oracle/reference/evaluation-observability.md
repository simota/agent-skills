Purpose: Use this file when you are designing evaluation suites, CI gates, rollout checks, tracing, or production monitoring for AI systems.

## Contents
- Two-layer evaluation model
- LLM-as-judge anti-patterns
- Task metrics
- CI/CD and rollout gates
- Observability pillars
- Monitoring thresholds
- Oracle gates

# Evaluation And Observability

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

## CI/CD And Rollout

Development:
1. run evals on every prompt change
2. block if regression is `>= 5%`
3. add failure traces to the stable test set

Deployment:
1. shadow mode `24h` minimum
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
| full request/response capture | query, response, tool calls, retrieved docs |
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
