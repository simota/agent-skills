# Nexus Confidence Scoring & Autonomous Decision Reference

**Purpose:** Compute task-understanding confidence from multiple context sources and translate the score into an autonomous proceed / ask decision.
**Read when:** You're in CLASSIFY (need a confidence score) or about to act (need a threshold check), or both.

This file merges the former `context-scoring.md` (what to compute) and `auto-decision.md` (what to do with the score). Treat the two halves below as one pipeline: **Sources → Score → Threshold → Decision → Action**.

---

## Pipeline Overview

```
Context sources ──► weighted score ──► confidence level ──► decision-type threshold ──► proceed / ask
   (Part 1)            (Part 1)         (Part 1)              (Part 2)               (Part 2)
                                                                  │
                                                                  ▼
                                                            Blocker check
                                                            (Safety Overrides)
```

High-confidence + reversible → proceed automatically with documented assumptions.
Low-confidence or blocker → clarify via `intent-clarification.md` or ask the user.

---

# Part 1: Confidence Scoring

## Scoring Sources

| Source | Weight | Description |
|--------|--------|-------------|
| `git_history` | 0.30 | Recent commits, branches, changes in progress |
| `project_md` | 0.25 | `.agents/PROJECT.md` activity log, shared knowledge |
| `conversation` | 0.25 | Current session context, user messages |
| `codebase` | 0.20 | File structure, existing patterns, dependencies |

### Source Signals & Sub-scores

| Source | Signals | Score contributions |
|--------|---------|---------------------|
| `git_history` | current branch, recent commits, uncommitted changes, branch-name pattern (fix/, feat/, ...) | branch matches task +0.15 / commits related +0.10 / uncommitted relevant +0.05 |
| `project_md` | activity log, shared knowledge, known issues | activity matches +0.15 / knowledge relevant +0.07 |
| `conversation` | explicit requirements, implicit intent, previous corrections | clear explicit +0.20 / inferable implicit +0.10 |
| `codebase` | file patterns, similar implementations, dependency graph | clear pattern +0.15 / partial patterns +0.08 |

## Confidence Thresholds

| Level | Score Range | Default Action |
|-------|-------------|----------------|
| HIGH | ≥ 0.80 | Auto-proceed without confirmation |
| MEDIUM | 0.60 – 0.79 | Proceed with stated assumptions |
| LOW | 0.40 – 0.59 | Single clarification question |
| VERY_LOW | < 0.40 | Multi-step clarification via `intent-clarification.md` |

## Scoring Calculation

```
Final = git_score × 0.30 + project_score × 0.25 + conversation_score × 0.25 + codebase_score × 0.20
      → confidence (0.00 – 1.00)
```

### Simplified Scoring (cross-model)

When weighted arithmetic is difficult, classify each source qualitatively (3/2/1/0) and sum:

| Source | HIGH (3) | MEDIUM (2) | LOW (1) | NONE (0) |
|--------|----------|------------|---------|----------|
| `git_history` | Branch + commits match | Some related commits | Repo exists, no match | No git info |
| `project_md` | Activity directly matches | Related activity found | File exists, no match | No file |
| `conversation` | Explicit clear request | Inferable intent | Vague request | No context |
| `codebase` | Clear pattern to follow | Partial patterns exist | Files exist, no pattern | No codebase |

| Total (max 12) | Level | Default Action |
|----------------|-------|----------------|
| 10-12 | HIGH | AUTO_PROCEED |
| 7-9 | MEDIUM | PROCEED_WITH_ASSUMPTIONS |
| 4-6 | LOW | SINGLE_CLARIFICATION |
| 0-3 | VERY_LOW | STRUCTURED_CLARIFICATION |

### Worked Example

```yaml
task: "Fix the login issue"
analysis:
  git_history:    {branch: "fix/auth-timeout", commits: ["fix: extend session"], score: 0.28}
  project_md:     {activity: "Scout investigated auth module yesterday", score: 0.18}
  conversation:   {explicit: "login doesn't work", implicit: "user frustrated", score: 0.12}
  codebase:       {patterns: "auth/* exists", score: 0.12}
final_score: 0.70      # = 0.28 + 0.18 + 0.12 + 0.12
level: MEDIUM
action: PROCEED_WITH_ASSUMPTIONS
```

