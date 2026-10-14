# Enhancement Assessment

Read for IMPROVE or a before/after self-modification assessment. Score observed artifacts, not a plan. These are repository assessment points, not measured execution success. The five component maxima already sum to 100: add points once, do not weight them a second time.

## Health Score Assessment

Canonical rubric, grades and response-time ladder: `reference/review-loop.md` § Agent Health Score and § Improvement Queue. Score the five components there; this file covers prioritization and the proposal format only.

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

The owning cadence and feedback windows remain in `reference/review-loop.md`. Use its rubric at PLAN/CHECK; execute at DO and carry verified results into ACT. SCHEDULED reviews score the selected batch, ON_AGENT_CREATION scores at 7 days, ON_ECOSYSTEM_CHANGE reassesses affected skills, and ON_QUALITY_ALERT requires an immediate P1 proposal.
