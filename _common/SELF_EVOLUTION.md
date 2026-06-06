# Self-Evolution Protocol (Inward-Facing)

How individual agents learn from their own experience. Complements `EVOLUTION.md` (outward-facing: ecosystem signal emission).

| Aspect | EVOLUTION.md | SELF_EVOLUTION.md (this) |
|--------|-------------|--------------------------|
| Direction | Outward — signals to ecosystem | Inward — learning from own experience |
| Scope | Ecosystem-wide | Individual agent |
| Actions | EVOLUTION_SIGNAL emission, ECOSYSTEM.md reading | Journal reading, effectiveness measurement, parameter adjustment |
| Orchestrator | Darwin collects | Each agent executes independently |

---

## Three Tiers

| Tier | Who | What | Trigger |
|------|-----|------|---------|
| **Tier 1: Context Loading** | All agents | Read prior context before starting work | Every task start |
| **Tier 2: Calibration Loop** | Agents with learning loops (19+) | Post-task effectiveness measurement & adjustment | Calibration Triggers (CT-01–06) |
| **Tier 3: Self-Modification** | Architect (+ future qualified agents) | Modify own SKILL.md / references | 30+ data points + Safety Level framework |

---

## Tier 1: Context Loading Protocol

Before starting any task, load prior context to avoid repeating mistakes and leverage learned patterns.

### Reading Targets

| Source | What to extract | Required |
|--------|----------------|----------|
| Own journal (`.agents/{name}.md`) | Past insights, apply-when conditions matching current task | Yes |
| `.agents/PROJECT.md` | Recent cross-agent activity, current project state | Yes |
| `.agents/ECOSYSTEM.md` | Own relevance score, cross-agent discoveries (reading rules → `EVOLUTION.md`) | If exists |

### Application Method

1. **Scan** — Check if any journal `Apply when:` conditions match the current task
2. **Adjust** — Modify approach based on matched patterns (e.g., avoid known pitfalls, reuse successful strategies)
3. **Proceed** — Start task with enriched context

### Rules

- Check file existence before reading (journals/ECOSYSTEM.md may not exist yet)
- Read selectively — only entries relevant to the current task type
- Complete within seconds — context loading must not delay task execution
- Do NOT modify any files during context loading

---

## Tier 2: Standard Calibration Loop

Post-task learning cycle. All existing agent loops map to these 6 phases.

### Phases

```
OBSERVE → MEASURE → EXTRACT → ADAPT → SAFEGUARD → PERSIST
```

| Phase | Purpose | Input | Output |
|-------|---------|-------|--------|
| **OBSERVE** | Collect raw execution data | Task results, user feedback, tool outputs | Structured observation record |
| **MEASURE** | Quantify effectiveness | Observation record + scoring template | Effectiveness Score (A–F) |
| **EXTRACT** | Identify actionable patterns | Score + observation + historical journal | Candidate adjustments (max 3) |
| **ADAPT** | Apply adjustments to internal parameters | Candidate adjustments | Updated heuristics / weights / thresholds |
| **SAFEGUARD** | Validate changes are safe | Pre/post comparison | Approved or rolled-back changes |
| **PERSIST** | Record to journal + emit signals | Approved changes | Journal entry + EVOLUTION_SIGNAL (if reusable) |

### Phase Details

**OBSERVE:** Record what happened — inputs, decisions made, outcomes, user reactions. Raw data only, no interpretation.

**MEASURE:** Apply the Effectiveness Score Template (below) to quantify performance. Requires 3+ data points for meaningful scoring.

**EXTRACT:** Compare current score against historical baseline. Identify what worked, what didn't, and why. Generate max 3 candidate adjustments per cycle.

**ADAPT:** Apply extracted adjustments to internal parameters (weights, thresholds, heuristics, approach preferences). Tier 2 agents may only adjust parameters within their existing SKILL.md framework — not modify the SKILL.md itself.

**SAFEGUARD:** Verify adjustments don't degrade performance on previously successful patterns. If degradation detected → rollback to pre-ADAPT state.

**PERSIST:** Write journal entry using the template below. If insight is reusable across agents, emit EVOLUTION_SIGNAL (format → `EVOLUTION.md`).

### Mapping Table: Existing Loops → Standard Phases

