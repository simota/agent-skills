# Migration Roadmap (ROADMAP phase)

Translate the parity matrix and architecture map into a phased, shippable, reversible plan. The roadmap is the agreement between Port and the implementer agents (`Native`, `Scaffold`, `Launch`).

> **2026-05 fixed-date constraints to weave into the roadmap:**
> - Xcode 26 + iOS 26 SDK already required for App Store Connect uploads (since **2026-04-28** — no exceptions, no extensions).
> - Apple 5-tier Age Rating questionnaire already enforced (since **2026-01-31** — App Store Connect blocks unanswered apps).
> - Google Play 16KB-page-size compliance hard cutoff **2026-05-31** (extension window closing this month).
> - Google Play **targetSdk 36** mandatory from **2026-08-31** for new apps and updates (Wear OS / TV / Auto stay on 35).
> - EU AI Act GPAI enforcement powers from **2026-08-02**; Article 50 transparency labeling applicable.
> - WWDC 2026: **2026-06-08 to 2026-06-12** — iOS 27 / iPadOS 27 / macOS 27 announcement window; may shift target OS recommendation for P2/P3.

---

## Default Phasing

```
Phase 0: Foundations
  → Skeleton, CI, design system primitives, telemetry, crash reporting
Phase 1: MVP (parity ~40-50%)
  → Auth, primary value-prop, push, deep links, T1 offline, observability
Phase 2: Parity (parity ~80-90%)
  → Secondary flows, settings, advanced search, T2 offline where needed
Phase 3: Enhancement
  → Power-user features, multi-window/foldable, IAP advanced, web-shutdown if applicable
```

> 3-5 phases is normal. 7+ phases means the plan is over-detailed; re-cluster.

---

## Phase 0: Foundations

| Workstream | iOS | Android | Owner |
|-----------|-----|---------|-------|
| Project skeleton | Xcode workspace + SPM packages, App target, Widget target if applicable | Gradle multi-module, `:app` + `:core:*` + `:feature:*` | `Scaffold` |
| CI/CD | GitHub Actions / Xcode Cloud / Fastlane Match for signing | GitHub Actions / Fastlane / Gradle Play Publisher | `Gear` |
| Design system primitives | DesignSystem package: tokens, base components, typography, color | `:core:designsystem` module: M3 theme, tokens | `Muse` + `Vision` |
| Networking + auth scaffolding | URLSession client + Keychain + interceptor + refresh logic | Retrofit + OkHttp + EncryptedSharedPreferences + Auth Interceptor | `Native` |
| Crash reporting | Firebase Crashlytics or Sentry | Same | `Native` |
| Analytics | Configurable SDK | Configurable SDK | `Pulse` + `Native` |
| Feature flags | LaunchDarkly / Unleash / native | Same | `Native` |
| Localization scaffolding | `Localizable.strings` / `String Catalog` | `strings.xml` + per-locale resources | `Polyglot` |
| App icons + launch | Asset Catalog | `mipmap` + adaptive icon | `Native` |
| Privacy manifest (iOS) | `PrivacyInfo.xcprivacy` per first/third party | — | `Cloak` + `Native` |
| Data safety form (Android) | — | Play Console form | `Cloak` + `Launch` |
| Min-OS / capabilities config | `Info.plist`, `entitlements`, capabilities | `AndroidManifest.xml`, `permissions` | `Native` |

Phase 0 must conclude with both apps installable from internal distribution (TestFlight / Play Internal Testing) showing a placeholder home screen and an authenticated network call.

---

## Phase 1: MVP

Scope:
- All `Full` and `Adapted` features marked `P1` in the parity matrix.
- Auth (login, logout, refresh, biometric re-auth, deep-link auth recovery).
- Primary navigation (tabs / nav bar) + 1-2 detail flows.
- Push notifications (transactional baseline).
- Deep links for primary entry points.
- Offline T1 for read-heavy domains.
- Localization for launch locales.
- Telemetry for top funnels.

Exit criteria:
- Both stores accept beta builds.
- Crash-free sessions ≥ 99.5% in beta.
- Cold start ≤ 2.5s on baseline device (iPhone 13 / Pixel 6).
- Auth happy path + 2 critical edge cases (expired token, network drop) verified on both platforms.
- A11y baseline: VoiceOver / TalkBack labels on all primary interactive elements.

Owner agents: `Native` (impl), `Voyager` (E2E), `Radar` (unit/integration), `Launch` (beta release), `Polyglot` (i18n).

---

## Phase 2: Parity

Scope:
- All remaining `Full` and `Adapted` features marked `P2`.
- T2 offline writes for any domain that needs it.
- Advanced search, filters, sorting.
- Settings completeness (notification prefs, language, theme, account management, data export).
- IAP if applicable.
- Sign in with Apple (mandatory if any third-party login present).

Exit criteria:
- App approaches "feels complete" — no obvious web-only feature missing for the average user.
- Crash-free sessions ≥ 99.85% in production.
- Store rating ≥ 4.0 (or unchanged from web baseline).
- Customer support ticket rate not elevated vs web baseline.

