# Usage Examples

**Purpose:** Representative use cases and output samples for the Native agent.
**Read when:** You need a reference for how to approach a task or shape the output.

---

## Example 1: Bootstrap a SwiftUI iOS app (Swift 6.3 / iOS 17+)

### User Request

Start a new iOS shopping app on Swift 6.3 with tab navigation (Home / Cart / Profile).

### Output Summary

- Xcode 26 project on iOS 17 deployment target
- SwiftUI `TabView` with three tabs (Home / Cart / Profile)
- `@Observable` ViewModel per feature
- `NavigationStack` + Coordinator per tab
- Swift Concurrency (`async`/`await`) for networking, default MainActor isolation
- Persistence via SwiftData (iOS 17+)

### Key Files

```
Sources/
├── App/
│   └── ShopApp.swift           # @main + TabView root
├── Features/
│   ├── Home/                   # HomeView, HomeViewModel, HomeCoordinator
│   ├── Cart/
│   └── Profile/
├── Core/
│   ├── Networking/             # APIClient (URLSession + async)
│   ├── Persistence/            # SwiftData ModelContainer
│   └── DesignSystem/           # Tokens, Buttons, etc.
└── PrivacyInfo.xcprivacy       # Required Reasons API declarations
```

### Handoff to Builder

```yaml
NATIVE_TO_BUILDER_HANDOFF:
  task: "Implement Home / Cart / Profile screens with @Observable ViewModels"
  pattern: "MV (View → @Observable ViewModel) + NavigationStack per tab"
  acceptance:
    - "Three tabs render and persist selection across cold launches"
    - "Cart count updates reactively when an item is added"
    - "All async work runs on MainActor by default"
```

---

## Example 2: Add Push Notifications (APNs + iOS 17+)

### User Request

Add push notifications to an existing SwiftUI app. Backend sends via APNs over HTTP/2.

### Output Summary

- `UNUserNotificationCenter.requestAuthorization` with a soft pre-prompt
- `application(_:didRegisterForRemoteNotificationsWithDeviceToken:)` handler
- Token registration / rotation against the `/devices` endpoint
- Foreground / background / terminated routing
- Deep link integration into the existing `NavigationStack`
- `NotificationServiceExtension` to log `delivered`

### Pre-Prompt Copy (English)

```
Title:    Stay updated on your orders
Message:  We'll send notifications about order status and delivery updates.
          You can change this anytime in Settings.
Allow:    Turn on notifications
Decline:  Not now
```

### Handoff to Gateway

- Token registry contract (`POST /devices`, `PATCH /devices/:id`, `DELETE /devices/:id`)
- Payload schema with mandatory `campaignId`
- Delivery / open analytics endpoints

---

## Example 3: Offline-First Field App (Android Kotlin / Jetpack Compose)

### User Request

Field-work logging app for Android. Must keep working in areas without cell coverage.

### Output Summary

- Single-source-of-truth `Repository` backed by Room 2.7
- Write queue persisted to Room, drained by `WorkManager` periodic + network-restore one-time work
- Image cache via Coil 3 disk cache
- Sync indicator UI driven by a `StateFlow<SyncState>` (idle / syncing / pending / error)
- Conflict resolution: Last-Write-Wins with explicit user confirmation

### Handoff to Builder

```yaml
NATIVE_TO_BUILDER_HANDOFF:
  task: "Implement field log Repository with offline write queue"
  pattern: "Repository → WorkManager + Room"
  acceptance:
    - "App works fully offline; no error toasts on no-network"
    - "Pending writes flush within 10 seconds of network restore"
    - "Conflicts surface a confirm dialog before overwriting"
```

---

## Example 4: SwiftUI In-App Purchase (StoreKit 2)

### User Request

Add a monthly subscription to a SwiftUI app using StoreKit 2.

### Output Summary

- `Product.products(for:)` to load offerings
- `Product.purchase()` flow with `VerificationResult` handling
- Subscription lifecycle management (active / grace / expired)
- Trial period handling with explicit pre-purchase disclosure
- Persistence and restore via `Transaction.currentEntitlements`
- Integration point for App Store Server Notifications v2

### Compliance Checks

- Restore button placed on Settings screen
- Auto-renewal disclosed before purchase
- Local currency from `Product.displayPrice`
- Privacy Manifest declares purchase data category

---

## Example 5: Pre-Submission Compliance Review (App Store)

### User Request

Run a guideline compliance check before submitting to the App Store.

### Output Summary (checklist form)

| Item | Status | Note |
|------|--------|------|
| PrivacyInfo.xcprivacy present | OK | Required Reasons API declared |
| Privacy Nutrition Labels match implementation | OK | Verified in App Store Connect |
| ATT prompt before IDFA usage | N/A | App does not use IDFA |
| StoreKit 2 IAP only (no external payment links) | OK | StoreKit 2 + Restore button |
| Subscription terms shown pre-purchase | OK | Term, price, auto-renewal disclosed |
| Age rating questionnaire complete | OK | 5-tier (2026-01-31 update) |
| 5.1.2(i) AI disclosure (if applicable) | OK | Foundation Models disclosed |
| Crash-free sessions baseline | OK | 99.92% on TestFlight External |
| Cold-start P95 | WARN | 2.4s on iPhone 12 mini — investigate |
| Built with Xcode 26 + iOS 26 SDK | OK | Required from 2026-04-28 |

### Handoff to Launch

- CHANGELOG draft attached
- Phased Release plan: 1% → 100% over 7 days
- Feature flags: `new_checkout` (default OFF), `live_activities` (default OFF)
- Rollback plan: Halt + flag OFF + Hotfix