## Boosters and Penalties

| Boost | Signal |
|-------|--------|
| +0.10 | User confirmed similar task before |
| +0.10 | Single valid interpretation |
| +0.05 | Existing tests for target area |
| +0.05 | Small scope (< 3 files) |

| Penalty | Signal |
|---------|--------|
| −0.15 | Multiple valid interpretations |
| −0.10 | No git history for area |
| −0.10 | User previously corrected similar |
| −0.05 | Large scope (> 10 files) |
| −0.05 | Security-sensitive area |

## Context Snapshot Format

```yaml
_CONTEXT_SNAPSHOT:
  timestamp: <ISO>
  task: <original request>
  scores: {git_history: 0.XX, project_md: 0.XX, conversation: 0.XX, codebase: 0.XX, final: 0.XX}
  confidence_level: HIGH | MEDIUM | LOW | VERY_LOW
  signals: {git: [...], project: [...], conversation: [...], codebase: [...]}
  assumptions: [...]
  recommended_action: AUTO_PROCEED | PROCEED_WITH_ASSUMPTIONS | CLARIFY
```

---

# Part 2: Autonomous Decision

## Decision-Type Thresholds

A higher-stakes decision needs a higher confidence floor. The same final score may auto-proceed for one decision type and ask for another.

| Decision Type | Threshold | Min Level (simplified) | Rationale |
|---------------|-----------|------------------------|-----------|
| Chain Selection | ≥ 0.85 | HIGH | Wrong chain wastes significant effort |
| Approach Selection | ≥ 0.80 | MEDIUM+ | Approaches are usually recoverable |
| Agent Routing | ≥ 0.80 | MEDIUM+ | Misrouting causes delays |
| Recovery Action | ≥ 0.75 | MEDIUM | Recovery is inherently corrective |
| Parallel vs Sequential | ≥ 0.70 | MEDIUM | Both are valid, different efficiency only |

`MEDIUM+` = MEDIUM with no blocking open questions. With open questions, downgrade to LOW.

## Auto-Proceed Conditions

```yaml
AUTO_PROCEED_IF:
  all_required:
    - confidence >= threshold_for_decision_type
    - no_l4_security_implications
    - action_is_reversible
  any_blocking:
    - l4_security_trigger          # Always asks
    - data_destructive_action      # Deletions, migrations
    - external_system_modification # APIs, deployments
    - cost_incurring_action        # Cloud, payments
```

## Per-Decision-Type Rules

### Chain Selection (threshold ≥ 0.85)
- **Auto when**: single best-fit chain, context indicates task type cleanly, no conflicting signals.
- **Ask when**: multiple equally valid chains, task type ambiguous, user-preference history unclear.

### Approach Selection (threshold ≥ 0.80)
- **Auto when**: clear best approach, matches project patterns, low risk if wrong.
- **Ask when**: trade-offs are significant, user preference unknown, approaches yield different outcomes.

### Recovery Action (threshold ≥ 0.75)
- **Auto when**: clear recovery path, previous similar recovery succeeded, rollback available.
- **Ask when**: multiple recovery options, recovery might lose work, previous recovery failed.

### Agent Routing (threshold ≥ 0.80)
- **Auto when**: clear agent-task match, agent available, no specialist override needed.
- **Ask when**: multiple specialists could help, capabilities overlap, task spans domains.

## Decision Flow

```
task / decision needed
        │
        ▼
  Compute confidence (Part 1)
        │
        ▼
  Threshold check (this section)
   ┌────┴────┐
   ▼         ▼
 ≥ thr.   < thr.
   │         │
   ▼         ▼
 Blocker  Prepare
 check?   question
   │         │
 ┌─┴─┐       ▼
 ▼   ▼   Ask user
 OK  Blk     │
 │   │       ▼
 ▼   ▼   Integrate
 Auto Ask answer
       │     │
       └──┬──┘
          ▼
     Execute decision
```

## Reversibility Assessment

