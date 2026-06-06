# Sunset Protocol

Procedure for generating sunset proposals when a skill classifies as SUNSET (Retention Score 5-9 + 3-condition gate) or DEPRECATE (0-4, immediate).

## 3-Condition Sunset Gate (from `retention-criteria.md`)

All three must hold before SUNSET proposal can be issued:

1. **6+ months without activity** in `.agents/PROJECT.md`.
2. **Clear alternative exists** — another skill covers the unique capabilities.
3. **No project depends on it** — zero mentions in `CLAUDE.md`, `_common/*.md`, or any active Pack profile.

If any condition fails, downgrade to **DEPRECATE-WATCH** (note for future audit; no action this cycle).

DEPRECATE (Retention < 5) bypasses condition 1 and 2 but still requires condition 3.

## Steps

### 1. Confirm gate eligibility

For each candidate, document evidence for all 3 conditions:

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

### 2. Identify the alternative migration

For each capability of the sunset target:

```yaml
capability_migration:
  - capability: <name>
    moves_to_skill: <alternative>
    confidence: HIGH | MEDIUM | LOW
    note: <required prompt phrase shift, if any>
```

If any capability has no alternative with HIGH confidence, flag as **partial coverage** and require user confirmation that the gap is acceptable.

### 3. Plan the archive

The skill is **archived, not deleted**. 90-day minimum retention window for reversibility.

| Task | Owner | Notes |
|------|-------|-------|
| Move `<skill>/` to `.archive/<skill>/` | User (manual) | Preserves SKILL.md + references + journal |
| Add archive note: `ARCHIVED_<YYYY-MM-DD>.md` in `.archive/<skill>/` | User (manual) | Re-activation steps + reason for archive |
| Remove from `_common/SKILL_PACKS.md` Pack entries | User (manual) | Note in commit message: "(archived; see .archive/<skill>)" |
| Remove from `~/.claude/profiles/*.json` `skills` arrays | User (manual) | Across all profile files |
| Remove from `nexus/reference/signal-keywords.md` | User (manual) | Route keywords to alternative skill |
| Update CLAUDE.md / `_common/*.md` mentions | User (manual) | Replace with alternative skill name |
| Append archive entry to `.agents/PROJECT.md` | User (manual) | Date + reason + alternative |

### 4. Proposal output format

```markdown
## Sunset Proposal: <skill>

**Verdict**: SUNSET (Retention <X>/25) OR DEPRECATE (Retention <X>/25)
**Gate verdict**: PASS — all 3 conditions met (or DEPRECATE bypass)

### Gate evidence
1. **Inactive**: last activity <YYYY-MM-DD>, <N> days ago
2. **Alternative**: `<alt-skill>` covers <pct>% of capabilities (HIGH confidence on <K> of <N>)
3. **No dependencies**: 0 CLAUDE.md mentions, 0 _common/ mentions, Pack memberships removable

### Capability migration
| Capability | → Moves to | Confidence | Note |
|-----------|------------|-----------|------|
| <cap1> | <alt> | HIGH | <note> |
| <cap2> | <alt> | MEDIUM | <prompt-shift required> |

### Downstream impact
- Pack memberships: [<list>] — remove all
- COLLABORATION partners: [<in/out list>] — redirect to <alt-skill> or remove
- Nexus signal keywords: [<list>] — redirect to <alt-skill>
- Profile coverage: [<profile-list>] — remove from each

### Reversibility (90-day window minimum)
- Archive location: `.archive/<skill>/`
- Archive note: `.archive/<skill>/ARCHIVED_<YYYY-MM-DD>.md` with re-activation steps:
  1. `mv .archive/<skill>/ <skill>/`
  2. Re-add to `_common/SKILL_PACKS.md` Pack entries [<list>]
  3. Re-add to profiles [<list>]
  4. Re-add signal keywords to `nexus/reference/signal-keywords.md`
  5. Notify Nexus via `ARCHITECT_TO_NEXUS_HANDOFF`

### Handoff
→ User (`PRUNE_TO_USER_SUNSET_APPROVAL`) — explicit approval gate before any file move
→ Nexus (`PRUNE_TO_NEXUS_ROUTING_UPDATE`) — after user approval, update signal keywords
```

## Always

- Document gate evidence for all 3 conditions even when DEPRECATE bypasses 1+2 (3 is still mandatory).
- Pair every sunset with a clear alternative skill and capability migration table.
- Preserve archive + re-activation instructions; never propose direct deletion.
- Require explicit user approval before execution — Prune does not move files.

## Never

- Sunset without the 3-condition gate (DEPRECATE bypasses 1+2 only; 3 always applies).
- Sunset a `core` Pack member (`nexus`, `sherpa`, `scout`, `builder`, `radar`, `zen`, `guardian`, `compass`, `architect`, `gauge`).
- Skip archive — direct deletion is never acceptable.
- Bypass user approval gate.

## DEPRECATE-WATCH ledger

When any of conditions 1 or 2 fails, the skill becomes DEPRECATE-WATCH:

```yaml
deprecate_watch:
  - skill: <name>
    failed_condition: 1 | 2
    next_audit_due: <YYYY-MM-DD (90 days out)>
    note: <what would need to change for sunset to be valid>
```

Persist in `.agents/prune.md` for the next audit cycle.
