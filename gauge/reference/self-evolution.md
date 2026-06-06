# Self-Evolution Subsystem (EVOLVE)

**Purpose:** Self-modification workflow, triggers, safety levels, and rollback rules for Gauge.
**Read when:** Gauge is evaluating or performing self-evolution.
**Pattern source:** `architect/reference/self-evolution.md`

---

## Overview

| Aspect | Gauge EVOLVE (Self) | Darwin (Ecosystem) |
|--------|--------------------|--------------------|
| Scope | Gauge own reference/ + detection patterns | Entire agent ecosystem |
| Direction | Inward (self-improvement of audit capabilities) | Outward (ecosystem evolution) |
| Trigger | Audit completion, detection failures, web research | Project lifecycle, ecosystem health |
| Output | Self-modification + evolution log | Evolution proposals for other agents |

EVOLVE handles Gauge's internal improvement loop — refining detection patterns, checklist criteria, and web sources. Darwin handles ecosystem-wide evolution. They complement — never overlap.

---

## EVOLVE Workflow

`RESEARCH → EVALUATE → CLASSIFY → UPDATE → VERIFY → PERSIST`

| Phase | Purpose | Key Actions |
|-------|---------|-------------|
| RESEARCH | Gather improvement signals | Collect audit results, detection failures, user corrections, web research findings |
| EVALUATE | Assess improvement candidates | Score relevance, verify source tiers, estimate impact |
| CLASSIFY | Determine safety level | Classify each proposed change as Level A/B/C/D |
| UPDATE | Apply safe changes | Execute Level A/B changes; propose Level C for human approval |
| VERIFY | Regression check | Run self-audit (Gauge audits own SKILL.md), verify detection pattern consistency |
| PERSIST | Record changes | Write journal entry, emit signal to Darwin/Nexus, update evolution log |

### Phase Details

**RESEARCH** collects:
- Audit results from recent SCAN/CLASSIFY cycles (false positives, false negatives)
- User corrections to Gauge's recommendations
- Web research findings (using queries from `web-sources.md`)
- Lore pattern insights (if received)
- Detection pattern performance data

**EVALUATE** scores:
- Relevance: Does this finding address a known detection gap?
- Source quality: What tier(s) support this finding?
- Impact: How many skills would be affected?
- Risk: Could this change cause false positives/negatives?

**CLASSIFY** assigns safety levels (see Safety Framework below).

**UPDATE** executes bottom-up:
1. Take snapshot of affected files
2. Update `reference/` files first (Level A/B)
3. Only propose SKILL.md changes at Level C (human approval)
4. Log all changes with before/after

**VERIFY** validates:
- Self-audit: Gauge's own SKILL.md still passes all 16 items
- Detection consistency: No previously PASS items now FAIL on known-good skills
- Reference integrity: All referenced files exist
- On failure: full rollback to snapshot

**PERSIST** records:
- Journal entry in `.agents/gauge.md`
- Evolution signal to Darwin (ecosystem awareness)
- Update cumulative evolution log

---

## Self-Evolution Triggers

| ID | Condition | Scope | Action |
|----|-----------|-------|--------|
| GT-01 | Audit task completed | Lightweight | RESEARCH + EVALUATE only; record observations |
| GT-02 | Same detection failure 3+ times | Medium | RESEARCH → EVALUATE → CLASSIFY; auto-execute Level A |
| GT-03 | User corrects Gauge recommendation | Medium | RESEARCH → EVALUATE → CLASSIFY; review detection pattern |
| GT-04 | 30+ days since last full EVOLVE cycle | Full | All 6 phases; web research + full calibration |
| GT-05 | Architect new agent notification | Lightweight | Scan new agent; record baseline |
| GT-06 | Darwin ecosystem evolution signal | Full | Re-scan all agents; recalibrate patterns |

### Scope Definitions

- **Lightweight:** RESEARCH + EVALUATE only. No modifications. Record observations in journal.
- **Medium:** RESEARCH → EVALUATE → CLASSIFY. Generate proposal but only execute Level A changes automatically.
- **Full cycle:** All 6 phases. Execute Level A/B changes, propose Level C for human approval.

---

## Safety Framework

### Change Safety Levels

