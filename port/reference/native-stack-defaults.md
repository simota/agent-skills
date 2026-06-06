# Native Stack Defaults (2026)

Default native stacks for Port blueprints. Deviate only when the survey reveals a constraint (existing native code, regulatory requirement, SDK floor). Document deviations in the blueprint.

## Stack Table

| Layer | iOS | Android |
|-------|-----|---------|
| Language | Swift 6.3 (strict concurrency, default MainActor isolation in Xcode 26) | Kotlin 2.4+ (K2 compiler default) |
| UI | SwiftUI + **Liquid Glass** (iOS 26 target — applied by default when built with iOS 26 SDK) / standard SwiftUI (iOS 17-18 target). UIKit interop only when required | Jetpack Compose + **Material 3 Expressive** (rolled out 2025-09 via Android 16 QPR1; `material3:1.4.0` stable 2025-09-24, `1.5.0-alpha` in flight 2026; **Compose BOM 2026.05.00** maps Compose to 1.11.1); Strong Skipping Mode default |
| Architecture | **MV / MVVM / MVVM-C / TCA** selected per scope (see `native-architecture-mapping.md`). `@Observable` (Swift 5.9+) is the default Model wrapper | MVVM (Now-in-Android style) for standard screens; MVI / Reducer for complex-state screens (form-heavy, real-time editor) |
| Async | `async/await`, `AsyncSequence`, structured concurrency, **Swift 6.3 Approachable Concurrency** (default MainActor isolation, `@concurrent` for explicit background) | Coroutines + Flow; UI: `collectAsStateWithLifecycle()` mandatory |
| DI | swift-dependencies / Factory / manual composition root | Hilt (large / enterprise) or Koin (small-mid / KMP-friendly) |
| Navigation | `NavigationStack`, `NavigationSplitView`, Coordinator pattern. Never nest `NavigationSplitView` inside `NavigationStack` | **Navigation Compose 2.8+ type-safe** (Kotlin Serialization, `@Serializable` data class routes). String routes are legacy |
| Networking | URLSession + async/await (Alamofire optional); Apollo iOS for GraphQL with Persisted Queries | Ktor (KMP-friendly) or Retrofit + OkHttp; Apollo Kotlin for GraphQL with Persisted Queries |
| Persistence | **SwiftData** (iOS 17+, default for new) or Core Data (iOS 16- / advanced predicates / FRC); Keychain (`kSecAttrAccessControl` with biometry) for secrets | **Room 3.0** (alpha 2026-03; `androidx.room3:room3-runtime`, Kotlin-only codegen, coroutines-first, SQLiteDriver-backed, KMP across Android/iOS/JVM/JS/Wasm) or **Room 2.7+ (KMP stable, 2025-04)** + DataStore Preferences; EncryptedSharedPreferences for secrets (legacy fallback); Tink for encryption |
| Auth | **Passkeys (FIDO2) first** via `ASAuthorizationController` + Secure Enclave + Keychain; `ASWebAuthenticationSession` for OAuth/OIDC fallback; **Sign in with Apple** required when any third-party social login is offered | **Credential Manager (Passkey + Password + Sign in with Google)** first; AppAuth + Custom Tabs as OAuth/OIDC fallback for non-supported IdPs |
| Push | APNs (UNUserNotificationCenter) + Live Activities (ActivityKit) | FCM (Firebase Cloud Messaging) + Notification Channels (mandatory) |
| Deep links | Universal Links (AASA) + custom scheme fallback | App Links (assetlinks.json) + intent filters. Firebase Dynamic Links retired — use AASA/assetlinks directly |
| Biometrics | LocalAuthentication (Face ID / Touch ID) — for **re-auth**, not initial login | BiometricPrompt — for **re-auth**, not initial login |
| Widgets | WidgetKit + iOS 18 Control Center API (`ControlWidgetToggle`) | **Jetpack Glance** (Compose-runtime-based) recommended for new widgets |
| AI (on-device) | Foundation Models framework (~3B quantized + Private Cloud Compute fallback); App Intents + Apple Intelligence | ML Kit GenAI APIs + Gemini Nano (AICore-managed) |
| Adaptive | NavigationSplitView (iPad), Trifold/foldable; respect Window Size Classes | Compose Adaptive Layouts 1.2+; Window Size Classes (compact / medium / expanded / **large** / **extra-large**); foldable + trifold |
| Privacy | **`PrivacyInfo.xcprivacy`** with Required Reasons API declarations (mandatory since 2024-05; 3rd-party SDKs since 2025-02-12) | **Data Safety form** in Play Console (covers all tracks, including Internal Testing) |
| Analytics | Configurable (Firebase / Amplitude / Segment) — verify Privacy Manifest provided | Configurable (same) — verify 16KB and Privacy Sandbox SDK Runtime status |
| Build | Xcode 26 + xcodebuild + Swift Package Manager (Xcode 26 + iOS 26 SDK required for all App Store Connect uploads from **2026-04-28**, no exceptions / no extensions) | Gradle + Kotlin DSL + AGP; 16KB native libs required since 2025-11-01 (extension auto-grants until 2026-05-31) |
| CI | Xcode Cloud / Fastlane / GitHub Actions | Gradle + Fastlane / GitHub Actions |
| Min-OS default | iOS 17+ (recommended); iOS 16+ (acceptable) | API 28 (Android 9)+ default; API 31+ if Material You / SplashScreen / Photo Picker mandatory |
| targetSdk (Android) | — | Currently **35** (mandatory since 2025-08-31); **36 mandatory from 2026-08-31** for new apps + updates (edge-to-edge enforced, predictive back default ON, large-screen forced sw 600dp+) |

