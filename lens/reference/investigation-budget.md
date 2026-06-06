# Investigation Budget Reference

## Codebase Size Classification

| Size | LOC | Typical Structure |
|------|-----|-------------------|
| Small | <5K | Single module/app |
| Medium | 5K-50K | Multi-module app |
| Large | 50K-500K | Monolith or multi-service |
| XLarge | 500K+ | Monorepo, enterprise |

## Budget Allocation by Size

### Small (<5K LOC)
- SCOPE: 1 pass, ≤5 min equivalent
- SURVEY: Depth 2 (entry points + direct dependencies)
- TRACE: Max 3 execution chains
- Total iterations: ≤2

### Medium (5K-50K LOC)
- SCOPE: 1-2 passes, boundary identification first
- SURVEY: Depth 3 (entry + deps + cross-module)
- TRACE: Max 5 execution chains
- Total iterations: ≤3

### Large (50K-500K LOC)
- SCOPE: 2+ passes, boundary-first approach mandatory
- SURVEY: Depth 4+ (progressive disclosure)
- TRACE: Max 8 execution chains, prioritize critical path
- Total iterations: ≤4
- Trigger: Ripple co-use recommended when affected services ≥3

### XLarge (500K+ LOC)
- SCOPE: Component-level decomposition required
- SURVEY: Per-component deep dive, cross-component shallow
- TRACE: Max 10 chains, strict path prioritization
- Total iterations: ≤5
- Trigger: Sherpa decomposition mandatory

## Context Budget Management

- Track token consumption per phase
- Abandon TRACE if >60% of context budget consumed in SCOPE+SURVEY
- Summarize findings before deep-diving (avoid context eviction of early findings)

## Escalation on Budget Exhaustion

1. Summarize current findings
2. Identify remaining unknowns
3. Handoff to Scout (if bug suspected) or Sherpa (if decomposition needed)
