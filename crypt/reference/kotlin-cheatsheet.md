# Kotlin Cryptographic Architecture Cheatsheet — Crypt

Focused library-selection and pattern guide for cryptographic architecture review in Kotlin (JVM and KMP server-side). Baseline: **Kotlin 2.3+ / K2 / Tink 1.13+ / BouncyCastle 1.78+** with **2.4 EAP outlook** (2026-05).

> Source-of-truth references (full catalog lives in Builder):
> - Production library matrix incl. crypto (§10.7), HTTP (§10.1), serialization (§10.3), logging (§10.5): [`builder/reference/kotlin-best-practices.md` §10 Production Library Matrix](../../builder/reference/kotlin-best-practices.md#10-production-library-matrix-2026-baseline)
> - Server-side stack (Ktor / Spring): [`builder/reference/kotlin-best-practices.md` §6 Server-side Kotlin](../../builder/reference/kotlin-best-practices.md#6-server-side-kotlin)
> - Multiplatform basics — `expect`/`actual` for platform crypto: [`builder/reference/kotlin-language-spec.md` §5 Multiplatform (KMP) Basics](../../builder/reference/kotlin-language-spec.md#5-multiplatform-kmp-basics)
> - Java interop pitfalls (relevant for JCA / `KeyStore` access): [`builder/reference/kotlin-anti-patterns.md` §7 Java Interop Pitfalls](../../builder/reference/kotlin-anti-patterns.md#7-java-interop-pitfalls)
> - Sibling reviewers: [`sentinel/reference/kotlin-cheatsheet.md`](../../sentinel/reference/kotlin-cheatsheet.md)
> - Crypt deep-dive references (cross-language): [`password-hashing.md`](./password-hashing.md), [`kms-integration.md`](./kms-integration.md), [`post-quantum-migration.md`](./post-quantum-migration.md)

**Do not duplicate the catalogs above.** This cheatsheet is the *Kotlin-specific crypto design decisions* Crypt makes; it links rather than restates.

Crypt's audit angle is **algorithm and protocol design**, not regex-grep code review (that is Sentinel). When a code-level fix is the right answer, hand off to Sentinel with the design constraint stated.

**Android scope note**: Android-specific patterns (Hardware-backed `KeyStore`, `StrongBox`, BiometricPrompt-gated keys, `EncryptedSharedPreferences`) are owned by the **`native`** skill. This file covers cross-platform Kotlin and server-side JVM crypto.

---

## 1. Crypto stack — Tink is the 2026 production default

| Library | Primary use | Verdict |
|---------|-------------|---------|
| **Google Tink (`tink`)** | Misuse-resistant high-level API for AEAD, MAC, signing, hybrid encryption | **Default for new production code 2026** — opinionated, hard-to-misuse, KMS-integrated |
| **BouncyCastle (`bcprov-jdk18on`)** | Algorithm coverage breadth, FIPS via `bc-fips`, post-quantum support | When Tink lacks an algorithm (e.g. ML-KEM today, niche curves, legacy interop) |
| **JCA / JCE built-in** | Plain JDK; available everywhere | Acceptable but error-prone — provider selection, padding choices, IV handling all caller-managed |
| **kotlinx-cryptography-core (whyoleg)** | KMP-friendly modern crypto wrapping JCA / OpenSSL / WebCrypto | KMP server code targeting JVM + JS + Native; **experimental** as of 2026-05 |
| **bc-kotlin** | Kotlin DSL over BouncyCastle | Acceptable BC wrapper; not widely adopted |
| **KmpCrypto (skolson)** | KMP BouncyCastle bundle | Niche; consider only for legacy BC patterns in KMP |

**Tink advantages**:
- AEAD interface forbids reuse-prone APIs (no exposed nonce parameter — Tink manages internally).
- Key rotation built in via `KeysetHandle` (multi-key sets, lookup by key ID embedded in ciphertext).
- KMS integration (AWS KMS, GCP KMS, Vault) is first-class — encrypted KeysetHandle.
- FIPS-compliant builds via `tink-bcfips`.

**When Tink is the wrong choice**:
- You need an algorithm Tink doesn't ship (ML-KEM as of 2026-05; obscure GOST variants).
- You're maintaining legacy code that already uses BC patterns — don't dual-import.
- You need fine control over nonce / IV management for protocol-compliance reasons.

```kotlin
// Tink: AEAD basics
import com.google.crypto.tink.*
import com.google.crypto.tink.aead.AeadConfig

AeadConfig.register()                                     // one-time init

// Generate or load keyset
val handle: KeysetHandle = KeysetHandle.generateNew(KeyTemplates.get("AES256_GCM"))
val aead: Aead = handle.getPrimitive(Aead::class.java)

val ciphertext: ByteArray = aead.encrypt(plaintext, associatedData)
val decrypted:  ByteArray = aead.decrypt(ciphertext, associatedData)

// Persist keyset — REJECT raw cleartext storage
val outputStream = JsonKeysetWriter.withOutputStream(file)
handle.write(outputStream, kmsAead)                       // wrap with KMS
```

Reference: [`builder/reference/kotlin-best-practices.md` §10.7 Crypto](../../builder/reference/kotlin-best-practices.md#107-crypto).

---

## 2. Symmetric encryption — AES-GCM and ChaCha20-Poly1305

| Need | Tink template | Notes |
|------|---------------|-------|
| AES-GCM 128 | `AES128_GCM` | Hardware-accelerated on AES-NI x86 / ARM |
| AES-GCM 256 | `AES256_GCM` | Default for 256-bit security level |
| ChaCha20-Poly1305 | `CHACHA20_POLY1305` | Faster on platforms without AES-NI |
| XChaCha20-Poly1305 (extended 192-bit nonce) | `XCHACHA20_POLY1305` | Use when nonces are random and you need collision-safe margin |
| AES-GCM-SIV (nonce-misuse-resistant) | `AES256_GCM_SIV` | Use when callers may reuse nonces |

**Tink manages nonces internally** — you don't see them in the API. The ciphertext layout is `key_id (4 bytes) || nonce || ct || tag`.

**If you must use raw JCA** (legacy / non-Tink stack):

```kotlin
import javax.crypto.Cipher
import javax.crypto.spec.GCMParameterSpec
import javax.crypto.spec.SecretKeySpec

// CORRECT: 12-byte random nonce, 16-byte tag, AAD bound
val nonce = ByteArray(12).also { SecureRandom().nextBytes(it) }
val cipher = Cipher.getInstance("AES/GCM/NoPadding")
cipher.init(Cipher.ENCRYPT_MODE, SecretKeySpec(keyBytes, "AES"), GCMParameterSpec(128, nonce))
cipher.updateAAD(aad)
val ct = cipher.doFinal(plaintext)
// Wire format: nonce || ct (tag is appended to ct by JCA)
```

| Audit | What |
|-------|------|
| `Cipher.getInstance("AES")` (no mode/padding) | **Reject** — defaults to `AES/ECB/PKCS5Padding` on most JDKs. ECB is broken. |
| `Cipher.getInstance("AES/CBC/PKCS5Padding")` | Reject for new code (POODLE / Lucky13 padding oracle history). Use AES-GCM. |
| `IvParameterSpec` with constant or counter-from-Date IV | Reject — predictable IV |
| AES-GCM with nonce reused across encryptions of the same key | Catastrophic; see §3 |
| Cipher instance shared across threads without external sync | `Cipher` is NOT thread-safe; use ThreadLocal or new instance per call |

---

## 3. Nonce uniqueness — the cardinal rule

For AES-GCM with a fixed key, **never reuse a nonce**. Single reuse → leaks XOR of plaintexts and can leak the authentication subkey.

| Strategy | Verdict |
|----------|---------|
| Random 96-bit nonce (`SecureRandom.nextBytes(ByteArray(12))`) | Safe up to ~2^32 encryptions per key (birthday bound) |
| Counter-based, persisted across restarts | Safe IF the counter survives crash / restart |
| Counter that resets on restart | **UNSAFE** — reuses nonces |
| Tink-managed (don't see the nonce) | Safe — Tink uses random nonces or key-rotation prevents reuse via `KeysetHandle` |
| `AES-GCM-SIV` (Tink template `AES256_GCM_SIV`) | Nonce-misuse-resistant; safe even on accidental reuse |
| `XChaCha20-Poly1305` (192-bit nonce) | Random nonces become collision-safe; use for stateless multi-writer scenarios |

**Architectural rule**: multi-instance servers sharing one AES-GCM key must partition the nonce space per instance (e.g. prefix nonce with instance ID) OR use random 96-bit nonces with key rotation before 2^32 encryptions OR switch to AES-GCM-SIV.

---

## 4. Asymmetric — signing and key agreement

| Use | Tink template | Library / class |
|-----|---------------|------------------|
| Ed25519 signing | `ED25519` | Tink `SignatureFactory` or BC `Ed25519PrivateKeyParameters` |
| ECDSA P-256 | `ECDSA_P256` | Tink (deterministic via RFC 6979 by default) |
| ECDSA P-384 / P-521 | `ECDSA_P384`, `ECDSA_P521` | Tink |
| RSA-PSS (≥3072) | `RSA_SSA_PSS_3072_SHA256_F4` | Tink |
| X25519 key agreement | Tink `HybridEncryptFactory` (encapsulates KA + AEAD) | Tink |
| ECDH P-256 | `ECIES_P256_HKDF_HMAC_SHA256_AES128_GCM` | Tink hybrid |

**Hybrid encryption** (Tink's recommended replacement for raw ECDH):

```kotlin
import com.google.crypto.tink.hybrid.HybridConfig

HybridConfig.register()
val privHandle = KeysetHandle.generateNew(KeyTemplates.get("ECIES_P256_HKDF_HMAC_SHA256_AES128_GCM"))
val pubHandle  = privHandle.publicKeysetHandle

val enc: HybridEncrypt = pubHandle.getPrimitive(HybridEncrypt::class.java)
val dec: HybridDecrypt = privHandle.getPrimitive(HybridDecrypt::class.java)

val ciphertext = enc.encrypt(plaintext, contextInfo)
val recovered  = dec.decrypt(ciphertext, contextInfo)
```

| Avoid | Why |
|-------|-----|
| Raw RSA encryption for payload (`RSA/ECB/PKCS1Padding`) | Bleichenbacher attack; use OAEP, and prefer hybrid (encrypt-AEAD-key-with-RSA-OAEP) |
| `RSA/ECB/OAEPWithSHA-1AndMGF1Padding` | SHA-1 in MGF1 weakens; use `OAEPWithSHA-256AndMGF1Padding` |
| RSA-PKCS1v15 signing for new code | Use RSA-PSS (`RSASSA-PSS`) |
| ECDSA without deterministic nonce on a weak RNG | Tink uses deterministic; BC's default does not unless you wire `Ed25519PrivateKeyParameters` or RFC-6979 ECDSA |
| Curves beyond Tink's defaults (secp256k1, brainpool*) | Use BouncyCastle directly; document interop requirement |

---

## 5. Password hashing — Argon2id is the 2026 default

JDK has no built-in Argon2. Options:

| Library | Verdict |
|---------|---------|
| `argon2-jvm` (phxql/argon2-jvm) | JNI wrapper around libargon2 — fast, OWASP-recommended |
| `password4j` | Pure JVM, multi-algo (Argon2 / bcrypt / scrypt / PBKDF2) with one API |
| `de.mkammerer:argon2-jvm` | Common dependency in Spring Boot stacks |
| `bcprov-jdk18on` (BouncyCastle) | Argon2 support; lower-level API |
| `springframework.security.crypto.argon2.Argon2PasswordEncoder` (Spring Security 5.3+) | Acceptable in Spring; wraps BC |

```kotlin
import com.password4j.Password
import com.password4j.types.Argon2

// 2026 OWASP-aligned defaults
val argon2 = Argon2Function.getInstance(
    47104,    // memory (KiB) ~ 46 MiB
    1,        // iterations (t_cost)
    1,        // parallelism (p_cost)
    32,       // output length (bytes)
    Argon2.ID // Argon2id
)
val hash = Password.hash(password).addRandomSalt(16).with(argon2).result   // PHC-format string
val ok   = Password.check(candidate, hash).with(argon2)
```

**Migration from bcrypt / PBKDF2** ([password-hashing.md](./password-hashing.md) for the deep dive):

Use a multi-algorithm verifier on login that detects the stored hash's algorithm prefix:

```kotlin
when {
    hash.startsWith("\$argon2id\$") -> Password.check(pw, hash).with(argon2)
    hash.startsWith("\$2a\$") || hash.startsWith("\$2b\$") || hash.startsWith("\$2y\$") ->
        Password.check(pw, hash).withBcrypt()
    hash.startsWith("\$pbkdf2-") -> Password.check(pw, hash).withPBKDF2()
    else -> throw IllegalStateException("Unknown hash algorithm")
}
// On match, opportunistically re-hash under Argon2id and write back
```

Spring Security's `DelegatingPasswordEncoder` provides this pattern out-of-the-box.

---

## 6. KMS integration — envelope encryption

Kotlin / JVM SDKs for the main KMS providers:

| KMS | SDK |
|-----|-----|
| AWS KMS | `software.amazon.awssdk:kms` (v2) — sync or async (`KmsAsyncClient`) |
| GCP Cloud KMS | `com.google.cloud:google-cloud-kms` |
| Azure Key Vault | `com.azure:azure-security-keyvault-keys`, `-secrets`, `-certificates` |
| HashiCorp Vault | `vault-java-driver` (BetterCloud) or `spring-cloud-starter-vault-config` |
| Tink integration | `tink-awskms`, `tink-gcpkms`, `tink-hcvault` — wraps each KMS as a Tink AEAD primitive |

**Envelope encryption pattern** (the only pattern that scales):

```text
1. Generate a Data Encryption Key (DEK) locally: 32 random bytes via SecureRandom.
2. Encrypt payload with DEK using AES-GCM (or Tink AEAD).
3. Send DEK to KMS for encryption under a Customer Master Key (CMK).
   → Receive encrypted DEK (EDEK).
4. Store: { EDEK, AEAD ciphertext, AEAD nonce }. Zero out plaintext DEK in memory.
5. Decrypt: send EDEK to KMS, receive plaintext DEK, decrypt payload, zero DEK.
```

**Tink + AWS KMS** (recommended pattern):

```kotlin
import com.google.crypto.tink.integration.awskms.AwsKmsClient
import com.google.crypto.tink.aead.AeadConfig

AeadConfig.register()
AwsKmsClient.register(Optional.of("aws-kms://arn:aws:kms:region:acct:key/cmk-id"), Optional.empty())

// EnvelopeAead: Tink does envelope encryption automatically
val kmsAead = AwsKmsClient.getAeadByKeyUri("aws-kms://arn:aws:kms:region:acct:key/cmk-id")
val handle  = KeysetHandle.generateNew(KeyTemplates.get("AES256_GCM"))
val aead    = KmsEnvelopeAead.create(KeyTemplates.get("AES256_GCM"), kmsAead)

val ciphertext: ByteArray = aead.encrypt(plaintext, associatedData)
// Single call: locally encrypt with DEK + KMS-encrypt DEK; ciphertext contains EDEK
```

**Key rotation**: re-encrypt only the EDEK via KMS (cheap), keep payload ciphertext intact. Rotate CMK every 90d or on incident.

Crypt cross-reference: [`kms-integration.md`](./kms-integration.md) for the deep dive.

---

## 7. TLS — OkHttp / Ktor client / Java HTTP Client

OkHttp uses the **platform default TLS engine** (JDK's `SSLContext`/`SSLSocketFactory`), not a Rust-style embedded rustls. For pinning:

```kotlin
import okhttp3.CertificatePinner
import okhttp3.OkHttpClient

val pinner = CertificatePinner.Builder()
    .add("api.example.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
    .add("api.example.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=")    // backup
    .build()
val client = OkHttpClient.Builder().certificatePinner(pinner).build()
```

| Audit | What |
|-------|------|
| Pin **SPKI hash** (`sha256/`) not cert serial | Cert rotation without SPKI rotation is the norm |
| Maintain ≥2 backup pins | One for current, one for next rotation |
| Have a kill-switch (remote config) | Pinning gone wrong has bricked apps |
| `HostnameVerifier` returning `true` unconditionally | **Reject** — disables hostname verification |
| `X509TrustManager.checkServerTrusted` returning without check | **Reject** — disables cert validation |
| `SSLContext.getInstance("SSL")` / `TLS` (no version) | Use `SSLContext.getInstance("TLSv1.3")` |
| JCA system property `jdk.tls.client.protocols=TLSv1.3` | Enforce at JVM startup |

Ktor client wraps the same `CertificatePinner` via `HttpClient(OkHttp) { engine { config { certificatePinner(pinner) } } }`.

---

## 8. Constant-time comparison

JDK and Kotlin stdlib do not provide a dedicated constant-time helper, but **`MessageDigest.isEqual(a, b)` has been constant-time since JDK 6u17 / 7** — use it. Alternatives: BC `org.bouncycastle.util.Arrays.constantTimeAreEqual`, Tink `com.google.crypto.tink.subtle.Bytes.equal`.

```kotlin
import java.security.MessageDigest
val ok: Boolean = MessageDigest.isEqual(userToken, storedToken)
```

Length leak: a `size != size` early-return reveals length. For variable-length secret comparisons, pad to fixed length first or accept that length is non-secret. Apply to auth tokens, MAC outputs, signature bytes, and any derived secret-like value (never re-compare password hashes manually — use the library `verify`).

---

## 9. Secret material lifecycle — Kotlin / JVM specifics

JVM-side secret hygiene is harder than Rust's because `String` is immutable (can't zero the backing `char[]`), the JIT may move objects (stale copies), and GC compaction copies live objects into fresh pages (secrets persist in freed memory). No Kotlin/JVM equivalent of Rust's `secrecy` crate prevents `toString`/`equals`/serialization leakage at the type level — discipline + Detekt + code review are the substitutes.

| Pattern | Verdict |
|---------|---------|
| `String password` from `HttpRequest.getParameter` | Accept reality; design around it via short-lived tokens |
| `CharArray password` zeroed after use | Preferred — APIs like `PBEKeySpec(password: CharArray, ...)` expect this |
| `ByteArray` for secret bytes, zero via `Arrays.fill(buf, 0)` | Best you can do on JVM; not memory-safe (GC may have copied) |
| `java.lang.ref.Cleaner` registering zero-on-collect | Acceptable defense in depth |
| Secret in `data class` | `equals`/`hashCode`/`toString` auto-derived leak secret; reject |
| `@JvmField val secret: String` | Java reflection reads directly; reject |
| `logger.info { "$secret" }` (kotlin-logging lambda form) | Reject — lambda still evaluates when level enabled |

Wrapper pattern: a class with `private val buffer: ByteArray`, an `inline fun <R> use(block: (ByteArray) -> R): R`, an explicit `close()` that runs `java.util.Arrays.fill(buffer, 0)`, and a `Cleaner.create()`-registered fallback that re-runs the same fill at GC time. Override `toString()` to return `"SecretBytes(<redacted ${buffer.size} bytes>)"`.

---

## 10. JWT — algorithm allowlist mandatory

Three main JVM JWT libraries:

| Library | Pros | Cons |
|---------|------|------|
| **`io.jsonwebtoken:jjwt`** | Mature, popular, sane defaults; throws on `none` by default since 0.11 | Verify version locks `none` out |
| **`com.nimbusds:nimbus-jose-jwt`** | Most spec-complete (JWS + JWE + JWK + JOSE) | Larger surface |
| **`kotlinx-jwt`** (kotlin-multiplatform) | KMP-friendly | Less mature than the JVM-only options |
| `auth0/java-jwt` | OK | Less feature than nimbus |

```kotlin
import io.jsonwebtoken.Jwts
import io.jsonwebtoken.security.Keys

// Hardened parser
val parser = Jwts.parser()
    .verifyWith(Keys.hmacShaKeyFor(secretBytes))     // bind to one key
    .requireIssuer("https://my-issuer.example")
    .requireAudience("my-service")
    .clockSkewSeconds(60)
    .build()

val jws = parser.parseSignedClaims(jwt)               // throws on alg mismatch / exp / sig fail
```

**Critical rules** (same baseline as Rust / Swift):

1. **Always set an explicit algorithm allowlist.** `Jwts.parser()` with `verifyWith(specificKey)` constrains alg implicitly; double-check the library version's default behavior. Reject tokens whose `alg` header doesn't match the key type.
2. **Reject `alg: none` unconditionally.** All modern jjwt versions do; nimbus-jose-jwt requires explicit configuration — verify.
3. **Reject `alg: HS*` when verifier is RS / ES** (algorithm confusion class — attacker uses public key as HMAC key).
4. **Validate `iss`, `aud`, `exp`, `nbf`.**
5. **`kid`-driven JWKS lookup**: allowlist `kid` values; never let the token's `kid` cause an unbounded HTTP fetch.

---

## 11. Post-quantum (2026 status — JVM ecosystem)

NIST finalized FIPS 203 / 204 / 205. JVM availability is **stronger than Swift, weaker than current Rust**:

| Algorithm | Standard | JVM availability (2026-05) |
|-----------|----------|----------------------------|
| ML-KEM (Kyber) | FIPS 203 | **BouncyCastle 1.78+** ships `MLKEMKeyGenerator`, `MLKEMKEMGenerator` |
| ML-DSA (Dilithium) | FIPS 204 | BouncyCastle 1.78+ ships `MLDSAKeyGenerator`, `MLDSASigner` |
| SLH-DSA (SPHINCS+) | FIPS 205 | BouncyCastle 1.78+ ships `SLHDSAKeyGenerator` |
| TLS hybrid X25519-MLKEM768 | Drafts | Depends on TLS engine; OpenJDK 21+ TLS doesn't ship hybrid yet (2026-05); BC TLS implementation has it |
| Tink PQ support | — | **Not yet** in Tink stable; experimental branch only |

**Migration strategy for JVM services (2026-05)**:

1. **TLS**: depends on the load balancer / front proxy. Most production TLS termination is at the LB (NGINX / Envoy / AWS ALB) — track their PQ adoption rather than JVM client TLS.
2. **Long-term sealed archives**: today, use BouncyCastle `MLKEMKEMGenerator` to wrap an AES-GCM key. Pure-JVM, pure-PQ for the wrap step.
3. **Hybrid signatures**: BC provides ML-DSA; pair with Ed25519 signature in dual-format until verifiers catch up.
4. **Short-lived tokens** (session JWT, OAuth): classical (Ed25519, ES256) remains acceptable through 2030.

```kotlin
import org.bouncycastle.pqc.crypto.crystals.kyber.*

val params = MLKEMParameters.ml_kem_768
val keygen = MLKEMKeyPairGenerator().apply { init(MLKEMKeyGenerationParameters(SecureRandom(), params)) }
val keypair = keygen.generateKeyPair()
// Use keypair.public for encapsulation; keypair.private for decapsulation
```

Crypt cross-reference: [`post-quantum-migration.md`](./post-quantum-migration.md) for the timeline matrix.

---

## 12. Multiplatform crypto — KMP considerations

For Kotlin Multiplatform server code targeting JVM + Native + JS:

| Library | KMP targets | Verdict |
|---------|-------------|---------|
| **`kotlinx-cryptography-core` (whyoleg)** | JVM (JCA), JS (WebCrypto), Native (OpenSSL) | **Experimental** as of 2026-05; promising but not yet production-stable |
| `KmpCrypto` (skolson) | KMP via BC | Niche |
| `expect`/`actual` pattern with platform-native APIs | All targets | Most control; most code |

**`expect`/`actual` pattern**: declare `expect class Aead { fun encrypt(...); fun decrypt(...) }` in `commonMain`; supply `actual class Aead` in each target — Tink on `jvmMain`, libsodium via `cinterop` on `nativeMain`, WebCrypto via kotlinx-cryptography on `jsMain`.

**Audit**: every `expect` / `actual` pair must produce **bit-identical** output for the same input, OR the wire format must include a version/platform tag so consumers can route to the matching decryptor.

---

## 13. Randomness — `SecureRandom`

| API | Verdict |
|-----|---------|
| `java.security.SecureRandom()` (default) | **CSPRNG**, OS-backed (`/dev/urandom` on Linux, CryptGenRandom on Windows). Acceptable. |
| `SecureRandom.getInstanceStrong()` | Uses entropy-blocking source (`/dev/random`); can stall startup — use only when blocking is acceptable |
| `SecureRandom.getInstance("NativePRNG")` | Linux-specific OS provider |
| `SecureRandom.getInstance("SHA1PRNG")` | **Deprecated alias** — implementations vary by JDK; on some, this was seedable-determistic; reject |
| `Random()` / `kotlin.random.Random` | **Not CSPRNG** — Mersenne Twister; reject for crypto |
| `ThreadLocalRandom` | **Not CSPRNG** — reject for crypto |
| `UUID.randomUUID()` for high-entropy secret | UUID v4 is CSPRNG via SecureRandom, but only 122 bits; OK for IDs, not for 256-bit keys |
| `System.currentTimeMillis()` as nonce | **Reject categorically** |

```kotlin
import java.security.SecureRandom

private val rng = SecureRandom()    // safe to share across threads; instance is thread-safe per spec

val key = ByteArray(32).also { rng.nextBytes(it) }
val nonce = ByteArray(12).also { rng.nextBytes(it) }
```

---

## 14. Common pitfalls — Kotlin-specific design errors

| Pitfall | Why it's wrong |
|---------|----------------|
| **`Cipher.getInstance("AES")`** (no mode/padding) | JDK default = `AES/ECB/PKCS5Padding`; ECB is broken |
| **`Cipher.getInstance("AES/CBC/PKCS5Padding")`** for new code | Padding-oracle history (POODLE, Lucky13); use AES-GCM |
| **Shared `Cipher` instance across threads** | `Cipher` is NOT thread-safe; use ThreadLocal or per-call |
| **Storing `KeysetHandle` cleartext** | Defeats Tink's KMS integration; always wrap with `kmsAead.write(...)` |
| **Reusing nonce across encrypts of same key** | Catastrophic for AES-GCM |
| **`SecureRandom.getInstance("SHA1PRNG")`** | Implementation-defined behavior across JDKs; reject |
| **Bcrypt cost factor 10** in 2026 | Below current OWASP minimum; rotate to ≥12 or migrate to Argon2id |
| **Logging `SecretKey.encoded`** | The raw key bytes; reject |
| **Spring `@ConfigurationProperties` exposing decoded secrets via `toString()`** | Spring Boot Actuator `/configprops` endpoint can leak; mark fields with `@JsonIgnore` and override `toString` |
| **JCA provider order ("BC" first vs JDK first)** | BC and JDK behave differently for the same algorithm name; pin the provider explicitly: `Cipher.getInstance("AES/GCM/NoPadding", "BC")` |
| **`KeyStore` cleartext file** | The default `JKS` / `PKCS12` keystore is password-protected but the password is often the same constant in code; rotate and externalize |
| **`SSLContext.init(null, trustAll, null)`** | Disables verification; reject |
| **HMAC verify via recomputed-then-`equals` instead of `Mac.equals` constant-time** | Timing oracle |

---

## 15. Crypto stack policy summary (2026 defaults)

| Concern | Default |
|---------|---------|
| Symmetric AEAD | Tink `AES256_GCM` or `XCHACHA20_POLY1305`; BC if Tink unsuitable |
| Asymmetric signing | Tink `ED25519`; `ECDSA_P256` for PKI interop |
| Key agreement | Tink Hybrid (`ECIES_P256_HKDF_HMAC_SHA256_AES128_GCM`) wraps ECDH + AEAD |
| Hashing | `SHA-256` / `SHA-384`; BLAKE3 via `blake3-jvm` if perf-critical |
| Password hashing | Argon2id via `password4j` or `argon2-jvm` |
| KDF | Tink KDF or `Mac` HMAC + manual HKDF construction; BC `HKDFBytesGenerator` |
| RNG | `java.security.SecureRandom()` |
| TLS | OkHttp / Ktor client with `CertificatePinner`; JCA `TLSv1.3` minimum |
| Hardware key store | (Android-specific — defer to `native` skill) |
| Server-side KMS | AWS/GCP/Azure SDK + Tink envelope encryption |
| JWT | `io.jsonwebtoken:jjwt`; algorithm allowlist mandatory |
| PQ | BouncyCastle for ML-KEM / ML-DSA today; Tink PQ TBD |

---

## Triage priorities

When multiple findings stack, rank by:

1. **Hand-rolled crypto primitives** — categorical reject; route to Tink / BouncyCastle.
2. **`Cipher.getInstance("AES")` defaulting to ECB** — instant break.
3. **JWT algorithm confusion** (`alg: none`, RS↔HS, kid-controlled JWKS) — directly exploitable.
4. **AES-GCM nonce reuse risk** (counter resets, multi-instance shared key without partition) — single instance leaks key material.
5. **Predictable IV / nonce** (`System.currentTimeMillis`, `Random()`) — protocol break.
6. **`==` / `Arrays.equals` on tokens/HMACs instead of `MessageDigest.isEqual`** — timing oracle.
7. **`SecureRandom.getInstance("SHA1PRNG")`** — implementation-defined cross-JDK; reject for crypto.
8. **Untrusted `KeyStore` from cleartext file with hard-coded password** — credential leak.
9. **Disabled hostname verification or TrustManager** — MitM trivial.
10. **Weak password hashing** (bcrypt cost <12, PBKDF2 <600k iterations 2026 baseline, plain SHA-256) — migrate to Argon2id.
11. **Storing `KeysetHandle` cleartext to disk** — defeats Tink's KMS integration.
12. **No PQ posture for >10-year-archive** — plan migration using BouncyCastle ML-KEM today.

---

## Sources

- Google Tink (Java): https://github.com/tink-crypto/tink-java
- Tink primitives overview: https://developers.google.com/tink/primitives-by-language
- BouncyCastle Java releases: https://www.bouncycastle.org/releasenotes.html
- BouncyCastle PQ algorithms: https://www.bouncycastle.org/documentation/specification_interoperability/
- OkHttp `CertificatePinner`: https://square.github.io/okhttp/features/https/
- `io.jsonwebtoken:jjwt`: https://github.com/jwtk/jjwt
- `com.nimbusds:nimbus-jose-jwt`: https://connect2id.com/products/nimbus-jose-jwt
- `password4j`: https://password4j.com/
- `argon2-jvm` (phxql): https://github.com/phxql/argon2-jvm
- Spring Security crypto: https://docs.spring.io/spring-security/reference/features/integrations/cryptography.html
- `kotlinx-cryptography-core` (whyoleg): https://github.com/whyoleg/cryptography-kotlin
- NIST FIPS 203 / 204 / 205: https://csrc.nist.gov/Projects/post-quantum-cryptography
- OWASP Password Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- OWASP Cryptographic Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
