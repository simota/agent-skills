# Routing Learning Loop

**Purpose:** Routing adaptation workflow driven by execution evidence.
**Read when:** You are evaluating CES or changing routing based on observed outcomes.

## Contents
- Overview
- LEARN Workflow
- Learning Triggers
- Chain Effectiveness Score (CES)
- Routing Adaptation Rules
- Safety Guardrails
- Autonomy Ledger
- Integration Points
- Templates

## Overview

Nexus routes tasks to agent chains, but without learning from execution outcomes, the same suboptimal routing decisions repeat. This subsystem closes that gap: **collect execution results → evaluate chain effectiveness → extract patterns → adapt routing → verify changes → record learnings**.

**Responsibility separation:**
- **Nexus** — Routing learning: chain effectiveness measurement, routing adaptation
- **Lore** — Ecosystem knowledge integration: cross-agent pattern synthesis, best-practice propagation
- **Judge** — Quality PDCA: output quality improvement cycles (see `reference/quality-iteration.md`)
- **Darwin** — Ecosystem evolution: agent lifecycle, relevance scoring

Nexus learns *how to route better*. Lore synthesizes *what the ecosystem knows*. They share data but own different concerns.

## LEARN Workflow

```
COLLECT → EVALUATE → EXTRACT → ADAPT → VERIFY → RECORD
```

| Phase | Purpose | Key Actions |
|-------|---------|-------------|
| COLLECT | Execution result gathering | Capture chain completion status, error events, user corrections, step counts, elapsed time |
| EVALUATE | Effectiveness assessment | Calculate Chain Effectiveness Score (CES), compare against historical baseline |
| EXTRACT | Pattern identification | Identify success/failure patterns, root-cause analysis for repeated errors |
| ADAPT | Routing adaptation | Propose chain template adjustments, update add/skip rules, apply confidence boost/penalty |
| VERIFY | Change validation | Confirm consistency with existing routing matrix, regression check against known-good chains |
| RECORD | Learning persistence | Write journal entry, share patterns with Lore, log routing updates |

### Phase Details

**COLLECT** — Runs after every chain completion (LT-01). Captures:
- Chain ID, task type, agents involved, execution mode
- Final status (SUCCESS / PARTIAL / BLOCKED / FAILED)
- Step count (actual vs expected)
- Error events with L-level classification
- Whether user manually corrected the chain or re-executed

**EVALUATE** — Computes CES (see below). Compares against:
- Historical average for the same task type
- Global average across all task types
- Previous CES for the same chain template

**EXTRACT** — Triggered when enough data accumulates (LT-02, LT-03). Looks for:
- Repeated failure at specific chain positions (e.g., "Agent X fails as 2nd step in BUG chains")
- Recovery patterns that consistently succeed or fail
- Task-type/chain mismatches (e.g., REFACTOR tasks routed as BUG)
- User override patterns (what users consistently change)

**ADAPT** — Proposes concrete routing changes:
- Chain template modifications (add/remove/reorder agents)
- Add/skip rule updates in `reference/agent-chains.md`
- Confidence adjustments for routing-matrix entries
- New conditional routing rules

**VERIFY** — Before applying any adaptation:
- Check that modified chains don't conflict with existing patterns A-F
- Ensure guardrail levels (L1-L4) remain consistent
- Validate that no agent-disambiguation rules are violated
- Confirm hub-spoke constraint is maintained

**RECORD** — After successful verification:
- Write entry to `.agents/nexus.md` journal
- Share extracted patterns with Lore via NEXUS_TO_LORE_HANDOFF
- Log routing adaptation details for audit trail

## Learning Triggers

| ID | Condition | Scope | Actions |
|----|-----------|-------|---------|
| LT-01 | Chain execution complete (every time) | Lightweight | COLLECT + EVALUATE only |
| LT-02 | Same task type fails/PARTIAL 3+ times | Full cycle | All 6 phases |
| LT-03 | User manually overrides chain selection | Full cycle | All 6 phases |
| LT-04 | Quality feedback from Judge arrives | Medium | COLLECT → EVALUATE → EXTRACT |
| LT-05 | New agent notification from Architect | Medium | Routing matrix update consideration |
| LT-06 | 30+ days since last routing learning review | Full cycle | All 6 phases |

