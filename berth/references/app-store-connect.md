# App Store Connect — Submission, Review Guidelines, Privacy

**Purpose:** iOS submission workflow, App Store Review Guidelines map, privacy declarations, TestFlight, and common rejection reasons.
**Read when:** Auditing or submitting an iOS build, or interpreting an iOS rejection.

> **Verify before asserting.** Apple revises the Review Guidelines, build/SDK deadlines, and the App Privacy taxonomy frequently. Everything below is a starting checklist. Confirm the current rule at the official source and state the "as of" date you used:
> - App Store Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
> - App Privacy details: https://developer.apple.com/app-store/app-privacy-details/
> - Required Reason API (Privacy Manifest): https://developer.apple.com/documentation/bundleresources/privacy-manifest-files

---

## Submission Workflow (App Store Connect)

1. **App record** — bundle ID, SKU, primary language, app name, subtitle.
2. **Build upload** — archive in Xcode (current required Xcode/SDK) → upload via Xcode Organizer / `xcodebuild` / Transporter. Build appears in App Store Connect after processing.
3. **Export compliance** — answer encryption usage (`ITSAppUsesNonExemptEncryption` in Info.plist short-circuits the prompt).
4. **App Privacy** — complete the data-collection questionnaire ("nutrition labels"). Blocks submission if absent.
5. **Age rating** — Apple age-rating questionnaire (e.g., violence, mature/suggestive themes, gambling, unrestricted web access).
6. **Pricing & availability** — price tier, storefront/country availability, pre-order if applicable.
7. **Listing** — description, keywords, support URL, marketing URL, screenshots, app previews, promotional text.
8. **App Review info** — demo account credentials (if any feature is behind login), contact, notes for reviewer.
9. **Version release** — Manually release / Automatically release / **Phased Release** (automatic-update rollout over 7 days — this is `Launch`'s rollout lever, not Berth's).
10. **Submit for Review.**

---

## Review Guidelines Map (top-level)

| Section | Theme | Frequent triggers |
|---------|-------|-------------------|
| **1. Safety** | Objectionable content, UGC moderation, kids category, physical harm, data security | 1.2 UGC needs filtering/reporting/blocking; 1.3 Kids Category restrictions |
| **2. Performance** | Completeness, beta content, accurate metadata, hardware compatibility | **2.1** crashes/bugs/placeholder/needs demo account; **2.3** inaccurate metadata/screenshots; 2.5 software requirements |
| **3. Business** | Payments, IAP, subscriptions, acceptable business models | **3.1.1** digital goods must use IAP; 3.1.2 subscription rules; 3.1.3 "reader"/external-purchase exceptions |
| **4. Design** | Minimum functionality, spam, sign-in, web clips | **4.2** minimum functionality (not just a website wrapper); **4.3** spam/duplicate; **4.8** Login Services (privacy-equivalent option) |
| **5. Legal** | Privacy, data use, intellectual property, gaming/contests, AI | **5.1.1** data collection & storage, purpose strings, **5.1.1(v)** account deletion; 5.1.2 data use/sharing; 5.2 IP |

---

## Common Rejection Reasons (iOS)

| Code | Reason | Remediation |
|------|--------|-------------|
| 2.1 | App Completeness — crash, bug, broken link, placeholder content, reviewer can't access gated features | Fix the defect; provide working demo account in App Review info; remove placeholder/"coming soon" content. |
| 2.3.x | Accurate Metadata — screenshots don't match app, misleading description, wrong category | Update screenshots to reflect real UI; align description; pick correct category. |
| 3.1.1 | Unauthorized payment — selling digital goods outside IAP | Route digital purchases through StoreKit IAP, or qualify for a documented external-purchase entitlement. |
| 4.2 | Minimum Functionality — too simple / website wrapper | Add native value beyond a webview; justify platform-specific functionality. |
| 4.3 | Spam — duplicate of an existing app or template farm | Differentiate or consolidate into one app. |
| 4.8 | Login Services — third-party login without a privacy-focused equivalent | Add an equivalent option (e.g., Sign in with Apple) meeting the data-minimization criteria. |
| 5.1.1 | Data Collection — missing/weak purpose strings, collecting before consent | Add specific `NS...UsageDescription` strings; gate collection behind consent; minimize. |
| 5.1.1(v) | Account Deletion — account creation without in-app deletion | Provide an in-app account-deletion path (not just "email us"). |
| 5.1.2(i) | AI/data sharing disclosure — sharing user data with third parties (incl. AI) without consent | Disclose and obtain consent; update App Privacy labels. |

---

## App Privacy & Privacy Manifest

- **App Privacy labels** — per data type: collected? linked to identity? used for tracking? purpose. Must match actual behavior (cross-check with `Cloak`'s data map).
- **Privacy Manifest (`PrivacyInfo.xcprivacy`)** — declares collected data types, tracking domains, and **Required Reason API** usage (e.g., `UserDefaults`, file timestamp, system boot time, disk space, active keyboard). Third-party SDKs must ship their own manifests + signatures. Missing Required-Reason declarations → automated rejection.
- **App Tracking Transparency (ATT)** — if you track across apps/sites, you must request permission via `ATTrackingManager` with `NSUserTrackingUsageDescription`.

---

## TestFlight

| Track | Testers | Review | Use |
|-------|---------|--------|-----|
| Internal | ≤ 100 (team members with roles) | No Beta App Review | Fast dogfooding |
| External | ≤ 10,000 | **Beta App Review** required (lighter than App Review) | Broader beta |

- Builds expire after 90 days. Provide test info / "what to test".
- TestFlight is for testing only — promote the same reviewed build concept to App Review for release.

---

## Review Timing & Expedited Review

- Most submissions reviewed within 24–48h (not guaranteed). Build this in; do not promise faster.
- **Expedited Review** — request for critical fixes / time-sensitive events; granted at Apple's discretion. Not a planning default.
- Rejections and dialogue happen in **Resolution Center**. Appeals go to the **App Review Board**. See `rejection-handbook.md`.
