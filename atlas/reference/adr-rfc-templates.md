# ADR / RFC Contracts

| Decision | Artifact |
|----------|----------|
| Major pattern, technology, public contract or irreversible trade-off | Full ADR |
| Significant cross-team proposal requiring input and migration planning | RFC |
| Small reversible but notable choice | Lightweight decision record |

Follow the repository's existing location/naming. Otherwise use `docs/architecture/decisions/` and an index with ID, title, status and date. An accepted ADR is immutable: record a changed decision in a new superseding ADR, not by rewriting the accepted narrative. The optional CI header (`constraints`, `affected`, `tests`) is a projection, never a replacement for that narrative.

## Full ADR

Required sections: `Status`; `Context` (problem, forces, pain points, constraints); `Decision` (active voice); `Alternatives Considered` (at least two feasible alternatives, each with pros, cons and rejection reason); `Consequences` (positive, negative and applicable neutral effects); `Implementation Plan`; `References`.

States: Proposed → Accepted; a later record/index may report Deprecated or Superseded by ADR-YYYY. Schedule the core contract's one-month outcome review; record Confirmed / Superseded / Deprecated without mutating the accepted decision. One ADR records one decision, not a whole component specification.

## RFC

Required sections: `Summary`; `Motivation` (pain, impact, urgency); `Detailed Design` (current/proposed state and key changes); `Migration Strategy` (preparation, implementation, cleanup); `Rollback Plan`; `Trade-offs` (before/after complexity, performance, maintainability); `Risks` (likelihood, impact, mitigation); `Open Questions`; `Timeline` (milestones, not invented calendar commitments).

## Lightweight Decision Record

Required fields: title, date, status, deciders, context, decision, rationale and consequences. Do not inflate a reversible local choice into a full RFC.

## Decision Completion Check

Require evidence; explicit criteria and feasible alternatives; affected stakeholders' agreement and dissent; versioned decision documentation; and an implementation/verification/review plan. Every non-deprecated ADR maps to at least one fitness function. Reject a proposal that contains only benefits, a strawman alternative, unsupported fashion/scale assumptions, no downstream/operations view, or no long-term consequences. Time-box uncertainty instead of keeping a decision indefinitely open.

## Modernization Proposal

This is Atlas's planning contract; route implementation to the owning skill. Include a dependency map, a replaceable slice, rollback/switch criteria, consistency and transaction boundaries, frontend consumers, legacy-domain expertise, milestones and explicit decommission evidence. Retire a legacy path only after traffic and validation prove the replacement works. Feature parity is a scope decision supported by usage/requirements, not a mandate to reproduce unused features.

| Constraint | Strategy to evaluate |
|------------|----------------------|
| Must stay running; separable slices | Strangler Fig with a routing facade and model translation |
| Legacy code cannot change | Leave & Layer with explicit integration contracts |
| Small scope and approved outage | A justified big-bang replacement may be considered |
| Infrastructure-only change | Lift & Shift; do not claim application debt was removed |
| Platform/runtime change | Re-platform with compatibility, migration and rollback evidence |

A rewrite without a staged alternative, migration without a data-consistency plan, or permanent old/new duplication without a retirement owner fails review. CDC, Saga, micro-frontends and a specific event platform are options only when the actual dependencies require them, not mandatory products.
