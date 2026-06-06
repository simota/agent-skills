Purpose: Track strategic execution after Helm delivers a plan. Use this for assumption monitoring, drift detection, health reporting, and OKR cascade design.

## Contents
- Monitoring workflow
- Assumption states and alerts
- Alignment score
- Health report template

# Strategy Monitoring

This absorbed the former Compass capability. Use it after Helm produces a roadmap, simulation, or strategic recommendation.

## Workflow

`ANCHOR -> TRACK -> ALERT -> CASCADE`

| Phase | Goal | Key actions |
|---|---|---|
| `ANCHOR` | Establish the baseline | Map assumptions to KPIs, define thresholds, capture the starting state |
| `TRACK` | Observe execution and assumptions | Compare actuals vs targets, check milestone progress, review assumption validity |
| `ALERT` | Detect drift early | Trigger WATCH/BREACH states and health alerts |
| `CASCADE` | Connect strategy to work | Translate strategy into company, team, and individual OKRs |

## Assumption Monitoring

### Assumption -> Metric Mapping

```markdown
| Assumption | Metric | Threshold | Status |
|-----------|--------|-----------|--------|
| "Market grows 15%/yr" | Industry revenue data | <10% = WATCH, <5% = BREACH | VALID |
| "Users prefer mobile" | Mobile usage % | <50% = WATCH | VALID |
| "Competitor doesn't enter" | Competitor announcements | Any entry = BREACH | VALID |
```

### Assumption States

```text
VALID -> WATCH -> BREACH
```

| State | Meaning | Action |
|---|---|---|
| `VALID` | Assumption still holds | Continue as planned |
| `WATCH` | Early warning threshold crossed | Prepare a contingency |
| `BREACH` | Assumption no longer holds | Trigger strategy revision or Magi escalation |

## Alert Levels

| Level | Trigger | Response |
|---|---|---|
| `GREEN` | All KPIs on track and assumptions valid | Continue monitoring |
| `YELLOW` | `1-2` KPIs miss by `<20%`, or an assumption is in WATCH | Investigate and prepare mitigation |
| `RED` | Major KPI miss `>20%`, or an assumption breaches | Escalate to Magi |
| `BLACK` | Multiple breaches or core strategy invalidated | Rebuild the strategy |

## OKR Cascade

### Top-Down Translation

```text
Strategy -> Company Objective -> Company KR -> Team OKR -> Individual KR
```

Example:

```text
Company Objective: Be the market leader in X
  -> Revenue KR
  -> NPS KR
  -> Retention KR
```

### Alignment Score

```text
Alignment = KRs with a clear parent link / Total KRs

Target: >80%
Warning: <60%
```

Use low alignment as a sign of orphan work, weak ownership, or strategic drift.

## Strategy Health Report

```markdown
## Strategy Health Report — [Period]

### Overall Status: [GREEN / YELLOW / RED / BLACK]

### KPI Dashboard
| KPI | Target | Actual | Trend | Status |
|-----|--------|--------|-------|--------|
| [KPI] | [target] | [actual] | [↑↓→] | [GREEN/YELLOW/RED] |

### Assumption Monitor
| Assumption | Status | Last Checked | Notes |
|-----------|--------|-------------|-------|
| [assumption] | [VALID/WATCH/BREACH] | [date] | [context] |

### Drift Analysis
- Strategy drift score: [0-100]
- Areas of concern: [list]
- Recommended actions: [list]

### Next Review: [date]
```

## Integration Rules

| Signal | Use |
|---|---|
| Repeated WATCH states | tighten monitoring cadence |
| Any BREACH on a core assumption | reopen the strategy in Helm or escalate to Magi |
| Alignment `<60%` | re-cascade strategy into OKRs |
| Health `RED/BLACK` | treat the roadmap as stale until reviewed |
