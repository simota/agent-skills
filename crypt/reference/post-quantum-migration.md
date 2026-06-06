# Post-Quantum Cryptography Migration Reference

Purpose: Plan the migration from classical public-key cryptography (RSA, ECDSA, ECDH, X25519) to NIST-standardized post-quantum algorithms. Optimize for the harvest-now-decrypt-later threat and for crypto-agility mandated by NIST IR 8547.

## Scope Boundary

- **Crypt `pqc`**: the migration plan itself — inventory, timeline, hybrid-scheme selection, rollout sequencing, rollback.
- **Crypt `algo`** (default): selects the current-best algorithm for a new use case; will flag quantum-vulnerability but does not own the migration program.
- **Crypt `tls`**: TLS/mTLS configuration. TLS 1.3 hybrid key exchange (X25519MLKEM768) is a `pqc` topic that `tls` applies — the migration decision lives here, the cipher-suite wiring lives there.
- **Oath**: maps regulatory mandates (CNSA 2.0, BSI TR-02102, ANSSI, MAS) that drive the timeline — `pqc` consumes those requirements.

If the question is "pick an algorithm today" → `algo`. If it is "how do we transition off RSA-2048 over 3 years?" → `pqc`.

## Threat Model: Harvest Now, Decrypt Later (HNDL)

A sufficiently capable adversary is assumed to record classical-public-key-protected traffic and archive it. When a cryptographically-relevant quantum computer (CRQC) becomes available — NIST's working assumption is 2030–2040 — Shor's algorithm breaks RSA, DH, ECDH, and ECDSA retroactively. Data whose confidentiality must outlast that horizon is already at risk today.

HNDL sensitivity ranking:
1. Long-lived confidential data (healthcare, state secrets, IP, genome) — **migrate now**.
2. Session-key-protected ephemeral traffic with long-lived authentication (TLS) — migrate KEX now (hybrid), signatures next.
3. Short-lived signatures (JWT 1-hour, session cookies) — lowest urgency; migrate with the signature-refresh cycle.
4. Data-at-rest under symmetric AES-256 — **no migration needed**; AES-256 is PQ-safe (Grover halves effective strength to 128-bit, still acceptable).

## NIST PQC Standards (2026-05 snapshot)

| Standard | Algorithm | Role | Replaces |
|----------|-----------|------|----------|
| FIPS 203 | ML-KEM (CRYSTALS-Kyber) | Key encapsulation | RSA-OAEP, ECDH, X25519 |
| FIPS 204 | ML-DSA (CRYSTALS-Dilithium) | General signatures | RSA-PSS, ECDSA, Ed25519 |
| FIPS 205 | SLH-DSA (SPHINCS+) | Hash-based conservative signatures | — (stateless backup; large signatures) |
| FIPS 206 (draft) | FN-DSA (FALCON) | Compact signatures | ECDSA where size matters |
| HQC (NIST selected Mar 2025; draft 2026, final 2027) | Code-based KEM | Backup for ML-KEM | — (diversification against lattice break) |

Parameter sets in practice:
- ML-KEM-768 → NIST Category 3 (~AES-192 equivalent) — default for TLS hybrid.
- ML-KEM-1024 → Category 5 (~AES-256) — long-term confidentiality, CNSA 2.0.
- ML-DSA-65 → Category 3 default; ML-DSA-87 for Category 5.
- SLH-DSA-SHA2-128s → smallest SLH-DSA, when stateless hash-based is required (firmware signing).

### Library / Platform Availability (2026-05)

| Surface | PQC status |
|---------|-------------|
| **OpenSSL 3.5+** (Apr 2025 release line) | Native `ML-KEM`, `ML-DSA`, `SLH-DSA` providers — no liboqs glue required for the standard algorithms. Default to 3.5+ for new builds; stay on 3.x + liboqs only when 3.5 cannot be deployed. |
| **Microsoft CNG (Windows Server 2025, Windows 11 client)** | `ML-KEM` and `ML-DSA` Generally Available since the November 2025 update; Certificate APIs handle PQ certs end-to-end. AD CS (Microsoft Active Directory Certificate Services) issues `ML-DSA` certificates as of the May 2026 update. |
| **AWS / Google / Cloudflare edge** | Hybrid `X25519MLKEM768` on by default for browser-facing TLS termination since 2024–2025; Akamai followed in **Feb 2026** (default for all customers). |
| **Apple platforms** | `iMessage PQ3` (iOS 17.4 / iPadOS 17.4 / macOS 14.4 / watchOS 10.4): **Level 3** PQ messaging — `ML-KEM` is woven into the ongoing ratchet, not just the handshake. |
| **Signal Protocol** | `PQXDH` (Level 2) — `ML-KEM` at session initialisation only. |
| **HashiCorp Vault** | `ML-KEM` / `ML-DSA` available behind feature flags; `transit/encrypt` hybrid envelope (X25519+ML-KEM) is the migration target. |

Apple + Signal together put PQC on **roughly 2 billion endpoints** today — the migration ecosystem has graduated from "proof of concept" to "your users already have PQ in their pocket".

## Migration Timelines

Match whichever applies and design to the earliest binding deadline:

