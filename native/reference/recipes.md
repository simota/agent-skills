# Native Recipe Behavior Notes

**Purpose:** Key gotchas, thresholds, and runtime constraints per Recipe Subcommand.
**Read when:** Activating a Recipe via subcommand dispatch and the "Read First" reference is loaded.

Each entry is a 1-line summary — load the Recipe's "Read First" reference (see SKILL.md `## Recipes` table) for full implementation detail.

---

| Recipe | Behavior |
|--------|----------|
| `swiftui` | iOS Swift 6.3 + `@Observable` + SwiftData/Core Data, T1 offline default, Liquid Glass on iOS 26. |
| `compose` | Android Material 3 Expressive + Strong Skipping + Type-safe Navigation 2.8+, targetSdk 35/36, edge-to-edge day 1. |
| `liquidglass` | iOS 26 adoption: new SwiftUI material APIs + 4-variant icons (Icon Composer) + dynamic tab-bar shrink + iOS 17/18 fallback. |
| `expressive` | M3 Expressive: replace deprecated BottomAppBar/indeterminate CircularProgressIndicator with FloatingToolbar/LoadingIndicator, spring motion, new shape library. |
| `offline` | Per-domain T0-T3 tier → local DB → write queue → conflict policy (LWW / CRDT / server reconciliation). |
| `push` | iOS APNs + UNUserNotificationCenter + Live Activities (max 8h + 4h stale, ~4KB, no ads); Android FCM + Notification Channels + POST_NOTIFICATIONS runtime perm. Soft pre-prompt mandatory. |
| `deeplink` | Universal Links (AASA) + App Links (assetlinks.json) + Coordinator/NavController routing. Firebase Dynamic Links retired. Custom scheme = fallback only. |
| `bg` | iOS BGTaskScheduler, Android WorkManager/JobScheduler. ~80% of OS window budget; plan Doze/App Standby/Low Power; Foreground Service Types on Android 14+. |
| `passkey` | Passkey (FIDO2/WebAuthn) default for new flows. iOS `ASAuthorizationController` + Secure Enclave + Keychain; Android Credential Manager. Sign in with Apple alongside any third-party social. |
| `privacy` | Apple Privacy Manifest + Required Reasons API (3rd-party SDKs since 2025-02-12); Google Data Safety form (all tracks). Hand off to Cloak. |
| `rollout` | iOS TestFlight phased (1/10/50/100% over 7d); Android Play Staged (5/20/50/100%). Halt + hotfix on regression; server-driven flags as primary kill switch. |
| `store` | Pre-submission compliance: Privacy Manifest, Data Safety, 5-tier Age Rating (by 2026-01-31), DSA, DMA, Sign in with Apple, AI disclosure (5.1.2(i) + Play AI Content), Photo Picker, Foreground Service Types, Liquid Glass icon variants. |
| `cli` | Terminal automation. iOS: `xcrun-cli.md` (simctl/devicectl/xctrace/xcresulttool/notarytool/atos). Android: `adb-cli.md` (pm/am/logcat/dumpsys/pair/Perfetto/monkey). adb reference includes iOS↔Android command map. |
