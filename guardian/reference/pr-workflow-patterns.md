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

## PR Description Template (canonical)

This is the **single source of truth** for the PR body Guardian composes — `output-templates.md` Section 14 and `pr-ship-flow.md` CREATE both follow it; do not invent divergent variants.

The PR body states the essence and nothing more: **why** the change exists, **what** changed, and **how** it was verified. Scale it to the change; omit any section that would be empty or that merely restates the Summary.

Default body (most PRs need only this):

```markdown
## Summary
<!-- 1-3 sentences: why this change exists and what it does -->

## Test plan
<!-- how it was verified — the suite run or the manual steps -->
```

`## Test plan` records what was **run**, never what was intended. Two rules bind it:

- **Never write an unperformed check.** "Regeneration matches", "tested on staging", "CI green" are claims; if the command was not run, the line does not exist. This is the single most damaging PR-body defect, because it converts a missing verification into a recorded one.
- **State the limit when a claim outruns its evidence.** A `Not verified:` line beneath the test plan is not an admission of weakness — it moves residual risk from invisible to decidable, and it is what lets a reviewer accept staged rollout instead of demanding more tests.

```markdown
## Test plan
- unit: same idempotency key returns the first result
- integration: 20 concurrent requests → provider called once
- manual: staging replay of a client retry

Not verified: simultaneous requests across regions — covered by staged rollout + duplicate-charge metric
```

Include the `Not verified` line whenever a claim rests on a narrower environment than production (single region, seeded data, mocked dependency), whenever coverage is structural rather than domain-boundary (100% branch coverage inside one tenant proves nothing about cross-tenant access), and on every AI-assisted PR where implementation and tests share an author — same author, same misunderstanding, tests that pass anyway.

Add a `## Changes` bullet list **only** when the diff spans several distinct essential changes the Summary cannot convey in a sentence (one bullet per essential change, no sub-bullets for noise).

Conditional sections — include each only when it carries real information:

| Section | Include when |
|---------|--------------|
| `## Changes` | multiple distinct essential changes (else fold into Summary) |
| `## Risk` | risk band is Medium+ or a rollback note is needed |
| `## Breaking changes` | the change breaks a public API/contract |
| `## Review focus` | the change crosses a boundary — see below |
| `## Related issues` | an issue exists (`Closes #123`) |
| `## Screenshots` | UI changed |

### `## Review focus` (boundary-crossing changes only)

Include **only** when the diff touches a public API or contract, persisted state or schema, a security/trust boundary, or consumers outside the authoring team. Everything else — the majority of PRs — omits it.

The section exists because reviewers disagree when they are reading at different magnifications: one comments on naming while another asks about service contracts, and the structural risk gets buried under style debate. Declaring the intended magnification, and what is deliberately *out* of it, resolves that before the first comment.

```markdown
## Review focus
change_scope:   module + public API
blast_radius:   checkout clients (4)
reversibility:  code high / persisted state low
review_needed:
  - invariant and error semantics
  - backward compatibility
  - telemetry
not_in_scope:
  - service boundary redesign
```

- `blast_radius` names *who* breaks, not how many files changed.
- `reversibility` is split whenever code and state differ — a revertable deploy that has already written bad rows is not reversible.
- `not_in_scope` is what makes the section work: it gives a reviewer permission to stop, and closes the "one more thing" loop before it opens.
- Reviewers are not expected to read every magnification at equal depth. Concentrate depth where `reversibility` is low or `blast_radius` is wide.

### Brevity rules (apply to every section above)

- Scale to size: `XS`/`S` PRs → Summary + Test plan only. Sections grow with the change, never by default.
- No boilerplate checklists ("self-review completed", "docs updated") in the body — self-review is author pre-flight, not reviewer-facing content.
- Do not inline the Guardian analysis report (Change Classification Table, Quality Score, full Risk breakdown). That report is review-prep for the author/reviewer; link or summarize it in one line, never paste it into the PR body.
- Guide with HTML comments, not long prose; delete the comment once filled.

## Anti-Patterns

| Pattern | Why it hurts | Safer alternative |
|---------|--------------|-------------------|
| mega PR (`>1000` lines) | review quality drops sharply | split into `200-400` line chunks |
| empty description | reviewers lack context | require a template |
| multiple unrelated concerns | review and rollback become harder | one concern per PR |
| self-merge without review | bypasses quality gates | require at least one review |
| stale PRs | conflict risk and lost context | define review SLAs such as `24h` |
| no self-review | easy issues leak into review | complete a checklist before requesting review |
