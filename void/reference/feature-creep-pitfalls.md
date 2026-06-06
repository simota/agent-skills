# Feature Creep Pitfalls & Scope Management

Purpose: Use this file when Void is evaluating feature growth, zombie functionality, or oversized product scope.

Contents:
- Core causes and detection signals for feature creep
- `90/10` principle and zombie-feature thresholds
- Strategic growth vs creep rules
- Pruning lifecycle, removal flow, and feature-addition gates

## 8 Common Causes

| ID | Cause | Mechanism | Void question |
|----|-------|-----------|---------------|
| `FC-01` | Feedback trap | Every request ships, creating an incoherent set of features | How many users asked for it? |
| `FC-02` | Competitor chasing | Feature mimicry erodes focus | Must we fight on that exact surface? |
| `FC-03` | No product vision | Everything sounds valuable | Does it strengthen the core value proposition? |
| `FC-04` | No usage data | All features are treated as equally important | Is usage actually measured? |
| `FC-05` | FOMO | Trend-driven additions ignore user value | Does this trend matter to our users? |
| `FC-06` | Stakeholder pressure | Authority outruns evidence | Can the impact be quantified? |
| `FC-07` | Sunk-cost fallacy | Prior work is used to justify more work | If starting fresh, would we still build this? |
| `FC-08` | Feature-count illusion | Quantity is mistaken for product value | Did this improve satisfaction or adoption? |
| `FC-09` | AI-accelerated build-rate | AI assistance makes "let's just ship it" cheaper than evaluating it; PR throughput rises `~20%` while incidents per PR rise `~23.5%` (2026 LeadDev / DORA-style data) | Has the success metric and removal criterion been written *before* writing the code? |

### Empirical Anchor

Microsoft's Kohavi et al. found that even with careful up-front analysis, only `~1/3` of shipped features improved the metrics they were designed to improve. Combined with 2026's `~41%` AI-generated code share and the `+23.5%` incidents-per-PR signal above, the default assumption should be that **unvalidated new functionality is more likely to harm than help** the product surface it lands on. Feature-addition gates and pruning lifecycles below are calibrated to that prior.

## Detection Signals

### Product Signals

| Signal | Threshold | Meaning |
|--------|-----------|---------|
| Onboarding completion time | `>30 min` | Product is too broad to grasp quickly |
| Submenu depth | `>2` levels | Information architecture is collapsing |
| "I don't know how to use this" support issue | appears in top 3 problems | Discoverability is poor |
| Release-cycle lengthening | `>1.5x` quarter over quarter | Feature coupling is slowing delivery |

### Delivery Signals

| Signal | Threshold | Meaning |
|--------|-----------|---------|
| New-feature speed drop | `<0.7x` quarter over quarter | Existing scope is dragging velocity |
| Bug-rate increase | `>1.3x` quarter over quarter | Feature interactions are causing instability |
| Test runtime increase | `>2x` quarter over quarter | Test matrix is exploding |
| Rollback rate | `>10%` | Change impact is no longer predictable |

## 90/10 Principle and Zombie Features

Rules:
- Often `90%` of users use only `10%` of features.
- The low-usage majority of features can consume a disproportionate share of maintenance cost.
- Regulatory and security features are exceptions and should not be removed on usage alone.

### Feature Classification

| Class | Usage | Default action |
|-------|-------|----------------|
| `Dead` | `<1%` | immediate `REMOVE` candidate |
| `Zombie` | `1-5%` | consider `REMOVE` or `SIMPLIFY` |
| `Niche` | `5-15%` | keep, but do not expand |
| `Active` | `15-50%` | normal maintenance |
| `Core` | `>50%` | improve before expanding elsewhere |

## Strategic Expansion vs Feature Creep

### Strategic expansion

- Deepens the core value proposition.
- Solves a major pain point for existing users.
- Is backed by usage evidence.
- Preserves product coherence.

### Feature creep

- Expands sideways away from the core.
- Solves "nice to have" requests without evidence.
- Copies competitors without clear strategy.
- Adds confusion and cross-feature dependency.

## Pruning Lifecycle

```text
INTRODUCE -> MONITOR -> EVALUATE -> PRUNE or GROW
```

Recommended controls:
- define the success metric before release
- define the exit criterion before release
- review usage and maintenance cost at least quarterly
- prefer staged retirement with flags or migration paths

## Removal Decision Flow

```text
Usage <5%?
  -> No: keep as Active/Core
  -> Yes
     -> Regulatory or security requirement?
        -> Yes: keep
        -> No
           -> Alternative exists?
              -> No: re-evaluate impact
              -> Yes
                 -> CoK >4?
                    -> No: DEFER
                    -> Yes: propose REMOVE with a phased plan
```

## Feature-Addition Gate

Every new feature request should answer:
1. What problem does it solve?
2. How many users are affected?
3. How does it align with the core value proposition?
4. What is the success metric?
5. What is the removal or re-review criterion?
6. What is the ongoing maintenance cost?

If the gate is incomplete, default to `DEFER` or `REJECT`.

### One In, One Out

Rule: when scope is already broad, adding one feature should force a conversation about removing one.

Exceptions:
- very early product stage
- regulatory or mandatory features

## Void Use

- Use low-usage features (`<5%`) as strong `REMOVE` candidates.
- Use feature-creep signal count to decide whether to trigger `Batch Audit`.
- Use the pruning lifecycle when a hard delete is unsafe.

Quality gates:
- usage `<5%` -> zombie-feature review
- onboarding `>30 min` -> recommend scope reduction
- missing gate answers -> block feature expansion
- 3 or more feature-creep signals -> recommend `Batch Audit`

Sources: [ProductPlan: Feature Creep](https://www.productplan.com/glossary/feature-creep/) · [Intercom: Managing Feature Requests](https://www.intercom.com/blog/managing-feature-requests/) · [Basecamp Shape Up](https://basecamp.com/shapeup/1.1-chapter-02) · [Kohavi et al. — Online Experimentation at Microsoft (Microsoft Experimentation Platform)](https://ai.stanford.edu/~ronnyk/2009-ExPControlledExperimentsAtScaleICSE.pdf) · [LeadDev — How AI-generated code accelerates technical debt (2026)](https://leaddev.com/technical-direction/how-ai-generated-code-accelerates-technical-debt)
