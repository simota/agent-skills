# Forms UX Patterns Reference

Purpose: Design forms that minimize user effort, fail gracefully, and cooperate with browser autofill and password managers. Choose the right field order, validation timing, error display, step flow, defaults, and submission feedback. Forms are the highest-friction surface in most products; a 10% completion-rate lift on a signup form often beats any other UX win.

## Scope Boundary

- **Palette `forms`**: field order rationale, inline vs submit-time validation, error-message voice direction, required-field indication, progressive disclosure, multi-step flows, autofill cooperation, password-manager handshake, submission feedback, unsaved-changes handling.
- **Palette `a11y` (elsewhere)**: WCAG 2.2 SC 3.3.x (error identification, suggestion, prevention), SC 1.3.5 (autocomplete identification), SC 3.3.8 (accessible authentication) conformance.
- **Flow (elsewhere)**: error-shake animation, success-check motion, step-transition easing.
- **Prose (elsewhere)**: exact error-message wording, label copy, help-text tone — Palette sets the **voice direction** (blame-free, specific, recovery-focused) and Prose writes the strings.
- **Artisan (elsewhere)**: React Hook Form / Formik / VeeValidate / SwiftUI Form production wiring, Zod / Yup schema, server-round-trip error handling.

If the question is "what is the right field order and validation timing?" → `forms`. If it's "what exact words for this error?" → Prose. If it's "how do I wire this in React Hook Form?" → Artisan.

## Contents

- Field-order rationale
- Validation timing
- Error display and voice
- Required-field indication
- Progressive disclosure
- Multi-step forms
- Defaults
- Submission and unsaved changes
- Autofill and password-manager cooperation
- Passkeys and modern authentication
- Accessible authentication (WCAG 2.2 SC 3.3.8)
- Anti-patterns
- Accessibility checklist

## Field-Order Rationale

Order fields to match the user's mental progression and minimize task-switching cost.

| Principle | Example |
|-----------|---------|
| Easy → hard | Name (typed) → email (typed) → password (effortful) |
| Identity → context → action | Who are you? → what do you want? → confirm |
| Group related fields | Street + city + zip together; not interleaved with phone |
| Required before optional | Required fields first; optional grouped at bottom |
| One decision per step (multi-step) | Don't mix identity and payment on the same step |

Anti-pattern: alphabetical order, database-column order, or "however the backend schema is shaped" order. These optimize for the developer, not the user.

## Validation Timing

| Strategy | Best for | Pitfalls |
|----------|----------|----------|
| Inline on blur | Most text fields (email, name, URL) | Don't validate on every keystroke — premature error |
| Inline on input, after first blur | Password strength, confirm-password match | Track "touched" state per field |
| Real-time | format-specific fields such as email, URL, phone, password strength | immediate help, but can interrupt typing |
| Submit-time only | Short forms (<4 fields), confirmation dialogs, cross-field or complex validation | Jarring if many fields fail at once |
| Async on blur (debounced) | "Username available?", "email already registered?" | Show loading state; never race server |

Rules:
- Never validate a field the user has not yet touched. "Please enter your email" shown before the user types once is noise.
- Inline success (green check) only when the validation was non-trivial (password rules, async uniqueness). Every-field success checkmarks become noise.
- On submit, if multiple fields fail: scroll to and focus the first failed field. Show an error summary above the form with links to each failed field (WCAG 2.2 SC 3.3.1 pattern).
- Use `aria-invalid` on invalid fields.
- Connect errors with `aria-describedby`.
- Announce blocking errors via `role="alert"` or `aria-live`.

## Error Display and Voice

Palette sets the **direction**; Prose writes the exact copy.

| Dimension | Direction |
|-----------|-----------|
| Blame | On the system / input constraint, not the user |
| Specificity | Name the field + the rule + the fix |
| Tone | Neutral and helpful, not apologetic or cheerful |
| Length | One sentence; never a paragraph |
| Recovery | Every error names the next action |

Direction examples (Palette → Prose):
- ❌ Palette says "Make it friendlier" → Prose writes "Oops! We need a valid email :)" (wrong — cheerful trivializes a block)
- ✅ Palette says "Specific + recovery" → Prose writes "Email must include a domain (e.g., name@example.com)."

