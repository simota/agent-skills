# Crypt Design Patterns

## Symmetric Encryption Patterns

### AES-256-GCM (Recommended Default)

```typescript
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

function encrypt(plaintext: string, key: Buffer): { ciphertext: Buffer; iv: Buffer; tag: Buffer } {
  const iv = randomBytes(12); // 96-bit IV for GCM
  const cipher = createCipheriv('aes-256-gcm', key, iv);
  const ciphertext = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return { ciphertext, iv, tag };
}

function decrypt(ciphertext: Buffer, key: Buffer, iv: Buffer, tag: Buffer): string {
  const decipher = createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(tag);
  return decipher.update(ciphertext) + decipher.final('utf8');
}
```

**Key rules:**
- Always generate a fresh random IV per encryption
- Store IV alongside ciphertext (IV is not secret)
- Store auth tag alongside ciphertext
- Never reuse (key, IV) pair

### Envelope Encryption (KMS Pattern)

```
1. Generate DEK (Data Encryption Key) locally
2. Encrypt data with DEK (AES-256-GCM)
3. Encrypt DEK with KEK (Key Encryption Key from KMS)
4. Store: encrypted_data + encrypted_DEK + IV + tag
5. Decrypt: KMS decrypts DEK → DEK decrypts data
```

**Benefits:** Key rotation only re-encrypts DEK, not all data

## Password Hashing Patterns

### Argon2id (Recommended)

```typescript
import argon2 from 'argon2';

// Hash
const hash = await argon2.hash(password, {
  type: argon2.argon2id,
  memoryCost: 65536,  // 64 MB
  timeCost: 3,        // 3 iterations
  parallelism: 4,     // 4 threads
});

// Verify
const valid = await argon2.verify(hash, password);
```

### Parameter Tuning Guide

| Environment | Memory | Time | Parallelism |
|-------------|--------|------|-------------|
| Web app (< 1s) | 64 MB | 3 | 4 |
| High-security | 256 MB | 4 | 8 |
| Resource-constrained | 32 MB | 4 | 2 |

**Rule:** Target 0.5-1.0 seconds per hash on your production hardware.

## JWT/JWS Patterns

### Secure JWT Configuration

```typescript
// Signing (Ed25519 recommended)
const token = jwt.sign(payload, privateKey, {
  algorithm: 'EdDSA',
  expiresIn: '15m',     // Short-lived access tokens
  issuer: 'your-app',
  audience: 'your-api',
});

// Verification (always validate)
const verified = jwt.verify(token, publicKey, {
  algorithms: ['EdDSA'],  // Whitelist allowed algorithms
  issuer: 'your-app',
  audience: 'your-api',
});
```

### Token Architecture

```
Access Token: Short-lived (15 min), signed JWT
  → Contains: user_id, tenant_id, roles, permissions
  → Storage: Memory only (never localStorage)

Refresh Token: Long-lived (7 days), opaque string
  → Contains: Reference to session (not claims)
  → Storage: httpOnly, secure, sameSite cookie
  → Server-side: Stored in DB with revocation support
```

## TLS Configuration Patterns

### Modern TLS (2024+ Recommended)

```nginx
ssl_protocols TLSv1.3 TLSv1.2;
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers on;
ssl_session_timeout 1d;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;

# HSTS
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
```

## Key Rotation Patterns

### Rotation with Grace Period

```
Phase 1: Generate new key (key_v2)
Phase 2: Sign with key_v2, verify with key_v1 AND key_v2
Phase 3: Grace period (overlap duration depends on token lifetime)
Phase 4: Remove key_v1 from verification set
Phase 5: Archive key_v1 for audit

Timeline:
  ──────┬────────────┬────────────┬──────
        │ key_v1     │  overlap   │ key_v2 only
        │ only       │  period    │
```

### KMS Key Rotation

```
Automatic rotation:
  - AWS KMS: Enable automatic rotation (every 365 days)
  - GCP KMS: Set rotation schedule
  - Azure Key Vault: Configure rotation policy

Manual rotation:
  1. Create new key version in KMS
  2. Update application to encrypt with new version
  3. Re-encrypt data encryption keys (not data) with new version
  4. Disable old key version after grace period
  5. Schedule old key version deletion (30-90 day delay)
```

