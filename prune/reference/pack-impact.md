# Pack and Profile Removal Impact

Load before a merge/sunset proposal. Read current `_common/SKILL_PACKS.md` and all actual host profiles; do not copy Pack/profile names or counts into this reference. Claude profiles may live at `~/.claude/profiles/*.json`; resolve other host arrangements through `_common/CLI_COMPATIBILITY.md`. Project-local skills/mirrors follow `_common/PROJECT_LOCAL_SKILLS.md`, not global Pack membership.

For every target, enumerate **all** memberships, remaining capability coverage and actual profile skill sets (a profile can select a subset of a Pack). Unknown/inaccessible profiles are an evidence gap, not an empty set.

## Evidence Fields

```yaml
target_skill: <name>
current_packs:
  - pack: <name>
    pack_size_before: <int>
    pack_size_after_removal: <int>
    pack_dropping_below_threshold: <bool, threshold = 8>
```

```yaml
pack: <pack-name>
target_unique_capabilities_in_pack:
  - capability: <name>
    other_pack_members_covering: [<list>]
    coverage_gap: <bool>  # true if no remaining Pack member covers
```

```yaml
profile: <name>
includes_target: <bool>  # may not, if profile uses subset of Pack
total_skills_before: <int>
total_skills_after: <int>
crosses_below_8: <bool>  # local review threshold
crosses_below_5: <bool>  # local blocking threshold
```

## Decision Table

The existing 8/5 thresholds below are local Prune review gates, not asserted vendor-wide optimums or empirical performance guarantees.

| Observed result | Proposal disposition |
|---|---|
| No Pack below 8 and no coverage gap | PROCEED subject to the SKILL's other gates |
| Pack falls below 8 but remains ≥5; no gap | PROCEED-WITH-NOTE; review profile coverage |
| Pack below 5 or coverage gap | BLOCK until an alternative/fill plan or explicit user decision resolves the impact; never override protected-skill or sunset eligibility |
| Profile crosses below 8 | Note; user decides whether to add coverage |
| Profile crosses below 5 | BLOCK pending user decision |

Append each affected Pack/profile's before/after size and delta, threshold crossings, lost capabilities with remaining coverers, recommendation and reason. A clean Pack result does not substitute for a profile check. Merge migration is owned by `reference/merge-protocol.md`; archive/removal verification by `reference/sunset-protocol.md`. Retain explicit user acceptance for an unresolved gap; it is not evidence that an alternative exists.
