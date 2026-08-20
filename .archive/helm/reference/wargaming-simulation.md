# Business Wargaming Simulation Reference — Helm

Purpose: Use this file when Helm must stress-test strategies through competitive wargaming simulation, build scenario trees from competitor responses, or integrate wargaming findings into strategic roadmaps.

## Contents

- Business wargaming in strategic context
- Helm's wargaming role vs Compete's role
- Wargaming simulation patterns
- Scenario tree integration
- Financial impact modeling
- Strategic stress-test protocol
- Templates

## Business Wargaming in Strategic Context

### Why Strategic Wargaming Matters

Traditional scenario planning asks "What if the market changes?" Wargaming asks "What if we act, and competitors react?" This transforms passive forecasting into active strategy stress-testing.

Key insight from military-to-business adaptation: AI-supported wargaming outperforms traditional methods by an average of `12.8%` in decision-making accuracy, with the most significant improvements in complex multi-actor scenarios.

### 2025-2026 Generative Wargaming State-of-the-Art

- **Johns Hopkins APL — GenWar / GenWar Sim** (announced 2025-03-03, dedicated GenWar Lab established 2025-11): integrates LLMs into the **Advanced Framework for Simulation, Integration and Modeling (AFSIM)** so new scenarios stand up in **under two weeks** vs months previously. Designed to "build wargames in days, analyze dozens of alternative futures at scale, and focus human attention on the scenarios that most demand thoughtful deliberation." ([JHU APL 2025-03-03](https://www.jhuapl.edu/news/news-releases/250303-generative-wargaming), [Military Times 2025-11-24](https://www.militarytimes.com/news/your-military/2025/11/24/new-lab-offers-generative-ai-for-defense-wargaming/))
- **CSIS Futures Lab — "It Is Time to Democratize Wargaming Using Generative AI"**: argues GenAI shifts the cost of running wargames from honoraria + travel + facilitator time to data curation, enabling many more analytical games per quarter; companion executive-education course `Building Better Strategies with AI, Red Teaming, and Gaming` extends the methodology to enterprise risk management, corporate governance, and strategic planning.
- **RAND** continues to publish on AI for wargaming and modeling (Artificial Intelligence for Wargaming and Modeling, EP68860), with a 2025 focus on guardrails for AI red-team agents to avoid escalation bias.
- Open research line — **`Scaling Intelligent Agents in Combat Simulations for Wargaming` (arXiv:2402.06694)** — provides the LLM-agent-as-Blue/Red-player baseline most enterprise adaptations build on.

For Helm, the practical takeaway: when Compete supplies competitor profiles, an LLM-agent loop can now generate the 3-5 most plausible response sequences per move at near-zero marginal cost. Use the financial scenario tree in `WG-1`/`WG-2`/`WG-3` to translate those branches into $ impact; do not trust the LLM-generated probabilities — assign them yourself or via Magi-style multi-perspective scoring.

### Helm's Role vs Compete's Role

| Responsibility | Owner | Description |
|---|---|---|
| Competitor response prediction | **Compete** | Red team / blue team, response probability, behavioral patterns |
| Strategic impact simulation | **Helm** | Financial modeling of responses, scenario-adjusted roadmaps |
| Combined wargame exercise | **Nexus** orchestrates | Compete predicts → Helm simulates → Magi decides |

Helm consumes Compete's wargaming outputs and translates them into financial scenarios and strategic roadmap adjustments.

## Wargaming Simulation Patterns

### Pattern WG-1: Response-Adjusted Scenario Simulation

Extend Helm's standard 3-scenario model with competitor response probabilities.

```text
For each strategic move under consideration:

Scenario A: No effective competitor response (P = Compete estimate)
  Revenue_A = Base forecast × (1 + move_uplift)
  Cost_A = Base cost + move_investment

Scenario B: Expected competitor response (P = Compete estimate)
  Revenue_B = Base forecast × (1 + move_uplift - response_impact)
  Cost_B = Base cost + move_investment + counter_response_cost

Scenario C: Aggressive competitor escalation (P = Compete estimate)
  Revenue_C = Base forecast × (1 + move_uplift - escalation_impact)
  Cost_C = Base cost + move_investment + escalation_defense_cost

Expected value = Σ (P_i × (Revenue_i - Cost_i))
```

### Pattern WG-2: Multi-Move Strategy Simulation

For strategies requiring sequential moves:

```markdown
## Multi-Move Simulation

### Move Sequence
| Move # | Our action | Investment | Expected competitor response | Response probability |
|---|---|---|---|---|
| 1 | [action] | $[X] | [from Compete wargame] | [X]% |
| 2 | [action, conditional on Move 1 outcome] | $[X] | [from Compete wargame] | [X]% |
| 3 | [action, conditional on Move 2 outcome] | $[X] | [from Compete wargame] | [X]% |

### Cumulative Financial Projection
| Path | Probability | Cumulative investment | Cumulative revenue impact | Net value |
|---|---|---|---|---|
| Best path (all moves succeed) | [X]% | $[X] | $[X] | $[X] |
| Expected path | [X]% | $[X] | $[X] | $[X] |
| Worst path (all moves face escalation) | [X]% | $[X] | $[X] | $[X] |

### Decision Rule
- Proceed if expected path NPV > 0 AND worst path is survivable
- Pause if expected path NPV > 0 BUT worst path threatens viability
- Abandon if expected path NPV < 0
```

### Pattern WG-3: Competitive Equilibrium Simulation

For markets approaching equilibrium or price wars:

```markdown
## Competitive Equilibrium Simulation

### Market State
- Total market: $[X]
- Number of active competitors: [X]
- Current price level: $[X]
- Margin structure: [X]%

### Price War Simulation
| Round | Our price | Competitor A | Competitor B | Our margin | Market share |
|---|---|---|---|---|---|
| Current | $[X] | $[X] | $[X] | [X]% | [X]% |
| Round 1 (our move) | $[X] | $[X] (predicted) | $[X] (predicted) | [X]% | [X]% |
| Round 2 (responses) | $[X] | $[X] | $[X] | [X]% | [X]% |
| Equilibrium | $[X] | $[X] | $[X] | [X]% | [X]% |

### Equilibrium Assessment
- New equilibrium price: $[X] (vs current $[X])
- Margin erosion: [X]pp
- Market share change: [X]pp
- Is this equilibrium sustainable? [Yes/No — why]
- Who benefits most from the new equilibrium? [Company]
```

## Scenario Tree Integration

### Converting Compete Wargame to Helm Scenarios

When receiving a scenario tree from Compete's wargaming, Helm assigns financial values to each branch:

```markdown
## Financial Scenario Tree

Our Move: [Action] — Investment: $[X]

### Branch A: No response (P=[X]%)
- Revenue impact: +$[X] / year
- Duration: [X] years
- NPV: $[X]
- Risk-adjusted value: $[X] (= NPV × P)

### Branch B: Price match (P=[X]%)
- Revenue impact: +$[X] / year (reduced from A due to price pressure)
- Margin impact: -[X]pp
- Counter-cost: $[X]
- NPV: $[X]
- Risk-adjusted value: $[X]

### Branch C: Escalation (P=[X]%)
- Revenue impact: -$[X] / year (net negative)
- Defense cost: $[X]
- NPV: $[X]
- Risk-adjusted value: $[X]

### Portfolio Expected Value
Σ Risk-adjusted values = $[X]

### Decision
- [PROCEED / PAUSE / ABANDON] based on portfolio expected value and worst-case survivability
```

## Financial Impact Modeling

### Wargame Impact on KPIs

```markdown
## Wargame Financial Impact Summary

### KPI Impact Matrix
| KPI | No response | Expected response | Escalation | Weighted average |
|---|---|---|---|---|
| Revenue growth | +[X]% | +[X]% | -[X]% | [X]% |
| Gross margin | [X]% | [X]% | [X]% | [X]% |
| CAC | $[X] | $[X] | $[X] | $[X] |
| Churn rate | [X]% | [X]% | [X]% | [X]% |
| Rule of 40 | [X]% | [X]% | [X]% | [X]% |
| Burn Multiple | [X]x | [X]x | [X]x | [X]x |

### Sensitivity Analysis
| Variable | ±10% impact on expected value | Most sensitive to |
|---|---|---|
| Competitor response probability | $[X] | [which probability assumption matters most] |
| Price elasticity | $[X] | [how price changes affect volume] |
| Response timing | $[X] | [fast vs slow competitor response] |
| Market growth rate | $[X] | [background market expansion] |
```

## Strategic Stress-Test Protocol

### WARGAME Mode Execution

When Helm is invoked in `WARGAME` mode:

```text
1. RECEIVE: Compete wargaming output (competitor response predictions)
2. QUANTIFY: Assign financial values to each scenario branch
3. SIMULATE: Run 3-scenario model for each branch
4. STRESS-TEST: Apply sensitivity analysis to key assumptions
5. SYNTHESIZE: Produce decision-ready recommendation
6. MONITOR: Define early warning signals and deviation thresholds
```

### Integration with FORESIGHT

After wargame-informed strategies are deployed:
- Track which scenario branch is materializing
- Compare predicted competitor response vs actual
- Recalibrate response probabilities for future wargames
- Feed accuracy data back to Compete for calibration (`HELM_TO_COMPETE_CALIBRATION`)

### Escalation Rules

| Wargame finding | Escalation |
|---|---|
| Expected value positive, worst case survivable | Proceed — include in roadmap |
| Expected value positive, worst case threatens viability | `HELM_TO_MAGI` for risk acceptance decision |
| Expected value negative | Recommend alternative strategy |
| High uncertainty (probability estimates have wide range) | Request additional Compete intelligence before deciding |

## Integration with Helm Workflow

Wargaming simulation integrates into the `VERIFY` phase:
- After standard scenario simulation, overlay competitor response scenarios
- Use wargaming to stress-test the strategic roadmap before `PRESENT`
- Include wargame findings in the Execution Roadmap section
- Set monitoring thresholds based on wargame scenario branches
- Feed results into FORESIGHT for post-deployment tracking
