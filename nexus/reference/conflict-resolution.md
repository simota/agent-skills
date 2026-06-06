# Nexus Conflict Resolution Reference

**Purpose:** Rules for detecting and resolving parallel-branch conflicts.
**Read when:** Parallel work touched overlapping files, logic, or ownership boundaries.
**See also:** This file handles conflicts that have already occurred at merge time. To **prevent** divergence before routing, see `handoff-validation.md` (handoff field requirements + integrity checks).

## Contents
- Overview
- Conflict Classification
- Auto-Resolution Strategies
- Ownership Scoring
- Resolution Flow
- Conflict Event Format
- Integration with Orchestration
- Confidence Thresholds
- Learning Loop

Automatic conflict resolution for parallel branch execution.

---

## Overview

When parallel branches modify overlapping files, conflicts must be resolved. This system enables automatic resolution for common cases, reducing user intervention.

---

## Conflict Classification

| Type | Description | Auto-Resolve |
|------|-------------|--------------|
| ADJACENT | Changes to different parts of same file | ✅ Yes |
| FORMATTING | Only whitespace/style differences | ✅ Yes |
| SEMANTIC | Same logic modified differently | ⚠️ Conditional |
| STRUCTURAL | Incompatible architectural changes | ❌ No |

---

## Auto-Resolution Strategies

### 1. Adjacent Changes (Always Auto-Resolve)

```yaml
ADJACENT_MERGE:
  description: Changes in different sections of same file
  detection:
    - No overlapping line ranges
    - Changes >= 10 lines apart

  resolution:
    action: ACCEPT_BOTH
    order: chronological  # Earlier change first
    verify: syntax_check

  example:
    branch_a: Lines 10-20 modified
    branch_b: Lines 50-60 modified
    result: Both changes merged
```

### 2. Formatting-Only (Always Auto-Resolve)

```yaml
FORMATTING_MERGE:
  description: Only whitespace, indentation, or style changes
  detection:
    - AST/semantic content identical
    - Only formatting differs

  resolution:
    action: REGENERATE
    tool: prettier/eslint/black (per project)
    verify: no_semantic_change

  example:
    branch_a: Tabs → Spaces
    branch_b: Added trailing commas
    result: Run formatter, accept output
```

### 3. Semantic Conflict (Conditional Auto-Resolve)

```yaml
SEMANTIC_MERGE:
  description: Same code modified with different intent
  detection:
    - Overlapping line ranges
    - Different semantic changes

  resolution:
    condition: ownership_score >= 0.70

    if_owner_clear:
      action: OWNERSHIP_PRIORITY
      keep: higher_ownership_branch
      log: "Resolved by ownership: [branch] owns [file]"

    if_owner_unclear:
      action: ESCALATE
      trigger: ON_PARALLEL_CONFLICT

  ownership_calculation:
    factors:
      - primary_agent_role: 0.40  # Who is the specialist?
      - more_changes: 0.30        # Who changed more?
      - task_alignment: 0.30      # Whose task is this file for?
```

### 4. Structural Conflict (Never Auto-Resolve)

```yaml
STRUCTURAL_CONFLICT:
  description: Incompatible architectural changes
  detection:
    - Different function signatures
    - Conflicting imports/exports
    - Breaking API changes

  resolution:
    action: ESCALATE_ALWAYS
    trigger: ON_STRUCTURAL_CONFLICT
    provide:
      - both_versions
      - impact_analysis
      - recommended_resolution
```

---

## Ownership Scoring

Determine which branch "owns" a file for conflict resolution:

```yaml
ownership_score:
  calculation:
    primary_agent_role: 0.40
    change_volume: 0.30
    task_alignment: 0.30

  primary_agent_role:
    # Who is the domain specialist?
    Builder_on_logic: 0.90
    Artisan_on_ui: 0.90
    Schema_on_db: 0.90
    Sentinel_on_security: 0.90
    other: 0.50

  change_volume:
    # Who made more changes?
    more_lines: 0.80
    similar_lines: 0.50
    fewer_lines: 0.20

  task_alignment:
    # Is this file central to their task?
    primary_target: 0.90
    related_file: 0.60
    incidental_change: 0.30
```

