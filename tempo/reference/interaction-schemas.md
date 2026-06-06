# Tempo Interaction Schemas

Question schemas for human-in-the-loop decisions and AUTORUN `_STEP_COMPLETE` output structure. Surface only when the corresponding INTERACTION_TRIGGER fires.

---

## INTERACTION_TRIGGERS

| Trigger | Timing | When to Ask |
|---------|--------|-------------|
| DST_POLICY_CHOICE | BEFORE_START | Schedule runs at local wall-clock time crossing DST |
| CATCHUP_DEPTH | BEFORE_START | Backfill scope is unbounded or unspecified |
| OVERLAP_POLICY | ON_DECISION | Average runtime approaches interval length |
| SEMANTICS_CHOICE | ON_DECISION | At-least-once (cheap) vs exactly-once (Temporal) is unresolved |
| PLATFORM_FIT | ON_RISK | Current platform's guarantees do not match requirement |

## Question Schema

```yaml
questions:
  - question: "How should the schedule behave across a DST transition?"
    header: "DST Policy"
    options:
      - label: "Defer to next valid time (Recommended)"
        description: "Skip non-existent times (spring-forward 02:30); use first occurrence at fall-back 01:30"
      - label: "Skip the ambiguous day"
        description: "Miss the run entirely when the wall-clock time is invalid/ambiguous"
      - label: "Run both occurrences at fall-back"
        description: "Accept double-run at 01:30 twice; requires strong idempotency"
      - label: "Switch schedule to UTC"
        description: "Evaluate in UTC; wall-clock drifts by +/-1h across DST"
    multiSelect: false
  - question: "How far back should backfill / catchup reach?"
    header: "Catchup"
    options:
      - label: "Since last successful watermark (Recommended)"
        description: "Replay from recorded watermark; bounded by data retention"
      - label: "Fixed window (e.g., last 24h)"
        description: "Cheap and predictable; may miss older gaps"
      - label: "No catchup -- skip forward"
        description: "Run at the next scheduled tick only; accept missed runs"
      - label: "Hard cap (e.g., max 7 days, then alert)"
        description: "Bounded catchup with ops alert on overflow"
    multiSelect: false
  - question: "What is the overlap policy when a run exceeds its interval?"
    header: "Overlap"
    options:
      - label: "Skip concurrent (Recommended)"
        description: "Drop the new tick if the previous run is still active; requires distributed lock"
      - label: "Queue sequentially"
        description: "Enqueue new ticks; may fall behind unbounded if runtime > interval"
      - label: "Allow concurrent"
        description: "Runs overlap; requires idempotent, stateless workload"
    multiSelect: false
  - question: "Which delivery semantics does the workload require?"
    header: "Semantics"
    options:
      - label: "At-least-once with idempotency (Recommended)"
        description: "Cheap on any platform; idempotency key protects against duplicates"
      - label: "Exactly-once via Temporal or similar"
        description: "Platform-native guarantee; higher infra cost, stricter model"
      - label: "At-most-once"
        description: "Acceptable data loss; simplest, use only for non-critical metrics"
    multiSelect: false
```

---

## AUTORUN `_STEP_COMPLETE` Output Schema

Tempo-specific Constraints in `_AGENT_CONTEXT`: `Platform`, `Timezone`, `SLA`, `DST_policy`, `Semantics`.

```yaml
_STEP_COMPLETE:
  Agent: Tempo
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [spec file path or inline]
    artifact_type: "Schedule Contract"
    parameters:
      cron_expression: "[cron string]"
      platform: GHA | EventBridge | K8s CronJob | Cloud Scheduler | Sidekiq | BullMQ | Celery | Temporal
      timezone: "[IANA name]"
      dst_policy: skip | defer | run-both | UTC
      overlap_policy: skip | queue | concurrent
      retry: {max_attempts, max_total_duration, backoff, retryable_on}
      idempotency: {key_formula, dedup_window, storage}
      dlq_destination: "[queue name or 'none']"
    files_changed: List[{path, type, changes}]
  Handoff:
    Format: TEMPO_TO_[NEXT]_HANDOFF
    Content: [Handoff content for next agent]
  Risks: [DST policy assumptions, platform SLA caveats, idempotency key lifetime]
  Next: Builder | Gear | Pipe | Weave | Beacon | Voyager | Judge | DONE
```
