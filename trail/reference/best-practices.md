# Trail Best Practices

## Investigation Principles

### 1. Start with the Question

Define a clear question before starting the investigation.

```yaml
GOOD_QUESTIONS:
  - "When did this test start failing?"
  - "Why did this function start throwing exceptions?"
  - "What was the purpose of adding this complex conditional?"

BAD_QUESTIONS:
  - "Look into what's happening" (too broad)
  - "Show me all the history" (no purpose)
  - "Who broke this" (blame-focused)
```

### 2. Narrow Before Deep Dive

Before investigating the entire history, narrow down the scope first.

```bash
# Bad example: Immediately bisect entire history
git bisect start
git bisect bad HEAD
git bisect good $(git rev-list --max-parents=0 HEAD)  # First commit

# Good example: First identify the range
# 1. Check recent release tags
git tag -l --sort=-creatordate | head -5

# 2. Identify related files from symptoms
git log --oneline -S "errorMessage" --since="1 month ago"

# 3. Bisect within narrowed range
git bisect start
git bisect bad HEAD
# ...
```

### 3. Verify Before Automate

Before automated bisect, manually verify the good/bad states.

```bash
# 1. Verify good commit
git checkout v2.0.0
npm test  # Does it really pass?

# 2. Verify bad commit
git checkout HEAD
npm test  # Does it really fail?

# 3. Verify test command
# Confirm exit code 0 = good, non-0 = bad
npm test; echo "Exit code: $?"

# 4. Once verified, start bisect
git checkout -
git bisect start
```

### 4. Document as You Go

Record discoveries during the investigation.

```markdown
## Investigation Log: Auth Error

### 2024-01-20 10:00 - Started
- Symptom: Login failure
- Hypothesis: Token validation logic change

### 10:15 - Initial Investigation
- v2.3.0 confirmed working
- HEAD confirmed failing
- 47 commits to investigate

### 10:30 - Bisect Execution
- Completed in 6 steps
- Identified def5678

...
```

---

## Bisect Best Practices

### Test Command Design

Conditions for a good test command:
- Deterministic (same input gives same result)
- Fast (runs at each step)
- Clear exit codes

```bash
# Good example: Run only specific tests
npm test -- --grep "login functionality"

# Good example: Specific file only
pytest tests/test_auth.py::test_login

# Bad example: Run all tests (slow)
npm test

# Bad example: Flaky test
npm test -- --grep "flaky integration test"
```

### Handling Special Cases

#### Flaky Tests

```bash
# Run multiple times and use majority vote
git bisect run bash -c '
  PASS=0
  for i in 1 2 3 4 5; do
    npm test -- --grep "sometimes fails" && PASS=$((PASS+1))
  done
  [ $PASS -ge 3 ]  # Good if passes 3+ out of 5
'
```

#### Build Errors

```bash
# Skip on build failure (exit 125)
git bisect run bash -c '
  npm run build 2>/dev/null || exit 125
  npm test
'
```

#### Dependency Changes

```bash
# Reinstall dependencies
git bisect run bash -c '
  npm ci || exit 125
  npm test
'
```

### Recovery from Bad Bisect

When bisect goes wrong:

```bash
# 1. Check current state
git bisect log

# 2. Reset
git bisect reset

# 3. Start over
# Or resume from log
git bisect replay bisect_log.txt
```

---

## Archaeology Best Practices

### Follow the Breadcrumbs

From one discovery, find the next clue.

```bash
# Step 1: Find last modifier with blame
git blame -L 100,110 src/auth.ts
# → abc1234 looks suspicious

# Step 2: Check that commit's details
git show abc1234
# → Message says "Fix for issue #123"

# Step 3: Look for related PR/Issue
# (Search #123 on GitHub/GitLab)

# Step 4: Check files changed together in that PR
git log --name-only abc1234^..abc1234

# Step 5: Understand context from surrounding commits
# ...
```

### Understand the "Why"

Understand the reason for code changes.

