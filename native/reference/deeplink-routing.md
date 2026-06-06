# Deep Link and Universal Link Reference (Pure-Native)

Purpose: Design a production deep-link layer that routes external URLs (web links, push payloads, ad clicks, QR codes) into the right in-app destination. Covers iOS Universal Links (AASA), Android App Links (assetlinks.json), custom URL scheme fallback, deferred deep links for post-install attribution, routing architecture, and attribution parameter handling.

> Pure-native only. React Native / Flutter are out of scope. Firebase Dynamic Links was retired in 2025 — run AASA / assetlinks.json directly. For attribution, adopt a Mobile Measurement Partner (Branch / AppsFlyer / Adjust).

## Scope Boundary

- **Native `deeplink`**: production routing from an external URL to an in-app screen, including OS-verified links, install-time deferred links, and attribution.
- **Forge `mobile`**: prototyping deep-link UX with `Linking.openURL` only; no AASA/assetlinks, no attribution wiring.
- **Sentinel**: audits deep-link handlers for open-redirect, intent-redirection, and Android `android:exported` misconfigurations. Native implements; Sentinel reviews.
- **Gateway**: server-side link-shortener, smart-link resolution, and attribution API. Native consumes these endpoints; Native does not design the server.

Rule of thumb: if the concern is "does the client route this URL to the right screen?" → `deeplink`. If it is "does the shortener/attribution server resolve the URL correctly?" → Gateway.

## Link Type Matrix

| Type | iOS | Android | Web fallback | Use when |
|------|-----|---------|--------------|----------|
| Universal Link / App Link | AASA file at `/.well-known/apple-app-site-association` | `assetlinks.json` at `/.well-known/assetlinks.json` | Yes — renders web page if app absent | Primary production path |
| Custom URL scheme | `myapp://` via `CFBundleURLTypes` | `<intent-filter>` with `android:scheme` | No — fails if app absent | Internal flows, QR codes, dev tools |
| Deferred deep link | Pasteboard / Install Referrer + attribution SDK | Google Play Install Referrer API | Yes via install page | Post-install onboarding, ad attribution |
| App Clip / Instant App | App Clip AASA (`appclips` array) | Instant App (deprecated path; check current support) | Native lite experience | Try-before-install flows |

Default to Universal/App Links for anything shared publicly. Custom schemes are a fallback, not a primary channel — they are silently swallowed by some browsers and social apps.

## Site-Association Files

```json
// iOS: /.well-known/apple-app-site-association  (no .json extension, Content-Type: application/json)
{
  "applinks": {
    "details": [{
      "appIDs": ["TEAMID.com.example.app"],
      "components": [
        { "/": "/order/*",   "comment": "Order detail" },
        { "/": "/promo/*",   "?": { "ref": "?*" }, "comment": "Promo with ref param" },
        { "/": "/account/*", "exclude": true }
      ]
    }]
  }
}
```

```json
// Android: /.well-known/assetlinks.json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.example.app",
    "sha256_cert_fingerprints": ["AA:BB:CC:..."]
  }
}]
```

Gotchas:

- Both files must be served over HTTPS with no redirects, correct `Content-Type`, and be reachable without authentication.
- Android App Links require `autoVerify="true"` and all listed hosts must pass verification, or none will be auto-opened.
- After changing AASA, iOS may cache the old file for up to a week. Force a reinstall or use the Apple CDN validator.

## Routing Architecture

Treat the deep-link handler as a pure function: `(url, session) -> Route | RequireAuth | NotFound`. Keep side effects (navigation, analytics) at the boundary.

```swift
// iOS: NavigationStack + continueUserActivity
.onContinueUserActivity(NSUserActivityTypeBrowsingWeb) { activity in
    guard let url = activity.webpageURL,
          let route = DeepLinkRouter.resolve(url, session: session) else { return }
    path.append(route)
}
```

```kotlin
// Android: Single-task activity + intent
override fun onNewIntent(intent: Intent) {
    super.onNewIntent(intent)
    intent.data?.let { uri ->
        val route = DeepLinkRouter.resolve(uri, session)
        navController.navigate(route)
    }
}
```

### Auth-Gated Links

Store the original URL when the user is unauthenticated, complete auth, then replay. Do not drop the user on the home screen after login — that is the top cause of deep-link churn.

## Deferred Deep Links

The user taps a link without the app installed. The install completes minutes (or days) later. The app must still route to the intended screen.

| Platform | Mechanism | Notes |
|----------|-----------|-------|
| iOS | Pasteboard pattern (attribution SDK) or App Clip upgrade | Direct App Store links lose context — attribution SDKs (Branch, Adjust, AppsFlyer) fill the gap |
| Android | Google Play Install Referrer API | First-party, no SDK required; Play Store forwards referrer string |
| Both | Short-link service (Gateway) that fingerprints the click | Works on both platforms; adds one network hop |

On first launch after install: check the install referrer / attribution payload within the first 5 seconds, route accordingly, then clear the stored state so a later cold start does not re-trigger.

## Attribution Parameter Handling

Standard UTM (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`) plus platform-specific keys. Treat all of these as untrusted strings.

1. Parse once at entry, normalize casing, trim whitespace.
2. Allow-list known keys before logging — never forward arbitrary query parameters to analytics.
3. Keep the attribution payload in a session-scoped store and attach to the first purchase/signup event, not every subsequent event.
4. Strip attribution params before the route lookup so `(orderId, ref=foo)` and `(orderId)` route to the same screen.

## Anti-Patterns

- ❌ Using custom URL schemes (`myapp://`) as the primary shared link — social apps and email clients often silently drop them.
- ❌ Routing logic inline in screen components — centralize in a router module so tests do not need to render UI.
- ❌ Forgetting to set `launchMode="singleTask"` (Android) — double-instancing the activity ignores deep-link intent.
- ❌ Navigating on a deep link before auth state is hydrated — produces a flash of the login screen then a jump.
- ❌ Not handling `NotFound` — sending the user to a blank screen or crashing on malformed URLs erodes trust.
- ❌ Logging the full URL with attribution params to third-party analytics — leaks personally identifiable campaign data.
- ❌ Hard-coding the AASA `appIDs` Team ID in source control examples without noting that it must match the signing team.

## Handoff / Next Steps

- **To Gateway**: the full URL path catalog, required query parameters per route, fallback web URLs, short-link resolution contract, attribution payload schema.
- **To Sentinel**: list of all intent filters and `onOpenURL` handlers, any dynamic route construction from URL parts, third-party attribution SDKs in the bundle.
- **To Launch**: AASA/assetlinks deployment checklist, TeamID verification, rollout plan for host list changes (invalidate iOS cache, trigger Android re-verification).
- **To Radar**: test matrix — cold start from link, warm start, auth-gated link, malformed URL, deferred link after install, link with attribution params, link opened from different source apps (Safari, Mail, SMS, Chrome).
