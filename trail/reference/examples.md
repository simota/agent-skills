# Trail Usage Examples

## Example 1: Basic Regression Investigation

### Scenario
Login functionality suddenly stopped working. It was working as of last week's release v2.3.0.

### Investigation Process

**Step 1: Confirm Symptoms**
```
User: I can't log in anymore. The error is "Invalid token format"
```

**Step 2: Trail's Response**
```markdown
## Starting Investigation

### Symptoms
- Error: "Invalid token format"
- Location: Login process
- Last known working: v2.3.0

### Identifying Search Range
- Good: v2.3.0 (abc1234)
- Bad: HEAD (xyz9999)
- Commits: 47

### Pre-bisect Confirmation

Let me confirm the test command. Is this correct?

```bash
npm test -- --grep "login"
```

[Yes, start] [Adjust test] [Manual bisect]
```

**Step 3: Execute Bisect**
```bash
# Executed by Trail
git bisect start
git bisect bad HEAD
git bisect good v2.3.0
git bisect run npm test -- --grep "login"

# Result
Bisecting: 0 revisions left to test after this
def5678 is the first bad commit
```

**Step 4: Results Report**
```markdown
## 🔄 Investigation Complete

### Summary
| Item | Value |
|------|-------|
| Root Cause | def5678 |
| Author | developer@example.com |
| Date | 2024-01-15 |
| Confidence | High (100%) |

### Timeline

```
✓ v2.3.0 (abc1234) - 2024-01-10
│
├── 111aaaa - Update dependencies
├── 222bbbb - Add new feature
├── def5678 - Refactor token handling ← ROOT CAUSE
├── 333cccc - Fix typo
│
✗ HEAD (xyz9999) - 2024-01-20
```

### Breaking Commit Details

```
commit def5678
Author: developer@example.com
Date: 2024-01-15

Refactor token handling for better performance

- Simplified token parsing
- Removed base64 fallback decoding
```

### Why It Broke

This commit removed `base64 fallback decoding`.
Users with tokens in the old format (base64 encoded)
cannot be processed by the new parser.

### Recommended Actions

1. **Immediate:** Restore base64 fallback
2. **Short-term:** Migrate existing tokens to new format
3. **Prevention:** Add tests for token format changes
```

---

## Example 2: Code Archaeology

### Scenario
There's a strange conditional in the code. I want to understand why it's written this way.

### Target Code
```typescript
// src/services/payment.ts:142
if (amount > 0 && amount < 10000 && !isWeekend && user.country !== 'JP') {
  // Why all these conditions?
  applyDiscount(0.1);
}
```

### Investigation Process

**Step 1: Check Last Change with Blame**
```bash
git blame -L 142,145 src/services/payment.ts
```

Result:
```
abc1234 (Alice 2023-06-15) if (amount > 0 && amount < 10000 && !isWeekend && user.country !== 'JP') {
abc1234 (Alice 2023-06-15)   // Why all these conditions?
abc1234 (Alice 2023-06-15)   applyDiscount(0.1);
abc1234 (Alice 2023-06-15) }
```

**Step 2: Check Commit Details**
```bash
git show abc1234
```

**Step 3: Track History of Each Condition**
```bash
git log -S "isWeekend" --oneline -- src/services/payment.ts
git log -S "country !== 'JP'" --oneline -- src/services/payment.ts
```