Display rules:
- Keep field-level errors specific and actionable.
- Use an error summary when submit-time validation returns multiple errors.
- Provide recovery actions for non-field failures.

Preferred field-error pattern:

1. Identify the field or action
2. Explain what is wrong
3. Tell the user how to fix it

## Required-Field Indication

| Approach | When to use |
|----------|-------------|
| Mark required with `*` + legend "* required" | Form has mostly optional fields |
| Mark optional with "(optional)" | Form has mostly required fields (NN/g 2024: preferred pattern for short forms) |
| `aria-required="true"` + `required` attr on all required | Always, regardless of visual choice |
| No indication at all | ❌ Never — users cannot predict what will fail |

Do not rely on asterisk color alone — WCAG 1.4.1 (use of color) requires a non-color indicator. A red `*` next to the label is color + shape; the shape carries meaning.

## Progressive Disclosure

Hide fields that only apply to a subset of users. Reveal based on prior answers.

- Payment form: show "Billing address" fields only if user toggles "Billing differs from shipping."
- Profile form: show "Company name" only if user selects "Business account."
- Address form: show "State/Province" dynamically based on country selection.

Rules:
- Revealed fields must receive focus on reveal only if the user triggered it via an explicit toggle. Auto-revealed fields (from country change) should not steal focus.
- Never hide required fields behind unrelated toggles — users will not find them and will abandon.
- Conditional sections should animate in at ≤200ms with a `prefers-reduced-motion` fallback to instant.

## Multi-Step Forms

| Rule | Why |
|------|-----|
| Show progress (1 of 4, stepper, progress bar) | WCAG 2.2 SC 3.2.6 (consistent help); reduces abandonment |
| Save progress on each step | Browser refresh must not wipe the form |
| Allow back-navigation without losing data | Users need to verify prior entries |
| Summarize on final step before submit | "Review & submit" reduces error-correction round trips |
| Validate per step, not only at the end | Surface errors close to their origin |
| Keep steps to 3–5 when possible | 7+ steps signals "break into separate forms or save drafts" |

Use URL-based routing for steps (`/signup/step-2`) so back button, refresh, and link-sharing work.

Additional affordances:
- Use real labels; placeholder is not a label.
- Add helper text when the format is non-obvious.
- Use character counters only when limits matter.
- Use tooltips for optional help, not critical instructions.

## Defaults

- Prefer smart defaults when confidence is high.
- Make defaults easy to inspect and change.
- Never hide risky auto-filled values.

## Submission and Unsaved Changes

- Submit buttons need idle, loading, success, and error states.
- Disable duplicate submission while the request is active.
- Warn before discarding unsaved changes.
- For destructive form actions, prefer confirm or undo patterns.

## Autofill and Password-Manager Cooperation

Autofill failures are silent — users get a worse experience and you never see the error. Get this right.

- Use correct `autocomplete` attributes (WCAG 2.2 SC 1.3.5):
  - `autocomplete="email"`, `"name"`, `"given-name"`, `"family-name"`, `"tel"`, `"street-address"`, `"postal-code"`, `"country"`, `"cc-number"`, `"cc-exp"`, `"cc-csc"`.
- Login form: pair `autocomplete="username"` with `autocomplete="current-password"`. Signup: `"new-password"`.
- Never split a single logical input (phone, credit card) into 3–4 separate boxes — password managers can't fill them correctly.
- Use `inputmode` for correct mobile keyboard: `numeric`, `decimal`, `tel`, `email`, `url`, `search`.
- Use semantic `<input type="...">`: `email`, `tel`, `url`, `number`, `date` — password managers and autofill rely on type.
- Place `<label>` adjacent to `<input>` with matching `for`/`id`. Floating labels are fine but must also work for screen readers (use `<label>`, not placeholder-only).

```html
<label for="email">Email</label>
<input
  id="email"
  type="email"
  name="email"
  autocomplete="email"
  inputmode="email"
  required
  aria-describedby="email-help"
/>
<p id="email-help">We'll send a verification link.</p>
```

## Passkeys and Modern Authentication

Prefer passwordless flows when the platform supports them.

