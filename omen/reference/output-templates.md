# Output Templates

**Purpose:** Report formats for Omen deliverables.
**Read when:** Producing final output in FORTIFY phase.

---

## Pre-mortem Report (DEEP mode)

```markdown
# Pre-mortem Analysis: [Subject]

## Scope
- **Target:** [name and overview of the subject being analyzed]
- **Assumptions:** [key assumptions]
- **Constraints:** [constraints]
- **Stakeholders:** [affected parties]

## FMEA Table

| # | Component | Failure Mode | Effect | S | O | D | RPN | Category | Mitigation |
|---|-----------|-------------|--------|---|---|---|-----|----------|------------|
| 1 | [name] | [how] | [impact] | [1-10] | [1-10] | [1-10] | [calc] | [cat] | [action] |

## Critical Failures (RPN > 200)

### FM-[N]: [Failure Mode Name]
- **RPN:** [score] (S:[s] × O:[o] × D:[d])
- **Scenario:** [concrete failure story]
- **Propagation Path:** [A → B → C chain]
- **Mitigation:**
  - Detection: [how to find it]
  - Prevention: [how to prevent it]
  - Recovery: [how to recover if it happens]
- **Residual Risk:** [RPN after mitigation]

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

### Detection
- [ ] [monitoring/alerting action]
- [ ] [test case addition]
- [ ] [review checklist item]

### Prevention
- [ ] [design change]
- [ ] [validation addition]
- [ ] [process change]

### Recovery
- [ ] [rollback procedure]
- [ ] [data recovery plan]
- [ ] [communication plan]

### Verification
- Pre-mitigation RPN: [original]
- Post-mitigation RPN: [reduced] (target S:[s] × O:[o] × D:[d])
- Residual risk accepted: [yes/no, with rationale]
```
