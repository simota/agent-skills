# RACI Matrix Reference

Purpose: Assign unambiguous responsibility for every spec item, decision, or deliverable using RACI (or variants DACI / RAPID). Accord attaches a RACI column to L3 and to major decisions so that every spec line has a named accountable owner.

## Scope Boundary

- **accord `raci`**: Responsibility assignment matrix (this document).
- **accord `stakeholder` (elsewhere)**: Who the stakeholders are and how to engage them.
- **accord `story-map` / `vision` / `requirements` / `detail` / `ac` (elsewhere)**: The content being assigned.
- **magi (elsewhere)**: Multi-perspective decision arbitration.
- **sherpa (elsewhere)**: Atomic step execution (RACI feeds into step ownership).

## Core RACI

```
R  Responsible  — person(s) who do the work
A  Accountable  — the one person who owns the outcome (must be exactly one)
C  Consulted    — two-way communication before decision/action
I  Informed     — one-way communication after decision/action
```

### Critical rules

1. **Exactly one A per row.** Multiple A's = no one is accountable.
2. **A cannot be blank.** Every row needs an owner.
3. **R can be multiple.** Teams do work collaboratively.
4. **C means bidirectional.** Input + response; not just notification.
5. **I is one-way.** Heads-up only, no expectation of response.
6. **A and R may be the same person.** For single-owner tasks.

### Matrix shape

```
              Alice   Bob    Carol   Dave
Decide KPI      A      C      R       I
Draft spec      C      A      R       I
Sign off        I      A      C       —
Implement       —      R      R       A
Test            —      I      C       A/R
```

## RACI Variants

| Variant | Adds | Use when |
|---------|------|----------|
| **RASCI** | S = Support (contributes resources) | Large, cross-functional programs |
| **RACI-VS** | V = Verifier, S = Signatory | Regulated industries (audit trail) |
| **DACI** | Driver / Approver / Contributor / Informed — decision-focused | One-off decisions rather than ongoing work |
| **RAPID** | Recommend / Agree / Perform / Input / Decide (Bain) | Complex strategic decisions, cross-functional |
| **RACI-F** | F = Feedback (reviews post-hoc) | Agile teams with retro culture |
| **CAIRO** | Adds O = Omitted (explicitly not involved) | Clarifying non-involvement |

### Choosing the right variant

| Context | Variant |
|---------|---------|
| Software team, ongoing features | RACI (default) |
| Single strategic decision | DACI |
| Multi-exec decision | RAPID |
| Regulated (SOC2 / HIPAA / ISO) | RACI-VS |
| Program with shared infra teams | RASCI |
| Kill-scope clarification | CAIRO |

## DACI (Decision-Focused)

```
D — Driver       moves the decision forward, sets deadline
A — Approver     has final say (one person)
C — Contributor  provides expertise / opinions
I — Informed     learns the outcome
```

Use for discrete decisions: "Which auth provider?", "SLO target?", "Launch date?"

## RAPID (Bain) — for strategic decisions

```
R — Recommend   owner of proposal
A — Agree       must veto if disagree (quality/policy gate)
P — Perform     executes once decided
I — Input       provides facts/analysis
D — Decide      final call (one person)
```

Example:
- Recommend: product lead proposes pricing change
- Input: finance, sales provide data
- Agree: legal must not object
- Decide: CEO makes call
- Perform: sales + product roll out

## Workflow

```
SCOPE        →  list items (spec lines / decisions / deliverables)
             →  decide scope — per item or per phase?

IDENTIFY     →  list people / roles (not individuals if roles are stable)
             →  from stakeholder map (accord `stakeholder`)

ASSIGN       →  for each row, assign exactly one A
             →  fill R (who does the work)
             →  fill C (who must be consulted) — keep < 3 per row
             →  fill I (who is informed) — keep < 5 per row

VALIDATE     →  no row has two A's
             →  no row has blank A
             →  no person is A on > ~5 rows without delegation plan
             →  no row has too many C's (decision paralysis)

COMMUNICATE  →  share matrix; get explicit acknowledgment from A's
             →  publish as living document

REVIEW       →  revisit on org change / phase transition
             →  retrospective: did A's actually own?
```

## Designing the Rows

The hardest part is what the rows represent. Good rows are:

