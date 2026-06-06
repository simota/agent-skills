# Integration Patterns

> Purpose: Read this when Rally enters or leaves a Nexus or Sherpa chain, or when chain type changes the team design.

## Table of Contents

1. Escalation Criteria
2. Collaboration Patterns
3. Chain-Type Team Mapping
4. Handoff Templates
5. Nexus Internal Parallelism vs Rally

## Escalation Criteria

Escalate from Nexus or Sherpa to Rally when any of these conditions apply:

| Condition | Example | Rally response |
|-----------|---------|----------------|
| `2+` independent implementation steps | frontend + backend | split into parallel teammates |
| `4+` files across `2+` domains | API + UI + DB + tests | choose a multi-role team pattern |
| Sherpa emits `parallel_group` | decomposed Epic with grouped steps | accept `SHERPA_TO_RALLY_HANDOFF` |
| Task explicitly requests parallel execution | "Implement these features in parallel" | direct Rally execution |
| Chain includes implementation + test + docs | Builder + Radar + Quill | use `Code/Test/Docs Triple` |
| Multiple independent bug fixes exist | `3+` unrelated bugs | use `Feature Parallel` |

Do not escalate to Rally for:

- investigation-only chains
- single-agent chains
- purely sequential chains
- changes under `10` lines total
- high-risk security work that should stay sequential with checkpoints

## Collaboration Patterns

| Pattern | Flow | Best for |
|---------|------|----------|
| Pattern A: Plan-then-Rally | Sherpa -> Rally -> Teammates -> Rally -> Nexus | complex features that need decomposition first |
| Pattern B: Nexus-delegates-Rally | Nexus -> Rally -> Teammates -> Rally -> Nexus | parallel implementation discovered mid-chain |
| Pattern C: Direct Rally | User -> Rally -> Teammates -> Rally -> User | explicit parallel execution requests |
| Pattern D: Rally-with-Specialist | Rally -> Specialist teammate -> Rally | investigation, review, or specialist side work |
| Pattern E: Learning Loop | Execute -> HARMONIZE -> Lore or Judge feedback -> updated defaults | cross-session optimization |

## Chain-Type Team Mapping

| Nexus chain type | Rally team pattern | Teammate roles | Typical size |
|------------------|-------------------|----------------|--------------|
| `FEATURE/L` | Frontend/Backend Split | Artisan + Builder + Radar | `3` |
| `FEATURE/fullstack` | Frontend/Backend Split | Artisan + Builder | `2-3` |
| `FEATURE/multi` | Feature Parallel | Builder x N | `2-4` |
| `BUG/multiple` | Feature Parallel | Builder x N | `2-3` |
| `REFACTOR/arch` | Feature Parallel | Zen x N | `2-4` |
| `SECURITY/full` | Specialist Team | Sentinel + Probe | `2` |
| `TEST/coverage` | Specialist Team | Radar + Voyager | `2` |
| `MODERNIZE/stack` | Feature Parallel | Builder x N | `2-4` |
| `DOCS/full` | Code/Test/Docs Triple | Quill + Canvas + Showcase | `3` |
| `INFRA/multi` | Feature Parallel | general-purpose x N | `2-3` |

## Handoff Templates

### `## NEXUS_TO_RALLY_CONTEXT`

```markdown
## NEXUS_TO_RALLY_CONTEXT
- Task: [task to parallelize]
- Scope:
  - [scope detail]
- File Restrictions:
  - [file restriction]
- Max Team Size: [limit]
- Expected Output: [deliverables]
```

### `## NEXUS_TO_RALLY_HANDOFF`

Use the same fields as `## NEXUS_TO_RALLY_CONTEXT`. Keep this header for compatibility when upstream already emits it.

```markdown
## NEXUS_TO_RALLY_HANDOFF
- Task: [task to parallelize]
- Scope:
  - [scope detail]
- File Restrictions:
  - [file restriction]
- Max Team Size: [limit]
- Expected Output: [deliverables]
```

### `## SHERPA_TO_RALLY_HANDOFF`

```markdown
## SHERPA_TO_RALLY_HANDOFF
- Epic: [epic name]
- Parallel Groups:
  - Group A: [task list]
    - Files: [file list]
  - Group B: [task list]
    - Files: [file list]
- Dependencies:
  - Group B depends on Group A: [reason]
- Constraints:
  - [constraint detail]
```

