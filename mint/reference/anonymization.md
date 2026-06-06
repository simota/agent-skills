# PII Masking & Anonymization

**Purpose:** Techniques for converting production data into safe test data — Faker-based replacement, format-preserving masks, k-anonymity, and the production-scrub pipeline.
**Read when:** Anonymizing production data or ensuring fixtures contain no real PII.
**Pair with:** `pii-masking-deidentification.md` for the formal de-id taxonomy (HMAC tokenization, FF3-1 FPE, k/l/t/ε guarantees, retention horizons, scope boundaries vs Cloak/Comply/Siege). This file is the hands-on Faker pipeline; the other is the privacy-engineering taxonomy.

---

## Anonymization Techniques

### 1. Faker Replacement (Recommended Default)

Replace real values with realistic fakes. Best for most test data needs.

```typescript
import { faker } from '@faker-js/faker';

function anonymizeUser(real: User): User {
  return {
    ...real,
    name: faker.person.fullName(),
    email: faker.internet.email(),
    phone: faker.phone.number(),
    address: faker.location.streetAddress(),
    ssn: undefined, // Remove entirely
    dateOfBirth: faker.date.birthdate(),
  };
}
```

### 2. Consistent Hashing

Preserve referential integrity while anonymizing.

```typescript
import { createHash } from 'crypto';

function consistentAnonymize(value: string, salt: string): string {
  const hash = createHash('sha256').update(value + salt).digest('hex');
  return hash.substring(0, 16);
}

// Same input always produces same output
// "john@example.com" → "a3f2b8c1d4e5f6a7" (always)
```

### 3. Format-Preserving Masking

Maintain data shape while removing real values.

```typescript
function maskEmail(email: string): string {
  const [local, domain] = email.split('@');
  return `${local[0]}${'*'.repeat(local.length - 1)}@${domain}`;
  // "john.doe@example.com" → "j*******@example.com"
}

function maskPhone(phone: string): string {
  return phone.replace(/\d(?=\d{4})/g, '*');
  // "090-1234-5678" → "***-****-5678"
}

function maskCreditCard(cc: string): string {
  return cc.replace(/\d(?=\d{4})/g, '*');
  // "4111111111111111" → "************1111"
}
```

### 4. k-Anonymity

Generalize values so each record is indistinguishable from k-1 others.

```typescript
function kAnonymizeAge(age: number, k: number = 5): string {
  const rangeSize = k;
  const lower = Math.floor(age / rangeSize) * rangeSize;
  return `${lower}-${lower + rangeSize - 1}`;
  // age 27, k=5 → "25-29"
}

function kAnonymizeZip(zip: string): string {
  return zip.substring(0, 3) + '**';
  // "10001" → "100**"
}
```

### 5. Differential Privacy (Aggregate Only)

Add calibrated noise for statistical queries.

```typescript
function addLaplaceNoise(value: number, sensitivity: number, epsilon: number): number {
  const scale = sensitivity / epsilon;
  const u = Math.random() - 0.5;
  const noise = -scale * Math.sign(u) * Math.log(1 - 2 * Math.abs(u));
  return value + noise;
}
```

---

## PII Field Classification

| Risk Level | Fields | Action |
|------------|--------|--------|
| Critical | SSN, credit card, password hash | **Remove entirely** |
| High | Name, email, phone, address, DOB | **Replace with Faker** |
| Medium | IP address, user agent, geolocation | **Generalize or hash** |
| Low | Preferences, settings, roles | **Keep as-is** |

---

## Production Data Pipeline

```
Production DB
     ↓
[1. Export] → pg_dump --data-only
     ↓
[2. Classify] → Identify PII columns per table
     ↓
[3. Anonymize] → Apply technique per classification
     ↓
[4. Validate] → Verify no PII leaked, FK intact
     ↓
[5. Import] → Load into test environment
```

### Validation Checklist

- [ ] No real email addresses (check for known domains)
- [ ] No real phone numbers (check for valid patterns)
- [ ] No real names cross-referenced with other fields
- [ ] FK constraints still valid after anonymization
- [ ] Data distributions roughly preserved
- [ ] Unique constraints still satisfied
- [ ] No PII in free-text fields (comments, notes, descriptions)

---

## Language-Specific Faker Locales

| Language | Locale | Key Features |
|----------|--------|-------------|
| Japanese | `ja` | 日本語名、住所、電話番号 |
| English | `en` | Names, addresses, phone |
| Chinese | `zh_CN` | 中文名、地址 |
| Korean | `ko` | 한국어 이름, 주소 |
| German | `de` | Deutsche Namen, Adressen |

```typescript
import { faker } from '@faker-js/faker/locale/ja';

const jaUser = {
  name: faker.person.fullName(),    // "田中 太郎"
  address: faker.location.city(),   // "横浜市"
  phone: faker.phone.number(),      // "090-1234-5678"
};
```

---

## Legal Considerations

- GDPR Article 4(5): Pseudonymization is NOT anonymization
- Properly anonymized data falls outside GDPR scope
- Test environments with real PII require same security controls as production
- Document anonymization approach for audit compliance
- Consider Cloak agent for full privacy engineering compliance

## 2026 Posture: Synthetic + Differential Privacy is the New Baseline

By 2026 the legal advice on "scrub production then ship to staging" has hardened. Multiple 2026 GDPR guidance pieces describe the old scrub-and-ship pipeline as **legally indefensible** for QA environments — pseudonymized production data still pulls in GDPR obligations, and audit trails for "we removed enough" are not credible under examination.

The 2026 gold standard:

1. **Synthetic data generation** (GAN-based, VAE-based, or LLM-based — see `llm-generated-fixtures.md`) becomes the source for test data; production data does not leave the production boundary.
2. **Differential Privacy** layered on top of the generator: calibrated noise during training prevents the synthetic model from memorising a specific individual. DP-protected synthetic data is the only widely-accepted shape that earns *anonymization* treatment under GDPR.
3. **Hold-out validation**: keep a small, locked real-data set inside the production boundary and verify that models / queries trained on synthetic produce comparable results — that is the credibility evidence for regulators.

Practical rules:

- For greenfield projects in 2026, **skip the production-scrub pipeline entirely** — synthesise from schema + statistics, never from real rows.
- For projects with a legacy scrub pipeline, **add DP** as the next step rather than refining the scrub. DP-protected outputs survive a GDPR audit; better-scrubbed PII does not.
- DP alone may qualify as pseudonymization under GDPR Articles 4(5) / 89 (still under controller obligations) — full *anonymization* requires DP-protected synthetic generation, not raw DP on production rows.
- For LLM-generated fixtures, validate DP claims independently — running `faker` + LLM through a privacy harness (e.g., SDV / Synthcity privacy metrics) is the audit evidence.

See `replay-production-scrub.md` for the migration path off scrub-and-ship pipelines and `llm-generated-fixtures.md` for the LLM-based synthesis flow.
