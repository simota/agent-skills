# Cron Patterns — Authoring, Validation, Platform Differences

Complete reference for cron expression design, validation, and platform-specific behavior. Read when authoring or reviewing any cron expression.

> **2026 framing: is cron the right tool?** Treat cron as the right answer when the job is **stateless, idempotent, and fits comfortably in one execution window** — `nightly ETL trigger`, `cache pre-warm`, `cert-renewal poll`. Reach for a durable workflow scheduler (Temporal Schedules, Cadence, Inngest, Azure Durable Functions) when the work is long-running, must survive worker crashes, needs catch-up after operator pause, or needs first-class "wait hours / days for an external signal" semantics. Kubernetes CronJob remains the cheap default for stateless containerised jobs; Temporal Schedules become the cheaper choice once the job grows retry / pause / time-machine requirements that you would otherwise reimplement on top of cron.

---

## Field Formats: 5-field vs 6-field

### 5-field Unix cron

```
┌──────────── minute      (0-59)
│ ┌────────── hour        (0-23)
│ │ ┌──────── day-of-month (1-31)
│ │ │ ┌────── month       (1-12 OR jan-dec)
│ │ │ │ ┌──── day-of-week (0-6 OR sun-sat; Sunday = 0 or 7 depending on platform)
│ │ │ │ │
* * * * *
```

Used by: Linux crontab, K8s CronJob, GitHub Actions, Cloud Scheduler, Sidekiq (via sidekiq-cron), BullMQ (via repeat.cron), Celery Beat (via crontab()).

### 6-field Quartz / Spring

```
┌──────────── second      (0-59)
│ ┌────────── minute      (0-59)
│ │ ┌──────── hour        (0-23)
│ │ │ ┌────── day-of-month (1-31) — OR use `?`
│ │ │ │ ┌──── month       (1-12 OR jan-dec)
│ │ │ │ │ ┌── day-of-week (1-7 OR MON-SUN; Sunday = 1 or 7 in Quartz) — OR use `?`
│ │ │ │ │ │
* * * * * ?
```

Used by: Quartz Scheduler (Java), Spring `@Scheduled(cron=...)`, some enterprise schedulers.

**Critical rule**: In Quartz, day-of-month and day-of-week cannot both be specified — one MUST be `?`. This disambiguates "the 15th" vs "every Monday".

### 6-field AWS EventBridge

```
cron(minute hour day-of-month month day-of-week year)
```

EventBridge has 6 fields but they mean: min, hour, dom, mon, dow, year. Same `?` rule as Quartz: dom OR dow must be `?`. UTC-only; use the `scheduleExpressionTimezone` field on Scheduler (not legacy rules) for IANA TZs.

---

## Common Patterns

### Interval expressions

| Intent | 5-field Unix | 6-field Quartz | Notes |
|--------|--------------|----------------|-------|
| Every minute | `* * * * *` | `0 * * * * ?` | |
| Every 5 minutes | `*/5 * * * *` | `0 */5 * * * ?` | |
| Every 15 minutes | `*/15 * * * *` | `0 */15 * * * ?` | |
| Every hour (top) | `0 * * * *` | `0 0 * * * ?` | |
| Every 2 hours | `0 */2 * * *` | `0 0 */2 * * ?` | Fires at 00, 02, 04, ... |
| Every day at 03:30 | `30 3 * * *` | `0 30 3 ? * *` | |
| Every Monday at 09:00 | `0 9 * * 1` | `0 0 9 ? * MON` | |
| First of month at 00:00 | `0 0 1 * *` | `0 0 0 1 * ?` | |
| Last day of month 23:59 | not portable | `0 59 23 L * ?` | Quartz `L` = last |

### Cron aliases (not portable across all platforms)

| Alias | Equivalent | Supported |
|-------|------------|-----------|
| `@yearly` / `@annually` | `0 0 1 1 *` | most Unix crons, GitHub Actions, K8s |
| `@monthly` | `0 0 1 * *` | most Unix crons |
| `@weekly` | `0 0 * * 0` | most Unix crons |
| `@daily` / `@midnight` | `0 0 * * *` | most Unix crons |
| `@hourly` | `0 * * * *` | most Unix crons |
| `@reboot` | at startup | Unix only, NOT in K8s or GHA |

