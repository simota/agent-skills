# Change Hotspot Analysis

Reference for Lens's `hotspot` recipe. Identify "hot+complex" files via change frequency × cognitive complexity. Pioneered by Adam Tornhill ("Your Code as a Crime Scene", 2015).

---

## 1. Methodology

```
Hotspot Score = Change Frequency × Cognitive Complexity
```

Files high in BOTH dimensions are top refactor candidates:
- High churn = unstable, frequently broken, ROI of refactor is high
- High complexity = expensive to maintain, error-prone
- Combination = compounding cost

---

## 2. Data Collection

### Change frequency
```bash
# Count commits per file in last 6 months
git log --since="6 months ago" --name-only --pretty=format: \
  | sort | uniq -c | sort -rn | head -20
```

Output format:
```
  47 src/services/UserService.ts
  31 src/api/handlers/order.ts
  28 src/components/Dashboard.tsx
  ...
```

### Cognitive complexity
Per language:
- TS/JS: SonarSource `eslint-plugin-sonarjs` rule `cognitive-complexity`
- Python: `radon cc`
- Go: `gocyclo`
- Java: SonarQube
- Rust: `cargo-geiger` (related)

```bash
# TS example: per-file complexity report
npx eslint --rule '{"sonarjs/cognitive-complexity": ["error", 0]}' \
  --no-eslintrc src/ --format json | jq '...'
```

### Bug correlation (optional, strengthens signal)
```bash
git log --since="6 months ago" --grep='fix\|bug\|hotfix' \
  --name-only --pretty=format: | sort | uniq -c | sort -rn
```

Files with high bug-fix touch rate × high churn = highest priority.

---

## 3. Hotspot Categorization

| Churn | Complexity | Category | Action |
|---|---|---|---|
| HIGH (top 20%) | HIGH (>15) | **CRITICAL** | Immediate refactor priority |
| HIGH | MEDIUM (5-15) | Hot but manageable | Monitor, refactor on next major touch |
| HIGH | LOW (<5) | Hot, simple | Likely correct (high churn = active feature, complexity controlled) |
| LOW | HIGH | Cold legacy | Low ROI to touch unless bug appears |
| LOW | LOW | Stable | Leave alone |

---

## 4. Refactor Prioritization

For CRITICAL hotspots:

```yaml
file: src/services/UserService.ts
metrics:
  commits_6mo: 47          # high churn
  cognitive_complexity: 28  # high
  bug_fix_commits: 12       # 25% of changes are bug fixes
  authors: 8                # broad ownership

risk_indicators:
  - "Fan-in: 23 (god module)"
  - "Last refactor: never (lifespan 4 years)"
  - "Test coverage: 38%"

refactor_plan:
  - Extract authentication concerns → AuthService
  - Split user CRUD from user query
  - Add unit test coverage for top-3 most-called methods
  - Estimated effort: 3-5 days
  - Estimated risk reduction: 60% bug-rate decrease
```

---

## 5. Visualization

### Heatmap output
```
Hotspot Map (size = LOC, color = complexity, brightness = churn)

█████████ UserService.ts        [CRITICAL]   47 commits, complexity 28
███████   OrderHandler.ts       [CRITICAL]   31 commits, complexity 22
█████     Dashboard.tsx         [HOT-MED]    28 commits, complexity 12
████      ReportGenerator.ts    [HOT-MED]    22 commits, complexity 14
███       PaymentProcessor.ts   [COLD-HIGH]   3 commits, complexity 31  ← bug-prone but stable
```

### Mermaid heatmap
```mermaid
graph TD
  classDef critical fill:#dc2626,color:#fff
  classDef hot fill:#f97316,color:#fff
  classDef cold fill:#9ca3af,color:#fff
  US[UserService.ts]:::critical
  OH[OrderHandler.ts]:::critical
  DB[Dashboard.tsx]:::hot
  PP[PaymentProcessor.ts]:::cold
```

---

## 6. Time-Window Sensitivity

| Window | Insight |
|---|---|
| 1 month | Active development hotspots |
| 6 months (default) | Sustained instability |
| 1 year | Long-term maintenance burden |
| All-time | Total accumulated change |

Run multiple windows to distinguish:
- "Now hot, always was hot" → core component
- "Now hot, was cold" → recent feature; may stabilize
- "Now cold, was hot" → matured area; defer refactor

---

## 7. Author Concentration Cross-Reference

Pair hotspot with bus factor (next recipe `evolution`):
- Hot + bus factor 1 = critical knowledge concentration risk
- Hot + bus factor 5+ = healthy distributed ownership

---

## 8. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Counting auto-generated file changes | Filter `*.lock`, `dist/`, `build/`, generated `*.ts` |
| Equal weight to typo fixes and refactors | Weight by lines changed (`git log --shortstat`) |
| Including merge commits | `--no-merges` flag |
| Single-author bursts skew score | Cross-check with author concentration |
| Treating tests as hotspots | Filter `**/*.test.*` separately |
| Cognitive complexity tool disagreements | Pick one (SonarSource recommended); document choice |
| Complexity threshold too generous | 15 for "high" works for most codebases; tune to project median |

---

## 9. Decision Walkthrough Template

```
Time window: ____ months
Total files analyzed: ____
Auto-generated / vendored excluded: ✓

Top hotspots (CRITICAL):
  1. ____ (commits: ___, complexity: ___, bug-fix %: ___%)
  2. ____ ...

Top hotspots (HOT-MEDIUM):
  ...

Cold but high-complexity (legacy risk):
  ...

Recommended refactor order (ROI-weighted):
  1. ____ (effort: ___ days, risk reduction: ___%)
  2. ____ ...

Cross-references needed:
  □ Bus factor (evolution recipe)
  □ Test coverage data
  □ Recent bug ticket history

Handoff:
  □ Atlas for refactor architecture
  □ Builder for execution
  □ Sweep for orphan-related cleanup
```

---

## 10. References
- Adam Tornhill: "Your Code as a Crime Scene" (Pragmatic, 2015)
- SonarSource Cognitive Complexity white paper
- CodeScene (commercial tool implementing this methodology)
- Microsoft: "Don't Touch My Code" (2009 paper, code stability research)
