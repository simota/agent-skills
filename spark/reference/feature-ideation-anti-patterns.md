# Feature Ideation Anti-Patterns

Purpose: prevent Spark from generating features that are politically driven, weakly validated, or strategically misaligned.

## Contents
- Core anti-patterns
- Kill criteria
- Shiny-object filter
- Explore vs exploit balance
- Proposal checklist

## Core Anti-Patterns

| Anti-pattern | Signal | Spark countermeasure |
| --- | --- | --- |
| Feature Factory | output count matters more than outcome | require outcome, adoption plan, and post-launch review |
| HiPPO Effect | executive opinion dominates evidence | require persona, data, and hypothesis |
| Build Trap | teams focus on building rather than outcomes | anchor every idea to a business result |
| Sunk Cost Fallacy | prior effort forces continuation | define kill criteria up front |
| Shiny Object Syndrome | novelty or competitor hype drives scope | require product-vision fit and persona evidence |
| Solution-as-request | user-suggested solution is accepted as the problem | ask for the underlying need first |
| Premature MVP | "minimal" becomes unusable | keep MVP viable, not merely small |
| Exploit-only Discovery | only optimize what exists | preserve exploration capacity |

## Feature Factory

Reference data point:
- roughly `80%` of enterprise software features are barely used or not used at all

Diagnostic signals:
- shipped feature count is treated as success
- adoption is not measured after launch
- backlog growth never slows down
- teams ask "what next?" more often than "why?"
- stakeholder requests enter delivery without discovery

Escape moves:
- focus OKRs on outcomes, not output
- use data-backed prioritization such as `RICE`
- define adoption and retention checks before shipping
- add kill criteria to every material proposal

## HiPPO And Build Trap

Rules:
- data beats hierarchy
- personas beat generic stakeholder preference
- hypotheses beat intuition
- outcomes beat busyness

Build Trap reframing:

```
Do not ask: "What should we build next?"
Ask: "Which outcome matters most, and what is the smallest move that can improve it?"
```

## Kill Criteria

### `## Kill Criteria`

Add this block when the proposal needs a post-launch stop condition.

Minimum structure:
- adoption below `___%` after `30 days`
- primary metric regresses by `___%`
- experiment shows no statistically significant improvement

Rule:
- if a feature cannot define a realistic kill condition, treat it as riskier than it looks

## Shiny Object Filter

Use this sequence:
1. Does it fit the product vision?
2. Is it grounded in a target persona need?
3. Is the `RICE Score` above the bar?
4. Can an existing feature be extended instead?

If any answer is no:
- reject, backlog, or convert the idea into an enhancement rather than a new feature

## Explore vs Exploit

| Mode | Meaning | Spark response |
| --- | --- | --- |
| `Exploit` | optimize existing strengths | use favorite patterns and current data |
| `Explore` | investigate new possibilities | widen the opportunity set before specifying |

Recommended portfolio balance:
- `Exploit 70%`
- `Explore 30%`

## Proposal Checklist

### Before proposing

- a concrete persona exists
- the desired outcome is named
- `RICE Score` is calculated
- kill criteria are defined when relevant
- existing feature extension was considered first

### While proposing

- the proposal is data-backed, not HiPPO-backed
- the idea matches product vision
- the hypothesis is measurable
- sunk-cost bias is not driving continuation

### After proposing

- adoption measurement is planned
- kill-criteria review is scheduled
