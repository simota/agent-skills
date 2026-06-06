# Guardian AUTORUN Mode Reference

Purpose: Define Guardian's autonomous behavior, pause conditions, partial completion rules, and `_STEP_COMPLETE` contract inside Nexus chains.

## Contents

- AUTORUN context
- Auto-execute actions
- Pause conditions
- Guardrails and recovery
- `_STEP_COMPLETE` contract
- Status semantics
- Partial execution rules

## AUTORUN Context Format

```yaml
_AGENT_CONTEXT:
  Role: Guardian
  Task: [Specific task from Nexus]
  Mode: AUTORUN
  Chain: [Previous agents in chain]
  Input: [Handoff received from previous agent]
```

## Auto-Execute

Guardian may execute these without confirmation:
- change classification
- branch-name generation
- PR size assessment
- noise detection and reporting
- quality score calculation
- commit message analysis
- risk factor assessment
- hotspot detection
- reviewer recommendation
- branch health check
- pre-merge checklist generation
- coverage integration
- squash group detection and scoring
- noise-commit identification
- squash optimization report generation
- rebase script generation

## Pause for Confirmation

Pause when any of these apply:
- PR split recommendation affects release timing
- merge strategy choice materially changes shared workflow
- force-push or history rewrite is suggested
- destructive Git operation would be required
- `quality_score < 35`
- `risk_score > 85`
- high-risk file changes have no security review
- hotspot refactoring recommendation changes scope
- squash plan involves `10+` commits
- multi-author squash raises attribution concerns
- squash score is neutral (`-14` to `+14`)
- history rewrite targets a shared or already-pushed branch

## Guardian-Specific Guardrails

```yaml
guardrails:
  git_conflict_unresolved:
    detection: "merge conflict markers remain"
    action: "handoff to Scout for conflict investigation"

  pr_too_large:
    detection: "PR size > XL"
    action: "auto-generate split proposal"

  branch_name_collision:
    detection: "suggested branch already exists"
    action: "generate suffixed alternatives such as -v2 or -alt"
```

## Recovery Strategies

```yaml
recovery_strategies:
  retry_with_reduced_scope:
    triggers: [analysis_timeout, memory_limit]
    action: "limit analysis to essential files first"
    max_retries: 2

  fallback_to_report_only:
    triggers: [missing_metadata, partial_ci_data]
    action: "report uncertainty and continue with explicit caveats"

  defer_blocking_decision:
    triggers: [shared_branch_rewrite, conflicting_handoffs]
    action: "emit BLOCKED or PARTIAL and require next decision point"
```

## `_STEP_COMPLETE` Format

```yaml
_STEP_COMPLETE:
  Agent: Guardian
  Status: SUCCESS|PARTIAL|BLOCKED|FAILED
  Output: <primary artifact or report>
  Next: <next action or next agent>
```

## Status Definitions

- `SUCCESS`: all requested analysis completed with no blocking uncertainty
- `PARTIAL`: usable output exists, but one or more non-fatal gaps remain
- `BLOCKED`: analysis cannot safely proceed without an external decision or handoff
- `FAILED`: required analysis could not be completed

## PARTIAL Status Conditions

Use `PARTIAL` when:
- some CI, coverage, or risk metadata is missing
- branch or PR context is incomplete but enough evidence exists for a scoped recommendation
- a non-blocking handoff is recommended but not yet completed
- analysis was intentionally reduced to essential files to stay within limits

## Decision Matrix

| Condition | Action |
|-----------|--------|
| destructive or shared-history change | pause |
| quality `< 35` | pause |
| risk `> 85` | pause |
| blocking security finding | handoff and block |
| non-blocking coverage or noise issue | handoff and continue |
| partial but actionable data | return `PARTIAL` |

## Partial Execution Support

When returning partial results:
- state which sections are complete
- mark missing evidence explicitly
- preserve all blocking findings
- recommend the smallest safe next action

### Partial `_STEP_COMPLETE` Example

```yaml
_STEP_COMPLETE:
  Agent: Guardian
  Status: PARTIAL
  Output: "PR quality score, risk report, and split proposal"
  Next: "Run Radar for missing coverage validation"
```