### Example Ownership Calculation

```yaml
scenario:
  file: src/auth/login.ts
  branch_a:
    agent: Builder
    task: "Fix login bug"
    lines_changed: 45
  branch_b:
    agent: Sentinel
    task: "Add input validation"
    lines_changed: 12

ownership:
  branch_a:
    primary_agent_role: 0.90 × 0.40 = 0.36  # Builder on logic
    change_volume: 0.80 × 0.30 = 0.24       # More lines
    task_alignment: 0.90 × 0.30 = 0.27      # Primary target
    total: 0.87

  branch_b:
    primary_agent_role: 0.70 × 0.40 = 0.28  # Sentinel adding validation
    change_volume: 0.20 × 0.30 = 0.06       # Fewer lines
    task_alignment: 0.60 × 0.30 = 0.18      # Related but not primary
    total: 0.52

resolution: Branch A wins (0.87 > 0.70 threshold)
           Branch B changes applied on top if non-conflicting
```

---

## Resolution Flow

```
Parallel Branches Complete
          │
          ▼
┌─────────────────────┐
│ Detect Conflicts    │ → List all conflicting files
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Classify Each       │ → ADJACENT | FORMATTING | SEMANTIC | STRUCTURAL
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
  Auto-OK    Needs Decision
     │           │
     ▼           ▼
  Merge      Calculate
  Directly   Ownership
     │           │
     │      ┌────┴────┐
     │      ▼         ▼
     │   >= 0.70   < 0.70
     │      │         │
     │      ▼         ▼
     │   Owner     Escalate
     │   Priority  to User
     │      │         │
     └──────┴────┬────┘
                 ▼
          Apply Resolution
                 │
                 ▼
          Verify (tests)
```

---

## Conflict Event Format

```yaml
_CONFLICT_EVENT:
  files:
    - path: [File path]
      type: [ADJACENT|FORMATTING|SEMANTIC|STRUCTURAL]
      branches: [A, B]
      resolution: [ACCEPT_BOTH|REGENERATE|OWNERSHIP_PRIORITY|ESCALATED]

  auto_resolved:
    - file: [path]
      method: [method]
      confidence: 0.XX

  escalated:
    - file: [path]
      reason: [Why auto-resolution not possible]
      options: [Possible resolutions]

  outcome: [FULLY_RESOLVED|PARTIALLY_RESOLVED|USER_REQUIRED]
```

---

## Integration with Orchestration

### Pattern B Enhancement

```yaml
pattern_b_parallel:
  on_branch_complete:
    1. Collect NEXUS_HANDOFF from all branches
    2. Identify file overlaps
    3. Classify conflicts
    4. Auto-resolve where possible
    5. Escalate remainder

  merge_order:
    - Highest ownership first
    - Then chronological
    - Formatting pass last
```

### Pre-merge Checklist

```yaml
pre_merge_check:
  all_branches_complete: true
  conflict_classification_done: true
  auto_resolutions_applied: true
  tests_pass_per_branch: true

  if_all_pass:
    action: AGGREGATE
    then: VERIFY (full test suite)

  if_conflicts_remain:
    action: ESCALATE
    present: conflict_summary_to_user
```

---

## Confidence Thresholds

| Scenario | Auto-Resolve Threshold |
|----------|------------------------|
| Adjacent changes | Always (confidence: 1.0) |
| Formatting only | Always (confidence: 1.0) |
| Semantic with clear owner | >= 0.70 ownership |
| Semantic with unclear owner | Escalate |
| Structural | Never (always escalate) |

---

## Learning Loop

Track resolution outcomes for improvement:

```yaml
resolution_learning:
  on_successful_auto_resolve:
    - Record pattern
    - Boost similar cases

  on_user_override:
    - Record the correction
    - Adjust ownership weights
    - Add to .agents/nexus.md

  metrics:
    auto_resolve_rate: target > 80%
    user_override_rate: target < 10%
    post_resolve_test_pass: target > 95%
```
