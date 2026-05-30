# Feedback Log (append-only)

The audit trail of every UI/UX feedback item and what became of it. **Never edit history; only append and update `status`/`promoted-to`.** Each entry follows `_templates/feedback-entry.md`.

> Status flow: `new` → `analyzed` → (`promoted` | `rejected`). A `promoted` entry links to the principle slug it produced.
> ID format: `FB-YYYYMMDD-<slug>` (date + short mnemonic — collision-free on concurrent appends).
> Promotion threshold: ≥2 independent items on a theme, OR a single high-severity item (data loss / blocked task / a11y blocker).
> Archive: move resolved prior-year entries to `feedback-log-<YEAR>.md` when this file grows large.

---

### FB-20260115-double-save (example)
- **Date:** 2026-01-15
- **Source:** usability-test
- **Platform:** frontend
- **Raw feedback:** "I tapped Save twice because nothing happened — then it saved twice."
- **Analysis:** Missing in-flight feedback on submit; double-submission risk. Theme: responsiveness. (Echo friction: high — uncertainty + duplicate side effect.) High-severity (duplicate write) → meets threshold on its own.
- **Proposed principle:** P-CORE-control-feedback (feedback within 100ms + disable while pending).
- **Status:** promoted
- **Reviewed by:** (human) · **Decision date:** 2026-01-16
- **Promoted to:** P-CORE-control-feedback

---

<!-- New feedback is appended below by the CAPTURE step with status: new. -->
