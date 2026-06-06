# Push Notifications Reference (Pure-Native)

Purpose: Wire production-grade push notifications across APNs (iOS) and FCM (Android). Covers the full token lifecycle, soft pre-prompt permission UX, payload shape, Live Activities (iOS), Notification Channels (Android), delivery-receipt analytics, and rate/quota limits. Goal: notifications that reach the right device, at the right time, without triggering opt-out.

## Scope Boundary

- **Native `push`**: production push pipeline on the client — token registration/rotation/revocation, permission UX, payload handlers, silent push, Live Activities, Notification Channels, analytics, quota discipline.
- **Forge `mobile`**: prototyping push UX. Tokens are faked, permissions are stubbed, no real APNs/FCM wiring.
- **Sentinel**: audits push for exposed API keys, insecure token storage, and payload-based injection. Native consumes Sentinel findings but does not perform the audit.
- **Gateway**: server-side push delivery API — APNs p8 key handling, FCM v1 HTTP, token registry schema, fan-out, batching, retries. Native calls Gateway; Native does not design the server endpoint.

Rule of thumb: if the concern is "does the device handle the payload correctly?" → `push`. If it is "does the server deliver correctly?" → Gateway.

> Out of scope: React Native push, Flutter push, Web Push. Pure-native APNs / FCM only.

## Token Lifecycle

| Stage | Trigger | Client Action | Server Contract |
|-------|---------|---------------|-----------------|
| Register | First permission grant or app install | Request APNs/FCM token, POST to `/devices` | Idempotent upsert keyed by `(userId, installId)` |
| Rotate | OS reissues token (reinstall, restore, token refresh callback) | Detect via `onTokenRefresh` / `didRegisterForRemoteNotifications`, PATCH `/devices/:id` | Replace stale token, preserve topic subscriptions |
| Revoke | Logout, permission revoked, uninstall signal | DELETE `/devices/:id` (logout path) | Mark inactive; stop targeting |
| Reconcile | App foreground, weekly heartbeat | Compare local token hash vs server record | Detect drift caused by silent token swaps |

Never treat the token as stable across sessions. Always re-fetch on cold start and diff against the last known hash.

## Permission UX

Ask at the moment of value, not at launch. iOS denial is sticky — recovery requires sending the user to Settings.

```
App launch
  ↓
User completes a relevant action (posts, subscribes, enables alerts)
  ↓
Pre-prompt screen: explain the value in 1 sentence, show 1 example payload
  ↓
System prompt (UNUserNotificationCenter.requestAuthorization / NotificationManagerCompat)
  ↓
Granted  → register token, send welcome-free low-priority confirmation
Denied   → graceful path: in-app inbox, Settings deep-link, do not re-prompt for 90 days
Provisional (iOS) → deliver quietly, track engagement, upgrade to full after positive signal
```

## Payload Structure

```json
// Alert (user-visible)
{
  "aps": { "alert": { "title": "...", "body": "..." }, "sound": "default", "badge": 3 },
  "data": { "deeplink": "app://order/123", "campaignId": "w17-retention" }
}

// Silent / data-only (background fetch trigger)
{
  "aps": { "content-available": 1 },
  "data": { "sync": "inbox", "since": "2026-04-24T00:00:00Z" }
}
```

Client rules:

- Treat `data.*` as untrusted input — validate types before dispatching navigation.
- Silent push has a strict budget (iOS: ~2–3 per hour throttled by the OS). Never use it for analytics beacons.
- Include a `campaignId` on every payload so client logs and server metrics can be joined.

## Delivery-Receipt and Analytics

| Event | Source | Use |
|-------|--------|-----|
| `sent` | Server (APNs/FCM ack) | Baseline for funnel |
| `delivered` | Client (Notification Service Extension / FCM data handler) | True delivery rate |
| `displayed` | Client foreground/banner callback | Separates delivery from visibility |
| `opened` | Deep-link handler | Primary engagement metric |
| `dismissed` | iOS 16+ / Android | Detects notification fatigue |

Wire a `NotificationServiceExtension` on iOS to log `delivered` before the banner shows; Android's `FirebaseMessagingService.onMessageReceived` gives the equivalent hook for data messages.

## Rate and Quota Limits

| Platform | Limit | Practical ceiling |
|----------|-------|-------------------|
| APNs | Per-connection HTTP/2 streams, soft throttle on silent push | ~1 user-visible per 10 min feels safe; >3/day triggers opt-out |
| FCM | 240 messages / minute / device (data), user-visible unthrottled but policy-limited | Batch with `topic` fan-out instead of per-device loops |
| iOS Live Activities | ActivityKit, 8h active + 4h stale, ~4KB payload, `apns-priority` 5 | No advertising/marketing copy permitted |
| Android Notification Channels | Per-channel user controls, channel created at first use | Mandatory since Android 8 (API 26); audit channels regularly |

Enforce a client-side de-dup key (hash of `campaignId + contentHash`) to drop duplicates from re-delivery retries.

## Platform Code Snippets

```swift
// iOS: request + handle token
UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, _ in
    guard granted else { return }
    DispatchQueue.main.async { UIApplication.shared.registerForRemoteNotifications() }
}

func application(_ app: UIApplication,
                 didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
    Task { await DeviceAPI.upsert(token: token) }
}
```

```kotlin
// Android: FCM token refresh
class AppMessagingService : FirebaseMessagingService() {
    override fun onNewToken(token: String) {
        scope.launch { deviceApi.upsert(token) }
    }

    override fun onMessageReceived(msg: RemoteMessage) {
        analytics.log("delivered", msg.data["campaignId"])
        if (msg.notification == null) backgroundSync.handle(msg.data)
    }
}
```

## Anti-Patterns

- ❌ Requesting permission on first launch with no context — guarantees denial, and iOS denial is sticky.
- ❌ Hard-coding APNs/FCM server keys in the client bundle — always stays on the server.
- ❌ Using silent push for analytics beacons — iOS will throttle and eventually stop delivering.
- ❌ Re-prompting after denial via custom dialog loops — violates App Store Review Guideline 4.5.4.
- ❌ Treating payload `data` as trusted — always validate before dispatching deep-links.
- ❌ Omitting `campaignId` from payloads — makes delivery/open-rate analysis impossible.
- ❌ Sending the same push to all time zones at once — schedule by local user time.

## Handoff / Next Steps

- **To Gateway**: expected delivery topology (per-user, per-topic, broadcast), payload schema, token registry contract, rate-limit budget per campaign.
- **To Sentinel**: location of token storage, any NotificationServiceExtension modification of payloads, third-party SDKs touching push (Braze, OneSignal, Airship).
- **To Launch**: store-compliance note (provisional authorization policy, rich-media review), feature-flag plan for staged rollout, KPI targets (opt-in rate, delivery rate, open rate, 7-day retention uplift).
- **To Radar**: test matrix covering cold-start delivery, background-app delivery, permission denial, token rotation after reinstall, deep-link open from notification.
