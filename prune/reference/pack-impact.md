# Pack Impact — SKILL_PACKS / Profile Impact Analysis

Mandatory pre-removal analysis whenever a merge or sunset proposal would change Pack membership or profile coverage.

Source of truth: `_common/SKILL_PACKS.md` (Pack definitions) and `~/.claude/profiles/*.json` (active-pack profiles).

## Why this matters

Removing a skill from a Pack changes the routing surface for every profile that activates that Pack. If a profile shrinks below 8 skills (Anthropic optimum lower bound), users may not notice; if it crosses below 5, routing degrades. If a profile loses a uniquely-covered capability without an alternative skill in the same Pack, the profile becomes incomplete.

## Inputs

1. Target skill(s) for removal — from merge proposal (merged-in side) or sunset proposal.
2. `_common/SKILL_PACKS.md` — Pack roster (currently 10 Packs: `core`, `web`, `mobile`, `security`, `ai-eval`, `growth`, `infra`, `design`, `research`, `package-gen`).
3. `~/.claude/profiles/*.json` — 9 profiles (`web`, `mobile`, `security`, `growth`, `infra`, `research`, `ai-eval`, `package-author`, `all`).

## Steps

### 1. Pack membership scan

For each target skill, list every Pack containing it:

```yaml
target_skill: <name>
current_packs:
  - pack: <name>
    pack_size_before: <int>
    pack_size_after_removal: <int>
    pack_dropping_below_threshold: <bool, threshold = 8>
```

### 2. Capability gap detection per Pack

For each Pack the target belongs to, check whether removal leaves a capability uncovered:

```yaml
pack: <pack-name>
target_unique_capabilities_in_pack:
  - capability: <name>
    other_pack_members_covering: [<list>]
    coverage_gap: <bool>  # true if no remaining Pack member covers
```

If `coverage_gap` is true for any capability, flag as **Pack incomplete after removal** and recommend either (a) keep the skill in the Pack, (b) add an alternative skill to the Pack, or (c) accept the gap with explicit user confirmation.

### 3. Profile impact scan

For each profile that activates an affected Pack:

```yaml
profile: <name>
includes_target: <bool>  # may not, if profile uses subset of Pack
total_skills_before: <int>
total_skills_after: <int>
crosses_below_8: <bool>  # Anthropic optimum lower bound
crosses_below_5: <bool>  # degradation threshold
```

### 4. Recommendations

Based on the scan, produce one of:

| Scenario | Recommendation |
|----------|---------------|
| No Pack crosses below 8 + no coverage gap | Proceed — clean removal |
| Pack drops below 8 but ≥ 5 + no coverage gap | Proceed with note; suggest profile review later |
| Pack drops below 5 OR coverage gap exists | **Block** — propose alternative skill to fill, or expand Pack with related skill |
| Profile crosses below 8 | Note in proposal; user decides whether to add other skills |
| Profile crosses below 5 | **Block** — profile becomes ineffective; require user decision |

### 5. Proposal output additions

Append to merge or sunset proposal:

```markdown
### Pack impact

**Pack membership changes**:
- `<pack1>`: <size_before> → <size_after> (delta -1) [WITHIN THRESHOLD | DROPS BELOW 8 | DROPS BELOW 5]
- `<pack2>`: <size_before> → <size_after>

**Coverage gaps detected**:
- `<pack1>` loses capability `<cap>` — no remaining member covers — **GAP**
- `<pack2>` loses capability `<cap>` — `<other-skill>` already covers — OK

**Profile impact**:
- `web.json`: <size_before> → <size_after>
- `package-author.json`: <size_before> → <size_after> (drops below 8 — review recommended)

**Recommendation**: <PROCEED | PROCEED-WITH-NOTE | BLOCK + reason>
```

## Always

- Scan all 10 Packs even when the target appears to belong to one — `_common/SKILL_PACKS.md` membership is overlapping.
- Scan all 9 profiles even when the target appears to be in a subset — profiles are user-editable.
- Quantify "drops below 8" and "drops below 5" thresholds explicitly per Anthropic guidance.

## Never

- Skip Pack scan because "the skill is only in one Pack" — verify, don't assume.
- Approve removal that creates a coverage gap without an explicit alternative or user confirmation.
- Ignore profile impact even when Pack impact is clean — profiles are the live user-facing config.

## Cross-references

- `_common/SKILL_PACKS.md` — Pack definitions and `core` always-on contract
- `~/.claude/profiles/*.json` — Active-pack profiles
- `reference/sunset-protocol.md` step 3 — Pack/profile cleanup in archive plan
- `reference/merge-protocol.md` step 4 — Pack/profile cleanup in migration plan
