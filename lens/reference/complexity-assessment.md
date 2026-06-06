# Complexity Assessment Reference

Concrete workflow, threshold tables, and hotspot ranking methodology for cognitive complexity assessment.

## Step 1: Static Metrics Collection

| Metric | Low Risk | Medium Risk | High Risk | Source |
|--------|----------|-------------|-----------|--------|
| Cognitive Complexity | ≤15 | 16-25 | >25 | SonarSource |
| Cyclomatic Complexity | ≤10 | 11-20 | >20 | McCabe |
| Parameters per function | ≤4 | 5-6 | >6 | Clean Code |
| Function length (LOC) | ≤30 | 31-60 | >60 | Industry consensus |
| Nesting depth | ≤3 | 4-5 | >5 | SonarSource |

## Step 2: Behavioral Metrics (when available)

- **NRevisit** (rs=0.91-0.99, strong correlation with cognitive load) [Source: IEEE TSE]
  - Low risk: ≤3 revisits
  - Medium risk: 4-6 revisits
  - High risk: >6 revisits
- **Time-to-understand estimate**: LOC × complexity_factor (0.5-2.0)
- **Review comment density**: locations with concentrated comments/review notes are hotspot candidates

## Step 3: Hotspot Ranking

1. Fetch change frequency:
   ```bash
   git log --format='%H' --since='6 months ago' -- {file} | wc -l
   ```
2. Hotspot score = change frequency × complexity score
3. Report top 10 hotspots

| Change Frequency (monthly) | Low Risk | Medium Risk | High Risk |
|---------------------------|----------|-------------|-----------|
| Commits per month | ≤5 | 6-15 | >15 |
| Hotspot rank | Bottom 80% | Top 20% | Top 5% |

## Step 4: Comprehension Debt Assessment

Estimating AI-generated code ratio:
- Presence of Co-authored-by trailers (Copilot, Claude, etc.)
- Bulk line-change patterns (100+ lines added in a single commit)
- Formulaic commit messages

Comprehension debt risk determination:

| AI Generated Rate | Review Rate | Risk Level |
|-------------------|-------------|------------|
| <30% | any | LOW |
| 30-60% | ≥0.5 | MEDIUM |
| 30-60% | <0.5 | HIGH |
| >60% | ≥0.3 | HIGH |
| >60% | <0.3 | CRITICAL |

## Assessment Output Template

```markdown
## Complexity Assessment

### Summary
- Files analyzed: N
- High-risk functions: N
- Hotspots identified: N
- Comprehension debt risk: [LOW | MEDIUM | HIGH | CRITICAL]

### Top Hotspots
| Rank | File:Function | Cognitive | Cyclomatic | Changes/mo | Score |
|------|---------------|-----------|------------|------------|-------|

### Recommendations
- [Refactor candidates for Zen]
- [Test coverage gaps for Radar]
- [Architecture concerns for Atlas]
```
