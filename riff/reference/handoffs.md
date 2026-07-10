# Handoff Templates

**Purpose:** Handoff format between Riff and other agents.
**Read when:** Handing off session outcomes to another agent.

---

## Riff → Magi (Decision Handoff)

Ask Magi to make a decision on the set of options that emerged during the session.

```yaml
RIFF_TO_MAGI_HANDOFF:
  context: [the brainstorm theme and background]
  candidates:
    - name: [option 1]
      description: [summary]
      pros: [benefits raised during the session]
      cons: [concerns raised during the session]
    - name: [option 2]
      description: [summary]
      pros: [benefits]
      cons: [concerns]
  evaluation_axes:
    - [evaluation axis 1 judged important during the session]
    - [evaluation axis 2]
  session_insights:
    - [insight that affects the decision]
  decision_needed: [what needs to be decided]
```

---

## Riff → Spark (Feature Seed Handoff)

Pass a promising idea seed to Spark to develop into a feature proposal.

```yaml
RIFF_TO_SPARK_HANDOFF:
  idea_seed:
    title: [idea title]
    one_liner: [one-line summary]
    origin: [which question it grew out of]
  user_context:
    pain_point: [the problem to solve]
    target_user: [the intended user]
  exploration_notes:
    - [exploration note 1 from the session]
    - [exploration note 2]
  constraints:
    - [constraint the user raised]
  open_questions:
    - [a question still unanswered]
```

---

## Riff → Accord (Requirement Seed Handoff)

Pass a concept to Accord as a seed for requirements definition.

```yaml
RIFF_TO_ACCORD_HANDOFF:
  concept:
    title: [concept title]
    summary: [2-3 sentence summary]
  stakeholder_perspectives:
    - perspective: [perspective 1 (e.g. end user)]
      needs: [needs]
    - perspective: [perspective 2 (e.g. ops team)]
      needs: [needs]
  scope_direction:
    must_have: [absolutely necessary elements]
    nice_to_have: [elements that would be nice to have]
    explicitly_excluded: [elements the session decided to exclude]
  risks:
    - [risk]
```

---

## Riff → Void (Pruning Handoff)

Ask Void to run a YAGNI check on the ideas that expanded during the session.

```yaml
RIFF_TO_VOID_HANDOFF:
  target: [the target to verify]
  current_scope:
    - [element 1]
    - [element 2]
    - [element 3]
  suspicion: [the part suspected of being excessive]
  session_context: [the dialogue context for why it felt excessive]
```

---

## Flux → Riff (Reframed Problem Handoff)

Receive Flux's reframing result and begin a dialogue-driven exploration.

```yaml
FLUX_TO_RIFF_HANDOFF:
  original_problem: [the original problem]
  reframed_as: [the reframed problem]
  key_assumption_reversed: [the assumption that was reversed]
  exploration_request: [the direction Riff should explore]
```

---

## Field → Riff (Research-to-Brainstorm Handoff)

Receive research findings and develop ideas from them.

```yaml
RESEARCHER_TO_RIFF_HANDOFF:
  research_topic: [research theme]
  key_findings:
    - [finding 1]
    - [finding 2]
  implications: [what is implied]
  brainstorm_request: [the angle Riff should explore]
```
