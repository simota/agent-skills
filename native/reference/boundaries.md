# Boundaries — Full Elaboration

Full rationale, citations, and threshold detail behind the condensed `## Boundaries` bullets in SKILL.md.

## Always (elaboration)

- Detect target platform(s) before writing any code. iOS + Android = **two separate codebases**, each idiomatic.
- Follow Apple HIG (Liquid Glass on iOS 26, classic HIG on iOS 17/18) and Material 3 Expressive (Android).
- Implement an offline fallback (minimum T0) for any network-dependent feature.
- Use platform-native navigation: `NavigationStack` / `NavigationSplitView` + Coordinator on iOS; Navigation Compose 2.8+ type-safe on Android.
- Handle every permission with a soft pre-prompt UX and graceful denial path.
- Write strict-typed code: Swift 6 strict concurrency; Kotlin explicit nullability; Compose Strong Skipping with `@Immutable` where instance-equality recomposition is a risk.
- Draft Privacy Manifest (iOS) and Data Safety form (Android) alongside the feature. Hand off to `Cloak`.
- Plan store compliance from MVP: Privacy Manifest, Data Safety, Sign in with Apple alongside any third-party login, AI disclosure UI, Photo Picker (Android), Liquid Glass icon variants (iOS 26).
- Default sign-in to **Passkey** (iOS 26 `ASAuthorizationAccountCreationProvider` / iOS 17-18 `ASAuthorizationController` / Android Credential Manager); `preferImmediatelyAvailableCredentials` for silent fallback; OAuth/OIDC (`ASWebAuthenticationSession` + PKCE on iOS, AppAuth + Custom Tabs on Android) only when an existing IdP requires it.
- **In-flow passkey nudge** after OTP/password success (KAYAK/eBay pattern → 75% creation vs ~3% non-nudged).
- **SwiftData**: define `Schema` + `VersionedSchema` + `SchemaMigrationPlan` from first release — retrofitting breaks production relationship integrity.
- **Liquid Glass scope**: apply `.glassEffect()` to navigation chrome only (NavigationBar / TabBar / Toolbar / Sheet / Popover). Never content. Standard SwiftUI components auto-adopt on Xcode 26 recompile.
- **`@Observable` ownership**: declare with `@State` only in the owning view; pass to children via `let` / `@Bindable` / `@Environment`. Child-side `@State` re-inits the model.
- Reference `reference/` for detail patterns; keep SKILL.md procedural and routable.

## Ask First (elaboration)

- Target platform ambiguous (iOS only / Android only / both).
- Offline tier unclear (T0-T3 selection).
- IAP design involves server-side receipt validation architecture.
- Feature requires custom native module (e.g., 3rd-party SDK without Privacy Manifest).
- iOS baseline: default 17; 16 acceptable; 26+ required for Liquid Glass / Foundation Models; 15 needs justification.
- Android baseline: default API 28; API 31+ required for Material You / SplashScreen / Photo Picker.
- **targetSdk 36 timing** — mandatory by 2026-08-31; plan migration before deadline.

## Never (elaboration)

- Implement React Native / Flutter / Kotlin Multiplatform / Compose Multiplatform. **Out of scope** — route to Forge.
- Ship without testing on both platforms when both are in scope.
- Hard-code API keys / secrets client-side (MASWE-0005; Zimperium 2025: ~50% of apps, trivially extracted by MobSF / APKLeaks). Use Keychain (iOS) / Tink-encrypted DataStore (Android); proxy via BFF.
- Store tokens in `UserDefaults` / `SharedPreferences` — use Keychain (`.biometryCurrentSet` + `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`) / Tink-encrypted DataStore.
- Apply `.glassEffect()` to content layers (lists, cards, body) — restrict to navigation chrome.
- Force TabBar / NavigationBar opaque on iOS 26 to hide Liquid Glass — adapt content instead.
- Declare `@unchecked Sendable` to silence strict-concurrency — fix isolation via `actor` / `@MainActor` / `Sendable`.
- Treat `@Observable` as drop-in `ObservableObject` — child-side `@State` re-inits and duplicates observation.
- Use `EncryptedSharedPreferences` on Android — deprecated in `security-crypto:1.1.0-alpha07`. Migrate to Tink-encrypted DataStore / `datastore-encrypted` 1.3.0-alpha07+.
- Keep `onBackPressed()` / `KEYCODE_BACK` on targetSdk 36 — not invoked. Migrate to `OnBackPressedDispatcher` / `PredictiveBackHandler` + `android:enableOnBackInvokedCallback="true"`.
- Lock `screenOrientation="portrait"` / `resizeableActivity="false"` on Android 16 — ignored for `sw600dp+`. `PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY` disappears at API 37.
- Pin third-party domains via cert pinning — restrict to first-party endpoints, public-key pinning with ≥ 2 backups, reserve for finance/health (OWASP 2025 toned down general recommendation).
- Hardcode `messageformat` or English plural rules — Russian/Arabic have 6 forms. Use ICU `{count, plural, ...}` via String Catalogs / `plurals.xml`; hand off to Polyglot.
- Bypass App Review or Play Policy for faster release.
- Apply web-only patterns (`localStorage`, `window.location`, cookie-bearing fetch) on mobile.
- Skip offline handling for network-dependent features.
- Hide platform divergence — if iOS and Android need different solutions, document and ship separately.
- Promise OTA updates of native code. **Not supported** by App Store / Play — use Phased Release / Staged Rollout.
- Ignore platform lifecycle events (backgrounding, memory warnings, Doze, app standby).
- Ship UI without Privacy Manifest / Data Safety completion — both stores reject submissions.
