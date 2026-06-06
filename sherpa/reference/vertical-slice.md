# Vertical Slice Planning Reference

Purpose: Decompose work by end-to-end customer value ("vertical slice") instead of by technical layer ("horizontal"). Each slice ships real user-visible behavior. Reserves horizontal bottom-up only for platform/infra where user value is not the unit of progress.

## Scope Boundary

- **sherpa `vertical-slice`**: Vertical vs horizontal decomposition trade-off and sizing (this document).
- **sherpa `walking-skeleton` (elsewhere)**: First vertical slice of a greenfield system.
- **sherpa `atomic` (elsewhere)**: ≤15-min step breakdown *inside* a vertical slice.
- **sherpa `epic` (elsewhere)**: Top-level epic decomposition. Vertical slicing is a strategy used inside epic breakdown.

## Vertical vs Horizontal

```
HORIZONTAL (layer-first)           VERTICAL (feature-first)
=========================          ==========================
┌─────────────┐                    ┌───┐ ┌───┐ ┌───┐
│  All UI     │ Sprint 1           │UI │ │UI │ │UI │ Sprint 1
├─────────────┤                    │API│ │API│ │API│ delivers
│  All API    │ Sprint 2           │DB │ │DB │ │DB │ Slice A,
├─────────────┤                    └───┘ └───┘ └───┘ B, C
│  All DB     │ Sprint 3            A    B    C
└─────────────┘
Ships nothing until               Each slice ships
Sprint 3. No user                 working feature.
feedback for months.              Feedback per sprint.
```

## When Vertical Slicing Applies

- **Product features** (user-facing).
- **Greenfield systems** after the walking skeleton.
- **Any project where user feedback matters per sprint**.
- **Startup / product-market-fit phase**.

## When Horizontal Slicing Is Acceptable

- **Platform / infrastructure work** with no direct user visibility (logging system, CI pipeline, dev tooling).
- **Foundational primitives** where correctness must be complete before use (crypto, distributed consensus).
- **Legacy replatforming** where maintaining invariants across the whole data layer matters.

Even then, aim to keep horizontal slabs small and integrate frequently.

## Slice Quality Checklist

A good vertical slice:

- [ ] **Delivers user value**: a human could describe what they can now do.
- [ ] **End-to-end**: touches every layer needed to deliver the value.
- [ ] **Independent**: ships without waiting for other slices.
- [ ] **Small**: fits in a sprint (or a day for atomic).
- [ ] **Testable**: has at least one acceptance test.
- [ ] **Demonstrable**: can be shown to a stakeholder.
- [ ] **Revertable**: can be disabled via feature flag without breaking others.

## Slicing Heuristics

### 1. By user goal, not by data shape

- ✅ "User can publish a post."
- ❌ "Post table migrations."

### 2. By happy path first

- Slice A: happy path works.
- Slice B: error case 1 handled.
- Slice C: edge case 2 handled.

### 3. By simplest data variant

- Slice A: single-user widget.
- Slice B: multi-user widget.
- Slice C: shared widget with permissions.

### 4. By rule-simplification

- Slice A: free tier only.
- Slice B: paid tier variations.
- Slice C: enterprise tier.

### 5. By pipeline-stage

- Slice A: ingest step end-to-end with mock downstream.
- Slice B: transform step end-to-end with mock upstream.
- Slice C: connect A and B.

## Anti-Patterns

| Anti-pattern | Signal | Fix |
|--------------|--------|-----|
| "Database sprint" | Sprint goal is purely DB tables | Re-slice around user goals |
| "API sprint" | Sprint goal is endpoints with no UI | Pair each endpoint with a consumer |
| Slice that ships invisible code | Cannot be demo'd | Make it visible or defer |
| Slice > 2 weeks | Too large | Break into smaller user-valuable pieces |
| All slices depend on "foundation" slice | Single point of serialization | Shrink foundation or absorb into first user slice |
| Slices that require each other to test | Not independent | Decouple or merge |
| "Plumbing-only" slice | No user value | Attach plumbing to the first slice that needs it |

## Example Re-slice

### Horizontal (bad for product work)
- Sprint 1: All DB tables for orders, products, users.
- Sprint 2: All API endpoints.
- Sprint 3: All UI screens.
- Ships: nothing until Sprint 3.

### Vertical (good for product work)
- Slice 1: User can add a single product to cart (real product, hardcoded user, no checkout).
- Slice 2: User can check out with a fake payment method.
- Slice 3: Real payment via Stripe.
- Slice 4: Real user auth.
- Slice 5: Multi-product cart.
- Ships: working (growing) feature each sprint.

## Slice Sizing Rubric

| Size | Duration | Definition |
|------|----------|-----------|
| XS | < 1 day | Single atomic step worth of user value |
| S | 1-2 days | One happy path, one CTA |
| M | 3-5 days | Multiple related actions, one persona |
| L | 1-2 weeks | Multi-step flow with 2-3 decisions |
| XL | > 2 weeks | **Split.** Too large to slice. |

If a slice is XL, it must be broken down further.

## Output Template

```markdown
## Vertical Slice Plan: [Epic Name]

### Epic Goal
[1-2 sentences of user outcome]

### Slicing Strategy
- **Primary dimension**: [user goal / happy path / data variant / rule simplification / pipeline stage]
- **Rationale**: [why this dimension]

### Slice Sequence
| # | Slice | User Value Statement | Size | Dependencies |
|---|-------|----------------------|------|--------------|
| 1 | [Name] | "User can ..." | S | none |
| 2 | [Name] | "User can ..." | M | slice 1 |
| ... | ... | ... | ... | ... |

### Quality Gates per Slice
- [ ] User value described
- [ ] End-to-end (all layers)
- [ ] Independently deployable
- [ ] Under 1 sprint (ideally 1 week)
- [ ] Acceptance test defined
- [ ] Demoable

### Horizontal Exception (if any)
- **Slice / layer**: [which one is horizontal, e.g., "shared auth middleware"]
- **Rationale**: [why vertical doesn't apply]
- **Integration plan**: [how it re-joins user value]

### Handoff
- `atomic` for step-level breakdown of each slice.
- Builder, Voyager, Radar for execution.
- Pulse for per-slice success metric.
```

## Interaction with Other Agents

- **titan** may execute slice-first pattern for S/M scopes.
- **atomic** breaks each slice into ≤15-min steps.
- **walking-skeleton** is the first slice of a greenfield system.
- **launch** gates slice deployment.
- **ripple** evaluates blast radius per slice (usually small).
- **guardian** recommends PR granularity (often 1 PR per atomic step, or 1 PR per slice).

## Deliverable Contract

When `vertical-slice` completes, emit:

- **Slicing dimension** with rationale.
- **Slice sequence** (numbered, each with user-value statement, size, dependencies).
- **Quality gates** per slice.
- **Horizontal exceptions** if any, with integration plan.
- **Handoff** to `atomic` for step-level detail.

## References

- Jeff Patton — *User Story Mapping* (slicing by user goal)
- Mike Cohn — *User Stories Applied* (INVEST, vertical slicing)
- Ron Jeffries — "Essential XP: Small Releases" (vertical slice practice)
- Dan North — "Behavior-Driven Development" (acceptance test per slice)
- Henrik Kniberg — Spotify "Scaling Agile" (slice granularity)
- Allen Holub — Small batch / incremental delivery advocacy
