# Tempo Handoff Templates

Standard handoff packages for Tempo's upstream and downstream collaborators. Copy these skeletons; fill the bracketed fields.

---

## User → Tempo (schedule requirements intake)

```
TEMPO_INTAKE_HANDOFF
--------------------
Task: [Brief description of the schedule need]

Frequency:
  - Desired: [e.g., "every 15 minutes", "nightly at 02:00 JST", "1st of month"]
  - Tolerance: [acceptable skew — e.g., "within 5 min OK", "strict SLA"]

Timezone:
  - User-facing TZ: [IANA name, e.g., Asia/Tokyo]
  - Server/cluster TZ: [UTC or other]
  - DST handling preference: [skip | defer | run-both | UTC-avoidance | unsure]

Semantics:
  - Delivery: [at-least-once + idempotency | exactly-once | at-most-once | unsure]
  - Idempotency key available?: [yes (natural key = X) | no (need design)]

Workload shape:
  - Expected runtime: [p50 / p99]
  - External calls: [list of dependencies, rate limits]
  - Overlap tolerance: [skip | queue | concurrent | unsure]

Platform:
  - Current: [GHA | EventBridge | K8s CronJob | Cloud Scheduler | Sidekiq | BullMQ | Celery | Temporal | none / undecided]
  - Constraints: [e.g., "must be on GHA", "no new infra"]

Failure handling:
  - SLA on missed runs: [N missed runs = page, etc.]
  - DLQ destination (if known): [queue name or "design needed"]
  - Replay expectation: [automated | manual runbook | none]

Business-calendar awareness:
  - JP holiday aware?: [yes | no | N/A]
  - Banking days?: [yes | no | N/A]
  - Business hours gate?: [yes (hours + TZ) | no]
```

---

## Tempo → Builder (implementation spec)

```
TEMPO_TO_BUILDER_HANDOFF
------------------------
Schedule:
  cron: "[expression]"
  field_count: [5 | 6]
  timezone: "[IANA name]"
  dst_policy: "[skip | defer | run-both | UTC]"
  platform: "[GHA | EventBridge | K8s CronJob | ...]"
  next_fire_preview:
    - [ISO 8601 #1]
    - [ISO 8601 #2 — across DST boundary]
    - [ISO 8601 #3]
    - [ISO 8601 #4]
    - [ISO 8601 #5]

Overlap:
  policy: "[skip | queue | concurrent]"
  lock_mechanism: "[redis:SET NX EX | pg_advisory_lock | none]"
  lock_key: "[e.g., tempo:job:nightly-report]"
  lock_ttl: "[e.g., 2 × p99 runtime]"

Retry:
  max_attempts: [N]
  max_total_duration: "[e.g., 10m]"
  backoff: "[exponential-full-jitter | decorrelated-jitter | fixed]"
  backoff_base: "[e.g., 500ms]"
  backoff_cap: "[e.g., 60s]"
  retryable_on:
    - [error class 1]
    - [error class 2]
  non_retryable_on:
    - [error class 1 — fail fast]

Idempotency:
  key_formula: "[e.g., SHA256(f'payment:{user_id}:{invoice_id}')]"
  dedup_window: "[e.g., 24h]"
  storage: "[redis-setex | db-unique-constraint | stripe-idempotency-key]"
  on_duplicate: "[return cached | noop]"

Dead-letter:
  destination: "[queue / topic / table name]"
  retention: "[e.g., 14 days]"
  drain_procedure: "[path to runbook or inline]"

Platform snippet:
  [ready-to-paste YAML or code for the target platform]

Test scenarios (hand to Voyager):
  - DST spring-forward day in [TZ]
  - DST fall-back day in [TZ]
  - End-of-month (28/29/30/31)
  - Feb-29 in leap year (if applicable)
  - Year rollover
  - [domain-specific scenarios]

Observability (hand to Beacon):
  - Missed-run threshold: [e.g., no fire for 2 × interval]
  - Execution p99 SLO: [e.g., 3m]
  - DLQ depth alert: [e.g., > 0 for 5 min = warn; > 10 = page]
  - Drift alert: [e.g., actual - expected > 60s = warn]

Open questions:
  - [e.g., "confirm retry on 503 vs 502 both acceptable"]
```

---

## Tempo → Gear (CI/CD cron config)

