# Toil Reduction Reference

Purpose: Identify toil rigorously, score automation candidates, enforce a toil budget, and design the runbook → script → auto-remediation escalation path. Beacon identifies WHAT should be automated; `Mend` executes runtime remediation.

## Scope Boundary

- **Beacon `toil`**: toil audit, definition compliance, automation priority scoring, escalation-path design, toil budget governance. Output: prioritized toil list and automation roadmap.
- **Mend**: runtime auto-remediation execution with safety tiers, staged verification, and rollback.
- **Gear**: implementation of the automation scripts themselves.

Beacon identifies and prioritizes; Mend remediates; Gear implements. Do not collapse these roles — `Mend` needs a curated candidate list with safety classification, which is `toil`'s deliverable.

## Toil Definition (Google SRE Book)

Work is toil when it meets MULTIPLE criteria below. One criterion is insufficient — thoughtful ops work (postmortem writing, design review) is manual and repetitive but is NOT toil.

| Criterion | Meaning |
|-----------|---------|
| Manual | Requires a human in the execution loop |
| Repetitive | The same workflow, again and again |
| Automatable | A machine could do it if the environment existed |
| Tactical | Interrupt-driven, reactive; not strategic planning |
| No enduring value | State returns to the same place after completion |
| O(n) with service size | Scales linearly (or worse) with users/traffic/fleet |

The O(n) criterion is the most important filter: work that does NOT scale with service size can often be tolerated; work that does will drown the team.

## Toil Budget (SRE)

Per the SRE book, toil should be < 50% of SRE time; target < 25%. Above the budget:

| Toil % | Response |
|--------|----------|
| < 25% | Healthy; continue eliminating opportunistically |
| 25-50% | Within budget, investigate top drivers |
| 50-75% | Over budget; halt feature work on that service and automate |
| > 75% | Team is operations-only; escalate to leadership, rebalance headcount or cut scope |

Measure toil with time-tracking on on-call tickets and interrupts, categorized weekly.

## Automation Priority Score

Score each toil candidate on four dimensions, multiply:

```
Score = Frequency × TimePerOccurrence × GrowthTrajectory × EngineeringValue
```

| Dimension | Scale | Notes |
|-----------|-------|-------|
| Frequency | 1 (monthly) → 5 (multiple times per day) | Measured, not estimated |
| TimePerOccurrence | 1 (<5 min) → 5 (>1 hour, incl. context switch) | Include cognitive switch cost |
| GrowthTrajectory | 1 (flat) → 5 (super-linear with fleet) | O(n) work with fleet growth scores high |
| EngineeringValue | 1 (cosmetic) → 5 (frees on-call to do project work) | Not the same as business value — the value of freed SRE capacity |

Sort candidates by score descending. Work the top of the list first; anything scoring < 8 is usually a deprioritization candidate.

## Runbook → Script → Auto-Remediation Escalation

Automation is a staircase, not a switch. Each step reduces toil; no step is wasted.

### Step 1: Runbook

A written, tested procedure. Every alert MUST have one (Beacon core contract).

Exit criteria to move up: runbook has been executed ≥ 5 times with no procedural variance; the steps are deterministic.

### Step 2: Script (human-triggered)

A CLI / notebook / button that executes the runbook steps. Human decides WHEN, machine decides HOW.

Value: eliminates procedural error, shrinks time-to-recover, creates a reusable building block.
Exit criteria to move up: script has been triggered ≥ 10 times with 100% correct outcome; trigger decision is itself mechanical (clear signal → clear action).

### Step 3: Auto-remediation (machine-triggered)

The system detects the condition and executes the script. Hand off to `Mend` at this step.

Prerequisites before handing to Mend:

- Safety tier classification (read-only / reversible / irreversible).
- Verification step: how does the system confirm the fix succeeded?
- Rollback path: what does Mend do if verification fails?
- Blast radius cap: max number of remediations per time window.
- Kill switch: a way for humans to disable the remediation without a deploy.

If any prerequisite is missing, stay at Step 2 — do NOT promote.

## Toil Audit Workflow

1. Collect 30 days of on-call tickets, alert fires, and Slack-pager events.
2. Categorize each into: toil (by definition) vs project vs overhead vs training.
3. Sum toil hours; compute toil % of SRE capacity.
4. Cluster toil items into candidates (similar root task → one candidate).
5. Score each candidate with the Frequency × Time × Growth × Value formula.
6. For the top N candidates, place each on the escalation staircase (Step 1 / 2 / 3).
7. Produce the prioritized toil list with: item, score, current step, next-step owner, Mend handoff readiness.

## Anti-Patterns

- Automating a poorly understood procedure — automates the mistake. Require Step-1 maturity first.
- Jumping to Step 3 without rollback design — one bad remediation can amplify an incident; hand off to Mend only with safety classification.
- Counting postmortems, design review, and incident response as toil — they are overhead, not toil. Eliminating them damages the team.
- Automating rare events (Frequency = 1) before frequent ones — maintenance cost of the automation exceeds the toil saved.
- Measuring toil-reduction success by "# of scripts written" — correct metric is hours of toil eliminated per week, sustained over 30 days.
- Never retiring obsolete automation — dead scripts become future toil when they misfire. Treat automation as code, with deprecation lifecycle.
- Building local heroic scripts that never graduate to shared tooling — same toil pays twice across the team.

## Handoff to Mend

When a candidate reaches Step 3 readiness, hand off to Mend with:

- Trigger condition (alert or metric threshold).
- Safety tier (read-only / reversible / irreversible).
- Verification step and success criteria.
- Rollback procedure.
- Blast-radius cap and cooldown window.
- Kill-switch mechanism.
- Expected toil reduction (hours/week).

Mend owns runtime execution, staged rollout, and incident-time invocation from that point.

## References

- Google SRE book, Ch. 5, "Eliminating Toil" — definition, budget, and philosophy.
- Google SRE Workbook, Ch. 6, "Eliminating Toil" — concrete measurement and case studies.

## Cross-Links

- `alerts` — alert-driven toil is a primary source; reduce noisy alerts before automating their handling.
- `slo` — SLO-violating toil is highest priority; protects error budget.
- Mend — receives Step-3-ready candidates for runtime auto-remediation.
- Gear — implements the scripts at Step 2.
