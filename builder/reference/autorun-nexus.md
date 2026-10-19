# Builder AUTORUN & Nexus Integration

## Agent Collaboration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT PROVIDERS                          │
│  Forge → Prototypes / Mock data / UI components             │
│  Guardian → Commit structure / Branch strategy              │
│  Scout → Bug investigation / Root cause analysis            │
│  Sherpa → Implementation plan / Requirements                │
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

### Input / Output Schema

`_AGENT_CONTEXT` input follows `_common/AUTORUN.md`; the canonical `_STEP_COMPLETE` schema is `reference/autorun-schema.md` — do not restate it here.

---

## Nexus Hub Mode

When user input contains `## NEXUS_ROUTING`, treat Nexus as hub.

- Do not instruct other agent calls (do not output `$OtherAgent` etc.)
- Always return results to Nexus (append `## NEXUS_HANDOFF` at output end)
- `## NEXUS_HANDOFF` required fields follow `_common/HANDOFF.md`: Summary / Next (Suggested next agent + Next action) / Verified (evidence objects, whenever the handoff claims something passes, builds, or is done). Step / Agent are optional; Key findings / Artifacts / Risks / Open questions are recommended.

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
- Verified (when claiming pass/build/done):
  - claim: [...] / command: [...] / exit_code: [...]
- Suggested next agent: [AgentName] (reason)
- Next action: CONTINUE (Nexus automatically proceeds)
```
