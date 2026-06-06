# Estimation Anti-Patterns

Purpose: Use this reference when Harvest includes estimated effort and you need to explain limitations or avoid misleading productivity claims.

## Contents

- LOC pitfalls
- Estimation anti-patterns
- Fatigue warnings
- Harvest-specific guardrails

## LOC Pitfalls

| ID | Problem | Why it matters |
|----|---------|----------------|
| `EA-01` | Solution complexity != problem complexity | Hard work can produce little code |
| `EA-02` | Language dependence | LOC varies by stack |
| `EA-03` | Refactoring penalty | Code reduction looks falsely "unproductive" |
| `EA-04` | Non-coding work ignored | Design, review, debugging are invisible |
| `EA-05` | No quality correlation | More code can mean more defects |
| `EA-06` | Copy-paste incentive | Volume can displace maintainability |
| `EA-07` | Generated code pollution | Boilerplate distorts effort |
| `EA-08` | Team contribution invisibility | Mentoring and review disappear |

## Estimation Anti-Patterns

| ID | Anti-pattern | Guardrail |
|----|-------------|-----------|
| `EA-09` | Optimism bias | Prefer historical data and buffers |
| `EA-10` | Anchoring | Re-estimate when new information arrives |
| `EA-11` | Parkinson's law | Separate buffer from expected effort |
| `EA-12` | Ignoring scope creep | Version estimates when scope changes |
| `EA-13` | Using the fastest person as baseline | Report team-safe ranges |
| `EA-14` | Assuming linear effort | Apply complexity multipliers in larger or riskier work |

## Fatigue Warning

Long-hours metrics need explicit caution:
- Sustainable work beats raw hours.
- Night/weekend work `> 10%` should trigger a health warning.
- Do not reward long hours as productivity.

## Harvest Guardrails

- Mark hours as estimated.
- Prefer `min / expected / max` when reporting to managers or clients.
- Exclude auto-generated files when they materially skew effort.
- If estimate accuracy falls below `60%`, recommend reviewing the estimation process.
- AI-assisted coding (Copilot, Claude Code, Cursor, etc.) decouples LOC from human effort. When AI usage is high, prefer review-cycle and pickup-time signals over LOC-derived hours and document the AI posture in the report.
