# Output Templates

**Purpose:** Report formats for Rank deliverables.
**Read when:** Producing final output in PRESENT phase.

---

## Priority Ranking Report (FULL mode)

```markdown
# Priority Ranking: [Context]

## Summary
- **Item count:** [N]
- **Frameworks used:** [Framework 1], [Framework 2]
- **Cross-framework correlation:** ρ = [value] ([Strong/Moderate/Weak])
- **Overall confidence:** [HIGH/MEDIUM/LOW]

## Ranked List

| Rank | Item | ICE | RICE | Final Score | Confidence | Action |
|------|------|-----|------|-------------|------------|--------|
| 1 | [name] | [score] | [score] | [combined] | [H/M/L] | [next step] |

## Score Rationale

### #1: [Item Name]
- **Impact:** [score] — [rationale]
- **Effort:** [score] — [rationale]
- **Confidence:** [score] — [data source]

## Sensitivity Analysis
[Which rankings are stable vs fragile]

## Bias Report
- **Detected bias:** [list with evidence]
- **Corrective measures:** [what was adjusted]

## Recommended Next Steps
| Priority | Item | Route To | Reason |
|----------|------|----------|--------|
| P0 | [top item] | Sherpa | Decompose for immediate execution |
```

---

## Quick Rank Report (QUICK mode)

```markdown
# Quick Rank: [Context]

| Rank | Item | ICE Score | Rationale |
|------|------|-----------|-----------|
| 1 | [name] | [I×C×E = score] | [1-line reason] |

**Note:** Single framework. FULL mode is recommended for important decisions.
```

---

## Batch Triage Report (BATCH mode)

```markdown
# Backlog Triage: [Context]

## MoSCoW Classification

### Must ([N] items, [X]% of estimated effort)
| Item | RICE Score | Effort | Action |
|------|-----------|--------|--------|

### Should ([N] items, [X]%)
| Item | RICE Score | Effort | Action |
|------|-----------|--------|--------|

### Could ([N] items, [X]%)
[list]

### Won't (this iteration)
[list with reason for exclusion]

## Top-5 Must Items (RICE Ranked)
[detailed ranking of Must items]
```
