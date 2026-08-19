# Template Scope Selection Guide

Purpose: Use this file when choosing `Full`, `Standard`, or `Lite`, or when the scope must be escalated safely.

## Contents

- Scope table
- Decision rules
- Complexity indicators
- Escalation rules

## Scope Table

| Scope | Requirement count | `L0` | `L1` | `L2` | `L3` | Typical effort |
|---|---:|---|---|---|---|---|
| `Full` | `12+` | Full | Full | all three sections | full BDD + full traceability | `2-4 hours` |
| `Standard` | `4-11` | Full | Full | only involved sections | major BDD scenarios | `1-2 hours` |
| `Lite` | `1-3` | Compact | Compact | inline notes only | key scenarios only | `<= 30 minutes` |

## Default Decision Rules

1. New product or major feature -> `Full`
2. Medium feature addition or improvement -> `Standard`
3. Small improvement or bug fix -> `Lite`
4. `3` teams deeply involved -> bias toward `Full` or `Standard`
5. `1-2` teams only -> bias toward `Lite` or `Standard`
6. `5+` stakeholders -> bias toward `Full`

## Complexity Indicators

| Indicator | Low -> `Lite` | Medium -> `Standard` | High -> `Full` |
|---|---|---|---|
| affected screens | `1-2` | `3-5` | `6+` |
| API changes | `0-1` | `2-4` | `5+` |
| database change | none | table change | new table |
| external integration | none | existing API use | new integration |
| user-flow impact | minor edit | new flow | flow redesign |
| stakeholders | `1-2` | `3-4` | `5+` |
| estimated duration | `1-3 days` | `1-3 weeks` | `1 month+` |

## Selection Heuristic

- `2+` High indicators -> `Full`
- else `2+` Medium indicators -> `Standard`
- otherwise -> `Lite`

Use `SCOPE_UNCLEAR` when the indicators are mixed and no safe default is obvious.

## Escalation Rules

- Escalation is always allowed.
- Demotion is avoided once details exist.
- Escalate from `Lite` to `Standard` when new `L2` sections become necessary.
- Escalate from `Standard` to `Full` when all `L2` sections or full traceability become necessary.

## Scope-Specific Traceability

| Scope | Minimum traceability |
|---|---|
| `Full` | complete matrix with all required links |
| `Standard` | `REQ -> AC` plus the involved cross-team links |
| `Lite` | `REQ -> AC` only |
