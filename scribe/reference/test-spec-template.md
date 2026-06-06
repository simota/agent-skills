# Test Specification Template

Purpose: Use this file for test planning, case design, traceability, execution status, and compact BDD-style specs.

Contents:

- full test specification template
- quick test spec
- Gherkin template
- quality checklist

## Template

```markdown
# Test Specification: [Feature Name]

## Document Info
| Field | Value |
|-------|-------|
| Version | v0.1 |
| Status | Draft |
| Audience | QA, Dev |
| Related Requirements | [REQ/FR links] |

## Change History
| Date | Version | Author | Change |
|------|---------|--------|--------|

## 1. Scope
- in-scope behavior
- out-of-scope behavior

## 2. Test Strategy
- unit
- integration
- E2E
- manual only if justified

## 3. Test Cases
### Positive Tests
| ID | Requirement | Scenario | Expected Result |
|----|-------------|----------|-----------------|
| `TC-001` | `FR-001` | valid login | token returned |

### Negative Tests
| ID | Requirement | Scenario | Expected Result |
|----|-------------|----------|-----------------|
| `TC-N001` | `FR-001` | wrong password | `AUTH_002` |

### Boundary Tests
| ID | Requirement | Scenario | Expected Result |
|----|-------------|----------|-----------------|
| `TC-B001` | `FR-001` | password length = 8 | accepted |

### Accessibility Tests
| ID | Requirement | Scenario | Expected Result |
|----|-------------|----------|-----------------|
| `TC-A001` | `NFR-A001` | screen reader login flow | labels announced |

## 4. Test Data
### Valid Data Set
- [fixture or seed]

### Invalid Data Set
- malformed email
- wrong password

## 5. Environment And Setup
- environment
- prerequisites
- mocks or external dependencies

## 6. Execution Notes
### 6.1 Risks
- [risk]

### 6.2 Escalation Path
- [who to contact on failure]

### 6.3 Data Setup Scripts
- [script or process]

## 7. Traceability Matrix
| Requirement | Test Cases | Status |
|-------------|------------|--------|
| `FR-001` | `TC-001`, `TC-N001` | Ready |
| `NFR-P001` | `TC-P001` | Ready |

## 8. Test Execution
| Test Case | Status | Notes |
|-----------|--------|-------|
| `TC-001` | Not Run | |

## 9. Bugs
| Bug ID | Related Test | Severity | Status |
|--------|--------------|----------|--------|

## 10. Appendix
### A. Test Case Status Definitions
- `Not Run`
- `Pass`
- `Fail`
- `Blocked`
- `Skipped`

### B. Glossary
- [term]
```

## Quick Test Spec (Minimal)

```markdown
# Test Spec: [Feature Name]

## Test Cases
| ID | Type | Scenario | Expected Result |
|----|------|----------|-----------------|
| `TC-001` | Positive | [scenario] | [result] |

## Test Data
- [fixtures]

## Traceability
- `REQ-001` -> `TC-001`
```

## Gherkin Format Template

```gherkin
Feature: [Feature Name]

  Scenario: [Scenario Name]
    Given [precondition]
    When [action]
    Then [result]
    And [additional assertion]
```

## Test Specification Quality Checklist

- [ ] Test types are explicit
- [ ] Positive, negative, and boundary cases exist
- [ ] Test data and setup are documented
- [ ] Expected result is explicit per case
- [ ] Requirements are traceable to tests
- [ ] Status and escalation path are defined
