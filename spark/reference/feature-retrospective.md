# Spark Feature Retrospective Reference

Purpose: Run post-launch reviews that extract durable learning, not blame. A feature retrospective separates *decision quality* from *outcome quality*, categorizes what was adopted / iterated / discarded, and feeds structured learnings back into the discovery loop so the next proposal benefits from the last one.

## Scope Boundary

- **Spark `retro`**: post-launch feature retrospective — outcome review, learning extraction, feeding learnings into discovery.
- **vs `Rank`**: Rank scores candidate items with ICE/RICE/WSJF; `retro` closes the loop on items that already shipped so Rank's future inputs are calibrated.
- **vs `Void`**: Void prunes scope; `retro` captures the learning from what was pruned and what was kept.
- **vs `Plea`**: Plea synthesizes user advocacy; `retro` reviews how actual users responded and corrects synthetic personas.
- **vs `Experiment`**: Experiment runs a single hypothesis test with a verdict matrix; `retro` reviews the feature over its full launch-to-steady-state lifecycle, across multiple experiments and organic usage.

If the question is "what did we learn from this launch?" → `retro`. If it is "did this single A/B test win?" → `Experiment`.

## When To Run Retro

| Trigger | Scope | Timing |
|---------|-------|--------|
| Major feature launch | Full retro | T+30 and T+90 |
| Experiment concluded (validated or invalidated) | Short retro | Within 1 week of verdict |
| Feature sunset | Sunset retro | T+30 after sunset |
| Outcome missed despite ship | Diagnostic retro | Within 2 weeks of miss detection |
| Outcome exceeded expectations | Success retro | Within 2 weeks — success is also learnable |

Run retros even on successes. Teams that only retro failures learn to fear launches, not to launch better.

## Adopted / Iterated / Discarded

Categorize each hypothesis, assumption, and decision from the launch into exactly one bucket:

| Category | Definition | Signal |
|----------|------------|--------|
| `ADOPTED` | Shipped as designed and the evidence supports continuing | Primary metric moved, guardrails held, sustained usage |
| `ITERATED` | Shipped but reshaped post-launch to fit reality | Feature pivoted, audience narrowed, mechanism changed |
| `DISCARDED` | Killed or quietly retired | Kill criteria triggered, or feature never found traction |

Every original proposal claim (persona, JTBD, hypothesis, fail condition, RICE inputs) is re-evaluated against outcome evidence. A proposal with five claims produces five category verdicts, not one.

## Retro Structure

```
## Feature Retrospective: [Feature Name]

Launched: [Date]  |  Retro window: [T+30 / T+90]  |  DRI: [name]

1. Original intent
   - Target outcome (KPI-aligned):
   - Target persona:
   - Hypothesis:
   - Fail condition:
   - RICE inputs at launch (R, I, C, E):

2. Observed reality
   - Actual reach vs projected:
   - Actual impact on target KPI:
   - Guardrail movement:
   - Unexpected effects (positive or negative):

3. Claim-by-claim verdict
   | Original claim            | Evidence | Verdict (ADOPTED / ITERATED / DISCARDED) |
   | Persona: [X]              | [data]   | [verdict]                                 |
   | JTBD: [Y]                 | [data]   | [verdict]                                 |
   | Hypothesis: [Z]           | [data]   | [verdict]                                 |
   | Fail condition held: [F]  | [data]   | [verdict]                                 |

4. Decision quality vs outcome quality
   - Decision quality: [did we reason well given the evidence available at the time?]
   - Outcome quality: [did reality confirm the decision?]
   - Disagreement (if any): [explain — this is often where the best learning is]

5. Learnings
   - Discovery learning (pattern to feed back into IGNITE):
   - Scoping learning (pattern to feed back into SPECIFY):
   - Validation learning (pattern to feed back into VERIFY):

6. Discovery-loop updates
   - Personas to update in Cast:
   - OST branches to prune / grow:
   - Proposal template refinements:
   - Anti-pattern additions:

7. Next bets
   - Follow-on opportunity (if any):
   - Explicit non-next-bet (what we are choosing NOT to do, and why):
```

## Decision-Quality vs Outcome-Quality

The most important lens a retro applies. A 2x2:

```
                     Good outcome        Bad outcome
                   +------------------+------------------+
Good decision      | Deserved win     | Unlucky — keep   |
                   | (reinforce)      | the reasoning    |
                   +------------------+------------------+
Bad decision       | Lucky — do not   | Deserved miss    |
                   | reinforce        | (change process) |
                   +------------------+------------------+
```

