# Test-Data De-identification Contract

Read when a fixture or replay dataset might contain production-derived or identifying data. Prefer schema-generated fixtures; production-derived replay requires the admission and release gates below.

## Admission and Ownership

- Classify source columns, free text, nested objects, metadata, and quasi-identifier combinations **before export**. Production access or an existing dump does not authorize transfer to CI, an LLM, a laptop, or a third party.
- Transform inside the approved protected boundary. Project an **allowlisted output schema**; never spread a real record and replace only known PII fields. Omit unclassified fields until reviewed.
- Radar owns the test dataset and utility evidence. Unresolved privacy design → Cloak; regulatory conclusions → Canon; load-volume generation → Siege. No masking method, synthetic label, or metric alone authorizes public sharing or proves legal anonymization.
- Suppress real credentials, password hashes, government identifiers, payment PANs, and unnecessary sensitive fields. Use reserved/provider test values for validators; do not send real or transformed production payment details to a processor.

## Select the Minimum Sufficient Transformation

| Test need | Mechanism | Required check |
|-----------|-----------|----------------|
| No production-specific behavior | Generate from schema and explicit edge cases | No real input rows or unapproved training data; valid constraints |
| Stable PK/FK relationships | Keyed HMAC tokenization with a consistent namespace per join domain | Canonical input encoding, stable key version, collision detection, all related tables transformed together |
| Display-only fields | Synthetic replacements in the required locale | Reserved contact destinations; no outbound delivery; distribution sufficient for the tests |
| Unused sensitive field | Suppression | No passthrough through JSON, logs, snapshots, or free text |
| Aggregate behavior | Generalization or a reviewed statistical mechanism | Explicit utility tolerance and measured re-identification risk |
| Strict shape validator | Reserved synthetic values first; otherwise reviewed domain-aware tokenization | Length/charset **and** checksum constraints; reversibility and key access documented |

HMAC is pseudonymous linkage, not a claim of anonymous data. Plain hashes, public salts, partial email/phone masks, and normalization do not establish a privacy floor. Keep keys outside fixtures and logs; key rotation requires re-issuing the linked dataset. Do not silently truncate tokens without a collision budget and rejection test.

Do not copy an FPE implementation or choose a cipher from this file. Check the current NIST specification and the installed audited library for the required domain; FPE does not inherently preserve check digits. The NIST revision-1 **second public draft** removed FF3/FF3-1; this is a draft status, not a claim that a final revision has been published.

## Statistical Release Gates

Preserve the repository's screening defaults only as **local risk-review inputs**, not legal guarantees:

| Metric | Local screening default | Measure, do not infer |
|--------|-------------------------|----------------------|
| k-anonymity | k ≥ 5 internal; k ≥ 10 external candidate | Minimum equivalence-class size across the **joint** quasi-identifier set; an age bucket width is not k |
| l-diversity | l ≥ 3 | Sensitive-value diversity within each equivalence class |
| t-closeness | t ≤ 0.2 | Declared distance metric and reference distribution; do not compare unlike definitions |

External release still requires approval and a linkage/re-identification assessment. A dataset passing these screens can remain identifying. For differential privacy, require a reviewed mechanism, adjacency definition, bounded contribution/sensitivity, randomness implementation, declared ε/δ, and composition accounting. A toy noise function, Faker output, or an LLM-generated dataset is not DP evidence. Do not invent a universal ε budget.

## Validation Before Release

- Verify the allowlisted output schema and scan **all** fields, free text, logs, artifacts, and snapshots. Check known source identifiers and join-based leakage; a regex or a known-domain check alone cannot prove absence of PII.
- Validate PK/FK/unique constraints, token collisions, nullability, and consuming assertions. Record the utility floor and measured distribution/edge-case coverage; do not preserve identifiable outliers merely to match a histogram.
- Verify no transformation secret, reversible lookup table, raw source sample, or real contact endpoint ships with the dataset. Keep any necessary mapping separately under the source boundary's access controls.
- Reject on unresolved privacy evidence, expired retention, or failed utility tests; do not weaken the privacy gate to make a fixture pass. Escalate a utility/privacy conflict to Cloak.

## Retention and Handoff

These are repository defaults; a stricter approved source policy wins. Every dataset carries `generated_at`, `expires_at`, source authorization, schema version, transformation/key version identifiers (never key values), per-column technique, validation evidence, and permitted recipients/use. Consumers reject expired datasets.

| Horizon | Storage control |
|---------|-----------------|
| ≤ 24 hours | In-memory only; no disk or backup |
| ≤ 7 days | Encrypted volume, automatic deletion, no laptop copies |
| ≤ 30 days | Encrypted, access-logged storage and periodic rescan |
| > 30 days | Explicit privacy-owner approval with a new expiry; re-masking alone does not extend permission |

Handoff includes the fixture set, utility limitations, privacy-test definitions/results, retention policy, and deletion responsibility. Siege may scale only the approved output; Canon receives evidence, not an unsupported compliance verdict.

## Canonical Checks

- NIST SP 800-188: https://csrc.nist.gov/pubs/sp/800/188/final — select a sharing model, review disclosure risk, and measure release criteria.
- NIST SP 800-38G revision: https://csrc.nist.gov/pubs/sp/800/38/g/r1/2pd — verify publication status and supported FPE algorithms before choosing an implementation.

Source entrypoints checked 2026-09-17. Offline: retain the declared controls and report missing specification/release evidence; never infer approval.
