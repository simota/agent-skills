# Diagramming Principles

Purpose: Read this when you need abstraction, density, and review heuristics before drawing.

## Contents

- General principles
- Density thresholds
- Diagram-family heuristics
- Review checklist

## General Principles

- One diagram should answer one primary question.
- Prefer a smaller truthful diagram over a comprehensive unreadable one.
- Choose the lowest abstraction that still serves the audience.
- Title and legend are always required.

## Density Thresholds

| Diagram | Rule |
|---------|------|
| General diagram | `<=20` nodes |
| Sequence | `<=15-20` messages |
| DFD | `3-9` processes |
| C4 | Usually stop at Level 1 or 2 |

## Family Heuristics

- Use sequence diagrams for temporal interaction, not hierarchy.
- Use mind maps for concepts, not runtime flow.
- Use ER diagrams for persistence structure, not service interaction.
- Use journey diagrams for experience progression, not implementation detail.

## Review Checklist

- The scope is explicit
- The abstraction fits the audience
- Labels are concrete
- Density stays within safe limits
- Legend exists
- Accessibility rules are respected