## E2EE Pattern (Simplified)

```
Sender                              Receiver
  │                                    │
  │  1. Generate ephemeral key pair    │
  │  2. Derive shared secret (X25519) │
  │  3. Derive message key (HKDF)     │
  │  4. Encrypt message (AES-GCM)     │
  │                                    │
  │  ──── encrypted message ────────→  │
  │  ──── ephemeral public key ─────→  │
  │                                    │
  │     5. Derive shared secret        │
  │     6. Derive message key          │
  │     7. Decrypt message             │
```

## Anti-Pattern Detection Checklist

| # | Anti-Pattern | Detection method | Severity |
|---|-------------|-----------------|----------|
| 1 | ECB mode | grep `aes-.*-ecb` or `ECB` | Critical |
| 2 | Fixed IV/nonce | Check IV generation (not hardcoded) | Critical |
| 3 | `Math.random()` for crypto | grep `Math.random` in crypto context | Critical |
| 4 | Keys in source | grep for base64/hex key patterns | Critical |
| 5 | MD5/SHA-1 for security | grep `createHash('md5'\|'sha1')` | High |
| 6 | No key rotation | Check for rotation mechanism | High |
| 7 | PKCS#1 v1.5 padding | grep `RSA_PKCS1_PADDING` | High |
| 8 | `alg: none` in JWT | Check JWT verification config | Critical |
| 9 | Unauthenticated encryption | AES-CBC without HMAC | High |
| 10 | Timing-vulnerable comparison | Using `===` for hash comparison | Medium |

## Library Recommendations

| Language | Library | Use case |
|----------|---------|----------|
| Node.js | `crypto` (built-in) | General crypto |
| Node.js | `jose` | JWT/JWE/JWS |
| Node.js | `argon2` | Password hashing |
| Python | `cryptography` | General crypto |
| Python | `PyJWT` + `cryptography` | JWT |
| Python | `argon2-cffi` | Password hashing |
| Go | `crypto/*` (stdlib) | General crypto |
| Rust | `ring` or `rustcrypto` | General crypto |
| Java | Tink (Google) | General crypto |
| Browser | `SubtleCrypto` (Web Crypto API) | Client-side crypto |


---

## Per-Recipe Behavior Notes (SKILL.md excerpt)

