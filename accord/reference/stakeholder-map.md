# Stakeholder Map Reference

Purpose: Map stakeholders on a Power × Interest grid, assign an engagement mode per quadrant, and design communication cadence and information-flow patterns. Accord uses this to anchor the L0 Vision audience and to drive communication plans for L1-L3 review cycles.

## Scope Boundary

- **accord `stakeholder`**: Power/Interest grid + engagement design (this document).
- **accord `vision` (elsewhere)**: L0 Vision Block — stakeholder map informs the audience section.
- **accord `raci` (elsewhere)**: Per-item responsibility assignment (different question).
- **cast (elsewhere)**: User personas. Stakeholder ≠ user; an admin, a regulator, a vendor, a board member are stakeholders but not users.
- **saga (elsewhere)**: Narrative for external audiences.
- **Magi (elsewhere)**: Multi-perspective arbitration.

## Mendelow Power × Interest Grid

```
          HIGH INTEREST
               │
    Keep       │    Manage
    Informed   │    Closely
               │   (Key players)
               │
───────────────┼───────────────── HIGH POWER
               │
    Monitor    │    Keep
    (min effort)│    Satisfied
               │
          LOW INTEREST
```

### Four quadrants

| Quadrant | Characteristics | Engagement mode |
|----------|-----------------|-----------------|
| **Manage Closely** (high power, high interest) | Decision-makers who care | Deep involvement, co-creation, weekly touchpoints |
| **Keep Satisfied** (high power, low interest) | Executives, compliance, legal — rubber-stamp when happy | Concise updates, headline-level only, avoid surprises |
| **Keep Informed** (low power, high interest) | Users, champions, power users | Regular updates, include them in feedback loops |
| **Monitor** (low power, low interest) | Tangential teams, occasional users | Minimal communication, notify on launch |

## Identification Workflow

```
LIST         →  enumerate every party that influences or is influenced
             →  internal: teams, functions, execs, board
             →  external: customers, vendors, regulators, partners
             →  silent: future users, legal/ethics, underrepresented

SCORE        →  power: can they block / accelerate / shape outcome? (1-5)
             →  interest: how directly does it affect their work? (1-5)

POSITION     →  place on 2x2 grid by median score cutoff
             →  watch for quadrant ties → tiebreak by recent activity

ENGAGE       →  assign engagement mode per stakeholder
             →  define information artifact (memo, demo, dashboard)
             →  define cadence (weekly / biweekly / monthly / at-milestone)

LOOP         →  reassess each quarter (positions change)
             →  new stakeholders enter; power shifts
```

## Engagement Mode Matrix

| Quadrant | Artifact | Cadence | Owner |
|----------|----------|---------|-------|
| Manage Closely | Working sessions, draft specs, demos | Weekly | PM + Lead |
| Keep Satisfied | Executive summary, dashboard, status email | Biweekly / monthly | PM |
| Keep Informed | Release notes, community posts, office hours | At milestone | DevRel / Marketing |
| Monitor | FYI channel post, release note link | At launch | Auto |

## Influence Dynamics

Not every stakeholder on the grid operates independently. Model:

- **Coalitions**: groups that move together (e.g., customer advisory board).
- **Blockers**: single stakeholders with veto (legal, security review).
- **Champions**: stakeholders who advocate internally on your behalf.
- **Silent stakeholders**: absent from the room but affected (end users, future hires, regulators).
- **Proxy stakeholders**: represent others (customer success rep represents users).

### RACI-adjacent roles (optional dimension)

For decision-heavy contexts, annotate per stakeholder:

| Role | Meaning |
|------|---------|
| D | Driver (moves work forward) |
| A | Approver (signs off) |
| C | Contributor (provides input) |
| I | Informed (kept in loop) |

This dovetails with `accord raci`.

## Information Flow Patterns

Different stakeholders need different views of the same reality.

