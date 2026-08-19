# Nexus Confidence Gate

**Purpose:** Decide whether CLASSIFY has enough evidence to select a route or must ask one focused question.
**Read when:** Entering CLASSIFY, selecting among multiple valid routes, or deciding whether a reversible assumption is safe.

Confidence is a routing aid, not an authorization mechanism. Evaluate blocking unknowns first, then assign one discrete evidence band. Do not invent source weights, add “boosters,” or average away an unresolved dimension.

## Pipeline

```text
Gather evidence → type unknowns → blocker gate → evidence band → decision threshold → proceed or ask
```

Evidence sources, in authority order:

1. The user's current request and explicit corrections.
2. Observed repository/runtime state.
3. Project rules and `.agents/PROJECT.md`.
4. Git history as supporting context, never as authority to expand scope.

Absence of a source is not automatically a penalty. Use only sources relevant to the decision being made.

## Blocking Unknown Gate

Type uncertainty using `intent-clarification.md` before assigning a score.

| Dimension | Blocking when | Action |
|-----------|---------------|--------|
| `authority` | Permission to delete, publish, push, spend, deploy, or modify an external system is unclear | Ask; no confidence score can authorize the effect |
| `referent` | The target cannot be resolved from the request or observed state | Ask for the target |
| `goal` | Two valid interpretations produce materially different outcomes | Ask for the deciding axis |
| `scope` | The boundary changes risk, effect class, or the files/systems affected | Offer bounded scope options |
| `constraint` | An unstated limit would change the chosen approach | Surface the constraint that would otherwise be assumed |
| `outcome` | Success cannot be observed with available evidence | Agree on an observable or mark it `UNVERIFIED` |

Rules:

- Unresolved `authority` always blocks.
- Two or more materially valid interpretations always trigger `GATE`, regardless of the numeric band.
- A minor assumption may remain only when it is explicit, reversible, and cannot change the requested outcome.
- Batch missing dimensions into the one-question format defined by `intent-clarification.md`; do not ask a sequence of open-ended questions.

## Discrete Evidence Bands

Assign the highest band whose complete description is true. The bands are intentionally coarse; pseudo-precision is not evidence.

| Score | Evidence state | Default action |
|------:|----------------|----------------|
| `1.00` | Goal, target, scope, constraints, outcome, and authority are explicit; one route fits | Auto-route |
| `0.80` | All load-bearing dimensions are settled; only minor reversible assumptions remain | Route and state assumptions |
| `0.60` | One non-blocking dimension is partial, but a safe reversible default is established and rollback is clear | Proceed cautiously and record the default |
| `0.40` | A load-bearing dimension is unresolved or multiple material interpretations remain | Ask one focused question |
| `0.20` | Goal or target is mostly absent | Clarify before route selection |
| `0.00` | No task-shaped intent can be recovered | Answer the meta/factual request directly or ask what outcome is wanted |

`context_confidence < 0.60` is the mechanical GATE floor used by `routing-matrix.md`. The independent “2+ valid interpretations” rule still fires at any score.

## Decision Thresholds

| Decision | Minimum band | Additional condition |
|----------|--------------|----------------------|
| Chain selection | `0.80` | One best-fit Recipe/task type and no blocker |
| Agent routing | `0.80` | Role boundary is clear |
| Approach selection | `0.80` | Wrong choice is reversible and does not change scope |
| Recovery action | `0.80` | Failure class is known and rollback/checkpoint exists |
| Parallel vs sequential | `0.60` | Branches are independent, have owners, and define a merge gate |

Below the threshold, use `intent-clarification.md` § Routing Decision Output to present the smallest useful choice. Do not dump the routing matrix or confidence arithmetic.

## Reversibility and Safety Overrides

| Effect | Examples | Auto-proceed |
|--------|----------|--------------|
| Read-only | Inspect files, run non-mutating checks | Yes when the route is clear |
| Reversible workspace edit | Git-tracked code/docs edit with a known rollback | Yes within approved scope |
| Moderate | Config or migration with a tested rollback | Ask when project rules require it |
| Difficult/irreversible | Data deletion, external send, production deploy, payment, key rotation | Never infer authority |

The following bypass the confidence band and use Nexus `Ask First`/safety rules:

- credential, auth, permission, or encryption-key changes;
- destructive or bulk data operations;
- production deploys and external-system mutations;
- cost-incurring actions;
- changes affecting 10+ files, breaking APIs, or architecture when not already approved.

AUTORUN modes do not bypass these controls. Explicit approval settles `authority` only for the named effect and scope; it does not raise unrelated confidence dimensions.

## Decision Record

```yaml
_CONTEXT_SNAPSHOT:
  task: "<original request>"
  evidence:
    conversation: ["<decisive user statement>"]
    repository: ["<observed state>"]
    project: ["<applicable rule or journal fact>"]
    git: ["<supporting history, if relevant>"]
  dimensions:
    referent: settled | partial | blocking
    scope: settled | partial | blocking
    goal: settled | partial | blocking
    constraint: settled | partial | blocking
    authority: settled | blocking
    outcome: settled | partial | blocking
  context_confidence: 0.00 | 0.20 | 0.40 | 0.60 | 0.80 | 1.00
  assumptions: ["<explicit reversible assumptions only>"]
  decision: proceed | ask | direct_answer
```

Record the evidence that changed the decision, not every file inspected. Re-evaluate when the user corrects the interpretation, observed state contradicts an assumption, or the action's effect class changes.

## Phase Integration

### CLASSIFY

1. Gather only decision-relevant evidence.
2. Type unknowns and apply the blocker gate.
3. Assign a discrete band.
4. If the band clears the decision threshold and no blocker exists, select the route.
5. Otherwise ask one focused question, integrate the answer, and re-evaluate from evidence rather than adding a fixed score bonus.

### EXECUTE

- Pass the approved intent contract and explicit assumptions, not the scoring rationale, to specialists.
- If new evidence invalidates a load-bearing assumption, stop at the nearest reversible boundary and re-enter CLASSIFY/GATE.

### HANDOFF

Handoff completion confidence is owned by `handoff-validation.md`. It must not be substituted for context confidence: a specialist can be highly confident in work performed against the wrong intent.

### LEARN

Record routing corrections as categorical evidence: which dimension was missed, which route was corrected, and whether the correction changed outcome or only efficiency. Do not tune invented weights; update examples, decision boundaries, or fixtures only after repeated verified cases.
