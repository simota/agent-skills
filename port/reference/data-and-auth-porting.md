# Data and Auth Porting

How to translate web storage, API, and auth flows into native iOS and Android equivalents — with offline tiers and security in mind.

---

## 2026 Update — Auth and Data shifts since 2024

### Passkeys (FIDO2 / WebAuthn) is the default new path

- **2026 baseline**: Passkeys are the recommended sign-in surface on both platforms.
- iOS: `ASAuthorizationController` + Secure Enclave + Keychain. Available since iOS 16; broadly adopted by 2026.
- Android: **Credential Manager API** — single UI for Passkey + Password + Sign-in-with-Google. Passkey-eligible API 28+. **Recommended path** per Android Developers Blog (2025-09).
- Industry results from Credential Manager rollouts: X 2× sign-in rate, KAYAK 50% sign-in time reduction, 36% of Passkey-eligible users enrolled (FIDO Alliance 2025-Q4).
- **Privacy benefit**: biometric data never leaves the device — only WebAuthn assertions. Helps with GDPR / personal information protection.

Port action:
- Plan Passkey + fallback (password / OAuth) at MVP.
- Migrate password sign-in users to Passkeys with a soft prompt after first successful sign-in.
- Hand off Secure Enclave + Keychain key-attestation specifics to `Crypt`.

### Sign in with Apple (SIWA) — 2024 relaxation

- The "must offer SIWA when offering any third-party login" rule was **relaxed in 2024-01**.
- Replacement: provide a "privacy-equivalent" option (limit to name+email, support private email relay, no cross-app tracking).
- **In practice, offering SIWA remains the safest path** — custom "privacy-equivalent" alternatives still attract reviewer scrutiny.

### Storage shifts

- iOS: **SwiftData** (iOS 17+) is the new default for object persistence in new projects when SwiftUI-centric. Use Core Data when iOS 16 support, advanced predicates, `NSFetchedResultsController`, or performance-critical paths are needed.
- iOS: Privacy Manifest **Required Reasons API** declarations needed for `UserDefaults`, `FileTimestamp`, `SystemBootTime`, `DiskSpace`, `ActiveKeyboards` — see `regulatory-checklist-2026.md`.
- Android: **Room 2.7** (released 2025-04) brought stable Kotlin Multiplatform support across Android / iOS / Desktop, KSP2, and Kotlin codegen by default. **Room 3.0 (alpha 2026-03)** is a breaking next-gen rewrite: new package `androidx.room3:room3-runtime`, **Kotlin-only codegen**, coroutines-first APIs, fully backed by `androidx.sqlite` driver APIs, KMP across Android / iOS / JVM / **JavaScript / Wasm**, and KSP-required (no kapt). New projects targeting KMP should start on Room 2.7 stable until Room 3.0 GA, then plan a migration window — Room 3.0 does not auto-migrate from 2.x.
- Android: **DataStore** (Preferences + Proto) is the standard for non-secret prefs. SharedPreferences is legacy. Sensitive data → EncryptedSharedPreferences (or Tink-encrypted DataStore).

### CRDT / sync engine choice (2026 default)

For T2 / T3 offline tiers with multi-device collaboration:

| Pattern | When | Library |
|---------|------|---------|
| **CRDT** (Yjs / Automerge 2.0 / Loro) | Multi-device collaborative editing, offline writes; default for 2026 | Yjs (web-friendly), Automerge 2.0 (Rust core, FFI to iOS/Android), Loro (Rust + WASM/FFI) |
| **OT (Operational Transform)** | Text editing requiring server-side sequence guarantees (e.g., Google Docs–style) | Custom; complex |
| **LWW (Last-Write-Wins)** | Single-field, low-collision data | Roll your own with server timestamps |
| **Mutation push + linear processing + client rebase** | Linear-style: client `local KV write → server linear processing → client rebase` | Custom (see Linear architecture studies) |

Source: 2025 Local-First / CRDT industry analyses (Velt, debugg.ai, Bytemash).

Be aware of "CRDT alone is not enough" — authorization, schema migration, and tombstone GC remain real-world challenges.

### API client redesign — BFF + GraphQL Persisted Queries (2026)

