# Council Mode — Persona Council (v4 fold-in)

Persona Council mode runs parallel multi-persona evaluation against a machine-readable Persona Contract. Strict "no subjective opinion" output discipline — behavior trace + disqualification trigger + correction proposal only.

## When to Use

- `nexus growth-acceptance` Phase 0 persona evaluation (required).
- `nexus acceptance` Phase 3B AI-user persona evaluation (Tier-S/A).
- Standalone: multi-persona disqualification check before launch.

## Persona Weights

| Weight | Meaning | Treatment |
|--------|---------|-----------|
| Primary | Must-pass (all success conditions must be met) | Block on FAIL |
| Secondary | Must-not-degrade (no new disqualification triggers) | Warn on regression |
| Non-target | Do not optimize for this persona | Ignore failures |
| Risk | Block on damage signals | Hard block |

## Org-Tier Cost Cap

Mandatory per Magi v4 C5 (enforced via Always/Never, no new guardrail).

| Org Tier | Persona Cap | Behavior |
|----------|-------------|----------|
| Solo | 0 | Skip Council entirely |
| SMB | 3 | Primary first; escalate only with remaining budget |
| Enterprise | 9 | Primary → Secondary → Non-target/Risk |

Never exceed cap with "just one more persona". If exhausted, defer to next session.

## Engine Diversity (Tier-S/A Required)

For Tier-S/A evaluations, Persona Council **MUST** run via `rally engine-paradigm` mode (Codex + Antigravity + Claude). Single-engine Council:
- **Tier-S**: forbidden.
- **Tier-A**: advisory only.
- **Tier-B/C**: allowed.

Rationale: correlated hallucination risk per Magi v4 G16 fold-in.

## Confidence Discipline

All Council output tagged `[hypothesis]` confidence by default. Promotion to `[validated]` requires Voice/Trace real-user calibration per Insight Ledger Survivor Bias rule.

## Persona Contract Schema

```yaml
persona_id: <unique id>
weight: primary | secondary | non-target | risk
situation: <one-sentence current context of the persona>
goal: <what the persona is trying to accomplish in this session>
fear: [<concern 1>, <concern 2>, ...] # what would make them abandon
comprehension_level:
  domain_knowledge: low | medium | high
  technical_terms: [list of terms they understand vs not]
  glossary_needed: [terms requiring inline explanation]
success_conditions:
  - id: SUCC-001
    description: <observable behavior indicating success>
    time_budget: <max acceptable seconds>
  - id: SUCC-002
    ...
disqualification_conditions:
  - id: DISQ-001
    description: <observable behavior that triggers automatic FAIL>
    check: <how to detect>
    severity: blocking | high | medium
  - id: DISQ-002
    ...
```

## Output Schema (Strict — No Free-Form)

```yaml
council_evaluation:
  persona_id: <ref>
  target_artifact: <screen/flow/copy under evaluation>
  result: PASS | FAIL | INCONCLUSIVE
  behavior_trace:
    - step: 1
      action: <what persona did>
      observation: <what they saw>
      duration_seconds: <numeric>
    - step: 2
      ...
  disqualification_triggers: [<DISQ-ID list, empty if none>]
  success_achieved: [<SUCC-ID list, empty if none>]
  correction_proposals:
    - target: <element id>
      change: <specific concrete change>
      rationale: <which disqualification this addresses>
```

## Forbidden Outputs

- Subjective opinions ("seems good", "feels nice", "I think users will…").
- Free-form recommendations outside the `correction_proposals` schema.
- Aggregate "overall verdict" outside per-persona `result` field.

## Always / Never Recap

**Always:**
- Emit Persona Contract first (situation/goal/fear/comprehension/success/disqualification).
- Produce only behavior-trace YAML — no free-form opinion.
- Respect Org-Tier persona cap.
- For Tier-S/A: run via `rally engine-paradigm` engine diversity.
- Tag output as `[hypothesis]` confidence by default.

**Never:**
- Emit subjective opinions.
- Exceed Org-Tier persona cap.
- Rely on single-engine evaluation for Tier-S (correlated hallucination risk).
