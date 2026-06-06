# Crypt Examples

## Example 1: API Authentication Design

### Requirements

```yaml
type: API authentication
framework: Node.js + Hono
auth_method: JWT
compliance: standard
threat_model: Public API, internet-facing
```

### Design Specification

```markdown
## Algorithm Selection

| Component | Algorithm | Parameters |
|-----------|-----------|------------|
| Token signing | Ed25519 (EdDSA) | 256-bit key |
| Token encryption | — (signed only) | — |
| Password hashing | Argon2id | 64MB, 3 iter, 4 parallel |
| Session ID | CSPRNG | 256-bit random |

## Token Architecture

### Access Token (JWT)
- Algorithm: EdDSA (Ed25519)
- Lifetime: 15 minutes
- Claims: sub, tenant_id, roles, iat, exp, iss, aud
- Storage: Memory only (never persisted client-side)

### Refresh Token
- Format: Opaque (256-bit random, base64url)
- Lifetime: 7 days (sliding)
- Storage: httpOnly + secure + sameSite=strict cookie
- Server: Stored in DB with SHA-256 hash

## Key Management
- Key pair stored in environment variable (production: KMS)
- Key rotation: Every 90 days with 48-hour overlap
- Key ID (kid) included in JWT header for rotation support

## Anti-Pattern Checklist
- [x] No `alg: none` — algorithm whitelist enforced server-side
- [x] No symmetric secret in JWT — using asymmetric Ed25519
- [x] No token in localStorage — memory + httpOnly cookie only
- [x] No long-lived access tokens — 15 min maximum
- [x] Refresh token hashed in DB — not stored in plaintext
```

## Example 2: Data-at-Rest Encryption Design

### Requirements

```yaml
type: data-at-rest encryption
data: PII (email, phone, address)
database: PostgreSQL
compliance: GDPR
key_management: AWS KMS
```

### Design Specification

```markdown
## Strategy: Application-Level Envelope Encryption

### Architecture
1. Each PII field encrypted with a unique DEK per record
2. DEK encrypted with tenant-level KEK (AWS KMS CMK)
3. Encrypted DEK stored alongside encrypted data

### Table Design

| Column | Type | Encrypted |
|--------|------|-----------|
| id | UUID | No |
| tenant_id | UUID | No |
| email_encrypted | BYTEA | Yes (AES-256-GCM) |
| email_iv | BYTEA | No (stored alongside) |
| email_tag | BYTEA | No (stored alongside) |
| phone_encrypted | BYTEA | Yes (AES-256-GCM) |
| dek_encrypted | BYTEA | Yes (KMS envelope) |

### Key Hierarchy
```
AWS KMS CMK (root)
  └── Tenant KEK (per tenant, KMS-managed)
       └── Record DEK (per record, locally generated)
            └── Field encryption (AES-256-GCM)
```

### Key Rotation
- KMS CMK: Annual automatic rotation
- Tenant KEK: Re-wrap DEKs quarterly (no data re-encryption)
- Record DEK: New DEK on data update (old DEK archived for audit)

### Searchable Encryption
For fields that need search (e.g., email lookup):
- Store blind index: HMAC-SHA256(email, search_key) → search_index column
- Search on blind index, decrypt result to verify
- Trade-off: Exact match only, no partial search

### Quantum Readiness
- Current: AES-256-GCM (quantum-safe for symmetric)
- Future: Monitor NIST PQC for asymmetric components
- Risk: KMS key wrapping uses RSA (quantum-vulnerable)
- Plan: Migrate to hybrid classical+PQC when KMS supports ML-KEM
```

## Example 3: Crypto Audit Report

```markdown
## Cryptographic Audit: payments module

### Summary
- Files scanned: 23
- Anti-patterns found: 4 (2 critical, 2 high)
- Quantum-vulnerable components: 1

### Critical Issues

#### CRYPT-001: Fixed IV in Card Token Encryption
**Location:** `src/payments/tokenizer.ts:34`
**Issue:** IV is derived from card number hash, not random
**Risk:** Same card always produces same ciphertext → pattern leakage
**Fix:** Generate random 12-byte IV per encryption; store alongside ciphertext

#### CRYPT-002: MD5 for Webhook Signature
**Location:** `src/webhooks/verify.ts:12`
**Issue:** HMAC-MD5 used for webhook signature verification
**Risk:** MD5 collision attacks possible
**Fix:** Upgrade to HMAC-SHA256; coordinate with webhook provider

### High Issues

#### CRYPT-003: No Key Rotation Mechanism
**Location:** `config/encryption.ts`
**Issue:** Single encryption key with no version or rotation support
**Fix:** Add key versioning; implement envelope encryption with KMS

#### CRYPT-004: Timing-Vulnerable Comparison
**Location:** `src/auth/hmac.ts:28`
**Issue:** `===` used for HMAC comparison instead of constant-time compare
**Fix:** Use `crypto.timingSafeEqual()` for all secret comparisons
```
