# Delphi Method Reference

Purpose: Structured anonymous expert convergence developed at RAND Corporation (Dalkey & Helmer, 1959-1963) for forecasting and decision-making under uncertainty. Multi-round questionnaire with controlled feedback isolates judgments from social pressure, status, and dominant personalities, allowing genuine convergence (or stable divergence) of expert opinion. Used when expertise is distributed, anchoring is risky, and audit trail of expert reasoning is required.

## Scope Boundary

- **magi `delphi`**: anonymous multi-round expert convergence on a forecast, estimate, or judgment with quantifiable distribution. Output is a converged estimate with IQR and Kendall's W stop-criterion record.
- **magi `decide` / `tradeoff` / `arbitrate` / `strategic` (default lanes)**: single-session three-perspective deliberation. Use when speed matters and a verdict (not a distribution) is the goal.
- **magi `sixhat` (elsewhere)**: single-room parallel-thinking. Delphi is multi-round and anonymous across rounds; Six Hats is co-located and named.
- **magi `devil` (elsewhere)**: structured opposition. Delphi seeks convergence; DA seeks to break consensus.
- **flux (elsewhere)**: reframes the problem. Delphi holds the question fixed and converges on its answer.
- **riff (elsewhere)**: collaborative iterative deepening, named and dialogue-based. Delphi is anonymous and questionnaire-based.
- **omen (elsewhere)**: enumerates failure modes. Delphi can quantify failure-mode probabilities, but its scope is broader (any uncertain quantity).

## Workflow

```
PANEL    →  select 7-15 domain experts; verify diverse expertise; isolate identities
         →  agree on question, response scale (numeric / Likert), stop criteria

ROUND-1  →  open-ended or anchored questionnaire; experts respond independently
         →  facilitator collects, anonymizes, computes distribution (median, IQR)

FEEDBACK →  send anonymized summary: median, IQR, range; outliers asked to justify
         →  experts see distribution but never identities or specific quotes attributable

ROUND-N  →  experts revise estimates with feedback; outliers re-justify or revise
         →  repeat until stop criterion met (typically 2-4 rounds total)

REPORT   →  final median + IQR + dissent rationales; Kendall's W for ranking convergence
         →  hand off to Magi VOTE with distribution as evidence, not as the verdict
```

## Classic vs Real-Time Delphi

| Aspect | Classic Delphi | Real-Time Delphi |
|--------|---------------|------------------|
| Tempo | Days-to-weeks per round | Minutes-to-hours; live dashboard |
| Format | Async questionnaire | Live anonymous platform |
| Anonymity | Strong (between rounds) | Strong (live) |
| Feedback timing | Between rounds, batched | Continuous, on-demand |
| Round count | 2-4 typical | Continuous until stable |
| Best for | High-stakes long-horizon forecasts | Time-pressed expert estimates |
| Risk | Drop-off across rounds | Live anchoring on early posters |

## Expert Panel Selection

| Criterion | Target | Why |
|-----------|--------|-----|
| Panel size | 7-15 | Below 7: noisy. Above 15: diminishing returns, dropout risk |
| Expertise diversity | 3+ sub-domains | Reduces shared-blindspot risk |
| Tenure spread | Mixed senior/mid | Prevents seniority anchoring |
| Stake symmetry | Mixed sponsors | Prevents single-stakeholder capture |
| Selection bias check | Document inclusion criteria | Auditability; avoid hand-picking confirming voices |
| Replacement policy | Tolerate up to 30% dropout | Below 70% retained, results unreliable |

## Anonymity Preservation

- **Identifier separation**: facilitator holds identity-to-response map separately; never embedded in analysis files.
- **Quote scrubbing**: free-text rationales are paraphrased or quoted without attribution before circulation.
- **Stylistic anonymization**: highly distinctive phrasing (jargon, idiolect) is normalized to prevent identification.
- **Outlier protection**: outliers asked to justify privately; their rationale circulated anonymously.
- **No live channel**: experts never communicate directly during rounds; all flow through facilitator.
- **Aggregate-only reports**: distribution shape, never per-expert traces.

## Convergence Indicators

