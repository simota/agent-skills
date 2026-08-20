Purpose: Use these anti-patterns to catch strategy quality failures before simulation or roadmap output. This is a compact pre-flight review for planning quality and execution readiness.

## Contents
- `SP-01..SP-10`
- Strategy-execution gap
- Helm integration rules

# Strategic Planning Anti-Patterns

## Anti-Pattern Catalog

| ID | Anti-pattern | Signal | Why it fails | Fix |
|---|---|---|---|---|
| `SP-01` | Static Planning | Annual plan created and ignored | Cannot adapt to market change | Quarterly rolling review + drift detection |
| `SP-02` | Overambition | `5+` priorities at once | Resource dilution, about `30%` lower effectiveness | Cut to `<=3` priorities |
| `SP-03` | Data Ignorance | Intuition replaces market evidence | Weakens decision quality | Use data triangulation |
| `SP-04` | Market Blindness | Little or no market validation | Investment into non-existent demand | Require competitor and customer validation |
| `SP-05` | Communication Gap | Strategy is not understood downstream | Execution stalls despite executive alignment | Cascade via OKRs and role-specific summaries |
| `SP-06` | Silo Strategy | Functions plan independently | Local optimization blocks strategic execution | Force cross-functional review |
| `SP-07` | Entire Market Fallacy | “We serve everyone” | No positioning or focus | Choose segment and wedge explicitly |
| `SP-08` | Growth Driver Error | Strategy built on untested growth assumptions | Misallocated roadmap and budget | Pilot and validate the driver first |
| `SP-09` | Clarity Deficit | Goals are qualitative or vague | Teams interpret success differently | Convert strategy into explicit KPIs |
| `SP-10` | Execution Neglect | Strategy exists without milestones or owners | Plan never becomes action | Add roadmap, milestones, owners, review dates |
| `SP-11` | Vibe Strategy | "Direction" emitted from an LLM session without explicit assumptions, KPIs, or scenarios | Karpathy's Feb-2025 *vibe coding* framing migrated to strategy — "we just feel where the market is going." No falsifiability, no kill criteria | Force the 3-scenario rule + assumption table + measurable KPI per leg; if the AI cannot produce them, reject as a brainstorm output, not a strategy |
| `SP-12` | Moat Illusion | "Like X but with AI" / thin wrapper on a frontier model | If your differentiation disappears when the underlying model ships its next feature, you have a timer, not a moat. Q4 2025 - Q1 2026 churn for thin-wrapper AI ARR runs `~65%` over 90 days vs `~35%` SaaS norm | Require at least one of: proprietary data flywheel, workflow depth, distribution lock-in, regulatory moat. Map the wrapper layer on a Wardley map — if all components are Commodity except the brand, abandon |
| `SP-13` | Validation Debt | Team "vibe-builds" with AI before talking to customers because "we can just build and see" | Builds the wrong product faster. Erodes the talk-to-users floor of YC / Sequoia AI Ascent 2026 playbook | Reinstate Tony Ulwick-style outcome interviews and Moesta-style switch-moment interviews **before** code; gate Forge prototypes on N≥5 validation conversations |

## Strategy-Execution Gap

Keep these execution-failure signals visible:

| Signal | Operational meaning |
|---|---|
| `67%` of well-formed strategies fail in execution | strategy quality alone is insufficient |
| `90%` of organizations fail to execute strategy consistently | roadmap and cascade matter as much as planning |
| `79%` of failures relate to poor collaboration | silo risk must be assessed explicitly |
| `60%` of resources can be wasted by misalignment | resource allocation must match strategic priorities |
| `5+` priorities reduce effectiveness by about `30%` | focus is a hard constraint, not a style preference |
| only `5%` of employees fully understand company strategy | strategy communication is systematically broken |
| `50%` of projects meet modern success criteria (PMI 2025) | project-level failure is a leading indicator of execution risk |
| `74%` of leaders say strategies are not translated to actions | planning-to-action translation is the critical bottleneck |

### Root Causes

| Cause | Severity | Fix |
|---|---|---|
| Alignment failure | Critical | Strategy -> function -> team -> individual linkage |
| Resource mismatch | Critical | Budget and staffing must follow priorities |
| Communication breakdown | High | Cascade strategy in role-specific language |
| Silo behavior | High | Cross-functional reviews and shared metrics |
| Weak accountability | High | Name owners and review cadence |
| Change resistance | Medium | Include transition risk and adoption plan |
| Weak measurement | Medium | Define KPIs before rollout |

## Execution Bridge

Use this bridge in roadmaps:

1. Translate strategy into KPIs and OKRs.
2. Align company, team, and individual goals.
3. Allocate budget and headcount by priority.
4. Communicate strategy to all levels.
5. Monitor monthly or quarterly.
6. Adapt when assumptions drift.

## Helm Integration

| Where | Use |
|---|---|
| `SCAN` | Check `SP-01..SP-10` before accepting the strategic frame |
| `SIMULATE` | Test priority overload and execution-capacity limits |
| `ROADMAP` | Score execution-gap risk before recommending a plan |
| Monitoring | Reuse alignment and communication checks from `ANCHOR` and `TRACK` |

When multiple anti-patterns are present, treat the output as lower-confidence even if the financial model looks clean.

## 2026 AI-Era Notes

- **Vibe-strategy detection signals** (any one triggers `SP-11`): no Assumption table, no KPI per option, "feels right" language without scenario branching, no kill criteria.
- **Moat-illusion gut check**: ask "would this product still exist 6 months after OpenAI / Anthropic / Google ships v-next of their flagship?" — if the answer is "no", `SP-12` applies. Reference: industry commentary on the "demo, not business" failure mode through 2025-2026; pairs with Carta Q1 2026 data showing AI seed valuations 42% above non-AI peers (`seobrien.com`, `Carta State of Pre-Seed Q1 2026`).
- **Karpathy 2026 evolution** (Anthropic, 2026-05-19): the same author who coined *vibe coding* explicitly retired the term in favor of *agentic engineering* — strategy work should follow the same trajectory away from "let the model decide" toward "the model is one bounded contributor in a verified pipeline."
