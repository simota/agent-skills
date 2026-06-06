# Error Message Guide

エラーメッセージ構造（何/なぜ/次に何を）、重要度別テンプレートのリファレンス。

---

## Error Message Structure

### The Three-Part Framework

```
1. WHAT happened (state the problem clearly)
2. WHY it happened (brief explanation, if helpful)
3. WHAT TO DO next (actionable resolution)

Example:
  WHAT: "Your payment couldn't be processed."
  WHY:  "The card on file has expired."
  NEXT: "Update your payment method to continue."
```

### Writing Rules

| Rule | Good | Bad |
|------|------|-----|
| **Be specific** | "File must be under 10 MB" | "File too large" |
| **Be human** | "We couldn't find that page" | "404 Error" |
| **Blame the system** | "We couldn't save your changes" | "You entered invalid data" |
| **Offer a path forward** | "Try again or contact support" | "An error occurred" |
| **Avoid jargon** | "Something went wrong on our end" | "Internal server error" |
| **Use active voice** | "We couldn't send your message" | "Message could not be sent" |

---

## Severity-Based Templates

### Critical Errors (Data loss, account issues)

```markdown
## Template
[Specific problem statement.]
[Brief cause if it helps the user.]
[Specific recovery action + alternative.]

## Examples
"Your account has been locked after too many login attempts.
Reset your password to regain access, or contact support
if you need help."

"We couldn't save your document due to a connection issue.
Your latest changes are stored locally and will sync
when you're back online."
```

### Validation Errors (Form input)

```markdown
## Template
[What's wrong with the input — be specific.]

## Rules
- Show inline, next to the field
- Use red/error color indicator
- Be specific about the requirement
- Show the requirement, not just the violation

## Examples
✅ "Password must be at least 8 characters"
❌ "Invalid password"

✅ "Enter a valid email (e.g., name@company.com)"
❌ "Invalid email format"

✅ "Username can only contain letters, numbers, and hyphens"
❌ "Special characters not allowed"
```

### System Errors (Server issues, timeouts)

```markdown
## Template
"Something went wrong [optional: specific area].
[Recovery action]. If this keeps happening, [escalation path]."

## Examples
"Something went wrong loading your dashboard.
Refresh the page to try again. If this keeps happening,
check our status page or contact support."

"We're having trouble connecting to the server.
Check your internet connection and try again."
```

### Permission Errors

```markdown
## Template
"You don't have access to [specific resource].
[How to get access]."

## Examples
"You don't have permission to edit this project.
Ask the project owner to grant you editor access."

"This feature is available on the Pro plan.
Upgrade your plan to unlock it."
```

### Not Found Errors

```markdown
## Template
"We couldn't find [what they were looking for].
[Suggestions or alternatives]."

## Examples
"We couldn't find a page at this address.
Check the URL or go back to the homepage."

"No results for 'acme widget'.
Try different keywords or browse categories."
```

---

## Error Message Patterns

### Inline Validation

```
Timing:
  - Validate on blur (when leaving field), not on every keystroke
  - Show success state only after previously showing error
  - Clear error as soon as input becomes valid

Position:
  - Below the field, left-aligned
  - Use aria-describedby for accessibility
  - Red color + icon for error, green + icon for success
```

### Toast/Snackbar Errors

```
Use for:
  - Background operation failures (save, sync, send)
  - Non-critical errors that don't block workflow

Duration:
  - Auto-dismiss after 5-8 seconds
  - Allow manual dismiss
  - Persist if action is needed

Content:
  - One line: "[What failed]. [Action link]"
  - Example: "Couldn't save changes. Try again"
```

### Full-Page Errors

```
Use for:
  - Page load failures
  - Authentication/authorization errors
  - Critical system outages

Include:
  - Illustration (friendly, not dramatic)
  - Clear message (no error codes unless technical audience)
  - Primary action (retry, go home, contact support)
  - Secondary action (status page, help docs)
```

---

## Error Message Checklist

```markdown
- [ ] States the problem clearly (no jargon)
- [ ] Uses active voice, human language
- [ ] Doesn't blame the user
- [ ] Includes a specific recovery action
- [ ] Provides alternative if primary action might fail
- [ ] Appropriate severity and display pattern
- [ ] Accessible (aria roles, color not sole indicator)
- [ ] Tested with real users for clarity
```

---

## Error Recovery Patterns

### Progressive Error Disclosure

