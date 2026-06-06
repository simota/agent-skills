# Trail Framework Templates

## SCOPE Phase Template

```yaml
INVESTIGATION_SCOPE:
  symptom: "[What's broken - test failure, behavior change, etc.]"
  known_good: "[Last known working state - commit, tag, date, or 'unknown']"
  known_bad: "[Current broken state - usually HEAD]"
  search_type:
    - REGRESSION: "Worked before, broken now"
    - ARCHAEOLOGY: "Why is the code like this?"
    - IMPACT: "What did this change affect?"
  files_of_interest:
    - "[File or directory paths]"
  test_criteria: "[How to verify good/bad state]"
```

## LOCATE Phase Commands

### For Regression (git bisect)

```bash
# Step 1: Identify good and bad commits
git log --oneline -20  # Recent history
git tag -l             # Check for version tags

# Step 2: Automated bisect (with user confirmation)
git bisect start
git bisect bad HEAD
git bisect good <known_good_commit>
git bisect run <test_command>

# Step 3: Record the result
git bisect log > bisect_log.txt
git bisect reset
```

### For Archaeology (history dive)

```bash
# Trace file evolution
git log --follow -p -- <file>

# Find when a line was introduced
git log -S "<search_string>" --oneline

# Understand a specific change
git show <commit> --stat
git show <commit> -- <file>
```

### For Impact Analysis

```bash
# What files changed together
git log --name-only --pretty=format: <commit_range> | sort | uniq -c | sort -rn

# Who touched this code
git shortlog -sn -- <file>

# Change frequency
git log --since="6 months ago" --oneline -- <file> | wc -l
```

## TRACE Phase Template (CHANGE_STORY)

```yaml
CHANGE_STORY:
  breaking_commit:
    sha: "[Full SHA]"
    short: "[Short SHA]"
    date: "[YYYY-MM-DD HH:MM]"
    author: "[Author name]"
    message: "[Commit message]"

  context_before:
    - commit: "[Previous relevant commit]"
      summary: "[What it did]"

  the_change:
    files_modified:
      - path: "[File path]"
        type: "[modified/added/deleted]"
        summary: "[What changed]"
    lines_added: N
    lines_removed: N
    intent: "[Apparent purpose of the change]"

  context_after:
    - commit: "[Following relevant commit]"
      summary: "[What it did]"

  why_it_broke:
    hypothesis: "[Why this change caused the issue]"
    evidence:
      - "[Supporting evidence 1]"
      - "[Supporting evidence 2]"
```

## REPORT Phase Template

```markdown
## Trail Investigation Report

### Summary
- **Symptom:** [What's broken]
- **Root Cause Commit:** [SHA] by [Author] on [Date]
- **Confidence:** [High/Medium/Low]

### Timeline
[Good State]
    │
    ├── abc1234 (2024-01-10) - Refactored user service
    │
    ├── def5678 (2024-01-11) - Added caching layer  ← BREAKING COMMIT
    │
    ├── ghi9012 (2024-01-12) - Updated tests
    │
[Bad State - Current]

### The Breaking Change
**Commit:** def5678
**Message:** Added caching layer for improved performance
**Author:** developer@example.com

**What Changed:**
- Modified `src/services/user.ts` (+45, -12)
- Added `src/cache/redis.ts` (new file)

**Why It Broke:**
The caching layer introduced a race condition where...

### Evidence
1. Test `user.spec.ts:42` passes on abc1234, fails on def5678
2. The change modified the return type of `getUser()` from...
3. No tests covered the edge case where...

### Recommendations
1. **Quick Fix:** [Immediate mitigation]
2. **Proper Fix:** [Root cause resolution]
3. **Prevention:** [How to avoid in future]
```

## RECOMMEND Phase Table

| Finding Type | Recommendation | Handoff To |
|--------------|----------------|------------|
| Clear regression | Revert or fix PR | Guardian → Builder |
| Design flaw | Architecture review | Atlas |
| Missing test | Add test coverage | Radar |
| Security issue | Immediate patch | Sentinel → Builder |

## Bisect Automation Script

```bash
#!/bin/bash
# trail_bisect.sh - Automated bisect runner

# Configuration (filled by Trail)
GOOD_COMMIT="$1"
BAD_COMMIT="$2"
TEST_COMMAND="$3"

# Safety checks
if [ -z "$GOOD_COMMIT" ] || [ -z "$BAD_COMMIT" ] || [ -z "$TEST_COMMAND" ]; then
    echo "Usage: trail_bisect.sh <good_commit> <bad_commit> <test_command>"
    exit 1
fi

# Verify commits exist
git rev-parse "$GOOD_COMMIT" > /dev/null 2>&1 || { echo "Good commit not found"; exit 1; }
git rev-parse "$BAD_COMMIT" > /dev/null 2>&1 || { echo "Bad commit not found"; exit 1; }

# Start bisect
echo "Starting bisect..."
echo "Good: $GOOD_COMMIT"
echo "Bad: $BAD_COMMIT"
echo "Test: $TEST_COMMAND"

git bisect start
git bisect bad "$BAD_COMMIT"
git bisect good "$GOOD_COMMIT"

# Run automated bisect
git bisect run sh -c "$TEST_COMMAND"

# Capture result
RESULT_COMMIT=$(git bisect view --oneline | head -1)
echo ""
echo "=== BISECT RESULT ==="
echo "First bad commit: $RESULT_COMMIT"
git show --stat $(echo $RESULT_COMMIT | cut -d' ' -f1)

# Clean up
git bisect reset
echo "Bisect complete. Working directory restored."
```

## Bisect Edge Cases

```yaml
BISECT_EDGE_CASES:
  flaky_test:
    detection: "Same commit gives different results"
    solution: "Run test 3 times, majority wins"
    script: |
      for i in 1 2 3; do
        $TEST_COMMAND && good=$((good+1)) || bad=$((bad+1))
      done
      [ $good -gt $bad ] && exit 0 || exit 1

  build_failure:
    detection: "Build fails on some commits"
    solution: "Skip unbuildable commits"
    command: "git bisect skip"

  large_range:
    detection: ">1000 commits to search"
    solution: "Use heuristics to narrow first"
    approach:
      - Check recent release tags first
      - Use git log -S to find relevant commits
      - Narrow to specific file changes

  merge_commits:
    detection: "Bisect lands on merge commit"
    solution: "Investigate both parents"
    command: "git log --first-parent"
```
