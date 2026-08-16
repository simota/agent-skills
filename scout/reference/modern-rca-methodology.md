# Modern RCA Methodology

**Purpose:** Evidence-driven RCA guidance for multi-factor failures and incident reviews.
**Read when:** Simple single-cause RCA is too shallow and you need contributing-factor analysis.

[Source: Google SRE — Site Reliability Engineering, Ch.15 "Postmortem Culture: Learning from Failure" (Lunney & Lueder, 2017) https://sre.google/sre-book/postmortem-culture/]

## Contents

- Contributing factors
- Evidence-driven RCA
- Causal graphs
- AI-assisted RCA
- Incident review

## From Root Cause To Contributing Factors

Modern RCA in complex systems assumes that multiple conditions often combine to create failure.

| Legacy Term | Modern Term |
|-------------|-------------|
| Root Cause | Contributing Factors |
| Human Error | Systemic Conditions |
| Failure | Unexpected Behavior |
| Blame | Learning Opportunity |

Rule:

- Even if you find `15` contributing factors, fixing the most meaningful `3-4` is usually enough.

## Limits Of Classic `5 Whys`

| Limitation | Countermeasure |
|------------|----------------|
| Single causal chain only | allow multiple `because` branches |
| Guessing without evidence | attach evidence to each why |
| Stops at human error | ask why the action was reasonable at the time |
| Ignores breadth | do breadth before depth |

## Evidence-Driven RCA

### Six-Step Flow

| Step | Action | Evidence Source |
|------|--------|-----------------|
| `1` | detect and quantify impact | dashboards, alerts |
| `2` | trace the request path | trace IDs, spans |
| `3` | correlate signals | traces, metrics, logs |
| `4` | identify recent changes | deploy history, flags, migrations |
| `5` | confirm cause | logs, repro tests, rollback validation |
| `6` | document and prevent | RCA report, monitoring, follow-up |

### High-Signal Heuristics

- Common-ancestor analysis: prioritize operations appearing in `50%+` of failing traces.
- Change intelligence: prioritize changes within `10 minutes` before the error spike.

## Causal Graphs

Model evidence as a chain or graph rather than a single line:

`Config Change -> Service A Timeout -> Service B Error Rate Up -> User-Facing Error`

Validate the graph with:

- reproduction
- traffic replay
- rollback or mitigation tests

## Counterfactual Test

A correlation survives until you try to break it. For each candidate factor, state the counterfactual **before** running it:

> If `<factor>` were absent or reverted, would the symptom disappear?

| Result | What it licenses |
|--------|------------------|
| Manipulating the factor makes the symptom disappear, reproducibly | Causal claim |
| Manipulation is impossible or was not performed | Correlational claim only — say so |
| Manipulation changes nothing | Factor is eliminated; record it so no one re-tests it |

Record eliminated factors explicitly. An RCA that lists only surviving hypotheses hides how much of the space was actually searched, and the next investigator re-walks it.

## Attribution Confidence

Every attribution carries a confidence label. Unlabeled attributions get read as `Confirmed` by default, which is how a plausible story becomes an accepted cause.

| Label | Bar |
|-------|-----|
| `Confirmed` | Reproduced, **and** the counterfactual manipulation removed the symptom |
| `Strongly supported` | Multiple independent evidence sources agree; counterfactual not performed |
| `Plausible` | Consistent with the evidence, but alternatives are not excluded |
| `Speculative` | Insufficient evidence; recorded as a hypothesis, not a finding |

Rules:

- Never report a single `Confirmed` cause for a major incident on the first pass — breadth before depth (see *Limits Of Classic `5 Whys`*).
- Downgrade, do not delete, a hypothesis that loses. The residual uncertainty is part of the report.
- State what evidence *would have been* decisive but was unavailable — the observability gap is itself a finding.

## AI-Assisted RCA

Useful AI capabilities:

- topology-aware correlation
- change intelligence
- causal graph proposal
- guardrail suggestion

Rules:

- AI proposes; humans verify.
- Evidence beats elegant theory.
- Silent logical errors are the most dangerous hallucination class.

## Incident Review

Preferred terms:

- `Incident Review`
- `Learning Review`

Suggested review sequence:

1. detect incident
2. declare incident
3. mitigate
4. resolve
5. wait `36-48 hours` before deep review
6. analyze
7. review meeting
8. track actions

Use blameless questions such as:

- What surprised us?
- Where was our system model wrong?
- Why did that action look reasonable at the time?

## Scout Usage

- Use contributing factors in `REPORT`.
- Include evidence links such as log lines, traces, config diffs, or replay links.
- When handing off to Builder, include systemic improvements, not just a local patch idea.
