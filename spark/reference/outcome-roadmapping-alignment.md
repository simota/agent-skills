# Outcome Roadmapping And Alignment

Purpose: align Spark proposals with outcomes, roadmap confidence, stakeholder roles, and staged validation.

## Contents
- Roadmap types
- NOW/NEXT/LATER rules
- DACI and product trio
- North Star alignment
- Ship-to-validate stages

## Roadmap Types

| Type | Focus | Benefit | Risk |
| --- | --- | --- | --- |
| Feature Roadmap | what ships and when | concrete and execution-friendly | rigid |
| Theme-Based Roadmap | focus areas | good storytelling | can blur priority |
| Outcome Roadmap | what result to improve | flexible and strategic | may feel abstract |

Spark default:
- record the target outcome in every proposal
- use Theme plus Outcome when comparing multiple proposals
- leave feature-level delivery sequencing to `Sherpa` or `Builder`

## NOW / NEXT / LATER

Classify proposals by confidence, not by calendar alone.

| Bucket | Confidence | Spark rule |
| --- | --- | --- |
| `NOW` | high | `RICE >= 100` and hypothesis already validated |
| `NEXT` | medium | `RICE 50-100` or currently under validation |
| `LATER` | low | idea stage, low confidence, or exploration only |

### `## Roadmap Position`

Required fields:
- `Position` (`NOW | NEXT | LATER`)
- `Related OKR`
- `Promotion Criteria`

## DACI And Product Trio

### `## Decision Framework (DACI)`

Required fields:
- `Driver`
- `Approver`
- `Contributors`
- `Informed`

Product trio mapping:
- PM viewpoint -> `Spark`
- Design viewpoint -> `Echo` or `Palette`
- Engineering viewpoint -> `Scout` or `Lens`

Use trio review when the proposal changes product behavior materially.

## North Star Alignment

Avoid:
- vanity metrics as the North Star
- setting the metric without operationalizing it
- keeping the same metric despite market change

Leading vs lagging mix:

| Type | Role | Examples | Ratio |
| --- | --- | --- | --- |
| Leading | predicts future movement | adoption, engagement | `60%` |
| Lagging | confirms business result | revenue, churn | `40%` |

### `## North Star Alignment`

Required fields:
- `North Star Metric`
- `Contribution`
- `Leading Indicator`
- `Lagging Indicator`

## Ship To Validate

Use staged validation rather than betting everything on full release.

### `## Validation Strategy`

#### Phase 1: Pre-build (`1-3 days`)
- `Fake Door Test`
- user interviews

#### Phase 2: Prototype (`1 week`)
- `Wizard of Oz` or `Forge` prototype
- persona validation with `Echo`

#### Phase 3: Limited Release
- feature-flagged release to a small segment
- track leading indicators for `___` days
- define kill criteria and rollback trigger

#### Phase 4: Full Release
- confirm guardrail metrics
- begin lagging-indicator tracking

Rule:
- validation-first shipping is preferred when uncertainty is material
