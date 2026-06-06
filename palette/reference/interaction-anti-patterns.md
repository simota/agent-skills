# Interaction Anti-Patterns

Purpose: Catch high-friction interaction mistakes before they become silent failures, inaccessible controls, or high-anxiety destructive flows.

## Contents

- IA anti-patterns
- Component-specific failures
- Feedback timing rules

## IA Anti-Patterns

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `IA-01` | Hide and hover | actions appear only on hover | keep actions visible or provide a consistent menu |
| `IA-02` | Small click target | target is below `44x44px` | expand target size |
| `IA-03` | Over-engineered interaction | simple task requires complex gesture or animation | match established mental models |
| `IA-04` | No batch action | repeated list actions must be done one by one | add multi-select and bulk actions |
| `IA-05` | Ambiguous labels | `Click here`, `Details`, `OK` | use verb + object |
| `IA-06` | Unlabeled controls | checkbox/radio/input has no associated label | connect real labels |
| `IA-07` | Happy-path-only design | no empty/error/loading/offline state | design the full state set |
| `IA-08` | UI bloat | too many controls on one screen | apply 80/20 and progressive disclosure |
| `IA-09` | Silent fail | only `console.error`, no user feedback | add toast, inline alert, or status feedback |
| `IA-10` | No destructive confirmation | delete/reset runs immediately | add confirm or soft delete + undo |

## Component-Specific Failures

- Modal: no focus trap, no `Esc`, nested modal stacks
- Tooltip: hides essential information or relies on hover only
- Carousel: auto-rotates or ignores reduced-motion preferences
- Dropdown: more than `7+` items without search, poor keyboard support

## Feedback Timing Rules

| Delay | UX requirement |
|-------|----------------|
| `0-100ms` | instant visual acknowledgment |
| `100-300ms` | light feedback recommended |
| `300ms-1s` | clear loading indicator |
| `1s-10s` | progress plus cancel when possible |
| `10s+` | background processing plus completion notification |