| Agent(s) | Loop Name | OBSERVE | MEASURE | EXTRACT | ADAPT | SAFEGUARD | PERSIST |
|----------|-----------|---------|---------|---------|-------|-----------|---------|
| Nexus | LEARN | COLLECT | EVALUATE | EXTRACT | ADAPT | VERIFY | RECORD |
| Rally | HARMONIZE | COLLECT | EVALUATE | EXTRACT | ADAPT | SAFEGUARD | RECORD |
| Arena | CALIBRATE | COLLECT | EVALUATE | EXTRACT | ADAPT | SAFEGUARD | RECORD |
| Orbit | REFINE | OBSERVE | MEASURE | ANALYZE | IMPROVE | SAFEGUARD | JOURNAL |
| Sherpa | CALIBRATE | RECORD | COMPARE | — | ADJUST | — | PERSIST |
| Helm, Compete | FORESIGHT/SHARPEN | TRACK | VALIDATE | — | CALIBRATE | — | PROPAGATE |
| Scribe, Quill, Morph, Accord, Prism | INSCRIBE/CHRONICLE/TRANSMUTE/UNIFY/SPECTRUM | RECORD | EVALUATE | — | CALIBRATE | — | PROPAGATE |
| Cast | EVOLVE | DETECT | ASSESS | — | APPLY | — | LOG+PROPAGATE |
| Architect | EVOLVE | INTROSPECT | DIAGNOSE | PRESCRIBE | MUTATE | VERIFY | PERSIST |
| Darwin | (framework) | SENSE | ASSESS | — | EVOLVE | VERIFY | PERSIST |

Agents retain their own naming. This table is for conceptual alignment only — no renaming required.

---

## Effectiveness Score Template

Generic template adaptable to any agent's domain. Each agent defines its own Primary_Outcome metric.

### Formula

```
ES = (Primary_Outcome × 0.35) + (Efficiency × 0.20) + (Quality × 0.20) + (Adaptability × 0.15) + (User_Autonomy × 0.10)
```

| Dimension | What it measures | Example metrics |
|-----------|-----------------|-----------------|
| Primary_Outcome | Core mission success | Task completion rate, accuracy, coverage |
| Efficiency | Resource usage relative to outcome | Time spent, token usage, iteration count |
| Quality | Output quality beyond basic success | User satisfaction, downstream agent acceptance |
| Adaptability | Response to novel/unexpected situations | Graceful degradation, creative solutions |
| User_Autonomy | User empowerment vs. dependency creation | Knowledge transfer, self-service enablement |

### Grading Scale

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 90–100 | Excellent — maintain current approach |
| B | 75–89 | Good — minor refinements |
| C | 60–74 | Adequate — targeted improvements needed |
| D | 40–59 | Below expectations — full cycle required |
| F | 0–39 | Critical — immediate intervention |

### Minimum Data Requirements

- **3+ data points** required before calculating a meaningful ES
- Below 3 data points: record observations only (OBSERVE + PERSIST), skip MEASURE–ADAPT
- Agents with existing scoring (CES/TES/AES/etc.) should map their scores to this scale

---

## Calibration Triggers

| ID | Trigger | Scope | Priority |
|----|---------|-------|----------|
| CT-01 | Task completion | **Lightweight** (OBSERVE + MEASURE only) | Normal |
| CT-02 | Same pattern fails 3+ times | **Full cycle** | High |
| CT-03 | User override / correction | **Full cycle** | Highest |
| CT-04 | Judge/Nexus quality feedback | **Medium** (OBSERVE → EXTRACT → PERSIST) | High |
| CT-05 | Lore cross-agent pattern notification | **Medium** | Normal |
| CT-06 | 30+ days since last calibration | **Full cycle** | Low |

