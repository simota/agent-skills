# Verification Methods

Purpose: Read this when choosing static verification techniques, assigning per-criterion verdicts, formatting evidence, or deciding when to route to runtime verification.

## Contents

- [Verification approach](#verification-approach)
- [Verification methods](#verification-methods)
- [Verdict assignment](#verdict-assignment)
- [Evidence format](#evidence-format)
- [Confidence scoring](#confidence-scoring)
- [Resource allocation guideline](#resource-allocation-guideline)

## Verification Approach

Attest performs static verification. It does not execute the system.

### What Attest Can Verify

| Aspect | Method | Confidence tendency |
|--------|--------|---------------------|
| Feature existence | Code search | `HIGH` |
| Data flow correctness | Logic trace | `MEDIUM` |
| Error handling presence | Error-path review | `HIGH` |
| State transitions | State check | `MEDIUM` |
| API contract shape | Signature matching | `HIGH` |
| Business-rule implementation | Logic trace | `MEDIUM` |
| Configuration compliance | Config inspection | `HIGH` |

### What Requires Runtime Verification

| Aspect | Why static verification fails | Route to |
|--------|-------------------------------|----------|
| Performance thresholds | Requires execution timing | `Bolt` / `Siege` |
| Concurrency behavior | Requires parallel execution | `Specter` |
| Visual rendering | Requires rendered UI | `Voyager` / `Echo` |
| External integrations | Requires live endpoints | `Voyager` |
| UX quality | Requires human or experiential review | `Warden` |

Mark these as `NOT_TESTED` with a runtime verification plan.

## Verification Methods

| Method | Purpose | Typical evidence |
|--------|---------|------------------|
| `CODE_SEARCH` | Confirm an implementation artifact exists | Route, handler, component, or config reference |
| `LOGIC_TRACE` | Verify business-rule ordering and transformations | Call chain or condition chain |
| `STATE_CHECK` | Compare state machine behavior to the spec | Enum, reducer, guard, workflow mapping |
| `ERROR_PATH` | Verify specified failure modes | Error handler, validation, response path |
| `ABSENCE_CHECK` | Confirm no implementation exists | Search locations checked and no relevant hit |

### Must-Keep Absence Pattern

```text
Criterion: AC-LOGIN-007 "Account lockout after 5 failed attempts"
Search locations:
  - src/controllers/auth.ts
  - src/middleware/auth.ts
  - src/models/user.ts
Result:
  No lockout logic found
Verdict:
  FAIL
```

## Verdict Assignment

### Per-Criterion Verdicts

| Verdict | Meaning | Evidence requirement |
|---------|---------|----------------------|
| `PASS` | Implementation fully satisfies the criterion | At least one direct code reference with matching logic |
| `PARTIAL` | Implementation exists but misses required aspects | Code reference plus explicit gap |
| `FAIL` | Implementation contradicts or omits the criterion | Contradiction evidence or confirmed absence |
| `NOT_TESTED` | Static verification is insufficient | Reason plus runtime test recommendation |
| `AMBIGUOUS` | The spec is too vague to judge | Reference to `AMBIGUOUS_FLAG` |

### Decision Flow

```text
1. Can the criterion be verified statically?
   -> No: NOT_TESTED
   -> Yes:
      2. Does implementation evidence exist?
         -> No: FAIL
         -> Yes:
            3. Does it match the specification fully?
               -> Fully: PASS
               -> Partially: PARTIAL
               -> Contradicts: FAIL
```

## Evidence Format

```yaml
EVIDENCE:
  criterion_id: AC-LOGIN-001
  verdict: PASS
  method: CODE_SEARCH + LOGIC_TRACE
  references:
    - file: src/routes/auth.ts
      line: 42
      snippet: "router.post('/api/auth/login', authController.login)"
      relevance: "Endpoint definition matching spec"
    - file: src/controllers/auth.ts
      line: 78-95
      snippet: "async login(req, res) { ... }"
      relevance: "Handler validates email + password"
  gaps: []
  notes: "Implementation matches spec."
```

### Gap Description for `PARTIAL` / `FAIL`

```yaml
EVIDENCE:
  criterion_id: AC-LOGIN-007
  verdict: FAIL
  method: ABSENCE_CHECK
  references: []
  gaps:
    - type: MISSING_IMPLEMENTATION
      description: "Account lockout mechanism not found"
      spec_requirement: "Lock account after 5 failed login attempts"
      searched_locations:
        - src/controllers/auth.ts
        - src/middleware/auth.ts
        - src/models/user.ts
      impact: CRITICAL
  notes: "No login attempt tracking or lockout logic exists in codebase"
```

## Confidence Scoring

| Confidence | Range | Meaning |
|------------|-------|---------|
| `HIGH` | `0.8-1.0` | Direct and unambiguous evidence |
| `MEDIUM` | `0.5-0.8` | Likely correct but requires some reasoning |
| `LOW` | `0.2-0.5` | Indirect evidence or heavy inference |

Rule: when confidence `< 0.5`, mark the result as `NOT_TESTED` with a runtime recommendation.

## Resource Allocation Guideline

| Priority | Effort share | Minimum scope |
|----------|--------------|---------------|
| `CRITICAL` | `40%` | All five methods plus adversarial probing |
| `HIGH` | `30%` | Inspection, logic analysis, and basic probes |
| `MEDIUM` | `20%` | Inspection and lighter probing |
| `LOW` | `10%` | Inspection only |

When scope must be reduced, finish all `CRITICAL` criteria first, then `HIGH`, then sampled `MEDIUM`. Defer `LOW` to `AUDIT` mode before reducing higher priorities.
