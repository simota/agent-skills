# Unified Specification References

This directory contains Scribe's cross-team and staged-specification recipes. The material was consolidated from the former standalone `accord` skill on 2026-08-19; Scribe is now the active owner.

## Route Map

| Need | Read |
|---|---|
| Full/Standard/Lite selection | `template-selection.md` |
| Canonical L0-L4 package | `unified-template.md` |
| Business-to-technical translation | `business-tech-translation.md` |
| BDD / Three Amigos / Example Mapping | `bdd-best-practices.md` |
| Bidirectional traceability | `cross-reference-guide.md`, `traceability-pitfalls.md` |
| Story quality and prioritization | `user-story-smells.md` |
| Package validation | `specification-anti-patterns.md` |
| Scope calibration | `specification-calibration.md` |
| Ask-first decisions | `interaction-triggers.md` |
| Structured handoffs | `handoff-formats.md` |
| Story maps | `user-story-mapping.md` |
| Stakeholder maps | `stakeholder-map.md` |
| RACI / DACI / RAPID | `raci-matrix.md` |

## Legacy Token Policy

Canonical tokens use `SCRIBE` (`FIELD/CAST/VOICE_TO_SCRIBE`, `SCRIBE_TO_BUILDER`, and related forms). During the 90-day reactivation window ending 2026-11-17, Scribe may consume an inbound token containing `ACCORD` as a compatibility alias, normalize it to `SCRIBE`, and emit only the canonical token.

The former `ACCORD_TO_SCRIBE` handoff is now an internal transition from a unified package to a formal PRD/SRS/HLD/LLD. It must not be emitted as `SCRIBE_TO_SCRIBE`.

The archived source remains under `.archive/accord/` for rollback; active recipes must not depend on archived files.