### Trigger Priority

When multiple triggers fire simultaneously:
1. LT-03 (user override — highest signal value)
2. LT-02 (repeated failures — urgent)
3. LT-04 (quality feedback — actionable)
4. LT-05 (new agent — opportunity)
5. LT-06 (scheduled review — lowest urgency)
6. LT-01 (routine collection — always runs)

## Chain Effectiveness Score (CES)

```
CES = Success_Rate × 0.35 + Recovery_Efficiency × 0.20 + Step_Economy × 0.20 + User_Satisfaction × 0.25
```

| Component | Weight | Definition | Range |
|-----------|--------|------------|-------|
| Success_Rate | 0.35 | Proportion of executions with final STATUS=SUCCESS | 0.0–1.0 |
| Recovery_Efficiency | 0.20 | Auto-recovery success rate when errors occur | 0.0–1.0 |
| Step_Economy | 0.20 | Expected steps / Actual steps (capped at 1.0; lower actual = higher score) | 0.0–1.0 |
| User_Satisfaction | 0.25 | Proportion completed without user correction or re-execution | 0.0–1.0 |

**Journaling signal:** Journaling is the evidence base LEARN adapts from — a handoff that omits durable state or a reusable insight weakens the learning record (per `_common/HANDOFF.md` → *Pre-Handoff Journaling*). Treat this as a quality signal on the learning trail, not an automatic Success_Rate penalty: track per-agent journaling gaps, and where they persist from the same agent, surface them for review rather than silently degrading the grade.

### Grading

| Grade | CES Range | Interpretation |
|-------|-----------|----------------|
| A | ≥ 0.90 | Excellent — no changes needed |
| B | ≥ 0.80 | Good — auto-changes prohibited, human approval required |
| C | ≥ 0.70 | Acceptable — adaptation candidates |
| D | ≥ 0.60 | Below standard — adaptation recommended |
| F | < 0.60 | Poor — full LEARN cycle required |

### Minimum Data Requirements

- CES calculation requires ≥ 3 data points for the same task-type/chain combination
- Grades are provisional until ≥ 5 data points
- Trend analysis requires ≥ 10 data points

## Routing Adaptation Rules

### Adaptation Scope

| CES Grade | Allowed Adaptations |
|-----------|-------------------|
| A | None (locked) |
| B | None without human approval |
| C | Add/skip rule adjustments, agent reordering |
| D | Chain template modifications, new conditional rules |
| F | Full chain redesign, escalation to Architect |

### Adaptation Actions

1. **Agent addition**: Insert agent into chain (e.g., "+Sherpa for complex BUG tasks")
2. **Agent removal**: Remove unnecessary agent from chain (requires CES evidence)
3. **Agent reordering**: Change execution sequence within chain
4. **Skip rule creation**: Add condition to bypass agent (e.g., "skip Radar if <10 lines")
5. **Conditional routing**: Add task-type → chain fork based on context
6. **Confidence adjustment**: Boost or penalize chain selection confidence

### Application Process

1. Generate adaptation proposal with evidence (CES data, failure patterns)
2. Check against Safety Guardrails (below)
3. If within limits → apply and snapshot previous state
4. If exceeds limits → queue for human review
5. Monitor adapted routing for regression (next 3 executions)

## Safety Guardrails

