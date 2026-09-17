# Functional Overlap Detection

Read during ANALYZE. Compare the proposed primary action, inputs and outputs with actual current SKILL.md definitions. Use `_common/BOUNDARIES.md` for authoritative ownership; do not substitute a copied roster or name similarity for a capability comparison.

## Matching and Score

| Capability relationship | Match value |
|-------------------------|-------------|
| Exact | 1.0 |
| Synonym / equivalent responsibility | 0.8 |
| Partial | 0.5 |
| Related but different responsibility | 0.2 |
| None | 0.0 |

`Overlap (%) = sum(capability match values) / total capabilities × 100`.

Record the capability inventory, each pairing and the denominator used. The original rubric does not specify normalization for unequal inventories: expose that ambiguity and review the ownership evidence rather than presenting an arbitrary normalization as canonical. Do not reuse example percentages as observations.

Assess three dimensions: functional (actions/inputs/outputs), domain (technical/business/code scope), and collaboration (chain position/partners/blocking dependencies). Shared domain alone is not shared ownership.

## Decision Bands

| Score | Decision |
|-------|----------|
| 0–10% | Proceed |
| 10–20% | Note overlap |
| 20–30% | Review differentiation |
| ≥30% and <50% | Ask first; document differentiation |
| ≥50% | Reject by default; propose the existing-owner alternative |

At a boundary, the higher approval requirement applies. SKILL.md owns the approval/rejection gate; scoring uncertainty near a gate must not be used to bypass it.

## Report Contract

Report the proposed name, purpose and category; the top three existing overlaps; matched and unique capabilities; per-agent scores with their evidence/denominator; the differentiating outcome; and a recommendation with alternatives. An overlap table without a concrete remaining gap is not a creation justification.

## Exceptions

A deliberate replacement, domain-specific variant or explicit request for overlapping agents requires user confirmation and a written reason. Record the overlap percentage, existing owner and distinguishing scope. A replacement also needs a migration plan; it does not authorize silent deletion or immediate rerouting.
