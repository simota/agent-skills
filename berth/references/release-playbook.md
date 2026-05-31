# Submission Playbook — Tracks, Signing, Timeline

**Purpose:** Sequence testing tracks, signing prerequisites, build upload, reviewer access, and a review-lead-time-aware submission timeline.
**Read when:** Running the `submit` recipe or building the submission section of a readiness plan.

> Berth owns *submission sequencing*. The staged-rollout *percentages*, Go/No-Go scoring, versioning, and rollback are `Launch`'s — hand them off, don't duplicate.

---

## Signing Prerequisites (verify before upload)

| Platform | Check |
|----------|-------|
| iOS | Valid Apple Distribution certificate; App Store provisioning profile; correct bundle ID & entitlements (push, App Groups, associated domains, etc.); `ITSAppUsesNonExemptEncryption` set. |
| Android | Upload key enrolled in **Play App Signing**; AAB built (not APK); `applicationId` matches the Console record; release signing config correct. |

A signing/entitlement mismatch fails upload or processing — resolve before scheduling review.

---

## Testing-Track Sequence

### iOS
```
Internal TestFlight (≤100, no Beta App Review)
   → External TestFlight (≤10,000, Beta App Review ~lighter)
   → App Review submission (full)
   → Release: Manual | Auto | Phased (Launch decides the lever)
```

### Android
```
Internal testing (≤100, fast)
   → Closed testing (alpha)        ← new personal accounts: ≥12 testers, ≥14 days
   → Open testing (beta)
   → Production (staged rollout %)  ← Launch decides the %
```

Pick the **lowest track** that satisfies the validation need. Always run the Android **pre-launch report** before promoting.

---

## Reviewer Access (mandatory if anything is gated)

- Provide a **working demo account** (iOS: App Review Information; Android: App access credentials).
- Note any region lock, feature flag default, or hardware dependency the reviewer needs.
- If a feature is server-flag-gated, ensure the **reviewed state** is reachable — hiding the feature from review then enabling it remotely is a bait-and-switch rejection/termination risk.

---

## Review Lead Time (the fixed gate)

| Store | Typical | Notes |
|-------|---------|-------|
| App Review (iOS) | 24–48h | Not guaranteed; expedited review is discretionary |
| Beta App Review (TestFlight external) | hours–1 day | Lighter than App Review |
| Play review (closed/open/prod) | hours–days | Varies; new-account closed-testing window dominates first release |

**Rule:** treat review as a non-compressible block in the timeline. Never schedule a hard launch date that assumes faster-than-stated review.

---

## Submission Timeline (template)

```
T-? : Build uploaded & processed; signing verified
T-? : Privacy declarations complete (BLOCKER gate)
T-? : Internal track validated
T-? : External / closed track (+ Beta App Review iOS / 14-day closed if new Android account)
T-0 : Submit for App Review / promote to Production review
T+review_lead_time : Approval
T+approval : Release (hand rollout staging to Launch)
```

Output this with concrete dates and emit `BERTH_TO_LAUNCH_HANDOFF` so `Launch` attaches rollout %, halt triggers, and Go/No-Go.

---

## "What's New" / Release Notes

- Berth authors/validates the **store-listing** "What's New" text (per locale), requesting copy from `Prose` and keyword sensitivity from `Growth`.
- The engineering **CHANGELOG / stakeholder release notes** belong to `Launch`. Keep them aligned but don't duplicate ownership.

---

## Expedited / Hotfix Submission Path

- iOS: request **Expedited Review** for critical fixes (discretionary); or ship a server-flag mitigation if the build is already approved.
- Android: promote a fixed build through **Internal → Production** fast-track; halt the prior staged rollout first.
- A mobile hotfix is still gated by review — the only instant lever is a **server-driven feature flag**, which is `Launch`'s rollback mechanism. Coordinate, don't reinvent.
