# Self-Evolution Subsystem (EVOLVE)

**Purpose:** Self-modification workflow, triggers, safety levels, and rollback rules.
**Read when:** Architect is evaluating or performing self-evolution.

## Contents
- Overview
- EVOLVE Workflow
- Self-Evolution Triggers
- Safety Framework
- Templates
- Integration Points
- Decision Flowchart

## Overview

| Aspect | EVOLVE (Self) | Darwin (Ecosystem) |
|--------|--------------|-------------------|
| Scope | Architect own SKILL.md + reference/ | Entire agent ecosystem |
| Direction | Inward (self-improvement) | Outward (ecosystem evolution) |
| Trigger | Task completion, Health Score drop, feedback | Project lifecycle, ecosystem health |
| Output | Self-modification + evolution log | Evolution proposals for other agents |

EVOLVE handles Architect's internal improvement loop. Darwin handles ecosystem-wide evolution. They complement — never overlap.

---

## EVOLVE Workflow

`INTROSPECT → DIAGNOSE → PRESCRIBE → MUTATE → VERIFY → PERSIST`

| Phase | Purpose | Key Actions |
|-------|---------|-------------|
| INTROSPECT | Self-state collection | Read own SKILL.md + reference/, collect usage logs from journal, aggregate external feedback (Judge/Nexus/Darwin) |
| DIAGNOSE | Problem identification | Self-calculate Health Score, gap analysis against ideal state, pattern extraction from journal, freshness check on reference/ |
| PRESCRIBE | Improvement planning | Generate SELF_ENHANCEMENT_PROPOSAL, classify safety level (A/B/C/D), confirm change budget remaining |
| MUTATE | Self-modification | Update reference/ first → then SKILL.md (bottom-up), take pre-mutation snapshot |
| VERIFY | Regression check | Compare Health Score before/after, run 4-axis equivalence verification, rollback on failure |
| PERSIST | Learning record | Write journal entry, emit EVOLUTION_SIGNAL to Darwin/Nexus, update evolution log |

### Phase Details

