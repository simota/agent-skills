# Spark Prioritization Frameworks Reference

Purpose: provide the canonical scoring rules Spark uses to compare ideas and write measurable hypotheses.

## Contents
- Impact-Effort matrix
- RICE scoring
- Hypothesis templates

## Impact-Effort Matrix

Quadrants:
- `Quick Win`: high impact, low effort, do first
- `Big Bet`: high impact, high effort, consider carefully
- `Fill-In`: low impact, low effort, do if time allows
- `Time Sink`: low impact, high effort, usually avoid

Impact scale:

| Score | Meaning | Example |
| --- | --- | --- |
| `5` | core workflow improvement | reduces a daily task by `50%` |
| `4` | significant time savings | automates a repetitive 10-minute task |
| `3` | nice enhancement | better feedback or visibility |
| `2` | minor improvement | easier navigation |
| `1` | negligible value | cosmetic change only |

Effort scale:

| Score | Meaning | Typical scope |
| --- | --- | --- |
| `5` | major architectural change | multiple weeks, many files |
| `4` | cross-cutting change | several days |
| `3` | isolated component work | `1-2 days` |
| `2` | minor code change | hours |
| `1` | trivial config or copy | minutes |

## RICE

Formula:

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

Definitions:
- `Reach`: users or customers affected per quarter
- `Impact`: `0.25`, `0.5`, `1`, `2`, `3`
- `Confidence`: `100%`, `80%`, `50%`
- `Effort`: person-months, including design, build, test, and release

Priority thresholds:
- `> 100`: high priority
- `50-100`: medium priority
- `< 50`: low priority

### `## RICE Evaluation: [Feature Name]`

Required fields:
- `Reach`
- `Impact`
- `Confidence`
- `Effort`
- `Calculation`
- `RICE Score`

## Hypothesis Templates

### `## Hypothesis: [Feature Name]`

Required fields:
- `We believe that`
- `For`
- `Will achieve`
- `We will know we are successful when`
- `We will validate this by`
- `Timeline`

### `## Hypothesis Card`

Required fields:
- `ID`
- `Feature`
- `Status`
- `Target Persona`
- `Target Metric`
- `Current Baseline`
- `Target Goal`
- `Validation Method`
- `Sample Size`
- `Timeline`
- `Key Assumptions`
- `Risks`
- `Minimum Success Criteria`

### `## Hypothesis Tracker`

Track:
- `ID`
- `Feature`
- `Status`
- `Metric`
- `Result`

## RICE Guardrails (detailed)

- **Reach**: use segment-specific reach, not total users. A settings feature reaching 100% of users is wrong — only 10-20% open settings. Always use a consistent time period (e.g., quarterly) across all features being compared. [Source: pmtoolkit.ai; saasfunnellab.com]
- **Impact**: enforce distribution — ≤20% of features at Impact = 3. Define "High = ≥10% improvement in key metric." If everything is high impact, nothing is. [Source: pmtoolkit.ai]
- **Confidence**: default to 50% for unvalidated ideas. Only increase above 80% with quantitative evidence (analytics, experiments, large-N surveys). Meeting discussions alone do not justify high confidence. [Source: saasfunnellab.com]
- **Effort**: include design + testing + documentation + maintenance, not just engineering person-months. Always add a ≥30% buffer — things take longer than expected. [Source: monday.com; saasfunnellab.com]
- **Scope limitation**: RICE deprioritizes tech debt and infrastructure improvements that lack direct user reach. For such items, flag the limitation and recommend a separate evaluation track or route to `Atlas`. [Source: productplan.com — RICE Scoring Model]
- **Cross-team calibration**: when multiple teams use RICE, scores diverge without shared guidelines. If the context involves cross-team prioritization, recommend a calibration session with anchor examples before scoring. [Source: dovetail.com — RICE scoring model; productteacher.com — RICE guide]

## RICE Anti-Patterns

- **RICE is decision-support, not a decision-maker** — the estimation conversation teaches more than the final number. [Source: logrocket.com — RICE framework guide]
- **No excessive precision** — RICE is a relative ranking system, not an exact science. Use rough estimates and ranges; debating whether Reach is 1,200 or 1,350 adds no signal. [Source: dovetail.com — RICE scoring model; productteacher.com — RICE guide]
- **No black-box scoring** — computing RICE alone in a spreadsheet and announcing results in Slack makes prioritization opaque. Require cross-functional input during scoring: engineering for Effort, customer success for Reach/Impact evidence, sales for deal-blocking Confidence. With ±20% error on each factor, the resulting score carries ~80% compounded error — the scoring conversation teaches more than the number. [Source: fygurs.com — prioritization frameworks 2026; swkhan.medium.com — prioritization framework error compounding]
- **Feature-level only** — do not use RICE to prioritize strategic initiatives; route those to `Magi`. [Source: pmtoolkit.ai — framework misapplication]

## Horizon Ladder / Ambition Preservation (conservatism guard)

Tag every proposal with a **Horizon**:
- `H1` safe/incremental reuse
- `H2` adjacent new capability
- `H3` transformative/contrarian

Rules:
- Ensure at least one candidate or alternative framing is `H2`/`H3`. Reuse-bound discovery is the floor, not the ceiling — the best feature is sometimes one your data does *not* yet support.
- Rank proposals **within** their Horizon, never `H3`-vs-`H1` on one raw number; a transformative bet competes against other transformative bets, not against a settings toggle.
- RICE's Confidence factor structurally penalizes novel, unproven, high-upside bets — the more original the idea, the thinner its evidence, the lower its score. Do not let this silently kill bold options. Bold bets are tagged honestly (lower RICE confidence, explicit risk), never dropped.
- A slate with zero `H2`/`H3` candidates fails the VERIFY gate. "Safe and obvious" is a finding to flag, not a default to settle on.

[Source: McKinsey — Three Horizons of Growth]


---

## RICE Scoring Guardrails (SKILL.md excerpt)

- **Reach**: segment-specific, not total users; consistent time period across compared features.
- **Impact**: enforce ≤20% of features at Impact=3; "High = ≥10% improvement in key metric."
- **Confidence**: default 50% for unvalidated ideas; >80% only with quantitative evidence.
- **Effort**: include design + testing + docs + maintenance, plus a ≥30% buffer.
- **Scope limitation**: RICE deprioritizes tech debt / infra lacking user reach — flag it or route to `Atlas`.
- **Cross-team calibration**: recommend a calibration session with anchor examples before cross-team scoring.
- **Ambition preservation (conservatism guard)**: rank proposals **within** their Horizon (`H1`/`H2`/`H3`), never `H3`-vs-`H1` on one raw number; a slate with zero `H2`/`H3` candidates fails the VERIFY gate.

Full guardrail/anti-pattern rationale, examples, and sources → `reference/prioritization-frameworks.md`.

