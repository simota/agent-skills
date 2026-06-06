# Mobile Security Audit (MASVS v2.1.0 + MAS Checklist 2025)

OWASP MASVS v2.1.0 + MAS Checklist static audit for iOS / Android apps. MASVS-PRIVACY added 2024-01; full MASTG coverage 2025-06. Map findings to MASWE (Mobile Application Security Weakness Enumeration).

## Scope boundaries

- Sentinel: static gaps, MASWE mapping, MobSF SAST/DAST integration
- `Probe`: runtime exploitability (Frida 17+ / MobSF dynamic / Drozer)
- `Crypt`: algorithm + key-management design (Keychain / Keystore / Secure Enclave / StrongBox)
- `Cloak`: Privacy Manifest, Required Reasons API, privacy-side compliance
- `Native`: implementation of the fix (Swift/SwiftUI or Kotlin/Compose)

## 8 MASVS categories

| Category | Static checks |
|----------|---------------|
| `STORAGE` | iOS: Keychain `.biometryCurrentSet` + `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`. Android: Tink-encrypted DataStore. Flag `UserDefaults` / plain `SharedPreferences` / deprecated `EncryptedSharedPreferences` for token storage. |
| `CRYPTO` | Constant-time comparison; no custom primitives. Route algorithm/parameter design to `Crypt`. |
| `AUTH` | Passkey / Credential Manager wiring; Sign in with Apple alongside 3rd-party SSO; session/JWT defaults. Cross-link `authn`. |
| `NETWORK` | TLS 1.2+ minimum floor; TLS 1.3 preferred (flag 1.2-only configs). First-party-only cert pinning with ≥2 backup public keys; flag wide third-party pinning. [OWASP Transport Layer Protection Cheat Sheet] |
| `PLATFORM` | Deep-link allowlist; IPC validation; WebView `javascriptEnabled` review; AT/AS hardening. |
| `CODE` | Third-party SDK CVE check. **MASWE-0005 hardcoded credentials priority** — scan `Info.plist`, `*.xcconfig`, `gradle.properties`, `local.properties`, `BuildConfig`, `strings.xml`, decompiled binary (not just source). |
| `RESILIENCE` | Root/jailbreak detection trade-offs; anti-tamper for high-risk apps only. |
| `PRIVACY` | Required Reasons API usage; ANDROID_ID handling. Cross-link `Cloak` for Privacy Manifest review. |

## MASWE-0005 — hardcoded credentials (priority finding)

~50% of mobile apps still contain hardcoded secrets per Zimperium 2025; trivially extracted by MobSF / APKLeaks. Proxy through a BFF instead.

**Scan targets beyond source code**:

- iOS: `Info.plist`, `*.xcconfig`, `*.entitlements`, Xcode build settings, decompiled IPA
- Android: `gradle.properties`, `local.properties`, `BuildConfig`, `res/values/strings.xml`, decompiled APK

## MobSF integration

Run MobSF v4.4.2 SAST/DAST as a CI step on APK/IPA artifacts and merge findings into the Sentinel report. MobSF dynamic findings escalate to `Probe`.

## Signal keywords routing to `mobile`

`MASVS`, `MASTG`, `MASWE`, `mobile security`, `iOS security`, `Android security`, `MobSF`, `Info.plist`, `gradle.properties`, `local.properties`, `xcconfig`, `BuildConfig`
