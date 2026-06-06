# Password Hashing Reference

Purpose: Design a password-storage scheme that resists offline cracking under a realistic attacker (GPU/ASIC) and survives algorithm churn (bcrypt → Argon2id migration, peppering rotation). Crypt outputs the scheme and parameters; implementation and static review belong elsewhere.

## Scope Boundary

- **Crypt `password`**: DESIGNS the hashing scheme — algorithm, parameters, pepper strategy, migration path.
- **Sentinel `authn`**: REVIEWS existing authentication code to confirm Crypt's design is correctly applied (no `===` on hash output, no plaintext logging, no silent algorithm downgrade).
- **Gateway**: owns the login endpoint contract; does not decide hashing parameters.

If the question is "which algorithm and what parameters?" → `password`. If it is "is this login code implementing it correctly?" → Sentinel `authn`.

## Algorithm Selection

Per OWASP Password Storage Cheat Sheet (latest baseline) and NIST SP 800-63B §5.1.1.2 (memorized-secret verifier):

| Algorithm | Pick when | Parameters (2026 baseline) |
|-----------|-----------|----------------------------|
| Argon2id | Greenfield, any modern runtime with libsodium / argon2-cffi / node-argon2 | m=19 MiB, t=2, p=1 (OWASP minimum); preferred m=64–128 MiB, t=3, p=1 |
| scrypt | Memory-hard required, Argon2id unavailable | N=2^17, r=8, p=1 (OWASP) |
| bcrypt | Legacy compat, FIPS-constrained stacks | cost ≥ 12 (72-byte input cap — pre-hash with SHA-256 if longer) |
| PBKDF2-HMAC-SHA-256 | FIPS 140 strict, no alternative | ≥ 600,000 iterations (OWASP); salt ≥ 16 bytes |

Default: **Argon2id**. Every other choice needs a written reason (FIPS scope, runtime constraint, or mandated legacy compatibility).

> **Passwords are quantum-safe — for now.** Symmetric KDF strength halves under Grover's algorithm, so Argon2id-128 effective security drops to 64-bit under a CRQC. Targeting `m ≥ 64 MiB` with the parameters above leaves substantial headroom even after that halving; no PQC-specific algorithm change is required for password hashing in 2026. The PQC migration scope is asymmetric crypto (`post-quantum-migration.md`), not KDFs.

## Parameter Tuning Procedure

1. Target **≥ 0.5 s** per verification on production hardware (auth is rare; latency is cheap; brute-force cost scales linearly with this budget).
2. Benchmark on the actual verification host, not a developer laptop. GPU/ASIC attackers are 100–1000× faster than CPU.
3. Tune memory first (`m`), then time (`t`). Memory cost is the anti-GPU lever.
4. Re-benchmark yearly; adjust parameters upward as hardware improves. Store the parameter tuple inside the hash string (Argon2 encoded form, `$argon2id$v=19$m=65536,t=3,p=1$...`).

## Salt and Pepper

- **Salt**: per-password, ≥ 16 bytes from a CSPRNG, stored with the hash. Non-negotiable. Argon2/bcrypt/scrypt encoded formats include it.
- **Pepper**: one server-wide secret applied via HMAC **before** hashing (`hash(HMAC_SHA256(pepper, password))`), or as Argon2 `secret` parameter where supported.
  - Store pepper in KMS (AWS KMS / GCP KMS / Vault Transit) — never in application config.
  - Pepper protects dumped databases when the application host is not compromised. It does not substitute for a salt.
  - Rotate pepper via dual-pepper overlap: verify with old OR new, rehash on next login, retire old after tail window.

## Migration Pattern: bcrypt → Argon2id

Required when inheriting a bcrypt-cost-10 corpus. Do not mass-rehash; opportunistically upgrade on login.

```
on_login(email, password):
  row = users.find(email)
  if row.algo == "bcrypt":
      if bcrypt.verify(password, row.hash):
          new_hash = argon2id.hash(password, m=65536, t=3, p=1)
          users.update(email, algo="argon2id", hash=new_hash)
          return SUCCESS
      return FAIL
  if row.algo == "argon2id":
      if argon2id.verify(row.hash, password):
          if argon2id.needs_rehash(row.hash):  # parameters bumped
              users.update(email, hash=argon2id.hash(password, ...))
          return SUCCESS
      return FAIL
```

Constraints:
- Never log the password or the hash.
- Use constant-time verify (`argon2id.verify`, `bcrypt.checkpw`) — never `hash_a == hash_b`.
- Set a cutoff date; force password reset for accounts that never log in past the migration window.

## Anti-Patterns (flag on sight)

- MD5 / SHA-1 / unsalted SHA-256 for password storage.
- `hash == stored_hash` comparison (timing side channel — use library `verify`).
- Peppering with a secret checked into source control.
- Re-using the auth hash as a session token or API key.
- Truncating bcrypt input silently at 72 bytes (pre-hash with SHA-256 first, then base64-encode to avoid NUL-byte issues).
- Storing password alongside the hash "for debugging".
- Returning different error messages for "user not found" vs "wrong password" (user-enumeration).

## Verification Throughput and Rate Limits

Crypt specifies the hashing cost; Gateway/Sentinel own the rate-limit control plane. Flag to downstream:
- Expected verify latency (e.g., 500 ms).
- Required per-account rate limit (e.g., 10 attempts / 15 min, exponential backoff).
- Account-lockout policy (NIST SP 800-63B §5.2.2: throttle, do not lock out permanently).

## Handoff to Builder / Sentinel

Deliver:
- Algorithm + full parameter tuple (include encoded example).
- Pepper source (KMS key ARN / Vault path), rotation cadence.
- Migration SQL / ORM snippet for `algo` + `hash` columns.
- Rehash-on-login trigger condition.
- Anti-pattern checklist result for existing code (if reviewing).

Sentinel `authn` then validates the implementation matches this design; Comply confirms the parameters meet the applicable standard (NIST SP 800-63B AAL levels, PCI-DSS 4.0 §8.3.6).