**Step 4: Investigation Report**
```markdown
## 🔍 Code Archaeology Report: payment.ts:142

### Target Code
```typescript
if (amount > 0 && amount < 10000 && !isWeekend && user.country !== 'JP') {
```

### Condition History

| Condition | Added | Commit | Reason |
|-----------|-------|--------|--------|
| `amount > 0` | 2022-01-10 | 111aaa | Initial implementation |
| `amount < 10000` | 2022-03-15 | 222bbb | PR#45: High-value order discount limit |
| `!isWeekend` | 2022-08-20 | 333ccc | Issue#78: Exclude weekend sales |
| `country !== 'JP'` | 2023-06-15 | abc1234 | Legal request: Japan fair trade compliance |

### Condition Details

#### 1. `amount > 0`
- **Added:** Initial implementation (2022-01-10)
- **Reason:** Orders of 0 or less are not eligible for discount (obviously)

#### 2. `amount < 10000`
- **Added:** 2022-03-15
- **Commit:** 222bbb
- **PR Link:** #45
- **Reason:**
  > High-value items (over 10,000) already have low margins,
  > so they're excluded from additional discounts. Marketing department request.

#### 3. `!isWeekend`
- **Added:** 2022-08-20
- **Commit:** 333ccc
- **Issue Link:** #78
- **Reason:**
  > Different promotions run on weekends,
  > to prevent double application. Accounting department's note.

#### 4. `country !== 'JP'`
- **Added:** 2023-06-15
- **Commit:** abc1234
- **Reason:**
  > Japan has restrictions on certain discount displays
  > under fair trade laws. Urgent request from legal department.
  > Details in internal Wiki: compliance/JP-discount-rules

### Recommendations

1. **Documentation:** Add code comments explaining these conditions
2. **Refactoring:** Extract conditions into named functions to clarify intent
   ```typescript
   function isEligibleForStandardDiscount(order: Order): boolean {
     return isValidAmount(order.amount)
       && !isWeekendPromotion()
       && !requiresJapanCompliance(order.user);
   }
   ```
3. **Testing:** Add tests for each condition's edge cases

### Related Documents
- PR#45: High-value order discount limit
- Issue#78: Weekend sale exclusion
- Internal Wiki: compliance/JP-discount-rules
```

---

## Example 3: Impact Analysis

### Scenario
I want to do a major refactoring of the `User` model. I need to know the impact scope.

### Investigation Process

**Step 1: Check Change Frequency of Target File**
```bash
git log --oneline --since="6 months ago" -- src/models/User.ts | wc -l
# Result: 23 changes
```

**Step 2: Identify Files Changed Together**
```bash
git log --name-only --pretty=format: --since="6 months ago" -- src/models/User.ts | sort | uniq -c | sort -rn | head -10
```

**Step 3: Impact Report**
```markdown
## 📊 Impact Analysis: User.ts Refactoring

### Analysis Target
- File: `src/models/User.ts`
- Period: Past 6 months
- Change Count: 23

### Frequently Co-Changed Files

| File | Co-change Count | Relationship |
|------|-----------------|--------------|
| src/services/auth.ts | 18 | Authentication logic |
| src/api/users.ts | 15 | API endpoints |
| src/models/User.test.ts | 14 | Unit tests |
| src/types/user.d.ts | 12 | Type definitions |
| src/utils/validation.ts | 8 | Validation |

### Dependency Map

```
User.ts
├── Direct References (12 files)
│   ├── services/auth.ts
│   ├── services/profile.ts
│   ├── api/users.ts
│   ├── api/admin.ts
│   └── ... (8 more)
│
├── Type Dependencies (5 files)
│   ├── types/user.d.ts
│   ├── types/api.d.ts
│   └── ...
│
└── Tests (3 files)
    ├── models/User.test.ts
    ├── services/auth.test.ts
    └── api/users.test.ts
```

### Risk Assessment

| Risk Item | Level | Description |
|-----------|-------|-------------|
| Auth Impact | 🔴 High | Auth service strongly depends on this |
| API Compatibility | 🟡 Medium | Public API changes may be needed |
| Test Coverage | 🟢 Low | Existing tests are comprehensive |

### Recommended Test Items

After refactoring, focus testing on:

1. **Entire Auth Flow**
   - Login/logout
   - Token refresh
   - Permission checks

2. **User API**
   - CRUD operations
   - Validation errors
   - Edge cases (deleted users, etc.)

3. **E2E Tests**
   - User registration flow
   - Profile updates

### Refactoring Strategy Suggestions

1. **Gradual Approach (Recommended)**
   - Run old and new models in parallel
   - Migrate feature by feature
   - Easy rollback

2. **Big Bang Approach**
   - Update all dependencies at once
   - Higher risk but simpler
   - Requires sufficient test coverage
```

---

## Example 4: Finding the Right Person to Ask

### Scenario
I want someone to review the payment processing code. I want to know who is most familiar with it.

### Investigation Result
```markdown
## 👥 Code Ownership Analysis: src/payment/

### Contributor Ranking (Past Year)

| Rank | Developer | Commits | Primary Contribution |
|------|-----------|---------|---------------------|
| 1 | alice@example.com | 45 | Payment logic overall |
| 2 | bob@example.com | 28 | Stripe integration |
| 3 | charlie@example.com | 15 | Error handling |

### Expert by File

| File | Primary Contributor | Last Update |
|------|---------------------|-------------|
| processor.ts | Alice (80%) | 3 days ago |
| stripe.ts | Bob (95%) | 1 week ago |
| errors.ts | Charlie (70%) | 2 weeks ago |
| refund.ts | Alice (60%), Bob (30%) | 1 month ago |

### Recommended Reviewers

1. **Alice** - Expert in payment logic overall. First choice.
2. **Bob** - Required if there are Stripe-related changes.
3. **Charlie** - Request participation if error handling changes.

### Knowledge Risk

⚠️ **Single Point of Failure Warning**

`stripe.ts` is 95% written by Bob.
If Bob is unavailable, there are limited people
who can handle changes in this area.

**Recommendations:**
- Conduct knowledge sharing sessions
- Knowledge transfer through pair programming
- Strengthen documentation
```

---

## Quick Reference: Common Commands

```bash
# Regression investigation
git bisect start && git bisect bad HEAD && git bisect good <tag>
git bisect run <test_command>
git bisect reset

# Archaeology
git blame -L <start>,<end> <file>
git log --follow -p -- <file>
git log -S "<string>" --oneline

# Impact analysis
git log --name-only --pretty=format: <range> | sort | uniq -c | sort -rn
git log --stat <commit>

# Ownership
git shortlog -sn -- <path>
git log --since="1 year ago" --format="%an" -- <path> | sort | uniq -c | sort -rn
```