| Flow | Trigger | Notes |
|------|---------|-------|
| Passkey creation | registration or settings | use `navigator.credentials.create()` with WebAuthn |
| Passkey sign-in | login page | use `navigator.credentials.get()` with conditional UI |
| Magic link | fallback for unsupported devices | send to email, expire after single use |
| OTP fallback | SMS or TOTP app | add `autocomplete="one-time-code"` to the input |

Identifier-first flow: collect email or username on step 1, then determine the best credential method on step 2. Do not reveal whether an account exists during step 1 (prevents account enumeration).

WebAuthn Conditional UI (autofill-based passkey prompt):

```typescript
if (
  window.PublicKeyCredential &&
  PublicKeyCredential.isConditionalMediationAvailable
) {
  const available = await PublicKeyCredential.isConditionalMediationAvailable();
  if (available) {
    // Add autocomplete="username webauthn" to the username input
    // Then call get() with mediation: 'conditional'
    const credential = await navigator.credentials.get({
      publicKey: {
        challenge: serverChallenge,
        rpId: window.location.hostname,
        userVerification: 'preferred',
        allowCredentials: [],
      },
      mediation: 'conditional',
    });
  }
}
```

UX rules:

- Always offer a visible alternative (password or magic link) alongside passkeys.
- Do not block password-manager autofill — use standard `autocomplete` attributes.
- Show clear error messages when biometric verification fails, with a retry path.
- Never require the user to remember a passkey ID — device handles it.

## Accessible Authentication (WCAG 2.2 SC 3.3.8)

- Do not require cognitive function tests (memorized passwords, CAPTCHAs relying on recognition) as the only path. Offer passkeys, magic links, OAuth, or paste-from-password-manager.
- Never disable paste on password or 2FA fields — it blocks password managers and violates SC 3.3.8.
- 2FA code fields: one input with `inputmode="numeric"` and `autocomplete="one-time-code"` is preferred over 6 separate boxes.

## Anti-Patterns

- ❌ Validating every field on every keystroke — premature errors, noise.
- ❌ Generic error "Invalid input" with no pointer to which field or rule failed.
- ❌ Placeholder text replacing the label (`placeholder="Email"` with no `<label>`) — fails a11y and disappears on focus.
- ❌ Disabling submit until all fields are valid without telling the user why it's disabled.
- ❌ Clearing form fields after a submit error — users must retype everything. WCAG 2.2 SC 3.3.7 (redundant entry) explicitly addresses this.
- ❌ Splitting a 10-digit phone into three boxes (area / prefix / line) — breaks autofill.
- ❌ Disabling paste on password or 2FA fields — WCAG 2.2 SC 3.3.8 fail and password-manager-hostile.
- ❌ Asking for the same data twice across a multi-step flow (email → "confirm email") without a reason — SC 3.3.7 violation.
- ❌ Using `type="text"` for passwords without `autocomplete="current-password" / "new-password"` — blocks password managers.
- ❌ Red asterisk as the only required indicator — WCAG 1.4.1 (use of color) fail.

## Accessibility Checklist

- Labels and grouping are explicit.
- Errors are announced.
- Tab order is logical.
- Instructions remain visible.
- The form works with keyboard only.

## Handoff

- **→ Prose**: exact wording for every label, placeholder, help-text, error-message, success-toast, and submit-button verb. Palette provides the voice direction; Prose writes the strings.
- **→ Artisan**: production form library choice (React Hook Form / Formik / VeeValidate / Conform), schema (Zod / Yup / Valibot), server-error wiring, SSR-safe validation, dirty-state unsaved-changes dialog.
- **→ Flow**: error-shake animation, success-check motion, field-reveal easing, step-transition timing (respecting `prefers-reduced-motion`).
- **→ a11y recipe**: WCAG 2.2 SC 1.3.5 (autocomplete), 3.3.1 (error identification), 3.3.3 (error suggestion), 3.3.4 (error prevention), 3.3.7 (redundant entry), 3.3.8 (accessible authentication) conformance audit.
- **→ Voyager**: E2E tests for happy path, per-field validation, multi-step back/forward, autofill (Playwright's `page.fill` + autocomplete attribute coverage), password-manager compatibility.