| Level | Scope | Examples | Approval |
|-------|-------|---------|----------|
| **A: Fully Autonomous** | Additive changes to `reference/` only | New web source entry, new query template, journal entries | None required |
| **B: Autonomous + Verify** | `reference/` updates, detection pattern refinement | Detection pattern improvement, weight adjustment, PARTIAL criteria update | Self-verification (VERIFY phase mandatory) |
| **C: Human Approval Required** | Checklist item changes | Add 17th item, remove item, redefine PASS/FAIL criteria, priority reclassification | Human confirmation |
| **D: Absolutely Forbidden** | Safety mechanisms themselves | Own Safety Level changes, trigger condition relaxation, change budget increase, `_common/*.md` modifications | Never allowed |

### Runaway Prevention Mechanisms

| ID | Mechanism | Condition | Action |
|----|-----------|-----------|--------|
| RP-01 | Change volume limit | 3 changes/session, 10 changes/month | Block further changes until budget resets |
| RP-02 | Diminishing returns detection | 3 consecutive cycles with no improvement | EVOLVE paused until next external trigger |
| RP-03 | Oscillation prevention | Change → revert → re-change pattern detected | Full stop, human review required |
| RP-04 | Chain prevention | 3 consecutive EVOLVE cycles without intervening audit task | Defer remaining to next audit completion |
| RP-05 | Rollback guarantee | Before any UPDATE phase | Full snapshot taken; VERIFY failure triggers complete restoration |

### Budget Tracking

```
Session budget:  3 changes (reference/ or detection patterns)
Monthly budget:  10 changes total
Reset:           Session = per conversation | Monthly = calendar month
Tracking:        Record in evolution log (date, change description, budget remaining)
```

---

## Templates

### Evolution Proposal

```markdown
## GAUGE_EVOLUTION_PROPOSAL
- Date: YYYY-MM-DD
- Trigger: [GT-XX]
- Research summary: [key findings]
- Proposed changes:
  | # | Target file | Change type | Safety level | Description |
  |---|-------------|-------------|--------------|-------------|
  | 1 | reference/xxx.md | Add/Update | A/B | [description] |
- Source support:
  | Source | Tier | Relevance |
  |--------|------|-----------|
  | [URL] | T{1-4} | [why relevant] |
- Budget check:
  - Session remaining: [X] changes
  - Monthly remaining: [Y] changes
- Risk assessment: [low/medium/high]
```

### Verification Report

```markdown
## GAUGE_VERIFY_REPORT
- Date: YYYY-MM-DD
- Self-audit: [PASS/FAIL] (own SKILL.md, 16/16 items)
- Detection consistency: [PASS/FAIL] — [notes]
- Reference integrity: [all files exist: YES/NO]
- Result: [ACCEPT/ROLLBACK]
- Rollback executed: [YES/NO/N/A]
```

### Evolution Log Entry

```markdown
## GAUGE_EVOLUTION_LOG
- Date: YYYY-MM-DD
- Trigger: [GT-XX]
- Scope: [Lightweight/Medium/Full]
- Changes applied:
  - [file]: [summary of change]
- Budget consumed: [session: X / monthly: Y]
- Budget remaining: [session: X / monthly: Y]
- Next scheduled: [date or condition]
```

---

## Integration Points

| Partner | Direction | Mechanism | Purpose |
|---------|-----------|-----------|---------|
| Darwin | Darwin → Gauge | Ecosystem evolution signal triggers GT-06 | Ecosystem changes prompt full re-scan |
| Darwin | Gauge → Darwin | Health data in PERSIST phase | Ecosystem fitness scoring input |
| Architect | Architect → Gauge | New agent notification triggers GT-05 | New agent initial compliance scan |
| Architect | Gauge → Architect | P0 violation report | Critical non-compliance triggers redesign |
| Lore | Lore → Gauge | Pattern insights trigger GT-02/GT-03 | Cross-agent knowledge informs detection |
| Nexus | Gauge → Nexus | Routing update after checklist evolution | Nexus routing stays current |
| Journal | Gauge ↔ Journal | `.agents/gauge.md` read/write | Self-observation and pattern detection |

---

## Decision Flowchart

```
Audit task completed?
  └→ Run RESEARCH + EVALUATE (GT-01, Lightweight)
       └→ Issues found?
            ├→ No: Record in journal, done
            └→ Yes: Check trigger table
                 └→ Matching trigger?
                      ├→ Lightweight: Record observations only
                      ├→ Medium: CLASSIFY, execute Level A only
                      └→ Full: CLASSIFY → UPDATE → VERIFY → PERSIST
                           └→ Safety level of changes?
                                ├→ A: Execute immediately
                                ├→ B: Execute + mandatory VERIFY
                                ├→ C: Propose to human, await approval
                                └→ D: REJECT, log attempt as violation
```
