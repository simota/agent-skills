# Staged Release & Rollout (Pure-Native)

**Purpose:** Pure-native iOS / Android release strategy — TestFlight Phased Release and Play Console Staged Rollout, server-driven Feature Flags, Halt + Hotfix.
**Read when:** Planning a release, designing a staged rollout, handling rollback, or executing an emergency hotfix.

> **Important:** In a pure-native environment, **OTA cannot update native code**. CodePush / EAS Update / Shorebird are React Native / Flutter only and out of scope here. For native, the rollback strategy centers on the combination of "**Phased Release** (iOS) / **Staged Rollout** (Android) + server-driven Feature Flags."

---

## Release-layer overview

```
[ Server (always rollback-able) ]
   ├─ Feature Flags (LaunchDarkly / Unleash / OSS)  ← primary kill switch
   ├─ Backend API (versioned, can revert independently)
   └─ Mobile API contract (BFF)

[ Client (slow rollback, store-mediated) ]
   ├─ App Binary (IPA / AAB)
   ├─ TestFlight Phased Release (iOS) / Staged Rollout (Android)
   └─ In-app remote config (assets / copy / pricing)
```

**Principle:** Client-side rollback is slow. Make server-driven Feature Flags the primary line of defense and store mechanisms the secondary line.

---

## iOS — TestFlight + Phased Release

### TestFlight tiers

| Stage | Audience | Review |
|-------|----------|--------|
| TestFlight Internal | Dev team (Apple Developer Program members, max 100) | Instant |
| TestFlight External | External testers (max 10,000) | First build undergoes ~24h Beta App Review |
| App Review | Public release review | Typically 24-72h, longer for new categories |

### Phased Release

Enabling "Phased Release for Automatic Updates" in App Store Connect spreads delivery to auto-update users **over 7 days** at 1% / 2% / 5% / 10% / 20% / 50% / 100%.

| Day | Auto-update % |
|-----|---------------|
| 1 | 1% |
| 2 | 2% |
| 3 | 5% |
| 4 | 10% |
| 5 | 20% |
| 6 | 50% |
| 7 | 100% |

Note: Manual updates (a user tapping Update in the App Store) bypass this throttle.

### Pausing / rolling back a Phased Release

- **Pause Phased Release** can be triggered at any time — halts auto-delivery to remaining users.
- Re-publish an older version by overwrite (a new build number with the same functionality = "rollback build").
- True rollback (reverting to the prior binary) is not provided. The accepted form is to **re-release the previous version's behavior in a new build**.
- Expedited Review can be requested — use only for severe issues; abusing it makes future requests more likely to be denied.

### Phased Release is unavailable for a brand-new app's first release

Phased Release is a feature for "auto-updates to existing users." It does not apply to first submissions, so the initial release is a normal (immediate-to-everyone) release.

---

## Android — Play Console Staged Rollout

### Track tiers

| Track | Audience | Review |
|-------|----------|--------|
| Internal Testing | Internal team (max 100) | Instant (minutes) |
| Closed Testing | Invitation-only (testers list) | Hours to 1 day |
| Open Testing | Public beta | Hours to 1 day |
| Production | Public | Typically hours to 1 day; first submissions or regulated categories take longer |

### Staged Rollout

Pick "Staged rollout" when shipping to Production and choose a percentage. Example:

| Step | % | Rough duration |
|------|---|----------------|
| 1 | 5% | 24-48h (watch Vitals) |
| 2 | 20% | 48-72h |
| 3 | 50% | 48-72h |
| 4 | 100% | — |

### Halting a Staged Rollout / partial release

- **Halted release** stops the rollout (remaining users stay on the previous version).
- "Resume" lets you continue at the same or a different percentage.
- True rollback: **re-release the same APK / AAB with an incremented versionCode** (Play Console rejects re-uploading the older versionCode). Rebuild from the "revert commit" with an incremented version code.

### Hotfix delivery

- Submit a hotfix as a new production release. Either ship Staged Rollout immediately at 100%, or ramp 5% → 20% while monitoring.

---

## Server-driven Feature Flags (primary defense)

Native rollback is slow, so Feature Flags are the real kill switch.

### Provider candidates

| Provider | Notes |
|----------|-------|
| LaunchDarkly | Enterprise, complete SDKs, multi-language coverage |
| Unleash | OSS, self-hostable, broad SDK lineup |
| Statsig | Experiment integration, free tier available |
| Firebase Remote Config | Free, integrated into the Firebase ecosystem, A/B tie-in |
| In-house | Backend API + simple HTTP fetch + cache |

### Design principles

- **Flag every high-risk feature** — auth flows, IAP, push receive logic, CRDT sync, AI calls.
- **Default = OFF** is the safe side. Treat fetch failure / timeout as OFF.
- Allow **per-platform / per-version** segmentation (if the bug only affects iOS 17, turn it off only on iOS 17).
- **Flag fetch timeout:** never block app launch by hundreds of milliseconds.
- **Removal flow:** track each flag with a "Sunset Date" and delete it once stable.

