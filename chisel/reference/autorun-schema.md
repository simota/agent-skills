# AUTORUN / Hub Schemas

**Purpose:** Chisel-specific `_STEP_COMPLETE.Output` and `NEXUS_HANDOFF` payload fields. The protocol itself (mode semantics, `_AGENT_CONTEXT` input, error handling) lives in `_common/AUTORUN.md`; the canonical handoff envelope lives in `_common/HANDOFF.md`.
**Read when:** Emitting `_STEP_COMPLETE` at the end of an AUTORUN step, or responding to `## NEXUS_ROUTING`.

---

## `_STEP_COMPLETE`

```yaml
_STEP_COMPLETE:
  Agent: Chisel
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: "specified prompt + ambiguity ledger"
    artifact_type: "prompt_specification | ambiguity_ledger | role_decomposition | prompt_audit | specified_brief"
    parameters:
      detections: "[count]"
      dispositions: "quantify:N behavioralize:N criteria:N decompose:N audience:N condition:N date:N parameterize:N keep:N delete:N"
      unresolved_parameters: "[count]"
      length_delta: "[+/- lines vs source]"
  Validations:
    intent_preserved: "[yes | flagged]"
    exit_checklist: "[passed | failed:<item numbers>]"
    fabricated_numbers: "[none | flagged]"
  Next: [NextAgent] | DONE
  Reason: [Why this next step]
```

`BLOCKED` is the correct status when the source's own purpose admits two incompatible readings — every downstream translation would inherit the wrong one. Return it for the hub's `GATE`; never resolve it by guessing.

---

## `NEXUS_HANDOFF` — Chisel-specific fields

Envelope per `_common/HANDOFF.md`. Surface these inline:

```yaml
NEXUS_HANDOFF:
  Agent: Chisel
  Chisel_findings:
    recipe: spec | scan | role | audit | brief
    detections_by_class: { quality: N, quantity: N, explanation: N, style: N, design: N, technical: N, judgment: N, open: N }
    kept_open: [{ term: <text>, reason: executor-has-better-information | reversible | premature-formatting }]
    routed_to_enforcing_layer: [{ requirement: <text>, layer: validator | permission | retrieval | approval | human-review }]
    interpretations: [{ source: <text>, reading_chosen: <text> }]   # each becomes a hub DEC-n
    exit_checklist: pass | fail:<items>
```

`interpretations` is the load-bearing field for the hub: every reading chosen where the source admitted more than one is a judgment call made without the user, and belongs in the Decision Ledger.

---

## `brief` Recipe Output

When invoked at the Nexus `SPECIFY` phase, return `SPECIFIED_BRIEF` instead of the four-section deliverable. Schema, gate, and injection rules → `nexus/reference/specify-phase.md`.
