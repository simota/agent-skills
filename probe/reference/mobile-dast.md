# Mobile DAST Reference

Purpose: Dynamically test built iOS and Android apps for runtime security flaws — insecure storage, weak transport, deep-link abuse, WebView XSS, IPC exposure — using MobSF, Frida, and OWASP MASVS / MASTG as the authoritative control catalog. Source-only review is out of scope — cross-link to Sentinel.

> **Currency note (2026-05)**:
> - **MobSF v4.4.6** is the latest release (2026-03-21, `github.com/MobSF/Mobile-Security-Framework-MobSF/releases`). MobSF v4.4.1 introduced **Frida 17+ support** with a breaking change for Corellium iOS (requires `frida-server >= 17`), updated SSL/pinning-bypass scripts, and improved Frida bridges. Pin MobSF `>= 4.4.6` and Frida `>= 17.5.2`.
> - **Frida 17.5.2** is the latest stable (released 2025-12-15, `frida.re/news/releases/`). Frida 17.4.0 (2025-10) added the new **`simmy` backend** for instrumenting Apple's CoreSimulator on iOS 18, fixed `dyld_sim` detection, and patched `Java.deoptimize*()` / `Java.backtrace()` on **Android 16**. Use `simmy` instead of bare `usbmuxd` for iOS 18 simulator instrumentation.
> - **OWASP MAS standard stack (2026)**: MASVS v2.0 (2023) + MASVS-PRIVACY v2.1 (2024) is still the published flagship. The MAS project also ships **MASTG** (testing guide) and **MASWE** (weakness catalog). No MASVS v3 has been released as of 2026-05 — track `mas.owasp.org` for status.

## Scope Boundary

- **Probe `mobile`**: dynamic + instrumentation testing of a compiled app binary (IPA / APK / AAB) on a controlled device or emulator. Confirms exploitability with evidence.
- **Sentinel**: static source / config / manifest audit. Probe `mobile` validates Sentinel findings against the running app (e.g. "the code says it encrypts, does it actually?").
- **Native**: builds and ships production mobile apps — navigation, offline, store review. Probe `mobile` tests the built artifact Native produced; Native does not test its own app.
- **Breach**: red-team engagement including mobile as one surface. Probe `mobile` is the DAST slice.

If the question is "does the source opt into ATS?" → Sentinel. "Does the built app actually enforce it against a MITM?" → `mobile`. "How do I implement secure storage?" → Native.

**AUTHORIZATION**: Written scope authorization is mandatory before any dynamic testing. Rooted / jailbroken device, SSL pinning bypass, Frida instrumentation, and repackaging are high-impact techniques that require explicit scope sign-off naming each technique. Testing on devices you do not own, or against app backends without written approval, is illegal. Passive-only inspection (public-store binary metadata, permissions declared in manifest) is the default until authorization arrives.

## OWASP MASVS 2.0 / MASTG Coverage

| MASVS | Control area | Primary dynamic check |
|-------|--------------|------------------------|
| MASVS-STORAGE | Sensitive data storage | Dump app sandbox (`/data/data/...`, app group container); inspect NSUserDefaults / SharedPreferences / SQLite / Keychain / Keystore |
| MASVS-CRYPTO | Cryptographic usage | Frida-hook crypto APIs; detect hardcoded keys, ECB mode, weak KDF |
| MASVS-AUTH | Authentication / session | Token storage, biometric bypass, session fixation, OAuth redirect handling |
| MASVS-NETWORK | Transport | MITM with Burp/mitmproxy after pinning bypass; verify ATS / cleartextTrafficPermitted |
| MASVS-PLATFORM | Platform interaction | Exported activities/services/receivers, deep link / universal link abuse, WebView XSS, pasteboard, IPC |
| MASVS-CODE | Code quality / updates | Outdated dependencies, insecure third-party SDKs, dynamic code loading |
| MASVS-RESILIENCE | Anti-tamper | Root/jailbreak detection quality (should raise attacker cost, not block assessment) |
| MASVS-PRIVACY | Privacy controls | Background telemetry, tracker SDKs, permission over-request |

## Tooling