Prefer explicit expressions over aliases for portability and readability.

---

## Anti-patterns

### 1. Every-minute overlap with long-running tasks

```yaml
# BAD
schedule: "* * * * *"
# task_duration_p99: 90s → runs will overlap every minute
```

**Symptom**: Resource contention, duplicated side effects, DB row-lock starvation.

**Fix options**:
- Use a distributed lock (Redis `SET NX EX`, PG advisory lock, `Sidekiq::Limiter`).
- Increase the interval to exceed p99 runtime + margin.
- Switch to a queue-based worker that pulls work continuously.
- Set platform overlap policy: K8s `concurrencyPolicy: Forbid`, Quartz `@DisallowConcurrentExecution`.

### 2. Midnight on DST transition days

```yaml
# BAD — in America/New_York
schedule: "0 0 * * *"   # "every day at midnight local"
```

**Symptom**:
- Spring-forward Sunday: midnight fires normally (midnight is not in the DST gap), but a 02:30 schedule is SKIPPED or DEFERRED.
- Fall-back Sunday: a 01:30 schedule would RUN TWICE.
- Midnight itself is usually safe in US/EU DST (transitions are at 02:00/03:00), but midnight in some zones (Chile `America/Santiago`) IS a DST transition time.

**Fix**:
- Run in UTC: `cron(0 5 * * ? *)` for 05:00 UTC.
- Or annotate an explicit DST policy in the spec.
- Or use a scheduler that accepts `scheduleExpressionTimezone: Asia/Tokyo` (EventBridge Scheduler, Cloud Scheduler, K8s CronJob v1.25+ `spec.timeZone`).

### 3. Day-31 in short months

```yaml
# BAD — fires only 7 times/year (Jan, Mar, May, Jul, Aug, Oct, Dec)
schedule: "0 0 31 * *"
```

**Symptom**: "Monthly" job actually runs only in 31-day months.

**Fix options**:
- Quartz: `0 0 0 L * ?` (`L` = last day of month).
- K8s / Unix cron: schedule daily + application-level "is-last-day" check.
- Cron-parser libraries do NOT universally support `L`; check platform docs.

### 4. Sunday = 0 vs Sunday = 7

```yaml
# AMBIGUOUS
schedule: "0 0 * * 0,7"   # Sunday double-specified? Or 0=Sun, 7=Sat?
```

**Fact**:
- POSIX cron: Sunday = 0 or 7 (both valid); Saturday = 6.
- Quartz: Sunday = 1 or 7 (different!); Saturday = 7.
- GitHub Actions / cronie: 0 and 7 both = Sunday.

**Fix**: Use `0` only in Unix cron contexts; use named days (`SUN`) in Quartz.

### 5. Day-of-month AND day-of-week combined

```yaml
# CONFUSING — semantics differ by platform
schedule: "0 0 15 * 1"   # 15th AND Monday? OR 15th OR Monday?
```

**Fact**:
- Vixie cron (most Linux): **OR** semantics — fires on the 15th OR on any Monday.
- Quartz: disallows both — one must be `?`.
- ISC cron (BSD/macOS): OR semantics.
- EventBridge: dom OR dow must be `?`.

**Fix**: Pick one filter; express the other at application level.

### 6. Second-field confusion

```yaml
# BAD in a K8s CronJob manifest
schedule: "0 */5 * * * *"   # 6 fields — K8s expects 5; will fail validation
```

**Fix**: K8s CronJob is 5-field. For sub-minute scheduling, use a Deployment with in-process scheduler, or switch to Quartz/Temporal.

---

## Platform-Specific Behavior

### Linux crontab / cronie

- 5-field Unix cron.
- Runs in the server's system timezone by default; set `CRON_TZ=UTC` at the top of the crontab to override.
- No timezone column per-entry until cronie 1.5 (`TZ=` per-line syntax).
- No retry on failure; no DLQ; output goes to mail by default.
- Skew: typically sub-minute.

### systemd timers

