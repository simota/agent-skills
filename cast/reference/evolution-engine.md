# Cast Evolution Engine

Purpose: Define drift detection, severity assessment, change application, confidence decay, and identity protection for `EVOLVE`.

## Contents

1. Drift axes
2. Severity levels
3. Merge rules
4. Log and versioning
5. Confidence decay
6. Batch evolution
7. Identity protection

## Drift Detection

### Four Drift Axes

| Axis | Detect | Threshold |
|---|---|---|
| `Goals` | Objective shift, changed JTBD, changed priorities | `>=1` significant goal shift |
| `Pain Points` | New complaints or resolved issues | `>=1` pain point added or removed |
| `Behavior` | Device mix, frequency, flow, navigation changes | `>=2` behavioral attributes changed |
| `Segment` | Segment boundaries or dominant user type changes | Segment boundary changes |

### Signal Sources

| Source | Typical drift signal |
|---|---|
| Trace | session pattern change, device mix change, drop-off shift |
| Voice | feedback themes, NPS shift, complaint emergence |
| Pulse | funnel change, cohort shift, engagement change |
| Researcher | new interview findings, revised segments, journey change |

## Impact Assessment

| Severity | Criteria | Action |
|---|---|---|
| `Minor` | `1` attribute within `1` axis | Auto-apply, minor version bump |
| `Moderate` | `2-3` attributes across `1-2` axes | Auto-apply with notification |
| `Significant` | `4+` attributes across `2+` axes | Ask first |
| `Identity` | Role or category would change | Block and create a new persona |

### Typical Change Classes

| Class | Examples |
|---|---|
| Minor | device share shift `<20%`, single behavior refinement, one pain point update |
| Moderate | tech-level shift, usage-frequency change, multiple pain-point updates |
| Significant | primary goal change, major behavior shift, segment boundary change, Echo mapping change |
| Identity | role change, category change, fundamental user-type shift |

## Evolution Application

### Merge Rules

| Rule | Meaning |
|---|---|
| Newer wins | More recent evidence takes precedence |
| Higher confidence wins | When timestamps are similar, stronger evidence wins |
| Additive preferred | Add or refine instead of replacing without cause |
| Evidence required | Every change cites its source |
| `[inferred]` preserved | Keep inferred markers until real data replaces them |

### Section-Level Behavior

| Section | Evolution behavior |
|---|---|
| `Profile` | Update attributes except Core Identity |
| `Quote` | Replace only when new evidence is clearly more representative |
| `Goals / Frustrations / Behaviors` | Maintain `3`; reorder, refine, add, or remove |
| `Emotion Triggers` | Refine trigger wording and polarity scores |
| `Context Scenarios` | Add or update scenarios |
| `JTBD` | Refine, but rarely replace |
| `Echo Testing Focus` | Update based on fresh friction data |
| Extended sections | Update attribute-by-attribute with evidence |

### Frontmatter Updates

On accepted evolution:

- bump minor `version`
- set `status: active`
- refresh `updated`
- increment `evolution_count`
- recalculate `confidence`

## Evolution Log

Append one row per accepted evolution:

| Field | Meaning |
|---|---|
| `Version` | New version |
| `Date` | ISO date |
| `Source` | Triggering evidence source |
| `Changes` | Concise summary |
| `Confidence Delta` | Signed change in confidence |

## Cross-Agent Confidence Feedback

Downstream agents feed findings back to Cast to close the persona lifecycle loop.

| Source Agent | Signal | Cast Action | Confidence Effect |
|-------------|--------|-------------|-------------------|
| **Echo** | Walkthrough friction findings for a persona | FUSE — adjust persona pain points and emotion triggers | +0.05 if findings align with persona; flag drift if misaligned |
| **Echo** | Synthetic persona walkthrough result | FUSE — validate or challenge proto-persona attributes | Positive validation: +0.10 toward promotion; Negative: flag for review |
| **Plea** | Demand calibration report (`[validated]`/`[supported]`/`[hypothesis]`) | FUSE — update persona coverage gaps | `[validated]` demands: +0.05; `[hypothesis]` with no match: flag persona gap |
| **Plea** | Persona coverage gap (demands from segments not in registry) | CONJURE — consider new persona candidate | New persona at proto tier (0.30) |
| **Trace** | Behavioral validation data | EVOLVE — existing path (drift detection) | Per standard drift rules |
| **Researcher** | Interview/survey validation | FUSE — promote proto → active | +0.20 (interview) / +0.15 (survey) per validation rules |

### Feedback Handoff Format

Downstream agents include the following in their `_STEP_COMPLETE` or handoff when persona-relevant findings exist:

```yaml
PERSONA_FEEDBACK:
  source_agent: "[Echo | Plea | Trace | Researcher]"
  persona_id: "[registry ID]"
  signal_type: "[validation | drift | gap | calibration]"
  findings: "[summary]"
  confidence_recommendation: "[+N / -N / review]"
```

## Confidence Decay

| Age since update | Rule |
|---|---|
| `<30` days | No decay |
| `30-60` days | `-0.05/week` |
| `60-90` days | `-0.10/week` |
| `90+` days | Freeze and recommend archival review |

### Notifications

| Day | Notification | Severity |
|---|---|---|
| `30` | Persona stale warning | Info |
| `45` | Confidence decay notice | Warning |
| `60` | Faster decay notice | Warning |
| `90` | Archival review recommendation | Critical |

## Batch Evolution

When running `EVOLVE ALL`:

1. Collect new data.
2. Compare each active persona.
3. Rank by severity.
4. Auto-apply minor/moderate changes.
5. Ask before significant changes.
6. Return a batch report with `persona / severity / axes / changes / confidence`.

## Core Identity Protection

### Immutable Fields

- `Role`
- `category`
- `service`

### Identity Change Protocol

1. Flag as `Identity`.
2. Trigger `ON_IDENTITY_CHANGE`.
3. If approved, create a new persona and archive the old one.
4. Cross-reference the old persona in `Source Analysis`.
5. Update registry coverage and lifecycle state.
