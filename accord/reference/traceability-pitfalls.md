# Requirements Traceability Pitfalls

Purpose: Use this file when traceability is incomplete, inconsistent, or too expensive for the chosen scope.

## Contents

- `RT-01..08`
- Four-way traceability
- SMART requirement gate
- maintenance rules
- completeness thresholds

## Traceability Pitfalls

| ID | Pitfall | Failure mode | Guardrail |
|---|---|---|---|
| `RT-01` | incomplete requirement | cannot design or test it | keep requirements atomic, unambiguous, and testable |
| `RT-02` | unsynced change | links drift after edits | update the matrix whenever requirements change |
| `RT-03` | inconsistent naming | searching and auditing fail | enforce `REQ-XXX`, `AC-XXX`, and related prefixes |
| `RT-04` | hidden dependency | impact analysis is incomplete | record assumptions and dependencies explicitly |
| `RT-05` | over-structured matrix | maintenance cost explodes | scale the matrix to `Full/Standard/Lite` |
| `RT-06` | manual-only maintenance | errors accumulate | keep verification lightweight and repeatable |
| `RT-07` | one-way trace only | reverse impact is lost | use forward and backward checks |
| `RT-08` | orphan item | no linked requirement or acceptance | run orphan detection |

## Four-Way Traceability

| Direction | Question |
|---|---|
| forward from requirements | is each requirement represented downstream? |
| backward to requirements | does each downstream artifact map back to a requirement? |
| forward from test cases | which requirements do the tests cover? |
| backward to test cases | does each requirement have a testable acceptance path? |

Minimum expectation:

- always keep `REQ -> AC`
- add the other directions as the scope increases

## Scope-Specific Expectation

| Scope | Forward Req->Design | Backward Design->Req | Forward Test->Req | Backward Req->Test |
|---|---:|---:|---:|---:|
| `Full` | required | required | required | required |
| `Standard` | required | recommended | recommended | required |
| `Lite` | optional | optional | optional | required |

## SMART Requirement Gate

Each requirement should be:

- `Specific`
- `Measurable`
- `Attributed`
- `Referenceable`
- `Testable`

## Maintenance Rules

| Event | Required update |
|---|---|
| add `REQ` | add the matrix row and at least a placeholder acceptance link |
| change `REQ` | review linked design and acceptance items |
| remove `REQ` | deprecate or remove linked artifacts and re-check orphans |
| change `AC` | verify the linked `REQ` still matches |
| design change | trace backward to impacted `REQ` and `AC` |

## Completeness Thresholds

`Traceability_Score = Linked_Items / Total_Items * 100`

| Scope | Target |
|---|---:|
| `Full` | `>= 95%` |
| `Standard` | `>= 85%` |
| `Lite` | `>= 70%` |

## Accord Quality Gates

- `Full` and score `< 95%` -> warning
- orphan `REQ` -> add or refine acceptance criteria
- orphan `AC` -> add the linked requirement or remove the criterion
- non-SMART requirement -> refine before approval
