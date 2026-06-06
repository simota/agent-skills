# Compliance Report

Purpose: Read this when issuing a final verdict, assembling `## Attest 適合レポート`, calculating traceability coverage, or generating `ATTEST_TO_*_HANDOFF` payloads.

## Contents

- [Verdict contract](#verdict-contract)
- [Report structure](#report-structure)
- [Traceability matrix](#traceability-matrix)
- [Handoff payloads](#handoff-payloads)
- [Quality rules](#quality-rules)

## Verdict Contract

Final outputs are rendered in Japanese. The rules below define the decision logic and required report contents.

| Verdict | Required condition set |
|---------|------------------------|
| `CERTIFIED` | Every `CRITICAL` criterion is `PASS`; every `HIGH` criterion is `PASS` or `NOT_TESTED` with a runtime plan; no open `CRITICAL` adversarial probes; traceability coverage `>= 90%` |
| `CONDITIONAL` | No `CRITICAL` criterion is `FAIL`; `<= 3` `HIGH` criteria are `PARTIAL`; remediation plan attached for every non-`PASS` item; remediation timeline specified; no unresolved `CTR` probes |
| `REJECTED` | Any `CRITICAL` criterion is `FAIL`; `> 3` `HIGH` criteria are `FAIL`; unresolved `CTR` probes remain; traceability coverage `< 50%`; or more than `5` unresolved `AMBIGUOUS_FLAG`s remain |

Decision rules:

- `NOT_TESTED` is allowed only when the criterion requires runtime validation and the report includes a runtime plan.
- `CONDITIONAL` and `REJECTED` must include a remediation plan.
- Do not issue `CERTIFIED` if any unresolved contradiction, critical probe, or critical criterion failure remains.

## Report Structure

Keep the section order below exactly.

```text
## Attest 適合レポート
### Summary
### Criteria Summary
### Traceability Matrix
### Findings (by severity)
### Adversarial Probe Results
### Specification Quality Feedback
### Remediation Plan (for CONDITIONAL/REJECTED)
### BDD Scenarios (generated)
```

### Section Requirements

| Section | Must include |
|---------|--------------|
| `### Summary` | Specification source, implementation scope, mode, final verdict, date |
| `### Criteria Summary` | Counts by priority and verdict |
| `### Traceability Matrix` | Criterion ID, priority, spec section, implementation mapping, tests, verdict, coverage percentage |
| `### Findings (by severity)` | `CRITICAL` first, then `HIGH`, then `MEDIUM/LOW`; each finding includes verdict, method, evidence, impact, and assigned agent |
| `### Adversarial Probe Results` | Open and closed probe summary with risk and spec gap |
| `### Specification Quality Feedback` | Ambiguities, omissions, contradictions, and recommended improvements |
| `### Remediation Plan (for CONDITIONAL/REJECTED)` | Action, assigned agent, priority, estimate or timeline |
| `### BDD Scenarios (generated)` | Total scenario count and category breakdown |

### Minimal Skeleton

```markdown
## Attest 適合レポート

### Summary

| Field | Value |
|-------|-------|
| Specification | [spec path/name] |
| Implementation | [files/modules list] |
| Mode | FULL / EXTRACT / AUDIT / ADVERSARIAL |
| Verdict | CERTIFIED / CONDITIONAL / REJECTED |
| Date | YYYY-MM-DD |

### Criteria Summary

[Counts by verdict and priority]

### Traceability Matrix

[Criterion-to-implementation-to-test mapping]

### Findings (by severity)

[Grouped findings]

### Adversarial Probe Results

[Probe summary]

### Specification Quality Feedback

[Ambiguities, omissions, contradictions]

### Remediation Plan (for CONDITIONAL/REJECTED)

[Required when verdict is not CERTIFIED]

### BDD Scenarios (generated)

[Scenario totals and file reference]
```

## Traceability Matrix

The traceability matrix maps:

```text
Specification criterion -> implementation file:line -> test file:line
```

### Coverage Calculation

```text
Traceability Coverage = Criteria with implementation mapping / Total criteria x 100

Example:
- Total criteria: 12
- Criteria mapped to implementation: 10
- Criteria mapped to tests: 8
- Implementation coverage: 10 / 12 = 83%
- Test coverage: 8 / 12 = 67%
```

### Coverage Thresholds

| Coverage | Assessment |
|----------|------------|
| `>= 90%` | Excellent; supports `CERTIFIED` |
| `70-89%` | Good; usually supports `CONDITIONAL` |
| `50-69%` | Insufficient; remediation required |
| `< 50%` | Unacceptable; triggers `REJECTED` |

For L1/L2/L3 coverage details and bidirectional analysis, read `reference/traceability-advanced.md`.

## Handoff Payloads

### `ATTEST_TO_BUILDER_HANDOFF`

```yaml
ATTEST_TO_BUILDER_HANDOFF:
  verdict: CONDITIONAL
  violations:
    - criterion_id: AC-XXX-002
      priority: CRITICAL
      gap: "Account lockout not implemented"
      spec_reference: "login-spec.md:L45"
      suggested_location: "src/controllers/auth.ts"
    - criterion_id: AC-XXX-005
      priority: HIGH
      gap: "Error message format does not match the spec"
      current: "Generic error returned"
      expected: "Specific error with error code"
  bdd_scenarios: "generated/login.feature"
```

### `ATTEST_TO_RADAR_HANDOFF`

```yaml
ATTEST_TO_RADAR_HANDOFF:
  bdd_scenarios:
    file: "generated/login.feature"
    total: 42
    by_priority:
      critical: 15
      high: 12
      medium: 10
      low: 5
  not_tested_criteria:
    - criterion_id: AC-XXX-003
      reason: "Requires runtime timing verification"
      suggested_test_type: "integration"
    - criterion_id: AC-XXX-008
      reason: "Requires browser rendering"
      suggested_test_type: "e2e"
```

### `ATTEST_TO_WARDEN_HANDOFF`

```yaml
ATTEST_TO_WARDEN_HANDOFF:
  verdict: CERTIFIED
  criteria_summary:
    total: 12
    pass: 10
    not_tested: 2
  traceability_coverage: 92%
  adversarial_probes:
    total: 18
    critical_open: 0
    high_open: 1
  spec_quality: GOOD
  recommendation: "Spec compliance verified. Proceed to V.A.I.R.E. evaluation."
```

### `ATTEST_TO_SCRIBE_HANDOFF`

```yaml
ATTEST_TO_SCRIBE_HANDOFF:
  ambiguity_flags:
    - criterion_id: AC-XXX-005
      type: UNMEASURABLE
      suggestion: "Define response time threshold"
  omissions:
    - category: ERROR_HANDLING
      description: "No specification for rate limiting behavior"
    - category: EDGE_CASE
      description: "Behavior when session expires mid-action not specified"
  contradictions:
    - criteria: [AC-XXX-003, AC-XXX-009]
      description: "AC-003 says allow retry, AC-009 says lock immediately"
```

## Quality Rules

- Use report prose to explain evidence and impact; do not change the verdict rules in prose.
- Every finding must map back to a criterion, probe, or explicit spec gap.
- If the report uses `NOT_TESTED`, include the runtime plan or handoff target.
- If the report uses `AMBIGUOUS`, include the clarification or rewrite suggestion.
- Keep verdict logic deterministic and separate from explanatory language.
