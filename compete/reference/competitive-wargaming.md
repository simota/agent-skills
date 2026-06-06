# Competitive Wargaming Reference

Purpose: Use this file when Compete must simulate competitor responses, stress-test strategic moves, or run red team / blue team exercises for strategic planning.

## Contents

- Wargaming fundamentals
- Wargame types
- Execution protocol
- Red team / blue team methodology
- Competitor response prediction
- Pre-mortem analysis
- Scenario tree construction
- Templates

## Wargaming Fundamentals

### What Is Competitive Wargaming?

Competitive wargaming is a structured simulation where teams role-play as competitors to anticipate responses to strategic moves. It transforms analysis from "what competitors are doing" to "what competitors will do in response to what we do."

### When to Use Wargaming

| Situation | Wargaming value |
|---|---|
| Before major pricing change | High — predict competitor price response |
| Before market entry | High — anticipate incumbent defense |
| Before product launch | Medium-High — anticipate competitive counter-launch |
| Before M&A | Medium — predict market restructuring |
| Annual strategy review | Medium — stress-test strategic plan |
| Reactive to competitor move | Medium — plan counter-response |

### Core Principles

1. **Role commitment**: Teams must think as the assigned competitor, not as themselves with insider knowledge.
2. **Information discipline**: Teams only use publicly available information about their assigned competitor.
3. **Multi-move thinking**: Consider 2-3 moves ahead, not just the immediate response.
4. **Structured output**: Every response must include rationale, timeline, and resource requirements.
5. **Debrief is the product**: The wargame itself is the process; the debrief findings are the deliverable.

## Wargame Types

| Type | Participants | Duration | Depth | Best for |
|---|---|---|---|---|
| **Tabletop** | Single analyst (Compete) | `1 session` | Moderate | Quick scenario exploration |
| **Red Team** | Compete + domain context | `1-2 sessions` | Deep | Specific competitor response prediction |
| **Full Wargame** | Multi-agent (via Nexus) | `2-3 sessions` | Comprehensive | Major strategic decision |

### Tabletop Wargame (Default)

Compete role-plays as each key competitor sequentially, predicting their response to a proposed move. This is the most common format and the default when wargaming is triggered.

## Execution Protocol

### Phase 1: Setup

```markdown
## Wargame Setup

### Strategic Move Under Test
- Our proposed action: [specific action]
- Timeline: [when we plan to execute]
- Investment required: [resources committed]
- Expected outcome if no competitor response: [best case]

### Competitor Roster
| Competitor | Role in wargame | Reason for inclusion |
|---|---|---|
| [Competitor A] | Primary adversary | [most likely to respond] |
| [Competitor B] | Secondary adversary | [could be affected] |
| [Competitor C] | Wild card | [unexpected response possible] |

### Information Base
- Competitor profiles: [available data sources]
- Recent moves: [last 6 months of competitive activity]
- Known strategic priorities: [from CI analysis]
- Resource constraints: [known limitations]
```

### Phase 2: Simulation (Per Competitor)

```markdown
## Competitor Response Simulation: [Competitor Name]

### Competitor Profile Summary
- Strategic priorities: [top 3]
- Known constraints: [budget, tech, talent, market position]
- Decision-making style: [aggressive/conservative/reactive/innovative]
- Historical response patterns: [how they responded to similar moves]

### Response Prediction
| Response option | Probability | Timeline | Intensity | Our impact |
|---|---|---|---|---|
| [Response A: e.g., price match] | [X]% | [timeframe] | H/M/L | [effect on our plan] |
| [Response B: e.g., feature counter] | [X]% | [timeframe] | H/M/L | [effect on our plan] |
| [Response C: e.g., ignore] | [X]% | [timeframe] | H/M/L | [effect on our plan] |
| [Response D: e.g., escalate] | [X]% | [timeframe] | H/M/L | [effect on our plan] |

### Most Likely Response
- Action: [predicted primary response]
- Rationale: [why this competitor would choose this]
- Timeline: [when they would respond]
- Our counter-move: [how we should prepare]

### Worst-Case Response
- Action: [most damaging possible response]
- Probability: [X]%
- Our contingency: [how we would handle this]
```

### Phase 3: Debrief and Synthesis