| Tool | Role |
|------|------|
| MobSF | Static + dynamic orchestrator; one-shot SAST/DAST report, malware heuristics |
| Frida / Objection | Runtime instrumentation, SSL pinning bypass, class dumping, method hooking |
| Burp Suite + Burp Mobile Assistant | MITM proxy with app-store-grade cert install |
| `apktool` / `jadx` / `class-dump` / Hopper | Decompilation, manifest inspection |
| `adb` + `frida-server` | Android runtime control |
| `ideviceinstaller` + `frida` (jailbroken) | iOS runtime control; Corellium for virtualized iOS without physical jailbreak |
| Drozer | Android IPC / exported component attack surface |
| Needle / iOS MASTG tooling | iOS-specific data protection class checks |

## Workflow

```
PLAN      →  confirm written scope, signed-off techniques (pinning bypass / Frida / root)
          →  obtain build artifacts (debug AND release); prefer release for realism
          →  prepare test device: rooted/jailbroken emulator or authorized physical device
          →  install Burp CA in system trust store (Android 7+ requires user or repackage)

SCAN      →  MobSF pass 1: static (manifest, permissions, secrets, weak crypto markers)
          →  Install release build; launch under Frida
          →  SSL pinning bypass (objection `android sslpinning disable` / Frida universal script)
          →  MITM: record full auth flow + sensitive actions through Burp
          →  Storage dump: pull app sandbox, grep for tokens/PII/hardcoded creds
          →  IPC probe (Drozer): exported activity / intent injection / content-provider SQLi
          →  WebView: inject payload via deep link parameter reaching loadUrl / evaluateJavascript
          →  Deep-link abuse: craft intent/universal-link to bypass auth screens
          →  Root/jailbreak detection: note quality — presence is good, blocking assessment is fine

VALIDATE  →  reproduce each finding with smallest possible repro (adb shell am start / curl)
          →  Confirmed vs Unconfirmed per finding
          →  CVSS v4.0 with mobile-context Supplemental metrics where helpful
          →  if static (Sentinel) and dynamic agree → raise confidence; disagreement → investigate

REPORT    →  per-finding: repro, evidence, CVSS, SLA, remediation
          →  handoff: Native (fix), Sentinel (static rule), Triage (critical)
```

## SSL Pinning Bypass — Authorized Only

Pinning bypass is legitimate for authorized assessment of an app you are contracted to test. It is not a license — document the technique and scope in the report.

```bash
# Android (release APK on rooted device, Frida 17.x)
frida -U -f com.example.app -l frida-multiple-unpinning.js

# iOS device (jailbroken or Corellium, frida-server >= 17 required by MobSF 4.4.1+)
objection -g "Example" explore
# ios sslpinning disable

# iOS simulator (Frida 17.4.0+, simmy backend)
frida -D simmy::booted -f com.example.app -l frida-multiple-unpinning.js
```

If pinning bypass fails after three distinct scripts, the app likely uses Certificate Transparency-enforced pinning or native-compiled pinning — document as "pinning robust" and move to other surfaces rather than burning scope time.

## Insecure Storage Checklist

- `/data/data/<pkg>/shared_prefs/*.xml` — tokens in cleartext?
- `/data/data/<pkg>/databases/*.db` — dump with sqlite3; check for PII
- Keystore / Keychain access control: `requireAuthentication` and `accessible=whenUnlockedThisDeviceOnly`?
- External storage (`getExternalFilesDir`) — world-readable on older Android
- iOS `NSFileProtection*` — verify release build uses `Complete` for sensitive files
- Logs (`adb logcat`, `Console.app`) — leaked tokens / PII?
- Screenshots in app-switcher cache — flag with `FLAG_SECURE` / iOS `applicationDidEnterBackground` blur

## Anti-Patterns

- Testing a debug build only — release-build obfuscation / minification changes behavior.
- Using emulator network settings for MITM — differs from real device path; confirm on physical when scope allows.
- Declaring "no pinning" without checking native code — pinning may be in a `.so`.
- Trusting root-detection as a security control — it's defense-in-depth; never the only gate for sensitive actions.
- Forgetting backup (`android:allowBackup=true`) — `adb backup` extracts sandbox without root.

## Handoff

- **→ Native**: confirmed finding + remediation (storage class, ATS config, WebView settings) + SLA.
- **→ Sentinel**: runtime confirmed flaw with probable source location → refine static rules.
- **→ Triage**: CVSS ≥ 9.0 (e.g. cleartext auth token, auth bypass via deep link, RCE via WebView).
- **→ Radar**: regression test pattern.
- **→ Vigil**: exploit signature → detection rule for backend telemetry.
