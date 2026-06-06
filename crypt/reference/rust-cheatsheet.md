# Rust Cryptographic Architecture Cheatsheet — Crypt

Focused crate-selection and pattern guide for cryptographic architecture review in Rust. Baseline: **Rust 1.85+ / Edition 2024 / rustls 0.23+ / RustCrypto 2024H2** (2026-05).

> Source-of-truth references (full catalog lives in Builder):
> - Constructive crypto / TLS stack: [`builder/reference/rust-best-practices.md` §7 Security practices](../../builder/reference/rust-best-practices.md#7-security-practices) (§7.3 secrecy+zeroize, §7.4 subtle, §7.5 rustls, §7.6 crypto crate matrix)
> - Security pitfalls including constant-time compare, secret logging, CSPRNG misuse: [`builder/reference/rust-anti-patterns.md` §12 Security Pitfalls](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls)
> - Sibling reviewer (SAST-level): [`sentinel/reference/rust-cheatsheet.md`](../../sentinel/reference/rust-cheatsheet.md)

**Do not duplicate the catalogs above.** This cheatsheet is the *crypto design decisions* Crypt makes; it links rather than restates code patterns.

Crypt's audit angle is **algorithm and protocol design**, not regex-grep code review (that is Sentinel). When a code-level fix is the right answer, hand off to Sentinel with the design constraint stated.

---

## 1. TLS stack — `rustls` is the 2026 default

| | `rustls` | `native-tls` |
|---|---|---|
| Implementation | Pure Rust | Wraps SChannel (Win), Secure Transport (macOS), OpenSSL (Linux) |
| Memory safety | No `unsafe` in TLS state machine (only in the crypto backend) | Inherits whatever the OS provides |
| Cipher policy | Modern only — TLS 1.2+, no RC4, no MD5, no CBC-with-SHA1 | Whatever the OS allows; varies wildly by platform |
| FIPS | `rustls-fips` variant + `aws-lc-rs` backend → FIPS-validated module | Inherits OS posture (Windows yes; macOS no; Linux depends on distro) |
| Build deps | None — works on Alpine/scratch images | Requires OpenSSL headers (frustrating on Alpine, Windows) |
| Trust store | App-bundled (`webpki-roots`) OR system (`rustls-platform-verifier`) | Always system |
| **2026 default** | **Yes** | Only when interop with the OS trust store is a hard requirement and `rustls-platform-verifier` is insufficient |

Backend choice within `rustls`:

```toml
# Default — ring (BoringSSL-derived); broadest platform support
rustls = "0.23"

# aws-lc-rs (AWS's BoringSSL fork) — FIPS-validatable, faster on aarch64
rustls = { version = "0.23", default-features = false, features = ["aws_lc_rs"] }
```

Trust-store choice:

| Crate | Use |
|-------|-----|
| `webpki-roots` | App-bundled Mozilla CA set. Reproducible, deterministic, no OS interaction. **Preferred for servers and most clients.** |
| `rustls-native-certs` | Read the OS trust store at startup (one-shot). Useful when corporate CAs are added system-wide. |
| `rustls-platform-verifier` | Delegate verification to the OS verifier on every connection (uses CryptoAPI / Security.framework / OpenSSL). Required when the platform performs MDM-driven trust pinning, OCSP stapling enforcement, or revocation. |

Reference: [`builder/reference/rust-best-practices.md` §7.5](../../builder/reference/rust-best-practices.md#7-security-practices). Migration: `tokio-tls` / `hyper-tls` → `tokio-rustls` / `hyper-rustls`.

---

## 2. Crypto primitives — RustCrypto suite is the 2026 default

| Need | Preferred crate (2026) | Alternative | Notes |
|------|------------------------|-------------|-------|
| AEAD (symmetric) | `aes-gcm` (AES-GCM), `chacha20poly1305` | `ring::aead`, `aws-lc-rs::aead` | RustCrypto crates are audit-friendly. `ring` is mature and high-perf. |
| AEAD with nonce-misuse resistance | `aes-gcm-siv`, `aead::AeadMisuseResistant` | — | Use when callers may reuse nonces (multi-writer scenarios). |
| Stream / extended-nonce | `xchacha20poly1305` (extended 192-bit nonce) | — | Random nonces become collision-safe; use for stateless encryptors. |
| SHA-2 | `sha2` | `ring::digest`, `blake3` | BLAKE3 for general hashing (faster, tree-hashing). SHA-256 for protocol compatibility. |
| SHA-3 / SHAKE | `sha3` | — | When the spec mandates SHA-3 / Keccak. |
| HMAC | `hmac` + `sha2` | `ring::hmac` | |
| Password hashing | `argon2` (Argon2id) | `password-hash` trait for poly-impl | Argon2id is the **2026 default**. See §5. |
| Public-key signing | `ed25519-dalek` v2 | `ring::signature::Ed25519` | Pure-Rust Ed25519. `ed25519` trait crate for poly-impl. |
| Key exchange | `x25519-dalek` | `ring::agreement::X25519` | Pure-Rust X25519. |
| RSA / ECDSA P-256 / P-384 | `rsa`, `p256`, `p384` | `ring::signature` | RustCrypto for spec compatibility. `ring`/`aws-lc-rs` for perf-critical paths. |
| Postquantum KEM | `ml-kem` (FIPS 203, formerly Kyber) | `pqcrypto-kyber` (legacy name) | See §9. |
| Postquantum sig | `ml-dsa` (FIPS 204, formerly Dilithium) | `slh-dsa` (FIPS 205, SPHINCS+) | See §9. |
| Mid-level all-in-one | `ring`, `aws-lc-rs` | RustCrypto suite | `ring` is BoringSSL-derived. `aws-lc-rs` is AWS's BoringSSL fork — FIPS-validatable. |
| TLS (consumes the above) | `rustls` | `native-tls` | See §1. |

Reference: [`builder/reference/rust-best-practices.md` §7.6](../../builder/reference/rust-best-practices.md#7-security-practices).

**Choosing RustCrypto vs `ring`/`aws-lc-rs`**:

| Criterion | RustCrypto | `ring` / `aws-lc-rs` |
|-----------|------------|----------------------|
| Pure Rust | ✓ (most crates) | Hybrid Rust + C/asm |
| Audit footprint | Smaller per primitive | Larger but well-audited (BoringSSL lineage) |
| Performance | Good; some primitives within 5% of `ring` | Usually fastest on x86_64 / aarch64 |
| FIPS path | Some crates (`fips204-rs`); not certified | `aws-lc-rs` is FIPS-validated |
| Stability / API freeze | Per-crate, often semver-stable | `ring` has slower release cadence |
| Embedded / `no_std` | Most RustCrypto crates support `no_std` | `ring` requires std |

**Rule of thumb**: RustCrypto for application code; `ring`/`aws-lc-rs` when FIPS, embedded perf, or BoringSSL parity is required.

---

## 3. Constant-time operations — `subtle`

Plain `==` on `&[u8]` short-circuits on the first mismatched byte. This is a **timing oracle**: an attacker can probe the length of a matching prefix.

**Always use `subtle::ConstantTimeEq` when comparing**:

- Authentication tokens
- API keys / session IDs
- MAC outputs / HMAC tags
- Password hashes
- Signature bytes prior to cryptographic verification

```rust
use subtle::ConstantTimeEq;

// FLAG: plain ==
if user_token == stored_token { /* accept */ }       // timing leak

// FIX: ct_eq returns subtle::Choice (constant-time bool)
if bool::from(user_token.ct_eq(&stored_token)) { /* accept */ }
```

**Length-mismatch leak**: `ct_eq` is constant-time *only when lengths match*. Early-returning on length mismatch leaks length. For variable-length comparisons, pad to a fixed length first or accept that length is non-secret.

**Branchless selection**: `subtle::ConditionallySelectable` provides `T::conditional_select(&a, &b, choice)` for branchless `if`.

Reference: [`builder/reference/rust-best-practices.md` §7.4](../../builder/reference/rust-best-practices.md#7-security-practices), [anti-patterns §12.11](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls).

---

## 4. Secret material lifecycle

Three crates compose; each owns one stage:

| Stage | Crate | What |
|-------|-------|------|
| In-memory representation | `secrecy::SecretBox<T>` / `SecretString` | Excludes self from `Debug`, `Display`, `Serialize` (no serde leak). Exposes via explicit `expose_secret()` — grep-able at every read site. |
| Heap wipe on drop | `zeroize::Zeroize` + `ZeroizeOnDrop` | Overwrites bytes with zeros before deallocation. Volatile-write to defeat optimizer. |
| Newtype safety | Manual `Drop` + opt-out `Debug`/`Display` | When the type is exposed in a public API surface. |

**Required minimum for any secret type**:

```rust
use secrecy::{SecretBox, ExposeSecret};
use zeroize::{Zeroize, ZeroizeOnDrop};

#[derive(Zeroize, ZeroizeOnDrop)]
struct ApiKey {
    inner: SecretBox<String>,    // SecretBox handles Debug/Display redaction
}

impl ApiKey {
    pub fn new(s: String) -> Self {
        Self { inner: SecretBox::new(Box::new(s)) }
    }
}

// Reading the secret — explicit, grep-able, narrowly scoped
fn auth_header(k: &ApiKey) -> String {
    format!("Bearer {}", k.inner.expose_secret())
}
```

**Hard rules**:

1. **Never** `#[derive(Debug)]` on a struct holding a non-`Secret*` secret field. `{:?}` is logged in panics, error chains, and `tracing`.
2. **Never** `#[derive(Clone)]` on `SecretBox` containers casually — each clone is a copy of the secret. Prefer reference-passing (`&SecretBox<T>`) or `Arc<SecretBox<T>>` for shared read access.
3. **Never** `#[derive(Serialize)]` on a struct containing a secret without `#[serde(skip)]` on that field. `secrecy::SecretBox` is `!Serialize` by default — this is by design.
4. **Always** `Zeroize` heap-allocated secret buffers (Vec<u8>, String). Stack-allocated `[u8; N]` is overwritten by `Zeroize` too — necessary for ephemeral keys.

Reference: [`builder/reference/rust-best-practices.md` §7.3](../../builder/reference/rust-best-practices.md#7-security-practices), [anti-patterns §12.2, §12.3, §12.18, §12.20](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls).

---

## 5. Password hashing — Argon2id with 2026 parameters

```rust
use argon2::{Argon2, Algorithm, Version, Params, PasswordHasher, PasswordVerifier};
use argon2::password_hash::{PasswordHash, SaltString, rand_core::OsRng};

// 2026 OWASP-aligned defaults — m=46 MiB, t=1, p=1
// Match against your latency budget and threat model; never go below these.
let params = Params::new(
    46 * 1024,   // m_cost in KiB (46 MiB)
    1,           // t_cost (time / iterations)
    1,           // p_cost (parallelism / lanes)
    None,        // output length (default 32 bytes)
)?;
let argon2 = Argon2::new(Algorithm::Argon2id, Version::V0x13, params);

// Hashing
let salt = SaltString::generate(&mut OsRng);
let hash = argon2.hash_password(password.expose_secret().as_bytes(), &salt)?.to_string();

// Verification
let parsed = PasswordHash::new(&hash)?;
Argon2::default().verify_password(password.expose_secret().as_bytes(), &parsed)?;
```

**Parameter selection** (target: 50–500 ms hash time on the server you'll run it on):

| Profile | m_cost | t_cost | p_cost | Rough latency on a 2026 server core |
|---------|--------|--------|--------|--------------------------------------|
| Interactive (login) | 19 MiB | 2 | 1 | ~50 ms |
| **OWASP 2024 minimum** | 46 MiB | 1 | 1 | ~100 ms |
| Sensitive (admin) | 64 MiB | 3 | 4 | ~300 ms |
| Backup / key derivation | 256 MiB | 4 | 8 | ~1 s |

**Migration from bcrypt / PBKDF2 / scrypt**:

Use the `password-hash` trait + multi-algorithm verifier on login:

```rust
use password_hash::PasswordHash;

let parsed = PasswordHash::new(&stored_hash)?;
match parsed.algorithm.as_str() {
    "argon2id" => argon2::Argon2::default().verify_password(pw, &parsed)?,
    "bcrypt"   => bcrypt::verify_pw_via_trait(pw, &parsed)?,   // legacy
    "pbkdf2"   => pbkdf2::Pbkdf2.verify_password(pw, &parsed)?,
    _ => return Err(UnknownAlgo),
}
// On success, opportunistically re-hash under Argon2id and update the row.
```

Reference: [`builder/reference/rust-best-practices.md` §7.6](../../builder/reference/rust-best-practices.md#7-security-practices) for the crate matrix. Existing skill reference: [`crypt/reference/password-hashing.md`](./password-hashing.md) for the deep dive.

---

## 6. Key management — envelope encryption pattern

Rust clients for the three major KMS providers:

| KMS | Crate |
|-----|-------|
| AWS KMS | `aws-sdk-kms` (official) |
| GCP Cloud KMS | `gcloud-sdk` + `google-cloud-kms` or hand-rolled gRPC via `tonic` |
| Azure Key Vault | `azure_security_keyvault` |
| HashiCorp Vault | `vaultrs`, `hashicorp_vault` |

**Envelope encryption pattern** (the only pattern that scales):

```text
1. Generate a Data Encryption Key (DEK) locally: 32 random bytes from OsRng.
2. Encrypt payload with DEK using `aes-gcm` or `chacha20poly1305`.
3. Send DEK to KMS for encryption under a Customer Master Key (CMK).
   → Receive encrypted DEK (EDEK).
4. Store: { EDEK, AEAD ciphertext, AEAD nonce }. Discard plaintext DEK after Zeroize.
5. To decrypt: send EDEK to KMS, receive plaintext DEK, decrypt payload, Zeroize DEK.
```

Why: payload is encrypted locally (cheap, no per-byte KMS calls); only the small DEK round-trips to KMS (cost + latency bounded); CMK never leaves KMS HSM.

**Key rotation**: re-encrypt only the EDEK (cheap), keep payload ciphertext intact. Rotate CMK on schedule (90d typical) or on incident.

**Rust idioms**:

```rust
use aes_gcm::{Aes256Gcm, KeyInit, AeadInPlace};
use aes_gcm::aead::OsRng as AeadOsRng;
use zeroize::Zeroizing;

// 1. Generate DEK
let mut dek_bytes = Zeroizing::new([0u8; 32]);
getrandom::getrandom(dek_bytes.as_mut())?;
let dek = Aes256Gcm::new_from_slice(&*dek_bytes)?;

// 2. Encrypt payload
let mut nonce = [0u8; 12];
getrandom::getrandom(&mut nonce)?;
let mut ciphertext = plaintext.to_vec();
dek.encrypt_in_place((&nonce).into(), aad, &mut ciphertext)?;

// 3. Wrap DEK under CMK via KMS
let edek = kms_client.encrypt()
    .key_id(cmk_arn)
    .plaintext(Blob::new(&*dek_bytes))
    .send().await?;

// 4. Zeroizing<[u8; 32]> wipes dek_bytes on drop automatically.
```

Existing skill reference: [`crypt/reference/kms-integration.md`](./kms-integration.md) for the deep dive.

---

## 7. Cryptographically secure randomness

Rust has two parallel RNG worlds; mixing them is the most common bug.

| Crate / Trait | Use |
|---------------|-----|
| `getrandom::getrandom(&mut bytes)?` | Direct CSPRNG bytes from the OS. **Use this for every cryptographic seed.** |
| `rand_core::CryptoRng` (marker trait) | Bound on functions that need a CSPRNG: `fn keygen<R: CryptoRng + RngCore>(rng: &mut R)`. |
| `rand::rngs::OsRng` | `Rng`-trait wrapper over `getrandom`. Use when you need the `Rng` interface (e.g. `OsRng.fill_bytes(&mut k)`). |
| `rand::thread_rng()` | **Not crypto.** Returns `ThreadRng`, which uses ChaCha-12 seeded from `OsRng`. It implements `CryptoRng` since rand 0.9 — but **only use it for crypto when you have explicitly checked** that the current `rand` version's `ThreadRng` carries the bound. Safer: bind on `CryptoRng + RngCore` and let callers pass `OsRng`. |
| `rand::rngs::StdRng::seed_from_u64(seed)` | **Never for crypto** — deterministic from a small seed. Test fixtures only. |

```rust
// FLAG — seeding crypto from non-CSPRNG
let mut key = [0u8; 32];
let mut rng = StdRng::from_entropy();    // OK-ish, but verify path
rng.fill_bytes(&mut key);

// FIX — direct from OS CSPRNG
let mut key = [0u8; 32];
getrandom::getrandom(&mut key)?;

// FIX — generic over CryptoRng
fn keygen<R: rand_core::CryptoRng + rand_core::RngCore>(rng: &mut R) -> SecretBox<[u8; 32]> {
    let mut k = [0u8; 32];
    rng.fill_bytes(&mut k);
    SecretBox::new(Box::new(k))
}
```

Reference: [anti-patterns §12.12](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls).

---

## 8. Signing and verification

| Algorithm | Crate | API style |
|-----------|-------|-----------|
| Ed25519 | `ed25519-dalek` v2 | `SigningKey` / `VerifyingKey`, returns `Signature`; implements the `ed25519` trait crate for poly-impl. |
| Ed25519 (alt) | `ring::signature::Ed25519KeyPair` | C-derived, slightly faster on some platforms. |
| ECDSA P-256 / P-384 | `p256`, `p384` (RustCrypto) | Implements `signature::Signer` / `Verifier`. |
| ECDSA (alt) | `ring::signature::EcdsaKeyPair` | |
| RSA-PSS / RSA-PKCS1v15 | `rsa` | Avoid PKCS1v15 for new signing; use PSS. |
| X.509 / certificate parsing | `x509-parser`, `x509-cert` | Parse-only; pair with `rustls::server::ResolvesServerCert` for live use. |

**Webcrypto compatibility** (when interop with browser JWT/COSE/JWS):

| Web algorithm | Rust crate path |
|---------------|------------------|
| `EdDSA` (Ed25519) | `ed25519-dalek` |
| `ES256` (ECDSA P-256 SHA-256) | `p256` + `ecdsa` |
| `ES384` | `p384` + `ecdsa` |
| `RS256` (RSA-PKCS1v15 SHA-256) | `rsa` with PKCS1v15 (legacy interop only) |
| `PS256` (RSA-PSS SHA-256) | `rsa` with PSS |
| `HS256` (HMAC-SHA-256) | `hmac` + `sha2` |

**The `signature` trait crate** provides poly-implementation:

```rust
use signature::{Signer, Verifier};

fn sign_with_any<S: Signer<Sig>, Sig>(key: &S, msg: &[u8]) -> Sig {
    key.sign(msg)
}
```

This is how you write generic code that works across Ed25519 / ECDSA / RSA.

---

## 9. Post-quantum (2026 status)

NIST finalized three standards in FIPS 203 / 204 / 205 (Aug 2024). Rust ecosystem:

| Algorithm | Standard | Rust crate (2026) |
|-----------|----------|--------------------|
| ML-KEM (was Kyber) | FIPS 203 | `ml-kem` (pure Rust, RustCrypto), `pqcrypto-kyber` (FFI to PQClean, legacy name) |
| ML-DSA (was Dilithium) | FIPS 204 | `ml-dsa` (pure Rust, RustCrypto), `pqcrypto-dilithium` |
| SLH-DSA (was SPHINCS+) | FIPS 205 | `slh-dsa`, `pqcrypto-sphincsplus` |
| Hybrid TLS (classical + PQ KEM) | Drafts | `rustls` 0.23+ has X25519-MLKEM768 hybrid KX behind a feature flag (status: stable as of rustls 0.23.x in 2026); `aws-lc-rs` backend ships hybrid by default |

**Migration strategy** (as of 2026-05):

1. **TLS**: enable hybrid `X25519-MLKEM768` in `rustls` if your client/server are both Rust and updated. Falls back to classical if peer doesn't support it.
2. **Long-term signatures** (code signing, certificate roots, document archives): begin issuing dual signatures (Ed25519 + ML-DSA) so verifiers that don't yet support PQ can fall back. Plan a 5–10 year crossover.
3. **Sealed long-term data** (encrypted archives kept for >10 years): wrap with PQ-KEM today — harvest-now-decrypt-later attacks. Use `ml-kem` to derive a key, encrypt payload under that key with AES-GCM or ChaCha20-Poly1305.
4. **Short-lived ephemeral keys** (session keys, OAuth tokens): low priority for PQ migration; classical X25519 + AES-GCM remains acceptable through 2030.

Existing skill reference: [`crypt/reference/post-quantum-migration.md`](./post-quantum-migration.md) for the deep dive.

---

## 10. JWT / JWS / JOSE

Two competing crates:

| Crate | Pros | Cons |
|-------|------|------|
| `jsonwebtoken` | Most popular, simple API, decent algorithm coverage | No `none` algorithm rejection by default in older versions — verify your version locks it out. No JWE. |
| `josekit` | Full JOSE: JWS + JWE + JWK + JWS-detached. Closer to spec. | Larger surface, steeper learning curve. |

**Mandatory hardening for both**:

```rust
use jsonwebtoken::{Algorithm, DecodingKey, Validation, decode};

let mut validation = Validation::new(Algorithm::RS256);
validation.algorithms = vec![Algorithm::RS256, Algorithm::ES256];   // ← allowlist
validation.required_spec_claims.insert("exp".to_string());
validation.required_spec_claims.insert("iss".to_string());
validation.required_spec_claims.insert("aud".to_string());
validation.set_audience(&["my-service"]);
validation.set_issuer(&["https://my-issuer.example"]);

let token = decode::<Claims>(&jwt, &decoding_key, &validation)?;
```

**Critical rules**:

1. **Always set `algorithms` to an explicit allowlist.** Default validators may accept whatever `alg` header the token claims. Attacker sends `alg: none` → bypasses signature check.
2. **Reject `alg: none` unconditionally.** Even if a library has a "verify_with_no_signature" mode, do not call it.
3. **Reject `alg: HS*` when you are an RS/ES verifier.** Attacker swaps to HMAC and signs with the public key as the HMAC key — classic alg-confusion attack.
4. **Validate `iss`, `aud`, `exp`, `nbf`.** Set `leeway` only with documented reason.
5. **For RS256/ES256**: use a `DecodingKey` constructed from a *specific* public key, not from a JWKS endpoint that the token's `kid` can manipulate without bounds.

Reference: [anti-patterns §12.6](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls) on deserialization (JWT claim payload is JSON — same body-size and budget rules apply).

---

## 11. Common pitfalls — Crypt-specific design errors

| Pitfall | Why it's wrong |
|---------|----------------|
| **Early-return on length mismatch** before constant-time compare | Leaks length of the secret. Pad to fixed length first, or accept length is non-secret. |
| **`.clone()` on `SecretBox<T>`** in business logic | Each clone is a copy of the secret in memory. Prefer reference-passing or `Arc<SecretBox<T>>`. |
| **Calling `expose_secret()` far from use site** | The secret-as-`&str` lifetime is wider than necessary. Inline the expose: `format!("{}", k.expose_secret())`. |
| **Forgetting `Zeroize` on temp buffers** | Stack-allocated `[u8; 32]` left for the compiler. Use `Zeroizing<[u8; 32]>` for scope-bound wipe. |
| **Using `==` to compare ciphertexts before decryption** | Not strictly a timing oracle since ciphertext is not secret — but `ct_eq` is harmless and you avoid the question. |
| **Reusing AEAD nonces** | Catastrophic for AES-GCM (key recovery from two encryptions with same nonce). Use random 96-bit nonce + `xchacha20poly1305` for extra margin, or a deterministic counter with strict bookkeeping. |
| **Encrypting variable-length plaintext to a fixed-size buffer with PKCS#7 padding** in modern protocols | Use AEAD instead. CBC + HMAC + padding has had 20 years of padding-oracle attacks (POODLE, Lucky13). |
| **Trusting cipher choice from the wire** (`alg` in JWT, `cipher_suite` in custom protocol) | Always pin acceptable algorithms at the verifier. |
| **Generating IVs from `chrono::Utc::now()`** | Predictable. Use `OsRng` / `getrandom`. |
| **Implementing crypto primitives by hand** | Reject categorically; route to RustCrypto / `ring` / `aws-lc-rs`. |
| **`tracing::info!("decrypted: {plaintext:?}")`** | Logs plaintext at INFO level. Audit log shippers, SaaS observability vendors. See [anti-patterns §12.2](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls). |

---

## Triage priorities

When multiple findings stack, rank by:

1. **Hand-rolled crypto primitives** — categorical reject; route to a vetted crate.
2. **Algorithm-confusion vulnerabilities** (JWT `none`, RS↔HS, downgrade) — directly exploitable, often missed in audits.
3. **AEAD nonce reuse** — single instance can leak the key. Audit any deterministic-nonce scheme rigorously.
4. **Timing leaks** (`==` on secrets, early-return on length) — exploitable with sufficient samples.
5. **CSPRNG misuse** (non-CryptoRng for keys, predictable IV) — directly weakens the protocol's security claim.
6. **Secret material lifecycle** (missing Zeroize, Debug derive on secrets, log leaks) — silent and persistent.
7. **Weak password hashing** (bcrypt with low cost factor, PBKDF2 with insufficient iterations) — migration path needed.
8. **TLS stack choice** (native-tls in 2026 for non-interop reason) — design-level, propose `rustls` migration.
9. **PQ readiness gap** for long-lived data (≥10 year archives, code signing) — not urgent today but plan the migration.

---

## Sources

- `rustls` book: https://docs.rs/rustls/
- RustCrypto organization: https://github.com/RustCrypto
- `ring`: https://github.com/briansmith/ring
- `aws-lc-rs`: https://github.com/aws/aws-lc-rs
- `secrecy` crate: https://docs.rs/secrecy/
- `zeroize` crate: https://docs.rs/zeroize/
- `subtle` crate: https://docs.rs/subtle/
- `argon2` crate: https://docs.rs/argon2/
- `password-hash` trait: https://docs.rs/password-hash/
- `getrandom`: https://docs.rs/getrandom/
- `ed25519-dalek` v2: https://docs.rs/ed25519-dalek/
- `signature` trait: https://docs.rs/signature/
- `ml-kem` (FIPS 203): https://docs.rs/ml-kem/
- `ml-dsa` (FIPS 204): https://docs.rs/ml-dsa/
- `jsonwebtoken`: https://docs.rs/jsonwebtoken/
- `josekit`: https://docs.rs/josekit/
- NIST FIPS 203 (ML-KEM): https://csrc.nist.gov/pubs/fips/203/final
- NIST FIPS 204 (ML-DSA): https://csrc.nist.gov/pubs/fips/204/final
- NIST FIPS 205 (SLH-DSA): https://csrc.nist.gov/pubs/fips/205/final
- OWASP Argon2 cheatsheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
