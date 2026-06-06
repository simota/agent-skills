# Output Templates

**Purpose:** Report formats for Omen deliverables.
**Read when:** Producing final output in FORTIFY phase.

---

## Pre-mortem Report (DEEP mode)

```markdown
# Pre-mortem Analysis: [Subject]

## Scope
- **対象:** [分析対象の名称と概要]
- **前提:** [主要な前提条件]
- **制約:** [制約事項]
- **利害関係者:** [影響を受ける関係者]

## FMEA Table

| # | Component | Failure Mode | Effect | S | O | D | RPN | Category | Mitigation |
|---|-----------|-------------|--------|---|---|---|-----|----------|------------|
| 1 | [name] | [how] | [impact] | [1-10] | [1-10] | [1-10] | [calc] | [cat] | [action] |

## Critical Failures (RPN > 200)

### FM-[N]: [Failure Mode Name]
- **RPN:** [score] (S:[s] × O:[o] × D:[d])
- **シナリオ:** [具体的な失敗ストーリー]
- **伝播経路:** [A → B → C の連鎖]
- **緩和策:**
  - 検出: [どう見つけるか]
  - 予防: [どう防ぐか]
  - 回復: [起きた場合どう復旧するか]
- **残存リスク:** [緩和後のRPN]

## Risk Distribution

| Level | Count | % |
|-------|-------|---|
| Critical (>200) | [n] | [%] |
| High (100-200) | [n] | [%] |
| Medium (50-99) | [n] | [%] |
| Low (<50) | [n] | [%] |

## Fault Tree (Top Failures)

[Mermaid diagram or ASCII representation]

## Swiss Cheese Analysis

| Defense Layer | Holes Identified | Alignment Risk |
|--------------|-----------------|---------------|
| Design | [weaknesses] | [HIGH/MED/LOW] |
| Process | [weaknesses] | [HIGH/MED/LOW] |
| Monitoring | [weaknesses] | [HIGH/MED/LOW] |
| Recovery | [weaknesses] | [HIGH/MED/LOW] |

## Recommended Next Steps

| Action | Priority | Route To | Reason |
|--------|----------|----------|--------|
| [action] | [P0-P3] | [Agent] | [why] |
```

---

## Quick Risk Report (RAPID mode)

```markdown
# Quick Risk Check: [Subject]

## Top-5 Failure Scenarios

| # | Failure | RPN | S | O | D | Quick Mitigation |
|---|---------|-----|---|---|---|-----------------|
| 1 | [scenario] | [rpn] | [s] | [o] | [d] | [action] |

## Verdict
- **Overall Risk:** [Critical / High / Medium / Low]
- **Release Readiness:** [Block / Conditional / Go]
- **Immediate Actions:** [list]
```

---

## Mitigation Plan Template

```markdown
## Mitigation Plan for FM-[N]

### Detection (見つける)
- [ ] [monitoring/alerting action]
- [ ] [test case addition]
- [ ] [review checklist item]

### Prevention (防ぐ)
- [ ] [design change]
- [ ] [validation addition]
- [ ] [process change]

### Recovery (復旧する)
- [ ] [rollback procedure]
- [ ] [data recovery plan]
- [ ] [communication plan]

### Verification
- Pre-mitigation RPN: [original]
- Post-mitigation RPN: [reduced] (target S:[s] × O:[o] × D:[d])
- Residual risk accepted: [yes/no, with rationale]
```
