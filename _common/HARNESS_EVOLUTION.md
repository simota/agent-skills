# Harness Evolution Protocol

Systematic re-evaluation of orchestration scaffolding as model capabilities improve. Scaffolding that was necessary for earlier models may become overhead for stronger models.

---

## Principles

> Every piece of scaffolding encodes an assumption about model limitations. As models improve, assumptions must be re-tested and scaffolding simplified or removed when no longer needed.

### Stale Assumptions (Managed Agents Pattern)

Harnesses encode assumptions about model limitations that become outdated as capabilities improve. Workarounds for earlier models (e.g., context anxiety mitigations, verbose chain decomposition) become "dead weight" for stronger models. Treat every scaffolding component as a hypothesis with an expiration date.

**Application:** Each HE component below tests whether its underlying assumption still holds. When the assumption expires, simplify or remove the scaffolding.

### Systematic Scaffold Audit ("What Can I Stop Doing?")

> Source: Anthropic "Harnessing Claude's Intelligence" (2025)

Periodically audit all scaffolding components using this protocol:

1. **Enumerate** — List every scaffolding component (guardrails, decomposition steps, recovery chains, context management workarounds)
2. **State the assumption** — For each component, document the model limitation it was designed to compensate for
3. **Test the assumption** — Verify whether that limitation still holds with the current model generation. Three audit dimensions:
   - **Orchestration**: Can the agent self-filter tool outputs via code execution instead of routing through context?
   - **Context management**: Can the agent use progressive disclosure (skills, on-demand file reads) instead of pre-loaded instructions?
   - **Persistence**: Can the agent use file-based memory (memory folders) instead of in-context accumulation?
4. **Propose simplification** — If the assumption no longer holds, feed into the HE evaluation cycle (below) for measured simplification

This protocol makes the implicit logic behind HE-01 through HE-06 explicit and systematic. Run it aligned with Darwin's 30-day review cycle (ET-06).

### Interface Stability over Implementation

> "Opinionated about interfaces, unopinionated about implementations."

Design stable contracts (handoff formats, `_STEP_COMPLETE` schema, `NEXUS_HANDOFF` structure) that outlast specific model capabilities. Implementations behind the interface (chain selection, agent internals, recovery strategies) can evolve freely without breaking the contract. When evolving scaffolding, change the implementation — not the interface — unless the interface itself is the bottleneck.

### Stateless Orchestrator (Cattle, not Pets)

Orchestrators (Nexus, Rally) should be stateless and replaceable. Session state (handoff context, checkpoint data, execution logs) must live outside the orchestrator so that:
- Orchestrator interruption does not lose progress
- Any orchestrator instance can resume from the last checkpoint
- Debugging does not require access to the orchestrator's internal state

**Current implementation:** `.agents/PROJECT.md` activity log + `_STEP_COMPLETE` handoff chain + journal files serve as the external session log. Checkpoint-resume in AUTORUN (4+ step chains) provides crash recovery.

---

## Metrics Definitions

| Metric | Full Name | Formula | Purpose |
|--------|-----------|---------|---------|
| **CES** | Chain Effectiveness Score | `Success_Rate(0.35) + Recovery_Efficiency(0.20) + Step_Economy(0.20) + User_Satisfaction(0.25)` | Overall chain quality (defined in Nexus SKILL.md) |
| **TES** | Token Efficiency Score | `output_information_tokens / total_tokens_consumed` | Cost efficiency — detects context bloat and unnecessary verbosity |
| **UQS** | User Quality Score | User satisfaction rating (1-5) averaged over chain deliverables | Subjective quality — captures what metrics miss |

**Grading:** A (>= 0.85), B (>= 0.70), C (>= 0.55), D (< 0.55)

---

## Evaluation Components

| ID | Component | Assumption | Simplification Condition | Measurement |
|----|-----------|-----------|-------------------------|-------------|
| HE-01 | Guardrail Levels | Models frequently make critical mistakes | L2+ trigger frequency drops 50% over baseline | Count L2/L3/L4 triggers per 100 tasks |
| HE-02 | Agent Chain Length | Multi-agent decomposition produces better results | CES grade A + step_economy approaches 1.0 | CES score with single-agent vs multi-agent |
| HE-03 | Recovery Chains | Auto-recovery is frequently needed | Recovery invocation rate drops below 5% | Recovery triggers per 100 executions |
| HE-04 | Context Reset Strategy | Sonnet struggles with large context | `continuous` strategy shows no quality degradation vs `reset` | UQS comparison across strategies |
| HE-05 | Evaluator Loop Iterations | Multiple loops needed for quality | First-iteration ACCEPT rate exceeds 80% | ACCEPT rate at iteration 1 |
| HE-06 | Sprint Contract Detail | Detailed contracts needed for alignment | Contract-free executions show no quality degradation | UQS comparison with/without contracts |

