# Persona Governance and Organizational Readiness

Purpose: Define lifecycle governance, update cadence, retirement rules, and organizational rollout practices for Cast-managed personas.

## Contents

1. Lifecycle phases
2. Update triggers
3. Retirement rules
4. Organizational readiness
5. Living document principles

## Lifecycle Governance

### Five Phases

| Phase | Goal | Typical output |
|---|---|---|
| Planning | Define purpose, scope, stakeholders, data sources | Persona plan |
| Conception | Collect data and draft proto-personas | Proto-personas |
| Maturation | Validate and promote to active use | `draft -> active` |
| Adulthood | Use, update, evolve, measure impact | Active persona portfolio |
| Retirement | Archive or replace obsolete personas | `active -> archived` |

### Maturation Gate

- Promote to `active` at `confidence > 0.60`.

## Update Triggers

| Trigger | Urgency | Example |
|---|---|---|
| Major market change | `P0` | regulation or disruptive competitor event |
| User-base shift | `P1` | new enterprise segment or sharp demographic shift |
| Behavior drift | `P2` | new usage pattern or funnel divergence |
| New release | `P2` | major feature shifts user behavior |
| Feedback accumulation | `P3` | recurring support/NPS pattern changes |
| Scheduled review | `P3` | quarterly review cycle |

### Suggested Cadence

- Monthly: freshness check, drift scan, decay application
- Quarterly: full review, coverage review, anti-persona review
- Yearly: large-scale revalidation, clustering rerun, retirement review

## Retirement Rules

### Triggers

| Trigger | Threshold / condition | Action |
|---|---|---|
| Segment disappearance | segment falls below `5%` | Archive quickly |
| Segment merge | no meaningful behavioral difference remains | Merge personas |
| Long-term unused | unused in decisions for `6 months` | Review for retirement |
| Confidence collapse | confidence below `0.30` | Revalidate or retire |
| Source loss | major evidence source disappears | Replace source or retire |
| Strategy shift | market or segment is no longer targeted | Archive |

### Retirement Process

1. Identify the retirement candidate.
2. Assess downstream dependency.
3. Obtain stakeholder approval.
4. Define successor or replacement if needed.
5. Move to archive and update registry metadata.

## Organizational Readiness

Evaluate readiness across:

- leadership support
- process integration
- data infrastructure
- team skill
- user-centered culture

### Rollout Roadmap

| Phase | Goal | Duration |
|---|---|---|
| Seed | awareness | `1-2` months |
| Grow | pilot adoption | `2-3` months |
| Scale | standardization | `3-6` months |
| Optimize | automation and measurement | `6-12` months |

## Living Document Principles

| Principle | Meaning |
|---|---|
| Easy to edit | difficult formats do not stay updated |
| Easy to access | personas must live where teams already work |
| Low update cost | attribute-level changes should be cheap |
| Visible history | everyone must see what changed and when |
| Stable but flexible | Core Identity stays fixed; peripheral details evolve |

Preferred formats:

- Markdown
- wiki / shared documentation
- structured YAML plus human-readable view

Avoid:

- static PDF as the only source
- hard-to-edit design files as the only source
- image-only persona assets

## Provenance and Versioning (as of 2026-05)

Personas are governance artifacts when they feed AI training, decisioning, or evaluation. Versioning and provenance practices must align with current external standards:

| Requirement | Source standard | Cast practice |
|---|---|---|
| Persona record carries provenance metadata (origin, contributors, edits) | C2PA Content Credentials 2.2 (`spec.c2pa.org/specifications/specifications/2.2/`) | `Source Analysis` section + frontmatter `created`, `updated`, `evolution_count` |
| AI-generated persona portraits or voice clips carry C2PA assertions | C2PA 2.2 (released 2025-04-22 / 2025-05-01) | Attach Content Credentials to any AI-generated media bundled with the persona; flag in registry as `synthetic_media: true` |
| AI-system lifecycle controls (bias mitigation, human oversight, traceability) | ISO/IEC 42001:2023 Annex A | Cast registry serves as the AIMS-aligned record-of-decisions for persona artifacts feeding downstream AI |
| Risk-treatment evidence per AI-specific risk category | ISO/IEC 23894:2023 + NIST AI 600-1 (2024-07) | `Evolution Log` records risk-treatment actions when bias-audit or drift triggers a change |
| PII handling for persona attributes derived from real users | GDPR (EU), CCPA (US), 改正個人情報保護法 (Japan APPI amendment bill, Cabinet-approved 2026-04-07; enforcement expected by 2028) | Anonymize before persona synthesis; for AI-training use cases, document statutory basis (e.g., APPI statistical-processing exemption) — see also Cloak skill |

### Update-Cadence Implication

EU AI Act milestones to keep on the calendar (high-risk and GPAI scope):

- **2025-08-02**: GPAI obligations + AI Office operational.
- **2026-08-02**: GPAI penalties applicable.
- **2026-08-02**: High-risk AI systems obligations enter into force (most provisions of Title III).
- **2027-08-02**: Pre-existing GPAI models (placed on market before 2025-08-02) full compliance.

When a persona set materially feeds an EU-scope AI system, schedule a governance review aligned with the next applicable milestone.
