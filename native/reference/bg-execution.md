# Background Tasks and Execution Reference (Pure-Native)

Purpose: Design background work that actually runs on modern iOS and Android under battery-saver, Doze, App Standby, and App-Refresh throttling. Covers iOS `BGTaskScheduler` (`BGAppRefreshTask` / `BGProcessingTask`), Android `WorkManager` / `JobScheduler`, Foreground Service Types (Android 14+), execution-time budgeting, and testing strategies. Goal: work that completes reliably within OS budgets, without draining battery or triggering kill-on-wake behavior.

> Pure-native only. React Native Headless JS / Expo Background Tasks are out of scope.

## Scope Boundary

- **Native `bg`**: production background execution — scheduling, constraints, budgeting, failure handling, observability.
- **Forge `mobile`**: prototyping the foreground flow only; background work is stubbed with immediate `setTimeout`.
- **Sentinel**: audits background handlers for information leaks, foreground-service abuse, and over-broad permissions.
- **Gateway**: server endpoints that background tasks call (sync APIs, upload targets, push-triggered fetches). Native orchestrates the client-side schedule; Gateway owns the endpoint contract.

Rule of thumb: if the concern is "will this code wake up, run, and finish under OS constraints?" → `bg`. If it is "will the server accept and respond to the call correctly?" → Gateway.

## Platform Budgets

| Platform | Mechanism | Typical budget | Constraints |
|----------|-----------|----------------|-------------|
| iOS | `BGAppRefreshTask` | ~30 s wall, best-effort schedule | Low priority; OS decides when based on usage, battery, network |
| iOS | `BGProcessingTask` | Minutes, only when device idle and charging | Requires entitlement; user can opt out via Background App Refresh toggle |
| iOS | `URLSession` background upload/download | Until completion, OS managed | Ideal for large transfers; survives app termination |
| Android | `WorkManager` (expedited) | ≤10 min wall, Doze-aware | Quota enforced; falls back to regular work if exceeded |
| Android | `WorkManager` (periodic) | Min 15 min interval | Batched with other jobs, Doze-deferred |
| Android | Foreground service | Unbounded, but mandatory user-visible notification | Android 14+ requires declared `foregroundServiceType`; Android 15+ caps `dataSync` / `mediaProcessing` to 6h / 24h |

Never assume a background task runs on schedule. Assume it runs sometime within a window, possibly not at all that day.

## Selection Matrix

| Need | Pick | Reason |
|------|------|--------|
| Periodic sync (inbox, feed) | iOS `BGAppRefreshTask`, Android `WorkManager` periodic | Low priority, OS-batched, battery friendly |
| One-off deferred work (retry failed upload) | Android `WorkManager` one-time + constraints, iOS silent push → `BGAppRefreshTask` | Retries built in, respects Doze |
| Large upload/download | iOS `URLSession` background config, Android `WorkManager` + foreground service | Survives process death |
| User-initiated transfer visible to user | Android foreground service + notification | Android 12+ requires this; iOS uses `beginBackgroundTask` briefly |
| Precise timing (alarms, reminders) | Local notifications, not background tasks | Background tasks are never precise — use scheduled notifications |

## Scheduling Patterns

```swift
// iOS: BGTaskScheduler — register at launch, submit request, handle task
import BackgroundTasks

BGTaskScheduler.shared.register(forTaskWithIdentifier: "com.example.refresh", using: nil) { task in
    handleAppRefresh(task: task as! BGAppRefreshTask)
}

func scheduleAppRefresh() {
    let request = BGAppRefreshTaskRequest(identifier: "com.example.refresh")
    request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60)
    try? BGTaskScheduler.shared.submit(request)
}

func handleAppRefresh(task: BGAppRefreshTask) {
    scheduleAppRefresh() // always chain the next one
    let op = SyncOperation()
    task.expirationHandler = { op.cancel() }
    op.completionBlock = { task.setTaskCompleted(success: !op.isCancelled) }
    OperationQueue().addOperation(op)
}
```