---

## Evaluation Cycle

**Frequency:** Aligned with Darwin ET-06 (30-day ecosystem review cycle).

**Process:**

```
1. Collect metrics for each HE component (minimum 3 data points)
     ↓
2. Compare against simplification conditions
     ↓
3. For each component meeting its condition:
     a. Propose simplification (documented in EVOLUTION_SIGNAL)
     b. Run A/B comparison (3 tasks minimum)
     c. Measure CES/TES/UQS impact
     ↓
4. Apply or reject simplification
     ├─ CES/TES drop <= 0.05 → Apply (safe simplification)
     ├─ CES/TES drop 0.05-0.10 → Apply with monitoring (1 cycle)
     └─ CES/TES drop > 0.10 → Reject (rollback immediately)
```

---

## Safety Guards

### Hard Constraints

- **Security scaffolding is exempt.** Never simplify Sentinel checks, L4 guardrails, or security-related recovery chains regardless of metrics.
- **Minimum data requirement.** At least 3 data points before any simplification decision.
- **Immediate rollback trigger.** If CES or TES drops more than 0.10 after simplification, rollback immediately without waiting for the full evaluation cycle.
- **One component at a time.** Never simplify multiple components simultaneously — isolate the impact of each change.

### Rollback Protocol

```
Simplification applied
  ↓
Monitor for 1 evaluation cycle (or until 5 tasks executed)
  ↓
CES/TES regression detected?
  ├─ > 0.10 drop → Immediate rollback, log as failed simplification
  ├─ 0.05-0.10 drop → Extend monitoring for 1 more cycle
  │    └─ Still regressed → Rollback
  │    └─ Recovered → Keep simplification
  └─ <= 0.05 drop → Simplification confirmed successful
```

---

## Evolution Signal Format

When a simplification is proposed or applied, emit an `EVOLUTION_SIGNAL`:

```markdown
<!-- EVOLUTION_SIGNAL
type: DRIFT
source: nexus
date: YYYY-MM-DD
summary: "HE-05: First-iteration ACCEPT rate at 85% (threshold: 80%). Proposing Max_Iterations reduction from 3 to 2."
affects: ["nexus", "evaluator-loop-protocol"]
priority: MEDIUM
reusable: true
-->
```

---

## Simplification Examples

### HE-01: Guardrail Reduction

**Before:** L2 checkpoint after every agent step.
**After:** L2 checkpoint only at VERIFY phase; L1 monitoring during EXECUTE.
**Condition met when:** L2+ triggers per 100 tasks < 5 (was 10+ at baseline).

### HE-02: Chain Compression

**Before:** Scout → Builder → Radar (3 agents).
**After:** Builder → Radar (2 agents; Builder subsumes investigation).
**Condition met when:** CES grade A with Scout skipped AND step_economy >= 0.9.

### HE-05: Evaluator Loop Reduction

**Before:** Max 3 iterations with full Evaluator team.
**After:** Max 2 iterations, or single-pass evaluation for low-complexity tasks.
**Condition met when:** First-iteration ACCEPT rate > 80%.

### HE-06: Contract Simplification

**Before:** Full SPRINT_CONTRACT with detailed acceptance criteria.
**After:** Lightweight contract (Goal + Scope only) or contract skipped for MEDIUM complexity.
**Condition met when:** UQS shows no degradation without detailed contracts.

---

## Tracking

Record harness evolution decisions in `.agents/nexus.md` journal:

```markdown
### Harness Evolution [YYYY-MM-DD]
- Component: HE-[ID]
- Action: [simplified | retained | rolled-back]
- Data points: [N]
- CES/TES impact: [delta]
- Decision: [rationale]
```

Integration with Darwin: Harness evolution findings are reported as `EVOLUTION_SIGNAL` type `DRIFT` for ecosystem-wide tracking. Darwin may incorporate these signals into its Ecosystem Fitness Score (EFS) assessment.

---

## Open Follow-ups

#TODO(agent): Fold the most recent Scaffold Audit cycle results back into `nexus/SKILL.md` and `_common/AUTORUN.md`. (The 2026-07 audit corrected cross-model retirement scaffolding and version drift in `_common/`; the next cycle should re-verify HE-01 L1-L4 checkpoint trigger frequency against the current model generation and simplify per the Evaluation Cycle if the condition is met.)