| Regime | Deadline | Source |
|--------|----------|--------|
| NIST general | Deprecate quantum-vulnerable by 2030; disallow by 2035 | NIST IR 8547 (draft) |
| NSA CNSA 2.0 (US NSS) | New equipment quantum-safe by **Jan 2027** | CNSA 2.0 (2022, updated 2024) |
| NSA CNSA 2.0 (applications) | Migrated by 2030 | CNSA 2.0 |
| NSA CNSA 2.0 (infra) | Migrated by 2035 | CNSA 2.0 |
| Classical 112-bit strength | Deprecated end of 2030 (RSA-2048, 2-key TDEA) | NIST SP 800-131A Rev 3 (draft) |
| **Google infrastructure** (public commitment, Mar 2026) | Full PQ migration by **2029** | Google PQC roadmap announcement |
| **Cloudflare** (public commitment) | Full PQ migration by **2029** | Cloudflare PQ roadmap |

The Google + Cloudflare 2029 commitments are the de-facto industry coordination point in 2026 — smaller vendors are pacing themselves against it. When a project has no explicit regulatory deadline, anchor the migration plan on **2029** rather than the looser NIST 2035 disallow date.

CNSA 2.0 mandates ML-KEM and ML-DSA (does not include SLH-DSA). For non-NSS workloads, SLH-DSA is allowed and recommended where hash-based assurance is preferred (firmware, long-term archive).

## Hybrid Scheme (Transition Default)

During the transition window, combine classical + PQC so the composite is at least as strong as the stronger component. This hedges against both classical advances and PQ algorithm breaks.

Key exchange (TLS 1.3, IKEv2, SSH): concatenate shared secrets.
- **X25519MLKEM768** (RFC-registered IANA code point `0x11EC`) — preferred hybrid group; shipped in Chrome, Firefox, Cloudflare, AWS, Google as of 2024-2026.
- SecP256r1MLKEM768, SecP384r1MLKEM1024 — IETF alternatives for ECDSA-anchored stacks.

Signatures (CMS, X.509, code signing): composite or parallel.
- Composite-Sigs (IETF draft, LAMPS WG): single X.509 SubjectPublicKeyInfo carrying ML-DSA + classical; verifier requires both valid.
- Parallel / dual signatures: two independent certificates; flexible but doubles storage.

When to drop the classical half: only after the ecosystem confirms interoperability and no regulatory mandate requires the hedge. CNSA 2.0 expects pure PQC (no hybrid) post-2033 for NSS.

## Migration Workflow

```
INVENTORY  →  enumerate every use of RSA / DH / ECDH / ECDSA / Ed25519
           →  classify by HNDL sensitivity and deadline regime
           →  tag: library, protocol, certificate, embedded constant

AGILITY    →  ensure algorithm selection is configuration, not hardcoded
           →  abstract behind interface; support runtime substitution
           →  version every stored ciphertext / signature with alg ID

PILOT      →  enable hybrid KEX on a non-critical TLS surface
           →  measure handshake latency (ML-KEM-768 adds ~1-2 KB)
           →  measure signature sizes for ML-DSA (~3.3 KB for ML-DSA-65)

ROLLOUT    →  stage by protocol: TLS KEX → signatures → at-rest wrap keys
           →  dual-stack: accept both classical and hybrid until 95% traffic is hybrid
           →  monitor error rates; HSMs and old middleboxes often MTU-fail large handshakes

SUNSET     →  remove classical fallback once mandated deadline or risk posture dictates
           →  keep verification-only path for archived signatures
```

## Anti-Patterns

- Treating PQC as a drop-in library swap — ML-DSA signatures are 10-40× larger than Ed25519; protocol framing, MTU, log size, and storage budgets all shift.
- Skipping the hybrid phase to "go native PQC" — if ML-KEM is broken (Kyber parameter adjustments already happened pre-standardization), pure-PQC is catastrophic; hybrid is the safety net.
- Adopting non-standardized candidates for production ("Kyber round-3" params instead of FIPS 203 ML-KEM) — these are not wire-compatible with the standard.
- Encoding algorithm choice in cert serial numbers or magic bytes — defeats crypto-agility. Always use proper OID / IANA code point identifiers.
- Forgetting firmware / HSM / smartcard paths — these have 5–10 year refresh cycles and dominate the real migration cost.
- Migrating signatures before KEX — HNDL risk is in the KEX (data confidentiality), not the signature (authentication integrity today).

## Handoff to Builder / Scaffold / Oath

Deliver:
- Inventory table (system, algorithm, key size, HNDL sensitivity, deadline).
- Target PQC algorithm + parameter set per use case (ML-KEM-768, ML-DSA-65, etc.).
- Hybrid scheme selection (X25519MLKEM768 for TLS, composite-sig for X.509).
- Per-protocol rollout order with success metrics (handshake latency budget, signature-size budget).
- Crypto-agility refactor list (hardcoded `RSA-2048` → config + version-tagged storage).
- Library selection: OpenSSL 3.4+ (ML-KEM/ML-DSA native), liboqs (provider), BoringSSL, AWS-LC.
- Rollback plan per phase.

Oath maps deadlines to business regulatory obligations; Scaffold provisions upgraded KMS/HSM firmware; Builder implements the refactor; Sentinel audits that no quantum-vulnerable algorithm remains after sunset.
