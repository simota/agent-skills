# Swift Security Audit Cheatsheet — Sentinel

Focused checklist for SAST and code-level security review of Swift codebases. Baseline: **Swift 6.2+ / Xcode 26** with **Swift 6.3 outlook** (2026-05).

> Source-of-truth references (full catalog lives in Builder):
> - Constructive Swift stack and library matrix: [`builder/reference/swift-best-practices.md` §9 Production Library Matrix (2026)](../../builder/reference/swift-best-practices.md#9-production-library-matrix-2026)
> - Concurrency / `@unchecked Sendable` / continuation safety: [`builder/reference/swift-anti-patterns.md` §3 Concurrency pitfalls](../../builder/reference/swift-anti-patterns.md#3-concurrency-pitfalls-swift-62-era)
> - Force-unwrap / IUO / `try!` / `as!` catalog: [`builder/reference/swift-anti-patterns.md` §1 Force-unwrap / force-try / IUO pitfalls](../../builder/reference/swift-anti-patterns.md#1-force-unwrap--force-try--iuo-pitfalls)
> - Error handling pitfalls (`catch and log` at wrong layer): [`builder/reference/swift-anti-patterns.md` §5 Error handling pitfalls](../../builder/reference/swift-anti-patterns.md#5-error-handling-pitfalls)
> - Memory model, isolation, region-based isolation, Sendable rules: [`builder/reference/swift-language-spec.md` §3 Concurrency Model](../../builder/reference/swift-language-spec.md#3-concurrency-model)
> - C / Objective-C interop boundary: [`builder/reference/swift-language-spec.md` §10 C / C++ / Objective-C Interop](../../builder/reference/swift-language-spec.md#10-c--c--objective-c-interop--embedded-swift)
> - SwiftLint starter rule set: [`builder/reference/swift-anti-patterns.md` Appendix A](../../builder/reference/swift-anti-patterns.md#appendix-a-swiftlint-quick-reference--starter-config)

**Do not duplicate the catalogs above.** This cheatsheet is the *order* and *triage angle* Sentinel applies on Apple-platform and server-Swift code; it links rather than restates.

Companion cheatsheets (same agent):
- Concurrency / race conditions: see `siege` concurrency recipe (absorbed from specter)
- Crypto stack design: [`crypt/reference/swift-cheatsheet.md`](../../crypt/reference/swift-cheatsheet.md)

---

## When auditing a Swift codebase, walk this checklist:

### 1. Scope the surface

| Step | Command | Why |
|------|---------|-----|
| 1.1 | `xcodebuild -list -project *.xcodeproj` | Enumerate targets — app, extensions (share, widget, notification-service, intents), unit tests, UI tests. Every extension has its own entitlements and sandbox profile. |
| 1.2 | `rg -n '@unchecked Sendable\|nonisolated\(unsafe\)' --type swift` | Locate every escape hatch from the data-race-safety system. Each one is a manual guarantee that must hold. |
| 1.3 | `rg -n 'try!\|as!\|!\.' --type swift -g '!*Tests*'` | Force unwrap / force cast / force try in non-test code. See [anti-patterns §1.1](../../builder/reference/swift-anti-patterns.md#11-catalog). |
| 1.4 | `find . -name 'PrivacyInfo.xcprivacy' -o -name '*.entitlements' -o -name 'Info.plist'` | Privacy Manifest + entitlements + ATS exceptions live here; review every file. |
| 1.5 | `swift package show-dependencies` (and `Package.resolved`) | Surface every SPM dep with its resolved revision and source URL. |

### 2. Force-unwrap / force-cast / `try!` audit

**Production code** must justify every `!`, `try!`, `as!`. **Test code** (`*Tests.swift`, `*Spec.swift`, `XCTestCase` subclasses, `@Test`-annotated suites) may use them freely — assert-fast is desirable in tests.

| Pattern | Production verdict | Reference |
|---------|--------------------|-----------|
| `let v = optional!` | Reject unless followed by `assertionFailure` or paired with a documented invariant in `// SAFETY:` style | [anti-patterns §1.1](../../builder/reference/swift-anti-patterns.md#11-catalog) |
| `try! someThrowing()` | Reject. `try?` for "I can recover" or `do { try ... } catch { return .failure(...) }` for surfaced failure. | §1.1 |
| `obj as! T` | Reject when `obj`'s static type comes from `Any`, JSON decoding, or `NSDictionary`. Use `as?` + `guard`. | §1.1 |
| `IUO` (`var x: Foo!`) | Allowed only for `@IBOutlet` (auto-installed before `viewDidLoad`), `@MainActor` lifecycle hosts, and Objective-C interop. Reject elsewhere. | §1.4 |
| Force unwrap on `URL(string:)` | Always wrong for runtime strings; OK for hard-coded `URL(string: "https://api.example.com")!` where the constant is checked at module-init via a precondition test. | §1.2 |

**SwiftLint enforcement** ([anti-patterns Appendix A](../../builder/reference/swift-anti-patterns.md#appendix-a-swiftlint-quick-reference--starter-config)):

```yaml
# .swiftlint.yml
opt_in_rules:
  - force_cast               # error severity in default config
  - force_try                # error severity in default config
  - force_unwrap
  - implicitly_unwrapped_optional
  - prohibited_super_call
  - private_outlet           # @IBOutlet must be private
```

### 3. `@unchecked Sendable` and `nonisolated(unsafe)` — the data-race escape hatches

Both bypass Swift 6's compile-time data-race safety. Every use must carry a `// SAFETY:` comment naming the invariant that makes it sound.

| Pattern | Audit rule |
|---------|------------|
| `final class Foo: @unchecked Sendable` | The class must be effectively immutable, or every mutable field must be lock-protected. Look for `var` properties without `Mutex`/`OSAllocatedUnfairLock`/`actor` wrapping. See [anti-patterns §3.3](../../builder/reference/swift-anti-patterns.md#33-unchecked-sendable-runtime-crash-mode). |
| `nonisolated(unsafe) var counter = 0` | Reject in concurrent code paths. Replace with `Atomic<Int>` (Swift 6.0+) or actor isolation. |
| `nonisolated(unsafe) let cache = NSCache<…>` | `NSCache` is thread-safe — acceptable. Document why in a `// SAFETY:` comment. |
| Cross-actor mutable singleton declared `@unchecked Sendable` | Always wrong. Wrap state in an `actor`, or use `Mutex<State>`. |

**Common runtime crash**: a `@unchecked Sendable` class with a mutable property gets concurrent writes → data race → memory corruption → unrelated crash later (often in ARC ref-count manipulation, making the trace useless).

### 4. Continuation safety

`withCheckedContinuation` / `withUnsafeContinuation` / `withCheckedThrowingContinuation` MUST resume exactly once. The compiler does not enforce this.

| Bug class | Symptom | Reference |
|-----------|---------|-----------|
| Resume zero times | Task hangs forever; resources leak | [anti-patterns §3.6](../../builder/reference/swift-anti-patterns.md#36-continuation-safety-wrapper) |
| Resume twice | `withCheckedContinuation` → fatal crash; `withUnsafeContinuation` → undefined behavior | §3.6 |
| Resume after early return | Same as twice — second resume crashes | §3.6 |

**Audit grep**:

```sh
rg 'withCheckedContinuation\|withUnsafeContinuation\|withCheckedThrowingContinuation' --type swift -A 30
```

For each hit verify:
1. Exactly one `continuation.resume(...)` per code path.
2. The closure does not capture `continuation` in escaping callbacks called more than once.
3. A timeout wrapper (if used) doesn't race with the closure's own resume.

**Canonical safe wrapper** (see [anti-patterns §3.6](../../builder/reference/swift-anti-patterns.md#36-continuation-safety-wrapper)):

```swift
// FLAG: legacyAPI may call both onSuccess AND onError under contention
func fetch() async throws -> Data {
    try await withCheckedThrowingContinuation { cont in
        legacyAPI.run(
            onSuccess: { cont.resume(returning: $0) },
            onError:   { cont.resume(throwing:  $0) }   // ← double-resume crash
        )
    }
}

// FIX: gate with AtomicBool so only one resume path wins
```

### 5. Network and TLS hardening

#### 5.1 `URLSession.shared` vs scoped session

| Use site | Audit |
|----------|-------|
| Auth / credential-bearing requests | Must use a **scoped** `URLSession` with explicit `URLSessionConfiguration`. Sharing the shared session pools cookies, credentials, and HTTP/2 connections across the entire app — a malicious URL inside the same session sees auth cookies. |
| Telemetry / analytics | Scoped session with `httpCookieAcceptPolicy = .never`. |
| Anonymous public reads | `URLSession.shared` is acceptable. |

#### 5.2 Certificate pinning

```swift
final class PinnedDelegate: NSObject, URLSessionDelegate {
    func urlSession(_ s: URLSession,
                    didReceive challenge: URLAuthenticationChallenge,
                    completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let trust = challenge.protectionSpace.serverTrust,
              SecTrustEvaluateWithError(trust, nil),
              let cert = (SecTrustCopyCertificateChain(trust) as? [SecCertificate])?.first
        else { return completionHandler(.cancelAuthenticationChallenge, nil) }

        let serverHash = SHA256.hash(data: SecCertificateCopyData(cert) as Data)
        if pinnedSPKIs.contains(Data(serverHash)) {
            completionHandler(.useCredential, URLCredential(trust: trust))
        } else {
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }
}
```

Audit checklist:
- Pin **SPKI hash**, not the leaf cert (cert rotation breaks leaf-pinning).
- Maintain ≥2 backup pins (current + next rotation).
- Have a kill-switch (remote config) — pinning gone wrong has bricked apps.
- Library alternative: `TrustKit` (Apple-platform mature, supports OCSP stapling).

#### 5.3 App Transport Security (ATS)

Open every `Info.plist` and search for `NSAppTransportSecurity`. Each exception must be justified.

| Key | When acceptable |
|-----|-----------------|
| `NSAllowsArbitraryLoads = true` | **Never** in production; reject in PR review |
| `NSAllowsArbitraryLoadsInWebContent = true` | Acceptable only if the WebView loads strictly attacker-irrelevant content (e.g. licensed video CDN); document the audited URL set |
| `NSExceptionDomains` with `NSExceptionAllowsInsecureHTTPLoads = true` | Only for known-legacy backends with a documented migration ticket |
| `NSExceptionRequiresForwardSecrecy = false` | Reject — modern infra supports PFS |

### 6. Keychain access patterns

| `kSecAttrAccessible*` value | When |
|------------------------------|------|
| `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` | **Default for tokens / passwords**. Wipes on device unpair, not on iCloud restore. |
| `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` | Background-task creds needed before user unlock |
| `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly` | High-sensitivity creds; requires user to have a passcode set |
| `kSecAttrAccessibleAlways` (DEPRECATED) | **Reject** — encrypted only at-rest until first boot, then accessible to anyone with file-system access |
| `kSecAttrAccessibleAlwaysThisDeviceOnly` (DEPRECATED) | **Reject** — same as above |

Reject Keychain queries missing `kSecUseDataProtectionKeychain: true` (data-protection keychain, file-keychain is legacy macOS-only).

Reject hand-rolled SecItem code without the per-item access-control flags. Prefer wrappers: `KeychainAccess` (mature), or `SimpleKeychain` (Auth0).

### 7. Privacy Manifest (PrivacyInfo.xcprivacy) compliance

Apple **rejects** App Store submissions missing or incomplete Privacy Manifests since 2024-spring.

| File | Required? | Audit |
|------|-----------|-------|
| App `PrivacyInfo.xcprivacy` | ✓ | Lists every required-reason API the binary calls. |
| Every 3rd-party SDK bundle | ✓ | The SDK must ship its own PrivacyInfo.xcprivacy. Missing → App Store rejection. |
| Each SDK in the "commonly-used SDK list" | Signature too | SDKs in the published list must be code-signed. |

**Required-Reason APIs** (NSPrivacyAccessedAPI). For each, the manifest must contain a reason key matching one of Apple's documented codes:

| API family | Reason key category |
|------------|---------------------|
| File timestamp (`fileModificationDate`, `creationDate`, `attributesOfItem`) | `NSPrivacyAccessedAPICategoryFileTimestamp` |
| System boot time (`systemUptime`, `mach_absolute_time`) | `NSPrivacyAccessedAPICategorySystemBootTime` |
| Disk space (`volumeAvailableCapacity*`, `NSURL` disk attributes) | `NSPrivacyAccessedAPICategoryDiskSpace` |
| Active keyboard list (`UITextInputMode.activeInputModes`) | `NSPrivacyAccessedAPICategoryActiveKeyboards` |
| User defaults (NSUserDefaults) | `NSPrivacyAccessedAPICategoryUserDefaults` |

Use Xcode's "Privacy Report" build action to surface unmanifest-ed API use.

### 8. Universal Links / `associatedDomains` injection surface

Every `applinks:` entry is an attacker-controlled deep-link surface.

| Audit | Why |
|-------|-----|
| `apple-app-site-association` (AASA) file under `/.well-known/` on every domain | Verify path patterns don't over-claim (e.g. `*` claims all paths — attacker-supplied URL params reach your handler) |
| Deep-link handler validates path **structure** before parameters | `Path: /share/<id>` — verify `id` is a UUID before accepting |
| Auth handler must verify origin context | Universal Links arriving in `UIApplication.shared.open(_:options:)` from a third-party app must not auto-execute privileged actions |
| Custom URL scheme (`myapp://`) | Reject for auth — any app can register the same scheme; use Universal Links exclusively |

Reference Apple docs: Supporting universal links / Defining a custom URL scheme for your app.

### 9. Code signing and entitlements review

| Entitlement | Audit |
|-------------|-------|
| `com.apple.developer.associated-domains` | Listed domains MUST match the AASA-hosting domains. Extra entries are attack surface. |
| `com.apple.security.application-groups` | App-group containers are shared writable surface — verify the extension truly needs write access |
| `keychain-access-groups` | Sharing Keychain across apps/extensions = sharing creds; verify group membership |
| `com.apple.security.network.client` / `.network.server` (macOS Hardened Runtime) | Strict-listed for distribution outside MAS; sandbox bypass requires justification |
| `com.apple.developer.endpoint-security.client` (macOS) | Highly privileged; only valid for security tooling |
| `com.apple.developer.driverkit` family | Kernel-adjacent; reject in app review unless the product is a driver |
| `com.apple.security.cs.allow-unsigned-executable-memory` (Hardened Runtime exception) | Reject unless JIT is a documented product requirement |
| `com.apple.security.cs.allow-dyld-environment-variables` | Reject — enables `DYLD_*` injection by anyone with execve access |

For macOS distribution, run `codesign -d --entitlements - <app>` and `spctl -a -vvv <app>` to verify gatekeeper acceptance.

### 10. Swift Package supply chain

| Check | How |
|-------|-----|
| **Pinned versions** | Every dep in `Package.swift` uses `.exact("x.y.z")` or `.upToNextMinor(from:)` — never `.branch("main")` in production. |
| **`Package.resolved` committed** | `.gitignore` MUST NOT exclude `Package.resolved`. Audit history for resolved-revision churn. |
| **`.binaryTarget` checksum** | Every `.binaryTarget(name:url:checksum:)` requires a SHA-256. Recompute with `swift package compute-checksum <file>.zip`. Missing or stale checksum = supply-chain risk. |
| **Source URL provenance** | Audit deps for typo-squat / namespace-squat (e.g. `github.com/imitator-org/Alamofire`). |
| **Source-only vs binary artifact** | Prefer source-built for audit. Binary artifacts cannot be inspected without `otool -L` / disassembly. |
| **macro plugins** | Every `@attached`/`@freestanding` macro runs at compile time in the host process. A malicious macro can read env / write files. Audit `Sources/<MacroPlugin>/`. |

CI gate:

```yaml
- run: swift package show-dependencies --format json > deps.json
- run: jq -r '.dependencies[] | .url' deps.json | sort -u > deps.txt
- run: diff deps.txt approved-deps.txt    # fail on new dep
```

### 11. WebKit JS bridge — XSS / `WKUserContentController` injection

`WKWebView` + `WKUserContentController.add(handler, name: "channel")` exposes a JS→Swift call surface. Treat every `WKScriptMessage.body` as untrusted.

| Pattern | Verdict |
|---------|---------|
| `let cmd = msg.body as! String` then exec | Reject — force-cast + injection |
| Decoding `msg.body` as JSON to a typed struct | Acceptable; combine with strict `Codable` and unknown-key rejection |
| `evaluateJavaScript("doThing('\(user_input)')")` | Reject — string-interpolated JS = direct injection. Use `callAsyncJavaScript(_:arguments:)` (iOS 14+) with `arguments:` dict. |
| `WKWebViewConfiguration.preferences.javaScriptEnabled = false` for trust-untrusted content | Acceptable defense in depth |
| `WKWebsiteDataStore.nonPersistent()` for sandboxed in-app browsers | Required when content is untrusted |
| Custom URL scheme handler (`setURLSchemeHandler`) | Audit handler — receives every `scheme://` URL the WebView loads |

Content-Security-Policy header from your origin should restrict `frame-src`, `script-src`. The WebView respects it.

### 12. Sandbox / Hardened Runtime audit (macOS distribution)

For macOS apps distributed outside MAS (DMG / sparkle update / direct download):

| Step | Verify |
|------|--------|
| Hardened Runtime enabled | `Codesign --display --verbose=4 <app>` shows `flags=0x10000(runtime)` |
| Notarization successful | `spctl -a -vvv <app>` returns `accepted source=Notarized Developer ID` |
| Library Validation enabled | No `com.apple.security.cs.disable-library-validation` entitlement |
| Sandbox enabled (if MAS) | `com.apple.security.app-sandbox = true` |
| `NSAllowsArbitraryLoads` not enabled | See §5.3 |
| Sparkle (update framework) used? | Use Sparkle 2.x with EdDSA signing; reject Sparkle 1.x (DSA-deprecated, known RCE in older versions) |

### 13. Reflection / KeyPath abuse

| Pattern | Risk |
|---------|------|
| `Mirror(reflecting: obj)` over a struct containing secret fields | Mirror reveals all stored properties — secrets leak into log dumps |
| `obj[keyPath: dynamicKeyPath]` where `dynamicKeyPath` comes from user input | KeyPath injection — attacker pivots to internal fields |
| `value(forKeyPath:)` on NSObject with untrusted path | Classic ObjC-style key-path injection |
| `_typeName(of:)` / Swift runtime metadata for security decisions | Type names leak module structure; metadata can be spoofed via `@_silgen_name` |

Wrap secret types to refuse Mirror:

```swift
struct ApiToken: CustomReflectable {
    private let raw: String
    var customMirror: Mirror { Mirror(self, children: [], displayStyle: .struct) }
}
```

### 14. Logging hygiene

| Pattern | Verdict |
|---------|---------|
| `print(secret)` / `NSLog("%@", secret)` | Reject. `print` writes to stderr; `NSLog` writes to syslog (collected by MDM and crash reporters). |
| `os_log("%{public}@", secret)` | Reject — `%{public}` literally publishes. Use `%{private}@` (default redacts in release). |
| `Logger.info("\(secret)")` (new `os.Logger`) | Reject when `secret` is a `String` — interpolation defaults to public. Use `Logger.info("\(secret, privacy: .private)")`. |
| `CustomStringConvertible` impl printing internal state | Audit every `description` on auth/crypto types |
| Crash reporter (Crashlytics, Sentry) captures `userInfo`/`NSError` `localizedDescription` | Audit error chains for secret content reaching the reporter |

```swift
// FLAG: defaults to public in os.Logger
logger.info("user \(email) logged in")

// FIX: explicit privacy
logger.info("user \(email, privacy: .private(mask: .hash)) logged in")
```

### 15. CI gate — SwiftLint security profile

```yaml
# .swiftlint.yml
opt_in_rules:
  - force_cast
  - force_try
  - force_unwrap
  - implicitly_unwrapped_optional
  - prohibited_super_call
  - private_outlet
  - explicit_acl                  # public/internal must be explicit
  - explicit_top_level_acl
  - missing_docs                  # public APIs documented
  - prefer_self_in_static_references
  - sorted_first_last
  - last_where
analyzer_rules:
  - unused_declaration
  - unused_import

# .github/workflows/swift-security.yml
- run: swiftlint --strict
- run: |
    xcodebuild -project App.xcodeproj -scheme App \
      analyze -destination 'generic/platform=iOS' \
      CLANG_STATIC_ANALYZER_OTHER_FLAGS='-Xanalyzer -analyzer-config -Xanalyzer -analyzer-check-objc-mismatched-types-in-collection-literal=true'
- run: |
    /usr/libexec/PlistBuddy -c "Print" PrivacyInfo.xcprivacy   # syntax-check manifest
- run: |
    codesign -d --entitlements - $BUILT_PRODUCTS_DIR/App.app | \
      grep -E 'allow-unsigned-executable-memory|disable-library-validation' && exit 1 || true
```

---

## Triage priorities

When multiple findings stack, rank by:

1. **`@unchecked Sendable` / `nonisolated(unsafe)` with mutable state** — data race in release builds, ARC corruption, untraceable crashes.
2. **Continuation double-resume / never-resume** — `withCheckedContinuation` crashes on second resume; `withUnsafeContinuation` is UB. Both block real production traffic.
3. **Force unwrap / `try!` / `as!` on attacker-influenced input** — DoS via crash, sometimes RCE via type confusion (`as!` on JSON).
4. **Missing Privacy Manifest / required-reason API** — App Store rejection; for shipped apps, current-policy violations can trigger removal.
5. **ATS exceptions (`NSAllowsArbitraryLoads`)** — silent plaintext credential exposure.
6. **Keychain `kSecAttrAccessibleAlways*`** — credentials survive jailbreak/backup extraction.
7. **WebView JS-bridge injection** — direct app→native command surface.
8. **Universal Link over-claim** — wide AASA paths grant attacker site reach into your auth handlers.
9. **macOS Hardened Runtime escape hatches** — `disable-library-validation`, `allow-dyld-environment-variables`.
10. **SwiftPM unpinned dep / missing `.binaryTarget` checksum** — supply-chain compromise vector.
11. **Logging secrets at `.public` privacy** — silent and persistent leak into telemetry / crash pipelines.

---

## Sources

- Swift Forums — Sendable & data-race safety: https://forums.swift.org/c/evolution/concurrency/
- Apple — Privacy manifest files: https://developer.apple.com/documentation/bundleresources/privacy_manifest_files
- Apple — Required Reason API list: https://developer.apple.com/documentation/bundleresources/privacy_manifest_files/describing_use_of_required_reason_api
- Apple — Keychain Services: https://developer.apple.com/documentation/security/keychain_services
- Apple — Hardened Runtime: https://developer.apple.com/documentation/security/hardened_runtime
- Apple — App Transport Security: https://developer.apple.com/documentation/security/preventing_insecure_network_connections
- Apple — Universal Links: https://developer.apple.com/documentation/xcode/supporting-universal-links-in-your-app
- OWASP Mobile Application Security (MAS) Verification Standard: https://mas.owasp.org/MASVS/
- TrustKit (cert pinning): https://github.com/datatheorem/TrustKit
- SwiftLint rule index: https://realm.github.io/SwiftLint/rule-directory.html
- Sparkle update framework: https://sparkle-project.org/documentation/
