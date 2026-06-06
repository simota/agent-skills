# Usage Examples

**Purpose:** Concrete sample outputs for Tome.
**Read when:** Verifying expected output format or quality.

---

## Example 1: Refactoring Change — Learning Document

### Input
```
Target: commit abc1234 "refactor(auth): extract validation logic"
Audience: intermediate
Format: learning_doc
```

### Output (excerpt)

```markdown
# Authentication Validation Logic Extraction — Learning Document

## Meta
| Field | Value |
|-------|-------|
| Target | commit abc1234 |
| Date | 2025-07-10 |
| Audience | intermediate |
| Related files | auth/handler.ts, auth/validator.ts (new), auth/handler.test.ts |
| Change volume | +85 / -42 lines, 3 files |

## Overview
Extracted validation logic mixed into the auth handler into an independent module.
Based on Single Responsibility Principle, improved readability and testability
of the authentication flow.

## Glossary
| Term | Definition | Context in this change |
|------|-----------|----------------------|
| Single Responsibility Principle (SRP) | A class/module should have only one reason to change | The handler had two responsibilities: "request processing" and "input validation" — this change resolves that |
| Extract Function | Refactoring technique that moves code into a new function/module | Applied to extract the validator module |

## Background (Why)
The auth handler exceeded 200 lines with validation logic and request processing
mixed together. Validation could not be unit-tested independently and relied on
E2E tests.

## Change Details (What & How)

### Change Point 1: Validation Function Extraction

**Before:**
```typescript
// auth/handler.ts (excerpt)
export async function handleLogin(req: Request) {
  // Validation logic directly embedded
  if (!req.body.email || !req.body.email.includes('@')) {
    throw new ValidationError('Invalid email');
  }
  if (!req.body.password || req.body.password.length < 8) {
    throw new ValidationError('Password too short');
  }
  // ... authentication processing
}
```

**After:**
```typescript
// auth/validator.ts (new)
export function validateLoginInput(input: LoginInput): ValidationResult {
  const errors: string[] = [];
  if (!input.email?.includes('@')) errors.push('Invalid email');
  if (!input.password || input.password.length < 8) errors.push('Password too short');
  return errors.length ? { valid: false, errors } : { valid: true, errors: [] };
}

// auth/handler.ts (after)
import { validateLoginInput } from './validator';

export async function handleLogin(req: Request) {
  const validation = validateLoginInput(req.body);
  if (!validation.valid) throw new ValidationError(validation.errors);
  // ... authentication processing only
}
```

**Learning Point:**
> Separating validation logic achieves: (1) simpler handler tests,
> (2) independent unit testing of validation rules, (3) reusability
> from other endpoints. Extract Function is the most fundamental
> refactoring technique.

## Design Decisions (Why This Way)

### Adopted Approach
Pure function validator. No external dependencies — input→output transformation only.

### Alternatives Considered
| Alternative | Summary | Rejection Reason |
|-------------|---------|-----------------|
| Class-based validator | DI rules into Validator class | Over-engineering for this scale |
| Zod schema | Declarative validation with zod | Prioritized consistency with existing code |

## Anti-patterns (Why Not)

### ❌ Moving validation to middleware
An express middleware approach was considered, but route-specific validation
should stay close to the handler. Middleware is for generic checks
(auth tokens, etc.).
```

---

## Example 2: Glossary Output

### Input
```
Target: PR #42 "feat(payment): add Stripe webhook handling"
Audience: beginner
Format: glossary
```

### Output (excerpt)

```markdown
# PR #42 Stripe Webhook Integration — Glossary

| Term | Category | Definition | Usage in Code | Related Terms |
|------|----------|-----------|--------------|---------------|
| Webhook | concept | A mechanism where an external service sends HTTP POST requests to your application's URL when events occur | `app.post('/webhook/stripe', handleStripeWebhook)` | Callback, Event |
| Idempotency | concept | The property that performing the same operation multiple times produces the same result. Important because webhooks may be delivered multiple times | `if (await isProcessed(event.id)) return;` | At-least-once delivery |
| Webhook Signature | security | A cryptographic signature to verify that a request comes from the legitimate sender | `stripe.webhooks.constructEvent(body, sig, secret)` | HMAC, Payload verification |
| Event Type | api | The kind of event notified via webhook (payment completed, refund, etc.) | `switch(event.type) { case 'payment_intent.succeeded': ... }` | Event, Payload |
```

---

## Example 3: Decision Record

### Input
```
Target: branch feature/cache-layer commits
Audience: advanced
Format: decision_record
```

### Output (excerpt)

```markdown
# ADR: Redis vs In-Memory Cache Selection

## Status
Accepted

## Context
API response time reached p99 of 800ms, with DB queries as the primary cause.
A cache layer is needed. Single-instance deployment means distributed cache
is not currently necessary.

## Options Considered

### Option 1: Redis
- **Pros:** Data persistence, TTL management, future scale-out support
- **Cons:** Operational cost increase, network latency, infrastructure dependency

### Option 2: node-cache (in-memory)
- **Pros:** Zero operational cost, minimal latency, no dependencies
- **Cons:** Lost on process restart, memory limits, no scale-out

### Option 3: LRU Cache (custom)
- **Pros:** Full control, no dependencies
- **Cons:** Reinventing the wheel, edge case handling cost

## Decision
Adopted node-cache. Currently single-instance, prioritizing minimal operational cost.
Introduced CacheInterface abstraction to facilitate future Redis migration.

## Consequences
- p99 latency: 800ms → 120ms (85% improvement)
- Memory usage: +50MB (within acceptable range)
- Migration path: Simply swap CacheInterface implementation to RedisAdapter
```
