# Cross-Platform Compliance Matrix

**Purpose:** Side-by-side iOS vs. Android compliance requirements and shared regulatory obligations.
**Read when:** Producing a unified readiness checklist or judging dual-platform scope.

> All thresholds/deadlines below are starting points. Verify against the live developer docs and record the "as of" date.

---

## Privacy Declarations

| Concern | iOS (Apple) | Android (Google) |
|---------|-------------|------------------|
| User-facing label | **App Privacy** "nutrition labels" in App Store Connect | **Data safety** section on the store listing |
| Manifest/SDK | **Privacy Manifest** (`PrivacyInfo.xcprivacy`) + Required-Reason APIs; third-party SDK manifests + signatures | SDK behavior must match Data safety; SDK Index transparency |
| Tracking consent | **ATT** (`ATTrackingManager`, `NSUserTrackingUsageDescription`) | Advertising ID declaration; user-resettable AAID; consent for sensitive data |
| Purpose strings | `NS...UsageDescription` per capability | Runtime permission rationale; prominent disclosure for sensitive perms |
| Accuracy rule | Labels must match real behavior | Form must match real + SDK behavior |

**Audit order:** declared data ⟷ actual data map (`Cloak`). A declared-vs-actual mismatch is the #1 hidden blocker.

---

## Account & Identity

| Requirement | iOS | Android |
|-------------|-----|---------|
| Third-party login parity | If you offer social/third-party login, must offer an equivalent privacy-focused option (Login Services / Sign in with Apple) | No equivalent mandate, but deceptive auth is a strike |
| Account deletion | **5.1.1(v)**: in-app account deletion required for account-creation apps | In-app deletion **+ web deletion URL** required |

---

## Ratings & Audience

| Concern | iOS | Android |
|---------|-----|---------|
| Age rating | Apple age-rating questionnaire | **IARC** content-rating questionnaire |
| Kids / Families | Kids Category (Guideline 1.3); stricter data/ads rules | Designed for Families; Target audience & content; Families ads SDK |
| Underage data | COPPA / GDPR-K parental consent | COPPA / GDPR-K; Families policy |

---

## Monetization

| Goods type | Rule (both stores) |
|------------|--------------------|
| Digital goods/services consumed in-app | Must use App Store IAP / Play Billing, unless a jurisdiction-specific external/alternative-billing entitlement applies |
| Physical goods/services | Use external payment (not store billing) |
| Subscriptions | Store subscription APIs; clear terms, restore, manage; auto-renew disclosure |
| External purchase links | EU DMA / US external-link rulings created entitlements — eligibility is conditional; verify per storefront |

**IAP product readiness (a common first-release blocker):** in-app purchase / subscription *products* are reviewed too, not just the binary.
- iOS: a new subscription's first submission typically requires the IAP product to be attached and submitted **with the build**, plus a localized review screenshot and metadata per product. Missing/unsubmitted products → rejection or "Missing Metadata".
- Android: Play Billing products (one-time / subscription with base plans & offers) must be configured and active in the Console; the subscription must be wired to a real purchase flow reachable by the reviewer.
- Both: prices, localizations, and tax/financial details must be complete before the product is purchasable in review.

---

## Technical Build Mandates

| Mandate | iOS | Android |
|---------|-----|---------|
| Build toolchain | Built with the currently required Xcode/SDK (Apple's annual deadline) | — |
| Bundle format | IPA via App Store Connect | **AAB** required for new apps |
| Signing | Apple distribution certificate + provisioning | **Play App Signing** (upload key + Google-held signing key) |
| API/SDK level | — | **Target API level** within one-year window of latest major release |
| Memory pages | — | **16 KB page size** support by Google's deadline |

---

## Regulatory Overlay (route specifics to `Comply` / `Clause`)

| Regulation | Region | Impact on store release |
|------------|--------|-------------------------|
| **COPPA** | US | Kids data handling, parental consent, ads restrictions |
| **GDPR / GDPR-K** | EU | Lawful basis, consent, data subject rights, kids protection |
| **DMA** | EU | Alternative app marketplaces / sideloading, external purchase, steering |
| **EAA** (European Accessibility Act) | EU | Accessibility conformance for in-scope apps |
| **CCPA/CPRA** | California | Opt-out of sale/share, privacy disclosures |
| **5.1.2(i) AI disclosure** | Apple guideline | Disclose + consent when sharing user data with third parties (incl. AI services) |

---

## Unified Readiness Checklist (template)

```
PRIVACY
[ ] iOS App Privacy labels complete & accurate vs data map
[ ] iOS Privacy Manifest Required-Reason APIs declared (incl. SDKs)
[ ] iOS ATT implemented if cross-app tracking
[ ] Android Data safety form complete & accurate vs data map
ACCOUNT
[ ] Third-party login parity (iOS Login Services)
[ ] In-app account deletion (iOS); in-app + web deletion (Android)
RATINGS
[ ] iOS age rating questionnaire; Android IARC done
[ ] Families/kids declarations if applicable
MONETIZATION
[ ] Digital goods via IAP / Play Billing (or valid entitlement)
[ ] Subscription terms/restore/disclosure
TECHNICAL
[ ] iOS built with required Xcode/SDK; valid signing/provisioning
[ ] Android AAB + Play App Signing; target API level; 16 KB support
PERMISSIONS
[ ] Sensitive permissions justified / declaration forms filed
LISTING
[ ] Screenshots/previews to spec; metadata accurate; reviewer demo account
REGULATORY
[ ] COPPA/GDPR-K/DMA/EAA obligations addressed (Comply)
DEADLINES
[ ] No upcoming hard deadline missed (target API / SDK / 16 KB)
```
