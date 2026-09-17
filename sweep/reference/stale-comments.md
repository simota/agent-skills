# Comment Cleanup Decisions

Load for `comments`; use `reference/cleanup-protocol.md`. Comments may carry types, build directives, licensing, suppression or safety obligations. Check those before confidence scoring; ≥70 is a proposal threshold, not permission to delete.

## Candidate Bands

| Category | Indicator | Confidence to remove |
|---|---|---|
| Aged TODO/FIXME | `// TODO(2023):` or git blame >180 days | 70-85 |
| Commented-out code | `/* ... */` block of N≥3 lines that was once code | 80-90 |
| Divergent JSDoc | `@param x: number` but actual signature is `string` | 60-75 (repair may be safer) |
| Version-stale | `// added in v1.2` and current version is 5.x | 75-85 |
| Author/date noise | `// John 2018-04-15` | 90+ only if not an audit trail |
| Dead reference | `// see docs/old-feature.md` (file deleted) | 85+ |
| Obvious paraphrase | `i++; // increment i` | 85+ |
| Outdated workaround | `// workaround for IE11 bug` (IE11 dropped) | 80-90 |


Age/version distance only starts investigation. Check linked work items, actual platform support, history and the replacement document before treating a TODO, workaround, `@since` or `@deprecated` note as obsolete. Prefer repairing divergent JSDoc over removing a still-needed contract.

## Protected Content

Preserve license headers, compliance author/date trails, active lint/build/compiler directives, type-providing JSDoc, unsafe/concurrency/order invariants (`SAFETY`, `WARN`, `INVARIANT`, `XXX-safety`), regex/algorithm explanations, justified type assertions, vendor quirks and otherwise ambiguous constants. Reference code may be intentional; verify its actual consumer, not merely code-like syntax.

## Scoring Signals

| Signal | Confidence delta |
|---|---|
| Tool flagged | +20 |
| `git blame` age > 180 days | +15 |
| `git blame` age > 365 days | +25 |
| Commented-out code (≥ 3 lines) | +30 |
| Author tag with old date | +20 |
| References deleted file | +25 |
| Divergent JSDoc + auto-fix available | +20 |
| Inside complex algorithm or regex | -40 |
| Contains `SAFETY` / `WARN` / `INVARIANT` keywords | -50 |
| License header | -100 (never remove) |


Record applicable signals and evidence. The legacy delta table does not define a base score, cap, or whether overlapping age deltas accumulate; do not invent a numeric confidence from it. Report that ambiguity and require review when it changes eligibility. Preserve the existing delivery bands: ≥80 expedited proposal, 70–79 review-required, below 70 not a removal proposal; neither band bypasses confirmation or protection.

## Verification and Handoff

Use configured source/JSDoc analysis and git history, not an unverified plugin or filename-unsafe shell loop. Establish JS/JSDoc type-checking baseline (`checkJs` where applicable); re-run the project's type checks, build, tests and lint after implementation. Check sourcemap/line-sensitive tests and emitted artifacts; “comments cannot change behavior” is not a verification result.

Report scope, scanned categories, candidate count, expedited/review/protected counts, per-item evidence, license/safety preservation, linked-TODO disposition and actual check results. Builder owns execution; Quill receives annotation-repair work.

Type-bearing JSDoc: https://www.typescriptlang.org/docs/handbook/jsdoc-supported-types.html (checked 2026-09-17). Confirm the target project's JS checking configuration.
