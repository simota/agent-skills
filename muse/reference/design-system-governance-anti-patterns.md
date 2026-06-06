# Design System Governance And Scaling Anti-Patterns

Purpose: Use this reference when adoption stalls, ownership is unclear, docs drift, or the system is scaling across multiple teams or products.

## Contents

- Adoption failures
- Governance drift
- Governance models
- Scaling quality gates
- Adoption practices

## Adoption Failures

| ID | Anti-pattern | Signal | Correction |
|----|--------------|--------|-----------|
| `DS-01` | Over-engineering | Building many components before demand exists; usage `< 10%` or weak reuse | Build from real need; prioritize items with likely use across `3+ products` |
| `DS-02` | No owner | No clear maintainer or RACI | Assign ownership and operating cadence |
| `DS-03` | Top-down enforcement | Teams avoid or fork the system | Collect feedback and co-design changes |
| `DS-04` | Documentation sprawl | Docs, code, and design live in separate truths | Use a single source of truth such as Storybook plus code |
| `DS-05` | Complexity mismatch | Excessively abstract APIs or configuration | Keep the `80%` path simple and make the rest extensible |
| `DS-06` | UI library mindset | The system is treated as components only | Position it as shared infrastructure across design and engineering |

## Governance Drift

| ID | Drift pattern | Signal | Guardrail |
|----|--------------|--------|-----------|
| `Drift-01` | Variant drift | `10+ variants` around one component family | Consolidate and document the supported set |
| `Drift-02` | Ownership drift | No decisions, no roadmap | Restore owner, cadence, and decision log |
| `Drift-03` | Documentation drift | Last update `> 1 sprint` ago | Refresh docs with implementation changes |
| `Drift-04` | Adoption drift | Teams bypass the system or usage falls `< 10%` | Audit reasons, reduce friction, fix missing coverage |
| `Drift-05` | Version / quality drift | Breaking changes land informally or stories drift from code | Reconnect lifecycle, semver, stories, and code review gates |

## Governance Models

| Model | Best fit | Risk |
|------|----------|------|
| Centralized | Early-stage or regulated products | Bottlenecks |
| Federated | Multi-team product orgs | Drift without strong rules |
| Hybrid | Most scaling teams | Requires clear ownership and review boundaries |

## Scaling Quality Gates

- Documentation currency `< 1 sprint`.
- Token coverage `95%+`.
- Dark mode coverage `100%`.
- Component adoption and ownership are visible.
- Stable token changes have lifecycle, semver, and migration notes.

## Decision Framework

Use this when deciding whether a new token, component, or governance rule belongs in the system:

1. Is there repeated demand?
2. Does it support `3+ products` or a clearly shared domain?
3. Is ownership explicit?
4. Is documentation colocated with implementation?
5. Is the API simpler for the `80%` case?
6. Does it reuse existing tokens instead of inventing new primitives?
7. Does it preserve accessibility and dark mode?
8. Is lifecycle and semver impact clear?
9. Are stories/tests/docs updated together?
10. Is removal or consolidation easier than indefinite preservation?

## Adoption Practices

- Measure real usage, not only component count.
- Keep docs colocated with implementation.
- Encourage contribution with simple intake and review rules.
- Remove or merge low-value components instead of preserving dead surface area.
