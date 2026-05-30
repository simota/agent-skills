# Core Design Principles (platform-agnostic)

Binding for **all** surfaces (web, iOS, Android). Platform layers (`frontend.md`, `ios.md`, `android.md`) may add deltas but must not contradict these. Each entry follows `_templates/principle-entry.md`. IDs are slugs (`P-CORE-<slug>`), not numbers — see `INDEX.md` for the cross-layer index.

> Status legend: `proposed` (awaiting human review — NOT yet binding) · `accepted` (binding) · `deprecated` (moved to Archive below).

---

### P-CORE-control-feedback — Every interactive control gives feedback within 100ms
- **Statement:** Any tap/click/keypress on an interactive element must produce a visible state change (press, loading, or result) within 100ms.
- **Rationale:** Perceived responsiveness; silence reads as "broken". [Source: baseline — Nielsen response-time limits]
- **Scope:** core
- **Tags:** feedback, responsiveness
- **Source feedback:** baseline
- **Do:** show a pressed state + inline spinner on submit; disable the control while pending.
- **Don't:** block the UI with no indicator while a request is in flight.
- **Token:** —
- **Status:** accepted · **Added:** 2026-01-01 · **Last reviewed:** 2026-01-01

### P-CORE-error-cause-action — Errors state the cause and the next action
- **Statement:** Error messages name what went wrong in plain language and offer a concrete recovery action.
- **Rationale:** Generic errors ("Something went wrong") strand users. [Source: baseline]
- **Scope:** core
- **Tags:** error, content
- **Source feedback:** baseline
- **Do:** "Card declined — try another payment method." + retry button.
- **Don't:** "Error 500" with no guidance.
- **Token:** —
- **Status:** accepted · **Added:** 2026-01-01 · **Last reviewed:** 2026-01-01

### P-CORE-reversible-destructive — Destructive actions are reversible or confirmed
- **Statement:** Any action that destroys user data offers undo, or requires explicit confirmation when undo is impossible.
- **Rationale:** Protects against accidental loss; trust. [Source: baseline]
- **Scope:** core
- **Tags:** error, feedback
- **Source feedback:** baseline
- **Do:** delete → toast with "Undo" for 5s; permanent delete → typed confirmation.
- **Don't:** immediate irreversible delete on a single tap.
- **Token:** —
- **Status:** accepted · **Added:** 2026-01-01 · **Last reviewed:** 2026-01-01

---

<!-- New accepted principles are appended above this line by the PROMOTE step. -->

## Archive (deprecated)

<!-- Superseded principles move here (keep full entry + `Superseded by:`). ENFORCE ignores this section. -->
