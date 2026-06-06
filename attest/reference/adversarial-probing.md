# Adversarial Probing Catalog

Purpose: Read this when you need probe selection, category coverage, risk assignment, or the `ADVERSARIAL_PROBES` payload.

## Contents

- [Probe contract](#probe-contract)
- [Risk classification](#risk-classification)
- [Probe families](#probe-families)
- [Execution strategy](#execution-strategy)
- [Output format](#output-format)
- [Quality rules](#quality-rules)

## Probe Contract

Adversarial probing searches for what the specification forgot, contradicted, or left unsafe. Run it after extracting criteria and before issuing any final verdict.

### Probe ID Convention

```text
PRB-{category_code}-{NNN}

Category codes:
- BND = Boundary
- OMS = Omission
- CTR = Contradiction
- IMP = Implicit
- NEG = Negative
- CNC = Concurrency
```

Each probe must include:

- `id`
- `category`
- `target_criterion` or affected scope
- `description`
- `spec_gap`
- `risk`
- `suggested_criterion`
- `implementation_status` when implementation evidence exists

## Risk Classification

| Risk | Definition | Effect on verdict |
|------|------------|-------------------|
| `CRITICAL` | Likely data loss, security breach, or system failure | Blocks `CERTIFIED`; requires remediation |
| `HIGH` | Likely user-facing failure or broken workflow | Blocks `CERTIFIED`; remediation plan required |
| `MEDIUM` | Edge-case or expectation gap with clear impact | Report and route for remediation |
| `LOW` | Minor or rare behavioral gap | Document for awareness |

## Probe Families

### Boundary (`BND`)

Use for limits, extremes, and threshold behavior.

| Probe focus | Typical checks | Example gap |
|-------------|----------------|-------------|
| Empty or null input | `null`, empty string, missing field | No required-field behavior specified |
| Numeric boundaries | `0`, negative, max, max+1, rounding | No overflow or precision rule |
| Collection size | empty list, single item, max size | No behavior for zero results |
| Date and time | leap day, timezone edge, midnight crossover | No timezone definition |
| Encoding and files | Unicode extremes, zero-byte file, oversized file | No invalid-file handling |

### Omission (`OMS`)

Use for behavior the spec forgot to mention.

| Probe focus | Typical checks | Example gap |
|-------------|----------------|-------------|
| Error messaging | distinct failure paths | No error text or error code rule |
| Loading and empty states | loading spinner, zero results | No empty-state behavior |
| Timeout and partial failure | slow dependency, batch partial success | No retry or recovery rule |
| Undo and notification | user reversal, event notice | No rollback or notification rule |
| Auditability | logging, tracking, audit trail | No recordkeeping requirement |

Omission review prompts:

1. What happens when the feature fails?
2. What states can each entity enter?
3. What happens before and after the user action?
4. What happens if the dependency is unavailable?

### Contradiction (`CTR`)

Use for conflicting requirements inside one spec or across related specs.

| Probe focus | Typical conflict |
|-------------|------------------|
| Cross-feature behavior | One feature allows X, another forbids X |
| Priority and UX | "Simple" conflicts with "cover all edge cases" |
| Permissions | Global admin power conflicts with local restriction |
| Data model | Create requires a field, update makes it optional |
| Timing model | Real-time promise conflicts with batch-only process |
| Security vs convenience | Seamless flow conflicts with strict re-authentication |

Contradiction review steps:

1. Group requirements by shared entity, workflow, or permission.
2. Compare action, timing, and state assumptions.
3. Flag any requirement that negates or weakens another.
4. Keep the probe open until the contradiction is clarified or resolved.

### Implicit (`IMP`)

Use for hidden assumptions that implementations often depend on.

| Probe focus | Typical assumption |
|-------------|--------------------|
| Time and locale | server timezone, locale-specific formatting |
| Auth state | user is already logged in or verified |
| Network conditions | always-online or low-latency behavior |
| Ordering and idempotency | stable sort order, safe retry |
| Scale and retention | data size, rate limits, retention period |
| Platform support | browser, device, or OS assumptions |

Assumption prompts:

1. Who is assumed to use this?
2. Where is it assumed to run?
3. When does ordering or timing matter?
4. How much volume or scale is assumed?
5. What breaks if the assumption is false?

### Negative (`NEG`)

Use for forbidden, invalid, or unauthorized behavior.

| Probe focus | Typical checks |
|-------------|----------------|
| Invalid input | malformed JSON, injection payloads, missing fields |
| Unauthorized access | other user's data, admin-only endpoint |
| Invalid transitions | impossible workflow steps or expired resources |
| Duplicate or out-of-order actions | double submit, retry before completion |
| Resource exhaustion | too many requests, full disk, OOM |
| Integrity violations | deleting parent with active children |

### Concurrency (`CNC`)

Use for race conditions, ordering, and parallel activity.

| Probe focus | Typical checks |
|-------------|----------------|
| Simultaneous updates | two users edit the same resource |
| Read-after-write | stale read immediately after mutation |
| Double submission | rapid repeat action |
| Cache or queue ordering | stale cache, reordered messages |
| Lost updates | last-write-wins without merge rule |
| Session collisions | same user on multiple devices |

## Execution Strategy

### Priority Order

1. `CTR` because contradictions can invalidate the entire spec.
2. `OMS` because missing requirements become production defects.
3. `NEG` because validation and authorization gaps are high-risk.
4. `BND` because data limits often break integrity.
5. `IMP` because hidden assumptions create latent failures.
6. `CNC` because concurrency is narrower but expensive when missed.

### Minimum Probes per Mode

| Mode | Minimum probes | Coverage rule |
|------|----------------|---------------|
| `FULL` | `12` | Cover all 6 categories |
| `ADVERSARIAL` | `24` | Cover all 6 categories with deeper variants |
| `AUDIT` | `6` | Focus on `OMS` and `CTR` |
| `EXTRACT` | `0` | No probing |

### Review Sequence

1. Map each probe to a criterion or spec section.
2. Verify the claimed gap against the actual spec text.
3. Assign risk based on business, security, and integrity impact.
4. Add a measurable `suggested_criterion`.
5. Feed open probes into the compliance report and remediation plan.

## Output Format

### Probe Template

```yaml
PROBE:
  id: PRB-BND-001
  category: Boundary
  target_criterion: AC-XXX-001
  description: "Empty email input on login form"
  spec_says: "User submits email and password"
  spec_gap: "No specification for empty email handling"
  expected_behavior: "Validation error displayed"
  risk: MEDIUM
  suggested_criterion: "When email field is empty, display 'Email is required' error"
```

### `ADVERSARIAL_PROBES`

```yaml
ADVERSARIAL_PROBES:
  total: 18
  by_category:
    boundary: 4
    omission: 5
    contradiction: 1
    implicit: 3
    negative: 3
    concurrency: 2
  by_risk:
    critical: 1
    high: 4
    medium: 8
    low: 5
  probes:
    - id: PRB-OMS-003
      category: Omission
      target: AC-LOGIN-001
      description: "Login spec does not mention account lockout"
      spec_gap: "No lockout mechanism specified after failed attempts"
      risk: CRITICAL
      suggested_criterion: "After 5 failed login attempts, lock the account for 30 minutes"
      implementation_status: NOT_IMPLEMENTED
```

## Quality Rules

- Do not keep a probe if the spec already addresses the concern.
- Do not invent a suggested criterion that is unrelated to the existing business intent.
- Treat unresolved `CTR` probes as release-blocking until clarified.
- Prefer one precise probe over several overlapping weak probes.
- Keep probes measurable so they can become criteria or tests immediately.
