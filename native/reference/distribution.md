# Shipping a Mac App — Distribution, Signing, Notarization, Updates

Production reference for taking a macOS app from build to a user's Dock: channel decision, code-signing chain, hardened runtime, notarization flow, packaging, self-updating (Sparkle), and Mac App Store submission. Exact command flags live in `reference/macos-xcrun-cli.md` — this file owns the *decision* and *flow* narrative; do not duplicate flag tables here.

> Scope: release-time decisions and pipeline shape. Entitlement selection (sandbox) is `reference/sandbox-entitlements.md`. XPC/helper-tool lifecycle is `reference/xpc-helpers.md`.

---

## 1. App Store vs. Developer ID — Decision Matrix

| Dimension | Mac App Store | Developer ID (direct) |
|---|---|---|
| App Sandbox | **Mandatory** | Optional (recommended, not required) |
| In-app purchase | Apple IAP only (own payment processors prohibited for digital goods) | Own payment processor (Stripe, Paddle, etc.) or none |
| Update mechanism | App Store handles delivery; user pulls updates (or auto-update via System Settings) | You own it — Sparkle 2.x (§ 7) or a custom checker; push cadence is entirely yours |
| Review latency | Days (App Review queue, varies by complexity/rejections) | None — notarization (automated, § 5) typically completes in minutes |
| Entitlement availability | Sandbox-compatible entitlements only; `temporary-exception.*` draws review scrutiny and rejection risk | Full entitlement surface, including unsandboxed apps and Full Disk Access-class TCC features |
| Revenue cut | Apple's standard commission (tiered; check current Apple Developer Program terms — do not hardcode a percentage here, it has changed historically) | 0% platform cut (payment-processor fees still apply) |
| Distribution certificate | Mac App Distribution + Mac Installer Distribution | Developer ID Application (+ Developer ID Installer for `.pkg`) |
| Discoverability | App Store search/browse | Self-driven (website, launch marketing) |
| XPC/System Extension reach | Sandbox-constrained | Broader — Endpoint Security, unsandboxed helpers reachable (still each has its own entitlement/approval gate) |

**Both as separate targets** is common: one target with `app-sandbox = true` + Mac App Distribution signing for the Store, one target with hardened runtime + Developer ID signing for direct download, sharing the same source and differing only in entitlements/scheme. Decide this at `DETECT`, not after the sandbox entitlement set is already locked in — retrofitting sandbox onto a Developer-ID-first app is a real rework cost (see `reference/sandbox-entitlements.md` § 9 for what breaks).

---

## 2. Code Signing Chain

| Certificate | Used for | Issued to |
|---|---|---|
| Apple Development | Local device builds, debugging (Xcode-managed) | Individual developer |
| Developer ID Application | Signing the `.app` bundle for direct distribution | Team (Account Holder/Admin generates) |
| Developer ID Installer | Signing a `.pkg` installer for direct distribution | Team |
| Mac App Distribution | Signing the `.app` bundle for Mac App Store submission | Team |
| Mac Installer Distribution | Signing the installer package submitted to App Store Connect | Team |

- Provisioning profiles are generally **not required for Developer ID** direct distribution (Developer ID signing does not consume a profile the way iOS ad hoc/App Store builds historically did). Mac App Store builds use an App Store provisioning profile the same way iOS does, managed automatically by Xcode when "Automatically manage signing" is on.
- Certificate discovery/import for CI: `reference/macos-xcrun-cli.md` § 5 (`security` keychain commands).

---

## 3. Hardened Runtime

Hardened Runtime is a **separate system from App Sandbox** — restated in full at `reference/sandbox-entitlements.md` § 9; the short version: Sandbox governs *what resources* the app can touch, Hardened Runtime governs *what code* can execute inside the app's process. Notarization requires Hardened Runtime; it does not require Sandbox.

Enable via `codesign --options runtime` (or the Xcode "Hardened Runtime" capability, which sets the same build flag). By default this blocks: loading unsigned dylibs/frameworks, JIT'ing executable memory, DYLD environment-variable injection, and debugger attachment from arbitrary processes.

### 3.1 Exception Entitlements