```markdown
## Wargame Debrief

### Scenario Summary
| Scenario | Probability | Net impact on our plan | Preparedness |
|---|---|---|---|
| Best case (competitors don't respond effectively) | [X]% | Positive | Ready |
| Base case (expected competitive response) | [X]% | [Positive/Neutral/Negative] | [Ready/Needs prep] |
| Worst case (aggressive coordinated response) | [X]% | Negative | [Ready/Needs prep] |

### Key Findings
1. [Finding 1 — what we learned about likely competitor behavior]
2. [Finding 2 — vulnerabilities in our plan]
3. [Finding 3 — opportunities we didn't see before]

### Strategic Recommendations
| Recommendation | Priority | Pre-condition |
|---|---|---|
| [Recommendation 1] | H/M/L | [what needs to happen first] |
| [Recommendation 2] | H/M/L | [what needs to happen first] |

### Contingency Plans
| Trigger | Response plan | Owner |
|---|---|---|
| [If competitor does X] | [We do Y] | [team/person] |
| [If competitor does A] | [We do B] | [team/person] |
```

## Red Team / Blue Team Methodology

### Red Team (Competitor Perspective)

The Red Team's job is to **attack** the proposed strategy as if they were the competitor.

Red Team questions:
1. What is the biggest vulnerability in this strategy?
2. How would I exploit it with the competitor's resources?
3. What would I do in the first 30/60/90 days?
4. What alliances would I form to counter this?
5. What messaging would I use to undermine this?

### Blue Team (Our Perspective)

The Blue Team's job is to **defend** and **adapt** the strategy based on Red Team attacks.

Blue Team questions:
1. Which Red Team attacks are most damaging?
2. Which can we prevent vs which must we absorb?
3. What modifications to our plan reduce vulnerability?
4. What early warning signals should we monitor?
5. What is our minimum viable response to each attack?

## Competitor Response Prediction

### Response Pattern Analysis

| Competitor type | Typical response pattern | Response speed |
|---|---|---|
| Market leader | Deliberate, resource-heavy, seeks to maintain status quo | Slow (weeks-months) |
| Fast follower | Quick copy/adapt, moderate investment | Fast (days-weeks) |
| Disruptor | Asymmetric response, may escalate unexpectedly | Variable |
| Niche player | Defend niche, may ignore if not directly threatened | Slow unless cornered |
| Resource-constrained | Limited response, may partner or pivot | Slow |

### Historical Pattern Matching

Always check: "How did this competitor respond to similar moves in the past?" Use:
- Press release / blog timeline after competitor announcements
- Pricing history after market changes
- Feature release cadence after competitive threats
- Hiring patterns after strategic shifts

## Pre-Mortem Analysis

### The Pre-Mortem Protocol

Imagine the strategy has failed. Work backward to find causes.

```markdown
## Pre-Mortem Analysis

### Scenario: Our strategy has failed. It is [date + 12 months].

### Failure Causes (brainstorm all plausible causes)
| Cause | Category | Probability | Preventability |
|---|---|---|---|
| [Cause 1] | Competitive response | [X]% | H/M/L |
| [Cause 2] | Market shift | [X]% | H/M/L |
| [Cause 3] | Execution failure | [X]% | H/M/L |
| [Cause 4] | Customer behavior | [X]% | H/M/L |
| [Cause 5] | Technology change | [X]% | H/M/L |

### Top 3 Most Dangerous Causes
1. [Cause] — Prevention: [specific action]
2. [Cause] — Prevention: [specific action]
3. [Cause] — Prevention: [specific action]

### Early Warning Signals
| Signal | What to watch | Check frequency | Threshold for action |
|---|---|---|---|
| [Signal 1] | [metric/event] | [daily/weekly/monthly] | [trigger condition] |
| [Signal 2] | [metric/event] | [daily/weekly/monthly] | [trigger condition] |
```

## Scenario Tree Construction

### Multi-Move Scenario Trees

For complex strategic situations, construct a decision tree showing 2-3 moves ahead.

```text
Our Move 1: [Action]
├── Competitor Response A (P=40%)
│   ├── Our Counter A1 → Outcome [+/-]
│   └── Our Counter A2 → Outcome [+/-]
├── Competitor Response B (P=35%)
│   ├── Our Counter B1 → Outcome [+/-]
│   └── Our Counter B2 → Outcome [+/-]
└── Competitor Response C (P=25%)
    ├── Our Counter C1 → Outcome [+/-]
    └── Our Counter C2 → Outcome [+/-]
```

### Rules for Scenario Trees

- Limit to 3 competitor responses per move (most likely, most dangerous, most surprising)
- Limit to 2-3 moves deep (beyond that, uncertainty dominates)
- Assign probabilities that sum to 100% at each branch
- Include a "do nothing" branch — competitors often don't respond
- Mark the highest expected-value path and the highest-risk path

## Integration with Compete Workflow

Wargaming fits into the `DIFFERENTIATE` phase:
- Use after `MAP` and `ANALYZE` provide sufficient competitive intelligence
- Feed wargame findings into battle cards and response plans
- Hand off strategic scenario results to Helm (`COMPETE_TO_HELM`) for financial simulation
- Hand off contingency plans to Sherpa via Nexus for execution decomposition
