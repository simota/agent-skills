# Scout Handoff Formats

Canonical YAML schemas for all Scout outbound handoffs. SKILL.md only lists handoff names; this file owns the schemas.

Universal handoff conventions: `_common/HANDOFF.md`.
Cross-cluster escalation handoffs (LENS_TO_SCOUT, SCOUT_TO_LENS, TRAIL↔SPECTER): `_common/INVESTIGATION_ESCALATION.md`.

## SCOUT_TO_BUILDER_HANDOFF

```yaml
SCOUT_TO_BUILDER_HANDOFF:
  bug_id: "[identifier or title]"
  root_cause: "[file:line — cause description]"
  confidence: "[HIGH | MEDIUM | LOW]"
  fix_direction: "[recommended approach]"
  files_to_modify: ["file1", "file2"]
  constraints: "[side effects, backward compatibility notes]"
  regression_tests: "[test ideas for Radar]"
  fix_prompt: "[paste-ready LLM Fix Prompt; see reference/fix-prompt-generation.md. Omit only when suppression rule applies.]"
  fix_prompt_verb: "[FIX | FIX-WITH-TEST | MITIGATE | INVESTIGATE-FURTHER | REFACTOR-FIX]"
  impact_scope:
    callers: ["file:line", ...]    # references that may break or need verification
    tests: ["test files"]           # tests to add or update
    types: ["type/schema files"]    # type/contract dependents
    configs: ["config/env keys"]    # env var / feature flag / config touch points
    docs: ["doc paths"]             # README / CHANGELOG / API docs to update
    axes_affected: <0-5>
    recommend_ripple: <true | false>  # true → route to Ripple before Builder
```

## SCOUT_TO_RADAR_HANDOFF

```yaml
SCOUT_TO_RADAR_HANDOFF:
  bug_id: "[identifier or title]"
  reproduction_steps: "[minimal repro]"
  root_cause: "[cause summary]"
  test_suggestions:
    - "[regression test 1]"
    - "[regression test 2]"
  coverage_gaps: "[areas lacking test coverage]"
```

## SCOUT_TO_TRIAGE_HANDOFF

```yaml
SCOUT_TO_TRIAGE_HANDOFF:
  bug_id: "[identifier or title]"
  severity: "[Critical | High | Medium | Low]"
  scope_change: "[expanded | unchanged | narrowed]"
  affected_users: "[scope description]"
  workaround: "[available workaround or 'none']"
  escalation_reason: "[why Triage needs to re-evaluate]"
```

## SCOUT_TO_SPECTER_HANDOFF

```yaml
SCOUT_TO_SPECTER_HANDOFF:
  bug_id: "[identifier or title]"
  symptom: "[observed concurrency or resource issue]"
  evidence: "[traces, timing, resource metrics]"
  suspected_type: "[race condition | memory leak | deadlock | resource exhaustion]"
  files_involved: ["file1", "file2"]
```

## SCOUT_TO_SENTINEL_HANDOFF

```yaml
SCOUT_TO_SENTINEL_HANDOFF:
  bug_id: "[identifier or title]"
  security_concern: "[description of suspected vulnerability]"
  evidence: "[observations suggesting security impact]"
  severity_estimate: "[Critical | High | Medium]"
  files_involved: ["file1", "file2"]
```

## SCOUT_TO_TRAIL_HANDOFF

```yaml
SCOUT_TO_TRAIL_HANDOFF:
  bug_id: "[identifier or title]"
  regression_signal: "[what suggests a regression]"
  time_range: "[suspected window]"
  files_of_interest: ["file1", "file2"]
  delegation_reason: "[why history analysis should be primary]"
```

## AUTORUN `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Scout
  artifact_type: "[Investigation Report | Regression Analysis | Impact Assessment | Reproduction Report | Tri-Engine Investigation Report]"
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [primary artifact]
    parameters:
      task_type: "[task type]"
      scope: "[scope]"
      confidence: "[HIGH | MEDIUM | LOW]"
      root_cause_location: "[file:line or 'unconfirmed']"
      reproduction_status: "[reproduced | partially reproduced | not reproduced]"
      impact_scope_axes_affected: "[0-5 — number of affected axes among callers/tests/types/configs/docs]"
      recommend_ripple: "[true | false — true when axes_affected ≥ 3 or uncertainty is high]"
    tri_engine:                                  # present only when `multi` Recipe ran
      engines_run: [codex, agy, claude]
      engines_failed: [list or none]
      perspective_verdict: "[CONVERGENT | DIVERGENT-N]"
      confidence_distribution:
        CONFIRMED: [count]
        LIKELY: [count]
        CANDIDATE-VERIFIED: [count]
      primary_rca:
        cluster_id: "[identifier]"
        engine_attribution: "[codex+agy+claude | codex+agy | codex-verified | ...]"
        ground_verdict: "[VERIFIED | LIKELY-VERIFIED]"
      alternative_hypotheses_count: [N — 0 if CONVERGENT]
      verification_ordering: "[present | absent — absent only if CONVERGENT]"
      rejected: [count + top categories — hallucination / chain-broken / mitigated / needs-info]
  Validations:
    completeness: "[complete | partial | blocked]"
    quality_check: "[passed | flagged | skipped]"
  Next: [Ripple | Builder | Radar | recommended next agent | DONE]
  Reason: [Why this next step]
```