```kotlin
// Android: WorkManager periodic with constraints
val constraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED)
    .setRequiresBatteryNotLow(true)
    .build()

val syncRequest = PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES)
    .setConstraints(constraints)
    .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 30, TimeUnit.SECONDS)
    .build()

WorkManager.getInstance(context).enqueueUniquePeriodicWork(
    "inbox-sync",
    ExistingPeriodicWorkPolicy.KEEP,
    syncRequest,
)
```

## Execution-Time Budgeting

Every background handler must:

1. Start a timer on entry. Bail cleanly at 80% of the budget (iOS: ~24 s of 30 s).
2. Do one thing. Periodic sync pulls the smallest delta that moves state forward — not a full refresh.
3. Persist progress incrementally so the next wake-up resumes from the checkpoint.
4. Call the completion callback on every exit path. Missing a callback on iOS accelerates throttling.
5. Record telemetry with the task identifier and outcome (`success`, `no_data`, `failed`, `timeout`).

## Doze, App Standby, Battery Saver

Android aggressively restricts background work in low-power states. Design for the worst case:

- **Doze (device idle)**: Work is deferred to maintenance windows, ~once per hour at first, stretching to several hours.
- **App Standby Buckets** (`active` / `working_set` / `frequent` / `rare` / `restricted`): unused apps fall to lower buckets and get quota cuts. `restricted` is a hard stop for most background APIs.
- **Battery Saver**: All discretionary jobs paused. Even `WorkManager` with connected constraint may wait.
- **Manufacturer overlays**: Xiaomi, Huawei, Oppo, OnePlus add on-top background kill policies; document known workarounds (battery-optimization exception prompt) and decide per-market.

iOS equivalents:

- **Background App Refresh toggle**: user-controlled, globally or per-app. If off, `BGAppRefreshTask` never runs.
- **Low Power Mode**: background refresh disabled system-wide.
- **Adaptive scheduling**: apps the user doesn't open lose budget over time. Solve with push-triggered refresh.

## Testing Strategies

| Technique | Platform | Use |
|-----------|----------|-----|
| `xcrun simctl launch --terminate-running-process <bundle> -BGTaskSchedulerDebug 1` + LLDB `e -l objc -- (void)[[BGTaskScheduler sharedScheduler] _simulateLaunchForTaskWithIdentifier:@"id"]` | iOS | Force a background refresh in Simulator |
| `adb shell cmd jobscheduler run -f <pkg> <jobId>` | Android | Trigger a specific WorkManager job |
| `adb shell dumpsys deviceidle force-idle` / `adb shell cmd battery unplug` | Android | Simulate Doze and battery-saver states |
| Maestro / Detox cold-start hook | Both | Assert handler registers on cold launch |
| Flipper / Perfetto trace | Both | Verify wake-up count and duration stay within budget |

Do not ship without running at least one forced-run under simulated low-power on each platform.

## Anti-Patterns

- ❌ Assuming a 15-minute periodic task actually runs every 15 minutes — iOS may skip for days.
- ❌ Holding a wake lock across a long network call — drains battery and trips OS throttling.
- ❌ Running indefinite background services on Android for analytics — violates Play policy and burns battery.
- ❌ Using a foreground service without a user-visible reason — Android 14+ will throw `ForegroundServiceTypeException`.
- ❌ Doing full-table sync on every background wake — budget-busts and causes OS to demote the app.
- ❌ Forgetting to chain the next `BGTaskScheduler` request from the handler — task silently stops running.
- ❌ Logging background execution only on success — throttling is diagnosed from the `failed`/`timeout`/`missing` cases.

## Handoff / Next Steps

- **To Gateway**: endpoints called from background context, idempotency keys, payload size targets (<100 KB preferred), retry/backoff contract.
- **To Sentinel**: list of background handlers, persistent stores touched from bg context, any foreground-service declarations and their `foregroundServiceType`.
- **To Beacon**: metric plan — wake-up count per day, success rate by bucket, duration histogram, timeout rate, per-manufacturer breakdown on Android.
- **To Radar**: test matrix — forced run, Doze-suspended run, Low Power Mode run, cold-start registration, permission-revoked path, budget-exceeded path, uninstall-reinstall persistence.
