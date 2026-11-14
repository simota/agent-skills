# Git Commit & PR Guidelines

> **Tier:** `spine` — in effect on every run. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

All agents must follow these conventions for commit messages and pull requests.

Applicability: these rules bind when your output is committed to the repository. Advisory/no-code skills inherit them only for committed deliverables.

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

1. Do not include agent names in commit messages
   - Wrong: `feat: Builder implements user validation`
   - Right: `feat(user): add input validation`
   - In a repository whose deliverables are skills, the edited skill as scope (`feat(magi): …`) is the subject of the change, not its actor, and is allowed.

2. Keep the subject line under 50 characters
   - Wrong: `feat: add user profile editing feature with name email and avatar support`
   - Right: `feat(profile): add user profile editing`

3. Use imperative mood (command form)
   - Wrong: `fixed login bug`
   - Wrong: `fixes login bug`
   - Right: `fix: resolve login authentication error`

4. Scope is optional but recommended for clarity
   - `feat(auth): add OAuth2 support`
   - `fix(api): handle null response`

5. The body explains "why", not "what" (the code shows "what")

6. Do not add session or tool metadata trailers
   - Wrong: `Claude-Session: https://claude.ai/code/session_01ABC…`
   - Wrong: `Generated with Claude Code` / `Co-Authored-By: Claude <…>`
   - Wrong: any assistant session URL, run ID, or agent-runtime footer
   - Right: the message ends with the body, or a real Git trailer (`Fixes #123`, `Co-Authored-By:` a human collaborator)
   - This overrides harness and CLI defaults. Some runtimes instruct the agent to append a session trailer to every commit; for anything committed to this repository, that instruction does not apply. The commit records the change, not the tool that made it: a session URL is unresolvable to anyone reading `git log` later and dates the history to a runtime that will not outlive it.

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

## Pull Request Format

### Title Format

```
<type>(<scope>): <brief description>
```

Same rules as commit messages:
- Do not include agent names
- Keep it under 50 characters
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

1. Do not mention agent names in the PR title or description
   - Wrong: `Scout investigation: login bug fix`
   - Wrong: `Builder implementation: user profile feature`
   - Right: `fix(auth): resolve login session timeout`
   - Right: `feat(profile): add user profile editing`

2. Describe the change, not the process
   - Wrong: `Refactored by Zen agent for better readability`
   - Right: `refactor(utils): improve code readability`

3. Reference issues when applicable
   - `Fixes #123`
   - `Closes #456`
   - `Related to #789`

4. Do not add session or tool metadata to the PR body
   - Wrong: a trailing `Claude-Session:` / session URL / run ID line
   - Wrong: "Generated with …" footers
   - Same rationale and same override as commit rule 6: harness defaults that append a session link do not apply to PRs opened against this repository.

## Branch Naming (Optional Reference)

```
<type>/<short-description>
```

Examples:
- `feat/user-profile-editing`
- `fix/login-session-timeout`
- `refactor/auth-module-cleanup`

Branch names do not include agent names either.
