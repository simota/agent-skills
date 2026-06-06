# Ecosystem Review Loop

**Purpose:** Health Score model and ecosystem review cadence.
**Read when:** You need scoring, degradation detection, or review timing.

## Contents
- Overview
- Review Cycle Framework
- Review Triggers
- Agent Health Score
- Health Score Calculation Template
- Improvement Queue
- Review Session Templates
- Ecosystem-wide Review
- Integration with SKILL.md

---

## Overview

The ecosystem review loop ensures:
- Consistent quality across all agents
- Early detection of degradation
- Proactive improvement planning
- Sustainable ecosystem growth

---

## Review Cycle Framework

```
    ┌────────────────────────────────────────────┐
    │                                            │
    │    PLAN ──────→ DO ──────→ CHECK ──────→ ACT
    │      ↑                                   │
    │      └───────────────────────────────────┘
    │                  (repeat)
    │
    └─ Continuous ecosystem improvement
```

### PLAN Phase
- Identify agents needing attention
- Prioritize improvement queue
- Define improvement goals and metrics

### DO Phase
- Execute improvements on SKILL.md
- Update reference files
- Verify Nexus integration

### CHECK Phase
- Calculate Health Score after changes
- Validate against quality checklist
- Compare before/after metrics

### ACT Phase
- Document lessons learned
- Update standards if needed
- Feed insights into next PLAN cycle

---

## Review Triggers

| Trigger | Condition | Priority | Action |
|---------|-----------|----------|--------|
| `SCHEDULED` | Weekly periodic review | P2 | Review 5-10 agents by category |
| `ON_AGENT_CREATION` | 7 days after new agent creation | P1 | Full validation of new agent |
| `ON_ECOSYSTEM_CHANGE` | 5+ agents changed | P1 | Cross-ecosystem consistency check |
| `ON_QUALITY_ALERT` | Score < 60 detected | P0 | Immediate attention required |
| `ON_USER_FEEDBACK` | User reports issue with agent | P1 | Targeted investigation |
| `ON_STALE_AGENT` | No activity for 90+ days | P3 | Relevance review |

### Trigger Detection Rules

```yaml
TRIGGER_DETECTION:
  SCHEDULED:
    frequency: "weekly"
    day: "Monday"
    scope: "rotate through categories"

  ON_AGENT_CREATION:
    event: "new SKILL.md committed"
    delay: "7 days"
    action: "full_validation"

  ON_ECOSYSTEM_CHANGE:
    threshold: 5
    window: "7 days"
    scope: "all changed agents + dependencies"
# ...
```

---

## Agent Health Score

### Scoring Formula

```
HEALTH_SCORE = Structure(30%) + Content(25%) + Integration(20%) + Activity(15%) + Freshness(10%)
```

### Score Components

#### Structure (30%)

| Item | Points | Criteria |
|------|--------|----------|
| Frontmatter valid | 6 | name + description present |
| CAPABILITIES_SUMMARY | 6 | HTML comment with 5-10 items |
| Boundaries section | 6 | Always/Ask/Never all present |
| INTERACTION_TRIGGERS | 4 | Table + YAML templates |
| AUTORUN Support | 4 | _AGENT_CONTEXT + _STEP_COMPLETE |
| Nexus Hub Mode | 4 | NEXUS_HANDOFF format |
| **Max** | **30** | |

#### Content (25%)

| Item | Points | Criteria |
|------|--------|----------|
| Clear mission statement | 5 | One sentence, specific outcome |
| Unambiguous boundaries | 5 | No vague terms |
| Complete YAML templates | 5 | Valid syntax, required fields |
| Unique philosophy | 5 | Not copied from other agents |
| Actionable daily process | 5 | Clear, verifiable steps |
| **Max** | **25** | |

#### Integration (20%)

| Item | Points | Criteria |
|------|--------|----------|
| INPUT partners defined | 5 | At least 1 partner |
| OUTPUT partners defined | 5 | At least 1 partner |
| Collaboration patterns | 5 | At least 1 pattern |
| Overlap < 30% | 5 | With all existing agents |
| **Max** | **20** | |

#### Activity (15%)

| Item | Points | Criteria |
|------|--------|----------|
| Used in last 30 days | 5 | Evidence of invocation |
| No reported issues | 5 | No open bugs/complaints |
| Positive feedback | 5 | User satisfaction signals |
| **Max** | **15** | |

#### Freshness (10%)

| Item | Points | Criteria |
|------|--------|----------|
| Updated within 90 days | 4 | Last modification date |
| References current patterns | 3 | No deprecated practices |
| Ecosystem-aligned | 3 | Consistent with current standards |
| **Max** | **10** | |

