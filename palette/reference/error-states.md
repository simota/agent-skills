# Error States

## Purpose

Errors are not exceptions — they are a system. Every interactive surface eventually fails (validation, permission, server, network). Users judge product quality by how the failure is handled, not by whether it happens. This reference defines the failure taxonomy, placement decisions, recovery paths, and message hierarchy.

## Scope Boundary

- IN scope: error classification, placement (inline vs toast vs banner vs page), recovery affordances (retry, undo, support escalation), error severity hierarchy, post-error state handoff to empty/loading.
- OUT of scope: exact error wording (delegate to `prose`), HTTP status-code → message mapping in code (delegate to `artisan`), backend error reporting (`beacon`), validation library configuration (`artisan`), accessibility audit details (use `a11y` subcommand).

## Core Concepts

### Error Taxonomy

| Class | Source | Recovery | Example |
|-------|--------|----------|---------|
| Validation | User-side input | User edits and resubmits | "Email must include @" |
| Permission | Server policy | Authenticate / request access | "Sign in to continue" / "You don't have access" |
| Server | Backend failure | Retry, often automatically | "We couldn't save. Trying again." |
| Network | Connectivity | Retry when online | "You're offline. We'll save when reconnected." |
| Conflict | Concurrent edit | Show diff, let user resolve | "Someone else changed this" |
| Quota / Rate | Limits exceeded | Wait, upgrade, or contact | "Daily limit reached" |
| Catastrophic | Data loss / unrecoverable | Apologize, escalate to support | "We lost your draft. Sorry." |

Different classes need different treatments. Treating a network blip the same as a validation error creates noise.

### Placement Decision

| Placement | When | Lifetime |
|-----------|------|----------|
| Inline (next to field) | Validation errors | Until field changes |
| Inline (next to action) | Action-specific failure | Until retry / dismiss |
| Toast (transient) | Server / save / non-blocking | Auto-dismiss after 4–8s |
| Banner (top-of-page) | Persistent state (offline, billing past due) | Until condition resolves |
| Modal | Conflict resolution / data loss | Until user decides |
| Full page | Auth failure / 404 / 5xx where the feature can't continue | Until navigation |

Rules:

1. The error appears where the user is looking. Form errors live next to fields; save errors near the save button; auth errors at page level.
2. Toasts can be missed. Reserve them for non-blocking confirmations and recoverable failures.
3. Modals are **interrupting**. Use only when the user **must** make a decision (conflict, destructive confirm, data loss).
4. Banners are persistent — overuse turns them into wallpaper. Limit to 1 active banner per page.

### Severity Hierarchy

| Severity | Color cue | Behavior |
|----------|-----------|----------|
| Info / advisory | Blue or neutral | Non-blocking; user proceeds |
| Warning | Yellow / amber | Action allowed but discouraged; require confirmation |
| Error | Red | Action blocked; must be resolved |
| Critical | Red + escalation | Data integrity / security; cannot continue |

WCAG: never rely on color alone (SC 1.4.1). Pair color with icon and text label.

### Message Construction

Effective error messages have four parts:

1. **What happened** (objective) — "We couldn't save your draft."
2. **Why** (cause, when known) — "The file is larger than 25 MB."
3. **How to recover** (action) — "Try a smaller file."
4. **Escape hatch** (alternative) — "Or contact support."

Avoid:

- Codes without translation ("Error 0x80004005").
- Blame ("You entered an invalid email").
- Apologies as the whole message ("Oops! Something went wrong.").
- Hidden errors (silent fail).
- Generic "An error occurred" without context.

Pair message tone with the error class — playful tone is fine for low-severity, inappropriate for data-loss.

### Recovery Affordances

| Affordance | When |
|------------|------|
| Inline correction | Validation — let user edit in place, no page reload |
| Retry button | Server / network — user-controlled retry after failure |
| Auto-retry with feedback | Network blips — silent retry with "Reconnecting…" indicator |
| Undo (toast) | Successful but reversible action ("Item deleted. Undo") |
| Save draft | Long forms — prevent loss on submit error |
| Conflict diff | Concurrent edit — "Your version" / "Their version" / "Merge" |
| Escalation | Catastrophic — "Contact support with code REF-87234" |

Always offer **at least one path forward**. Dead-end errors ("Cannot continue") destroy trust.

### Optimistic UI and Rollback

For low-stakes mutations (likes, toggles, reorders), apply the change immediately and roll back on failure. The pattern:

1. Optimistically update local state.
2. Send mutation.
3. On success: confirm silently (or with subtle toast).
4. On failure: roll back, show error toast with retry.

For high-stakes (payment, irreversible actions), do **not** apply optimistic UI — wait for confirmation.

### Form Validation Timing

| Trigger | When |
|---------|------|
| On submit only | Short forms; avoid premature critique |
| On blur | Per-field validation as user moves on (the most common pattern for production forms) |
| On change (debounced) | Strong constraints (password strength, username availability) |
| Mixed | Most production: blur for most fields, on-change for high-feedback fields |

Never show errors as the user types — frustrates users by criticizing incomplete input.

### Server-Error Boundaries

In code (delegate to `artisan`), but the design contract:

| Layer | Behavior |
|-------|----------|
| Component-level | Catch render errors, show inline fallback |
| Route-level | Catch async failures, show "Couldn't load this section. Retry." |
| App-level | Last-resort catch-all, "Something went wrong. Reload the app." |

