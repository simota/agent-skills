# Business-Tech Translation

Purpose: Use this file when business language must be turned into implementable requirements without losing intent.

## Contents

- Translation loop
- Intent mapping
- Scope-creep detection
- Glossary cues
- Communication anti-patterns

## Translation Loop

`CLARIFY -> ALIGN -> GUARD -> DOCUMENT`

| Phase | Goal | Typical action |
|---|---|---|
| `CLARIFY` | convert vague business intent into explicit requirements | turn vague language into measurable `L1` items |
| `ALIGN` | remove expectation gaps | compare business and technical interpretations |
| `GUARD` | prevent scope creep | flag new asks, impact, and trade-offs |
| `DOCUMENT` | preserve decisions | record assumptions, rationale, and decisions |

## Intent Mapping

| Business says | Translate as | Accord action |
|---|---|---|
| "make it fast" | performance requirement | define measurable SLA or KPI |
| "simple to use" | usability requirement | define usability criteria in `L2-Design` |
| "secure" | security requirement | define scope and threat expectations in `L1/L2-Dev` |
| "scalable" | load or growth requirement | define load targets |
| "like [competitor]" | feature parity request | map the exact capability, not the brand |
| "ASAP" | urgency, not scope | propose a cut or phased delivery |
| "can you just..." | likely scope expansion | flag as change impact |
| "it should be obvious" | implicit requirement | make it explicit in `L1` |

## Scope-Creep Signals

| Signal | Risk | Response |
|---|---|---|
| "while we're at it..." | high | defer or split |
| "can we also add..." | medium | estimate impact and trade-off |
| "it would be nice if..." | low | track as future enhancement |
| growing acceptance criteria | high | compare with original `L1` scope |
| new stakeholder late in the process | medium | re-align `L0` and scope |

## Glossary Cues

| Business term | Technical translation |
|---|---|
| downtime | service unavailability or SLA target |
| response | API or UI latency target |
| security | auth, authorization, encryption, auditability |
| scalability | load capacity and scaling model |
| usability | task completion, accessibility, cognitive load |
| performance | measurable latency or throughput targets |
| quality | defect rate, testability, reliability |

## Communication Anti-Patterns

| Anti-pattern | Failure mode | Prevention |
|---|---|---|
| jargon dumping | business readers disengage | translate through glossary |
| silent assumptions | each team imagines something different | list assumptions explicitly |
| scope ambiguity | "phase 1" means different things | define deliverables and out-of-scope work |
| missing why | teams cannot prioritize correctly | keep `L0` and `L2-Biz` clear |
| one-way specs | teams read but do not align | use `L3` plus cross-references |
