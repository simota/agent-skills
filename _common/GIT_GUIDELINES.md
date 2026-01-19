# Git Commit & PR Guidelines

Standard guidelines for commit messages and pull requests. All agents must follow these conventions.

---

## Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, semicolons, etc.) |
| `refactor` | Code refactoring (no feature change, no bug fix) |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks (deps, build, etc.) |
| `ci` | CI/CD changes |
| `security` | Security fixes |

### Rules

1. **DO NOT include agent names** in commit messages
   - ❌ `feat: Builder implements user validation`
   - ✅ `feat(user): add input validation`

2. **Keep subject line under 50 characters**
   - ❌ `feat: add user profile editing feature with name email and avatar support`
   - ✅ `feat(profile): add user profile editing`

3. **Use imperative mood** (command form)
   - ❌ `fixed login bug`
   - ❌ `fixes login bug`
   - ✅ `fix: resolve login authentication error`

4. **Scope is optional but recommended** for clarity
   - `feat(auth): add OAuth2 support`
   - `fix(api): handle null response`

5. **Body explains "why", not "what"** (the code shows "what")

### Examples

```
feat(auth): add password reset functionality

fix(cart): resolve race condition in quantity update

refactor(user): extract validation logic to separate module

docs(api): update authentication endpoint documentation

perf(search): add database index for faster queries

test(payment): add edge case tests for refund flow

chore(deps): upgrade React to v18.2.0

security(input): sanitize user input to prevent XSS
```

---

## Pull Request Format

### Title Format

```
<type>(<scope>): <brief description>
```

Same rules as commit messages:
- **DO NOT include agent names**
- Keep under 50 characters
- Use imperative mood

### PR Description Template

```markdown
## Summary
Brief description of what this PR does (1-3 sentences).

## Changes
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Edge cases covered

## Notes
Any additional context, screenshots, or considerations.
```

### Rules

1. **DO NOT mention agent names** in PR title or description
   - ❌ `Scout investigation: login bug fix`
   - ❌ `Builder implementation: user profile feature`
   - ✅ `fix(auth): resolve login session timeout`
   - ✅ `feat(profile): add user profile editing`

2. **Focus on the change, not the process**
   - ❌ `Refactored by Zen agent for better readability`
   - ✅ `refactor(utils): improve code readability`

3. **Reference issues** when applicable
   - `Fixes #123`
   - `Closes #456`
   - `Related to #789`

---

## Branch Naming (Optional Reference)

```
<type>/<short-description>
```

Examples:
- `feat/user-profile-editing`
- `fix/login-session-timeout`
- `refactor/auth-module-cleanup`

---

## Summary

| Element | Include Agent Name? | Format |
|---------|---------------------|--------|
| Commit message | ❌ No | `type(scope): description` |
| PR title | ❌ No | `type(scope): description` |
| PR description | ❌ No | Focus on changes, not process |
| Branch name | ❌ No | `type/short-description` |
