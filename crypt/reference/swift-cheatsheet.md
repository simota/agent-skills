# Swift Cryptographic Architecture Cheatsheet — Crypt

Focused crate/framework-selection and pattern guide for cryptographic architecture review in Swift. Baseline: **Swift 6.2+ / CryptoKit (Apple) + swift-crypto 4.x (cross-platform)** with **Swift 6.3 outlook** (2026-05).

> Source-of-truth references (full catalog lives in Builder):
> - Production library matrix (server + Apple platforms): [`builder/reference/swift-best-practices.md` §9 Production Library Matrix](../../builder/reference/swift-best-practices.md#9-production-library-matrix-2026)
> - Server-side Swift (Vapor / Hummingbird) HTTP stack: [`builder/reference/swift-best-practices.md` §8 Server-Side Swift](../../builder/reference/swift-best-practices.md#8-server-side-swift)
> - Memory model and ARC semantics (relevant for secret-buffer hygiene): [`builder/reference/swift-language-spec.md` §9 Memory Model & ARC](../../builder/reference/swift-language-spec.md#9-memory-model--arc)
> - Concurrency model (for thread-safe key/session containers): [`builder/reference/swift-language-spec.md` §3 Concurrency Model](../../builder/reference/swift-language-spec.md#3-concurrency-model)
> - Sibling reviewers: [`sentinel/reference/swift-cheatsheet.md`](../../sentinel/reference/swift-cheatsheet.md)
> - Crypt deep-dive references (cross-language): [`password-hashing.md`](./password-hashing.md), [`kms-integration.md`](./kms-integration.md), [`post-quantum-migration.md`](./post-quantum-migration.md)

**Do not duplicate the catalogs above.** This cheatsheet is the *Swift-specific crypto design decisions* Crypt makes; it links rather than restates.

Crypt's audit angle is **algorithm and protocol design**, not regex-grep code review (that is Sentinel). When a code-level fix is the right answer, hand off to Sentinel with the design constraint stated.

---

## 1. CryptoKit vs swift-crypto — choose by platform target

| Need | Library | Why |
|------|---------|-----|
| Apple-platform-only app (iOS / macOS / tvOS / watchOS / visionOS) | **`CryptoKit`** (system framework) | Free, no dep size, hardware acceleration via CommonCrypto / SecureEnclave |
| Cross-platform Swift (Linux server, embedded, KMP-Swift) | **`swift-crypto`** | Apple-shipped, BoringSSL-backed, API parity with CryptoKit |
| Both targets in one Package.swift | `swift-crypto` everywhere | Single-source — CryptoKit's API surface is a subset; swift-crypto provides identical names so platform conditionals are unneeded |

```swift
// Package.swift — recommended pattern
.package(url: "https://github.com/apple/swift-crypto.git", from: "4.0.0"),

// In source:
#if canImport(CryptoKit)
import CryptoKit          // Apple platforms: free, framework-backed
#else
import Crypto             // Linux: swift-crypto pure Rust+BoringSSL
#endif
```

`swift-crypto` 3.0+ provides matching APIs (`AES.GCM`, `P256.Signing`, etc.) so most code is platform-conditional-free if you just `import Crypto` — the package umbrella header re-exports `CryptoKit` symbols on Apple.

**Boundary**: `CryptoKit.SecureEnclave.*` types exist only on Apple. swift-crypto does NOT replicate them.

---

## 2. Symmetric encryption — AES-GCM and ChaChaPoly

| Use | Type | Notes |
|-----|------|-------|
| AEAD (default) | `AES.GCM` | 128/192/256-bit keys; 96-bit nonce; 16-byte tag |
| AEAD on platforms without AES-NI (older ARM, software) | `ChaChaPoly` | 256-bit key; 96-bit nonce; 16-byte tag |
| Streaming / chunked AEAD | Build on `AES.GCM.SealedBox` with per-chunk nonces | No built-in streaming; implement framing |

```swift
import CryptoKit
import Foundation

// Encrypt
let key = SymmetricKey(size: .bits256)            // CryptoKit-managed; not extractable as Data unless you copy
let nonce = AES.GCM.Nonce()                       // 12 random bytes from kSecRandom
let sealed = try AES.GCM.seal(plaintext, using: key, nonce: nonce, authenticating: aad)
let onWire = sealed.combined!                     // nonce || ciphertext || tag

// Decrypt
let box = try AES.GCM.SealedBox(combined: onWire)
let plaintext = try AES.GCM.open(box, using: key, authenticating: aad)
```

### Nonce uniqueness — the cardinal rule

For AES-GCM with a fixed key, **never reuse a nonce**. A single reused-nonce pair leaks the XOR of the two plaintexts AND can leak the authentication key.

| Strategy | Verdict |
|----------|---------|
| Random 96-bit nonce per encryption (`AES.GCM.Nonce()`) | Safe up to ~2^32 encryptions per key (birthday bound). Default Apple behavior. |
| Counter-based (deterministic) nonce | Safe IF the counter is **persisted across restarts** and never resets without key rotation |
| Counter + restart-on-restart | **UNSAFE** — restart resets counter, reuses nonces |
| ChaChaPoly with random nonce | Same as AES-GCM — safe up to ~2^32 |
| `AES.GCM.SIV` (nonce-misuse-resistant) | **Not in CryptoKit / swift-crypto as of 2026-05** — use the IETF `XChaCha20-Poly1305` extension for misuse resistance, available via `swift-crypto` extensions |

**Architectural rule**: if multiple writers (multi-instance server) share an AES-GCM key, each writer must have a non-overlapping nonce space (counter prefix per instance) OR you must use random nonces with key rotation before reaching 2^32 encryptions.

---

## 3. Asymmetric — curves and signing

| Use | Type | Notes |
|-----|------|-------|
| Modern signing | `Curve25519.Signing.PrivateKey` / Ed25519 | 32-byte keys, deterministic, fastest |
| Key agreement (ECDH-X25519) | `Curve25519.KeyAgreement.PrivateKey` | Pair with HKDF |
| Interop signing (older systems, PKI) | `P256.Signing.PrivateKey` (ECDSA P-256) | NIST curve; required for many JWT / X.509 contexts |
| Higher security margin | `P384.Signing.PrivateKey` / `P521.Signing.PrivateKey` | Slower; required by some compliance (CNSA) |

```swift
// Sign / verify
let signer = Curve25519.Signing.PrivateKey()
let sig = try signer.signature(for: message)
try signer.publicKey.isValidSignature(sig, for: message)   // throws on mismatch

// Key agreement (ECDH)
let ours = Curve25519.KeyAgreement.PrivateKey()
let shared = try ours.sharedSecretFromKeyAgreement(with: theirPublicKey)
let symKey: SymmetricKey = shared.hkdfDerivedSymmetricKey(
    using: SHA256.self,
    salt: salt,
    sharedInfo: Data("session-v1".utf8),
    outputByteCount: 32
)
```

### When NOT to use a curve

| Avoid | Why |
|-------|-----|
| ECDSA P-256 without a deterministic nonce (RFC 6979) | Non-deterministic ECDSA + bad RNG → leaks private key (PS3 hack). CryptoKit uses deterministic nonce by default; `swift-crypto` matches. Verify if hand-coded. |
| RSA-PKCS1v15 for signing new code | Padding-oracle history; use RSA-PSS (`_RSA.Signing.PSS`) from `swift-crypto`'s `_RSA` module |
| RSA-2048 for ≥10-year archives | Begin PQ transition; see §9 |
| secp256k1 (Bitcoin curve) | Not in CryptoKit / swift-crypto. Use `swift-secp256k1` only when Bitcoin/Ethereum interop is the requirement. |

---

## 4. HKDF — key derivation from a shared secret

```swift
let derived: SymmetricKey = HKDF<SHA256>.deriveKey(
    inputKeyMaterial: ikm,            // SymmetricKey from KeyAgreement output or password
    salt: salt,                       // 16+ bytes, may be public
    info: Data("session-v1".utf8),    // context binding; include protocol version
    outputByteCount: 32
)
```

| Salt | When |
|------|------|
| Random 16+ bytes per session | Default; gives independence between sessions |
| Empty / nil | Acceptable only when the IKM is already high-entropy and unique per session |
| Constant | Reject — defeats the purpose of HKDF |

**`info` parameter discipline**: include the protocol name + version + role + any context (e.g. `"my-protocol-v2-client-session"`). This binds the derived key to a specific use; rotating `info` rotates the key.

---

## 5. Secure Enclave (Apple devices only)

`CryptoKit.SecureEnclave` provides hardware-backed P-256 keys that **cannot be exported**. The private key never leaves the SE; signing/key-agreement operations happen inside the SE chip.

```swift
import CryptoKit
import LocalAuthentication

guard SecureEnclave.isAvailable else { /* fallback to keychain-backed software key */ }

// Create with access control (require biometric + passcode)
let access = SecAccessControlCreateWithFlags(
    nil, kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly,
    [.privateKeyUsage, .biometryCurrentSet], nil
)!
let key = try SecureEnclave.P256.Signing.PrivateKey(accessControl: access)

// dataRepresentation is opaque (encrypted blob) — store this, not the key bytes
let stored = key.dataRepresentation
// Reload later
let reloaded = try SecureEnclave.P256.Signing.PrivateKey(dataRepresentation: stored)
```

| Use Secure Enclave when | |
|--------------------------|---|
| Device authentication / user identity | ✓ — gate signing on biometrics |
| Long-lived device-bound credentials (Passkey provider, FIDO2 attestation) | ✓ |
| Encryption keys for at-rest data | ✓ — derive symmetric key via SE-key-agreement on each open |
| Server-side keys | ✗ — Apple devices only |
| Algorithms beyond P-256 | ✗ — SE supports P-256 only |

**Audit checklist**:
- `accessControl` flags appropriate to threat (passcode vs biometric vs both)
- Fallback path when `SecureEnclave.isAvailable == false` (simulator, older devices)
- `dataRepresentation` stored in Keychain (not Defaults / file) for at-rest protection of the encrypted blob

---

## 6. Password hashing — no Apple built-in

Neither CryptoKit nor swift-crypto provides Argon2, bcrypt, or scrypt. You must add a third-party crate.

| Crate | Verdict |
|-------|---------|
| `swift-bcrypt` (vapor/bcrypt) | Acceptable for legacy. Cost factor 12+ in 2026. |
| `Argon2Swift` (tmthecoder) | **Preferred new code** — pure Swift Argon2id |
| `Crypto.Argon2` from `swift-crypto`? | **Not present as of 2026-05** — Apple has discussed adding password-hashing primitives but nothing shipped |
| Hand-rolled PBKDF2 via CommonCrypto | Acceptable for compatibility with existing PBKDF2 corpora; not for new design |
| Vapor's `Bcrypt` | Wraps `swift-bcrypt`; OK for Vapor stacks |

```swift
import Argon2Swift

// 2026 OWASP-aligned defaults for Argon2id
let salt = Salt.generateRandomSalt(length: 16)
let result = try Argon2Swift.hashPasswordString(
    password: password,
    salt: salt,
    iterations: 1,                              // t_cost
    memory: 47104,                              // m_cost in KiB (~46 MiB)
    parallelism: 1,                             // p_cost
    length: 32,                                 // output bytes
    type: Argon2Type.id                         // Argon2id (recommended)
)
let stored = result.encodedString()             // PHC-format string; safe to store
// Verify:
let ok = try Argon2Swift.verifyHashString(password: candidate, hash: stored, type: .id)
```

Crypt cross-reference: [`password-hashing.md`](./password-hashing.md) for the deep dive on parameter selection and migration matrix.

---

## 7. Constant-time comparison — no stdlib helper

Swift has **no built-in** constant-time byte compare. `==` on `Data`/`[UInt8]` short-circuits on first mismatch — timing oracle.

| Option | Notes |
|--------|-------|
| `swift-crypto` `HMAC.isValidAuthenticationCode(_:authenticating:using:)` | Constant-time by construction; use this for HMAC verification — don't recompute HMAC then `==` it |
| Hand-rolled in `subtle`-style | Required when comparing tokens/hashes; see below |
| `Crypto`-equivalent `safeCompare` | **Not present** in stdlib; some libs provide their own |

```swift
// Constant-time compare — bitwise OR accumulator, no early exit
func ctEq(_ a: Data, _ b: Data) -> Bool {
    guard a.count == b.count else { return false }   // length leak — see below
    var diff: UInt8 = 0
    for i in 0..<a.count {
        diff |= a[i] ^ b[i]
    }
    return diff == 0
}
```

**Length leak**: `guard a.count == b.count` reveals length on mismatch. For variable-length secret comparisons, pad both to a fixed length first, or accept that length is non-secret.

**Use cases that need constant-time**:
- Auth tokens / API keys / session IDs
- HMAC tags / MAC outputs
- Password hash comparison (Argon2/bcrypt verify routines handle this internally — never re-compare hashes manually)
- Signature bytes prior to verification (signatures themselves are not secret, but if your comparison is on a derived secret-like value, use ct)

Reference: pull `subtle`-style helper into a shared `CryptoSupport` target; have Sentinel grep for `==` on token/MAC types.

---

## 8. Secret material lifecycle — Swift specifics

Swift's ARC and Copy-on-Write semantics make secret-wiping **harder than in C or Rust**:

1. `Data` and `String` are value types but with COW backing storage — multiple references share a buffer until mutation.
2. `withUnsafeBytes { $0.bindMemory(to: UInt8.self).update(repeating: 0, count: $0.count) }` writes zeros to the buffer — but Swift may have already moved data to a new buffer via COW.
3. `let s: String = "secret"`: small-string optimization may inline into the `String` struct (no heap), so zeroing the buffer doesn't reach the inlined bytes.
4. Compiler optimization can elide "dead" writes — the zeroing write may be removed if no later read.

**Hard rules**:

1. **Never** `#[derive(Debug)]`-equivalent: `CustomStringConvertible` / `CustomDebugStringConvertible` must redact secret fields. Default Swift `String(describing:)` reflects all properties via `Mirror`.
2. **Refuse Mirror reflection** on secret types — implement `CustomReflectable` returning empty children.
3. **Store secrets in `Data`, not `String`** — `String`'s small-string optimization and UTF-8 normalization make in-place zeroing unreliable.
4. **Wrap with explicit lifetime** via a class with manual `deinit` doing `withUnsafeMutableBytes` + memset:

```swift
final class SecretBytes {
    private var bytes: [UInt8]
    init(_ b: [UInt8]) { self.bytes = b }
    func withSecret<R>(_ body: ([UInt8]) throws -> R) rethrows -> R { try body(bytes) }

    deinit {
        bytes.withUnsafeMutableBufferPointer { buf in
            // memset_s is C; from Swift use Darwin/Glibc memset volatile pattern
            _ = memset_s(buf.baseAddress, buf.count, 0, buf.count)
        }
    }
}
```

5. **`SymmetricKey`** (CryptoKit) already manages its own buffer — prefer it over hand-rolled `[UInt8]` for key bytes.

**Audit rule**: secrets stored in `String` are red flags. Use `Data` + `SymmetricKey` for key material, and a wrapper class for tokens.

---

## 9. Post-quantum (2026 status)

NIST finalized FIPS 203 / 204 / 205 in Aug 2024. Apple ecosystem status:

| Algorithm | Standard | Swift availability (2026-05) |
|-----------|----------|------------------------------|
| ML-KEM (was Kyber) | FIPS 203 | **Not yet** in CryptoKit / swift-crypto stable. `swift-crypto` roadmap discusses PQ; watch repo. |
| ML-DSA (was Dilithium) | FIPS 204 | Same — not yet stable |
| SLH-DSA (was SPHINCS+) | FIPS 205 | Same |
| iMessage PQ3 | Apple proprietary | Already deployed (iMessage end-to-end since iOS 17.4) — not an API |
| TLS hybrid (X25519-MLKEM768) | Drafts / experimental | Network.framework / URLSession follow OS-level TLS stack; check `secitemd` configuration |

**Migration strategy for Swift apps (2026-05)**:

1. **TLS**: rely on Apple's `Network.framework` / `URLSession` to deliver hybrid KX when the OS adopts it (iOS 18.x / macOS 15.x have begun rollout). Application code rarely needs to do anything special.
2. **Long-term archives** (>10 years sealed): wrap symmetric key with `ml-kem` once it lands in swift-crypto; in the meantime, plan the migration but don't ship homegrown PQ KEMs.
3. **Cross-platform PQ today**: use `liboqs` via a `swift-package` wrapper (e.g. `OpenQuantumSafe/liboqs-swift` if community-maintained). Treat as experimental.
4. **Hybrid signatures** (classical + PQ): infrastructure not yet present in CryptoKit; defer until swift-crypto ships.

Crypt cross-reference: [`post-quantum-migration.md`](./post-quantum-migration.md) for the timeline matrix.

---

## 10. JWT / JOSE — algorithm allowlist mandatory

Two main Swift JWT crates:

| Crate | Pros | Cons |
|-------|------|------|
| `jwt-kit` (Vapor) | Server-side mature, full JWS coverage, JWK support | Vapor-ecosystem-focused; works standalone too |
| `JOSESwift` (airsidemobile) | iOS-focused, JWS + JWE | Less active maintenance than jwt-kit |
| `SwiftJWT` (Kitura, archived) | — | **Abandoned** — Kitura is unmaintained; do not use for new code |

```swift
import JWTKit

let signers = JWTSigners()
let jwk = JWK(...)
try signers.use(jwk: jwk)

// Hardened verification
struct Payload: JWTPayload {
    var iss: IssuerClaim
    var aud: AudienceClaim
    var exp: ExpirationClaim
    func verify(using signer: JWTSigner) throws {
        try exp.verifyNotExpired()
        try iss.verifyIntendedAudience(includes: "https://my-issuer.example")
        try aud.verifyIntendedAudience(includes: ["my-service"])
    }
}
let token = try signers.verify(jwtString, as: Payload.self)
```

**Critical rules** (same as the cross-language baseline; see [`rust-cheatsheet.md` §10](./rust-cheatsheet.md#10-jwt--jws--jose)):

1. **Always set an explicit `algorithms` allowlist.** Reject `alg: none` unconditionally.
2. **Reject `alg: HS*` when verifier is RS/ES** (algorithm confusion class).
3. **Validate `iss`, `aud`, `exp`, `nbf`.**
4. **Pin `DecodingKey` to a specific public key**, not a token-controlled JWKS endpoint.
5. For `kid`-driven JWKS lookup, allowlist `kid` values to a known set.

---

## 11. TLS — URLSession / Network.framework

```swift
// URLSession with cert pinning via delegate (see sentinel/reference/swift-cheatsheet.md §5.2)
// For programmatic TLS control, use Network.framework directly:

import Network

let tlsOptions = NWProtocolTLS.Options()
sec_protocol_options_set_min_tls_protocol_version(
    tlsOptions.securityProtocolOptions, .TLSv13
)
sec_protocol_options_append_tls_ciphersuite(
    tlsOptions.securityProtocolOptions,
    tls_ciphersuite_t(rawValue: UInt16(TLS_AES_256_GCM_SHA384))!
)
let params = NWParameters(tls: tlsOptions)
```

| Audit | What |
|-------|------|
| `setMinTLSProtocolVersion(.TLSv13)` for new services | TLS 1.3 minimum in 2026 |
| Cipher suite allowlist | Strip CBC + RC4 + 3DES |
| `verify_block` (cert verification override) | Reject unless implementing strict pinning per Sentinel §5.2 |
| `NWProtocolTLS.Options.security_protocol_options_set_verify_block` returning unconditional pass | Reject — disables verification |
| Mutual TLS (client cert) | `sec_protocol_options_set_local_identity` with `SecIdentityRef` from Keychain |

---

## 12. Randomness — `SystemRandomNumberGenerator` and `kSecRandom`

| API | Verdict |
|-----|---------|
| `SystemRandomNumberGenerator()` | **CSPRNG**, backed by `arc4random_buf` (macOS/iOS) — safe for crypto |
| `Int.random(in: 0..<n)` using default RNG | Uses `SystemRandomNumberGenerator` — safe |
| `SecRandomCopyBytes(kSecRandomDefault, count, &bytes)` | Direct CSPRNG; preferred for filling key buffers |
| `AES.GCM.Nonce()` | CryptoKit uses `kSecRandom` internally — safe |
| `arc4random()` (32-bit) | Acceptable for crypto on Apple platforms (despite the name, modern arc4random is CSPRNG); prefer `SystemRandomNumberGenerator` |
| `Foundation.UUID()` for tokens | UUID v4 is random but only 122 bits; OK for ID uniqueness, not for high-entropy crypto secrets — use 32 random bytes |
| `Date().timeIntervalSince1970` as nonce source | **Reject categorically** — predictable |
| Linear-congruential `srand`/`rand` | **Reject** — not crypto |

```swift
// FIX — direct from CSPRNG
var key = [UInt8](repeating: 0, count: 32)
let status = key.withUnsafeMutableBytes { ptr in
    SecRandomCopyBytes(kSecRandomDefault, ptr.count, ptr.baseAddress!)
}
guard status == errSecSuccess else { throw CryptoError.rng }

// PREFERRED — CryptoKit manages
let symKey = SymmetricKey(size: .bits256)    // uses kSecRandom
```

---

## 13. Common pitfalls — Swift-specific design errors

| Pitfall | Why it's wrong |
|---------|----------------|
| **Storing `SymmetricKey.dataRepresentation` to UserDefaults** | UserDefaults is unencrypted; survives app uninstall on macOS; backed up to iCloud |
| **`String` for secrets, then `secret.data(using: .utf8)`** | UTF-8 normalization (NFC vs NFD) silently changes bytes — same password hashes differently after normalization |
| **`AES.GCM.SealedBox(combined:)` parsing untrusted input without length validation** | Combined format is `nonce(12) || ct || tag(16)` — attacker-supplied `ct` of length 0 is valid syntactically; verify expected size |
| **Reusing `AES.GCM.Nonce()` across encryptions with the same key (e.g. encrypt-then-restart-reset-counter)** | Catastrophic; see §2 |
| **`ECDSA` without RFC 6979 deterministic nonces** | CryptoKit / swift-crypto use deterministic nonces; hand-rolled ECDSA via CommonCrypto may not |
| **`CryptoKit.SHA256.hash(data:)` of a password directly (no salt, no work factor)** | Not password hashing — rainbow tables; see §6 |
| **`Sec*` C API without error code checking** | Many `SecItemAdd` / `SecItemUpdate` calls return non-`errSecSuccess` and silently leave secrets unstored |
| **`NSKeyedArchiver` for serializing crypto state** | Polymorphic — vulnerable to class-swizzling on unarchive. Use `Codable` with explicit types. |
| **Logging `SymmetricKey` via `String(describing:)`** | `Mirror` reflects internal `_storage` |
| **`URLSession` shared session for auth + telemetry** | Connection reuse → telemetry server sees auth cookies; use scoped session |

---

## 14. Crypto stack policy summary

| Concern | Default for 2026 |
|---------|------------------|
| Symmetric AEAD | `AES.GCM` (CryptoKit) or `ChaChaPoly` for non-AES-NI |
| Asymmetric signing | `Curve25519.Signing` (Ed25519); `P256` for PKI interop |
| Key agreement | `Curve25519.KeyAgreement` (X25519) |
| Hashing | `SHA256` / `SHA384`; `BLAKE3` not in CryptoKit (use `blake3-swift` if needed) |
| Password hashing | `Argon2Swift` (Argon2id); `swift-bcrypt` legacy |
| KDF | `HKDF<SHA256>` |
| RNG | `SystemRandomNumberGenerator` / `kSecRandom` |
| TLS | Network.framework / URLSession (TLS 1.3 min); cert pinning per Sentinel §5.2 |
| Hardware key store | `SecureEnclave.P256` for device identity |
| JWT | `jwt-kit` (server) / `JOSESwift` (client); algorithm allowlist mandatory |
| PQ | Wait for swift-crypto stable; iMessage PQ3 deployed transparently |

---

## Triage priorities

When multiple findings stack, rank by:

1. **Hand-rolled crypto primitives** — categorical reject; route to CryptoKit / swift-crypto.
2. **JWT algorithm confusion** (`alg: none`, RS↔HS swap, JWKS-controlled `kid`) — directly exploitable.
3. **AES-GCM nonce reuse risk** (counter reset on restart, multi-instance shared key without nonce-space partitioning) — single instance leaks key material.
4. **Predictable nonce / IV / token** (Date()-based, `arc4random` confusion) — protocol break.
5. **`==` comparison on tokens/HMACs** — timing oracle (rare for short tokens, real for long secrets).
6. **`SecureEnclave` not used when device-bound identity is the threat model** — credentials extractable from backup.
7. **Secret stored in `String`** — small-string optimization, UTF-8 normalization, ARC issues; switch to `Data` + `SymmetricKey`.
8. **`UserDefaults` for credentials** — survives uninstall, syncs via iCloud.
9. **TLS pre-1.3 minimum** — interop legacy that should not apply in 2026.
10. **Weak password hashing** (PBKDF2 low iterations, bcrypt cost <12, plain SHA-256) — migrate to Argon2id.
11. **No PQ posture for >10-year-archive use case** — plan migration once swift-crypto ships PQ.

---

## Sources

- Apple CryptoKit framework: https://developer.apple.com/documentation/cryptokit
- swift-crypto (Apple): https://github.com/apple/swift-crypto
- `swift-asn1` and `swift-certificates` (X.509 in Swift): https://github.com/apple/swift-certificates
- Apple — Storing Keys in the Secure Enclave: https://developer.apple.com/documentation/security/certificate_key_and_trust_services/keys/storing_keys_in_the_secure_enclave
- Apple — Network framework TLS: https://developer.apple.com/documentation/network/protocols
- `jwt-kit` (Vapor): https://github.com/vapor/jwt-kit
- `JOSESwift`: https://github.com/airsidemobile/JOSESwift
- `Argon2Swift`: https://github.com/tmthecoder/Argon2Swift
- `swift-bcrypt` (Vapor): https://github.com/vapor/bcrypt
- iMessage PQ3 (Apple Security Engineering): https://security.apple.com/blog/imessage-pq3/
- NIST FIPS 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA): https://csrc.nist.gov/Projects/post-quantum-cryptography
- OWASP Mobile Application Security Verification Standard: https://mas.owasp.org/MASVS/
- WWDC22 "Secure your data with the Secure Enclave"
- WWDC23 "Improve your network security" (Apple)
