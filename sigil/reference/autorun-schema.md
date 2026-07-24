# Sigil — AUTORUN `_STEP_COMPLETE` Schema

When invoked with `_AGENT_CONTEXT`:
- Parse `Role / Task / Task_Type / Mode / Chain / Input / Constraints / Expected_Output`.
- Execute the canonical six-phase pipeline `SCAN → DISCOVER → CRAFT → INSTALL → VERIFY → ATTUNE` (or the Skill Evolution path when refresh is signalled).
- Skip verbose narration; produce final report only.
- Emit the completion block below.

```yaml
_STEP_COMPLETE:
  Agent: Sigil
  Task_Type: SKILL_GEN | SKILL_REFRESH | SKILL_AUDIT | SYNC_REPAIR | ATTUNE_CALIBRATION
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    project: <name + detected stack>
    skills_generated: <count>
    skills_updated: <count>
    skills_archived: <count>
    average_quality: <0-12>
    per_skill:
      - name: <kebab-case-name>
        type: Micro | Full
        score: <0-12>
        description_chars: <int>
        description: <verbatim frontmatter description>
        install_paths:
          - .claude/skills/<name>/SKILL.md
          - .agents/skills/<name>/SKILL.md
    sync_status: in_sync | drift_detected | drift_repaired
    evolution_opportunities: [<short label>, ...]
  Handoff:
    schema: see `_common/HANDOFF.md`
    recommended_next:
      - Judge   # when score 6-8 on any skill
      - Grove   # when new skill directories created
      - Lore    # when reusable pattern detected
      - Nexus   # to broadcast new-skill availability
  Next: <agent name> | DONE
  Reason: <terse cause for non-SUCCESS, or "all skills passed 9+/12 with sync intact" for SUCCESS>
```

Full schema definitions → `_common/AUTORUN.md`.
