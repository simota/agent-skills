# Rank — AUTORUN `_STEP_COMPLETE` Schema

When Rank receives `_AGENT_CONTEXT`, parse `task_type`, `items`, `constraints`, `frameworks`, `stakeholders`, and `work_mode`, choose the correct output route, run the COLLECT→CRITERIA→SCORE→CALIBRATE→PRESENT workflow, produce the ranking deliverable, and return `_STEP_COMPLETE`.

### `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Rank
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [ranking report]
    parameters:
      work_mode: "[FULL | QUICK | BATCH]"
      frameworks_used: "[list]"
      items_ranked: "[count]"
      rank_correlation: "[Spearman rho between frameworks]"
      confidence: "[HIGH | MEDIUM | LOW]"
  Next: [Sherpa | Builder | Magi | Magi | DONE]
  Reason: [Why this next step]
```
