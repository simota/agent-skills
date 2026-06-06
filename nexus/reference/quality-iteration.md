# Quality Iteration (absorbed from Hone)

**Purpose:** PDCA loop for iterative quality improvement after initial delivery.
**Read when:** Judge feedback or user requests require iterative polishing.

PDCA-based quality improvement methodology. Previously a standalone agent (Hone), now integrated as a Nexus orchestration pattern.

---

## When to Apply

Use this pattern when Nexus needs to iteratively improve output quality:
- After initial implementation, quality gate fails
- Judge reports quality issues requiring multiple specialist fixes
- User requests "polish" or "improve quality" of existing output

---

## PDCA Cycle

```
PLAN(Diagnose) → DO(Execute) → CHECK(Measure) → ACT(Learn) → repeat or terminate
```

### PLAN: Diagnose quality gaps
- Run Judge for code review findings
- Measure current baseline (see UQS below)
- Identify highest-impact improvement areas
- Select specialist agents for fixes

### DO: Execute improvements
- Route to specialist agents in order (see coordination below)
- Each agent addresses specific quality gap

### CHECK: Measure improvement
- Re-run Judge / relevant quality checks
- Calculate new UQS score
- Compute delta from previous cycle

### ACT: Learn and decide
- If target met → terminate
- If diminishing returns → terminate
- Otherwise → next cycle with remaining gaps

---

## Unified Quality Score (UQS)

| Agent | Normalization | Weight |
|-------|--------------|--------|
| Judge | `100 - (CRIT×25 + HIGH×15 + MED×5 + LOW×2)` | 0.25 |
| Consistency | `100 - (HIGH×15 + MED×5 + LOW×2)` | 0.10 |
| Test Quality | `isolation×0.25 + flaky×0.25 + edge×0.20 + mock×0.15 + read×0.15` | 0.10 |
| Zen | `max(0, 100 - (avgCC - 10) × 5)` | 0.15 |
| Radar | `coverage%` | 0.20 |
| Warden | `avg(dimensions) / 3 × 100` | 0.12 |
| Quill | `pass_rate × 100` | 0.08 |

`UQS = Σ (normalized_score_i × weight_i)`

**Interpretation**: 90-100 Excellent · 80-89 Good · 70-79 Acceptable · 60-69 Fair · <60 Poor

---

## Agent Coordination Order

```
Judge(detect) → Builder(fix critical) → Sentinel(if security) → Zen(simplify) → Radar(add tests) → Quill(document) → Warden(UX, if UI)
```

| Quality Gap | Primary Agent | Skip If |
|-------------|--------------|---------|
| Bugs detected | Judge → Builder | No bugs |
| High complexity | Zen | avgCC < 10 |
| Low coverage | Radar | coverage > 80% |
| Poor docs | Quill | docs complete |
| UX violations | Warden → Palette | Not UI |

---

## Termination Conditions (Priority Order)

1. All quality targets achieved (UQS >= target)
2. Diminishing returns (delta < 5% for 2 consecutive cycles)
3. Maximum cycles reached (default: 3)
4. User manual stop

---

## Cycle Modes

| Mode | Max Cycles | Target UQS | Use Case |
|------|-----------|-----------|----------|
| QUICK | 2 | 70 | Fast turnaround |
| STANDARD | 3 | 80 | Balanced (default) |
| INTENSIVE | 5 | 90 | High-quality requirements |
