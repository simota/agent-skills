# Guardian AUTORUN Decisions

Read when an autonomous PR/history analysis reaches a pause, recovery, or partial-result decision. Emit the default completion schema in `_common/AUTORUN.md`; authorization and status follow that contract, not a local substitute.

## Pause for Confirmation

- Release timing, shared merge workflow, or hotspot-refactoring scope would change.
- A destructive Git action, force-push, shared/already-pushed history rewrite, or attribution-sensitive multi-author squash is proposed.
- `quality_score < 35`, `risk_score > 85`, or high-risk changes have no security review.
- Squash plan has `10+` commits, or its score is neutral (`-14` through `+14`).

A blocking security finding requires the security handoff and blocks completion. A non-blocking coverage/noise handoff alone does not authorize changes or block other safe analysis.

## Recovery

| Condition | Action |
|-----------|--------|
| Unresolved merge-conflict markers | Route investigation to Scout; do not guess a resolution |
| PR size `> XL` | Propose a split using `reference/pr-split-strategy.md`; size alone does not authorize edits |
| Suggested branch name already exists | Offer suffixed alternatives; never overwrite it |
| Analysis timeout or memory limit | Reduce to essential files, maximum two retries; record omitted scope |
| Missing metadata or partial CI | Report uncertainty; do not invent a passing score/check |
| Shared rewrite or conflicting handoffs | Return `BLOCKED` or `PARTIAL` according to the remaining actionable scope |

## Partial Results

Use `PARTIAL` for missing CI/coverage/risk evidence, incomplete branch context, outstanding non-blocking work, or reduced analysis scope. Name completed sections, missing evidence, all blocking findings, and the smallest safe next action. A usable report does not make the omitted work `SUCCESS`.
