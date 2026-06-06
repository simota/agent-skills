# Spark Kill Criteria & Sunset Reference

Purpose: Author kill criteria *before* commit and run sunset decisions *after* launch with intellectual honesty. The default human instinct is to nurse underperforming features; this reference gives Spark the structure to resist sunk-cost escalation, trigger fail-fast actions, and communicate sunsets without eroding user trust.

## Scope Boundary

- **Spark `kill`**: authoring kill-criteria thresholds at proposal time and running sunset decisions for launched features (feature-deprecation checklist, migration-off plan, sunset communication).
- **vs `Void`**: Void runs systematic YAGNI scope-cutting across a codebase or backlog; `kill` is narrowly about the shutdown decision for a specific proposed or launched feature.
- **vs `Rank`**: Rank is the priority-scoring framework (what to do next); `kill` is the sunset framework (what to stop doing).
- **vs `Plea`**: Plea surfaces user advocacy that may justify keeping a feature; `kill` consumes that signal but enforces the pre-committed threshold.
- **vs `Experiment`**: Experiment validates a hypothesis with a pre-committed MDE and guardrail; `kill` extends that discipline to post-launch feature lifecycle beyond a single test window.

If the question is "should this one feature stop?" → `kill`. If it is "should this whole scope get pruned?" → `Void`.

## Pre-Commit Kill Criteria

Authored at DISCOVER / SPECIFY, never after launch. A proposal without a kill threshold is a feature factory artifact.

| Dimension | Required threshold | Example |
|-----------|-------------------|---------|
| Adoption floor | minimum reach within window | `< 2% of eligible users adopt in 30 days -> kill` |
| Retention floor | repeat usage over window | `< 20% of adopters return W2 -> kill` |
| Primary-metric lift | directional improvement required | `no detectable lift on target KPI after 90 days -> kill` |
| Guardrail ceiling | regressions that trigger immediate kill | `support-ticket volume > +15% sustained 14 days -> kill` |
| Cost envelope | per-user serving cost | `unit economics LTV:CAC < 1.5 after 90 days -> kill` |

Rules for authoring:
- Thresholds must be **numeric** and **dated**. "Low usage" is not a kill criterion; "< 2% adoption at day 30" is.
- State the **measurement instrument** alongside the number (which dashboard, which event, which denominator).
- State the **decision-maker** and **review cadence** (weekly / monthly / at review gate).
- Every kill criterion must have a matching success criterion. Asymmetric thresholds that only define success produce features that never die.

## Fail-Fast Triggers

Not every kill waits for the formal review gate. Fail-fast triggers fire immediately.

| Trigger | Action | Owner |
|---------|--------|-------|
| Guardrail breach | Andon-cord pull — halt rollout / disable flag | On-call or DRI |
| Security / privacy regression | Immediate rollback | Sentinel + DRI |
| Cost anomaly beyond envelope | Rate-limit or disable | Ledger + DRI |
| Core-journey regression (signup / checkout) | Automatic rollback via flag | Release automation |

Andon-cord semantics: *anyone* on the team can pull the cord. The cost of a false pull is small; the cost of a missed pull compounds. Make the pull mechanism a named flag / command / channel — not a vibes-based Slack thread.

## Sunk-Cost Fallacy Resistance

The predictable failure mode: the feature underperforms, kill criteria trigger, and the team escalates commitment instead of killing. Counter-structure:

1. **Pre-commit in writing** — kill criteria signed by DRI + PM + engineering lead at launch. Retroactive softening requires the same three signatures and a dated note.
2. **Invert the question** — at every review gate, ask: "if this feature did not exist today, would we build it?" If no, sunset.
3. **Name the stakeholder who benefits from keeping it alive** — if the answer is "the team that built it", that is sunk cost; if it is "a concentrated user segment", measure their willingness to pay a keep-alive cost.
4. **Budget the rescue** — if the team wants one more iteration, time-box it (≤2 sprints) with a new, stricter threshold. A second miss is terminal.
5. **Separate decision quality from outcome quality** — a well-reasoned kill of a feature that later "could have worked" is still a good decision if the pre-committed evidence did not support keeping it.

## Feature Deprecation Checklist

Once sunset is decided, run the checklist in order. Skipping steps is how sunsets erode user trust.

```
[ ] Decision recorded with date, DRI, rationale, evidence link
[ ] Affected user segments enumerated (count + concentration)
[ ] Power-user / high-revenue dependency check  (flag exceptions)
[ ] Migration path defined  (alternative feature / manual workaround / data export)
[ ] Data export path confirmed for any user-owned data
[ ] Support + CS briefed with talking points and FAQ
[ ] Communication scheduled  (T-60 / T-30 / T-7 / T-0 / T+30)
[ ] Feature flag wired for staged disable
[ ] Analytics event retained for 1 cycle post-sunset (to measure residual usage)
[ ] Code + docs archival plan (not immediate deletion — see Migration section)
[ ] Post-sunset retro scheduled (T+30)
```

