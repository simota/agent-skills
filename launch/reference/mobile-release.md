# Mobile Release — TestFlight Phased Release and Play Staged Rollout

This reference covers the `mobile` Recipe: planning, executing, and halting mobile app store releases for pure-native iOS and Android builds handed off from `Native`.

Mobile differs structurally from web release on three axes:
1. **Rollback is not available.** Once a binary is delivered, only progressive halt + flag-based kill-switch can contain a regression.
2. **Store review is a Go/No-Go gate the team cannot accelerate.** Plan 24-72h for App Review / Play Review; assume worst case at submission time.
3. **The compliance surface is regulated.** Privacy Manifest (iOS), Data Safety (Android), Sign in with Apple, 5.1.2(i) AI disclosure, DSA trader status, EAA accessibility — submission is rejected without these, not just delayed.

## TL;DR — Mobile Release Checklist

Before triggering the `mobile` Recipe, validate the incoming `NATIVE_TO_LAUNCH_HANDOFF`:

- [ ] `privacy_manifest_complete: true` (iOS auto-rejects without `PrivacyInfo.xcprivacy` + Required Reasons API)
- [ ] `data_safety_complete: true` (Google Play blocks all tracks, including Internal Testing, since 2024)
- [ ] `feature_flags` includes at least one server-driven kill-switch per new user-facing feature (mobile cannot fast-roll back; flags are the rollback)
- [ ] 5.1.2(i) AI disclosure UI present when the app sends user data to third-party AI providers (effective 2025-11-13)
- [ ] Sign in with Apple offered alongside any third-party social login (Guideline 4.8)
- [ ] Crash-free sessions baseline from the prior version ≥ 99.85% (target for new release halt-trigger)
- [ ] Hotfix submission path tested (TestFlight expedited review request or Play Internal → Production fast-track)
- [ ] Server-driven flags wired and verified live in production with all new features shipped dark

Reject the handoff and route back to Native if any item fails.

## TestFlight Phased Release (iOS)

### Schedule

Phased Release shifts traffic in 7 days. Distribution is fixed by Apple; you cannot accelerate it. You can pause up to 30 days per release with no count limit, and any pricing / entitlement / auth / sync change MUST go through phased release.

| Day | Cumulative % |
|-----|---|
| 1 | 1% |
| 2 | 2% |
| 3 | 5% |
| 4 | 10% |
| 5 | 20% |
| 6 | 50% |
| 7 | 100% |

### Pipeline

```
TestFlight Internal (≤ 100 internal testers, immediate)
  ↓ verify no crashers / build errors, smoke test critical paths
TestFlight External (≤ 10,000 external testers, requires Beta App Review for first build of a version)
  ↓ collect 24-48h crash-free baseline and user feedback
App Review submission
  ↓ wait 24-72h (no SLA; budget 48h)
App Review approved → manual release OR auto-release
  ↓
Phased Release (7-day automated, can pause up to 30d)
  ↓ at any halt trigger: pause from App Store Connect or App Store Connect API
100% release
```

### Automation via App Store Connect API

- `POST /v1/appStoreVersions/{id}/relationships/appStoreVersionPhasedReleases` — start phased release
- `PATCH /v1/appStoreVersionPhasedReleases/{id}` with `phasedReleaseState=PAUSED` — halt
- `PATCH ... phasedReleaseState=ACTIVE` — resume
- `PATCH ... phasedReleaseState=COMPLETE` — push to 100%

Wire halt triggers to Crashlytics / Datadog / Bugsnag alerts via webhook → Lambda / Cloud Run → App Store Connect API call.

### Source