- Not cron syntax — uses `OnCalendar=` with its own grammar (e.g., `OnCalendar=*-*-* 02:30:00`).
- Supports `AccuracySec=` (jitter reduction), `RandomizedDelaySec=` (explicit jitter).
- Timezone: `OnCalendar=` can include a TZ suffix (`UTC`, `Asia/Tokyo`).
- Better than crontab for modern systems: persistent state, logging via journald, dependency management.

### GitHub Actions

- 5-field Unix cron, UTC only, no per-workflow timezone.
- **Best effort delivery** — may skew 5-15 minutes, occasionally longer on high load; documented by GitHub as not for time-critical jobs.
- Minimum practical interval: 5 minutes (shorter intervals are deprioritized or skipped by the scheduler).
- Scheduled workflows on forked repos are disabled by default; default branch only.
- No automatic retry on failure; use `uses: nick-fields/retry@v3` or equivalent action.

```yaml
# Example: daily at 15:00 UTC = 00:00 JST (next day)
on:
  schedule:
    - cron: '0 15 * * *'
```

### AWS EventBridge (classic Rules)

- 6-field: `cron(min hour dom mon dow year)`.
- `?` required on dom or dow (cannot both be specified).
- UTC only for classic EventBridge Rules; use **EventBridge Scheduler** (separate service) for IANA TZ support via `ScheduleExpressionTimezone`.
- Retry: downstream Lambda async invocation — up to 2 retries (0/1/2 configurable), then SQS DLQ.
- Skew: typically sub-minute.

```
# Every weekday at 09:00 UTC
cron(0 9 ? * MON-FRI *)
```

### EventBridge Scheduler (newer)

- Same 6-field format but supports `ScheduleExpressionTimezone`.
- Supports one-time schedules (`at(2026-12-31T23:59:59)`) and `rate(N units)`.
- Flexible time windows (`flexibleTimeWindow`) for load spreading.
- Explicit retry policy per schedule; DLQ via target config.

### Kubernetes CronJob

- 5-field Unix cron.
- Default timezone: UTC on the controller node (historically confusing — differed by cluster).
- `spec.timeZone` (IANA name) is **GA in K8s 1.27+**; beta in 1.25. Always set it explicitly.
- `concurrencyPolicy`: `Allow` (default), `Forbid`, `Replace` — controls overlap.
- `startingDeadlineSeconds`: if a scheduled run misses by more than this, it is NOT started. Must be > 10s.
- `successfulJobsHistoryLimit` / `failedJobsHistoryLimit`: retained Job count; defaults 3/1.
- `backoffLimit` on the underlying Job: pod retry count; default 6 with exponential backoff.
- Skew: depends on controller load; usually sub-minute.

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nightly-report
spec:
  schedule: "0 2 * * *"
  timeZone: "Asia/Tokyo"
  concurrencyPolicy: Forbid
  startingDeadlineSeconds: 300
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      backoffLimit: 3
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: report
              image: myorg/report:latest
