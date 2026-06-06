# Trail Investigation Patterns

## Pattern Catalog

### 1. Regression Hunt Pattern

The most common pattern. Used when a feature that previously worked is now broken.

```yaml
REGRESSION_HUNT:
  trigger:
    - "It was working yesterday"
    - "Tests suddenly started failing"
    - "Problems appeared after deployment"

  prerequisites:
    - Clear definition of the "broken" state
    - Reproducible test command
    - (Preferably) Information about when it last worked

  workflow:
    1. Confirm symptoms:
       - What is broken
       - How is it broken
       - Reproduction steps

    2. Identify search range:
       - Last known working state (good commit)
       - Current broken state (bad commit = HEAD)
       - Related files

    3. Execute bisect:
       - Validate test command
       - Run automated bisect
       - Verify results

    4. Analyze cause:
       - Review identified commit contents
       - Understand why it caused the issue
       - Check related changes

    5. Create report:
       - Timeline
       - Root cause
       - Recommended actions

  example_commands:
    # Basic bisect
    git bisect start
    git bisect bad HEAD
    git bisect good v1.0.0
    git bisect run npm test

    # Limit to specific file
    git log --oneline v1.0.0..HEAD -- src/auth/

    # Search for specific string
    git log -S "validateToken" --oneline
```

### 2. Code Archaeology Pattern

Answers the question "Why is this code written this way?"

```yaml
ARCHAEOLOGY:
  trigger:
    - "I don't understand this code's intent"
    - "Why is this implementation so complex?"
    - "How long has this TODO been here?"

  prerequisites:
    - Target code location (file, line)
    - Specific questions

  workflow:
    1. Surface investigation:
       - Use git blame to find last modifier
       - Check change date and commit message

    2. Deep investigation:
       - Track file history with git log --follow
       - Review related commits chronologically
       - Look for links to PRs/Issues

    3. Gather context:
       - Design decisions at the time
       - Related constraints
       - Subsequent changes

    4. Document:
       - Summarize discovered history
       - Determine if it should be recorded as tech debt
       - Note improvement suggestions if applicable

  example_commands:
    # Detailed blame
    git blame -L 100,150 src/utils.ts

    # File history (with rename tracking)
    git log --follow -p -- src/utils.ts

    # History of specific lines
    git log -L 100,150:src/utils.ts

    # Search related keywords
    git log --all --grep="workaround"
```

### 3. Impact Analysis Pattern

Analyze how much impact a specific change has had.

```yaml
IMPACT_ANALYSIS:
  trigger:
    - "What does this change affect?"
    - "What would break if we revert this commit?"
    - "What's the scope of this refactoring?"

  prerequisites:
    - Target commit or commit range
    - Purpose of analysis (revert decision, review support, etc.)

  workflow:
    1. Understand change contents:
       - List of changed files
       - Type of changes (add, modify, delete)
       - Change volume

    2. Track dependencies:
       - Code referencing changed files
       - Places using changed APIs
       - Test coverage

    3. Risk assessment:
       - Affected features
       - Potential breaking changes
       - Areas without tests

    4. Create report:
       - Impact matrix
       - Risk assessment
       - Testing recommendations

  example_commands:
    # List of changed files
    git show --stat abc1234

    # Files referencing specific file (requires static analysis)
    grep -r "import.*from.*utils" src/

    # Files frequently changed together
    git log --name-only --pretty=format: abc1234~10..abc1234 | sort | uniq -c | sort -rn
```

### 4. Ownership Analysis Pattern

Identify who is the expert on specific code.

```yaml
OWNERSHIP_ANALYSIS:
  trigger:
    - "Who should I ask about this code?"
    - "Who should review this?"
    - "I want to check knowledge concentration"

  prerequisites:
    - Target file or directory

  workflow:
    1. Identify contributors:
       - Main contributors per file
       - Recent contributors
       - Long-term contributors

    2. Analyze knowledge distribution:
       - Identify single points of failure
       - Knowledge bias
       - Onboarding needs

    3. Recommendations:
       - Code reviewer candidates
       - Knowledge sharing needs
       - Documentation priorities

  example_commands:
    # Contributor ranking for a file
    git shortlog -sn -- src/auth/

    # Recent contributors
    git log --since="3 months ago" --format="%an" -- src/auth/ | sort | uniq -c | sort -rn

    # Owner per line
    git blame --line-porcelain src/auth/index.ts | grep "^author " | sort | uniq -c | sort -rn
```

### 5. Change Frequency Analysis Pattern

Identify hotspots from change frequency.

```yaml
CHANGE_FREQUENCY:
  trigger:
    - "Which code breaks often?"
    - "I want to prioritize refactoring"
    - "I want to identify tech debt hotspots"

  prerequisites:
    - Analysis period
    - Target directory

  workflow:
    1. Measure change frequency:
       - Number of changes per file
       - Types of changes (bugfix, feature, refactor)
       - Change size

    2. Discover patterns:
       - Files frequently changed together
       - Files with many bug fixes
       - Correlation between complexity and change frequency

    3. Prioritize:
       - Refactoring candidates
       - Test enhancement candidates
       - Documentation candidates

  example_commands:
    # Change frequency ranking
    git log --since="6 months ago" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20

    # Files in bug fix commits
    git log --since="6 months ago" --grep="fix" --name-only --pretty=format: | sort | uniq -c | sort -rn

    # Change frequency for specific file
    git log --oneline --since="6 months ago" -- src/auth/index.ts | wc -l
```

---

## Pattern Selection Guide

| Situation | Recommended Pattern |
|-----------|---------------------|
| Test suddenly failing | Regression Hunt |
| Code I don't understand | Archaeology |
| Want to know revert impact | Impact Analysis |
| Looking for a reviewer | Ownership Analysis |
| Planning refactoring | Change Frequency |

---

## Anti-Patterns

### Patterns to Avoid

1. **Blind Bisect**
   - ❌ Starting bisect without validating test command
   - ✅ Always manually verify good/bad before starting

2. **Blame Game**
   - ❌ Using blame to assign personal blame
   - ✅ Focus on commits and changes

3. **Infinite Archaeology**
   - ❌ Digging through history without purpose
   - ✅ Investigate with specific questions

4. **Scope Creep**
   - ❌ Endlessly expanding investigation scope
   - ✅ End when the original question is answered

5. **History Modification**
   - ❌ Modifying history during investigation
   - ✅ Limit to read-only operations
