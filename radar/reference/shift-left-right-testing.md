# Shift-Left/Shift-Right & Production Testing

Purpose: Connect Radar with the full software lifecycle, from early design checks to production feedback loops. Read this when testing strategy depends on observability, QAOps, or production-facing validation.

Contents:

- shift-left maturity
- shift-right test types
- observability-driven prioritization
- chaos and QAOps gates
- synthetic monitoring

## Shift-Left Testing

### Maturity Model

| Level | When Testing Starts | Relative Cost |
|-------|---------------------|---------------|
| L0 | After coding | `×100` |
| L1 | During coding | `×10` |
| L2 | During design | `×1` |
| L3 | During requirements | `×0.1` |

High-value shift-left practices:

- static analysis
- pre-commit hooks
- TDD for unstable logic
- BDD / acceptance criteria for business-critical flows
- contract-first design for APIs

## Shift-Right Testing

| Test Type | Purpose | Risk |
|-----------|---------|------|
| Canary release | Gradual blast-radius control | Low |
| Feature flag rollout | Limited user exposure | Low |
| A/B test | Behavioral comparison | Low |
| Synthetic monitoring | Ongoing health verification | Low |
| Chaos test | Resilience validation | Medium to high |
| Traffic mirroring | Real-request shadow validation | Medium |

## Observability-Driven Testing

Use production signals to shape test priorities.

| Signal | Radar Action | Priority |
|--------|--------------|----------|
| Error-rate spike | Add regression tests immediately | `P0` |
| SLO budget burn `> 50%` | Strengthen related test paths | `P1` |
| New error pattern | Add edge-case tests | `P1` |
| P99 latency degradation | Add performance-aware checks or hand off | `P2` |
| Failure on a rare path | Add long-tail coverage | `P3` |

## Chaos Testing

Chaos experiments should stay explicit and reversible.

Recommended template fields:

- steady-state hypothesis
- injected fault
- blast radius
- rollback trigger
- result and follow-up action

Useful fault candidates:

- network latency
- dependency outage
- CPU load `80%+`
- disk pressure `90%+`
- DNS failure

## QAOps Gates

| Gate | Includes | Budget | Failure Effect |
|------|----------|--------|----------------|
| Gate 1 | lint, type check, unit | `< 2min` | block PR |
| Gate 2 | integration, contract | `< 10min` | block merge |
| Gate 3 | E2E, performance, security | `< 30min` | block deploy |
| Gate 4 | smoke, synthetic, canary | continuous | trigger rollback or incident flow |

## Synthetic Monitoring

| Scenario | Frequency | Example |
|----------|-----------|---------|
| Health check | `1 min` | API ping |
| Critical path | `5 min` | login -> key action -> logout |
| Transaction | `15 min` | payment or checkout flow |
| Global reachability | `30 min` | multi-region probe |

Synthetic monitoring is not a substitute for pre-release E2E. It is the production safety net after release.

## Radar Integration

| Radar Mode | Shift-Left Use | Shift-Right Use |
|------------|----------------|-----------------|
| Default | Add edge-case tests earlier | Feed back production errors into regression coverage |
| FLAKY | Detect nondeterminism early | Compare against production instability signals |
| AUDIT | Catch design-time coverage gaps | Compare test coverage to real production paths |
| SELECT | Auto-select tests from change impact | Prioritize by observed production failures |