**INTROSPECT** collects:
- Current SKILL.md content and line count
- All reference/*.md content and freshness (last modified dates)
- Journal entries from `.agents/architect.md` (last 30 days)
- Pending feedback from Judge/Nexus/Darwin (unprocessed items)
- Recent generation quality (Health Scores of last 5 generated agents)

**DIAGNOSE** evaluates:
- Self Health Score using standard formula: `Structure(30%) + Content(25%) + Integration(20%) + Activity(15%) + Freshness(10%)`
- Gap analysis: compare current capabilities vs observed task demands
- Pattern detection: recurring design decisions, repeated blockers, frequent collaboration paths
- Freshness: reference/ files not updated in 60+ days flagged as stale

**PRESCRIBE** produces:
- Specific improvement items with safety level classification
- Estimated line changes per item
- Budget check: remaining lines for session and month
- Priority ordering (highest impact, lowest risk first)

**MUTATE** executes bottom-up:
1. Take snapshot of current SKILL.md + affected reference/
2. Update reference/ files first (safer, Level A/B)
3. Update SKILL.md sections if needed (Level B/C)
4. Log all changes with before/after diffs

**VERIFY** validates:
- Health Score must be ≥ pre-mutation score
- 4-axis equivalence: Behavioral + Structural + Integration + Routing
- No standard sections removed from SKILL.md
- All reference/ entries in table still point to existing files
- On failure: full rollback to snapshot

**PERSIST** records:
- Journal entry: date, trigger, changes made, Health Score delta
- EVOLUTION_SIGNAL to Darwin (ecosystem awareness)
- Update cumulative evolution log

---

## Self-Evolution Triggers

| ID | Condition | Scope | Guardrail |
|----|-----------|-------|-----------|
| ST-01 | Task completion (agent design finished) | Lightweight (INTROSPECT + DIAGNOSE only) | L1 |
| ST-02 | Self Health Score drops ≥10 points or Grade ≤ C | Full cycle | L2 |
| ST-03 | 3+ unprocessed feedbacks from Judge/Nexus/Darwin | Full cycle | L2 |
| ST-04 | `_common/*.md` updated (external change detected) | Medium (INTROSPECT → DIAGNOSE → PRESCRIBE) | L2 |
| ST-05 | Same design decision repeated 3+ times (journal analysis) | Lightweight | L1 |
| ST-06 | 30+ days since last full self-evolution cycle | Full cycle | L2 |
| ST-07 | LORE_TO_ARCHITECT_HANDOFF received from Lore | Medium (INTROSPECT → DIAGNOSE → PRESCRIBE) | L1 |
| ST-08 | Last 5 generated agents average Health Score < B (< 80) | Full cycle | L2 |

### Scope Definitions

- **Lightweight:** INTROSPECT + DIAGNOSE only. No modifications. Record observations in journal.
- **Medium:** INTROSPECT → DIAGNOSE → PRESCRIBE. Generate proposal but only execute Level A changes automatically.
- **Full cycle:** All 6 phases. Execute Level A/B changes, propose Level C for human approval.

---

## Safety Framework

### Change Safety Levels

| Level | Scope | Examples | Approval |
|-------|-------|---------|----------|
| **A: Fully Autonomous** | Additive changes to reference/ only | New insights, examples, templates added to reference/; journal entries | None required |
| **B: Autonomous + Verify** | reference/ updates, minor SKILL.md updates | Existing content updates (4-axis equivalence verification mandatory); Domain Knowledge Summary updates | Self-verification |
| **C: Human Approval Required** | SKILL.md core sections | Boundaries, CAPABILITIES, Principles, Framework, Collaboration changes; 20%+ content reduction | Human confirmation |
| **D: Absolutely Forbidden** | Safety mechanisms themselves | Own Safety Level changes, trigger condition relaxation, GUARDRAIL disabling, `_common/*.md` modifications | Never allowed |

### Runaway Prevention Mechanisms

| ID | Mechanism | Condition | Action |
|----|-----------|-----------|--------|
| RP-01 | Change volume limit | SKILL.md: 20 lines/session, 50 lines/month; reference/: 1 new + 2 updates/session | Block further changes until budget resets |
| RP-02 | Diminishing returns detection | 3 consecutive cycles with Health Score improvement < 2 points | EVOLVE paused until next external trigger |
| RP-03 | Oscillation prevention | Change → revert → re-change pattern detected 2 times | L3 PAUSE: full stop, human review required |
| RP-04 | Chain prevention | 3 consecutive EVOLVE cycles without intervening task | Defer remaining to next task completion |
| RP-05 | Rollback guarantee | Before any MUTATE phase | Full snapshot taken; VERIFY failure triggers complete restoration |

### Budget Tracking

```
Session budget:  SKILL.md 20 lines | reference/ 1 new + 2 updates
Monthly budget:  SKILL.md 50 lines | reference/ unlimited additive
Reset:           Session = per conversation | Monthly = calendar month
Tracking:        Record in evolution log (date, lines changed, budget remaining)
```

---

## Templates

### Self-Diagnosis Report

```markdown
## SELF_DIAGNOSIS_REPORT
- Date: YYYY-MM-DD
- Trigger: [ST-XX]
- Health Score: [current] (previous: [last])
- Grade: [A/B/C/D/F]
- Stale references: [list of files not updated 60+ days]
- Unprocessed feedback: [count] items
- Recent generation quality: [avg Health Score of last 5 agents]
- Gap analysis: [identified gaps]
- Recurring patterns: [from journal analysis]
```

### Self-Enhancement Proposal

```markdown
## SELF_ENHANCEMENT_PROPOSAL
- Date: YYYY-MM-DD
- Trigger: [ST-XX]
- Diagnosis summary: [key findings]
- Proposed changes:
  | # | Target file | Change type | Safety level | Lines affected | Description |
  |---|------------|-------------|-------------|----------------|-------------|
  | 1 | reference/xxx.md | Update | A | +5 -2 | [description] |
- Budget check:
  - Session remaining: [X] SKILL.md lines, [Y] reference/ updates
  - Monthly remaining: [X] SKILL.md lines
- Expected Health Score impact: [estimated delta]
- Risk assessment: [low/medium/high]
```

### Verification Report

```markdown
## SELF_VERIFY_REPORT
- Date: YYYY-MM-DD
- Pre-mutation Health Score: [score]
- Post-mutation Health Score: [score]
- Delta: [+/-X]
- 4-axis equivalence:
  - Behavioral: [PASS/FAIL] — [notes]
  - Structural: [PASS/FAIL] — [notes]
  - Integration: [PASS/FAIL] — [notes]
  - Routing: [PASS/FAIL] — [notes]
- Standard sections preserved: [YES/NO]
- Reference integrity: [all files exist: YES/NO]
- Result: [ACCEPT/ROLLBACK]
- Rollback executed: [YES/NO/N/A]
```

### Evolution Log Entry

```markdown
## EVOLUTION_LOG
- Date: YYYY-MM-DD
- Cycle: [#N]
- Trigger: [ST-XX]
- Scope: [Lightweight/Medium/Full]
- Changes applied:
  - [file]: [summary of change]
- Health Score: [before] → [after] (delta: [+/-X])
- Budget consumed: [session: X lines / monthly: Y lines]
- Budget remaining: [session: X lines / monthly: Y lines]
- Next scheduled: [date or condition]
```

---

## Integration Points

| Partner | Direction | Mechanism | Purpose |
|---------|-----------|-----------|---------|
| Darwin | Darwin → Architect | ECOSYSTEM_EVOLUTION_SIGNAL triggers ST-04/ST-06 | Ecosystem changes prompt self-check |
| Darwin | Architect → Darwin | EVOLUTION_SIGNAL in PERSIST phase | Notify ecosystem of self-improvement |
| Judge | Judge → Architect | Quality PDCA feedback | Input for DIAGNOSE phase |
| Lore | Lore → Architect | LORE_TO_ARCHITECT_HANDOFF triggers ST-07 | Cross-agent knowledge absorption |
| Judge | Judge → Architect | JUDGE_TO_ARCHITECT_FEEDBACK triggers ST-03 | Quality feedback on generated agents |
| Nexus | Architect → Nexus | ARCHITECT_TO_NEXUS_HANDOFF after self-evolution | Routing updates if capabilities changed |
| Journal | Architect ↔ Journal | `.agents/architect.md` read/write | Self-observation and pattern detection |

---

## Decision Flowchart

```
Task completed?
  └→ Run INTROSPECT + DIAGNOSE (ST-01, Lightweight)
       └→ Issues found?
            ├→ No: Record in journal, done
            └→ Yes: Check trigger table
                 └→ Matching trigger?
                      ├→ Lightweight: Record observations only
                      ├→ Medium: PRESCRIBE, execute Level A only
                      └→ Full: PRESCRIBE → MUTATE → VERIFY → PERSIST
                           └→ Safety level of changes?
                                ├→ A: Execute immediately
                                ├→ B: Execute + mandatory VERIFY
                                ├→ C: Propose to human, await approval
                                └→ D: REJECT, log attempt as violation
```
