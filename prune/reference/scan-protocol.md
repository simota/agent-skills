# Scan Protocol

Inventory sources and order for the SCAN phase. Mandatory before any SCORE / CLASSIFY work.

## Sources (in scan order)

1. **Skill roster** — `ls ~/.claude/skills/` filtered for directories with `SKILL.md` (exclude `_common/`, `_templates/`).
2. **Frontmatter** — `name`, `description` extracted from every `SKILL.md`. Description is the only routing signal Claude sees at selection time.
3. **CAPABILITIES_SUMMARY** — HTML comment block at top of each `SKILL.md`. Lists declared capabilities + COLLABORATION_PATTERNS + BIDIRECTIONAL_PARTNERS + PROJECT_AFFINITY.
4. **Reference files** — `ls <skill>/reference/` count + total size. High reference count without usage is a maintenance-cost signal.
5. **Activity log** — `.agents/PROJECT.md` lines matching the skill name. Aggregate last-90-day count.
6. **Journal** — `.agents/<skill>.md` last-modified date and entry count. Stale journal + low activity = sunset signal.
7. **CLAUDE.md / `_common/`** — grep for skill name in repo CLAUDE.md and `_common/*.md`. Hard dependency.
8. **Pack membership** — `_common/SKILL_PACKS.md` entries containing the skill name.
9. **Profile coverage** — `~/.claude/profiles/*.json` `skills` arrays containing the skill name.
10. **Nexus routing** — `nexus/SKILL.md` and `nexus/reference/signal-keywords.md` mentions.

## Output schema (intermediate, not user-facing)

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

## Always

- Scan the **full** roster even when the user asks for a subset — subset filtering happens at CLASSIFY, not SCAN. Hidden dependencies cross subsets.
- Verify scan output before SCORE — empty fields likely mean a read error, not zero activity.
- Cache the inventory for the session; re-scan only on explicit FOLLOWUP mode.

## Never

- Skip sources to save time. Missing a Pack membership leads to incorrect impact analysis.
- Edit any file during SCAN — read-only.
- Trust frontmatter without validating CAPABILITIES_SUMMARY exists. Empty CAPABILITIES_SUMMARY is a maintenance signal in itself.
