# Nexus Result Validation Protocol

Purpose: Read this file when Titan receives `## NEXUS_COMPLETE_[STATUS]`, validates resulting artifacts, maps status into Anti-Stall, or updates `TITAN_STATE`.

## Contents

- `NEXUS_COMPLETE` status types
- Result validation flow
- Phase-specific required artifacts
- Status to Anti-Stall mapping
- `TITAN_STATE` update rules

Defines how Titan validates and responds to Nexus chain completion results.

---

## NEXUS_COMPLETE Status Types

When an Epic chain completes, Nexus returns `## NEXUS_COMPLETE_[STATUS]` with one of four statuses:

| Status | Meaning | Titan Response |
|--------|---------|---------------|
| **FULL** | All steps completed, all acceptance criteria met | Update TITAN_STATE → next Epic |
| **PARTIAL** | Some steps completed, some criteria unmet | Validate artifacts → Anti-Stall L1 |
| **BLOCKED** | Chain halted on external dependency | Validate partial → Anti-Stall L2 |
| **FAILED** | Chain failed, no usable output | Anti-Stall L1 Agent swap |

### `recovery_attempted` Field

Nexus includes a `recovery_attempted` field in `NEXUS_COMPLETE_[STATUS]` to indicate whether internal recovery was already executed before reporting to Titan. This prevents duplicate retry efforts and wasted Anti-Stall budget.

```markdown
## NEXUS_COMPLETE_[STATUS]
recovery_attempted: true | false
recovery_actions: [list of recovery actions taken by Nexus, if any]
recovery_result: [outcome of Nexus-level recovery]
```

| `recovery_attempted` | Meaning |
|---------------------|---------|
| `false` | Nexus reported status without attempting recovery (e.g., external block) |
| `true` | Nexus already attempted L1-L3 internal recovery before reporting |

---

## Result Validation Flow

```
NEXUS_COMPLETE_[STATUS] received
  ├─ 1. Parse status and chain output
  ├─ 2. Run phase-specific artifact checklist
  ├─ 3. Validate artifact quality (exists + non-empty + format correct)
  ├─ 4. Update TITAN_STATE with results
  └─ 5. Route to next action based on status + validation result
```

### Validation Decision Matrix

| Status | Artifacts Valid | Action |
|--------|---------------|--------|
| FULL | Yes | Next Epic immediately |
| FULL | No (unexpected) | Re-validate → L1 if confirmed missing |
| PARTIAL | Partial | Identify gaps → L1 Retry missing items only |
| PARTIAL | None valid | Treat as FAILED |
| BLOCKED | Partial | Accept valid → L2 Skip blocked items |
| BLOCKED | None | L2 Alt approach or Skip+return |
| FAILED | Salvageable | Extract valid parts → L1 Agent swap for remainder |
| FAILED | None | L1 Agent swap → L2 if swap fails |

---

## Phase-Specific Required Artifacts

Single source of truth for phase-specific artifact requirements and exit criteria: `reference/exit-criteria-validation.md`.

When validating `NEXUS_COMPLETE` results, check artifacts against the phase-specific validation checklists defined there. Key validation rules:

- **Required** artifacts must be present and non-empty for the phase to pass.
- **Recommended** artifacts improve the exit score but are not blocking.
- **Conditional** artifacts depend on scope or project type (e.g., A/B setup is XL only).
- Use the scope-adaptive validation rules (S/M/L/XL) to determine which phases and criteria apply.

---

## Status → Anti-Stall Mapping

### Conditionalized Anti-Stall Entry (recovery_attempted aware)

| Nexus Status | `recovery_attempted` | Anti-Stall Entry | Rationale |
|-------------|---------------------|-----------------|-----------|
| PARTIAL | `false` | **L1** (1.1 Retry) | Nexus didn't retry; Titan retries with context |
| PARTIAL | `true` | **L1** (1.3 Decompose) | Retry already failed; skip to decomposition |
| BLOCKED | `false` | **L2** (2.2 Skip+return) | External block; skip and return later |
| BLOCKED | `true` | **L2** (2.1 Alt approach) | Nexus already attempted workaround; escalate |
| FAILED | `false` | **L1** (1.2 Agent swap) | Agent-level failure; try alternative first |
| FAILED | `true` | **L2** (2.1 Alt approach) | Agent swap already attempted by Nexus; escalate |

**Rule**: When `recovery_attempted: true`, Titan skips the recovery level that Nexus already exhausted and enters Anti-Stall at the next effective level. This prevents duplicate retries and conserves Anti-Stall budget.

### Escalation from Nexus Failures

```
PARTIAL → L1.1 Retry with gap context
  └─ Still PARTIAL → L1.3 Decompose (smaller chains)
    └─ Still failing → L2.3 Scope Reduction (accept partial)

BLOCKED → L2.2 Skip+return (continue other Epics)
  └─ All Epics blocked → L2.1 Alt approach
    └─ Still blocked → L3.1 Phase reorder

FAILED → L1.2 Agent swap
  └─ Still FAILED → L1.3 Decompose
    └─ Still FAILED → L2.1 Alt approach
```

---

## TITAN_STATE Update Rules

On receiving any `NEXUS_COMPLETE_[STATUS]`:

1. **Record**: Add to Epic history with status, artifacts, timestamp
2. **Accumulate**: Update phase completion percentage
3. **Track**: Increment stall counters if PARTIAL/BLOCKED/FAILED
4. **Persist**: Write updated state to `.agents/titan-state.md`

### State Fields Updated

```markdown
## Current Phase Status
- Epic [N]: [STATUS] — artifacts: [list] — recovery: [none/L1/L2/...]
- Phase completion: [X]% ([completed]/[total] Epics)
- Consecutive failures: [N] (threshold: 3 → escalate)
```

### Consecutive Failure Escalation

| Consecutive Failures | Action |
|---------------------|--------|
| 1 | Normal Anti-Stall routing per status |
| 2 | Bump Anti-Stall +1 level (L1→L2, L2→L3) |
| 3+ | Mandatory Magi consultation before next attempt |
