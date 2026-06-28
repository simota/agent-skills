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

Assess project health across four indicators. **Evidence-grounded — never assert a status you did not probe.** Each indicator's color MUST come from an actual cheap check (run it within the 5s timeout) or be reported as ⚪ `unknown (not probed)`. Fabricating a 🟢 you didn't verify is forbidden (repo rule: don't fabricate, measure don't guess).

| Indicator | Probe command (run it — don't guess) | Status |
|-----------|--------------------------------------|--------|
| `test_health` | the repo's test runner (e.g. `npm test`, `pytest -q`) — or its last CI result if a run is too slow for the 5s budget | 🟢/🟡/🔴/⚪ |
| `security_health` | `npm audit --json` / `pip-audit` / lockfile advisory scan | 🟢/🟡/🔴/⚪ |
| `code_health` | the repo's lint/typecheck (e.g. `eslint`, `tsc --noEmit`, `ruff`) | 🟢/🟡/🔴/⚪ |
| `doc_health` | README mtime vs last code commit; obvious doc gaps | 🟢/🟡/🔴/⚪ |

**Assessment Criteria:**
- 🟢 Healthy: check ran, no issues detected
- 🟡 Warning: check ran, minor issues present
- 🔴 Action Required: check ran, immediate attention needed
- ⚪ Unknown: not probed (check too slow / tool absent / no test suite) — **say so explicitly**, do not infer green from silence

A recommendation may only cite an indicator that was actually probed. An ⚪ indicator yields a "verify X" recommendation (run the check), not a fix for an unconfirmed problem.

---

### Phase 0-C: Recommendation Generation

**Priority Decision Logic:**

| Priority | Conditions |
|----------|------------|
| 🔴 High | Security issues, test failures, build errors |
| 🟡 Medium | Lint warnings, coverage regression, missing documentation |
| 🟢 Low | Refactoring opportunities, optimization suggestions |

**Recommendations route to Recipes, not bare agents.** Each recommendation carries the **Recipe** that will run it, so the selected action executes the curated phase contract (and its VERIFY→SHIP discipline) rather than a one-shot agent call: failing tests / build errors → `bug`; vulnerabilities → `security`; slow paths → `optimize`; lint/dead-code/smells → `refactor`; missing capability → `feature`; multi-axis polish → `kaizen`; docs → Quill direct. The named agent is the Recipe's lead, not the whole chain.

**Grounding + dedup rules (apply before surfacing any recommendation):**
- **Verify it still exists.** Before recommending work on a file / flag / TODO, confirm it is still present in the current tree — git log and stale notes can name things already removed. Don't recommend fixing what isn't there.
- **Dedup against in-flight work.** Exclude anything already underway: uncommitted changes, an open PR, or a branch for that work → recommend *continuing* it, not starting a duplicate.
- **No busywork on a healthy project.** If all probed indicators are 🟢 and nothing is in-flight, say so plainly — surface at most 1-2 *forward-looking* opportunities (clearly marked optional) or recommend nothing. Do not manufacture low-value tasks to fill the table; "nothing urgent" is a valid, honest result.
- **Confidence honesty.** An ⚪ unknown indicator yields a "run the check to confirm" recommendation, never a fix for an unverified problem.

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

### Phase 0-D: North Star Alignment

Phases 0-A–0-C are **reactive** — they surface what's broken or stale. Phase 0-D is **proactive**: read the project's North Star and propose one workstream that advances it, the way a teammate who knows the mission would. [Source: claude.com/blog/building-effective-human-agent-teams — "establish a north star", and the example of an agent proactively recommending onboarding-copy fixes that measurably improved onboarding.]

**1. Locate the North Star (first hit wins, else skip this phase):**
- `docs/CHARTER.md` §1 Mission & Objectives
- `.agents/PROJECT.md` mission / goal section
- `docs/specs/*` locked goals, or a `README` stated goal
- If none exists → **emit no 0-D recommendation**; optionally note "No North Star found — `/nexus charter` or `/nexus goal` would establish one" (at most once, non-pushy).

**2. Propose at most ONE North-Star-aligned workstream.** It must:
- name the North Star clause it advances (cite the source line) — no citation, no proposal;
- be **forward-looking** (a new capability/improvement that moves the goal), distinct from the reactive 0-C fixes;
- be grounded in the current tree (an actual gap/opportunity you can point to), not aspirational filler;
- route to a Recipe (`feature`/`kaizen`/`delve`/`spec`), clearly marked **🧭 North Star** and **optional**.

**Restraint:** this phase is the legitimate use of the "at most 1-2 forward-looking opportunities" allowance in Phase 0-C — it does **not** add busywork on a healthy project; it replaces vague "optional ideas" with one mission-grounded one. If reactive 🔴/🟡 items exist, rank those first; the 🧭 item is always lowest urgency. Skip silently when no North Star is found or no honest opportunity exists.

```markdown
## Nexus Proactive Analysis

### Project Status

| Item | Status |
|------|--------|
| Latest Activity | [YYYY-MM-DD] - [Agent] - [summary] |
| Uncommitted Changes | [none / X files modified] |
| Health | test: 🟢 / security: 🟢 / code: 🟡 / doc: 🟢 |

### Recommended Actions

| # | Priority | Suggestion | Recipe | Evidence | Reason |
|---|----------|------------|--------|----------|--------|
| 1 | 🔴 High | [suggestion] | [`bug`/`security`/…] | [probe result that grounds it] | [reason] |
| 2 | 🟡 Medium | [suggestion] | [Recipe] | [evidence] | [reason] |
| 3 | 🟢 Low | [suggestion] | [Recipe] | [evidence] | [reason] |
| 4 | 🧭 North Star | [forward-looking workstream] | [`feature`/`kaizen`/…] | [North Star clause cited (Phase 0-D)] | [how it advances the mission] |

*(The 🧭 North Star row appears only when Phase 0-D found a mission and an honest opportunity; omit it otherwise. If the project is healthy with nothing in-flight and no North Star item: state "Nothing urgent — all probed indicators 🟢".)*

### Next Step

Select a number to run a recommended action (it runs through its Recipe's phase contract).
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
