# PII Masking / De-identification for Test Data

**Purpose:** Transform production-flavored data into test-safe datasets through deterministic or randomized tokenization, format-preserving encryption (FPE), and statistical privacy guarantees (k-anonymity / l-diversity / t-closeness / differential privacy). Mint owns the test-data-shaped output; Cloak owns the production-system privacy architecture that produced the raw source.
**Pair with:** `anonymization.md` for the hands-on Faker-based replacement pipeline (locale-aware names, format-preserving masks, production-scrub workflow). This file is the formal de-id taxonomy and scope boundaries; the other is the day-to-day Faker recipe set.

## Scope Boundary

- **Mint `pii`**: test-dataset masking algorithms (tokenization / FPE / k-anon / l-div / t-close / DP). Optimized for reproducible test utility with privacy floor.
- **Cloak (elsewhere)**: production-system privacy engineering — data flow mapping, consent, DPIA, live PII detection in running systems.
- **Oath (elsewhere)**: regulatory framework mapping (GDPR / HIPAA / PCI-DSS controls, audit trails, Policy as Code).
- **Siege (elsewhere)**: volume generation for load tests; does not mask, consumes masked output.

If the hypothesis is "is this test dataset safe to check in or share with a vendor?" → `pii`. If it's "is our production pipeline GDPR-lawful?" → Cloak + Oath.

## Technique Selection

| Technique | Preserves | Reversible? | Use when |
|-----------|-----------|-------------|----------|
| Deterministic tokenization (HMAC) | FK joins, uniqueness | No (with secret destroyed) | Referential integrity across tables must hold in tests |
| Random tokenization | uniqueness only | No | No join requirement, strongest unlinkability |
| Format-preserving encryption (FPE) | format (length, charset, check-digit) | Yes (with key) | Downstream system validates shape (credit card, SSN, phone) |
| Suppression | nothing (field removed) | No | Field is never read by code under test |
| Generalization | distribution | No | Aggregate queries acceptable (age → bucket) |
| Perturbation (noise) | aggregates within ε | No | Numeric columns used in statistics |
| k-Anonymity | group indistinguishability ≥ k | No | Quasi-identifier combinations leak identity |
| l-Diversity | sensitive-value diversity ≥ l within k-group | No | k-anonymity group has uniform sensitive value |
| t-Closeness | sensitive-value distribution within t of global | No | l-diversity still skewed vs population |
| Differential privacy (ε-DP) | aggregate answers ± Lap(Δ/ε) | No | Published statistics, query APIs |

Default for Mint test datasets: **deterministic HMAC tokenization** for identifiers + **Faker replacement** for display fields + **suppression** for Critical-tier (SSN / card PAN / password hash).

## Suppress vs Perturb vs Generalize

```
suppress      → column removed / set NULL           (loses utility, gains safety)
perturb       → value + calibrated noise            (preserves aggregates, breaks exact match)
generalize    → value → bucket / prefix             (preserves ordering, breaks precision)
```

Decision rule: pick the **weakest** transformation that still meets the utility-floor required by the tests consuming the dataset. Over-masking silently breaks test signal; under-masking creates legal / retention risk.

## Deterministic HMAC Tokenization

```python
import hmac, hashlib

def tokenize(value: str, secret: bytes, length: int = 16) -> str:
    mac = hmac.new(secret, value.encode("utf-8"), hashlib.sha256).hexdigest()
    return mac[:length]

# Same input + same secret → same output → FK joins preserved
# Secret rotation = full dataset re-issuance (track secret version in dataset metadata)
```

Store `secret` in the test-data build pipeline, never in the committed fixture. Rotate annually or on incident.

## Format-Preserving Encryption (FF3-1)

Use FPE when downstream validators check shape:

```python
from ff3 import FF3Cipher  # pyffx / ff3 / cryptography-ff3
cipher = FF3Cipher(key_hex, tweak_hex, radix=10)
masked_card = cipher.encrypt("4111111111111111")  # → "7263518204937482" (Luhn-invalid unless re-shaped)
```

Caveats: FF3-1 preserves length and charset but **not** Luhn check-digit. If the test requires Luhn-valid cards, use a domain-aware tokenizer that re-computes the check digit after encryption, or use the issuer's test-card range directly.

## k-Anonymity / l-Diversity / t-Closeness

| Metric | Guarantee | Typical target |
|--------|-----------|----------------|
| k-anonymity | each quasi-id tuple appears ≥ k times | k=5 internal, k=10 external |
| l-diversity | sensitive attr has ≥ l distinct values per k-group | l=3 |
| t-closeness | sensitive-attr distribution within t of global | t=0.2 |

Quasi-identifier = columns that alone don't identify but in combination do (ZIP + DOB + sex famously re-identifies 87% of US pop). Treat quasi-ids as high-risk even if each column feels "low risk."

## Differential Privacy Basics for Datasets

For published aggregates or query APIs — not for row-level test data.

```python
import numpy as np
def laplace_mechanism(true_answer: float, sensitivity: float, epsilon: float) -> float:
    return true_answer + np.random.laplace(0, sensitivity / epsilon)
```

Typical budgets: ε = 1 (strong), ε = 5 (weak but sometimes unavoidable), ε = 10 (explain to Oath). Track cumulative ε across a dataset's lifetime — each query spends from the budget.

## Retention-Limited Test Datasets

| Horizon | Policy |
|---------|--------|
| ≤ 24h | In-memory only, no disk, no backup |
| ≤ 7d | Encrypted volume, auto-delete cron, no copy to laptops |
| ≤ 30d | Encrypted + access-logged storage, periodic re-scan |
| \> 30d | Requires re-masking round or approval from Cloak |

Mask datasets carry a `generated_at` + `expires_at` header; consumers must check before use.

## Anti-Patterns

- Embedding real PII "just for one test run" — production data landing in CI logs is a breach class.
- Using `MD5` or plain `SHA256` (no salt / secret) — rainbow-tableable, not tokenization.
- Format-preserving-encrypting a payment PAN without Luhn recomputation, then sending to a processor sandbox that rejects it.
- Applying k=2 anonymity to satisfy a checkbox — effectively identifies every record when quasi-ids are specific.
- Perturbing primary keys or FK columns — breaks referential integrity while providing no privacy benefit.
- Committing masked fixtures with the HMAC secret alongside them in the repo.
- Re-using a single DP budget across every test-data query without tracking cumulative ε.
- "Masking" by lowercasing / trimming — this is normalization, not de-identification.

## Handoff

**To Radar:** masked fixture set + utility-floor notes (which columns are generalized / suppressed) so assertions don't rely on exact values that no longer exist.
**To Siege:** masked dataset + volume multiplier recipe; Siege inflates, Mint masks.
**To Cloak:** feedback on columns that could not be safely masked while preserving test utility — often a signal that the production schema leaks PII into non-PII columns.
**To Oath:** dataset-level evidence package (technique per column, k / l / t / ε values, retention policy) for audit trail.
