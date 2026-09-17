# Sunset Proposal and Removal Verification

Prune proposes; the user approves and executes archive/removal. SUNSET and DEPRECATE both require `reference/retention-criteria.md`'s full three-condition gate and protected-skill checks. Low retention does **not** waive inactivity or alternative coverage. All removal proposals also require `reference/pack-impact.md`.

## Gate and Capability Evidence

```yaml
gate_evidence:
  condition_1_inactive:
    last_activity: <YYYY-MM-DD or "never">
    days_since: <int>
    pass: <bool>
  condition_2_alternative:
    alternative_skill: <name>
    overlap_with_target: <pct>
    covers_unique_capabilities: <bool>
    pass: <bool>
  condition_3_no_dependency:
    claude_md_mentions: <int with file:line>
    common_md_mentions: <int with file:line>
    pack_memberships: [<list>]
    profile_coverage: [<list>]
    pass: <bool>
gate_verdict: PASS | FAIL (any condition false → FAIL → DEPRECATE-WATCH)
```

`never` requires a complete observation window; missing logs cannot prove never-used. Inactivity is ≥6 months, not the 90-day usage-scoring window. Record actual project/host namespaces and all active consumers, not only a hard-coded Claude directory.

```yaml
capability_migration:
  - capability: <name>
    moves_to_skill: <alternative>
    confidence: HIGH | MEDIUM | LOW
    note: <required prompt phrase shift, if any>
```

Any capability lacking HIGH-confidence coverage is a partial-coverage gap requiring explicit review; user acceptance is not proof that the alternative condition passes. If a gate fails, record no-action/watch status rather than a ready-to-execute sunset.

## Archive and Consumer Manifest

Before proposing the move, search tracked/configured consumers across the full repository and relevant host configuration; preserve command/scope/result. Every discovered consumer joins the manifest below. Archive the skill, its references and associated journal at `.archive/<skill>/` with `ARCHIVED_<YYYY-MM-DD>.md`, reason, alternative and **≥90-day** retention/reactivation plan.

| Consumer to update | Reverse restoration obligation |
|---|---|
| `_common/SKILL_PACKS.md` and all actual host profiles | Restore recorded Pack/profile membership |
| Nexus `signal-keywords.md` and `routing-matrix.md` | Restore keyword targets and default-chain task types |
| Nexus `recipes-index.md` **and** SKILL.md Recipe Registry allowlist | Restore both atomically |
| Nexus `agent-disambiguation.md` and `_common/BOUNDARIES.md` | Restore disambiguation/boundary entries |
| Every partner's COLLABORATION_PATTERNS / BIDIRECTIONAL_PARTNERS | Restore both directions |
| Project CLAUDE.md / AGENTS.md, `_common` and any additional discovered consumer | Restore exact references/contract-delivery paths and intentional mirrors/symlinks |
| Stated skill counts | Re-derive from the restored/current roster |
| `.agents/PROJECT.md` | Append dated archive/reactivation record; don't rewrite history |

Reactivation restores the archived directory **and** this entire recorded consumer set, then notifies Nexus and re-runs repository validation. A directory-only restore is incomplete.

## Verification by Absence

After approved execution, repeat the pre-move search. Permitted residuals: `.archive/<skill>/`, dated `.agents/PROJECT.md` archive records, CHANGELOG and journal history. A live routing/contract/profile reference anywhere else means **not removed**. Report actual command and counts; `SUNSET_VERIFIED: <N> residual hits, all in archive/records` is permitted only after this check, never from a checklist of steps performed.

## Proposal Fields and Handoff

Deliver verdict/retention score; all three gate results with dates and file:line evidence; per-capability alternative/confidence; complete downstream consumer/Pack/profile manifest; pre-move residual counts; archive note/path and reverse steps; post-move validation status (pending until execution). Request `PRUNE_TO_USER_SUNSET_APPROVAL` before any move. After approved execution emit `PRUNE_TO_NEXUS_ROUTING_UPDATE` with residual-search evidence.

## DEPRECATE-WATCH

Persist failed gates in `.agents/prune.md`; no execution this cycle:

```yaml
deprecate_watch:
  - skill: <name>
    failed_condition: 1 | 2 | 3
    next_audit_due: <YYYY-MM-DD (90 days out)>
    note: <what would need to change for sunset to be valid>
```
