# Nexus Proactive Mode Reference

**Purpose:** Project-scan flow and recommendation logic for `/Nexus` with no task.
**Read when:** Nexus is invoked without arguments and needs to recommend next actions.

## Contents
- Trigger Conditions
- Analysis Phases
- Output Format
- User Interaction
- Relationship to AUTORUN
- Lightweight Execution Guidelines

Mode that auto-activates when `/Nexus` is invoked by itself with no arguments.

---

## Trigger Conditions

| Condition | Activation |
|-----------|------------|
| `/Nexus` only (no arguments) | ✅ PROACTIVE_MODE |
| `/Nexus [task]` | ❌ Standard routing |
| `## NEXUS_AUTORUN` | ❌ Standard AUTORUN |
| `## NEXUS_HANDOFF` | ❌ Continuation flow |

---

## Analysis Phases

### Phase 0-A: Project State Scan

**1. Git Status Check**
```bash
git status --porcelain
```
- Whether uncommitted changes exist
- Staging status
- Untracked files

**2. Activity Log Review**
```
.agents/PROJECT.md → Activity Log section
```
- Most recent activity timestamp
- Most recent agent
- Most recent work summary

**3. Commit Pattern Analysis**
```bash
git log --oneline -10
```
- Recent work patterns
- Frequently touched files/directories
- Commit types (`feat`/`fix`/`refactor`, etc.)

---

### Phase 0-B: Health Assessment

Assess project health across four indicators:

| Indicator | Evaluation Method | Status |
|-----------|-------------------|--------|
| `test_health` | Test results, coverage | 🟢/🟡/🔴 |
| `security_health` | Vulnerability scans, dependencies | 🟢/🟡/🔴 |
| `code_health` | Lint warnings, type errors | 🟢/🟡/🔴 |
| `doc_health` | README freshness, JSDoc coverage | 🟢/🟡/🔴 |

**Assessment Criteria:**
- 🟢 Healthy: No issues detected
- 🟡 Warning: Minor issues present
- 🔴 Action Required: Immediate attention needed

---

### Phase 0-C: Recommendation Generation

**Priority Decision Logic:**

| Priority | Conditions |
|----------|------------|
| 🔴 High | Security issues, test failures, build errors |
| 🟡 Medium | Lint warnings, coverage regression, missing documentation |
| 🟢 Low | Refactoring opportunities, optimization suggestions |

**Category-Specific Suggestion Templates:**

```yaml
# Testing
- condition: "Tests are failing"
  priority: 🔴
  suggestion: "Fix failing tests"
  agent: Radar
  reason: "Restore a passing CI/CD state"

- condition: "Coverage is below 80%"
  priority: 🟡
  suggestion: "Improve test coverage"
  agent: Radar
  reason: "Reduce regression risk"

# Security
- condition: "npm audit reports vulnerabilities"
  priority: 🔴
  suggestion: "Update vulnerable dependencies"
  agent: Sentinel
  reason: "Remove security exposure"

# Code Quality
- condition: "There are more than 10 lint warnings"
  priority: 🟡
  suggestion: "Resolve lint warnings"
  agent: Zen
  reason: "Maintain code quality"

- condition: "Unused code is detected"
  priority: 🟢
  suggestion: "Remove dead code"
  agent: Sweep
  reason: "Improve maintainability"

# Documentation
- condition: "README has not been updated for more than 30 days"
  priority: 🟢
  suggestion: "Refresh the README"
  agent: Quill
  reason: "Keep documentation current"

# Work Continuation
- condition: "There are uncommitted changes"
  priority: 🟡
  suggestion: "Continue the previous task"
  agent: "(previous agent)"
  reason: "Finish interrupted work"
```

---

## Output Format

```markdown
## Nexus Proactive Analysis

### Project Status

| Item | Status |
|------|--------|
| Latest Activity | [YYYY-MM-DD] - [Agent] - [summary] |
| Uncommitted Changes | [none / X files modified] |
| Health | test: 🟢 / security: 🟢 / code: 🟡 / doc: 🟢 |

### Recommended Actions

| # | Priority | Suggestion | Agent | Reason |
|---|----------|------------|-------|--------|
| 1 | 🔴 High | [suggestion] | [Agent] | [reason] |
| 2 | 🟡 Medium | [suggestion] | [Agent] | [reason] |
| 3 | 🟢 Low | [suggestion] | [Agent] | [reason] |

### Next Step

Select a number to run a recommended action.
To start a new task, enter `/Nexus [task]`.
```

---

## User Interaction

Options after proactive analysis:

```yaml
ON_PROACTIVE_START:
  timing: BEFORE_START
  when: "/Nexus is invoked with no arguments"
  options:
    - label: "Run recommended action #1 (Recommended)"
      description: "[highest-priority suggestion]"
    - label: "Run recommended action #2"
      description: "[next suggestion]"
    - label: "Continue previous work"
      description: "Resume the latest task from the Activity Log"
    - label: "Start a new task"
      description: "Begin a new task with `/Nexus [task]`"
```

---

## Relationship to AUTORUN

Proactive mode is positioned as the **pre-stage** to AUTORUN:

```
/Nexus (no arguments)
    ↓
Phase 0: PROACTIVE_ANALYSIS
    ↓
User Selection
    ↓
├─ Recommended action selected → Start AUTORUN_FULL
├─ Continue previous work → Start AUTORUN_FULL
└─ New task specified → Standard routing
```

Full backward compatibility with existing AUTORUN mode is preserved.

---

## Lightweight Execution Guidelines

To keep proactive analysis lightweight, follow these rules:

1. **Incremental execution**: Fetch only the information that is currently needed
2. **Use caching**: Do not re-run the same analysis within one session
3. **Timeouts**: Keep each check under 5 seconds
4. **Skip condition**: If `.agents/PROJECT.md` is missing, run only the lightweight analysis
