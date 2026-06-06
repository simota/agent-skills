# Cast Distribution Adapters

Purpose: Adapt personas for downstream agents without changing the underlying persona record.

## Contents

1. Adapter overview
2. Echo adapter
3. Spark adapter
4. Retain adapter
5. Compete adapter
6. Accord adapter
7. Generic fallback
8. Selection logic
9. Multi-persona delivery

## Adapter Overview

| Adapter | Focus |
|---|---|
| Echo | testing flows, friction, confidence, recent changes |
| Spark | unmet needs, opportunity signals, constraints |
| Retain | lifecycle, churn risk, re-engagement |
| Compete | expectations, switching behavior, loyalty anchors |
| Accord | business context, alignment, decision confidence |
| Generic | minimal neutral summary |

## Echo Adapter

Use exact anchor:

`## ECHO_CONTEXT`

Required sections:

- `Persona Confidence`
- `Recent Changes`
- `Recommended Review Priority`

## Spark Adapter

Required sections:

- `## Persona: {name}`
- `### Unmet Needs`
- `### Feature Opportunity Signals`
- `### Constraints`
- `### Key Behaviors (Design Constraints)`

## Retain Adapter

Required sections:

- `## Persona: {name}`
- `### Engagement Profile`
- `### Value Drivers (Why They Stay)`
- `### Churn Risk Factors`
- `### Re-engagement Triggers`
- `### Lifecycle Recommendations`

## Compete Adapter

Required sections:

- `## Persona: {name}`
- `### Expectations Baseline`
- `### Comparison Behavior`
- `### Competitive Vulnerability`
- `### Loyalty Anchors`

## Accord Adapter

Required sections:

- `## Persona: {name}`
- `### Business Summary`
- `### Key Metrics Context`
- `### Business Objectives Alignment`
- `### Risk Areas`
- `### Decision Confidence`

## Generic Adapter

Required sections:

- `## Persona Summary: {name}`
- `### Core`
- `### Context`
- `### File`

## Adapter Selection Logic

| Target | Adapter |
|---|---|
| Echo | Echo adapter |
| Spark | Spark adapter |
| Retain | Retain adapter |
| Compete | Compete adapter |
| Accord | Accord adapter |
| Unknown | Generic fallback |

## Multi-Persona Delivery

When sending more than one persona, include:

- `## Cast Distribution: {service_name} -> {target_agent}`
- `### Quick Comparison`
- `### Individual Profiles`
- `### Cross-Persona Patterns`