- **Outcomes**, not activities ("Payment feature shipped" vs "write code").
- **Gateable** — clear "done" state.
- **At the right altitude** — not too fine (one row per sub-task) or too coarse (one row per project).

Typical altitudes for Accord L0-L3:

| Accord level | RACI row type |
|--------------|---------------|
| L0 Vision | Goal statements, major decisions |
| L1 Requirements | Each REQ-* item |
| L2 Detailed spec | Component-level design + key decisions |
| L3 AC / test | Per AC group or per risk area |

## Heat Map Diagnostics

Plot the matrix as a heat map and look for patterns:

| Pattern | Meaning | Fix |
|---------|---------|-----|
| Row with many A's | Multiple accountable (invalid) | Pick one |
| Row with no R | Accountable with no worker | Assign R (may be A) |
| Row with 5+ C's | Over-consulting paralysis | Tighten; some become I |
| Row with only I's | No one accountable or doing | Add A and R |
| Column over-loaded | That person is a bottleneck | Redistribute |
| Column with only I's | Token inclusion only | Reassess — do they need to be here? |
| Column with many A's | Power concentration | Spread accountability |

## Output Template

```markdown
## RACI Matrix: [Scope]

### Legend
- R = Responsible (does the work)
- A = Accountable (owns outcome, exactly one)
- C = Consulted (bidirectional, before)
- I = Informed (one-way, after)

### Scope
- **Scope level**: [L0 / L1 / L2 / L3 / decision-set]
- **Variant**: [RACI / DACI / RAPID / ...]
- **Time window**: [phase / quarter]

### Matrix
|   | [Person A] | [Person B] | [Person C] | [Person D] | [Person E] |
|---|-----------|-----------|-----------|-----------|-----------|
| Row 1 | A | C | R | I | — |
| Row 2 | C | A | R | I | I |
| Row 3 | I | A | C | — | R |

### Diagnostics
- [ ] Exactly one A per row
- [ ] No blank A
- [ ] No row with > 3 C's
- [ ] No person is A on > ~5 rows unaddressed
- [ ] No column is token-only (all I's)

### Decision Variant Rows (DACI / RAPID)
If any rows are decisions, annotate separately:
| Decision | D | A | C | I |
|----------|---|---|---|---|
| Auth provider | PM | CTO | Sec, Legal | Everyone |

### Communication
- **Published to**: [channel / doc / wiki]
- **Acknowledgment required from A's**: [date]
- **Review cadence**: [phase boundaries]

### Handoffs
- Accord L3 handoff: attach RACI column per item
- Sherpa: per-step ownership derived from matrix R
- Magi: escalate un-ambiguous As to decision arbitration
- Scribe: formalize as governance document
- Stakeholder (elsewhere): ensure matrix aligns with engagement plan
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Multiple A's per row | Pick one; others become R or C |
| Blank A | Assign; if no one will own, row should not exist |
| R with no A | R executes, but who's accountable? Add A |
| Every row has 5 C's | Paralysis; tighten to 1-2 C's |
| Matrix never updated | Review at phase boundaries and after org change |
| Matrix is performative only | Explicit A-acknowledgment ceremony |
| RACI used for strategic decisions | Use DACI or RAPID instead |
| One person is A on 15+ rows | Bottleneck; redistribute or delegate |
| Team members not on matrix | Missing scope coverage; expand rows or roster |
| Cultural mismatch (US vs JP) | Adjust ceremony; accountability language differs |

## Deliverable Contract

When `raci` completes, emit:

- **Variant selection** (RACI / DACI / RAPID / etc.) with rationale.
- **Matrix** with unambiguous A per row.
- **Diagnostics** passing all checks.
- **Decision-variant rows** separated if any.
- **Communication plan** (publish, acknowledge, review cadence).
- **Handoffs**: Accord L3, Sherpa, Magi, Scribe, Stakeholder.

## References

- Responsibility Assignment Matrix — PMI PMBOK chapter on resource management
- Bain & Company — *RAPID®: Bain's tool for assigning decision rights* (Rogers & Blenko, HBR 2006)
- Atlassian — DACI decision-making framework
- Scaled Agile Framework (SAFe) — RACI in ART governance
- ISO 9001 / ITIL — RACI for process control
- Mind Tools — RACI chart introduction
- McKinsey — *The people puzzle: decision rights* (decision rights adjacent to RACI)
- *Responsibility Charting* — Beer, Eisenstat — organizational design foundations
