# PR Workflow Patterns

Purpose: Choose a PR structure that keeps review quality high and merge latency low.

## Contents

- PR size guidance
- Stacked PRs
- Draft PRs
- PR description template
- Anti-patterns

## PR Size Guidance

| Size | Lines | Guidance |
|------|-------|----------|
| `Small` | `< 200` | ideal, fastest review |
| `Medium` | `200-400` | recommended range |
| `Large` | `400-1000` | review quality starts dropping |
| `Mega` | `> 1000` | anti-pattern, split required |

Default principle:
- `1 PR = 1 task / 1 concern`

## Stacked PRs

Use stacked PRs when a large feature can be reviewed as dependent slices without blocking delivery.

Example flow:
1. `feature/step-1` -> `main`
2. `feature/step-2` -> `feature/step-1`
3. label or title each PR with stack position, such as `[1/3]`

Representative tools:
- `Graphite`
- `ghstack`
- `Git Town`

Example:

```bash
gt branch create feat-step-1
gt commit create -m "feat: add schema"
gt branch create feat-step-2
gt stack submit
```

## Draft PRs

Use Draft PRs to:
- validate direction early
- surface CI failures before full review
- signal to reviewers that feedback should focus on direction, not merge readiness

## PR Description Template

```markdown
## Summary
<!-- What changed and why -->

## Changes
- [ ] Change 1
- [ ] Change 2

## Related Issues
<!-- Closes #123, Refs #456 -->

## Screenshots / Recordings
<!-- If UI changed -->

## Test Plan
- [ ] Unit tests added/updated
- [ ] Manual testing steps

## Checklist
- [ ] Self-review completed
- [ ] Documentation updated (if needed)
- [ ] No breaking changes (or documented)
```

Keep templates short and guide authors with HTML comments instead of long prose.

## Anti-Patterns

| Pattern | Why it hurts | Safer alternative |
|---------|--------------|-------------------|
| mega PR (`>1000` lines) | review quality drops sharply | split into `200-400` line chunks |
| empty description | reviewers lack context | require a template |
| multiple unrelated concerns | review and rollback become harder | one concern per PR |
| self-merge without review | bypasses quality gates | require at least one review |
| stale PRs | conflict risk and lost context | define review SLAs such as `24h` |
| no self-review | easy issues leak into review | complete a checklist before requesting review |
