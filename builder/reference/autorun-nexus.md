# Builder AUTORUN & Nexus Integration

## Agent Collaboration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT PROVIDERS                          │
│  Forge → Prototypes / Mock data / UI components             │
│  Guardian → Commit structure / Branch strategy              │
│  Scout → Bug investigation / Root cause analysis            │
│  Plan → Implementation plan / Requirements                  │
│  Artisan → Frontend components needing backend              │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
            ┌─────────────────┐
            │     BUILDER     │
            │  Code Craftsman │
            └────────┬────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT CONSUMERS                          │
│  Radar → Test requests       Guardian → PR preparation      │
│  Judge → Code review         Tuner → DB optimization        │
│  Sentinel → Security audit   Canvas → Domain diagrams       │
│  Quill → Documentation       Nexus → AUTORUN results        │
└─────────────────────────────────────────────────────────────┘
```

---

## AUTORUN Support (Nexus Autonomous Mode)

When invoked in Nexus AUTORUN mode:
1. Parse `_AGENT_CONTEXT` to understand task scope and constraints
2. Execute normal work (type-safe implementation, error handling, API integration)
3. Skip verbose explanations, focus on deliverables
4. Append `_STEP_COMPLETE` with full implementation details

### Input Format (_AGENT_CONTEXT)

```yaml
_AGENT_CONTEXT:
  Role: Builder
  Task: [Specific implementation task from Nexus]
  Mode: AUTORUN
  Chain: [Previous agents in chain, e.g., "Scout → Builder"]
  Input: [Handoff received from previous agent]
  Constraints:
    - [Time/scope constraints]
    - [Technical constraints]
    - [Quality requirements]
  Expected_Output: [What Nexus expects - files, tests, etc.]
```

### Output Format (_STEP_COMPLETE)

```yaml
_STEP_COMPLETE:
  Agent: Builder
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    implementation_type: [Feature / BugFix / Refactor / Integration]
    files_changed:
      - path: [file path]
        type: [created / modified / deleted]
        changes: [brief description]
    patterns_applied:
      - [DDD pattern / validation / error handling / etc.]
    test_coverage:
      status: [Generated / Partial / Needs Radar]
      files: [test file paths if generated]
    type_safety:
      status: [Complete / Partial / Needs Review]
      notes: [any type issues]
  Handoff:
    Format: BUILDER_TO_RADAR_HANDOFF | BUILDER_TO_GUARDIAN_HANDOFF | etc.
    Content: [Full handoff content for next agent]
  Artifacts:
    - [Implementation files]
    - [Test skeletons]
    - [Configuration updates]
  Risks:
    - [Potential issues / edge cases not covered]
  Next: Radar | Guardian | Tuner | Sentinel | VERIFY | DONE
  Reason: [Why this next step is recommended]
```

---

## Nexus Hub Mode

When user input contains `## NEXUS_ROUTING`, treat Nexus as hub.

- Do not instruct other agent calls (do not output `$OtherAgent` etc.)
- Always return results to Nexus (append `## NEXUS_HANDOFF` at output end)
- `## NEXUS_HANDOFF` must include at minimum: Step / Agent / Summary / Key findings / Artifacts / Risks / Open questions / Suggested next agent / Next action

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: [AgentName]
- Summary: 1-3 lines
- Key findings / decisions:
  - ...
- Artifacts (files/commands/links):
  - ...
- Risks / trade-offs:
  - ...
- Open questions (blocking/non-blocking):
  - ...
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name if any, e.g., ON_DB_MIGRATION]
  - Question: [Question for user]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] → A: [User's answer]
- Suggested next agent: [AgentName] (reason)
- Next action: CONTINUE (Nexus automatically proceeds)
```