| Category | Examples | Auto-Proceed |
|----------|----------|--------------|
| Fully reversible | Code edits (git), test runs, lint fixes | Yes |
| Easily reversible | Config changes, refactoring | Yes |
| Moderately reversible | DB migrations with rollback | With caution + confirmation |
| Difficult to reverse | Data deletion, external API calls | No |
| Irreversible | Production deploy, payments, key rotation | Never auto |

## Safety Overrides (ALWAYS_ASK)

These bypass the threshold and unconditionally require user confirmation:

```yaml
ALWAYS_ASK:
  security:  [credential_changes, auth_modifications, permission_changes, encryption_key_ops]
  data:      [bulk_deletion, schema_breaking_changes, user_data_export]
  external:  [production_deploy, external_api_key_usage, payment_ops, third_party_integrations]
  scope:     [changes_affecting_10plus_files, architectural_changes, breaking_api_changes]
```

## Confidence Degradation

```yaml
degradation_triggers:
  consecutive_errors:        -0.10 per error
  user_correction:           -0.15 for this session
  unexpected_state:          -0.10
  missing_expected_file:     -0.05

recovery:
  successful_execution:      +0.05
  user_confirmation:         restore to baseline
  explicit_approval:         +0.10 for similar decisions
```

## Mode-Specific Behavior

| Mode | Auto-Decision Behavior |
|------|------------------------|
| AUTORUN_FULL | Full auto-decision with guardrails |
| AUTORUN | Auto for SIMPLE, ask for COMPLEX |
| GUIDED | Auto with confirmation at decision triggers |
| INTERACTIVE | No auto-decision, ask everything |

## Auto-Decision Record Format

```yaml
_AUTO_DECISION:
  decision_type: chain_selection | approach | recovery | routing
  confidence: 0.XX
  threshold: 0.XX
  decision: <what was decided>
  assumptions: [...]
  signals_used: [...]
  reversibility: fully | easily | moderate
  rollback_plan: <how to undo if wrong>
```

---

## Usage in Execution Phases

### PLAN / CLASSIFY
1. Gather context from all sources.
2. Compute confidence (Part 1).
3. Match against decision-type threshold (Part 2).
4. If HIGH/MEDIUM + reversible + no blockers → proceed to CHAIN_SELECT.
5. Else → clarify first (see Low-Confidence Clarification below).

### CHAIN_SELECT
- Multiple valid chains + confidence ≥ 0.85 → auto-select highest-fit.
- Multiple valid chains + confidence < 0.85 → present options (use `routing-explanation.md`).

### EXECUTE
- Pass `_CONTEXT_SNAPSHOT` to agents so they share assumptions.
- New information contradicting assumptions → re-score and potentially pause.

## Low-Confidence Clarification

When confidence is LOW or VERY_LOW:

1. Read `intent-clarification.md` for the methodology.
2. Resolve ambiguity, ask one focused question if needed.
3. Feed clarification back into scoring:
   - Clarified intent → +0.20 to conversation score.
   - Resolved assumptions → remove penalties.
   - User correction → log for future scoring.

## Integration with Other Systems

| System | Interaction |
|--------|-------------|
| Guardrails (`guardrails.md`) | Auto-decision proceeds → guardrails monitor execution → L3/L4 escalate back to user |
| Handoff Validation (`handoff-validation.md`) | Agent completes → handoff confidence checked → auto-decision routes to next agent or asks |
| Routing Learning (`routing-learning.md`) | Auto-decision outcomes feed CES — successes raise thresholds, corrections lower them |

## Metrics and Learning

```yaml
metrics:
  auto_decision_count: N
  accuracy_rate: X%       # Decisions not later corrected
  by_type:
    chain_selection:  {count: N, accuracy: X%}
    approach:         {count: N, accuracy: X%}
    recovery:         {count: N, accuracy: X%}
    routing:          {count: N, accuracy: X%}

learning:
  on_success:
    - Record signals that led to correct decision
    - Boost similar patterns in future
  on_correction:
    - Record gap between assumption and reality
    - Adjust threshold (+0.05 conservative) for this pattern
    - Append to .agents/nexus.md as learned pattern
```
