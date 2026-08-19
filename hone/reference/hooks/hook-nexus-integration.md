# Nexus Integration

Purpose: Read this when Hone runs under Nexus `AUTORUN`, when the input contains `## NEXUS_ROUTING`, or when you need `_STEP_COMPLETE:` / `## NEXUS_HANDOFF` templates.

## Contents

- [AUTORUN agent context](#autorun-agent-context)
- [AUTORUN step completion](#autorun-step-completion)
- [NEXUS handoff format](#nexus_handoff-format)
- [Nexus routing integration](#nexus-routing-integration)

## AUTORUN Agent Context

When Nexus invokes Hone in `AUTORUN` mode:

```yaml
_AGENT_CONTEXT:
  Role: Hone
  Task: [Specific hook task]
  Input:
    request: [User request]
    current_hooks: [Current hook summary]
    project_type: [Project type]
  Constraints:
    - Change only the `hooks` section in settings.json
    - Create a backup before modification
    - Remind the user to restart the session
  Expected_output:
    - Settings changes
    - Scripts created
    - Verification result
```

## AUTORUN Step Completion

After Hone finishes, append:

```yaml
_STEP_COMPLETE:
  Agent: Hone
  Status: SUCCESS|PARTIAL|BLOCKED|FAILED
  Output:
    hooks_configured: [Configured hooks]
    scripts_created: [Created scripts]
    settings_modified: true|false
    backup_created: true|false
    verification: [Verification summary]
  Risks:
    - [Risk item if any]
  Reminders:
    - Session restart required
  Next: [Next agent]|DONE
```

## NEXUS_HANDOFF Format

When returning results to Nexus hub, use `## NEXUS_HANDOFF` and preserve the broader field contract defined in `SKILL.md`.

```markdown
## NEXUS_HANDOFF

### Step: Hone
**Agent:** Hone
**Summary:** [One-line summary]

### Key findings
- [Finding]

### Artifacts
- **settings.json:** [Changed content]
- **Scripts:** [Created or updated scripts]
- **Backup:** [Backup information]

### Verification
- `/hooks`: [Result]
- `claude --debug`: [Result]
- Script test: [Result]

### Risks
- [Risk or follow-up]
- Session restart required

### Open questions
- [Question if any]

### Pending Confirmations (Trigger/Question/Options/Recommended)
- [Confirmation item if any]

### User Confirmations
- [Accepted confirmation if any]

### Next
**Suggested next agent:** [Next agent]
**Next action:** [Next action]
```

## Nexus Routing Integration

| Task Type | Chain | Use when |
|-----------|-------|----------|
| `HOOKS` | `Hone` | Configure or debug Claude Code hooks |
| `HOOKS/security` | `Sentinel -> Hone` | Turn security requirements into hooks |
| `HOOKS/quality` | `Hone -> Radar` | Pair quality-gate hooks with test verification |
| `INFRA/hooks` | `Hone -> Gear` | Connect hooks with infrastructure or CI/CD work |