```

### GCP Cloud Scheduler

- 5-field Unix cron (`* * * * *`) or App Engine cron syntax (`every 1 hours`).
- `timeZone`: any IANA name.
- Retry: `retryConfig` with `retryCount`, `maxRetryDuration`, `minBackoffDuration`, `maxBackoffDuration`, `maxDoublings`.
- Target: HTTP endpoint, Pub/Sub topic, App Engine.
- Skew: typically sub-minute.

### Sidekiq (Ruby)

- Uses `sidekiq-cron` gem with standard cron syntax, any IANA TZ.
- Built-in retry: 25 retries with exponential backoff (`retry_in` formula = `count^4 + 15 + rand(30)*(count+1)`).
- **Sidekiq 8.x**: scheduler polling accuracy improved from 15s to **5s**, reducing job start latency for scheduled jobs. Source: [Sidekiq Changes.md](https://github.com/sidekiq/sidekiq/blob/main/Changes.md).
- Failed jobs after retries exhausted → "Morgue" (dead queue), retained 6 months default.
- Idempotency: `sidekiq-unique-jobs` gem with locks.

### BullMQ (Node.js)

- **v5.16.0+**: The `repeat` / repeatable-jobs API is **deprecated** in favor of **Job Schedulers** (`queue.upsertJobScheduler(schedulerId, { pattern: '...', tz: 'Asia/Tokyo' }, jobData)`). Job Schedulers provide a more robust API with named schedulers and `startDate`. Source: [BullMQ Job Schedulers](https://docs.bullmq.io/guide/job-schedulers).
- Retry: `attempts: N, backoff: { type: 'exponential', delay: 1000 }`.
- Failed jobs → `failed` list; can be moved to another queue manually.
- Idempotency: set custom `jobId` (same ID = deduped).

```javascript
// v5.16.0+ recommended API
await queue.upsertJobScheduler(
  'nightly-report',
  { pattern: '0 2 * * *', tz: 'Asia/Tokyo' },
  { name: 'generate-report', data: { type: 'nightly' } }
);
```

### Celery Beat (Python)

- `crontab(minute=..., hour=..., day_of_week=..., day_of_month=...)` in `celery.conf.beat_schedule`.
- Timezone: set `timezone = 'Asia/Tokyo'` in Celery config.
- Retry: `@app.task(autoretry_for=(Exception,), retry_backoff=True, retry_backoff_max=600, max_retries=5)`.
- No built-in DLQ; route failed tasks via `task_routes` + custom handler.

### Temporal

- Cron on `WorkflowOptions.setCronSchedule("0 2 * * *")` — 5-field.
- First-class retry policy (`RetryPolicy`) with `initialInterval`, `backoffCoefficient`, `maximumAttempts`, `maximumInterval`, `nonRetryableErrorTypes`.
- Workflow ID is the natural idempotency key — two starts with the same ID collide (configurable).
- Exactly-once workflow semantics (with at-least-once activity retries).

---

## Validation Tools

### Online

- **crontab.guru** (https://crontab.guru) — 5-field Unix cron; shows next-fire times in the browser's TZ.
- **cronhub.io/examples** — pattern library.

### CLI / library

- **cronstrue** (npm / py) — translate cron to English: `cronstrue "0 0 * * *"` → `"At 12:00 AM"`.
- **croniter** (Python) — next-fire prediction, DST-aware.
- **cron-parser** (npm) — JS equivalent of croniter; supports `tz` option.
- **CronExpression** (Quartz Java) — `getNextValidTimeAfter(date)`.

### Next-fire prediction snippets

**Python (croniter)**:
```python
from croniter import croniter
from datetime import datetime
from zoneinfo import ZoneInfo

base = datetime(2026, 3, 8, 0, 0, tzinfo=ZoneInfo("America/New_York"))
iter = croniter("0 2 * * *", base)
for _ in range(5):
    print(iter.get_next(datetime))
# Shows the spring-forward Sunday skip: Mar 8 02:00 → Mar 9 02:00 → ...
# BUT check: Mar 9 2026 02:00 does not exist in NY; croniter handles the gap.
```

**Node (cron-parser)**:
```javascript
import parser from 'cron-parser';

const iter = parser.parseExpression('0 2 * * *', {
  tz: 'America/New_York',
  currentDate: '2026-03-08T00:00:00-05:00',
});
for (let i = 0; i < 5; i++) {
  console.log(iter.next().toString());
}
```

**Java (Quartz)**:
```java
CronExpression ce = new CronExpression("0 0 2 * * ?");
ce.setTimeZone(TimeZone.getTimeZone("America/New_York"));
Date next = ce.getNextValidTimeAfter(new Date());
```

---

## Checklist: before shipping a cron expression

- [ ] Field count matches the platform (5 vs 6).
- [ ] Timezone annotated (IANA name) in the spec AND in the platform config.
- [ ] DST policy explicit if the schedule runs at local wall-clock.
- [ ] Next-fire simulated across at least one DST boundary.
- [ ] Next-fire simulated across a month boundary, including short months if `day-of-month` used.
- [ ] Overlap policy declared (platform config + app-level lock if needed).
- [ ] dom/dow combination semantics verified for the platform.
- [ ] Validated via crontab.guru or equivalent.
- [ ] Paired with retry policy (see `retry-strategies.md`).
- [ ] Paired with idempotency key (see `retry-strategies.md`).
