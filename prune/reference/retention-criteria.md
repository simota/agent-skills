# Inventory, Retention and Overlap

Use before SCORE/CLASSIFY. Prune remains read-only/propose-only; `SKILL.md` owns approval, protected-skill and archive requirements.

## Inventory

Resolve the actual host's installed skill root through `_common/CLI_COMPATIBILITY.md`; include project-local sources and distinguish intentional mirrors via `_common/PROJECT_LOCAL_SKILLS.md`. Scan the full roster for hidden dependencies even for TARGETED classification; cache within the session and re-scan for FOLLOWUP. An unavailable log/profile is unknown, never zero use/dependencies.

Read in order: roster; every frontmatter and CAPABILITIES_SUMMARY/COLLABORATION_PATTERNS/BIDIRECTIONAL_PARTNERS/PROJECT_AFFINITY; reference count/size and actual consumers; `.agents/PROJECT.md` activity; per-skill journal; project CLAUDE.md/AGENTS.md and `_common/` dependencies; current `_common/SKILL_PACKS.md`; all actual host profiles; Nexus skill, signal keywords and routing consumers. Use 90 days for usage scoring but inspect the full ≥6-month horizon for sunset evidence. Validate empty/missing fields before scoring.

```yaml
inventory:
  - skill: <name>
    frontmatter:
      description_chars: <int>
      description_has_when_clause: <bool>
    capabilities:
      count: <int>
      collaboration_partners_in: [<list>]
      collaboration_partners_out: [<list>]
    files:
      skill_md_lines: <int>
      references_count: <int>
      references_total_chars: <int>
    activity:
      project_md_entries_90d: <int>
      journal_last_modified: <YYYY-MM-DD or null>
      journal_entry_count: <int>
    dependencies:
      claude_md_mentions: <int>
      common_md_mentions: <int>
      pack_memberships: [<pack-name>]
      profile_coverage: [<profile-name>]
      nexus_routing_mentions: <int>
```

## Scoring Axes

Each axis is 0–5; retain the observed inputs and maximum 25-point sum. Size/reference count are maintenance **signals**, not targets: optional references need no minimum count. Never create references to improve a score.

### 1. Usage (0-5)

Activity in `.agents/PROJECT.md` over the last 90 days.

| Score | Threshold |
|-------|-----------|
| 5 | Weekly use (12+ entries / 90 days) |
| 4 | Bi-weekly (6-11) |
| 3 | Monthly (3-5) |
| 2 | Rare (1-2) |
| 1 | One-off in last 90 days |
| 0 | No activity in 90+ days |

### 2. Overlap (0-5, inverted)

Maximum overlap percentage against any other skill, from the overlap matrix.

| Score | Max overlap |
|-------|-------------|
| 5 | < 10% (unique) |
| 4 | 10-19% (clearly differentiated) |
| 3 | 20-29% (acceptable specialization) |
| 2 | 30-49% (merge candidate, evaluate) |
| 1 | 50-69% (strong merge candidate) |
| 0 | ≥ 70% (likely duplicate, sunset or merge mandatory) |

### 3. Uniqueness (0-5)

Number of CAPABILITIES_SUMMARY entries that are NOT covered by any other single skill.

| Score | Unique capabilities |
|-------|---------------------|
| 5 | 5+ unique capabilities |
| 4 | 3-4 |
| 3 | 2 |
| 2 | 1 |
| 1 | 0 unique, but distinct combination of shared capabilities |
| 0 | All capabilities exist in another single skill |

### 4. Coverage (0-5)

Number of `PROJECT_AFFINITY` rows with H or M relevance, plus Pack membership count.

| Score | Coverage breadth |
|-------|------------------|
| 5 | Member of 3+ Packs and high relevance to 3+ project domains |
| 4 | Member of 2 Packs, 2+ project domains |
| 3 | Member of 1-2 Packs, 1-2 project domains |
| 2 | 1 Pack, 1 domain |
| 1 | No Pack but referenced in CLAUDE.md or `_common/` |
| 0 | No Pack membership, no CLAUDE.md / `_common/` reference |