### Score Interpretation

| Score | Grade | Status | Action |
|-------|-------|--------|--------|
| 90-100 | A | Excellent | No action needed |
| 80-89 | B | Good | Minor improvements optional |
| 70-79 | C | Acceptable | Schedule improvements |
| 60-69 | D | At risk | Priority queue |
| <60 | F | Critical | Immediate attention |

---

## Health Score Calculation Template

```yaml
HEALTH_SCORE_CALCULATION:
  agent: "[Agent Name]"
  date: "[YYYY-MM-DD]"

  structure:  # Max 30
    frontmatter: 0  # 0-6
    capabilities_summary: 0  # 0-6
    boundaries: 0  # 0-6
    interaction_triggers: 0  # 0-4
    autorun_support: 0  # 0-4
    nexus_hub_mode: 0  # 0-4
    subtotal: 0

  content:  # Max 25
    mission_statement: 0  # 0-5
# ...
```

---

## Improvement Queue

### Queue Structure

```
IMPROVEMENT_QUEUE
├── P0 (Critical) ─── Security issues, broken agents
│                     Response: < 24 hours
│
├── P1 (High) ─────── Score < 60, missing required sections
│                     Response: < 1 week
│
├── P2 (Medium) ───── Score 60-70, overlap issues
│                     Response: < 2 weeks
│
└── P3 (Low) ──────── Score 70-80, enhancement opportunities
                      Response: < 1 month
```

### Queue Management

```yaml
QUEUE_MANAGEMENT:
  p0_critical:
    criteria:
      - "Security vulnerability in agent logic"
      - "Agent completely non-functional"
      - "Blocking other agents"
    response_time: "< 24 hours"
    escalation: "Immediate Architect attention"

  p1_high:
    criteria:
      - "Health score < 60"
      - "Missing required sections"
      - "New agent validation failed"
    response_time: "< 1 week"
# ...
```

---

## Review Session Templates

### Weekly Review Session

```markdown
## Weekly Review Session: [YYYY-MM-DD]

### Trigger
- [ ] SCHEDULED (weekly rotation)
- [ ] Other: _____________

### Scope
**Category being reviewed:** [Category Name]
**Agents in scope:** [List of agents]

### Health Scores

| Agent | Structure | Content | Integration | Activity | Freshness | Total | Grade |
|-------|-----------|---------|-------------|----------|-----------|-------|-------|
| [Agent1] | /30 | /25 | /20 | /15 | /10 | /100 | |
...
```

### Single Agent Review

```markdown
## Agent Review: [Agent Name]

### Trigger
- [ ] ON_AGENT_CREATION (7-day validation)
- [ ] ON_QUALITY_ALERT (score < 60)
- [ ] ON_USER_FEEDBACK
- [ ] ON_STALE_AGENT
- [ ] Other: _____________

### Health Score Breakdown

**Structure (30%):** [X/30]
- Frontmatter: [X/6]
- CAPABILITIES_SUMMARY: [X/6]
- Boundaries: [X/6]
...
```

---

## Ecosystem-wide Review

### Cross-Ecosystem Consistency Check

```yaml
CONSISTENCY_CHECK:
  categories:
    naming:
      check: "All agents follow naming conventions"
      reference: "reference/naming-conventions.md"

    structure:
      check: "All agents have required sections"
      reference: "reference/validation-checklist.md"

    collaboration:
      check: "Collaboration patterns are consistent"
      reference: "reference/nexus-integration.md"

    overlap:
# ...
```

### Ecosystem Health Dashboard

```markdown
## Ecosystem Health: [YYYY-MM-DD]

### Summary
- **Total Agents:** [count]
- **Average Health Score:** [X/100]
- **Agents at Risk (Score < 70):** [count]

### Grade Distribution
| Grade | Count | Percentage |
|-------|-------|------------|
| A (90-100) | | |
| B (80-89) | | |
| C (70-79) | | |
| D (60-69) | | |
| F (<60) | | |
...
```

---

## Integration with SKILL.md

Reference in SKILL.md:

```markdown
## ECOSYSTEM REVIEW LOOP

Continuous improvement cycle. See `reference/review-loop.md` for details.

**Health Score Formula:**
```
HEALTH_SCORE = Structure(30%) + Content(25%) + Integration(20%) + Activity(15%) + Freshness(10%)
```

**Review Triggers:**
- SCHEDULED: Weekly category rotation
- ON_AGENT_CREATION: 7-day post-creation validation
- ON_QUALITY_ALERT: Immediate when score < 60

**Priority Queue:**
- P0: Critical - < 24 hours
- P1: High - < 1 week
- P2: Medium - < 2 weeks
- P3: Low - < 1 month
```