```yaml
INFORMATION_SOURCES:
  1. Commit messages:
     - Check first
     - Pay attention to keywords like "Fix", "Workaround", "Temporary"

  2. PR descriptions:
     - Often contain more detailed background
     - Review comments are also important

  3. Issues/tickets:
     - Details of the original problem
     - Discussion history

  4. Related documentation:
     - ADRs (Architecture Decision Records)
# ...
```

### Time-box Your Investigation

Set time limits for investigations.

```yaml
TIME_BOXING:
  quick_check: 15 minutes
    scope: "Check commit messages and blame"
    deliverable: "Basic understanding of history"

  standard: 1 hour
    scope: "PR/Issue investigation, related commits"
    deliverable: "Detailed history report"

  deep_dive: half day
    scope: "Multiple files, long-term tracking"
    deliverable: "Comprehensive architecture evolution"

  when_to_stop:
    - Question has been answered
# ...
```

---

## Reporting Best Practices

### Structure Your Findings

Report discoveries in a structured format.

```markdown
## Investigation Report Template

### Executive Summary
- Conclusion in 1-2 sentences

### Question and Answer
- Q: [Original question]
- A: [Concise answer]

### Timeline
- Visually show chronology

### Details
- Evidence for findings
- Related commits
...
```

### Visual Timeline

Make timelines visual.

```
Good State ─────────────────────────────────── Bad State
    │                                           │
    │   ┌─ abc1234: Add feature                 │
    │   │                                       │
    │   ├─ def5678: Refactoring ← ROOT CAUSE    │
    │   │                                       │
    │   └─ ghi9012: Bug fix                     │
    │                                           │
    ▼                                           ▼
  v2.0.0                                      HEAD
```

### Confidence Levels

Be explicit about confidence levels.

```yaml
CONFIDENCE_LEVELS:
  high:
    description: "This commit is definitely the cause"
    criteria:
      - Identified by bisect
      - Manually verified reproduction
      - Change content matches symptom

  medium:
    description: "This commit is probably related"
    criteria:
      - Timing matches
      - Change content is related
      - Full verification not done

# ...
```

---

## Anti-Patterns to Avoid

### 1. Blame Game

```yaml
BAD:
  - "Alice introduced this bug"
  - "Who wrote this code?"
  - "Identify the responsible person"

GOOD:
  - "The change was introduced in commit abc1234"
  - "This was refactored in this PR"
  - "Understand the background of the change"
```

### 2. Scope Creep

```yaml
BAD:
  - Trying to solve all problems in one investigation
  - Following all related history
  - "While we're at it" investigating other issues

GOOD:
  - Focus on one clear question
  - Investigate within necessary scope
  - Record additional issues as separate tasks
```

### 3. History Modification

```yaml
NEVER_DO:
  - Creating commits during bisect
  - Rebasing during investigation
  - Amending for "fixes"

ALWAYS_DO:
  - Limit to read-only operations
  - Make changes after investigation completes
  - Work on separate branches
```

### 4. Ignoring Context

```yaml
BAD:
  - Not reading commit messages
  - Not checking PR descriptions
  - Not considering circumstances at the time

GOOD:
  - Always read commit messages
  - Check PR/Issue when possible
  - Consider constraints and requirements at the time
```

---

## Efficiency Tips

### 1. Use Aliases

```bash
# Add to .gitconfig
[alias]
  # Readable log
  lg = log --oneline --graph --decorate

  # File history
  hist = log --follow --oneline --

  # Contributor ranking
  contributors = shortlog -sn

  # Today's changes
  today = log --since=midnight --oneline
```

### 2. Cache Results

```bash
# Save bisect log
git bisect log > bisect_$(date +%Y%m%d_%H%M).log

# Record investigation results in Markdown
# Add to .agents/trail.md
```

### 3. Parallel Investigation

Work in parallel with multiple terminals:
- Terminal 1: Run bisect
- Terminal 2: Investigate related commits
- Terminal 3: Write documentation
