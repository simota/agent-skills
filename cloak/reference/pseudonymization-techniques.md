# Pseudonymization & De-identification Techniques

Purpose: Technique catalog for transforming personal data so it cannot be attributed to a subject without additional information held separately. Covers the formal de-identification spectrum (k-anonymity → l-diversity → t-closeness → differential privacy) and the operational primitives (tokenization, hashing, format-preserving encryption). Anchored in GDPR Art. 4(5) — pseudonymized data remains personal data; only properly anonymized data exits the GDPR scope.

## Scope Boundary

- **cloak `pseudonymize`**: technique selection and parameter calibration. Outputs the transform spec; does not run the transform.
- **cloak `pii` (sibling)**: detects raw PII to be transformed. `pseudonymize` consumes the inventory.
- **cloak `flow` (sibling)**: data lineage. `pseudonymize` annotates which segments of the flow are pseudonymized vs anonymized.
- **cloak `appi` (sibling)**: applies the 仮名加工 / 匿名加工 distinction; the operational difference is whether the mapping key is retained or destroyed — `pseudonymize` defines that boundary.
- **cloak `gdpr` (sibling)**: Art. 4(5) and Art. 32 reference. Pseudonymization is a recognized safeguard but not an exit from GDPR scope.
- **canon (elsewhere)**: standard-conformance check (ISO/IEC 20889 de-identification techniques, NIST SP 800-188).
- **crypt (elsewhere)**: cryptographic primitives — AES-GCM, HMAC, FF1/FF3-1, HKDF. Cloak chooses *what*; Crypt designs *how*.
- **clause (elsewhere)**: legal sufficiency review when claiming "anonymized" externally — re-identification risk attestation.

## Workflow

```
DISCOVER   →  enumerate quasi-identifiers (QI), sensitive attributes (SA), direct identifiers (DI)
           →  characterize utility goals (analytics? release? ML training?)

CLASSIFY   →  decide release model: pseudonymize-internal vs anonymize-external vs DP-aggregate

MAP        →  attack surface — linkage, homogeneity, background-knowledge, similarity attacks

ASSESS     →  pick technique and parameters: k, l, t, ε, δ; check utility vs privacy tradeoff

REMEDIATE  →  generate transform spec — primitive (tokenize/hash/FPE/encrypt/generalize/perturb),
           →  parameters, key custody, retention of mapping, audit hooks

VERIFY     →  re-identification risk test — Motwani-Xu, prosecutor/journalist/marketer model;
           →  utility test on downstream queries
```

## De-Identification Spectrum

| Level | Definition | Defends Against | Utility Cost |
|-------|-----------|-----------------|--------------|
| Pseudonymization (GDPR Art. 4(5)) | Reversible with separate key; still personal data | Casual re-id; insider with no key access | Low |
| k-anonymity (Sweeney 2002) | Each record indistinguishable from ≥k-1 others on QIs | Linkage attack | Medium |
| l-diversity (Machanavajjhala 2007) | Each equivalence class has ≥l "well-represented" SA values | Homogeneity, background knowledge | Medium-High |
| t-closeness (Li 2007) | SA distribution in each class within t of overall distribution | Similarity attack | High |
| (ε,δ)-Differential Privacy (Dwork 2006) | Output distribution shifts ≤e^ε with δ leakage probability when one record changes | All attribute disclosure (provable) | High; tunable |

## k-anonymity Math

Group records by QI tuple; require each group `|G| ≥ k`. Achieved via **generalization** (ZIP 12345 → 1234*) and **suppression** (drop outliers). Choose `k=5` for low-risk releases, `k=10–20` for medical, `k≥50` for public releases. **Collapses** when SA is homogeneous in a group → escalate to l-diversity.

## l-diversity Math

Per equivalence class: at least `l` distinct SA values **and** entropy-l-diversity `H(SA|class) ≥ log(l)` (recommended). Distinct-l alone is insufficient when distribution is skewed. Recursive (c,l)-diversity bounds the most frequent SA at `c × Σ(rest)`.

## t-closeness Math

Per equivalence class, the distance `D(P_class, P_global) ≤ t` where D is Earth-Mover's Distance for ordinal SA, variational distance for categorical. `t=0.2` balances; `t<0.1` often destroys utility.

## Differential Privacy Basics