```swift
// iOS example — fetch flags once at launch with a sound fallback
@Observable
final class FeatureFlags {
    private(set) var newCheckoutEnabled = false  // default OFF

    func refresh() async {
        let timeout: TimeInterval = 0.4
        do {
            let result = try await withTimeout(timeout) {
                try await flagsClient.fetch()
            }
            newCheckoutEnabled = result.bool("new_checkout") ?? false
        } catch {
            // On timeout, keep OFF
        }
    }
}
```

```kotlin
// Android example
class FeatureFlags(private val client: FlagsClient) {
    private val _newCheckoutEnabled = MutableStateFlow(false)  // default OFF
    val newCheckoutEnabled: StateFlow<Boolean> = _newCheckoutEnabled.asStateFlow()

    suspend fun refresh() {
        try {
            withTimeout(400) {
                _newCheckoutEnabled.value = client.fetch().bool("new_checkout") ?: false
            }
        } catch (e: Exception) {
            // keep current value (or default OFF)
        }
    }
}
```

---

## Staged Rollout monitoring checklist

| Metric | Threshold | Action |
|--------|-----------|--------|
| Crash-free sessions | < 99.5% | Consider Halt + Hotfix |
| Crash rate (per session) | > 0.5% | Halt + investigate |
| ANR rate (Android) | > 0.5% | Halt + investigate |
| Cold start P95 | > 4 s | Investigate |
| Auth error rate | > baseline 2× | Turn auth flag OFF |
| API error rate (5xx) | > baseline 2× | Server-side investigation + consider client flag OFF |
| Store rating | > -0.3 vs baseline | Read reviews while investigating |

Monitoring tools:
- iOS: MetricKit, Crashlytics / Sentry, Xcode Organizer
- Android: Android Vitals, Crashlytics / Sentry, Firebase Performance

---

## Rollback decision tree

```
Staged Rollout for new version
      ↓
Monitor first N% (iOS: 1% phased / Android: 5%)
      ↓
Crash spike / ANR spike / severe error?
   ├─ YES → Halt immediately (both stores support this)
   │         ↓
   │       Can a Feature Flag turn the offending feature OFF?
   │         ├─ YES → Flag OFF + prepare fix build
   │         └─ NO  → Hotfix release (version bump + new build)
   │
   └─ NO → Wait 24h → Error rate climbing?
              ├─ YES → Pause + investigate
              └─ NO  → Advance to next %
```

---

## Hotfix release procedure

| Step | iOS | Android |
|------|-----|---------|
| 1. Halt current release | Pause Phased Release in App Store Connect | Halt rollout in Play Console |
| 2. Flag OFF | If possible, disable the feature via server Feature Flag | Same as left |
| 3. Fix commit | Bug fix only, minimal scope | Same as left |
| 4. Build / versionCode | Bump build number | Bump versionCode |
| 5. Re-submit | App Review (request Expedited Review if needed) | Create a new release in Play Console |
| 6. Roll out | Smoke test in TestFlight Internal → brief External → Phased Release in Production (or 100% immediately in emergencies) | Internal → Closed if needed → Production staged or 100% |

---

## CHANGELOG / Release Notes

The `Launch` agent generates and manages release notes. Native hands over the changes in structured form:

```yaml
NATIVE_TO_LAUNCH_RELEASE_HANDOFF:
  app_version: "2.4.0"
  ios_build: "2400"
  android_version_code: 2400
  changes:
    user_facing:
      - "Real-time inventory display on the new order screen"
      - "Live Activities for delivery tracking"
    fixes:
      - "Re-login flow when the auth token expires"
    technical:
      - "Migrated to Swift 6.2 Approachable Concurrency"
      - "Adopted Compose BOM 2025.05 + Material 3 Expressive"
  feature_flags_for_kill_switch:
    - name: "live_activities"
      default: false
      ramp_plan: "1% → 25% → 100% over 7 days"
    - name: "new_order_screen"
      default: true
      can_revert_via_flag: true
  rollout_plan:
    ios: "TestFlight Internal → External (48h) → App Review → Phased Release"
    android: "Play Internal → Open Testing (48h) → Production staged 5/20/50/100"
  rollback_strategy:
    primary: "Feature flag OFF for live_activities and new_order_screen"
    secondary: "Halt phased release / staged rollout"
    tertiary: "Hotfix build with revert"
```

---

## Anti-patterns

- **Assuming OTA can update native code.** Impossible in pure-native. Do not import React Native / Flutter assumptions.
- **Bolting on flags at the last minute.** Flags wired in just before rollout produce flag-broken bugs. Write flags alongside the feature.
- **Phased Release at 100% immediately.** Except in emergencies, always ramp. The point of 1% is to surface problems early.
- **Overwriting with a new binary without halting.** Users left on the broken old version remain. **Halt first.**
- **Stopping at TestFlight Internal.** Internal skews to insiders and finds few defects. Use Closed / External to cover diverse devices and networks.
- **Not aiming for 99.85% crash-free.** Falling below industry benchmarks collapses app ratings.

---

> Pure-native cannot escape via OTA. Make Feature Flags the primary line of defense, Staged Rollout the secondary, and Hotfix the last resort.
