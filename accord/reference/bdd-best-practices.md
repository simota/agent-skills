# BDD Acceptance Criteria Best Practices

Purpose: Use this file when `L3` scenarios are vague, too technical, or not agreed across teams.

## Contents

- `BDD-01..12`
- Three Amigos
- Quality checklist
- Good and bad examples
- Accord quality gates

## BDD Pitfalls

| ID | Pitfall | Failure mode | Guardrail |
|---|---|---|---|
| `BDD-01` | BDD as QA-only tool | business ownership disappears | treat BDD as a collaboration tool |
| `BDD-02` | Abstract scenario | cannot be verified | require concrete values and observable outcomes |
| `BDD-03` | Over-detailed scenario | turns into a test script | focus on user behavior, not implementation |
| `BDD-04` | DOM-coupled scenario | breaks when UI labels change | write in domain language |
| `BDD-05` | Multiple `When` steps | too many actions in one scenario | one scenario = one user action |
| `BDD-06` | Missing business value | scenario does not justify the behavior | keep the value visible |
| `BDD-07` | No Three Amigos | gaps between teams survive | align across Biz, Dev, and test perspectives |
| `BDD-08` | Stale scenarios | code and spec drift apart | review and update scenarios with the package |
| `BDD-09` | Written after implementation | BDD loses design value | write before implementation |
| `BDD-10` | Uniform template everywhere | format becomes ceremony | adapt while keeping the principles |
| `BDD-11` | No coverage measurement | blind spots remain hidden | track scenario coverage |
| `BDD-12` | AC/DoD confusion | functional criteria and team-wide quality get mixed | keep AC feature-specific |
| `BDD-13` | Scenario Outline overuse | combinatorial explosion slows test suite | use outlines only for true data-driven variants; cap rows at `~8` per outline |
| `BDD-14` | Imperative scenario style | step-by-step UI interaction sequences couple scenarios to interaction flow; break on any UI change even when business logic is unchanged | write declarative scenarios describing business outcomes, not interaction steps |

## Three Amigos

| Role | Accord mapping | Main responsibility |
|---|---|---|
| business | `L2-Biz` voice | explain the why and business rules |
| development | `L2-Dev` voice | explain technical constraints and feasibility |
| test | `L3` voice | challenge edge cases and observability |

Suggested session flow (Example Mapping):

1. place the story on a yellow card
2. capture business rules on blue cards
3. add concrete examples on green cards (each maps to a future scenario)
4. note questions and assumptions on red cards
5. time-box to `25 min`; if red cards dominate, the story needs splitting
6. convert green cards into `Given / When / Then` scenarios after the session

## Quality Checklist

- `Given` describes state, not behavior
- `When` is one user action
- `Then` is observable and testable
- domain language is used instead of UI selectors
- happy path and edge case coverage both exist
- every `AC` links back to at least one `REQ`

## Bad Examples

```gherkin
Given the user is logged in
When they search
Then results are displayed correctly
```

```gherkin
Given the user is on /login
When they click #submit-btn
Then .dashboard-container is visible
```

## Good Examples

```gherkin
Scenario: AC-001 - Prevent ordering an out-of-stock item - Linked: REQ-003
  Given product "Premium Widget" has stock 0
  When the user tries to add "Premium Widget" to the cart
  Then the message "Out of stock" is shown
  And the cart item count stays unchanged
```

```gherkin
Scenario: AC-002 - Apply discount coupon - Linked: REQ-005
  Given the cart total is 10000 JPY
  And coupon "SAVE20" is valid
  When the user applies coupon "SAVE20"
  Then the total updates to 8000 JPY
  And the user sees "20% discount applied"
```

## Accord Quality Gates

- abstract `Then` -> warning
- multiple `When` -> split recommendation
- no `REQ` link -> incomplete scenario
