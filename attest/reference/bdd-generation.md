# BDD Scenario Generation

Purpose: Read this when turning `AC-*` criteria into `SC-*` scenarios, checking scenario coverage by priority, or validating Given/When/Then quality.

For Gherkin block-element syntax (Feature / Background / Scenario / Scenario Outline / Examples / Tags / Steps), see `gherkin-authoring.md` § Gherkin Anatomy. This file focuses on **scenario generation from acceptance criteria** — coverage minimums by priority, scenario types (HP/NP/BP/EP), and generation anti-patterns.

## Contents

- [Generation rules](#generation-rules)
- [Given/When/Then structure](#givenwhenthen-structure)
- [Scenario templates by category](#scenario-templates-by-category)
- [Coverage matrix](#coverage-matrix)
- [Output format](#output-format)
- [Anti-patterns](#anti-patterns)
- [Quality checklist](#quality-checklist)

## Generation Rules

### Core Principle

Every acceptance criterion produces at least:
1. Happy path
2. Negative path
3. Edge or boundary path

### Scenario ID Convention

```text
SC-{criterion_id}-{type}-{NNN}

Types:
  HP = Happy Path
  NP = Negative Path
  BP = Boundary Probe
  EP = Edge / Error Path
```

## Given/When/Then Structure

### Given

- Establish the starting state.
- Include roles, data state, or system configuration when relevant.
- Prefer concrete examples over abstract placeholders.

```gherkin
Given a registered user with email "user@example.com" and role "admin"
```

### When

- One primary action per scenario.
- Include the relevant input values.
- Describe the business action, not incidental UI clicks.

```gherkin
When the user submits the login form with correct credentials
```

### Then

- Use observable, verifiable outcomes.
- Include concrete status codes, values, or state changes when possible.
- Add secondary `And` clauses only when they describe required outcomes.

```gherkin
Then the HTTP response status is 200
And the user is redirected to "/dashboard"
```

## Scenario Templates by Category

### Happy Path

```gherkin
@happy-path @{criterion_id}
Scenario: {Business rule succeeds}
  Given {valid preconditions}
  When {the primary action with valid inputs}
  Then {the successful outcome}
```

### Negative Path

```gherkin
@negative @{criterion_id}
Scenario: {Business rule rejects invalid input}
  Given {preconditions}
  When {the action with invalid or unauthorized input}
  Then {the expected rejection}
  And {state remains unchanged if required}
```

### Boundary Probe

```gherkin
@boundary @{criterion_id}
Scenario: {Boundary value handling}
  Given {boundary preconditions}
  When {the action with boundary input}
  Then {the expected boundary behavior}
```

### Edge / Error Path

```gherkin
@edge-case @{criterion_id}
Scenario: {Unusual but valid situation}
  Given {edge-condition preconditions}
  When {the action under edge conditions}
  Then {the graceful outcome}
```

### Must-Keep Example

```gherkin
# AC-LOGIN-001: Valid credentials grant access
Scenario: Successful login with valid credentials
  Given a registered user with email "user@example.com"
  And the user has a valid password
  When the user submits the login form with correct credentials
  Then the user is redirected to the dashboard
  And a session token is issued

Scenario: Login failure with invalid password
  Given a registered user with email "user@example.com"
  When the user submits the login form with an incorrect password
  Then an error message "Invalid credentials" is displayed
  And no session token is issued

Scenario: Login with boundary email length
  Given a registered user with a 254-character email
  When the user submits the login form with correct credentials
  Then the user is redirected to the dashboard
```

## Coverage Matrix

```yaml
SCENARIO_COVERAGE:
  criterion_id: AC-LOGIN-001
  criterion_text: "Valid credentials grant access"
  scenarios:
    happy_path: 1
    negative: 2
    boundary: 1
    edge_case: 0
  total: 4
  coverage_verdict: SUFFICIENT
```

### Minimum Coverage Requirements

| Priority | Min scenarios | Required types |
|----------|---------------|----------------|
| `CRITICAL` | `5` | `HP(1)` + `NP(2)` + `BP(1)` + `EP(1)` |
| `HIGH` | `3` | `HP(1)` + `NP(1)` + `BP(1)` |
| `MEDIUM` | `2` | `HP(1)` + `NP(1)` |
| `LOW` | `1` | `HP(1)` |

Coverage verdict: `SUFFICIENT` when the minimum requirement is met or exceeded.

## Output Format

```yaml
BDD_SCENARIOS:
  spec_source: "docs/login-spec.md"
  total_criteria: 12
  total_scenarios: 42
  scenarios_by_type:
    happy_path: 12
    negative: 15
    boundary: 10
    edge_case: 5
  coverage_verdict: SUFFICIENT
  gherkin_file: "generated/login.feature"
```

## Anti-Patterns

| Code | Anti-pattern | Prevention |
|------|--------------|------------|
| `AP-001` | Retrospective scenarios | Generate scenarios before or during implementation, not after |
| `AP-002` | Isolated authoring | Use collaborative refinement for ambiguous specs |
| `AP-003` | BDD treated only as QA | Keep scenarios in business language |
| `AP-004` | Incidental details | Focus on outcomes, not UI click sequences |
| `AP-005` | Multiple rules per scenario | Enforce one business rule per scenario |
| `AP-006` | Poor titles | Use criterion ID + business-rule summary |
| `AP-007` | Given/When/Then mixing | Keep state in `Given`, action in `When`, result in `Then` |
| `AP-008` | Over-specification | Stop at priority-based minimums unless risk requires more |
| `AP-009` | UI-focused writing | Describe user intent and business behavior |
| `AP-010` | Missing negative coverage | Require at least one negative scenario for every `CRITICAL` / `HIGH` criterion |

## Quality Checklist

- [ ] Scenarios were generated before or during implementation
- [ ] One scenario covers one business rule
- [ ] Language is business-facing, not implementation-facing
- [ ] `Given` = state, `When` = one action, `Then` = verifiable result
- [ ] Titles describe the business purpose clearly
- [ ] Negative and boundary coverage is present where required
- [ ] Scenario count satisfies priority-based minimums
