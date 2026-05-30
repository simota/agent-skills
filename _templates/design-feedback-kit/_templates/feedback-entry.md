# Feedback Entry Template

Append this block to `feedback-log.md` during the CAPTURE step (fill `status: new`, leave Analysis/Proposed blank until ANALYZE).

## ID scheme (collision-free)
`FB-<YYYYMMDD>-<slug>` — date of capture + a short kebab-case mnemonic of the feedback.
- `FB-20260115-double-save`, `FB-20260203-tiny-tap-target`.
- Date + slug avoids the shared-counter collision that plain `FB-NNN` causes when several people log feedback the same day.

```markdown
### FB-YYYYMMDD-<slug>
- **Date:** YYYY-MM-DD
- **Source:** interview | usability-test | review | support-ticket | analytics | app-store-review | echo-walkthrough
- **Platform:** core | frontend | ios | android
- **Raw feedback:** "<verbatim or close paraphrase — keep the user's words>"
- **Analysis:** <ANALYZE step: theme cluster + friction assessment; blank until analyzed>
- **Proposed principle:** <P-...-slug draft, or 'none'; blank until analyzed>
- **Status:** new | analyzed | promoted | rejected
- **Reviewed by:** <human, REVIEW step> · **Decision date:** YYYY-MM-DD
<!-- if promoted: -->
- **Promoted to:** P-<SCOPE>-<slug>
<!-- if rejected: -->
- **Reject reason:** <why this did not become a principle — e.g. one-off below threshold, out of scope, contradicts P-...>
```

## Rules
- **Keep the user's words** in Raw feedback — don't pre-interpret; interpretation belongs in Analysis.
- **Promotion threshold (guidance):** promote a theme to a principle when **≥2 independent feedback items** share it, OR a **single high-severity** item (data loss, blocked task, a11y blocker). Below that, mark `analyzed` and leave for accumulation — don't promote one-off opinions.
- **One signal ≠ one law.** A single low-severity complaint can be `analyzed` then `rejected` with a reason; that rejection is itself useful history.
- **Tag the platform** so ANALYZE knows whether the resulting principle is core or a delta.
- **Archive yearly:** when `feedback-log.md` grows large, move resolved prior-year entries to `feedback-log-<YEAR>.md` to keep the active log scannable.
