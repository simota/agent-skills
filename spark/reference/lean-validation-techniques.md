# Lean Validation Techniques

Purpose: choose the lightest validation method that can confirm demand, usability, or value before full implementation.

## Contents
- Method comparison
- Selection rules
- Fake Door
- Wizard of Oz and Concierge
- Lightweight PRD, RFC, ADR
- Spec-Driven Development

## Pre-Build Validation Methods

| Method | Cost | Typical duration | Best for | Fidelity |
| --- | --- | --- | --- | --- |
| `Fake Door Test` | very low | hours to `1 day` | demand and interest | low |
| `Wizard of Oz` | low to medium | `1-2 weeks` | user experience and usability | medium to high |
| `Concierge MVP` | medium | `2-4 weeks` | value and workflow | high |
| `Prototype (Forge)` | medium | `1-2 weeks` | UX and core flow | medium |
| `A/B Test (Experiment)` | high | `2-6 weeks` | measured effect on outcomes | high |

Selection rules:
- unknown demand -> `Fake Door Test`
- demand seems real but usability is unclear -> `Wizard of Oz` or `Concierge MVP`
- solution options need comparison -> prototype or `A/B Test`

## `## Pre-validation Plan`

Use this block in proposals that need early validation.

Required fields:
- validation method
- placement or entry point
- target segment
- success metric
- sample size
- what to do if the result misses the threshold

## Fake Door Test

Use patterns such as:
- CTA button to a waitlist
- menu item to a "Coming Soon" state
- in-app invite to a beta
- pre-order or early-access signup

Advanced metrics to watch:
- unique vs total clicks
- time to click
- post-click continuation vs bounce

Suggested proposal fields:
- `Placement`
- `CTA Text`
- `Success Criteria` such as `CTR >= ___%`
- `Duration`
- `Sample Size`
- below-threshold action: reconsider or pivot

## Wizard of Oz And Concierge MVP

| Method | User perception | Best for | Main risk |
| --- | --- | --- | --- |
| `Wizard of Oz` | users think the system is automated | UX and experience validation | ethical transparency and operator cost |
| `Concierge MVP` | users know humans provide the service | value and workflow validation | very limited scale |

Use `Wizard of Oz` when:
- the feature is technically complex
- experience quality matters more than scalability
- you need pre-build learning for AI-like behavior

Use `Concierge MVP` when:
- the full workflow must be validated end to end
- a human-delivered service can stand in for automation

## Lightweight Spec Formats

| Format | Best use | Notes |
| --- | --- | --- |
| Lightweight PRD | quick alignment | concise and iteration-friendly |
| `1-Pager` | fast stakeholder alignment | compresses key detail into one page |
| Amazon `6-Pager` | narrative-heavy strategic framing | dense reading, no slideware |
| `RFC + ADR` | changes needing feedback and a recorded decision | keep ADRs short |

RFC/ADR rules:
- use `RFC` when the change affects others and needs buy-in
- use `ADR` to record the chosen implementation direction after review
- keep the RFC review window to `2-3 days`
- keep the process lightweight

## Spec-Driven Development

Treat the proposal as an input artifact for AI-assisted build systems.

Implications for Spark:
- structured specs improve downstream build quality
- technical constraints must be explicit
- Builder handoffs should be ready for spec-first execution

Reference tool styles:
- Amazon Kiro: requirements -> design -> tasks
- GitHub spec-kit: multi-step spec plus constitution
- Tessl: specification as a maintained artifact

## Spark Phase Mapping

| Spark phase | Validation technique | Purpose |
| --- | --- | --- |
| `IGNITE` | discovery cadence | continuous opportunity discovery |
| `SYNTHESIZE` | ODI opportunity scoring | compare candidate opportunities |
| `SPECIFY` | lightweight PRD or RFC | document the idea quickly |
| `VERIFY` | Fake Door, Wizard of Oz, Concierge | validate before build |
| `PRESENT` | 1-Pager or SDD-ready spec | align stakeholders and downstream agents |
