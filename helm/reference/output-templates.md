# Output Templates Reference — Helm

Purpose: Provide canonical output skeletons for strategy work without forcing unnecessary sections into every engagement.

## Contents

- Strategic roadmap template
- KPI forecast template
- Risk matrix template
- M&A / exit template
- Executive summary template

## Template 1: Strategic Roadmap

Use for the default full-package output.

```markdown
## 経営シミュレーションレポート

### Executive Summary
- one-line conclusion
- recommended strategy
- expected impact
- biggest risk

### 現状診断
- SWOT summary
- PESTLE summary when relevant
- Porter summary when relevant

### 推奨戦略
| Option | Expected ROI | Risk | Execution Difficulty | Investment | Recommendation |
|--------|--------------|------|----------------------|------------|----------------|
| [...] | X% | Low/Med/High | Low/Med/High | ¥Xm | ★★★ |

### シミュレーション結果
#### 前提仮定
| Parameter | Value | Reason |
|-----------|-------|--------|
| [...] | [...] | [...] |

#### KPI推移
| KPI | Current | T+1 | T+2 | T+3 | T+4 |
|-----|---------|-----|-----|-----|-----|
| [...] | [...] | [...] | [...] | [...] | [...] |

#### 3シナリオ比較
| Metric | Baseline | Optimistic (+X%) | Pessimistic (-X%) |
|--------|----------|------------------|-------------------|
| [...] | [...] | [...] | [...] |

### リスク・機会マトリクス
| Item | Probability | Impact | Priority | Mitigation / Action | Owner |
|------|-------------|--------|----------|---------------------|-------|
| [...] | High/Med/Low | High/Med/Low | [...] | [...] | [...] |

### 実行ロードマップ
#### Phase 1 (0-6 months)
- [ ] action
- success metric

#### Phase 2 (6-18 months)
- [ ] action

#### Phase 3 (18+ months)
- [ ] action

### 前提条件・制約事項
- assumption caveats
- data gaps
- directional disclaimer if long-term

### 次のアクション
| Action | Recommended Agent | Priority |
|--------|-------------------|----------|
| Go/No-Go decision | Magi | High |
| Documentation | Scribe | Medium |
| Task breakdown | Sherpa | Medium |
| Visualization | Canvas | Low |
```

## Template 2: KPI Forecast Table

Use for short-horizon executive tracking.

```markdown
# KPI Forecast — [...]

| KPI | Current | 3 Months | 6 Months | 12 Months | 24 Months |
|-----|---------|----------|----------|-----------|-----------|
| MRR | [...] | [...] | [...] | [...] | [...] |
| ARR | [...] | [...] | [...] | [...] | [...] |
| Customer Count | [...] | [...] | [...] | [...] | [...] |
| MRR Churn | [...] | [...] | [...] | [...] | [...] |
| LTV:CAC | [...] | [...] | [...] | [...] | [...] |
| CAC Payback | [...] | [...] | [...] | [...] | [...] |
| Gross Margin | [...] | [...] | [...] | [...] | [...] |
| Monthly Cash Flow | [...] | [...] | [...] | [...] | [...] |
| Runway | [...] | - | - | - | - |

## Scenario Comparison (12 Months)
| Metric | Baseline | Optimistic (+X%) | Pessimistic (-X%) |
|--------|----------|------------------|-------------------|
| [...] | [...] | [...] | [...] |

## Sensitivity Analysis
| Variable | -20% | Base | +20% | Sensitivity |
|----------|------|------|------|-------------|
| [...] | [...] | [...] | [...] | High/Med/Low |
```

## Template 3: Risk Matrix

Use when the main need is risk and opportunity management.

```markdown
# Risk and Opportunity Matrix — [...]

## Risks
| ID | Risk | Probability | Impact | Priority | Mitigation | KPI / Threshold | Owner |
|----|------|-------------|--------|----------|------------|-----------------|-------|
| R1 | [...] | High | High | Highest | [...] | [...] | [...] |

## Opportunities
| ID | Opportunity | Probability | Impact | Conditions | Recommended Action | Deadline |
|----|-------------|-------------|--------|------------|--------------------|----------|
| O1 | [...] | High | High | [...] | [...] | [...] |
```

## Template 4: M&A / Exit Evaluation

```markdown
# M&A / Exit Evaluation — [...]

## Executive Summary
| Field | Value |
|-------|-------|
| Objective | [...] |
| Target | [...] |
| Recommended Action | [...] |
| Decision Deadline | [...] |

## Valuation
| Method | Value | Rationale |
|--------|-------|-----------|
| Revenue Multiple | [...] | [...] |
| EBITDA Multiple | [...] | [...] |
| DCF | [...] | [...] |
| Comparable Transactions | [...] | [...] |

## Option Comparison
| Option | Estimated Value | Probability | Timeline | Recommendation |
|--------|-----------------|-------------|----------|----------------|
| [...] | [...] | X% | X years | ★★★ |
```

## Template 5: Executive Summary

Use for leadership review when one page is enough.

```markdown
# Strategic Summary — [...]

## Current Snapshot
| Metric | Current | Vs Previous | Vs Target | Status |
|--------|---------|-------------|-----------|--------|
| MRR | ¥Xm | +X% | X% | 🟢/🟡/🔴 |
| Customers | X | +X | X% | 🟢/🟡/🔴 |
| Churn | X% | ±X% | X% | 🟢/🟡/🔴 |
| Runway | X months | - | >18 months | 🟢/🟡/🔴 |

## Top Actions This Period
- [...]
- [...]

## Risk Signals
| Risk | Status | Response |
|------|--------|----------|
| [...] | 🔴/🟡 | [...] |

## 12-Month Landing View
| Scenario | MRR | Probability | Conditions |
|----------|-----|-------------|------------|
| Optimistic | ¥Xm | X% | [...] |
| Baseline | ¥Xm | X% | [...] |
| Pessimistic | ¥Xm | X% | [...] |
```