- [Release a version update in phases — Apple Developer](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/)
- [App Store Connect API — Apple Developer](https://developer.apple.com/documentation/appstoreconnectapi)

## Google Play Staged Rollout (Android)

### Schedule

Play Staged Rollout uses `userFraction` per track (Production / Open / Closed / Internal). You define the steps. Halt does NOT pull back users already updated; it stops further distribution.

Reference schedule:

| Step | userFraction | Observation window |
|------|---|---|
| Day 1 | 5% (0.05) | 24h |
| Day 2-3 | 20% (0.20) | 48h |
| Day 4-5 | 50% (0.50) | 48h |
| Day 6+ | 100% (1.0) | continuous |

Shrink the steps for high-risk releases (1% → 5% → 20% → 50% → 100% over 10-14 days).

### Pipeline

```
Internal Testing (≤ 100 testers, instant)
  ↓ smoke + Data Safety completeness
Closed Testing (alpha / beta groups, can be open-listed)
  ↓ 24-48h crash baseline
Open Testing (public opt-in)
  ↓ broader real-device coverage
Production Staged Rollout (5% → 20% → 50% → 100%)
  ↓ halt + hotfix via halt + new version push
```

### Automation via Android Publisher API

- `androidpublisher.edits.tracks.update` with body:
  ```json
  {
    "track": "production",
    "releases": [{
      "name": "1.2.3",
      "userFraction": 0.05,
      "status": "inProgress"
    }]
  }
  ```
- Set `status: "halted"` to halt the current rollout (already-updated users remain on new version)
- Set `status: "completed"` with `userFraction: 1.0` to promote to 100%

Trigger from CI on Crashlytics / Sentry / Datadog alert. Tools like `fastlane supply` wrap the API.

### Source

- [Release rollout to a percentage of users — Google Play Console Help](https://support.google.com/googleplay/android-developer/answer/6346149)
- [Android Publisher API — Tracks resource](https://developers.google.com/android-publisher/tracks)

## Halt Triggers (Both Platforms)

Define automated halt conditions before launch. Manual checking does not scale and adds 30+ min recovery time.

| Trigger | Threshold | Source signal |
|---------|-----------|---------------|
| Crash-free sessions | `< 99.85% for 1h` | Crashlytics / Sentry |
| App Not Responding (Android) | `ANR rate > 0.47% for 1h` | Play Vitals |
| P0 store-policy regression | Any rejection or policy strike | App Store Connect notification / Play Console policy email |
| Authentication failure rate | `> 5% for 15min` | Auth backend metric |
| Critical user flow conversion drop | `> 20% vs baseline for 1h` | Product analytics (Amplitude / Mixpanel / PostHog) |
| Payment / IAP failure rate | `> 2% for 30min` | StoreKit / Play Billing metric |
| Domain-specific KPI (e.g., ride completion, message delivery) | Owner-defined | Backend |

## Server-Driven Feature Flags as Primary Rollback

Mobile rollback is slower than web. **Feature flags are the kill-switch**, not the binary.

Requirements:
- **Streaming propagation ≤ 5 minutes**. Server-Sent Events (SSE) or WebSocket; long-poll over 5min is not a kill-switch. LaunchDarkly / Statsig / Unleash / Flagsmith provide streaming clients.
- **One kill-switch per new user-facing feature** at release time, wired to a kill-flag dashboard. Default state: enabled (or off for dark launch). Document the disable condition.
- **Test the kill path before submission**. Flip the flag on a TestFlight / Play Internal build; verify the fallback UI is reachable.
- **Cleanup ticket created with the flag**. Stale kill-flags become dead code. Default cleanup at 60 days post-100%-stable.

Example `LAUNCH_TO_NATIVE_HANDOFF.flag_disable_signals`:

```yaml
flag_disable_signals:
  - flag: "new_checkout_flow_v2"
    condition: "checkout_completion_rate < 90% for 1h OR P0 payment regression"
    action: "Fall back to v1 checkout via existing code path; cleanup ticket NATIVE-1234"
  - flag: "ai_summary_panel"
    condition: "5.1.2(i) consent UI bug reported OR third-party AI vendor outage"
    action: "Hide panel; show static help link"
```

## Reversible Migrations (Database, UserDefaults, DataStore)

A halted rollout leaves already-updated users on the new version. Non-reversible schema changes amplify the blast radius.

Required patterns:
- **Expand-Contract for schema**: add new columns / fields in this release, write to both old and new, switch reads to new in a follow-up release ≥ 2 versions later, drop old in release ≥ 4 versions later.
- **Dual-write for local stores**: write both `UserDefaults.legacy` and `UserDefaults.v2` until ≥ 90% are on the new version; then collapse.
- **Forward-compatible JSON**: never remove fields the old client reads; add new fields only.
- **CRDT / sync schema versioning**: include a `schema_version` field; old clients silently ignore future versions.

## Anti-Patterns

1. **Big Bang mobile release** — 100% from day 1 on either store. Combined with no feature flags, this is the single highest-cost release mistake.
2. **Manual halt-checking** — "I'll watch the dashboard". Wire automated alerts → halt API.
3. **Skipping Internal / Closed testing** — phased release does NOT replace internal smoke; it just slows the blast radius once a regression ships.
4. **Treating Fastlane Match as a stable Apple-managed primitive** — Apple removed the underlying API in May 2025; the project is functional via git-shared cert/profile but no replacement was provided. Use individual CI-server signing + `xcodes` / `tuist` / `sake` as alternatives for new projects.
5. **Phased release with non-reversible migrations** — halted rollout leaves updated users on a schema you cannot roll back.
6. **One flag for many features** — bundles unrelated rollback decisions. One kill-switch per feature.
7. **Skipping hotfix path testing** — when the regression hits at 50%, this is when you discover the expedited review request needs documentation you don't have.
8. **Wide-pin third-party domains** — TLS rotation by the third party kills your app without warning. Limit certificate pinning to first-party endpoints.

## App Review / Play Review Lead Time Budgeting

These are Go/No-Go gates the team cannot accelerate. Plan:

| Path | Typical | Worst-case |
|------|---------|------------|
| App Review (standard) | 24-48h | 7 days (rare, holiday windows) |
| App Review (expedited request) | 4-24h | 48h (granted ~50% of requests) |
| Play Review (first submission of an app) | 7 days | 14 days |
| Play Review (subsequent submissions) | 1-3 days | 7 days |
| Beta App Review (TestFlight External, first build of a version) | 24-48h | 5 days |

Schedule submission Mon-Wed to leave hotfix room before weekend. Avoid Fri / pre-holiday submission unless the rollout is non-time-sensitive.

## Source

- [Privacy Manifest — Apple Developer](https://developer.apple.com/documentation/bundleresources/privacy-manifest-files)
- [Data Safety section — Google Play Console](https://support.google.com/googleplay/android-developer/answer/10787469?hl=en)
- [App Store Review Guideline 5.1.2(i) — Apple Developer](https://developer.apple.com/news/?id=ey6d8onl)
- [LaunchDarkly: What is a kill switch?](https://launchdarkly.com/blog/what-is-a-kill-switch-software-development/)
- [Fastlane Match — Apple API removal discussion](https://github.com/fastlane/fastlane/issues/29469)
- [App Store Connect API — Phased Release](https://developer.apple.com/documentation/appstoreconnectapi/appstoreversionphasedreleases)
- [Android Publisher API — Tracks](https://developers.google.com/android-publisher/tracks)