Owner agents: `Native`, `Voyager`, `Launch`, `Voice` (feedback), `Bond` (engagement triage).

---

## Phase 3: Enhancement

Scope:
- `Deferred` items from the parity matrix.
- Multi-window / foldable / iPad split-view layouts.
- Advanced media (camera, video).
- Power-user features.
- Optional: web-shutdown if applicable.

Exit criteria depend on product priorities.

---

## Web-Shutdown Gating

If the goal is to retire the web app, the roadmap must include a shutdown gate. Otherwise omit this section.

| Gate | Criterion | Owner |
|------|-----------|-------|
| Mobile install rate | ≥ X% of MAU on mobile native (target 80%+) | `Pulse` |
| Mobile session frequency | ≥ baseline web session frequency | `Pulse` |
| Mobile crash-free | ≥ 99.85% sustained 30 days | `Native` + `Beacon` |
| Mobile NPS | ≥ web NPS | `Voice` |
| Mobile parity | All `Full` + `Adapted` `P1`+`P2` features in production | `Port` (verify) |
| Web feature parity for shutdown candidates | Mobile covers all features the shutdown list assumes | `Port` (verify) |
| Comms | 90-day shutdown notice with email + in-product banner | `Launch` + `Prose` |
| Migration assistance | In-product guide to install mobile + transfer data + login | `Native` + `Prose` |
| Support readiness | Support team trained on mobile-only flows | `Launch` |

Stage shutdown:
1. Soft notice (90 days out): banner + email.
2. New-user gate (30 days out): block new web signups.
3. Read-only mode (7 days out): web becomes read-only, write paths route to mobile.
4. Shutdown: web returns 410 Gone or redirect to a static "we've moved to mobile" page.

Each step is reversible until step 4.

---

## Store Submission Timeline

| Step | iOS | Android |
|------|-----|---------|
| Internal beta | TestFlight Internal (immediate) | Play Internal Testing (immediate) |
| External beta | TestFlight External (~24 hr review on first build) | Play Closed / Open Testing (~hours-day) |
| Production review | App Review (~24-72 hr typical, longer for novel apps) | Play Console review (~hours-day, longer for sensitive permissions) |
| Phased rollout | "Phased Release" 1%/10%/50%/100% over 7 days | Play "Staged Rollout" 5%/20%/50%/100% |
| Hotfix | Expedited review (rare; gate carefully) | Increment versionCode and re-release |

Plan for at least one rejection cycle per store on first submission. Common reasons: privacy manifest missing third-party SDK, Sign in with Apple missing, IAP rules violation, restricted content.

---

## Rollback Strategy

| Issue | Rollback move |
|-------|---------------|
| Critical bug after release | Halt staged rollout (both stores support pause); push hotfix |
| Auth break | Server-side rotate keys; ship hotfix; consider feature-flag downgrade |
| Crash regression | Pause rollout; revert via store ("revert to previous version" Android, expedited new build iOS) |
| Server-side incompatibility | Server rolls back; client tolerates older API via versioning |
| Offline corruption | Ship migration; if data-loss risk, ship a "reset local cache" toggle |
| Store policy violation in production | Pull binary; respond to store rejection; ship corrected build |

Mobile rollback is slower than web. **Server-driven feature flags** are the primary mitigation — every Phase-1 risky feature ships behind a flag with a kill switch.

---

## Risk-Aware Phasing

For each `risk-assessment.md` row with high probability × impact, pin a mitigation phase:
- High-risk dependency on a third-party SDK → resolve in Phase 0.
- Auth flow that changes API contract → mock API in Phase 0, real in Phase 1.
- Push backend redesign → ship server changes Phase 1; mobile ships Phase 1.
- IAP migration of existing web subscribers → Phase 2; coordinate with Legal.

---

## Output Skeleton

```markdown
# Migration Roadmap: <App Name>

## Phasing Summary
- P0: Foundations (X weeks)
- P1: MVP (X weeks)
- P2: Parity (X weeks)
- P3: Enhancement (X weeks)

## Phase 0 — Foundations
- Workstreams: …
- Exit: TestFlight Internal + Play Internal builds installable

## Phase 1 — MVP
- Scope: [parity-matrix P1 items]
- Exit criteria:
  - Crash-free ≥ 99.5%
  - Cold start ≤ 2.5s
  - Auth + push + deep links verified
- Owner agents: Native, Voyager, Launch

## Phase 2 — Parity
- Scope: [parity-matrix P2 items]
- Exit: …

## Phase 3 — Enhancement
- Scope: [parity-matrix Deferred items]

## Web Shutdown (optional)
- Gates: install %, parity verification, NPS, support readiness
- Steps: soft notice → new-user gate → read-only → shutdown

## Store Submission
- iOS: TestFlight → External → App Review → Phased Release
- Android: Internal → Closed → Open → Production Staged Rollout

## Rollback
- Server feature flags as primary mitigation
- Per-risk pinned mitigations: [list]

## Per-phase exit gates
| Phase | Gate | Owner |
| …     | …    | …     |
```

Consumed by `Launch`, `Native`, `Pulse`, `Voice`.
