# Cognitive Load Anti-Patterns

Purpose: Reduce avoidable user effort by controlling choice count, information density, recall burden, disclosure depth, and navigation complexity.

## Contents

- Load types
- CL anti-patterns
- Hick and Miller application
- Progressive disclosure failures
- Quality checklist

## Load Types

- Intrinsic load: complexity of the domain itself
- Extraneous load: avoidable UI burden introduced by the design
- Germane load: useful effort that helps the user understand and progress

Palette should reduce extraneous load first.

## CL Anti-Patterns

| ID | Anti-pattern | Signal | Fix |
|----|--------------|--------|-----|
| `CL-01` | Too many choices | too many options on one screen | keep primary choices around `5-7` where possible |
| `CL-02` | Information density overload | scanning feels impossible | improve whitespace and hierarchy |
| `CL-03` | Inconsistent UI patterns | each screen behaves differently | standardize with the design system |
| `CL-04` | Recall-heavy design | user must remember data between steps | prefer recognition over recall |
| `CL-05` | Ambiguous microcopy | user knows something failed but not why | use `What + Why + How` |
| `CL-06` | Everything shown at once | first-use screen is overwhelming | apply progressive disclosure |
| `CL-07` | Too-deep hierarchy | core task takes `4+` clicks | flatten or add shortcuts |
| `CL-08` | Visual noise | decoration steals attention | keep ornament meaningful and sparse |

## Hick And Miller Application

- top-level navigation: aim for `5-7` items
- dropdown with `20+` items: add search
- page with `3+` peer CTAs: clarify one primary action
- multi-step form with `7+` steps: reconsider grouping or flow structure
- chunk long numeric content into smaller groups

## Progressive Disclosure Failures

- important features hidden too deeply
- no middle layer between basic and advanced
- no “show all” path for expert users
- expanded content loses context or current position

## Quality Checklist

- the page purpose is clear in seconds
- one primary action stands out
- the user does not need to memorize prior-step data
- advanced controls are available without overwhelming first-time users