### 5. Maintenance Cost (0-5, inverted)

SKILL.md size, reference count, journal freshness.

| Score | Cost signal |
|-------|-------------|
| 5 | SKILL.md ≤ 5k tokens, ≤ 5 references (zero allowed), journal updated < 30 days ago |
| 4 | ≤ 7k tokens, ≤ 7 references, journal < 60 days |
| 3 | ≤ 10k tokens, ≤ 10 references |
| 2 | 10-15k tokens, > 10 references OR stale journal (60-180 days) |
| 1 | > 15k tokens OR > 15 references OR very stale (180-365 days) |
| 0 | Unmaintained: > 15k tokens, > 15 references, journal > 365 days |



**Ambiguous bands:** the original Usage table overlaps at one entry, Coverage has overlapping Pack/domain bands, and Maintenance conditions may match more than one row. Expose the eligible score range; do not silently invent a tie policy. Seek a decision if that range changes the verdict. Missing evidence is not a zero score.

## Pairwise Overlap

Normalize declared capabilities to `(verb, object, qualifier)`, then use semantic equivalence checked against description/Recipes/Trigger Guidance. For every pair in the audit scope:

```text
raw_overlap_pct = 100 × shared_capabilities / max(capabilities_A, capabilities_B)
boundary_adjusted = raw_overlap_pct − min(20, 5 × explicit_mutual_exclusions)
pack_adjusted = boundary_adjusted × 1.2 if the pair shares a Pack, otherwise boundary_adjusted
```

Keep raw and adjusted results. Empty capability sets require missing-data review, not division by zero. Explicit mutual-exclusion clauses are intentional boundaries; verify each counted exclusion. Use adjusted overlap in axis 2's bands. The written cross-Pack modifier subtracts 0.1 from axis 2 for cross-Pack overlap ≥30%; report it separately rather than silently reversing its sign. Adjusted overlap is a policy index and can exceed 100, not a literal shared-capability percentage.

Report only pairs with adjusted overlap ≥30% in the triangular matrix, with matching capabilities, boundary deductions, Pack adjustment and canonical-owner evidence. Do not use invented below-threshold matrix values as examples. ≥50% requires merge investigation; ≥70% requires absorb/sunset investigation, **not** permission to bypass retention/protection gates. Usage and Coverage select the owner through `reference/merge-protocol.md`.

For `_common`/reference near-duplicates, the SKILL's `HD-ENTROPY` test is a lossless merge trial with fewer net lines; heading/token similarity alone is not proof.

## Registry Drag

For below-KEEP scores and new proposals, inspect selection ambiguity (`HD-OPAQUE`), unnecessary external/fan-out latency, and excess permission surface (`HD-PERM`). Use observed routing/rework/authorization evidence. Drag supports a MERGE argument, never a separate SUNSET path. Every addition must declare what would make it unnecessary.

## Classification Thresholds

Sum the 5 axes (max 25):

| Retention Score | Verdict | Action |
|----------------|---------|--------|
| 20-25 | **KEEP** | No action; healthy skill |
| 15-19 | **KEEP with improvement** | Handoff to Architect IMPROVE recipe |
| 10-14 | **MERGE candidate** | Apply merge protocol (find canonical owner) |
| 5-9 | **SUNSET candidate** | Apply 3-condition gate (see Core Rule 5) before proposing |
| 0-4 | **DEPRECATE** | Urgent review; archive within 30 days only if the full sunset gate and approval pass |



## 3-Condition Sunset Gate

All three are mandatory, including DEPRECATE candidates: ≥6 months without evidenced activity; a clear capability-covering alternative; and no active project dependency (project CLAUDE.md/AGENTS.md, `_common` and active profiles). Missing evidence or a failed condition means **DEPRECATE-WATCH**, not approval. Scores cannot override this gate.

Apply the protected set from `SKILL.md` and current mandatory Pack membership; project-CLAUDE.md dependencies are protected too. Score for completeness but classify protected skills KEEP. Use `reference/pack-impact.md` before any removal proposal, then `reference/merge-protocol.md` or `reference/sunset-protocol.md` for delivery.
