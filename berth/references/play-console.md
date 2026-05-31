# Google Play Console — Submission, Policies, Data Safety

**Purpose:** Android submission workflow, Developer Program Policy map, Data safety, testing tracks, technical mandates, and common policy strikes.
**Read when:** Auditing or submitting an Android build, or interpreting a Play policy strike.

> **Verify before asserting.** Google revises policies, target API mandates, and testing-access requirements on a rolling basis. Confirm the current rule at the official source and state the "as of" date:
> - Developer Program Policies: https://play.google.com/about/developer-content-policy/
> - Data safety: https://support.google.com/googleplay/android-developer/answer/10787469
> - Target API level: https://support.google.com/googleplay/android-developer/answer/11926878

---

## Submission Workflow (Play Console)

1. **App record** — app name, default language, app/game category, free/paid.
2. **App bundle** — upload **AAB** (Android App Bundle; required for new apps). Play generates per-device APKs via **Play App Signing** (Google holds the app signing key; you keep the upload key).
3. **Store listing** — short & full description, app icon, feature graphic, phone/tablet screenshots, optional promo video.
4. **App content (Policy declarations)** — Privacy policy URL, Ads, App access (login credentials for review), **Content rating (IARC questionnaire)**, Target audience & content, Data safety, Government apps, Financial features, Health apps, News.
5. **Data safety form** — collected/shared data types, purposes, encryption-in-transit, deletion mechanism. Blocks submission across all tracks if absent.
6. **Choose track** — internal / closed / open / production. Run **pre-launch report** (automated device testing).
7. **Release** — set **staged rollout** percentage for production (this % lever is `Launch`'s, not Berth's). **Managed publishing** lets you batch and time-control going live.

---

## Testing Tracks

| Track | Testers | Review | Use |
|-------|---------|--------|-----|
| Internal | ≤ 100 | Fast (minimal) | Quick internal builds |
| Closed | Configurable lists | Reviewed | Alpha / structured QA |
| Open | Public opt-in | Reviewed | Public beta |
| Production | All users | Full review | Live |

> **New personal developer accounts** (created from late 2023 onward) must run **closed testing with ≥ 12 testers for ≥ 14 continuous days** before requesting production access. This dominates first-release timelines — surface it at intake.

---

## Developer Program Policy Map (top-level)

| Category | Examples |
|----------|----------|
| Restricted Content | Sexual content, hate speech, violence, illegal activities, gambling rules |
| Privacy, Deception & Device Abuse | Data handling, Permissions & APIs that access sensitive info, deceptive behavior, malware, mobile unwanted software |
| Monetization & Ads | Payments (Play Billing for in-app digital goods), subscriptions, disruptive ads, families ads |
| Store Listing & Promotion | Metadata, ratings/reviews manipulation, impersonation |
| Families | Designed for Families, target audience, content rating, ads SDK requirements |
| Spam & Minimum Functionality | Broken/limited functionality, repetitive content |

---

## Common Policy Strikes / Rejections (Android)

| Area | Reason | Remediation |
|------|--------|-------------|
| Data safety mismatch | Declared data practices don't match observed/SDK behavior | Reconcile the form with the actual data map (`Cloak`); declare all SDK-collected data. |
| Sensitive permissions | Background location, All files access, SMS/Call Log, exact alarm, package visibility without justification | Remove if unused; file the declaration form; use scoped alternatives (Photo Picker, scoped storage). |
| Broken functionality | Crashes in pre-launch report, login not working for reviewer | Fix; provide working App access credentials. |
| Misleading store listing | Screenshots/description don't match app | Align listing with actual app. |
| Account deletion | Account creation without in-app + web data deletion | Provide in-app deletion and a web deletion URL. |
| IAP bypass | Digital goods sold outside Play Billing | Use Play Billing, or a qualifying external/alternative billing program. |
| Families / content rating | Wrong target audience, ads SDK not Families-compliant | Re-run IARC, set correct audience, swap to compliant ads SDK. |

---

## Technical Mandates (verify current values)

| Mandate | Note |
|---------|------|
| **AAB** | New apps must publish as Android App Bundle, not APK. |
| **Play App Signing** | Required for new apps; safeguards the app signing key. |
| **Target API level** | Must target within one year of the latest major Android release; annual deadline for new apps/updates with possible extensions. Below the threshold → can't submit updates (and discoverability limits for existing apps). |
| **16 KB page size** | Apps targeting recent Android versions must support 16 KB memory page sizes (native libraries) by Google's stated deadline. |
| **Permissions declarations** | Background location, All files access, exact alarm, photo/video, health, accessibility — each has a declaration/justification flow. |
| **Account deletion** | In-app deletion + a publicly reachable web deletion URL for apps with account creation. |

---

## Permissions That Trigger Extra Review

- `ACCESS_BACKGROUND_LOCATION` — declaration form + prominent disclosure.
- `MANAGE_EXTERNAL_STORAGE` (All files access) — strong justification; prefer scoped storage / Photo Picker.
- `SCHEDULE_EXACT_ALARM` — limited to eligible use cases.
- `QUERY_ALL_PACKAGES` — limited to eligible use cases.
- `READ_SMS` / `READ_CALL_LOG` — only for default handler use cases.
- Health Connect, Accessibility API — purpose-restricted; misuse is a common strike.

---

## Pre-Launch Report

Automated install + crawl on real devices: surfaces crashes, ANRs, accessibility, security, and performance issues *before* review. Treat its findings as pre-submission blockers.