| Pattern | Example |
|---------|---------|
| Top-down summary | Exec sees 1-pager monthly; team sees full doc |
| Bottom-up signal | Users report via NPS; PM aggregates for leadership |
| Peer-to-peer bridge | Design shares Figma with engineering daily |
| Gate-and-review | Legal reviews only at milestone boundaries |
| Dashboard pull | Stakeholder self-serves from live dashboard |
| Milestone push | Launch + post-mortem sent to all at event |

For each high-power stakeholder, choose *one* dominant pattern. Mixing causes noise.

## Output Template

```markdown
## Stakeholder Map: [Project / Feature]

### Stakeholder Inventory
| Stakeholder | Power (1-5) | Interest (1-5) | Quadrant | Role (D/A/C/I) |
|-------------|-------------|----------------|----------|----------------|
| [name/role] | [n] | [n] | [quadrant] | [role] |
| ... | ... | ... | ... | ... |

### Grid Visualization
[ASCII or Canvas handoff]

### Engagement Plan
| Quadrant | Stakeholders | Artifact | Cadence | Owner |
|----------|-------------|----------|---------|-------|
| Manage Closely | [list] | [doc type] | [freq] | [person] |
| Keep Satisfied | [list] | [doc type] | [freq] | [person] |
| Keep Informed | [list] | [doc type] | [freq] | [person] |
| Monitor | [list] | [doc type] | [freq] | [person] |

### Dynamics
- **Coalitions**: [...]
- **Blockers**: [...]
- **Champions**: [...]
- **Silent**: [...] — how surfaced in decisions

### Information Flow
| Stakeholder | Dominant pattern | Why |
|-------------|------------------|-----|
| [name] | [pattern] | [reason] |

### Risks
- [ ] Blocker identified with mitigation plan
- [ ] Silent stakeholders have a surrogate or representative
- [ ] Executive Keep-Satisfied group has pre-agreed surprise policy
- [ ] Cadence feasible with team bandwidth

### Review
- **Next reassessment**: [quarter / trigger event]

### Handoffs
- Accord L0 Vision: audience section references this map
- Accord `raci`: per-item responsibility assignment
- Prose: communication templates per artifact
- Canvas: visual rendering of the grid
- Scribe: formal stakeholder register document
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Everyone listed as "manage closely" | Apply discipline; the grid has four quadrants for a reason |
| Static map, never updated | Reassess quarterly; after org change or pivot |
| Conflating stakeholders with users | Users get research/persona; stakeholders get engagement plans |
| No silent-stakeholder analysis | Add proxy representation; future users, regulators, ethics |
| One-size-fits-all cadence | Power/Interest quadrant drives cadence |
| No named owner per engagement | Assign explicitly; "the team" = no one |
| Ignoring blockers until milestone | Surface blockers in discovery; give them early warning |
| No conflict-resolution plan | When stakeholders disagree, pre-define escalation |

## Deliverable Contract

When `stakeholder` completes, emit:

- **Stakeholder inventory** with power × interest scores.
- **Grid visualization** (ASCII or Canvas handoff).
- **Engagement plan** per quadrant (artifact, cadence, owner).
- **Dynamics** (coalitions, blockers, champions, silent).
- **Information flow pattern** per high-power stakeholder.
- **Risk check** and **review cadence**.
- **Handoffs**: Accord L0, Accord `raci`, Prose, Canvas, Scribe.

## References

- Aubrey Mendelow — original Power/Interest matrix (1991)
- Johnson, Scholes, Whittington — *Exploring Corporate Strategy* (applied matrix)
- PMI PMBOK — stakeholder engagement processes
- Gardner — "Effectively Managing Upwards" (Keep Satisfied dynamics)
- Marty Cagan — *Inspired* (product stakeholder patterns)
- Teresa Torres — *Continuous Discovery Habits* (customer as stakeholder vs user)
- Cynefin / Stakeholder Salience Model (Mitchell, Agle, Wood 1997) — power/legitimacy/urgency extension
- Atlassian / Miro templates for stakeholder mapping workshops
