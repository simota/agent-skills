# Orbit Nexus Integration

Purpose: load this when Orbit receives Nexus markers or must emit Nexus-compatible completion signals. It preserves mode priority, `_AGENT_CONTEXT`, `_STEP_COMPLETE:`, and `## NEXUS_HANDOFF`.

## Contents

- Mode priority
- `_AGENT_CONTEXT` contract
- `_STEP_COMPLETE:` template
- `## NEXUS_HANDOFF` template

## Mode Priority

```text
Receive input
  -> if `## NEXUS_ROUTING` exists: Nexus Hub Mode
  -> else if `_AGENT_CONTEXT` exists: AUTORUN Mode
  -> else: Interactive Mode
```

| Input characteristics | Operating mode | Output format | `_STEP_COMPLETE` |
|-----------------------|----------------|---------------|------------------|
| `## NEXUS_ROUTING` present | Nexus Hub Mode | `## NEXUS_HANDOFF` block | do not output |
| `_AGENT_CONTEXT` present, no `## NEXUS_ROUTING` | AUTORUN Mode | `_STEP_COMPLETE:` | required |
| neither marker present | Interactive Mode | Japanese prose | do not output |
| both markers present | Nexus Hub Mode takes priority | `## NEXUS_HANDOFF` block | do not output |

Rules:

- `## NEXUS_ROUTING` always wins over `_AGENT_CONTEXT`.
- Nexus Hub Mode returns through Nexus only; do not instruct direct agent-to-agent calls.
- Preserve token spelling exactly.

## `_AGENT_CONTEXT` Contract

When Orbit is invoked in `AUTORUN` mode, parse these fields before acting:

- `Role`
- `Task`
- `Task_Type`
- `Mode`
- `Chain`
- `Input`
- `Constraints`
- `Expected_Output`

Rules:

- Execute silently with contract-first behavior.
- Keep the Orbit workflow intact; only the outer response format changes.
- Use `_STEP_COMPLETE:` exactly once at the end of the run.

## `_STEP_COMPLETE:` Template

Required in `AUTORUN` mode only.

```text
_STEP_COMPLETE:
- Agent: Orbit
- Task_Type: LOOP_OPS
- Status: SUCCESS | PARTIAL | BLOCKED | FAILED
- Output: <contract-focused summary>
- Handoff: <target agent or NONE>
- Next: <CONTINUE|VERIFY|DONE>
- Reason: <why this next action is safest>
```

Rules:

- Do not emit `_STEP_COMPLETE:` in Nexus Hub Mode or Interactive Mode.
- Keep `Task_Type` and field labels exact.
- `Next` must remain one of `CONTINUE`, `VERIFY`, or `DONE`.

## `## NEXUS_HANDOFF` Template

Required when input contains `## NEXUS_ROUTING`.

```markdown
## NEXUS_HANDOFF
Step: <step>
Agent: Orbit
Summary: <short summary>
Key findings / decisions:
- <finding or decision>
Artifacts:
- <artifact path or NONE>
Risks / trade-offs:
- <risk or trade-off or NONE>
Open questions:
- <question or NONE>
Pending Confirmations:
- <confirmation still needed or NONE>
User Confirmations:
- <confirmed user constraint or NONE>
Suggested next agent: <agent or NONE>
Next action: <single safest next action>
```

Rules:

- Preserve the heading and field labels exactly.
- Keep one suggested next agent and one next action.
- Use artifact references instead of raw logs when possible.
