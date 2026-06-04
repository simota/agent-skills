# Code Review Effectiveness & Metrics

> Review effectiveness measurement, cognitive load and optimal PR size, KPI design, and reviewer fatigue research.

## 1. Key Metrics for Review Effectiveness

### Quality Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Defect Escape Rate** | Percentage of bugs found after passing review | < 5% |
| **Review Coverage** | Percentage of code changes reviewed | > 95% |
| **False Positive Rate** | Percentage of incorrect findings | < 20% |
| **Actionable Finding Rate** | Percentage of findings that led to actual fixes | > 60% |
| **Severity Accuracy** | Validity of severity classifications | > 80% |

### Efficiency Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Review Turnaround Time** | Time from PR creation to review completion | < 24 hours |
| **Time to First Comment** | Time from PR creation to first comment | < 4 hours |
| **Review Iterations** | Number of round-trips until approval | ≤ 2 |
| **PR Rejection Rate** | Percentage of rejected PRs | 10–20% |
| **Lines Reviewed per Hour** | Lines of code reviewed per hour | 200–400 LOC |

### Process Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **PR Size** | Lines changed (additions + deletions) | < 400 LOC |
| **Comment Density** | Comments per lines changed | Appropriate (neither too many nor too few) |
| **Review Participation** | Percentage of team members participating in reviews | > 80% |
| **Knowledge Distribution** | Evenness of review assignment distribution | Gini ≤ 0.4 |

---

## 2. Cognitive Load and Optimal PR Size

### Cisco Study + 2025 LinearB Analysis

```
Cisco Study (findings confirmed over time):
  - 200-400 LOC is the optimal review size
  - 60-90 minutes is the optimal session duration
  - Bug detection rate drops sharply beyond 400 LOC/hour

LinearB 2025 (6.1M PRs, 3,000 teams analyzed):
  - Elite team average: 219 LOC/PR
  - This aligns with Cisco's optimal range
```

### Cognitive Load Cliff

```
Relationship between lines reviewed and defect detection rate:

LOC/hr  | Detection rate | State
--------|---------------|------
< 200   | High          | Optimal zone
200-400 | Medium-High   | Recommended range
400-450 | Sharp decline | Warning zone
> 450   | Only 13%      | 87% of defects missed

Cause: Working memory capacity is ~4 chunks → cognitive capacity exceeded
```

### PR Size Guidelines

| Size | LOC | Review depth | Recommended action |
|------|-----|-------------|-------------------|
| **Small** | < 100 | Deep | Review immediately |
| **Medium** | 100–400 | Adequate | Standard review |
| **Large** | 400–1000 | Declining | Recommend splitting |
| **XL** | > 1000 | Perfunctory risk | Strongly recommend splitting |

---

## 3. Reviewer Fatigue Research

### Causes and Effects of Fatigue

| Cause | Effect | Research finding |
|-------|--------|-----------------|
| **Decision Fatigue** | Declining judgment quality in later portions | Short/large/complex changes get skipped |
| **Context Switching** | Fragmented concentration | Review efficiency drops 30% |
| **Review Anxiety** | Fear of criticism / pressure | Demonstrated in Springer 2024 study |
| **High PR Volume** | Burnout | Root cause of the Heroing pattern |

### Fatigue Mitigation

```
Mitigation by Judge:
  1. Automated review handles basic checks
     → Humans focus on higher-order judgment
  2. Severity classification clarifies priorities
     → No need to "review everything"
  3. False positive filtering
     → Noise reduction lowers review burden
  4. Automated PR summary generation
     → Accelerates context comprehension

Organizational mitigation:
  1. Introduce review rotation
  2. Limit sessions to 60 minutes
  3. Foster a culture of small PRs
  4. Visualize and balance review load
```

---

## 4. DX Core 4 Framework

### Integrated Developer Productivity Measurement

```
DX Core 4 = DORA + SPACE + DevEx integrated

4 axes:
  Speed        — Deploy frequency, lead time
  Effectiveness — Developer experience, flow state
  Quality      — Change failure rate, defect density
  Impact       — Business outcomes

Code review sits at the intersection of Quality and Effectiveness:
  - Quality gate function (Quality)
  - Design that does not disrupt developer flow (Effectiveness)
```

---

## 5. Judge's Metrics Application

### Auto-Measurable Metrics

```
Metrics Judge can measure automatically:
  □ PR size (LOC) → warn on large PRs
  □ Finding count and severity distribution
  □ Estimated false positive rate (pattern-based)
  □ Intent alignment score
  □ Consistency issue count
  □ Test quality score

Metrics Judge cannot measure (organization-level):
  × Review turnaround time
  × Defect escape rate
  × Review participation rate
  × Fix adoption rate
```

### PR Size Warning Rules

```
PR size warnings in Judge reports:

if (totalLOC > 1000):
  ⚠️ "PR exceeds 1000 LOC.
      Review quality may degrade significantly.
      Strongly recommend splitting."

elif (totalLOC > 400):
  ℹ️ "PR exceeds 400 LOC.
      Consider splitting to reduce
      reviewer cognitive load."
```

**Source:** [PropelCode: Measuring Code Review Effectiveness](https://www.propelcode.ai/learn/measuring-code-review-effectiveness) · [Rishi Baldawa: Cognitive Load Cliff in Code Review](https://rishi.baldawa.com/posts/pr-throughput/cognitive-load-cliff/) · [Arxiv: Rethinking Code Review Workflows with LLM](https://arxiv.org/html/2505.16339v1) · [Springer: Code Review Anxiety](https://link.springer.com/article/10.1007/s10664-024-10550-9) · [Qodo: Code Quality Metrics 2026](https://www.qodo.ai/blog/code-quality-metrics-2026/)

---

## 6. Adversarial / Multi-Agent Review ROI

When deciding whether to add an adversarial-reviewer sub-agent (a second agent prompted to aggressively challenge the first pass), budget against a measured baseline rather than assuming "more review is free":

| Effect of adding an adversarial reviewer | Measured delta |
|------------------------------------------|----------------|
| Accuracy | **+6%** |
| Token consumption | **+32%** |
| Latency | **+72%** |

Two corollaries from the same deployment:
- **Don't downgrade the reviewer to save cost.** Swapping the adversarial reviewer to a cheaper model *lost the accuracy gain without recovering meaningful latency* — the review step is where reasoning quality pays off.
- **Reserve adversarial review for high-stakes diffs.** At +72% latency it is not a default for every PR; gate it on risk (money / authz / state-machine / irreversible changes), consistent with the tiered approach Judge already applies.

**Source:** [Anthropic: How Anthropic Enables Self-Service Data Analytics with Claude](https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude)