| Entitlement | Unlocks | Typical need |
|---|---|---|
| `com.apple.security.cs.allow-jit` | Allocate JIT-compiled executable memory | Script interpreters, emulators, JS engines embedded in the app |
| `com.apple.security.cs.allow-unsigned-executable-memory` | Broader unsigned-executable-memory allowance beyond JIT | Legacy interpreters/plugins that can't be fully re-architected; prefer `allow-jit` if it alone suffices |
| `com.apple.security.cs.disable-library-validation` | Load dylibs/frameworks signed by a *different* Team ID (or unsigned) | Plugin-hosting apps (DAWs, editors with third-party plugin ecosystems) |
| `com.apple.security.cs.debugger` | Declares the app itself as a debugging tool, permitted to attach to and control other processes | Debuggers, profilers, instrumentation tools only |
| `com.apple.security.cs.allow-dyld-environment-variables` | Honor `DYLD_*` env vars at launch | Rare — dev/test tooling; avoid in shipping consumer apps |
| `com.apple.security.get-task-allow` | Allows any process to attach a debugger (task port access) | **Development builds only** — Apple explicitly requires this be absent/false for notarization; leaving it `true` in a release build blocks notarization |

Each exception weakens the hardened-runtime guarantee it belongs to — request only the ones the app's actual architecture needs (a plugin host needs `disable-library-validation`; it does not also need `allow-jit` unless it separately runs a script engine).

---

## 4. Deep-Signing Order

`codesign` must sign from the **inside out**: embedded frameworks and helper/XPC bundles before the outer `.app`, because the outer signature's seal covers the already-signed inner components' checksums.

```
1. Sign every embedded .framework / .dylib          (Frameworks/)
2. Sign every embedded XPC service                    (Contents/XPCServices/*.xpc)
3. Sign every embedded helper tool / login item .app   (Contents/Library/LoginItems/, .../Helpers/)
4. Sign the outer .app bundle last                     (with --entitlements for the outer app)
```

- `codesign --deep` will *attempt* this walk automatically, but it applies **one flat signing pass with one entitlements file to everything** — it cannot give the outer app one set of entitlements and an XPC service a different, narrower set. Any nontrivial app (embedded XPC service, differently-scoped helper) needs manual per-component signing in the order above; `--deep` is acceptable only for the trivial case of "no embedded components need distinct entitlements."
- Exact `codesign` flags (`-s`, `--options runtime`, `--entitlements`, `-dv --verbose=4`) → `reference/macos-xcrun-cli.md` § 2.

---

## 5. Notarization Flow

```
xcodebuild archive/export (or manual codesign chain, § 4)
        │
        ▼
zip or .dmg/.pkg the signed artifact
        │
        ▼
xcrun notarytool submit <artifact> --keychain-profile <profile> --wait
        │
        ├─ Accepted ──▶ xcrun stapler staple <artifact>
        │                        │
        │                        ▼
        │               xcrun spctl -a -vvv <artifact>   (verify Gatekeeper acceptance)
        │
        └─ Invalid ───▶ xcrun notarytool log <submission-id>   (diagnose, § 5.1)
```

- Exact `notarytool`/`stapler`/`spctl` flags and the `store-credentials` keychain-profile setup → `reference/macos-xcrun-cli.md` § 5.
- Staple the artifact you actually distribute (`.dmg`/`.pkg`), not just the inner `.app` — Gatekeeper checks the outer container's staple on first launch from that container; if you staple only the `.app` before zipping into a `.dmg`, the staple still travels with the `.app` and is checked when the user drags it out, but stapling the `.dmg` itself additionally lets Gatekeeper validate offline before the user even opens it.
- Notarization requires Hardened Runtime (§ 3) and a Developer ID (or Mac App Distribution, though the Store path skips notarytool entirely — App Review is the gate there) signature; unsigned or ad-hoc-signed artifacts are rejected outright.

### 5.1 Ticket/Log Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `notarytool log` shows `The signature does not include a secure timestamp` | Signed without network access, or `codesign` timestamp server unreachable | Re-sign with network available (timestamping is default-on but requires connectivity) |
| `The binary is not signed with a valid Developer ID certificate` | Wrong cert (e.g. Apple Development instead of Developer ID Application) | Re-sign with the correct identity (§ 2) |
| `get-task-allow` rejection | Debug entitlement left in a release build (§ 3.1) | Strip `com.apple.security.get-task-allow` from the release entitlements file |
| Nested binary not signed / signed with wrong identity | Deep-signing order skipped (§ 4) | Re-sign inside-out |
| `stapler staple` fails with "no ticket found" | Stapled before `notarytool submit --wait` actually completed (accepted asynchronously without `--wait`, or stapled too soon) | Always gate stapling on `--wait`'s success exit, or poll `notarytool info <id>` until `status: Accepted` |
| `spctl -a -vvv` reports "rejected" post-staple | Artifact modified after signing/stapling (e.g. re-zipped, contents changed) | Re-run the full sign → notarize → staple sequence on the final artifact, never touch it after |

---

## 6. Packaging