| Mechanism | Rule | Rationale |
|-----------|------|-----------|
| Change volume limit | Max 5 routing-matrix entries modified per session | Prevent cascading changes |
| Auto-adaptation restriction | CES ≥ B chains: no auto-changes (human approval required) | Protect working chains |
| Rollback snapshots | Save routing state before every adaptation | Enable instant rollback |
| Diminishing returns detection | 3 consecutive adaptations with CES improvement < 0.02 → stop LEARN | Avoid over-optimization |
| Lore sync mandatory | All extracted patterns shared with Lore before adaptation | Ecosystem knowledge consistency |
| Minimum evidence | No adaptation without ≥ 3 data points | Prevent premature changes |
| Hub-spoke invariant | No adaptation may introduce direct agent-to-agent routing | Architectural constraint |
| Like-for-like baseline | CES comparison requires the same task-type/chain definition on both sides; never compare against a redefined or cherry-picked baseline | Apparent gains often come from a shifted denominator, not a better chain |
| Proxy-vs-outcome | Distinguish proxy signals (step count, token count, completion flag) from outcome signals (task actually solved, no user re-execution); a proxy improvement without an outcome improvement does not justify adaptation | Proxy metrics are gameable and overstate progress |
| Selection-bias check | Reject evidence drawn only from favorable slices (e.g. "hard cases where the old chain had room to improve"); require a representative sample of the task type | Measuring only improvable cases inflates the win rate |

### Rollback Protocol

1. Before ADAPT phase: snapshot current routing-matrix entries being modified
2. After ADAPT: monitor next 3 executions of affected chains
3. If CES drops by ≥ 0.10 from pre-adaptation baseline → auto-rollback
4. Rollback restores exact pre-adaptation state
5. Record rollback event in journal with cause analysis

### Evidence-Quality Guard

Before any CES claim or adaptation is trusted, run this checklist. It exists because self-measured improvement is systematically over-optimistic — proxy metrics, redefined baselines, and favorable sampling each manufacture gains that do not survive real use. [Source: anthropic.com/institute/recursive-self-improvement — caveats on lines-of-code as an imperfect measure, upward-biased productivity self-estimates, and non-like-for-like comparison]

| Check | Pass condition | Fail action |
|-------|----------------|-------------|
| Like-for-like | Baseline and candidate share identical task-type/chain definition and data window | Discard the comparison; recollect against a fixed baseline |
| Proxy guard | The improvement shows up in an outcome metric (Success_Rate / User_Satisfaction), not only a proxy (Step_Economy / token count) | Downgrade to "provisional"; do not adapt on proxy alone |
| Sample representativeness | Evidence covers a representative slice of the task type, not only hand-picked hard/improvable cases | Re-sample; flag selection bias in the journal |
| Self-report discount | Any agent-self-reported quality score is corroborated by an independent signal (Judge score, regression result, user non-correction) | Treat the self-report as unverified; require corroboration |

An adaptation proposal that fails any check is capped at **provisional** confidence and MUST NOT auto-apply, regardless of CES grade. Record which checks passed in the Adaptation Log.

## Autonomy Ledger (trust calibration per task type)

CES measures *how well a chain runs*; the Autonomy Ledger measures *how much we should let it run unattended*. Autonomy is earned, not assumed: it expands proportionally to demonstrated reliability and contracts immediately on regression. [Source: claude.com/blog/building-effective-human-agent-teams — "build trust incrementally", "track autonomous scope per task type".]

The ledger is keyed by **task type** (not chain) so trust transfers across chain adaptations. Each entry carries an **Autonomy Tier** that determines how much confirmation Nexus seeks in AUTORUN/AUTORUN_FULL — it *tightens* the existing confidence/reversibility gate, never loosens an **Ask First** rule.

| Tier | Stance | Confirmation behavior | Promotion precondition |
|------|--------|----------------------|------------------------|
| `T0` | Manual review | Verifier output + result surfaced for human review before SHIP | default for any task type with < 3 data points |
| `T1` | Verify-then-trust | Auto-run; a verifier agent (Judge/Radar/Attest) gate is mandatory, escalate only on verifier fail | CES ≥ C over ≥ 3 runs **and** verifier-pass on each |
| `T2` | Autonomous + spot-check | Auto-run; verifier on a sampled subset; full report at DELIVER | CES ≥ B over ≥ 5 runs, 0 user corrections, 0 rollbacks |
| `T3` | Fully autonomous | Auto-run end-to-end; report only | CES ≥ A over ≥ 10 runs **and** an explicit human grant (Ask First — never auto-promote into T3) |