Rules:
- A good decision with a bad outcome is **not** cause for process change. Reinforce the reasoning, note the luck, proceed.
- A bad decision with a good outcome is **not** cause for celebration. Name the luck explicitly or the team will repeat the mistake.
- Process changes land on `bad decision / bad outcome` and `good decision / bad outcome where the pre-available evidence was stronger than we used`.

## Learning Extraction

Every retro must produce at least one durable learning in each of three layers. "We'll do better next time" is not a learning.

| Layer | Example learning | Where it lands |
|-------|------------------|----------------|
| Discovery | "Power users of feature X are not the same segment as power users of feature Y — our persona merged them wrongly" | `Cast` persona update + `Spark` IGNITE note |
| Scoping | "Our Effort estimates systematically miss migration cost on features touching billing" | `Rank` Effort guardrail + `Spark` RICE rubric |
| Validation | "30-day adoption window under-measured this feature class — habit formation needed 60 days" | `Experiment` MDE policy + `Spark` kill-criteria template |

A learning is durable when it changes a template, a default, a checklist, or a threshold — not when it changes a team mood.

## Feeding Learnings Back into Discovery

The retro is worthless if the output sits in a doc. Required feedback paths:

| Finding | Feedback target |
|---------|-----------------|
| Persona mismatch | Update `Cast` persona registry; record delta |
| Opportunity tree was wrong | Prune / rewire OST in next `brainstorm` session |
| RICE inputs systematically biased | Update `Rank` scoring rubric with calibration example |
| Fail condition never triggered despite miss | Tighten `kill` thresholds for similar features |
| Synthetic user advocacy was off | Re-calibrate `Plea` prompts for this segment |
| Anti-pattern observed | Append to `feature-ideation-anti-patterns.md` |
| Sunset executed well / badly | Append template refinement to `kill-criteria-sunset.md` |

Every retro entry in `.agents/spark.md` ends with: "Fed back to: [named artifact + update]." If that line is blank, the retro did not finish.

## Blameless Framing

Retros die when they become blame sessions. Blameless rules:

- Critique decisions, not people. "The fail condition was under-specified" is fair; "X should have caught this" is not.
- Assume every participant had the best information available at the time. When the decision looks wrong in hindsight, the gap is usually information, incentives, or process — not judgment.
- Invite upstream-and-downstream agents (Pulse, Voice, Compete, Builder, Experiment) to contribute evidence. A retro run only by the proposer confirms the proposer's narrative.
- Name concrete next-bet owners. "Someone should update the persona" never happens; "Cast, by next Tuesday" does.

## Anti-Patterns

- Running retros only on failures — successes are learnable, and retro-less successes get mis-attributed.
- Single-verdict retros ("it worked / it didn't") — the unit of review is the claim, not the feature.
- Conflating decision quality with outcome quality — produces either over-confidence after lucky wins or over-correction after unlucky losses.
- Retros without a feedback target — the learning dies in the doc.
- Blame framing ("whose fault") — kills the next retro's honesty.
- "We'll do better next time" as a learning — not durable, not testable.
- Retro-by-proposer only — confirmation loop; invite upstream evidence owners.
- Skipping retros because the feature is "still running" — the T+30 and T+90 windows exist precisely so retros do not wait for arbitrary stability.
- Retro findings that reinforce the team's prior beliefs every time — this is narrative maintenance, not learning.
- No explicit non-next-bet — without naming what you choose not to do, the team will do all of them.

## Handoff / Next Steps

- If retro surfaces a persona update → hand to `Cast` with the persona delta.
- If retro surfaces an OST rewire → re-enter `brainstorm` with the updated tree.
- If retro surfaces a RICE / Effort / Impact calibration issue → hand to `Rank` with the calibration example.
- If retro surfaces a sunset decision for a still-running feature → hand to `kill` with evidence link.
- If retro surfaces an anti-pattern worth adding to the corpus → update `reference/feature-ideation-anti-patterns.md` directly.
- If retro is blocked by missing telemetry → hand to `Pulse` to instrument; park retro at T+30 extension.
- If retro needs real user interviews to resolve "why did adoption plateau?" → hand to `Field` or `Voice`.

Record the retro in `.agents/spark.md` with: feature name, retro window, top-three learnings, feedback targets updated. Incomplete feedback targets block retro closure.
