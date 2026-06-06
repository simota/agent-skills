# AI and LLM Persona Generation Risks

Purpose: Define AI-specific bias, ethics, validation, confidence guardrails, and cross-agent governance rules for persona generation. Referenced by **Cast** (generation), **Echo** (UI walkthrough), **Plea** (synthetic demand), and **Field** (validation).

## Contents

1. Risk categories
2. Bias effects
3. Hybrid workflow
4. Guardrails
5. Ethics
6. Cast integration
7. Synthetic persona governance (cross-agent rules)
8. Bias audit failure modes
9. Tagging rules
10. Usage constraints
11. Feedback loop

## Risk Categories

| Category | Risk |
|---|---|
| Data quality | biased training data, weak representativeness, stale snapshot effects |
| Bias | gender, age, cultural, socioeconomic stereotyping |
| Ethics | weak consent, privacy leakage, deepfake personas, weak explainability |
| Methodology | over-homogenization, weak segment discovery, amplified confirmation bias, weak validation |
| Organization | over-automation, skill erosion, cost illusion, unclear accountability |

## Bias Effects

Typical failure modes:

- stereotyped gender-role assumptions
- oversimplified older-user representations
- English- or majority-culture bias in global products
- persuasive but false personas produced by prompt injection or weak review

## Recommended Hybrid Approach

| Phase | Owner | Output |
|---|---|---|
| AI hypothesis generation | AI | draft proto-persona |
| Human deepening | Human reviewer | corrected and contextualized persona |
| Data validation | Research / analytics | validated persona |
| Continuous monitoring | AI + fresh data | drift alerts and update suggestions |

## Mandatory Guardrails

| Guardrail | Rule |
|---|---|
| Bias check | Review for gender, age, and cultural stereotyping |
| Source transparency | Record where each important attribute came from |
| Human review | AI-generated personas always require review |
| Confidence cap | AI-only generation is capped at `0.50` |
| Diversity check | Evaluate persona-set diversity, not just individual quality |
| Version tracking | Record AI-generated vs human-updated history |

## Ethics Principles

- Transparency: record model, prompt, and sources when AI materially shaped output.
- Fairness: audit for bias regularly.
- Human-centricity: real user evidence remains the authority.
- Minimality: use only the minimum sensitive data needed.
- Accountability: humans own the decision, not the generated persona.

## Cast Integration

Recommended generation-method labels:

- `manual`
- `ai_assisted`
- `ai_generated`
- `data_driven`

Promotion path:

- `ai_generated` or `proto`
- `ai_assisted` after human review
- `validated` after data-backed validation

---

## Synthetic Persona Governance

Cross-agent confidence and lifecycle rules for AI-generated personas.

| Rule | Definition | Applies To |
|------|-----------|------------|
| **Confidence cap** | AI-only generation capped at confidence ≤ 0.50 | Cast (generation), Echo (usage), Plea (usage) |
| **Promotion condition** | `proto → active` requires at least 1 human research validation stream | Cast (registry), Field (validation) |
| **Expiry** | Synthetic personas without human validation require forced review at 60 days | Cast (decay rules) |

## Bias Audit Failure Modes

All synthetic personas must be checked for these 4 failure modes before distribution:

| Failure Mode | Description | Detection |
|-------------|-------------|-----------|
| **Mode collapse** | AI produces homogeneous personas clustered around stereotypical archetypes | Check diversity across trait dimensions |
| **Bias laundering** | Fluent empathetic language masks underrepresentation of marginalized perspectives | Compare demographic coverage against target population |
| **Over-sanitization** | AI avoids negative traits, producing unrealistically positive personas | Verify negative/frustration attributes are present |
| **People-pleasing** | AI generates what it thinks the team wants to hear | Compare against real Voice/Trace data when available |

## Tagging Rules

| Context | Required Tag | Applies To |
|---------|-------------|------------|
| All synthetic-derived findings | `[synthetic-hypothesis]` | Echo (reports), Plea (demand reports) |
| Downstream bias risk | Include bias caveat in DISTRIBUTE packet | Cast (distribution) |
| WEIRD population warning | Flag when target is non-Western, non-English | Cast, Echo, Field |

## Usage Constraints

| Constraint | Rule |
|-----------|------|
| **Go/No-Go decisions** | Synthetic-only findings must NOT be used for go/no-go decisions |
| **Demand forecasting** | Synthetic demands require real-data calibration (see `plea/reference/calibration.md`) |
| **Research split** | 80% synthetic (rapid iterations, screening) / 20% human (depth, edge cases, cultural nuance) |
| **High-risk domains** | Regulated, novel markets, or culturally-sensitive contexts require human validation before any action |

## Feedback Loop

Synthetic persona findings flow back to Cast to improve confidence over time:

```
Echo walkthrough result      → Cast FUSE   (confidence adjustment)
Plea demand calibration      → Cast FUSE   (coverage gap signal)
Trace behavioral validation  → Cast EVOLVE (existing path)
Field interview result  → Cast promotion (proto → active)
```