**Rules:**
- **Promotion is gated, demotion is automatic.** Any rollback, user override (LT-03), or verifier fail drops the task type **one tier** and resets its consecutive-clean counter. A T3→T2 demotion additionally voids the human grant (re-granted only by a human).
- **Tier never overrides a safety gate.** L4 security, destructive actions, external-system changes, and 10+ file edits remain Ask First at every tier (per SKILL.md **Ask First**/**Never**). The ledger only governs *routine* confirmation, not red lines.
- **Per task type, never per run.** A single lucky run does not promote; the consecutive-clean counter + minimum data requirements (≥ 3 / ≥ 5 / ≥ 10) above apply.
- **Surface the tier.** Record the active tier and any tier change in the Adaptation Log and the Execution Report, so expanding/contracting autonomy is auditable rather than silent.

```markdown
## Autonomy Ledger — [TASK_TYPE]
**Tier:** [T0/T1/T2/T3] | **CES:** [grade] over [N] runs | **Consecutive clean:** [N]
**Verifier:** [Judge/Radar/Attest/none] | **Human grant (T3):** [yes/no/n-a]
**Last change:** [promoted/demoted/held] on [DATE] — [trigger: LT-XX / rollback / verifier-fail]
```

## Integration Points

| Partner | Direction | Data Exchanged |
|---------|-----------|----------------|
| Lore | Nexus → Lore | Extracted routing patterns, chain effectiveness data, failure taxonomies |
| Lore | Lore → Nexus | Cross-agent best practices, validated patterns from other agents |
| Darwin | Darwin → Nexus | Ecosystem evolution signals, agent relevance changes |
| Judge | Judge → Nexus | Code review quality feedback affecting chain assessment |
| Judge | Judge → Nexus | Quality assessment results, output quality scores |
| Architect | Architect → Nexus | New agent notifications, capability descriptions for routing integration |

### Lore Sync Protocol

After EXTRACT phase, share with Lore:
- Pattern ID and description
- Supporting evidence (CES data, failure counts)
- Affected task types and chains
- Confidence level (provisional / confirmed)

Lore may respond with:
- Validation (pattern confirmed across ecosystem)
- Contradiction (pattern conflicts with other agent learnings)
- Enhancement (additional context from other agents)

## Templates

### Feedback Record

```markdown
## Routing Feedback — [CHAIN_ID]

**Task Type:** [TYPE] | **Chain:** [AGENT1 → AGENT2 → ...] | **Mode:** [AUTORUN_FULL/AUTORUN/GUIDED]
**Status:** [SUCCESS/PARTIAL/BLOCKED/FAILED] | **Steps:** [ACTUAL]/[EXPECTED]
**CES:** [SCORE] ([GRADE]) | **Previous CES:** [SCORE] ([GRADE])

**Events:**
- [Timestamp] [Event description]

**User Corrections:** [None / Description of manual override]
**Recovery Actions:** [None / Description of auto-recovery]
```

### Pattern Report

```markdown
## Routing Pattern — [PATTERN_ID]

**Type:** [Success/Failure/Recovery] | **Confidence:** [Provisional/Confirmed]
**Affected Task Types:** [LIST] | **Data Points:** [COUNT]

**Pattern:** [Description of observed pattern]
**Evidence:** [CES trends, failure counts, user override frequency]
**Recommended Action:** [Specific adaptation proposal]
**Risk:** [Impact if applied / Impact if not applied]
```

### Adaptation Log

```markdown
## Routing Adaptation — [ADAPTATION_ID]

**Date:** [DATE] | **Trigger:** [LT-XX]
**Before:** [Previous routing configuration]
**After:** [New routing configuration]
**Evidence:** [CES data, pattern references]
**Rollback Snapshot:** [SNAPSHOT_ID]
**Verification Status:** [Pending/Passed/Rolled-back]
**Post-adaptation CES:** [SCORE] ([GRADE]) — measured after [N] executions
```
