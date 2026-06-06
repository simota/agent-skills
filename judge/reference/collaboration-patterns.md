# Collaboration Patterns

Detailed collaboration flows and agent integration patterns for Judge.

---

## Pattern A: Full PR Review Flow

```
Builder creates PR
       ↓
┌─────────────────────────────────────────────┐
│ Judge reviews with codex review --base main │
│ Generates: Review Report + Findings         │
└──────────────────┬──────────────────────────┘
                   ↓
          [CRITICAL/HIGH found?]
                   │
        ┌─────────┴─────────┐
        ↓ Yes               ↓ No
┌───────────────┐   ┌────────────────┐
│ JUDGE_TO_     │   │ Verdict:       │
│ BUILDER_      │   │ APPROVE        │
│ HANDOFF       │   └────────────────┘
└───────┬───────┘
        ↓
  Builder fixes
        ↓
  Judge re-reviews
```

---

## Pattern B: Security Escalation

```
Judge detects potential vulnerability
                   ↓
┌─────────────────────────────────────────────┐
│ Trigger: ON_SECURITY_FINDING                │
│ User chooses: "Detailed audit with Sentinel"│
└──────────────────┬──────────────────────────┘
                   ↓
         JUDGE_TO_SENTINEL_HANDOFF
                   ↓
┌─────────────────────────────────────────────┐
│ Sentinel deep security analysis             │
│ - Exploit scenario assessment               │
│ - OWASP classification                      │
│ - Remediation guidance                      │
└──────────────────┬──────────────────────────┘
                   ↓
         SENTINEL_TO_JUDGE_HANDOFF
                   ↓
  Judge incorporates in final report
```

---

## Pattern C: Quality Improvement

```
Judge finds non-blocking quality issues
                   ↓
┌─────────────────────────────────────────────┐
│ Observations (INFO level):                  │
│ - Complex function (could split)            │
│ - Naming inconsistency                      │
│ - Code duplication                          │
└──────────────────┬──────────────────────────┘
                   ↓
         JUDGE_TO_ZEN_HANDOFF
                   ↓
┌─────────────────────────────────────────────┐
│ Zen refactors (non-blocking)                │
│ - Improves readability                      │
│ - Extracts functions                        │
│ - Applies naming conventions                │
└─────────────────────────────────────────────┘
```

---

## Pattern D: Test Coverage Gap

```
Judge identifies untested scenarios
                   ↓
┌─────────────────────────────────────────────┐
│ Findings with missing test coverage:        │
│ - Edge case not tested                      │
│ - Error path not covered                    │
│ - New feature without tests                 │
└──────────────────┬──────────────────────────┘
                   ↓
         JUDGE_TO_RADAR_HANDOFF
                   ↓
  Radar adds regression/edge case tests
```

---

## Pattern E: Pre-Investigation

```
Scout completes bug investigation
                   ↓
         SCOUT_TO_JUDGE_HANDOFF
                   ↓
┌─────────────────────────────────────────────┐
│ Judge verifies fix addresses root cause     │
│ - Reviews proposed fix                      │
│ - Checks edge cases covered                 │
│ - Validates no regression introduced        │
└─────────────────────────────────────────────┘
```

---

## Pattern F: Build-Review Cycle

```
Builder implements feature/fix
                   ↓
         BUILDER_TO_JUDGE_HANDOFF
                   ↓
┌─────────────────────────────────────────────┐
│ Judge reviews implementation                │
│ - Correctness check                         │
│ - Security review                           │
│ - Intent alignment                          │
└──────────────────┬──────────────────────────┘
                   ↓
          [Issues found?]
                   │
        ┌─────────┴─────────┐
        ↓ Yes               ↓ No
  JUDGE_TO_BUILDER     Verdict: APPROVE
  (iterate)
```

---

## Agent Integration Details

### Scout Integration (Pre-Review)

When complex bugs are suspected, Scout investigates first:

```markdown
## Scout → Judge Handoff

**Bug Report**: [Issue description]
**Root Cause**: [Scout's findings]
**Affected Code**: [File locations]

**Request**: Judge to verify fix addresses root cause
```

### Builder Integration (Post-Review)

After Judge finds issues, hand off to Builder for fixes:

```markdown
## Judge → Builder Fix Request

**Findings**: [List of issues from Judge report]
**Priority**: CRITICAL findings first

**Files to Fix**:
| File | Finding | Priority |
|------|---------|----------|
| `src/api/user.ts:42` | CRITICAL-001 | Fix immediately |
| `src/utils/validate.ts:15` | HIGH-001 | Fix before merge |

**Acceptance Criteria**:
- All CRITICAL findings resolved
- HIGH findings addressed or documented
- Re-review by Judge after fixes
```

### Sentinel Integration (Security Findings)

```markdown
## Judge → Sentinel Security Review

**Potential Vulnerability**: [Finding from Judge]
**Location**: [File and line]
**Risk Level**: [Judge's assessment]

**Request**: Deep security analysis and remediation guidance
```

### Zen Integration (Quality Suggestions)

```markdown
## Judge → Zen Handoff

**Observations** (not bugs, but improvements):
- [Code smell or readability issue]
- [Complexity concern]
- [Naming suggestion]

**Note**: These are non-blocking suggestions for code quality improvement.
```

### Radar Integration (Test Coverage)

```markdown
## Judge → Radar Test Request

**Findings Without Tests**:
| Finding | Type | Test Needed |
|---------|------|-------------|
| CRITICAL-001 | Bug fix | Regression test |
| HIGH-002 | Edge case | Edge case test |

**Request**: Ensure test coverage for identified issues
```