| Format | Tool | When |
|---|---|---|
| `.dmg` | `hdiutil` (manual) or `create-dmg` (community wrapper, styled background/icon layout) | Default for Developer ID direct distribution — drag-to-Applications is the expected UX |
| `.pkg` | `pkgbuild` (component package) + `productbuild` (distribution package, multi-component + license/welcome screens) | Installer-driven flows: privileged helper install at first launch, multiple bundled components, or Mac App Store submission (Store always wants a signed `.pkg`) |

- `pkgbuild --component App.app --install-location /Applications ComponentApp.pkg` builds a single-component package; `productbuild --distribution dist.xml --package-path . Final.pkg` composes multiple `.pkg` components (e.g. main app + privileged helper installer) plus a distribution XML controlling install-location choices and welcome/license panes.
- `create-dmg` (third-party, common in CI) wraps `hdiutil` with background image, icon positions, and Applications-folder symlink placement — evaluate as a build-script dependency, not a standard Apple tool.
- Exact `hdiutil`/`pkgbuild`/`productbuild`/`productsign` invocations → `reference/macos-xcrun-cli.md` § 6.

---

## 7. Sparkle 2.x Self-Updating (Developer ID only)

Sparkle is the de facto standard for Developer-ID-distributed Mac apps that need in-app update checking (the App Store path has its own built-in updater and must not ship Sparkle).

| Component | Role |
|---|---|
| Appcast (`appcast.xml`) | RSS-based feed listing available versions, download URLs, release notes, and EdDSA signatures — hosted by you |
| EdDSA signing | Sparkle 2.x signs each update with an Ed25519 key; the app embeds the public key (`SUPublicEDKey` in Info.plist), you keep the private key to sign each release (`generate_keys`/`sign_update` tools bundled with Sparkle) |
| `SUFeedURL` | Info.plist key pointing at the hosted appcast URL |
| Sandboxed Sparkle XPC services | Sparkle 2.x ships XPC service targets (`Downloader`, `Installer`) so a *sandboxed* host app can still self-update — required if the Developer ID target also enables App Sandbox; unsandboxed targets can skip the XPC services and update in-process |
| Delta updates | Sparkle can generate/apply binary-diff updates between adjacent versions to shrink download size; optional, configured via the `generate_appcast` tool's delta-version flags |

- Sparkle's own update-downloading and unpacking path is signature-verified against the embedded EdDSA public key before install — a compromised appcast host without the private key cannot push a malicious update, but a compromised *build machine* holding the private key can. Treat the EdDSA private key like a code-signing key.
- Update UI conventions: Sparkle's default UI follows Mac HIG (a small "Update Available" panel with release notes, Install/Skip/Remind-Me-Later) — customize the delegate only for real product needs, not cosmetic drift from the platform-standard flow.

### 7.1 Minimal Setup

```xml
<!-- Info.plist -->
<key>SUFeedURL</key>
<string>https://example.com/updates/appcast.xml</string>
<key>SUPublicEDKey</key>
<string>base64-ed25519-public-key-from-generate_keys</string>
<key>SUEnableAutomaticChecks</key>
<true/>
```

```bash
# One-time key generation (Sparkle's bundled tool)
./bin/generate_keys
# Per-release: sign the update archive, paste the output into the appcast entry
./bin/sign_update App-1.2.0.zip
```

```xml
<!-- appcast.xml — one <item> per release -->
<item>
  <title>Version 1.2.0</title>
  <sparkle:version>120</sparkle:version>
  <sparkle:shortVersionString>1.2.0</sparkle:shortVersionString>
  <sparkle:minimumSystemVersion>13.0</sparkle:minimumSystemVersion>
  <enclosure url="https://example.com/updates/App-1.2.0.zip"
             sparkle:edSignature="base64-signature-from-sign_update"
             length="12345678"
             type="application/octet-stream" />
</item>
```

- Sandboxed hosts must embed Sparkle's `Autoupdate.app`, `Downloader.xpc`, and `Installer.xpc` helper targets alongside the main app and sign each per the deep-signing order in § 4 — omitting the XPC targets is the most common "Sparkle works unsandboxed but silently fails once I add App Sandbox" report.

---

## 8. Mac App Store Submission Specifics

