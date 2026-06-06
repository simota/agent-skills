# Dead Code Impact & Prevention

Purpose: business framing, operational risk reminders, prevention policies, and cleanup health metrics.

## Contents

1. Why dead code matters
2. Notable incidents
3. Prevention rules
4. Metrics to track

## Why Dead Code Matters

Dead code is not harmless. It expands attack surface, slows builds, increases bundle or payload size, adds cognitive load, and can be reactivated by configuration changes.

| Risk | Operational Impact |
|------|--------------------|
| Security exposure | Old libraries or unchecked paths remain available |
| Performance drag | Larger bundles, slower builds, more CI time |
| Cognitive load | Harder onboarding, debugging, and review |
| Maintenance waste | More files to test, review, and update |
| Reactivation risk | Disabled code can become live again unexpectedly |

## Notable Incidents

- **Knight Capital (2012):** stale flag-controlled code was reactivated, contributing to a catastrophic trading incident. Treat zombie code as risky, not dormant.
- **Meta SCARF:** large-scale automated cleanup showed that systematic graph-based removal can reclaim major engineering attention and code health.

## Prevention Rules

- Enforce YAGNI. Delete instead of keeping speculative code.
- Prefer deletion over long-lived commented-out code.
- Give feature flags a TTL and remove expired branches.
- Keep cleanup changes small and reviewable.
- Integrate dead-code detection into CI or scheduled maintenance.
- Track cleanup trends so false positives and regressions stay visible.

## Metrics To Track

| Metric | Target |
|--------|--------|
| Dead Code Rate | `< 5%` |
| Detection Accuracy | `> 80%` |
| False Positive Rate | `< 20%` |
| Time to Cleanup | `< 2 sprints` |
| Regression Rate After Cleanup | `< 1%` |

Record trend data in `SCAN_BASELINE` so cleanup quality can improve over time.
