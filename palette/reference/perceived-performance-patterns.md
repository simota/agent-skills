# Perceived Performance Patterns

Purpose: Improve perceived speed and confidence by choosing the right loading pattern, optimistic strategy, and feedback timing.

## Contents

- PP anti-patterns
- Skeleton vs spinner vs progress bar
- Optimistic UI rules
- Feedback timing

## PP Anti-Patterns

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `PP-01` | Full-page spinner | loading blocks the whole content area | use skeletons for known layouts |
| `PP-02` | Layout shift on load | content jumps after data arrives | reserve layout dimensions in advance |
| `PP-03` | Skeleton on tiny interactive elements | fake buttons or labels invite failed taps | hide or disable small elements instead |
| `PP-04` | Static placeholder | placeholder feels broken after `1s+` | add pulse or wave animation |
| `PP-05` | Over-aggressive optimistic UI | high-risk action rolls back awkwardly | use optimistic UI only when failure rate is `<1%` and recovery is natural |
| `PP-06` | No immediate feedback | click produces no visible response within `100ms` | add instant state change or acknowledgment |

## Skeleton vs Spinner vs Progress Bar

| Pattern | Best for |
|---------|----------|
| Skeleton | structured content loads |
| Spinner | short action-level waits |
| Progress bar | long or measurable work |
| Optimistic UI | low-risk, reversible state change |

Rules:

- avoid skeletons for loads shorter than about `300ms`
- do not use optimistic UI for billing, destructive actions, or high-integrity updates

## Optimistic UI Rules

Use when:

- failure rate is very low
- rollback is understandable
- no user data integrity risk exists

Avoid for:

- payment and billing
- destructive create/delete flows
- multi-user integrity-sensitive actions

## Feedback Timing

| Delay | Guidance |
|-------|----------|
| `0-100ms` | instant acknowledgment |
| `100ms-1s` | short feedback state |
| `1s-10s` | loading/progress plus cancel when possible |
| `10s+` | background job plus completion notification |