- Upload via Xcode Organizer, `xcodebuild -exportArchive` with the App Store export method, or `notarytool`-adjacent App Store Connect API tooling (Store submissions do not go through `notarytool` — App Review is the gate).
- **TestFlight for macOS** is available the same as iOS — internal/external testers, build expiration, matching entitlement/sandbox constraints as the eventual Store build (a TestFlight build that isn't sandboxed will not later pass Store review unmodified).
- **Phased release**: Store updates can roll out over 7 days to a growing percentage of existing users (opt-in per release in App Store Connect) — use for high-risk updates; pair with crash-rate monitoring during the rollout window.
- In-app purchase (if used) must go through StoreKit/Apple IAP — this is the primary constraint that pushes apps with existing payment infrastructure toward Developer ID instead (§ 1).
- App Sandbox is non-negotiable for this channel — if `reference/sandbox-entitlements.md` § 9's "sandbox-incompatible feature" list intersects the app's core functionality, Developer ID is the only viable channel, not a preference.

---

## 9. Common Distribution Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Deciding sandbox scope after the app is already Developer-ID-shaped, then trying to add App Store as a second channel | Retrofitting sandbox onto file-access/XPC/networking code written without entitlement discipline is a real rework, not a checkbox flip | Decide both-or-one channel at `DETECT` (Core Contract in `dock/SKILL.md`); if both are planned, scaffold entitlements for the *stricter* (sandboxed) target from day one even on the Developer ID build |
| Treating `codesign --deep` as sufficient for a bundle with an XPC service | The XPC service silently inherits the host app's (wrong, too broad or too narrow) entitlements | Sign inside-out manually (§ 4) |
| Shipping `com.apple.security.get-task-allow = true` in a release build | Notarization rejects the submission outright | Strip debug entitlements from the release `.entitlements` file, verify via `codesign --display --entitlements -` (`reference/macos-xcrun-cli.md` § 3) |
| Stapling before `notarytool submit --wait` actually reports `Accepted` | `stapler staple` fails with "no ticket found," or worse, silently staples nothing if scripted without checking the exit code | Gate stapling on the `--wait` call's success, or poll `notarytool info` until `status: Accepted` |
| Adding Sparkle to a sandboxed app without its XPC service targets | Auto-update silently fails to download/install once sandbox is enabled | Bundle and sign `Autoupdate.app` + `Downloader.xpc` + `Installer.xpc` (§ 7.1) |
| Assuming the Mac App Store revenue cut is a fixed, hardcodeable percentage | Stale numbers in specs/docs age badly as Apple's terms change | Reference the current Apple Developer Program Agreement / App Store Connect terms at decision time rather than a cached figure |

---

## 10. Release Checklist

- [ ] Distribution channel decided (App Store / Developer ID / both) — locked before entitlement scaffolding, not retrofitted
- [ ] Hardened Runtime enabled (`codesign --options runtime`), with only the exception entitlements (§ 3.1) the app actually needs
- [ ] `com.apple.security.get-task-allow` absent from the release entitlements file
- [ ] App Sandbox entitlements least-privilege audited (`reference/sandbox-entitlements.md`)
- [ ] Deep-signing order followed inside-out: frameworks → XPC services → helper tools → outer `.app` (§ 4)
- [ ] (Developer ID) `notarytool submit --wait` accepted, `stapler staple` applied to the distributed artifact (`.dmg`/`.pkg`), `spctl -a -vvv` confirms Gatekeeper acceptance
- [ ] (Developer ID) DMG or PKG packaged and tested on a clean machine (no prior dev-cert trust)
- [ ] (Developer ID, self-updating) Sparkle appcast published, EdDSA-signed, `SUFeedURL` reachable, sandboxed XPC services included if the app is sandboxed
- [ ] (App Store) TestFlight build validated with production-matching entitlements before submission
- [ ] (App Store) Phased release configured for high-risk updates
- [ ] Release artifact handed to `Launch` (`NATIVE_MACOS_TO_LAUNCH_HANDOFF` — `reference/macos-handoffs.md`) with distribution channel, notarization status, and appcast coordination noted

---

## Sources

- [Notarizing macOS software before distribution | Apple Developer Documentation](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution) (accessed 2026-07)
- [Hardened Runtime | Apple Developer Documentation](https://developer.apple.com/documentation/security/hardened-runtime)
- [Configuring the hardened runtime | Apple Developer Documentation](https://developer.apple.com/documentation/xcode/configuring-the-hardened-runtime)
- [NOTARYTOOL(1) man page](https://keith.github.io/xcode-man-pages/notarytool.1.html) (accessed 2026-07)
- [Customizing the notarization workflow | Apple Developer Documentation](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow)
- Sparkle project documentation — <https://sparkle-project.org/documentation/> (EdDSA signing, appcast format, sandboxed XPC services; verify against the Sparkle 2.x release notes for the version pinned in the project)
- [Distributing your app for beta testing and releases (TestFlight for macOS) | Apple Developer Documentation](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases)
- Cross-reference: `reference/macos-xcrun-cli.md` (exact `codesign`/`notarytool`/`pkgbuild`/`productbuild` command flags + CI recipe), `reference/sandbox-entitlements.md` (entitlement catalog + hardened-runtime-vs-sandbox distinction), `reference/xpc-helpers.md` (helper-tool lifecycle referenced by Sparkle's XPC services)
