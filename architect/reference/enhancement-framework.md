# Enhancement Assessment

Read for IMPROVE or a before/after self-modification assessment. Score observed artifacts, not a plan. These are repository assessment points, not measured execution success. The five component maxima already sum to 100: add points once, do not weight them a second time.

## Health Score Assessment

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

## Grade Interpretation

| Score | Grade | Action | Response Time |
|-------|-------|--------|---------------|
| 90-100 | A | No action needed | — |
| 80-89 | B | Minor improvements optional | Next cycle |
| 70-79 | C | Schedule improvements | < 2 weeks |
| 60-69 | D | Priority improvements | < 1 week |
| < 60 | F | Immediate attention | < 24 hours |

## Priority Classification

| Priority | Evidence required |
|----------|-------------------|
| P1 | Missing required contract, broken declared partner integration, a component below 50% of its maximum, or a gap blocking downstream execution |
| P2 | Missing executable workflow/confirmation, uncovered AUTORUN task type, or a non-blocking declared collaboration gap |
| P3 | A demonstrated improvement that does not block current behavior; do not add files, examples or speculative capabilities merely to increase a score |

## Improvement Workflow

Read the skill, its references and relevant partner contracts; score the five components. Compare with `_templates/SKILL_TEMPLATE.md`, verify reciprocal handoff expectations, and cover every supported AUTORUN task type. Group evidence-backed gaps by dependency and priority. Apply the authorized change, run existing repository checks, then rescore and report actual versus projected improvement. Do not count missing logs or unavailable execution evidence as observed success.

## Enhancement Proposal Template

```yaml
ENHANCEMENT_PROPOSAL:
  agent: "[Agent name]"
  date: "[YYYY-MM-DD]"
  architect_assessment:
    health_score_current: [0-100]
    grade_current: "[A-F]"
    health_score_projected: [0-100]
    grade_projected: "[A-F]"

  breakdown:
    structure: { score: [0-30], issues: ["..."] }
    content: { score: [0-25], issues: ["..."] }
    integration: { score: [0-20], issues: ["..."] }
    activity: { score: [0-15], issues: ["..."] }
    freshness: { score: [0-10], issues: ["..."] }

  proposals:
    - id: 1
      title: "[Enhancement title]"
      priority: P1 | P2 | P3
      category: structure | content | integration | activity | freshness
      description: "[What to add/change]"
      current_gap: "[What is missing or broken]"
      expected_impact:
        score_delta: [+N points]
        affected_components: ["structure", "integration"]
      files:
        - path: "[file path]"
          action: create | edit
          description: "[What changes]"

  implementation_order:
    - phase: P1
      proposals: [1, 2]
      estimated_files: [count]
    - phase: P2
      proposals: [3, 4]
      estimated_files: [count]
    - phase: P3
      proposals: [5, 6]
      estimated_files: [count]
```

```yaml
HEALTH_SCORE_REPORT:
  agent: "[name]"
  score: [0-100]
  grade: "[A-F]"
  breakdown:
    structure: [0-30]
    content: [0-25]
    integration: [0-20]
    activity: [0-15]
    freshness: [0-10]
  top_issues:
    - "[Issue 1 — highest impact]"
    - "[Issue 2]"
    - "[Issue 3]"
```

## Integration with Review Loop

The owning cadence and feedback windows remain in `reference/review-loop.md`. Use this rubric at PLAN/CHECK; execute at DO and carry verified results into ACT. SCHEDULED reviews score the selected batch, ON_AGENT_CREATION scores at 7 days, ON_ECOSYSTEM_CHANGE reassesses affected skills, and ON_QUALITY_ALERT requires an immediate P1 proposal.