### `## USER_TO_RALLY_REQUEST`

```markdown
## USER_TO_RALLY_REQUEST
- Goal: [parallel outcome requested]
- Scope:
  - [work item]
- Constraints:
  - [limits or approvals]
- Expected Output:
  - [deliverables]
```

### `## RALLY_TO_NEXUS_HANDOFF`

```markdown
## RALLY_TO_NEXUS_HANDOFF
- Team: [team name]
- Teammates: [count]
- Tasks Completed: [completed]/[total]
- Files Changed:
  - [file list]
- Build Status: PASS/FAIL
- Test Status: PASS/FAIL
- Risks:
  - [risk list]
- Next Recommended: [next agent] (reason)
```

### `## RALLY_TO_GUARDIAN_HANDOFF`

```markdown
## RALLY_TO_GUARDIAN_HANDOFF
- Summary: [what the team implemented]
- Files Changed:
  - [file list]
- Verification:
  - Build: PASS/FAIL
  - Tests: PASS/FAIL
  - Lint/Typecheck: PASS/FAIL
- PR Risks:
  - [risk list]
- Suggested Commit Grouping:
  - [grouping suggestion]
```

### `## RALLY_TO_RADAR_HANDOFF`

```markdown
## RALLY_TO_RADAR_HANDOFF
- Integrated Scope: [what needs verification]
- Files Changed:
  - [file list]
- High-Risk Areas:
  - [risk area]
- Existing Verification:
  - [what already passed]
- Requested Tests:
  - [unit/integration/e2e focus]
```

### `## RALLY_TO_LORE_HANDOFF`

```markdown
## RALLY_TO_LORE_HANDOFF
- Pattern: [team pattern or lesson]
- Evidence:
  - Task Type: [type]
  - Team Size: [count]
  - TES: [score or grade]
- Recommendation:
  - [actionable lesson]
- Confidence: HIGH/MEDIUM/LOW
```

### `## RALLY_TO_JUDGE_HANDOFF`

```markdown
## RALLY_TO_JUDGE_HANDOFF
- Scope: [integrated output]
- Files Changed:
  - [file list]
- Verification Status:
  - Build: PASS/FAIL
  - Tests: PASS/FAIL
  - Lint/Typecheck: PASS/FAIL
- Review Focus:
  - [quality concern]
```

### `QUALITY_FEEDBACK`

```markdown
QUALITY_FEEDBACK
- Source: Judge
- Summary: [quality signal]
- Findings:
  - [finding]
- Recommended Action:
  - [action]
```

### Nexus AUTORUN and Hub Mode

AUTORUN handoff:

```text
_AGENT_CONTEXT:
  Role: Rally
  Task: Execute parallel implementation
  Mode: AUTORUN
  Chain: [upstream chain]
  Input: [handoff payload]
  Constraints:
    - Max team size: 4
    - File ownership from upstream decomposition
  Expected_Output: Unified implementation result
```

Hub mode exchange:

```markdown
## NEXUS_ROUTING
- Task: Implement features A, B, C in parallel
- Chain: [...previous agents...] -> Rally -> [...next agents...]
- Context: [accumulated context]

## NEXUS_HANDOFF
- Step: X/Y
- Agent: Rally
- Summary: Parallel execution completed
- Key findings/decisions: [summary]
- Artifacts: [team composition, ownership map, changed files]
- Suggested next agent: [agent]
```

## Nexus Internal Parallelism vs Rally

| Aspect | Nexus `_PARALLEL_BRANCHES` | Rally teams |
|--------|----------------------------|-------------|
| Execution model | single session, simulated parallel | multi-session, true parallel |
| Max branches | `4` | `10` teammates, `2-4` preferred |
| File ownership | `file_ownership` YAML | teammate `ownership_map` |
| Conflict handling | `CONCAT` / `RESOLVE` / `MANUAL` | `ON_RESULT_CONFLICT` |
| Guardrails | per-branch L1-L4 | Rally monitoring via `TaskList` |
| Best use | lightweight branches | real implementation, mixed roles, heavy work |

Use Rally when:

- each branch likely exceeds `~50` lines of code,
- different agent roles are needed, or
- ownership and synthesis need active supervision.