段階的情報提示により、コグニティブロードを30-40%削減する。

```markdown
## Disclosure Levels

Level 1 — Summary (always visible)
"Couldn't save your changes."

Level 2 — Cause (expandable / on hover)
"Your session has expired."

Level 3 — Resolution (on request)
"Sign in again to continue. Your draft is saved locally."

## When to Use Each Level
- Level 1: Always. Every error shows a summary.
- Level 2: Show automatically for non-obvious causes.
  Hide for obvious ones (e.g., "No internet connection").
- Level 3: Show only when the recovery step is non-trivial.
  Simple actions ("Try again") don't need a third level.

## Implementation Notes
- Use aria-expanded for collapsible detail sections
- Default to collapsed on mobile (thumb-friendly)
- Never hide Level 1 — it must always be visible
```

### Undo/Redo UX Copy

破壊的操作の確認パターン。`OK/キャンセル` を禁止し、アクション名を明記する。

```markdown
## Destructive Action Modal

Title:   "Delete [item name]?"
Body:    "This will permanently remove [item]. You can't undo this."
Confirm: "Delete [item name]"   ← specific, not "OK"
Cancel:  "Keep [item name]"     ← specific, not "Cancel"

## Rules
1. Confirm button names the destructive action explicitly
2. Cancel button names what is preserved
3. Never use "OK / Cancel" for destructive actions
4. Red color for confirm; default/outline for cancel
5. Cancel is the keyboard default (focus on safe action)

## Tone
- No passive voice: "Are you sure?" → DELETE → DONE
- No hedging: "This action cannot be undone" is sufficient
- No guilt-tripping: "Delete forever" ≠ "No, keep my data"
```

### Soft Delete Pattern

削除後に取り消し手段を提供する。モーダル確認の代替として使用する。

```markdown
## Toast Pattern (Preferred for recoverable deletes)

"[Item name] deleted.  Undo"
                       ↑ inline action link, not a button

## Rules
1. Show for 8-10 seconds (longer than standard toasts)
2. "Undo" link triggers immediate restore
3. After dismiss: deletion is permanent
4. Never show for items that affect others (shared resources)

## Variants
"3 files deleted.  Undo"
"Message discarded.  Restore"
"Draft removed.  Undo"

## When NOT to use soft delete
- Financial transactions (use confirmation modal instead)
- Account deletion (multi-step confirmation required)
- Shared resources that affect other users
```

### Inline Validation — Approachable Error Copy

フォームフィールドのエラーコピー。親しみやすく、具体的に。

```markdown
## Tone Principles
- Talk to the user, not at them
- Name the requirement, not the violation
- Avoid "invalid", "error", "wrong"

## Templates
"[Field] needs to be [requirement]."
"Enter a [format]. Example: [concrete example]"
"[Field] is [too short/too long]. Use [X]–[Y] characters."

## Good vs Bad
✅ "Password needs at least 8 characters."
❌ "Invalid password"

✅ "Enter your email like: name@company.com"
❌ "Email format is incorrect"

✅ "Username is taken. Try adding a number or symbol."
❌ "Username already exists"

✅ "That's a bit short — 3 characters minimum."
❌ "Minimum length not met"

## Timing (reinforcement)
- Show on blur (not on keystroke)
- Clear the error as soon as the field becomes valid
- Don't stack multiple errors per field — show the most important one
```

### Error Prevention Microcopy

不可逆アクションの前に確認パターンを設ける。

```markdown
## Pre-Action Warning (inline, before button tap)

Pattern: Warning text adjacent to the destructive button.
"This will permanently delete your account and all data."
[Delete my account]

## Confirmation Input (for high-stakes actions)

Pattern: Require user to type a phrase before confirming.
"Type DELETE to confirm account deletion."
[text field] [Confirm deletion]

Use when:
- Account deletion
- Bulk data deletion (> 100 items)
- Billing cancellation with data loss

## Friction Copy Rules
1. Friction must be proportional — don't gate low-stakes actions
2. Explain what will be lost, not just what will happen
3. Provide a clear escape: "Actually, keep my account →"
4. Never auto-select the destructive option

## Warning vs Confirmation Choice
| Risk Level | Pattern |
|-----------|---------|
| Low (reversible) | Soft delete + Undo toast |
| Medium (partial loss) | Confirmation modal (specific labels) |
| High (full irreversible loss) | Confirmation modal + type-to-confirm |
```