Each layer must offer a recovery action; "Reload" is the minimum.

### Accessibility

- `aria-live="polite"` for non-urgent announcements (form validation results).
- `aria-live="assertive"` only for critical alerts that interrupt (data loss, security).
- `role="alert"` for errors that need immediate attention.
- Pair the visual error with text reading by screen readers — color alone fails (WCAG 1.4.1).
- Focus management: on submit error, move focus to the first invalid field (or a top-of-form summary).
- Don't trap focus in a modal error without an escape path.

### Error Empty State Handoff

After an error, the underlying surface is often empty (failed list load, search returning zero, deleted item view). Pair the error with the appropriate empty state — see `empty-states.md`.

### Error Logging and Privacy

The visible message is the **user-facing** error. The internal log is separate:

- Visible: short, recovery-oriented, no stack trace.
- Internal: full stack, request ID, user agent, timestamp.
- Reference ID shared with user only when escalation is offered: "If you contact support, share REF-87234."
- Never echo PII into errors ("Email john@example.com is invalid" — leak risk).

## Workflow

1. **Classify the error** — validation / permission / server / network / conflict / quota / catastrophic.
2. **Choose placement** — inline / toast / banner / modal / page.
3. **Pick severity** — info / warning / error / critical (with color + icon + label).
4. **Compose message** — what / why / how-to-recover / escape hatch.
5. **Design recovery affordance** — inline correct / retry / auto-retry / undo / save-draft / diff / escalation.
6. **Decide optimistic UI** — apply only for low-stakes reversible mutations.
7. **Set validation timing** — submit / blur / change / mixed.
8. **Pair with empty state** if surface becomes empty after error.
9. **Verify accessibility** — `aria-live`, `role="alert"`, focus management, color independence.
10. **Document logging policy** — what's visible, what's logged, no PII echo.

## Output Template

```yaml
error_design:
  surface: "checkout submit"
  errors:
    - id: E-validation-card
      class: validation
      placement: inline_field
      severity: error
      message:
        what: "カード番号が正しくありません"
        why: ""             # implicit
        recover: "番号をご確認ください"
        escape: ""
      timing: on_blur
      recovery: inline_correction
      a11y:
        aria_live: polite
        focus_on_submit: first_invalid_field
        color_independence: yes
    - id: E-server-charge
      class: server
      placement: banner_below_button
      severity: error
      message:
        what: "決済を完了できませんでした"
        why: "カード会社で承認されませんでした"
        recover: "別のカードを試すか、しばらく待って再試行してください"
        escape: "問題が続く場合は support@example.com まで（REF-{id} を共有）"
      recovery: retry_button + escalation
      optimistic_ui: no   # high-stakes
      a11y:
        role: alert
        aria_live: assertive
      log:
        visible_to_user: short
        internal: full_stack + request_id + REF-id
        pii_in_message: no
    - id: E-network-blip
      class: network
      placement: toast_persistent
      severity: warning
      message:
        what: "オフラインです"
        recover: "接続が回復したら自動で保存します"
      recovery: auto_retry_with_feedback
      banner_text: "再接続中…"
```

## Anti-Patterns

- "An error occurred" with no context — the worst possible message.
- Stack traces or HTTP codes shown to end users without translation.
- Errors that don't tell the user what to do next.
- Treating all errors as red — devalues the truly critical ones.
- Modal for low-stakes errors — interrupts unnecessarily.
- Toast for errors the user must see (auto-dismiss = guaranteed miss).
- Validation on every keystroke — punishes typing.
- Form-level "Please fix the errors" with no anchor link to the first error.
- Generic copy for every class ("Failed" doesn't tell the user it's a permission issue vs server issue).
- Echo of PII in error messages ("Password 'qwerty123' is too weak").
- Optimistic UI on high-stakes mutations (payments, deletes without undo).
- Errors that block all interaction without offering recovery.
- Silent failures (no UI feedback when something fails server-side).
- Error pages with no link back to working content.
- Reference ID shown by default — clutters; show only on escalation.
- Treating offline as a hard error — connectivity is normal; queue and retry.

## Deliverable Contract

An error-state design is complete when:

- All anticipated failures classified into the 7 classes.
- Placement chosen for each (inline / toast / banner / modal / page).
- Severity assigned with color + icon + label (no color-only).
- Message has what / why / recover / escape parts.
- Recovery affordance specified per error.
- Validation timing decided (submit / blur / change / mixed).
- Optimistic UI policy stated per mutation.
- Accessibility specified (aria-live, role, focus, color independence).
- Empty-state handoff designed if applicable.
- Logging and PII policy documented.

## References

- Jakob Nielsen, *Heuristic #9: Help users recognize, diagnose, and recover from errors* (NN/g, classic).
- W3C, *WCAG 2.2*, SC 3.3.1 / 3.3.3 / 3.3.4 — error identification, suggestion, prevention.
- Don Norman, *The Design of Everyday Things* — error vs slip vs mistake distinction.
- Nicole Fenton & Kate Kiefer Lee, *Nicely Said* — error-message tone guide.
- Microsoft Writing Style Guide — error messages chapter.
- Apple HIG / Material Design — platform-specific severity and placement.
- Frank Spillers, *Demystifying the User Experience of Errors* (UX Magazine, 2024).
- WAI-ARIA Authoring Practices, *Alert pattern*.
- Google's Material Design — *Confirmation & acknowledgement*.
- Atlassian Design System, *Error and warning patterns*.
