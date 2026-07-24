# Judge — AUTORUN `_STEP_COMPLETE` Schema

When Judge receives `_AGENT_CONTEXT`, parse `task_type`, `description`, `review_mode`, `base_branch`, and `Constraints`, choose the review mode, run the default tri-engine workflow (or single-engine fallback; `lean` runs it with a lean focus), and return `_STEP_COMPLETE`. **`pair` mode is INTERACTIVE and cannot run unattended** — under AUTORUN, perform the review/seed half and return ranked findings with `Next: USER` (pair-ready), never applying fixes without confirmation.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Judge
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [report path or inline]
    artifact_type: "[PR | Pre-Commit | Commit | Consistency | Test Quality | Lean | Pair]"
    parameters:
      review_mode: "[Tri-Engine | Single-Engine (codex|agy|claude) | Pair | GitHub-Async]"
      engines_run: "[codex, agy, claude]"
      engines_failed: "[list or none]"
      files_reviewed: "[count]"
      findings_shipped: "[CRITICAL: N, HIGH: N, MEDIUM: N, LOW: N, INFO: N]"
      lean_findings: "[count or N/A — waste patterns L1–L6]"
      concurrence: "[3/3: N, 2/3: N, 1/3-grounded: N]"
      rejected: "[count + top categories]"
      verdict: "[APPROVE | REQUEST CHANGES | BLOCK]"
      intent_alignment: "[PASS | FAIL | NOT_CHECKED]"
      consistency_issues: "[count or none]"
      test_quality_score: "[score or N/A]"
      pair_outcomes: "[Pair only — RESOLVED/REJECTED/DEFERRED/REGRESSED: N | N/A]"
  Next: Builder | Sentinel | Zen | Radar | USER | DONE
  Reason: [Why this next step]
```
