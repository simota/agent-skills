# Feedback Log (append-only)

The audit trail of every UI/UX feedback item and what became of it. **Append new entries; preserve their original date, source, platform, and raw feedback.** Fill or update Analysis, Proposed principle, Status, Reviewed by, Decision date, Promoted to, and Reject reason as the entry progresses through the loop. Record later decision changes as appended notes so prior review history remains visible. Each entry follows `_templates/feedback-entry.md`.

> Status flow: `new` → `analyzed` → (`promoted` | `rejected`). A `promoted` entry links to the principle slug it produced.
> ID format: `FB-YYYYMMDD-<slug>` (date + short mnemonic; check uniqueness and add a source/session suffix on collision).
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
