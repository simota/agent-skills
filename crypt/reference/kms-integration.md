# KMS Integration Reference

Purpose: Design the cryptographic integration with a Key Management Service (AWS KMS, GCP KMS, Azure Key Vault, HashiCorp Vault Transit) so that the application never touches key material directly. Envelope encryption, data-key caching, and HSM-backed CMK decisions live here.

## Scope Boundary

- **Crypt `kms`**: cryptographic KMS-integration pattern — envelope encryption, CMK vs DEK separation, HSM-backing, data-key cache, crypto-context/AAD binding, KMS-native key rotation.
- **Crypt `key`**: general key-management strategy — key hierarchy, rotation policy, key ceremony, destruction — one layer above `kms`. `key` decides policy; `kms` selects the service wiring.
- **Gear `secret`**: application-level secrets-management architecture (Vault / AWS Secrets Manager / Doppler) — the devops integration pattern for non-cryptographic secrets (DB passwords, API tokens, OAuth creds).
- **Scaffold**: provisions the KMS / HSM resources via IaC once `kms` has selected the service.

Overlap with Gear `secret` is intentional: the same platform (e.g., Vault) serves both a cryptographic role (Vault Transit) and a secret-storage role (Vault KV). `kms` designs the Transit side; `secret` designs the KV side.

## Provider Selection

| Provider | Pick when | Skip when |
|----------|-----------|-----------|
| AWS KMS | Already on AWS, envelope + S3/EBS/RDS integration | Multi-cloud; per-operation KMS cost unacceptable at your QPS |
| AWS KMS (CloudHSM-backed CMK) | FIPS 140-2 Level 3, tenant-isolated HSM required | Cost-sensitive workloads |
| GCP Cloud KMS | Already on GCP, Cloud HSM tier for HSM-backed keys | AWS-native ecosystem |
| Azure Key Vault (Managed HSM) | Azure-native, FIPS 140-3 Level 3 HSM required | Non-Azure stacks |
| HashiCorp Vault Transit | Multi-cloud / on-prem, encryption-as-a-service without exposing keys | No team to operate Vault HA |
| PKCS#11 HSM (Thales / AWS CloudHSM direct) | Root-of-trust / code-signing keys, rare operations | High-QPS bulk encryption |

Default: **cloud-native KMS matching the workload's primary cloud**, HSM-backed CMK only where compliance or threat model demands it.

### Post-Quantum Readiness of the KMS Itself (2026-05)

PQC is no longer just a TLS-layer migration; the KMS itself must be able to wrap data keys with a post-quantum-safe algorithm. As of 2026-05:

| Provider | PQ envelope status |
|----------|-----------------------|
| AWS KMS | Hybrid `X25519MLKEM768` available for the API-layer TLS termination; native post-quantum CMK algorithms remain on the roadmap — wrap a `ML-KEM` DEK at the application layer when needed |
| GCP Cloud KMS | Hybrid TLS to the API; PQC CMK previewing — track for production GA |
| Azure Key Vault / Managed HSM | `ML-DSA` certificate issuance and `ML-KEM` key types in preview alongside Microsoft's CNG GA (Nov 2025) |
| HashiCorp Vault Transit | `ML-KEM` / `ML-DSA` available behind feature flags; the practical migration is `transit/encrypt` hybrid envelope (X25519 + ML-KEM) |
| PKCS#11 HSM (CloudHSM, Thales, etc.) | Firmware refresh cycle dominates; treat as the slowest-moving surface in the migration plan |

Operational rule: keep the **KMS protocol negotiation** post-quantum-safe (hybrid TLS to the API endpoint) even when the **wrapping algorithm** is still classical. That covers the HNDL risk on the network traffic between the application and the KMS while the deeper algorithm migration is in flight. See `post-quantum-migration.md` for the broader plan.

## Envelope Encryption Pattern

Never encrypt application payloads directly under the CMK. Use the standard two-tier envelope:

```
CMK  (stays inside KMS / HSM, never leaves)
 └─ generates/wraps ─┐
                     ▼
                    DEK  (data encryption key, AES-256)
                     └─ encrypts ─┐
                                  ▼
                               plaintext payload
```