```
TEMPO_TO_GEAR_HANDOFF
---------------------
Purpose: [e.g., "nightly lint + security scan"]

Current config (if modifying):
  file: [.github/workflows/X.yml]
  current_cron: "[expression]"
  current_tz: "[UTC — GHA default]"

Proposed config:
  file: [.github/workflows/X.yml]
  new_cron: "[expression]"
  tz_note: "GitHub Actions is UTC-only; this fires at [IANA time] local"
  best_effort_caveat: "GHA schedule.cron is best-effort; skew 5-15 min possible"

GHA concurrency block (prevent overlap):
  concurrency:
    group: [workflow-name]
    cancel-in-progress: false   # or true per policy

Retry inside workflow:
  step: [uses: nick-fields/retry@v3]
  with:
    timeout_minutes: [N]
    max_attempts: [N]
    retry_wait_seconds: [N]

If SLA cannot tolerate GHA skew:
  recommendation: "Move to EventBridge Scheduler or Cloud Scheduler; GHA keeps build-only triggers"
```

---

## Tempo → Pipe (new GHA workflow with advanced cron)

```
TEMPO_TO_PIPE_HANDOFF
---------------------
Workflow purpose: [description]

Cron schedule:
  cron: "[UTC expression]"
  local_equivalent: "[e.g., 09:00 JST = 00:00 UTC]"
  dst_drift_note: "UTC-based; wall-clock drifts ±1h over the year in DST-observing zones"

Matrix / multi-job concerns:
  - [If fanning out, note per-job concurrency/locking]

Reusable workflow considerations:
  - [Inputs if this is a reusable workflow]
  - [Caller responsibility for retry / idempotency]

Security:
  - [If touching secrets or production, confirm principle of least privilege]

Handoff to Gear for maintenance after rollout.
```

---

## Tempo → Weave (retry state machine definition)

```
TEMPO_TO_WEAVE_HANDOFF
----------------------
Task: [Describe the retryable operation, e.g., "payment webhook delivery"]

State machine definition:
  states:
    - pending        # just enqueued
    - attempting     # active retry
    - retry_waiting  # waiting for next backoff window
    - succeeded
    - failed_retryable    # transient error; loop back to retry_waiting
    - failed_permanent    # non-retryable; go to dead_letter
    - dead_letter         # retry budget exhausted
    - replayed            # drained from DLQ and replayed

  transitions:
    - from: pending
      to: attempting
      on: worker_pickup
    - from: attempting
      to: succeeded
      on: result:success
    - from: attempting
      to: failed_permanent
      on: result:non_retryable_error
    - from: attempting
      to: retry_waiting
      on: result:retryable_error
      guard: "attempts < max_attempts AND elapsed < max_total_duration"
    - from: attempting
      to: dead_letter
      on: result:retryable_error
      guard: "attempts >= max_attempts OR elapsed >= max_total_duration"
    - from: retry_waiting
      to: attempting
      on: backoff_timer_expired
    - from: dead_letter
      to: replayed
      on: manual_replay

Retry policy input (from Tempo):
  max_attempts: [N]
  max_total_duration: "[e.g., 10m]"
  backoff: [formula]

Deliverable from Weave: YAML / XState / Statechart spec + validator.
```

---

## Tempo → Beacon (schedule observability targets)

```
TEMPO_TO_BEACON_HANDOFF
-----------------------
Schedule under observation: [name, cron, TZ]

SLIs:
  - missed_run:
      metric: "time_since_last_successful_run_seconds"
      expected_max: [interval × 1.5]
      alert_threshold: [interval × 2]
      severity: [warn | page]

  - execution_duration:
      metric: "job_execution_duration_seconds"
      p50_target: [X seconds]
      p99_target: [Y seconds]
      alert_threshold: "p99 > [Y × 2] for 3 consecutive runs"

  - drift:
      metric: "scheduled_minus_actual_fire_time_seconds"
      expected: "|drift| < 60s"
      alert_threshold: "|drift| > 300s"

  - dlq_depth:
      metric: "dlq_queue_depth"
      expected_max: 0
      alert_threshold_warn: "> 0 for 5 min"
      alert_threshold_page: "> 10"

SLOs:
  - success_rate:
      target: [e.g., 99.5% over 30d]
      error_budget: [1 - target]

Dashboards:
  - schedule_overview:
      panels: [last-fire, next-fire, duration histogram, success rate, DLQ depth]

Runbook link: [path to DLQ drain + missed-run recovery runbook]
```

---

## Tempo → Voyager (temporal test scenarios)