| Concept | Formula | Intuition |
|---------|---------|-----------|
| (ε,δ)-DP | Pr[M(D) ∈ S] ≤ e^ε · Pr[M(D') ∈ S] + δ for neighboring D, D' | Single-record influence bounded |
| Sensitivity Δf | max\|f(D) − f(D')\| over neighbors | How much output can change |
| Laplace mechanism | f(D) + Lap(Δf/ε) | Continuous queries, pure ε-DP |
| Gaussian mechanism | f(D) + N(0, σ²), σ ≥ Δf · √(2ln(1.25/δ))/ε | Heavier tail, supports (ε,δ) |
| Composition | Sequential: ε_total = Σε_i; advanced gives √-savings | Budget across queries |
| Privacy loss budget | Total ε across analyst's lifetime | Once spent, cannot query |

**Calibration tiers** (NIST SP 800-226 informed):

| Sensitivity | ε per query | Total budget |
|------------|-------------|--------------|
| Public-facing aggregate | 0.1 – 1.0 | 1 – 5 |
| Internal analytics | 1 – 5 | 5 – 20 |
| Research / training | 5 – 10 | 10 – 50 |
| Last-resort / debug | up to 20 | bounded |

ε > 10 provides weak guarantees; treat as non-private. δ should be `< 1/n²` where n is record count.

## Operational Primitives

| Primitive | Reversible | Format-preserving | Key custody | Use case |
|-----------|-----------|-------------------|-------------|----------|
| Tokenization (vault-based) | Yes (lookup) | Yes | Vault-only | PCI scope reduction; PAN replacement |
| Tokenization (deterministic) | Yes (with key) | Yes | KMS | Cross-system join while masking |
| Hashing (HMAC-SHA-256 + salt) | No | No | Salt is the secret | One-way pseudonym; collision-resistant |
| Hashing (plain SHA-256) | No (but rainbow-attackable on small domains) | No | None | NEVER for low-entropy PII (email, phone, SSN) |
| Format-Preserving Encryption (FF1/FF3-1) | Yes | Yes | KMS | Replace 16-digit card with 16-digit ciphertext; legacy schema fit |
| Symmetric encryption (AES-GCM) | Yes | No | KMS | Encrypted-at-rest; reversible to authorized roles |
| Generalization | No | Sometimes | None | k-anonymity prerequisite |
| Suppression | No | No | None | Drop high-risk outliers |
| Perturbation / noise | No | Sometimes | None | Differential privacy realization |
| Synthetic data (GAN/CTGAN) | No (statistical) | Yes | None | ML training without releasing real data |

**Hashing-of-PII trap**: SHA-256 of an email is brute-forceable in seconds — the email space is small. Always use HMAC with a secret salt, or treat the "hash" as encryption with the salt as key (then key custody applies).

## Tokenization vs Hashing vs Encryption Tradeoffs

| Concern | Tokenization | Hashing | FPE | AES-GCM |
|---------|-------------|---------|-----|---------|
| Reversibility | Yes (vault) | No | Yes | Yes |
| Format preserved | Yes | No | Yes | No |
| Schema fit (legacy) | Yes | No | Yes | No |
| Cross-system join | Deterministic only | Yes (deterministic) | Yes | Yes (deterministic mode) |
| Throughput | Vault round-trip latency | Compute-only | Compute-only | Compute-only |
| Standards | PCI DSS recognized | NIST FIPS 180 | NIST SP 800-38G | NIST FIPS 197 |
| Brute-force resistance (low-entropy input) | High (vault) | Low (hash plain) / High (HMAC+salt) | High | High |

## Key Management Essentials

| Concern | Standard |
|---------|----------|
| Key generation | KMS HSM-backed; never application-side `Math.random` |
| Key storage | KMS / HSM; mapping table separate from data |
| Key rotation | Annually + on-incident; FF3-1 supports tweak-based partial rotation |
| Key destruction | NIST SP 800-88 sanitization for true 匿名加工 / "anonymized" claim |
| Audit | Every decrypt / detokenize logged with subject, role, purpose |
| Separation of duties | Data engineers cannot self-grant decrypt; break-glass with dual approval |

Without key destruction, you have pseudonymized — not anonymized — data. Many "anonymization" claims fail this audit.

## Re-identification Risk Models

| Adversary | Knowledge | Test |
|-----------|-----------|------|
| Prosecutor | Targets known individual in dataset | min equivalence-class size = k |
| Journalist | Targets some matching individual | expected uniqueness rate |
| Marketer | Population-level inference | average risk across all records |

ENISA/Article 29 WP guidance: assess all three before releasing as anonymized.

## Anti-Patterns

- **Hashing email/phone with plain SHA-256** — domain is small enough for offline brute force in seconds. Use HMAC with a kept-secret salt, or accept it is encryption, not hashing.
- **Calling tokenized data anonymized** — vault enables reversal; this is pseudonymization with vault as the "additional information." GDPR scope still applies.
- **Skipping l-diversity after k-anonymity** — homogeneity attack: if all 50 records in a class have the same diagnosis, k=50 doesn't help.
- **Differential privacy with ε > 10** — provides ~no guarantee. Choose ε ≤ 5 for analytics, ≤ 1 for public release; document the budget formally.
- **Reusing the DP budget** — once exhausted, queries must stop or guarantee weakens monotonically. Build a budget accountant; alert at 80%.
- **Generalization without utility test** — over-generalized data is useless and may still be re-identifiable via auxiliary datasets. Validate against known linkage benchmarks.
- **Single-pass anonymization on streaming data** — k-anonymity assumes static release; streams require different mechanisms (CASTLE, FADS) or DP from the start.
- **Forgetting the mapping-table half** — pseudonymization splits sensitive data from the key. Storing both in the same DB defeats the safeguard.
- **Synthetic data as a free pass** — modern membership-inference attacks recover training records from generative models. Treat synthetic data as DP-bounded, not zero-risk.

## Handoff

- **To Crypt**: KMS architecture, FF1/FF3-1 / AES-GCM parameter selection, HMAC salt management, key rotation and destruction procedures.
- **To Canon**: ISO/IEC 20889 technique mapping, NIST SP 800-188 conformance, GDPR Art. 4(5) / Art. 32 standard alignment.
- **To Clause**: re-identification risk attestation language for external "anonymized" releases; data-sharing agreement clauses.
- **To Comply**: SOC 2 / HIPAA Safe Harbor / ISO 27701 control mapping; evidence package for the 18-identifier HIPAA Expert Determination path.
- **To Builder**: implement transform pipelines — tokenization adapter, FPE wrapper, DP-noise layer, generalization rules.
- **To Schema**: column-level annotations (`pseudonymized: hmac-sha256+salt`, `anonymized: dp ε=2`), key-id references, retention separation.
- **To Stream**: streaming-DP or CASTLE integration for real-time pipelines that cannot wait for batch anonymization.