**Lightweight** = OBSERVE + MEASURE + PERSIST (no parameter changes).
**Medium** = OBSERVE + MEASURE + EXTRACT + PERSIST (identify but don't apply).
**Full cycle** = All 6 phases.

---

## Safety Framework

### What Tier 2 Can and Cannot Modify

| Modifiable (Tier 2) | Not Modifiable (Tier 2) |
|---------------------|------------------------|
| Internal heuristic weights | SKILL.md content |
| Approach preferences / ordering | Boundaries (Always/Ask/Never) |
| Threshold values within existing ranges | Collaboration patterns |
| Pattern confidence scores | Core identity / principles |
| Journal-recorded strategies | `_common/*.md` files |

### Change Budget

| Scope | Limit |
|-------|-------|
| Per session | Max 3 parameter adjustments |
| Per month | Max 15 parameter adjustments |
| Per cycle | Max 3 candidate adjustments evaluated |

### Runaway Prevention

| ID | Mechanism | Condition | Response |
|----|-----------|-----------|----------|
| RP-01 | Budget enforcement | Session/monthly limit reached | Block until budget resets |
| RP-02 | Diminishing returns | 3 consecutive cycles with ES improvement < 2 points | Pause until next external trigger (CT-02/03/04) |
| RP-03 | Oscillation prevention | Change → revert → re-change detected twice | Full stop; require human review |
| RP-04 | Chain prevention | 3 consecutive cycles without intervening task | Defer remaining to next task completion |
| RP-05 | Rollback guarantee | Before any ADAPT phase | Snapshot current state; restore on SAFEGUARD failure |
| RP-06 | Evidence minimum | Fewer than 3 data points | OBSERVE + PERSIST only; skip MEASURE–ADAPT |

### Rollback Protocol

1. Before ADAPT: snapshot all parameters being modified
2. After ADAPT: run SAFEGUARD validation
3. If SAFEGUARD detects degradation: restore snapshot entirely (no partial rollback)
4. Record rollback in journal with reason

---

## Tier 3: Self-Modification

Direct modification of own SKILL.md and references. Currently implemented by Architect only.

### Safety Level Framework

| Level | Scope | Example | Approval |
|-------|-------|---------|----------|
| **A: Autonomous** | reference/ additions only | New insights, examples, templates | None |
| **B: Autonomous + Verify** | reference/ updates, minor SKILL.md updates | Content updates with equivalence verification | Self-verify |
| **C: Human Approval** | Core SKILL.md sections | Boundaries, Principles, Framework changes | Human required |
| **D: Forbidden** | Safety mechanisms | Own Safety Level, trigger conditions, guardrails | Never |

### Tier 3 Activation Requirements

An agent may implement Tier 3 only when ALL conditions are met:

1. **30+ data points** in journal with consistent patterns
2. **Dedicated reference file** at `reference/self-evolution.md` with full Safety Level definitions
3. **RP-01 through RP-05** implemented with agent-specific budgets
4. **Level D** includes: own safety levels, `_common/*.md`, other agents' files
5. **Explicit design** — Architect must include Tier 3 capability when creating the agent

---

## Integration Points

### Darwin Integration

- PERSIST phase → emit EVOLUTION_SIGNAL (format → `EVOLUTION.md`) for reusable insights
- Darwin collects signals during Journal Synthesis (ET-04) and updates ECOSYSTEM.md
- Agent reads own Relevance Score from ECOSYSTEM.md during Tier 1 Context Loading

### Lore Integration

- PERSIST phase → Lore discovers cross-agent patterns from journal entries
- Lore PATTERN notification → triggers CT-05 for relevant agents
- Agents apply Lore-propagated patterns during EXTRACT phase

### EVOLUTION.md Relationship

This protocol does NOT redefine EVOLUTION_SIGNAL format or ECOSYSTEM.md reading rules. For those specifications → `_common/EVOLUTION.md`.

---

## Journal Entry Template (Calibration Record)

```markdown
## YYYY-MM-DD - Calibration: [Brief Title]

**Trigger:** [CT-01–06 ID and description]
**Scope:** Lightweight | Medium | Full
**ES Score:** [Grade] ([Score]/100) — Previous: [Grade] ([Score]/100)
**Observations:** [What happened during the task]
**Adjustments:** [What was changed, or "None (lightweight)"]
**Evidence:** [Data points supporting the adjustment]
**Rollback:** [Not needed | Performed — reason]
```

---

## Adoption Guide

### For Agents Without Learning Loops (Tier 1 Only)

Implement Tier 1 Context Loading at task start. No SKILL.md changes needed — this is standard operational behavior:

1. Read own journal → check `Apply when:` matches
2. Read PROJECT.md → recent cross-agent context
3. Read ECOSYSTEM.md (if exists) → own relevance, discoveries
4. Adjust approach based on matched patterns
5. Proceed with task

### For Agents With Existing Learning Loops (Tier 2)

No changes required. Existing loops already implement the standard phases under different names. Use the Mapping Table above for conceptual alignment. When adding new loop features, align with the 6-phase structure.

### For Tier 3 Implementation

Follow Tier 3 Activation Requirements above. Reference Architect's `reference/self-evolution.md` as the canonical implementation example.