```
TEMPO_TO_VOYAGER_HANDOFF
------------------------
Schedule under test: [name, cron, TZ]

Test matrix:
  - scenario: dst_spring_forward
    tz: [e.g., America/New_York]
    frozen_clock: "[date of spring-forward in TZ]"
    input_time: "[schedule fire time]"
    expected: "[behavior per DST policy]"
    assertion: "[exact expected result]"

  - scenario: dst_fall_back
    tz: [same]
    frozen_clock: "[date of fall-back in TZ]"
    input_time: "[fire time during the repeated hour]"
    expected: "[runs once, per policy]"
    assertion: "[exact expected result]"

  - scenario: end_of_month
    frozen_clock: "[Jan 31, Feb 28 in non-leap, Feb 29 in leap, Mar 31]"
    expected: "[behavior]"

  - scenario: leap_year_feb29
    frozen_clock: "[Feb 29 in leap year, e.g., 2028-02-29]"
    expected: "[fires / skips as designed]"

  - scenario: year_rollover
    frozen_clock: "[Dec 31 23:59:59]"
    expected: "[fires across year boundary correctly]"

  - scenario: jp_holiday_gate
    frozen_clock: "[a 祝日]"
    expected: "[skipped | deferred to next banking day]"

  - scenario: concurrent_tick
    simulation: "[previous run still active when next tick arrives]"
    expected: "[per overlap policy: skip | queue | run]"

Clock-mocking tool: [@sinonjs/fake-timers | freezegun | java Clock.fixed | timecop]

Deliverable from Voyager: Playwright/Jest test suite + CI integration.
```

---

## Tempo → Judge (schedule correctness review)

```
TEMPO_TO_JUDGE_HANDOFF
----------------------
Review scope: [files and PR URL]

Spec artifact: [path to the Tempo schedule spec doc]

Check focus:
  - Cron expression matches spec (field count, platform).
  - Timezone annotated in config (not just in docs).
  - DST policy implementation matches declared policy.
  - Retry policy caps attempts AND duration.
  - Idempotency key is deterministic and covers retries.
  - Dedup window sized correctly.
  - DLQ destination configured.
  - No `new Date()` / `datetime.now()` without TZ.
  - No 4xx retries (except 408, 429).
  - Observability metrics emitted (as specified for Beacon).

Review deliverable: findings per-file + overall go/no-go.
```

---

## Triage → Tempo (incident replay request)

```
TRIAGE_TO_TEMPO_HANDOFF
-----------------------
Incident: [incident ID]

Missed-run window:
  - Service/job: [name]
  - Downtime start: [ISO 8601 UTC]
  - Downtime end: [ISO 8601 UTC]
  - Last successful watermark: [ISO 8601 UTC or sequence ID]
  - Missed count estimate: [N runs]

Data lag:
  - Downstream systems affected: [list]
  - Late-arriving data tolerance: [yes up to X | no]

Backfill constraints:
  - Max backfill rate: [to avoid DB overload]
  - Business window: [backfill during off-hours only?]
  - Idempotency guarantees: [in place | need design]

Deliverable expected from Tempo:
  - Replay runbook (step-by-step)
  - Catchup bound decision (with rationale)
  - Idempotency re-confirmation (or design if missing)
  - Beacon observability during replay (increased alert sensitivity)
  - Rollback plan if replay causes secondary incident
```

---

## Nexus ↔ Tempo handoff

```yaml
# Nexus → Tempo
_AGENT_CONTEXT:
  Role: Tempo
  Task: "[Specific scheduling task]"
  Mode: AUTORUN
  Chain: [previous agents]
  Input: [handoff from previous agent]
  Constraints:
    - Platform: [specified]
    - Timezone: [IANA name]
    - SLA: [specified]
    - DST_policy: [specified or 'decide']
    - Semantics: [specified or 'decide']
  Expected_Output: "Schedule contract + platform snippet"

# Tempo → Nexus
_STEP_COMPLETE:
  Agent: Tempo
  Status: SUCCESS
  Output:
    deliverable: [path to schedule contract]
    artifact_type: "Schedule Contract"
    parameters:
      cron_expression: "[string]"
      platform: [platform]
      timezone: [IANA]
      dst_policy: [policy]
      overlap_policy: [policy]
      retry: { ... }
      idempotency: { ... }
      dlq_destination: [destination]
    files_changed:
      - path: [path]
        type: created
        changes: [brief]
  Handoff:
    Format: TEMPO_TO_BUILDER_HANDOFF
    Content: [full handoff block above]
  Artifacts:
    - [schedule contract doc]
    - [platform snippet]
    - [next-fire simulation]
    - [test scenario matrix]
  Risks:
    - [DST assumption risk]
    - [Platform SLA risk]
  Next: Builder | Gear | Pipe | Weave | Beacon | Voyager | Judge | DONE
  Reason: [why next step]
```