Write path:
1. `GenerateDataKey(CMK, AES_256)` → `{plaintext_dek, encrypted_dek}`.
2. Encrypt payload locally with `plaintext_dek` using AES-256-GCM; generate random 96-bit IV per message.
3. Store `{ciphertext, iv, tag, encrypted_dek, cmk_id, alg_version}` together. Zero `plaintext_dek` immediately.

Read path:
1. `Decrypt(encrypted_dek, CMK)` → `plaintext_dek`.
2. Decrypt payload with `plaintext_dek`; verify GCM tag.
3. Zero `plaintext_dek` after use.

Always bind an encryption context / AAD (AWS KMS `EncryptionContext`, GCP `additionalAuthenticatedData`) to the tenant or row identity so a ciphertext cannot be decrypted outside its original scope.

## Data-Key Caching

KMS `Decrypt` is rate-limited and billed per request. For high-QPS paths, cache plaintext DEKs in memory under strict TTL.

Policy (AWS Encryption SDK defaults are a reasonable starting point):
- Max bytes encrypted per DEK: 2^32 messages or 10 GB, whichever first (AES-GCM nonce-exhaustion guard).
- Max age per cached DEK: ≤ 10 minutes.
- Max entries: bounded (e.g., 1000); LRU eviction.
- Zero cache on process exit and on CMK rotation event.
- Never persist the plaintext DEK outside the process memory.

Do **not** roll your own cache for AWS: use the AWS Encryption SDK's caching CMM. For Vault Transit, use `batch_input` rather than per-call decrypt.

## CMK Hierarchy and Rotation

Separate CMKs per:
- trust zone (prod vs staging vs dev — never share),
- data class (PII vs billing vs logs),
- tenant (for high-assurance multi-tenant SaaS; use KMS grants + encryption context otherwise).

Rotation:
- Enable KMS-managed annual rotation for symmetric CMKs (AWS KMS: 365-day default, now configurable 90–2560 days).
- For customer-managed rotation, publish a new `key_version`; keep old versions wrap-decrypt-only until DEK corpus aging out.
- Alias-based lookup (`alias/app-prod-pii`) — never hardcode key ARN/resource ID in application code.

HSM-backed CMK (AWS CloudHSM / GCP Cloud HSM / Azure Managed HSM):
- Required for: code-signing root, root-of-trust for E2EE, CNSA 2.0 / FIPS 140-3 Level 3 scope.
- Not required for: bulk application data encryption — standard CMK is sufficient and cheaper.

## IAM and Grants

- Least-privilege per CMK: separate principals for `Encrypt`, `Decrypt`, `GenerateDataKey`, and administrative actions.
- KMS key policy is authoritative; IAM policy alone cannot grant access to a CMK. Gate rotation/deletion by a break-glass role with MFA.
- AWS KMS grants for short-lived delegation (expire within hours).
- Log every `Decrypt` call (CloudTrail / Cloud Audit Logs). Alert on decryption from unexpected principals or regions.

## Anti-Patterns

- Calling `Encrypt`/`Decrypt` on the CMK directly for payload data (ignores envelope; hits per-request limits; leaks metadata size).
- Reusing a plaintext DEK across unrelated records without a nonce strategy — single-key AES-GCM is limited to ~2^32 messages.
- Skipping encryption context / AAD — enables cross-tenant ciphertext replay.
- Storing `encrypted_dek` in a separate store than the ciphertext (recovery becomes impossible if they diverge).
- Treating Vault Transit as a general secrets store — use Vault KV for that (→ Gear `secret`).
- Hardcoding CMK ARNs in code — use aliases so rotation or region failover doesn't require redeploy.
- Disabling CloudTrail KMS events "for cost" — this is the only audit signal for key misuse.

## Handoff to Builder / Scaffold

Deliver:
- Provider + CMK alias + region(s), HSM-backing decision with justification.
- Envelope encryption pseudocode with exact library calls (AWS Encryption SDK, `@google-cloud/kms`, `vault.logical.write('transit/encrypt/...')`).
- Encryption-context schema (keys used to bind ciphertext to logical owner).
- Data-key cache policy (max bytes, max age, max entries).
- CMK rotation cadence and migration plan for old DEK corpus.
- IAM / key-policy split (encrypt-only service role, decrypt-only reader role, admin break-glass role).
- CloudTrail / audit-log alert rules.

Scaffold provisions the CMK + IAM; Builder wires the SDK calls; Sentinel verifies no plaintext DEK escapes the process boundary.
