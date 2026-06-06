# PII Detection Reference

## Field Name Patterns

Common field names that indicate PII presence in code, schemas, and APIs.

### Direct Identifiers (CRITICAL)

| Pattern | Regex | Examples |
|---------|-------|----------|
| Full name | `(?i)(full_?name\|first_?name\|last_?name\|family_?name\|given_?name\|display_?name\|user_?name)` | `firstName`, `last_name`, `displayName` |
| Email | `(?i)(e_?mail\|email_?address\|mail_?to\|contact_?email)` | `email`, `emailAddress`, `contactEmail` |
| Phone | `(?i)(phone\|tel\|mobile\|cell\|fax)(_?num(ber)?)?\b` | `phone`, `mobileNumber`, `tel` |
| National ID | `(?i)(ssn\|social_?security\|my_?number\|national_?id\|passport\|driver_?license)` | `ssn`, `myNumber`, `passportNo` |
| Address | `(?i)(address\|street\|city\|zip_?code\|postal_?code\|prefecture\|state\|country)` | `streetAddress`, `zipCode` |

### Indirect Identifiers (HIGH)

| Pattern | Regex | Examples |
|---------|-------|----------|
| IP address | `(?i)(ip_?addr(ess)?\|remote_?addr\|client_?ip\|source_?ip)` | `ipAddress`, `clientIp` |
| Device | `(?i)(device_?id\|device_?fingerprint\|ua\|user_?agent\|imei\|mac_?addr)` | `deviceId`, `userAgent` |
| Location | `(?i)(lat(itude)?\|lng\|lon(gitude)?\|geo_?loc\|coordinates\|location)` | `latitude`, `geoLoc` |
| Cookie/Session | `(?i)(cookie\|session_?id\|tracking_?id\|visitor_?id\|analytics_?id)` | `sessionId`, `trackingId` |

### Financial (CRITICAL)

| Pattern | Regex | Examples |
|---------|-------|----------|
| Credit card | `(?i)(card_?num\|cc_?num\|credit_?card\|pan\|card_?holder)` | `cardNumber`, `ccNum` |
| Bank | `(?i)(bank_?account\|iban\|routing\|swift\|sort_?code\|account_?num)` | `bankAccount`, `iban` |
| Payment | `(?i)(payment_?token\|billing\|invoice_?amount)` | `paymentToken` |

### Health (CRITICAL — Special Category)

| Pattern | Regex | Examples |
|---------|-------|----------|
| Medical | `(?i)(diagnosis\|prescription\|medical\|health\|patient\|symptom\|allergy\|blood_?type)` | `diagnosis`, `patientId` |
| Insurance | `(?i)(insurance_?id\|policy_?num\|claim)` | `insuranceId` |

## Value-Level PII Detection

Regex patterns for detecting PII values in strings, logs, and payloads.

```
# Email
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

# Japanese phone (with/without hyphens)
0[0-9]{1,4}-?[0-9]{1,4}-?[0-9]{4}

# International phone
\+?[1-9]\d{1,14}

# Credit card (Luhn-checkable)
\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b

# SSN (US)
\b\d{3}-?\d{2}-?\d{4}\b

# My Number (Japan, 12 digits)
\b\d{4}\s?\d{4}\s?\d{4}\b

# IPv4
\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b

# Japanese postal code
\b\d{3}-?\d{4}\b

# Date of birth patterns
\b(19|20)\d{2}[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b
```

## Common PII Hiding Spots

Places where PII is often found but easily overlooked:

| Location | What to check | Risk |
|----------|---------------|------|
| **Log statements** | `console.log`, `logger.info/debug`, error messages | PII in production logs |
| **Error responses** | Stack traces, validation errors with user input | PII leaked to client |
| **URL parameters** | Query strings, path parameters | PII in server logs, browser history, referrer headers |
| **HTTP headers** | Custom headers carrying user data | PII in proxy/CDN logs |
| **Cache keys** | Redis/memcached keys containing user data | PII in cache dumps |
| **Analytics events** | Tracking payloads with user properties | PII sent to third parties |
| **Test fixtures** | Hardcoded real user data in test files | PII in source control |
| **Comments/TODOs** | Developer notes with real data examples | PII in source control |
| **Environment variables** | API keys referencing user-specific endpoints | Credential + PII coupling |
| **Seed/migration files** | Database seeds with real data | PII in source control |
| **i18n interpolation** | Template strings with PII variables | PII in translation files |

## Scanning Strategy

### Phase 1: Schema Scan
1. Scan DB migration files and schema definitions for PII field names.
2. Check ORM model definitions for sensitive field types.
3. Look for missing encryption annotations on sensitive fields.

### Phase 2: API Surface Scan
1. Scan request/response types for PII fields.
2. Check OpenAPI specs for PII in examples.
3. Verify API responses don't over-fetch (returning more PII than needed).

### Phase 3: Code Flow Scan
1. Trace PII from input (forms, APIs) through processing to storage.
2. Check for PII in log statements (all log levels).
3. Verify PII is not in URL query parameters.
4. Check error handlers for PII leakage.

### Phase 4: Third-Party Scan
1. Identify analytics SDK calls carrying PII.
2. Check third-party API calls for PII in payloads.
3. Verify cookie consent before tracking initialization.

## Data Classification Output Format

```markdown
## PII Inventory

| # | Field | Location | Tier | Data Subject | Lawful Basis | Retention | Risk |
|---|-------|----------|------|-------------|-------------|-----------|------|
| 1 | email | users.email | Personal | Customer | Contract | Account lifetime + 30d | MEDIUM |
| 2 | ssn | profiles.tax_id | Sensitive | Customer | Legal obligation | Tax year + 7y | HIGH |
| 3 | ip_address | access_logs.ip | Personal | Visitor | Legitimate interest | 90 days | LOW |
```
