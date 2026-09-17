# Merge Proposal

Use after retention scoring: a pair with overlap ≥30% and both Usage≤3; a 3+-skill cluster with mutual overlap≥25%; or a new addition raising another skill above 30%. Read `reference/retention-criteria.md` for evidence/scoring; overlap alone is not a merger decision.

## Canonical Owner

Choose exactly one owner in order: higher Usage, higher Coverage, lower maintenance burden, higher Uniqueness, then documented arbitrary alphabetical tiebreak. If all scores are within ±1 or ownership is otherwise ambiguous, use Ask First rather than letting alphabetical order manufacture confidence. For multi-way merges, choose the owner once and record each absorbed skill separately.

Propose the union of capabilities minus actual duplicates, trigger coverage and collaboration partners. Preserve unique capabilities outside the overlapping theme explicitly (`absorbed from <skill>` when appropriate). Trial reference consolidation for claim preservation and net reduction; do not copy entire supporting libraries by default.

## Migration and Reversal

| Change | Owner |
|---|---|
| Canonical CAPABILITIES_SUMMARY, description triggers and unique references | Architect after approval |
| Pack memberships and Nexus keyword routing to the owner | Architect; cross-Pack assignment requires explicit justification/confirmation |
| Archive absorbed skill at `.archive/<name>/` for ≥90 days | User/manual, never direct deletion |
| All actual host profiles and project/common mentions | User/manual |

Use `reference/pack-impact.md` for coverage/profile gates and `reference/sunset-protocol.md` for the full downstream consumer set and reverse restoration manifest. Canonical owner's Pack wins for the proposed cross-Pack assignment; document every lost membership, don't infer that all profiles still include the owner.

## Deliverable

For every absorbed skill include: pairwise overlap and evidence, both retention/Usage/Coverage scores, chosen owner and reason, capabilities to add, per-reference source→destination or merge disposition, Pack/profile changes, in/out collaboration partners, project/common file:line consumers, Nexus keywords/routing, archive path and complete reactivation steps.

Emit `PRUNE_TO_ARCHITECT_MERGE` **before execution** with the approved proposal and unresolved gates. Prune does not implement. After implementation, Nexus receives `PRUNE_TO_NEXUS_ROUTING_UPDATE`; verify residual consumers rather than assuming the migration task list succeeded.
