# Core Contract — Rationale

Evidence and reasoning behind the Core Contract bullets in `SKILL.md`. Read when a
contract line needs justification, calibration, or a citation.

## Causal discipline

- **Correlation is not causation.** Two co-occurring events do not imply one caused the
  other. Require causal evidence (code path, state transition, or controlled toggle)
  before declaring root cause.
- **Never accept the first plausible cause.** Apply 5 Whys or Fault Tree Analysis to drill
  past surface-level symptoms until a systemic root cause is reached.
- **Two independent evidence points minimum** to confirm a root cause — e.g. code path +
  log trace, or bisect result + reproduction. One source is a hypothesis, not a finding.
- **Document ruled-out hypotheses** with the evidence that eliminated them. Negative
  results prevent future re-investigation of dead ends and strengthen confidence in the
  declared root cause.

## Breadth of evidence

- **Synthesize all available sources**: logs, metrics, traces, deploy records, feature flag
  changes, dependency health, recent config changes. A single data source biases the
  hypothesis space.
- **Reconstruct the event timeline** (who did what, when, in what order) before analyzing
  cause. Timeline gaps are investigation gaps — fill them before concluding.
- **Contributing factors alongside root cause.** Incidents rarely have a single cause;
  document environmental conditions, process gaps, and dependencies that enabled failure.

## After the root cause

- **Extent-of-cause check.** Once root cause is confirmed, search for the same pattern
  elsewhere in the codebase — a bug found once likely exists in similar code paths.
- **Track fix effectiveness.** Recommend monitoring failure recurrence for 2-4 weeks
  post-fix before declaring resolution confirmed.

## AI-authored code

- **Extra hypothesis round for AI-specific failure patterns** (boundary conditions, error
  handling gaps, dependency misunderstanding) when investigating AI-coauthored changes —
  Snyk reports ~36% security vulnerability rate in such code.
- **Slopsquat / hallucinated-import check** on `ImportError` / `ModuleNotFoundError` /
  unresolved-import symptoms involving recently-added dependencies: query registry
  existence and download history before code-path hypotheses. 5-21% of AI-suggested
  package names do not exist, and typo-squats are increasingly attacker-registered.
- **Generator-Evaluator separation.** When an AI agent authored the suspect change,
  investigate with a *different* model/role to avoid self-grade inflation; document engine
  attribution per evidence item.
- **Comprehension Debt as an RCA factor.** When root cause is "team did not understand what
  the AI generated", record `comprehension_debt: HIGH` and recommend `judge` review of the
  source change before the fix lands.
