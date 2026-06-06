# Debugging Anti-Patterns & Cognitive Biases

**Purpose:** Bias checks and anti-pattern guardrails for stalled or noisy investigations.
**Read when:** The investigation is drifting, overfitting an early theory, or generating noise faster than evidence.

## Contents

- Cognitive biases
- Debugging anti-patterns
- Scientific debugging
- Scout checklist

## Cognitive Biases

| Bias | Failure Mode | Countermeasure |
|------|--------------|----------------|
| Confirmation bias | only seeks supporting evidence | design falsification tests |
| Anchoring | sticks to the first error or theory | keep multiple active hypotheses |
| Availability heuristic | overweights recent similar bugs | require evidence before pattern matching |
| Fixation bias | slow hypothesis switching | use a `30-minute` progress rule |
| Hyperbolic discounting | prefers a quick patch over understanding | require repro and cause before fix handoff |
| Selective perception | sees only expected patterns | use a checklist and structured notes |

## Debugging Anti-Patterns

| Pattern | Failure Mode | Guardrail |
|---------|--------------|-----------|
| Shotgun debugging | many random changes, no learning | change one thing at a time |
| Premature fix | symptom suppressed, cause preserved | reproduce -> locate -> assess before fix |
| Printf overload | too much unstructured noise | if you add `10+` prints, switch to debugger or structured logs |
| Correlation mistaken for causation | wrong culprit | verify with rollback, repro, or traffic analysis |
| Cascading-error trap | fixes secondary failures first | resolve the first error, then rerun |
| Unverified assumptions | wrong mental model | assume nothing, verify everything |
| Multiple simultaneous changes | unclear causal result | isolate one variable per experiment |

## Scientific Debugging

`OBSERVE -> HYPOTHESIZE -> EXPERIMENT -> CONCLUDE`

Use:

- `Wolf Fence` style narrowing for large search spaces
- rubber-duck explanation to expose hidden assumptions
- pair debugging or fresh eyes when the investigation stalls

## Scout Checklist

Before starting:

- [ ] symptom, timing, and environment recorded
- [ ] `3` hypotheses from different categories generated
- [ ] timebox set for each hypothesis

During investigation:

- [ ] no single hypothesis has consumed more than `30 minutes` without progress
- [ ] results are recorded, not remembered
- [ ] one variable at a time is changing
- [ ] causal claims are backed by evidence

Before reporting:

- [ ] root cause is evidence-backed
- [ ] impact scope is assessed
- [ ] reproduction is minimal or conditions are clearly stated
