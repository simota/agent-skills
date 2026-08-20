Purpose: Use this checklist to prevent low-quality scenario work. It preserves the practical traps, the bias layer, and the quality gate Helm should apply before trusting scenarios.

## Contents
- `SCN-01..SCN-10`
- Bias impact
- Scenario quality checklist
- Helm quality gate

# Scenario Planning Pitfalls

## Anti-Pattern Catalog

| ID | Pitfall | Failure mode | Fix |
|---|---|---|---|
| `SCN-01` | Searching for the “correct” future | Treats scenarios as prediction instead of decision support | Use “plausible” and “challenging,” then ask what action each scenario demands |
| `SCN-02` | Asking the wrong question | Question is too broad, too narrow, or detached from decisions | Anchor the scenario question to a live investment or policy choice |
| `SCN-03` | Mixing trends and uncertainties | Uses deterministic trends as scenario axes | Separate fixed trends from true uncertainties |
| `SCN-04` | Four versions of the same worldview | Scenarios do not force different choices | Require materially different decisions per scenario |
| `SCN-05` | Data dominance, no imagination | Spreadsheets replace creative future recombination | Use data to inform stories, not to flatten them |
| `SCN-06` | Lifeless narrative | No actors, weak causality, no memorability | Add concrete actors, motives, and causal links |
| `SCN-07` | Decision-makers excluded | Scenarios do not change executive thinking | Involve decision-makers early in question and uncertainty selection |
| `SCN-08` | Missing “So what?” | Scenario creation stops before strategic implications | Spend equal time on action implications |
| `SCN-09` | One-off exercise | Scenarios are published and forgotten | Build early-warning indicators and review cadence |
| `SCN-10` | Ignoring emotional impact | Stakeholders resist because threatening futures are emotionally unmanaged | Normalize discomfort and make implications explicit |

## Bias Layer

| Bias | Distortion | Mitigation |
|---|---|---|
| Confirmation bias | Preferred scenario appears “most likely” | Assign a devil’s advocate |
| Anchoring | First scenario dominates evaluation | Start from multiple anchors |
| Overconfidence | Ranges are too narrow | Run a pre-mortem |
| Availability heuristic | Recent events dominate scenario salience | Review historical analogs |
| Framing | Wording shifts scenario evaluation | Reframe the same scenario from multiple angles |
| Groupthink | Agreement pressure reduces diversity | Use anonymous voting / Delphi-style input |

## Scenario Quality Checklist

### Design Quality

- The focus question is tied to a real decision.
- Scenario axes reflect genuine uncertainty, not fixed trends.
- The scenarios force different decisions.
- Each scenario is internally coherent.

### Narrative Quality

- Human actors and incentives are visible.
- Causal chains are explicit.
- The story is understandable to non-specialists.

### Process Quality

- Decision-makers participated.
- Strategic implications were derived.
- Early-warning indicators were defined.
- A refresh schedule exists.

### Bias Check

- A Red Team or devil’s advocate reviewed the set.
- “Most likely” language was avoided.
- At least one uncomfortable scenario was included.

## Helm Quality Gate

| Gate | Rule |
|---|---|
| Post-generation review | Run the full checklist on every scenario set |
| Bias penalty | If bias checks were skipped, subtract `0.2` from confidence |
| Refresh warning | If no update schedule exists, add a warning flag |
| Simulation use | Only feed high-quality scenarios into `SIMULATE` and `ROADMAP` |

## Integration

Use these rules with:

- `simulation-patterns.md` for short-, mid-, and long-horizon scenario generation
- `strategic-calibration.md` to track scenario quality over time
- `strategy-monitoring.md` to bind scenarios to live signals and assumption drift

## 2026 Generative-AI Scenario-Building Guardrails

GenAI now generates scenarios at near-zero marginal cost (per `wargaming-simulation.md`'s GenWar / CSIS-Futures-Lab notes and the *Scaling Intelligent Agents in Combat Simulations* line of work). Three failure modes are now standard checks:

| Failure | Signal | Mitigation |
|---|---|---|
| LLM "consensus future" | All N generated scenarios converge on the same trend (often the median pretraining-data view) | Force the model to defend the *minority* scenario; require historical analog citations |
| Hallucinated probabilities | Model attaches confident `P=...%` without evidence | Strip model-emitted probabilities; reassign via human-assessed Delphi or Magi panel |
| Narrative homogeneity | Same protagonist archetype across scenarios | Specify divergent actor roles (incumbent / disruptor / regulator / non-consumer) per scenario before generation |

Treat GenAI scenario output as Tier 4 (external default) per `data-inputs.md` — usable with disclosure, never authoritative.
