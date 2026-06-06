# Merge Protocol

Procedure for generating merge proposals when two or more skills classify as MERGE (Retention Score 10-14) or share ≥ 30% overlap with low individual Usage.

## When to apply

- Two skills with overlap ≥ 30% and both Usage scores ≤ 3.
- Cluster of 3+ skills with mutually ≥ 25% overlap (multi-way merge).
- A new skill addition raises an existing skill's overlap above 30%.

## Steps

### 1. Identify the merge cluster

List all skills in the candidate set (pair or cluster). For each pair, capture overlap % from `overlap-matrix.md`.

### 2. Select the canonical owner

The canonical owner inherits the merged scope. Choose based on (in priority order):

1. **Higher Usage score** — most-active skill stays.
2. **Higher Coverage score** — broader Pack/domain coverage wins.
3. **Lower Maintenance cost** — smaller, fresher SKILL.md wins.
4. **Higher Uniqueness** — skill with more uncovered capabilities stays.
5. **Tiebreaker** — alphabetical by skill name, documented as arbitrary.

Never skip this step. If no candidate clearly wins (all scores within ±1), flag as **canonical-owner ambiguity** and route to user via `## Ask First` (Boundary).

### 3. Compute the merged scope

```
canonical_owner.capabilities = union(canonical.caps, merged_in.caps) − duplicates
canonical_owner.description = extended to cover merged-in trigger keywords
canonical_owner.collaboration_partners = union(canonical, merged_in)
```

### 4. Plan the migration

| Task | Owner | Notes |
|------|-------|-------|
| Extend canonical SKILL.md CAPABILITIES_SUMMARY | Architect | Add merged-in capabilities; preserve semantic accuracy |
| Update canonical description WHEN clause | Architect | Add merged-in trigger keywords |
| Migrate merged-in references that have no equivalent | Architect | Copy unique references; merge equivalent ones |
| Archive merged-in skill to `.archive/<merged-in-name>/` | User (manual) | Preserve for 90-day re-activation window |
| Update `_common/SKILL_PACKS.md` Pack memberships | Architect | Remove merged-in from all Packs |
| Update `~/.claude/profiles/*.json` `skills` arrays | User (manual) | Remove merged-in from all profiles |
| Update `nexus/reference/signal-keywords.md` | Architect | Route merged-in keywords to canonical owner |
| Update CLAUDE.md / `_common/` mentions | User (manual) | Replace merged-in references with canonical |

### 5. Proposal output format

```markdown
## Merge Proposal: <canonical> ⊕ <merged-in>

**Overlap**: <pct>% (from overlap-matrix)
**Canonical owner**: <canonical> — Retention Score <X>/25, Usage <Y>, Coverage <Z>
**Merged-in**: <merged-in> — Retention Score <X>/25
**Justification**: <one line: why canonical wins>

### Capabilities to add to canonical
- <cap1>
- <cap2>
- ...

### References to migrate
- <merged-in>/reference/<name>.md → <canonical>/reference/<name>.md (unique) OR merged into existing
- ...

### Downstream impact
- Pack memberships: <merged-in> currently in [<packs>], all to be removed
- COLLABORATION partners: <list of in/out partners to redirect>
- CLAUDE.md mentions: <count>, file:line locations
- Nexus signal keywords: <list to redirect>

### Reversibility
- Archive location: `.archive/<merged-in>/`
- Re-activation: restore directory, re-add to Pack(s) [<list>], re-add signal keywords

### Handoff
→ Architect (`ARCHITECT_TO_NEXUS_HANDOFF` after execution)
```

## Always

- Identify exactly one canonical owner per merge proposal.
- Explicitly enumerate every downstream impact (Pack, profile, COLLABORATION, CLAUDE.md, Nexus routing).
- Preserve archive + re-activation instructions.

## Never

- Propose merge without naming the canonical owner.
- Execute the merge — Prune is propose-only; execution is Architect's job.
- Delete the merged-in skill directly — archive only.
- Skip cross-Pack canonical-owner justification when merging across Packs.

## Edge cases

- **Three-way merge**: Apply step 2 to find canonical, then treat remaining two as merged-in. Document each merge separately for reversibility.
- **Bidirectional capability**: When canonical lacks a capability the merged-in has but is unrelated to the overlap, add it explicitly to canonical's CAPABILITIES_SUMMARY with `(absorbed from <merged-in>)` annotation.
- **Pack-spanning merge**: Canonical owner's Pack wins; merged-in's Packs lose membership. Confirm with user before proposing.