- `algorithm`: Use-case-specific algorithm recommendations (symmetric, asymmetric, hash, KDF). Run anti-pattern checklist. Includes quantum-resistance assessment. Flags quantum-vulnerable choices but does not own the migration program — route to `pqc` for that.
- `key`: General key-management strategy — key hierarchy, rotation policy, key ceremony, derivation chains, revocation, destruction. Policy layer above `kms`; defines the lifecycle that `kms` then wires to a specific service.
- `e2ee`: Signal Protocol / MLS / custom E2EE architecture design. Includes key exchange flow, forward secrecy, and PFS design.
- `tls`: TLS 1.3 configuration, cipher suite priority, mTLS mutual authentication. Applies PQC hybrid KEX (X25519MLKEM768) selected by `pqc` — does not own the transition decision itself.
- `signature`: Ed25519 / ECDSA / ML-DSA signature scheme design. Includes JWT verification flow, algorithm pinning, and timing-safe comparison.
- `password`: Password-hashing scheme design. Default Argon2id with OWASP 2024 parameters (m=19 MiB, t=2, p=1 minimum; preferred m=64–128 MiB, t=3, p=1); bcrypt cost ≥ 12 for legacy compatibility; scrypt or PBKDF2-HMAC-SHA-256 (≥ 600k iterations) where Argon2id unavailable. Require per-password salt (≥ 16 bytes, CSPRNG) plus server-wide pepper held in KMS. Specify bcrypt → Argon2id migration via rehash-on-next-login and Argon2id `needs_rehash` on parameter bump. Align with NIST SP 800-63B memorized-secret verifier. Sentinel `authn` reviews the implementing code against this design; Crypt does not audit code. Cross-link: Sentinel `authn` (implementation audit), Canon[regulatory] (NIST SP 800-63B / PCI-DSS 4.0 §8.3.6).
- `kms`: KMS-service integration pattern. Provider selection (AWS KMS / GCP KMS / Azure Key Vault / HashiCorp Vault Transit), envelope encryption (CMK wraps DEK, DEK encrypts payload with AES-256-GCM + random 96-bit IV), encryption-context / AAD binding, data-key cache policy (max 10 GB or 2^32 messages per DEK, ≤ 10-minute TTL), KMS-managed automatic CMK rotation, alias-based lookup. HSM-backed CMK (CloudHSM / Cloud HSM / Managed HSM) only where FIPS 140-3 Level 3, CNSA 2.0, or tenant-isolated HSM is mandated. IAM split (encrypt-only, decrypt-only, admin break-glass) and CloudTrail `Decrypt` audit alerting. Cross-link: `key` (policy layer; runs first), Gear `secret` (application-level secrets store — e.g., Vault KV for DB passwords vs Vault Transit for crypto operations; overlap is intentional), Scaffold (provisions the CMK via IaC).
- `pqc`: Post-quantum migration plan against the launch-now-decrypt-later threat. Inventory every RSA / DH / ECDH / ECDSA / Ed25519 use; classify by HNDL sensitivity and deadline regime (NIST IR 8547 draft: deprecate by 2030, disallow by 2035; NSA CNSA 2.0: new NSS quantum-safe by Jan 2027, applications by 2030, infrastructure by 2035). Target NIST standards: FIPS 203 ML-KEM for key encapsulation, FIPS 204 ML-DSA for general signatures, FIPS 205 SLH-DSA for conservative hash-based signatures (non-CNSA). Use hybrid schemes during transition — X25519MLKEM768 (IANA `0x11EC`) for TLS 1.3 KEX, composite-sig for X.509. Chrome shipped X25519MLKEM768 as the default TLS 1.3 KEX in v131 (Nov 2024); since v138 users can no longer disable it, and the `PostQuantumKeyAgreementEnabled` enterprise policy is slated for removal in v147 — treat hybrid PQ KEX as a baseline expectation in browser fleets. [Source: The SSL Store — Google Chrome Adds Hybrid PQC](https://www.thesslstore.com/blog/google-chrome-adds-support-for-a-hybrid-post-quantum-cryptographic-algorithm/) Stage rollout KEX → signatures → at-rest wrap keys. Symmetric AES-256 does not migrate (Grover-safe at 128-bit effective). Cross-link: `algo` (picks current algorithms; flags but does not own migration), `tls` (applies the hybrid KEX once selected here), Canon[regulatory] (CNSA 2.0 / BSI / ANSSI mandates drive the timeline).
- `mobile`: Mobile-specific key custody + auth design. **iOS Keychain**: `kSecAttrAccessControl` with `.biometryCurrentSet` (auto-invalidates on Face ID / Touch ID re-enrollment) + `kSecAttrAccessibleWhenUnlockedThisDeviceOnly` (excludes iCloud backup) for secret storage; **Secure Enclave**: generate signing keys with `kSecAttrTokenIDSecureEnclave` so private keys never leave the chip. **Android Keystore**: `setIsStrongBoxBacked(true)` for hardware-isolated keys on supported devices (Pixel / flagship), graceful fall back to TEE; use `setUserAuthenticationRequired(true)` with `setUserAuthenticationParameters(timeoutSec, AUTH_BIOMETRIC_STRONG)` for biometry-gated keys. **Passkey / WebAuthn / FIDO2 server-side**: verify attestation, store credential ID + public key + signature counter; reject sign-ins where counter does not advance (cloned authenticator). **Mobile JWT defaults (2025 standard)**: access-token lifetime 15-60 min; refresh-token lifetime 30-90 days WITH rotation (each use issues a new refresh, old is revoked); replay of an invalidated refresh triggers full session revocation. Algorithm: ES256 (P-256 + ECDSA) for signing — never `HS256` shared secret on mobile, never `alg: none`. **Certificate pinning**: pin public keys (not certificates), ≥ 2 backup pins, restrict to first-party endpoints — OWASP 2025 toned down general recommendation; reserve for high-risk apps (finance / health). **Anti-pattern**: hardcoded API keys in the binary (MASWE-0005, ~50% of mobile apps fail per Zimperium 2025) — proxy through a BFF. `Native` implements the spec; `Sentinel` `mobile` audits the result; `Probe` confirms runtime exploitability.