## Critical Thresholds

| Decision | Threshold | Action |
|----------|-----------|--------|
| Parity verdict mix | If `Dropped` + `Deferred` > 30% of web features | Escalate to user — re-conceive scope before blueprint |
| Offline tier | T0 default; T1+ if any data is read offline; T2+ if writes happen offline; CRDT recommended for T2/T3 multi-device collaborative writes | Document tier per data domain; pick LWW vs CRDT vs server-reconciliation |
| Auth flow | Default = Passkeys (FIDO2) + token-in-Keychain / Credential Manager. Web cookie-only sessions require redesign | Never reuse cookies; design Sign in with Apple alongside any third-party login (App Store guideline) |
| State management | If web uses Redux/Zustand/Pinia/Vuex with > 10 stores | Decompose into per-feature ViewModels; cross-cut state in `AppState` env / DI only |
| Bundle / lazy routes | If web has > 20 lazy-loaded routes | Map to feature modules; plan dynamic feature delivery (Android) and on-demand resources (iOS) only when needed |
| Push / deep links | If web has email-magic-link, OG share, or push UI | Add APNs + FCM, Universal Links + App Links to MVP scope |
| Min-OS baseline iOS | iOS 17+ recommended (SwiftData / `@Observable` / latest Concurrency), iOS 16 acceptable, iOS 15- requires explicit justification | Older = more workarounds, no SwiftData |
| Min-OS baseline Android | API 28 (Android 9)+ default; API 31 (Android 12)+ if Material You / Splash Screen API / Photo Picker are required | Older = manual polyfills |
| targetSdk (Android) | targetSdk 35 mandatory for new submissions since 2025-08-31; **targetSdk 36 mandatory from 2026-08-31** (Wear OS / TV / Auto remain on 35) | Plan API 36 readiness (edge-to-edge enforced, predictive back default ON, large-screen resizability forced sw 600dp+) |
| Xcode / iOS SDK | Xcode 26 + iOS 26 SDK required from **2026-04-28** | Roadmap must include Liquid Glass adoption or explicit decision to defer |
| 16KB page size (Android) | Required for new releases since **2025-11-01** for any app with NDK dependencies (Play Console extension auto-grants until **2026-05-31**; hard cutoff after) | Audit native libraries; reject SDKs without 16KB support |
| Phase count | 3-5 Strangler-Fig phases ideal; 7+ is suspicious | Re-cluster phases; long phase chains suffer accuracy decay |
| AI feature in scope | If app uses third-party AI (OpenAI/Anthropic/Google) | App Store 5.1.2(i) disclosure UI + Google Play AI Content Policy labeling required at MVP, not afterward |
| EU distribution | If app is sold in EU | EU Accessibility Act (EN 301 549 / WCAG 2.1 AA, in force 2025-06-28); DSA trader status declaration; DMA alternative-marketplace option |
| Children-targeted | If app targets < 18 users | Apple 5-tier age rating questionnaire by **2026-01-31**; Declared Age Range API; parental controls; HealthKit / advertising restrictions |
| Fintech / Crypto | If app handles regulated financial activity | Per-country license proof (Apple 3.1.5(b)); KYC/AML; submission lead time +weeks/months; 36% APR cap on loans (US 2025-11) |
| Store policy blockers | Any feature flagged as policy risk | Resolve at blueprint, not at submission |
