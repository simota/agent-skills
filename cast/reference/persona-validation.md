# Persona Validation Methods

Purpose: Define how Cast validates personas with triangulation, survey evidence, clustering, and staged confidence upgrades.

## Contents

1. Why validation matters
2. Triangulation patterns
3. Survey thresholds
4. Clustering guidance
5. Synthetic persona rules
6. Validation statuses

## Why Validation Matters

Validation exists to avoid:

- proto-personas treated as facts
- confirmation bias from creators
- over-generalizing from too little data
- stale personas surviving market or product change

## Triangulation Patterns

| Pattern | Methods | Strength |
|---|---|---|
| Basic | interview `5-10` + survey `350+` | Cost-efficient |
| Behavioral | interview + behavior logs + experiment / test evidence | Verifies saying vs doing |
| Full | interview + survey + behavior logs + usability evidence | Highest confidence |

## Quantitative Survey Thresholds

- `350+` respondents per segment for `95%` confidence
- `1000+` total when comparing multiple segments
- Prefer behavior-based questions over preference-only questions
- Likert + free text is the default hybrid

## ML Clustering Guidance

### Algorithm Fit

| Algorithm | Use when | Caveat |
|---|---|---|
| K-means | clearly separated segments | requires preselected cluster count |
| DBSCAN | irregular clusters and outliers | parameter-sensitive |
| Hierarchical clustering | exploratory structure analysis | weak for very large datasets |
| Gaussian mixture | overlapping segments | higher computational cost |

### Cluster Count Rules

- Use `Elbow + Silhouette + Gap` together.
- `Silhouette > 0.5` is a good signal.
- Recommended persona count is `3-7`.
  - early product: `3-4`
  - mature product: `5-7`

## Validation Workflow

1. Collect behavior, survey, support, and satisfaction data.
2. Preprocess and normalize.
3. Cluster with more than one method when possible.
4. Match clusters against current personas.
5. Treat uncovered clusters as new persona candidates.
6. Raise confidence only after evidence-backed mapping.

## Synthetic Persona Rules

- Synthetic personas are hypothesis tools, not production truth.
- Use them to improve guides, expose gaps, or explore edge cases.
- Never treat them as substitutes for real user validation.
- Keep synthetic and real-data-backed personas explicitly separated.

### Algorithmic Fidelity (research baseline as of 2026-05)

When LLM-generated personas are used as synthetic survey respondents or simulated users, evaluate them against the "algorithmic fidelity" concept (Argyle et al., 2023; subsequent work through 2025-2026): the extent to which LLM outputs conditioned on a sociodemographic backstory actually reproduce the beliefs / attitudes / response patterns of the target sub-population.

Key 2024-2026 findings to keep visible during validation:

| Finding | Source pattern | Cast implication |
|---|---|---|
| Persona-conditioned LLMs often produce homogeneous, mode-collapsed responses on real-world prediction tasks (elections, national surveys) | Arxiv 2602.18462 and successors; NeurIPS 2024 "Questioning the Survey Responses of LLMs" | Treat single-LLM persona panels as **biased toward training-data majority**; require human triangulation before any policy-relevant claim |
| Of 63 peer-reviewed 2023-2025 persona-LLM studies reviewed, only ~35% discussed representativeness of their LLM personae | "Whose Personae?" (Arxiv 2512.00461) | Cast `bias-audit` must always report representativeness, not only attribute coverage |
| Persona-instructed LLMs maintain stable self-reports but regress toward mean on multi-agent simulations | "Stable Personas" (Arxiv 2601.22812) | Stable ≠ accurate; pair stability with external-validity check |
| Turn-by-turn persona drift of 20–40% across instruction-tuned LLMs (Gemma 2, Qwen 3, Llama 3.3) in prolonged dialogue | 2025 persona-drift studies | Multi-turn distribution packets (e.g., Echo walkthroughs) must include refresh anchors every 8–12 turns |
| Counterfactual instruction-following is weak: even when asked to simulate low-performing personas, GPT-4-turbo only drops 4.6%, o1 ~0% | Arxiv 2504.06460 | Treat LLM persona "weakness simulation" outputs as unreliable for accessibility / novice testing |

Operational rules:

- Cap AI-only personas at `0.50` confidence (proto tier) regardless of LLM provider.
- Require at least one non-LLM validation stream (interview, survey, behavioral log) before promotion to `active`.
- Record the LLM provider, model version, system prompt, and seed in `Source Analysis` for reproducibility — minimum metadata for any synthetic persona.
- Apply ISO/IEC 23894 risk-category framing (algorithmic transparency / fairness / robustness / human-AI interaction) when documenting synthetic-persona risk.

## Validation Statuses

| Status | Meaning |
|---|---|
| `proto` | hypothesis only |
| `partial` | validated by one stream only |
| `validated` | triangulated |
| `ml_validated` | supported by clustering evidence |

### Confidence Contributions

| Validation state | Contribution |
|---|---|
| Proto baseline | `0.30` |
| Interview validation | `+0.20` |
| Survey validation | `+0.15` |
| ML validation | `+0.20` |
| Triangulation complete | `+0.10` |

## Anti-Patterns

Common persona failure modes to detect and avoid during creation, maintenance, and organizational rollout.

| ID | Name | What goes wrong | Mitigation |
|---|---|---|---|
| `PA-01` | Demographics Fixation | Persona is mostly age/gender/job labels | Anchor on goals, pain points, and behaviors |
| `PA-02` | Single Monolithic Persona | One persona tries to represent everyone | Keep at least `P0/P1/P2` by default |
| `PA-03` | Happy Path Persona | Only ideal users are represented | Include friction-heavy or underserved users |
| `PA-04` | Proto-Persona Ossification | Hypotheses are treated as stable truth | Keep validation status explicit |
| `PA-05` | User-Buyer Conflation | Buyer and end user are merged | Split if goals or behaviors differ materially |
| `PA-06` | One-Shot Creation | Persona is created once and never updated | Use `AUDIT` and `EVOLVE` regularly |
| `PA-07` | Over-Designed Artifact | Persona looks polished but is weakly evidenced | Favor evidence density over visual polish |
| `PA-08` | Specificity Imbalance | Too vague or too fictional | Keep roughly 80% evidence / 20% inference |
| `PA-09` | Silo Creation | Persona is not shared or reusable | Register and distribute systematically |
| `PA-10` | Gallery Display | Persona exists as decoration only | Tie personas to downstream agent tasks |

### Persona Fatigue

Causes: too many personas, stale personas, personas not used in real decisions, overly repetitive artifacts. Mitigation: keep count manageable, deprecate stale personas, track downstream use, distribute task-specific versions.

### Anti-Persona

Use anti-personas to define who the product should not optimize for. Identify mismatched segments, document why out-of-scope, record cost/risk, keep separate from primary personas, revisit during strategy shifts.
