# Operational Review Loop

Use for review scheduling and the canonical Health Score rubric (§ Agent Health Score). `reference/enhancement-framework.md` reuses this rubric for IMPROVE prioritization and proposals; it does not define its own.

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

### Scoring Components

```
HEALTH_SCORE = Structure(30%) + Content(25%) + Integration(20%) + Activity(15%) + Freshness(10%)
```

### Structure Score (30%)

| Check Item | Points | Criteria |
|-----------|--------|----------|
| SKILL.md exists and well-formed | 10 | Valid frontmatter, owned outcome and boundaries present |
| Reference delivery | 8 | Every needed reference is reachable at its trigger; zero is valid when none is needed |
| Handoff contract delivery | 4 | Applicable shared envelope and any unique payload are reachable; no dedicated duplicate file required |
| Standard sections complete | 5 | Required sections per `_templates/SKILL_TEMPLATE.md` and current lint |
| Entrypoint size | 3 | Under 500 lines; heavy detail remains on demand, without a size minimum |

**Maximum: 30 points**

### Content Score (25%)

| Check Item | Points | Criteria |
|-----------|--------|----------|
| CAPABILITIES_SUMMARY complete | 5 | All capabilities listed for Nexus routing |
| Boundaries well-defined | 5 | Explicit mandatory actions, approval gates and prohibitions; no quota |
| Confirmation coverage | 5 | Required approval gates are actionable; templates only when their format is needed |
| Domain expertise depth | 5 | Reference files contain actionable knowledge |
| Workflow defined | 5 | Inputs, decisions and completion checks are executable |

**Maximum: 25 points**

### Integration Score (20%)

| Check Item | Points | Criteria |
|-----------|--------|----------|
| BIDIRECTIONAL_PARTNERS defined | 5 | Clear INPUT and OUTPUT partners listed |
| Collaboration patterns | 5 | Declared partner flows have clear ownership; no diagram quota |
| Handoff templates complete | 5 | Both inbound and outbound handoffs |
| AUTORUN support | 3 | _AGENT_CONTEXT and _STEP_COMPLETE defined |
| Nexus Hub Mode | 2 | NEXUS_HANDOFF format defined |

**Maximum: 20 points**

### Activity Score (15%)

| Check Item | Points | Criteria |
|-----------|--------|----------|
| Operational logging | 5 | Relevant logging requirements delivered through the operational contract |
| Journal section | 5 | Agent journal with clear guidelines |
| Git guidelines reference | 5 | Canonical `_common/GIT_GUIDELINES.md` resolves |

**Maximum: 15 points**

### Freshness Score (10%)

| Check Item | Points | Criteria |
|-----------|--------|----------|
| Recent updates (< 30 days) | 4 | File modified within last 30 days |
| Ecosystem alignment | 3 | Current role boundaries and registry agree; derive counts rather than maintaining copies |
| No deprecated patterns | 3 | No stale references or outdated formats |

**Maximum: 10 points**

### Context Efficiency Score (Bonus: +0 to 10)

Applied as a tiebreaker on top of the base 100-point Health Score.

| Check Item | Points | Criteria |
|-----------|--------|----------|
| Boilerplate ratio < 15% | 3 | Deduplication applied to common sections |
| Token budget within target | 3 | Section-level token estimates documented |
| Layout compliance | 2 | Task constraints and completion remain easy to locate in the canonical template order |
| Compression equivalence verified | 2 | 4-axis verification passed |

**Maximum Bonus: 10 points** (added to base score, used only as tiebreaker for same-grade agents)

See `reference/context-compression.md` for detailed methodology.

---

### Score Interpretation

| Score | Grade | Action |
|-------|-------|--------|
| 90-100 | A | No action needed |
| 80-89 | B | Minor improvements optional |
| 70-79 | C | Schedule improvements |
| 60-69 | D | Priority improvements |
| < 60 | F | Immediate attention |

Response times come from § Improvement Queue below — the only SLA ladder.

---

## Health Score Calculation Template

```yaml
HEALTH_SCORE_CALCULATION:
  agent: "[Agent Name]"
  date: "[YYYY-MM-DD]"
  structure: 0      # 0-30
  content: 0        # 0-25
  integration: 0    # 0-20
  activity: 0       # 0-15
  freshness: 0      # 0-10
  total: 0          # 0-100 (component maxima already sum to 100 — no second weighting)
  context_efficiency_bonus: 0  # 0-10, tiebreaker only
  grade: "[A-F]"
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

## Per-Recipe Behavior + VERIFY Gates (SKILL.md excerpt)

Behavior notes per Recipe. Each `**VERIFY**:` is the recipe-specific gate **in addition to** Architect's universal discipline (ENVISION / Health Score / validation never skipped, Nexus hub-and-spoke preserved, formal topology for any multi-agent design).
- `create`: ENVISION (20-30% effort) → ANALYZE (overlap scoring) → GENERATE (SKILL.md + references) → VALIDATE (current checklist). Read `creative-thinking.md` first. **VERIFY**: ENVISION actually run (20-30% effort, not skipped); overlap < 30% with every existing agent (30-49% → Ask First, ≥50% → reject); applicable validation passes (all REQUIRED + RECOMMENDED ≥80%); SKILL.md < 500 lines / 5000 tokens with only necessary, conditionally loaded references; `description:` carries **negative triggers** ("Don't use when…"); CAPABILITIES_SUMMARY + COLLABORATION_PATTERNS + explicit INPUT/OUTPUT partners + AUTORUN + Nexus Hub Mode all present.
- `improve`: Read `review-loop.md` for Health Score. ANALYZE → SCORE → PRIORITIZE → VALIDATE workflow. **VERIFY**: Health Score computed **before and after**; validation re-passes post-change; changes to Boundaries / CAPABILITIES / Principles / Framework (Level C) gated on human approval; no new overlap introduced; the improved skill stays under the size ceiling.
- `compress`: Token-budget analysis before changes. Verify 4-axis equivalence (Behavioral/Structural/Integration/Routing). Confirm if reduction > 20%. **VERIFY**: token-budget analysis done before any edit; 4-axis equivalence verified (Behavioral + Structural + Integration + Routing all preserved); section-by-section analysis (no uniform or lossy compression); > 20% reduction confirmed with the user; reversible compression preferred over speculative.
- `audit-verbosity`: COLLECT samples → MEASURE 5 metrics (filler/tier/format/header/tautology) → PROPOSE diff to Output Contract → emit `OUTPUT_AUDIT_REPORT`. Refuse if zero samples; never grade on speculation. **VERIFY**: refuses outright if zero real runtime samples (never grades on speculation); all 5 metrics measured (filler / tier / format / header / tautology); a concrete diff to the Output Contract proposed; `OUTPUT_AUDIT_REPORT` emitted.
- `evolve`: Architect self-modification only. Strictly enforce Safety Level A/B/C/D. Rollback snapshot is mandatory. **VERIFY**: scope is Architect self-modification only; a rollback snapshot is taken **before** any mutation (auto-rollback on VERIFY failure); Safety Level A/B/C/D enforced (Level C → human approval, Level D → forbidden); change budget (20 lines/session, 50/month) not exceeded without approval; outcome persisted to `.agents/architect.md`.