- For chatty REST or RSC-heavy web backends, design a **Mobile BFF** (Backend For Frontend).
- **GraphQL Persisted Queries**: client sends only the query hash; server keeps the registered query allowlist. Benefits:
  - Reverse-engineering protection (hashes don't reveal structure)
  - Cache-friendly (REST-like via stable URLs)
  - Smaller payloads
- Schema Federation (Apollo Federation) + Schema Registry + Persisted Queries is the 2026 BFF standard set.

Hand off to `Gateway` for OpenAPI / GraphQL SDL specification.

### Networking client refresh (2026-05)

- iOS: **URLSession + async/await** is the default; iOS 15+ baseline acceptable. Combine is legacy in new code. **Swift 6.2 Approachable Concurrency (Xcode 26)** changes the default — new projects get MainActor-by-default isolation, so async repository code should explicitly `nonisolated` / `@concurrent` to opt into background execution. `NonisolatedNonsendingByDefault` makes nonisolated async functions inherit caller's isolation, which removes a common class of `Sendable` errors.
- Android (incl. KMP): **Ktor Client** for KMP-friendly path; Retrofit + OkHttp + Coroutines for pure-Android. **Kotlin 2.2.20 + K2 default** in 2026; JetBrains' coming Swift export work for KMP coroutines + flows is in active development — track for downstream impact on iOS interop.
- WebSocket: `URLSessionWebSocketTask` (iOS) / OkHttp or Ktor WebSocket (Android). Heartbeat ~30-60s.
- Apollo iOS / Apollo Kotlin for GraphQL with normalized cache (maps well to T1/T2 offline).

### Push & Live Activities (2026)

- iOS: APNs + **Live Activities** (`ActivityKit`, max 8h active + 4h stale, payload ~4KB, no advertising copy).
- Android: FCM + Notification Channels (mandatory). AI Notification Organizer (Android 16, mid-2025, Pixel-first then expanding).
- Android 13+ (API 33): `POST_NOTIFICATIONS` runtime permission. Use **soft pre-prompt UI** before the system dialog.
- iOS: First denial is sticky — only Settings can re-grant. Soft pre-prompt is mandatory.

### Universal Links / App Links — Firebase Dynamic Links retired

- **Firebase Dynamic Links was shut down in 2025** — apps must run their own AASA / `assetlinks.json` infrastructure.
- For attribution / deferred deep links, use a Mobile Measurement Partner: AppsFlyer, Adjust, or Branch (effective default after Firebase exit).
- Email-link wrapping (SendGrid / Mailgun click tracking) breaks Universal Links — coordinate domain handling.

### Cookies / WebView session migration (legacy recovery only)

- WKWebView (iOS) and Android WebView keep their cookie stores **separate** from native URLSession / OkHttp.
- iOS Intelligent Tracking Prevention (ITP) discards many cookies under CORS conditions.
- **Default rule**: do not attempt cookie sync; redesign as token-based auth from MVP. Cookie-bridge designs are reserved for legacy recovery cases that have run out of better options.

### Logout completeness checklist (2026)

| Step | iOS | Android |
|------|-----|---------|
| Server-side token revocation | API call | API call |
| Secure storage clear | Keychain item delete | EncryptedSharedPreferences clear |
| Local cache wipe (optional) | Core Data / SwiftData wipe | Room database delete |
| Push token unregister | APNs token unregistered server-side | FCM token unregistered server-side |
| Analytics user reset | Analytics SDK reset | Analytics SDK reset |
| Passkey credential delete (if revoking) | Keychain Passkey delete | Credential Manager `clearCredentialState()` |
| Navigate to login | Coordinator → root | NavController `popUpTo(start)` |

---

---

## Storage Classification

Classify every web storage usage from `web-analysis-checklist.md` Section 5 into one of four classes. Each class has a fixed native target.

| Class | Examples | iOS target | Android target |
|-------|----------|------------|----------------|
| **Secret** | Auth tokens, refresh tokens, OAuth client secrets, payment tokens, biometric-protected data | Keychain (`kSecClassGenericPassword`, optional `kSecAttrAccessControl` with biometry) | EncryptedSharedPreferences or Tink-encrypted DataStore; biometric gating via BiometricPrompt |
| **Personal** | User profile, drafts, app-specific user-generated content | Core Data / SwiftData (encrypted at rest via NSFileProtection) | Room with SQLCipher if regulated, otherwise default Room |
| **Cache** | API responses, images, search results, server-state cache | URLCache + per-feature `FileManager` cache dir; SDImage / Kingfisher for images | OkHttp cache + Coil/Glide for images; Room as feature cache |
| **Preference** | User-selected settings (theme, locale, notification toggles) | UserDefaults (or `@AppStorage`) | DataStore Preferences |

**Rule:** Never store **Secret** data in UserDefaults / SharedPreferences. They are unencrypted, world-readable on jailbroken / rooted devices, and backed up to iCloud / Google by default.

---

## Offline Tiers

| Tier | Description | When to choose | iOS | Android |
|------|-------------|----------------|-----|---------|
| **T0** | Read cache only | Online-first product, minimal offline | URLCache + `stale-while-revalidate` | OkHttp cache |
| **T1** | Local read persistence | App must show data when offline | Core Data / SwiftData as cache | Room as cache |
| **T2** | Optimistic writes + queue | Users edit offline | Repository + write queue + `BackgroundTasks` for retry | Repository + WorkManager retry |
| **T3** | Full sync (CRDT or server reconciliation) | Multi-device collaboration | CRDT lib (e.g., Automerge) or custom diff | Same; add Firestore / Supabase / custom sync |

**Decide tier per data domain.** Auth tokens are always present (effectively T1 by necessity). User profile may be T1. Drafts / unsent posts are T2. Collaborative documents are T3. Don't over-design — T2/T3 is real engineering work.

---

## Repository Pattern

Both platforms share a conceptual repository per feature:

```
ViewModel → UseCase (suspend / async) → Repository (single source of truth)
                                          ├─ Memory cache (LRU)
                                          ├─ Disk cache (Core Data / Room)
                                          └─ Network (URLSession / Ktor / Retrofit)
```

**Key rules:**
- The Repository decides which tier serves the read.
- The ViewModel never calls the network directly.
- Offline-aware reads emit from the disk cache, then refresh in the background.
- Writes go: optimistic in-memory → persist to disk → enqueue network → reconcile on success.

---

## Auth Porting

### From web cookie sessions

If the web uses HTTP-only cookies and a server-rendered session:

1. **Do not reuse the cookie on mobile.** Cookies on mobile webviews are fragile and inconsistent.
2. Add a token-based mobile login flow on the backend (or BFF). Issue access + refresh tokens.
3. Store tokens in Keychain (iOS) / EncryptedSharedPreferences (Android).
4. Add `Authorization: Bearer <token>` to API client requests.
5. Implement refresh-on-401 with locking (refresh in-flight, queue concurrent requests).

### From web JWT in localStorage

If the web stored JWT in localStorage / sessionStorage (insecure):

1. Treat it as a security debt to repay on mobile.
2. Mobile uses tokens but stores them in **secure** storage.
3. Plan to migrate the web off localStorage in parallel (or sooner).

### OAuth / OIDC flows

| Provider | iOS | Android |
|----------|-----|---------|
| Generic OIDC | `ASWebAuthenticationSession` (system browser) | Custom Tabs + AppAuth |
| Google | Sign in with Google (Credential Manager on Android) or Generic OIDC | Credential Manager |
| Apple | Sign in with Apple (`AuthenticationServices`) — **Required by App Store if any third-party login is offered** | Sign in with Apple via web flow |
| Facebook | Facebook iOS SDK | Facebook Android SDK |
| Custom IdP | Generic OIDC (PKCE mandatory) | Generic OIDC (PKCE mandatory) |

**PKCE is mandatory for native OAuth/OIDC.** Native apps cannot keep a client secret; PKCE replaces it.

### Magic-link / Email-link login

1. Email contains a Universal Link (iOS) and App Link (Android), not a custom scheme.
2. App receives the URL → extracts token → exchanges for session → tokens go to secure storage.
3. Token TTL ≤ 15 minutes; one-time use; server-side enforced.

### Sign in with Apple specifics

- Required if any non-Apple third-party login is offered (App Store guideline 4.8).
- Provide the same set of scopes the other providers offer (name + email).
- Handle private-relay email forwarding.

### Biometric gating

Use biometrics for **re-authentication**, not initial login.

| iOS | Android |
|-----|---------|
| LocalAuthentication: `LAContext.evaluatePolicy` | BiometricPrompt |
| Keychain item with `kSecAttrAccessControl` and `.biometryAny` or `.biometryCurrentSet` | EncryptedSharedPreferences with BiometricPrompt-gated access |
| Fallback: device passcode | Fallback: device credential |

Never bypass platform biometric APIs with custom UI; reject any "tap fingerprint" mockups.

### Logout

| Step | iOS | Android |
|------|-----|---------|
| Revoke server token | API call | API call |
| Clear secure storage | Keychain item delete | EncryptedSharedPreferences clear |
| Clear local cache (optional) | Core Data wipe | Room database delete |
| Clear push token registration | Unregister APNs token from server | Unregister FCM token |
| Reset analytics user ID | Analytics SDK reset | Analytics SDK reset |
| Navigate to login | Coordinator pops to root | NavController popUpTo(start) |

---

## API Client Redesign

Web API contracts often need adjustment for mobile:

| Issue | Mobile-friendly redesign |
|-------|--------------------------|
| Many small requests per screen | Compose into a single `screen-data` endpoint |
| Large list responses without pagination | Cursor or offset pagination, page size ~20-50 |
| Large image payloads | Server-side resize variants, signed CDN URLs |
| Server-rendered HTML in responses | JSON only; render in native |
| Cookies for state | Tokens in `Authorization` header |
| No retry guidance | Server returns `Retry-After`; client uses exponential backoff with jitter |
| No offline guidance | Add `ETag` / `Last-Modified` for conditional fetches |
| No real-time | WebSocket or SSE for live data; polling as fallback |
| Web-only fields (HTML body, CSS classes) | Strip; replace with platform-native rendering directives |

Hand off the redesign list to `Gateway` agent.

### Networking client setup

| Layer | iOS | Android |
|-------|-----|---------|
| HTTP client | URLSession + custom configuration | OkHttp + Retrofit (or Ktor) |
| Auth interceptor | Custom `URLSessionDelegate` or async wrapper that injects tokens and refreshes on 401 | OkHttp `Interceptor` for token injection + `Authenticator` for refresh |
| Logging | OSLog + os_signpost; redact tokens | OkHttp Logging Interceptor (debug only); redact tokens |
| Cert pinning | URLSessionDelegate + SecTrust | OkHttp `CertificatePinner` |
| Retry / backoff | Custom retry middleware with jitter | OkHttp interceptor or RetrofitAdapter wrapper |
| Connectivity | `NWPathMonitor` | `ConnectivityManager.NetworkCallback` |

### GraphQL clients

| iOS | Android |
|-----|---------|
| Apollo iOS — codegen + normalized cache + persisted queries | Apollo Kotlin — codegen + normalized cache + persisted queries |

Both support normalized caching that maps well to T1/T2 offline.

### WebSocket

| iOS | Android |
|-----|---------|
| `URLSessionWebSocketTask` (built-in) | OkHttp WebSocket / Ktor WebSocket |
| Reconnection: exponential backoff with jitter | Same |
| Heartbeat: app-level ping every 30-60s | Same |
| Background: terminated when app backgrounded; resume on foreground | Same; consider FCM data messages for critical pushes |

---

## Sync Strategies (T2 / T3)

| Strategy | When | Implementation sketch |
|----------|------|------------------------|
| **Last-write-wins** | Single-device, low collision | Server timestamps; latest wins |
| **Per-field merge** | Forms, profiles | Field-level versioning; merge non-conflicting |
| **Operational Transform** | Collaborative editing | Server-side OT engine; complex |
| **CRDT** | Multi-device, offline-tolerant | Automerge / Yjs; non-trivial |
| **Server reconciliation API** | Custom domain rules | Server endpoint accepts client-state + returns canonical |

T3 is rarely justified for a port — usually T2 with last-write-wins is enough. If the web product already does collaborative editing, design carefully.

---

## Push Notifications

| Concern | iOS | Android |
|---------|-----|---------|
| Service | APNs | FCM (Firebase Cloud Messaging) |
| Permission | Explicit request (iOS 12+) | Explicit request (API 33+) |
| Token | APNs device token; rotates on app reinstall | FCM registration token; rotates similarly |
| Token storage | Server-side per user; rotate on logout | Same |
| Payload | Alert / Silent (`content-available`) / Mutable | Notification / Data / Mixed |
| Background fetch | Silent push triggers BGAppRefreshTask | Data message triggers FirebaseMessagingService |
| Rich content | UNNotificationServiceExtension | Custom layouts via NotificationCompat |
| Notification channels | Categories (less granular) | Channels (mandatory, user-controlled) |

Server payload schema must support both. Design at blueprint, not afterwards.

---

## Deep Links

| iOS | Android |
|-----|---------|
| Universal Links via Associated Domains + AASA file at `https://example.com/.well-known/apple-app-site-association` | App Links via `assetlinks.json` at `https://example.com/.well-known/assetlinks.json` |
| Custom URL scheme as fallback only | Custom intent filters (avoid for primary) |
| Handler: `onOpenURL` modifier or `application(_:continue:restorationHandler:)` | Handler: `Intent` with `ACTION_VIEW` + filter |

Routing strategy:
1. Receive URL.
2. Parse to a typed `Route` enum / sealed class.
3. Coordinator / NavController navigates.
4. If unauthenticated, gate then replay.

---

## Output Skeleton

```markdown
# Data and Auth Porting Plan: <App Name>

## Storage Classification
| Web mechanism | Class | iOS target | Android target |
| …             | …     | …          | …              |

## Offline Tiers
| Domain | Tier | Reasoning |
| Auth   | T1   | …         |
| Profile| T1   | …         |
| Drafts | T2   | …         |

## API Client
- iOS: URLSession + interceptor pattern, refresh-on-401, cert pinning
- Android: Retrofit + OkHttp, Auth Interceptor, Authenticator for refresh

## Auth Flow
- Provider: …
- Web pattern: …
- Mobile redesign: tokens in Keychain / EncryptedSharedPreferences
- OAuth/OIDC + PKCE
- Sign in with Apple: required ✓
- Magic link: Universal Link / App Link
- Biometric re-auth: ✓ on N flows

## Push
- APNs payload: …
- FCM payload: …
- Server schema: …

## Deep Links
- Universal Links: ✓
- App Links: ✓
- Routes: [list]

## Sync Strategy
- T2 domains: [list], strategy: last-write-wins
```

Consumed by `Native`, `Schema`, `Gateway`, `Builder`.
