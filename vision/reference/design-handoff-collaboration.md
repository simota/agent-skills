# Design-to-Development Handoff & Collaboration

Purpose: Use this file when delegating design work to implementation agents or checking whether a design is ready for development.

Contents:
- handoff anti-patterns
- token sync pipeline
- `Ready for Dev` checklist
- collaboration model

## Handoff Anti-patterns (`HO-01` to `HO-06`)

| ID | Anti-pattern | Risk | Response |
|----|--------------|------|----------|
| `HO-01` | wall-over-the-wall handoff | unbuildable designs and rework | involve developers early |
| `HO-02` | token-name mismatch | design/code drift | align Figma Variables and code tokens |
| `HO-03` | vague specs | interpretation drift | specify values, states, variants, edge cases |
| `HO-04` | happy-path-only design | missing empty/error/loading states | require all key states |
| `HO-05` | undefined responsive behavior | mobile breakage | define all breakpoints |
| `HO-06` | unspecified interaction states | developer guesswork | define hover, focus, active, disabled, and motion |

## Token Sync Pipeline

```text
Figma Variables -> Tokens Studio / Style Dictionary -> CI/CD -> Code
```

Core rule: keep one source of truth for token names and mappings.

## `Ready for Dev` Checklist

- tokens are consistent across all components
- all interaction states are designed
- all breakpoints are defined
- empty, error, loading, and skeleton states are covered
- accessibility requirements are explicit
- animation specs include duration, easing, trigger, and reduced-motion handling
- design intent and technical notes are documented
- related tickets and docs are linked

## Collaboration Model

- involve developers during wireframes, not only after design signoff
- use shared language for token, component, and state names
- keep asynchronous review records in durable tools, not only chat
- treat Storybook and design-system docs as living references

Delegation block:
- if `Ready for Dev` is incomplete, do not delegate implementation work