| Indicator | Definition | Stop threshold |
|-----------|-----------|----------------|
| IQR (Interquartile Range) | Q3 − Q1 of numeric estimates | IQR ≤ 1 unit on 1-10 scale, or ≤ 10% of median |
| IQR shrinkage rate | (IQR_n − IQR_n+1) / IQR_n | < 15% improvement → stop (no more convergence to be had) |
| Kendall's W | Coefficient of concordance for rankings | W ≥ 0.7 = strong agreement; ≥ 0.5 = moderate |
| Median stability | abs(median_n − median_n+1) | < 5% of scale → stop |
| Dropout rate | (round 1 − round n) / round 1 | > 30% → results untrustworthy |

## Stop Criteria (Conjunctive)

Continue rounds until **all** of:

1. IQR ≤ threshold OR IQR shrinkage < 15% (no more convergence available)
2. Median stability < 5% across two consecutive rounds
3. No new substantive arguments introduced in feedback
4. Round count ≥ 2 (single round is a survey, not Delphi)
5. Round count ≤ 4 (more rounds: fatigue exceeds signal)

If criteria 1-3 hold but expert distribution remains bimodal, **declare stable disagreement** rather than forcing convergence — bimodality is information.

## Round-Count Guidance

| Rounds | Use case | Risk |
|--------|----------|------|
| 1 | Not Delphi — survey only | No iteration, no feedback effect |
| 2 | Quick Delphi for time-pressed decisions | Limited convergence; minimum acceptable |
| 3 | Standard Delphi | Best balance of convergence and dropout |
| 4 | Complex multi-question decisions | Watch dropout |
| 5+ | Almost never justified | Fatigue, arbitrary tie-breaking, diminishing returns |

## Tie-In With Magi's Three Perspectives

- Delphi outputs feed Magi as **distribution evidence**, not as a verdict:
  - **Logos** consumes numeric distributions, IQR, Kendall's W
  - **Pathos** consumes dissent rationales (why outliers held position)
  - **Sophia** consumes implication of distribution shape (bimodal = strategic disagreement; tight = high confidence)
- Delphi can replace one perspective when expertise is heavily external (e.g., regulatory forecast where in-house judgment is weak). In that case, Logos = Delphi distribution, Pathos and Sophia remain.
- For Engine Mode: Delphi-style anonymous rounds across Claude/Codex/Antigravity are conceptually possible, but engines lack independent training contexts in the way human experts do — treat as a calibration ensemble, not a true Delphi.

## Anti-Patterns

- Single-round survey labeled "Delphi" — without iteration and feedback, it's just a poll. Minimum 2 rounds.
- Identity leakage between rounds — exposed identities reintroduce social pressure, defeating the protocol's core mechanism.
- Forcing convergence on bimodal distributions — bimodality is information about genuine strategic disagreement; flattening it loses signal. Report stable divergence.
- Excessive rounds (5+) — fatigue and dropout dominate; convergence beyond round 4 is usually artifact, not insight.
- Hand-picked expert panel — selection bias produces engineered consensus. Document inclusion criteria; aim for diverse sub-domains and tenure.
- Skipping outlier justification — outliers may hold the highest-information position; their rationale is the most valuable feedback artifact.
- Sharing per-expert traces in feedback — even partial attribution (timing, response order) erodes anonymity. Aggregate-only.
- Using Delphi for time-critical decisions — even Real-Time Delphi has minimum hours; don't run it under acute time pressure where Magi `decide` would suffice.
- Treating Delphi median as the verdict — Magi's perspectives still vote; Delphi distribution is evidence, not vote count.

## Handoff

- **To Magi VOTE**: distribution (median, IQR, dissent rationales, Kendall's W) becomes structured evidence; perspectives evaluate against the distribution, not against individual expert votes.
- **To Omen**: if Delphi was used to estimate failure probabilities, output feeds Omen's RPN/AP scoring directly.
- **To Flux**: stable bimodality on a question often signals frame disagreement; route to Flux for reframing before further rounds.
- **To Researcher**: when expert panel disagrees on user-facing facts, escalate to empirical user research rather than running additional Delphi rounds.
- **To human**: bimodal distributions, low Kendall's W (<0.4), or >30% dropout require human judgment on whether to act on partial signal or commission deeper investigation.
- **To audit trail**: panel composition, round-by-round distributions, dropout log, anonymization protocol, and stop-criterion outcomes preserved; Delphi runs are reusable as priors for future similar questions.