## Migration-Off Plan

A sunset without migration is a breakage. Required components:

| Component | Requirement |
|-----------|-------------|
| Alternative path | Named existing feature or documented manual workaround |
| Data portability | Export in a standard format (CSV / JSON) if user-owned data was captured |
| Grace window | Minimum 30 days for paid plans; 60–90 days for enterprise contracts |
| Partial dependents | API consumers / integrators notified via changelog + email, not only in-app |
| Reversibility window | Feature flag held for 1 full cycle past T-0 before code archival |

## Sunset Communication Template

```
Subject: [Product Name] is changing: [Feature X] will be retired on [Date]

We're writing to let you know that [Feature X] will be retired on [Date]. We're sharing this now so you have time to plan.

Why we're making this change
[1–2 sentences, outcome-focused, no blame on users. Either "usage has been limited and we're focusing on [area]" or "we've built [better alternative]". Do not lie.]

What this means for you
- [What stops working, and when]
- [What you can do instead — alternative feature / workflow / export path]
- [How to export your data, if applicable]

Timeline
- [T-30]: This notice
- [T-7]: Final reminder
- [T-0]: [Feature X] is read-only / disabled
- [T+30]: Code and data archived

Questions: [support link]

Thanks for using [Feature X]. Your feedback helped us learn what to build next.
```

Rules:
- Send to all affected users, not just active users — dormant users return and find breakage if uninformed.
- Never describe the sunset as "improvements" or "streamlining" without naming the loss. Euphemism erodes trust.
- If >5% of affected users are on paid plans, include a concession (extended grace window, credit, discounted migration assist).

## Andon-Cord Patterns

Borrowed from Toyota production: any team member can halt the line. Translated to features:

| Pattern | Trigger | Effect |
|---------|---------|--------|
| Red cord | Guardrail breach during rollout | Automatic flag-disable for new users; existing users unaffected until review |
| Yellow cord | Anomaly worth a human look | Page DRI; rollout pauses pending decision within SLA (≤4h) |
| Green cord | Routine review gate | Scheduled review at cadence |

Make the cords operationally real — a named channel, command, or dashboard — not a philosophical aspiration.

## Decision-Quality vs Outcome-Quality

Kill decisions are often second-guessed after the fact ("we killed it too early"). Separate the two axes:

- **Decision quality**: was the pre-committed evidence evaluated honestly at the threshold?
- **Outcome quality**: did the subsequent world confirm or contradict the decision?

A high-decision-quality, low-outcome-quality kill (feature later succeeds elsewhere) is still a good kill. Punishing it trains teams to never kill. Record decision rationale so retrospectives score the decision, not the outcome.

## Anti-Patterns

- Launching without pre-committed kill criteria — guarantees sunk-cost escalation.
- Using qualitative kill criteria ("low usage", "disappointing") instead of numeric thresholds.
- Retroactively softening the threshold after a miss without a signed, dated note.
- Treating "we might use it later" as a reason to keep — YAGNI belongs to `Void`, but the same logic holds for sunsets.
- Sunsetting silently or only via in-app banner — dormant users return and feel broken.
- Describing sunset as "improvement" without naming the loss.
- Immediate code deletion at T-0 — always hold the flag for one full cycle to allow reversal.
- Punishing the DRI for a high-decision-quality kill because the outcome disappointed — trains the org to never kill.
- Running sunset on a feature with a concentrated high-revenue dependency without offering a concession.
- Kill criteria with only success thresholds — asymmetric bars produce zombie features.

## Handoff / Next Steps

- If kill decision is pre-commit authoring → ship the criteria into the RFC and hand back to the normal `propose` / `refine` flow.
- If sunset is triggered by guardrail breach → hand to `Triage` for incident response, then return to `kill` for the formal sunset plan.
- If migration-off plan requires code archival and dependency cleanup → hand to `Sweep` + `Builder`.
- If sunset communication needs user-facing copy beyond the template → hand to `Prose`.
- If a concentrated high-revenue segment objects to sunset → hand to `Magi` for strategic arbitration.
- If the sunset yields learnings worth feeding back into discovery → hand to `retro` (see `reference/feature-retrospective.md`).

Record kill decisions in `.agents/spark.md` with decision date, rationale, evidence link, and outcome-at-T+90 so the org learns from kills, not just ships.
