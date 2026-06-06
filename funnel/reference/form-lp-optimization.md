# LP Form Optimization Reference

Purpose: Design LP-context forms that maximize completion without eroding lead quality. Every field is a conversion tax — quantify it, justify it, or cut it. This reference covers field minimization, progressive disclosure, autofill/password-manager cooperation, real-time validation, error-prevention patterns, and submit-button friction specifically for LPs (lead gen, signup, download, trial).

> **2026 traffic mix: passkey + AI agent flows are baseline.** Two shifts to factor into form design:
>
> 1. **Passkey-first signup** is now table-stakes for consumer LPs. Offer "Sign in with passkey" alongside email + password, prefer it for first-time creation when the platform supports it (`navigator.credentials` WebAuthn). Email-only fallback remains for cross-device portability.
> 2. **AI shopping / agent-driven flows** convert at higher rates than non-branded organic (ChatGPT referrals `~31%` higher in 2025–2026 retail data). Forms reached by an AI agent on the user's behalf must auto-fill cleanly from structured data the agent already has — that means the same machine-readable `autocomplete` + ARIA discipline as in the autofill section below, applied as a hard requirement rather than a nice-to-have.

## Scope Boundary

- **Funnel `form`**: LP form spec (field count, step split, validation strategy, submit-button value prop, autofill contract).
- **Artisan (elsewhere)**: React/Vue production implementation of the form, state management, network submission, error boundary integration.
- **Prose (elsewhere)**: exact field-label wording, error-message voice/tone, placeholder microcopy authored to the design system.
- **Growth (elsewhere)**: CRO experimentation on field count, cross-page form analytics, drop-off funnel instrumentation, exit-intent recovery.
- **Muse (elsewhere)**: input / label / error-state design tokens (spacing, radius, color, focus-ring).

If the question is "how many fields and in what order?" → `form`. If it's "what exact words go in the error?" → Prose. If it's "which framework component and how is state wired?" → Artisan.

## Field-Count Cost Model

Each field beyond the minimum incurs measurable conversion tax. Budget fields against the downstream value.

| Field count | Typical CV rate | Use when |
|-------------|----------------|----------|
| 1 (email only) | ~23% | Top-of-funnel: newsletter, guide download, waitlist |
| 2-3 | ~18% | Lead magnet with mild qualification (email + name, email + company) |
| 4-5 | ~13-15% | Qualified lead for sales handoff (email, name, company, role, team size) |
| 6+ | <10% | Strongly discourage. Split with progressive disclosure or move to post-conversion. |

**Rules:**

- Every field must answer "does the 20-30% CV penalty pay for itself downstream?" If the sales team ignores the field, cut it.
- Phone number is the single highest-friction standard field — ask only if sales calls are the follow-up motion.
- Never ask for data you can enrich (company size, industry, revenue) from Clearbit / ZoomInfo / BuiltWith on the email domain.
- Optional fields should be visually de-emphasized and labeled `(optional)` — unlabeled optionals are treated as required and abandoned.

## Progressive Disclosure: Single vs Multi-Step

| Pattern | Conversion profile | Pick when |
|---------|-------------------|-----------|
| Single-step (all fields visible) | Higher completion when ≤ 3 fields | Simple lead-gen, email-only, download gate |
| 2-step (email → details) | Higher completion when ≥ 4 fields; foot-in-the-door effect | Trial signup, demo request, qualified lead form |
| Multi-step (3+ steps with progress bar) | Higher qualified-lead rate when 5+ fields; feels lighter | Enterprise demo, onboarding-as-form, pricing calculator |

**2-step pattern (default for 4+ fields):**

```
Step 1: Email only ──► [Continue]
                       │
                       ▼
Step 2: Name, Company, Role ──► [Get my demo]
```

Why it works: Step 1 commitment captures a partial lead (recoverable via email) even if Step 2 is abandoned. Commitment-consistency bias raises Step 2 completion by 15-30%.

**Progress indicator rules:**

- Show progress only when ≥ 3 steps. For 2-step, omit — indicator adds cognitive cost.
- Label steps by meaning (`Your email` · `About you` · `Your team`), not numbers (`1 / 3`).
- Never hide the final step count — "just one more step" surprises erode trust.

## Autofill and Password-Manager Cooperation

LP forms must be machine-readable. Browsers and password managers complete forms 3-5× faster than typing; blocking them is a self-inflicted conversion wound.

**Required attributes:**

| Field | `autocomplete` | `inputmode` | `type` |
|-------|---------------|-------------|--------|
| Email | `email` | `email` | `email` |
| First name | `given-name` | `text` | `text` |
| Last name | `family-name` | `text` | `text` |
| Full name | `name` | `text` | `text` |
| Company | `organization` | `text` | `text` |
| Job title | `organization-title` | `text` | `text` |
| Phone | `tel` | `tel` | `tel` |
| Country | `country-name` | `text` | `text` |
| Postal code | `postal-code` | `numeric` | `text` |
| New password (signup) | `new-password` | — | `password` |
| Current password (login) | `current-password` | — | `password` |

**Password-manager cooperation:**

- Use standard `<label>` bound via `for` / `id` — custom label implementations (aria-only, floating divs) break 1Password / LastPass / Bitwarden detection.
- Never use a single `<input>` for email+password. Browsers cannot save credentials from non-standard forms.
- Signup forms with a password field: `autocomplete="new-password"` enables suggested-strong-password prompts. Using `off` here is a common anti-pattern that kills signup conversion.

## Real-Time Validation Strategy

Validate on blur, not on keystroke. Keystroke validation fires errors before the user finishes typing — experienced as nagging, not helpful.

| Validation moment | Use for | Why |
|------------------|---------|-----|
| On blur (field loses focus) | Format checks: email syntax, phone pattern, postal code | User completed intent, feedback is timely |
| On submit | Cross-field and server-side: password match, email uniqueness, captcha | Cannot be checked without full context or network |
| On keystroke | Only: password strength meter, character counter, live preview | Feedback is additive, not corrective |

**aria-invalid contract:**

- Set `aria-invalid="true"` only after the first blur-validation fails, not on initial render.
- Pair with `aria-describedby` pointing to the error element's `id`.
- Clear `aria-invalid` on next valid blur — do not wait until submit.

**Success-state feedback:**

- For non-obvious fields (password strength, username availability), show inline success (checkmark + "Available") within 400ms.
- Never show success on trivial fields (email format) — confirms nothing the user doesn't already know.

## Error-Prevention Patterns

Prevent errors before they occur. The cheapest error message is the one never shown.

- **Constrain inputs at the source**: date pickers over free-text dates, country dropdowns over free-text, `<input type="number">` with `min`/`max` over post-hoc validation.
- **Smart defaults**: detect country from IP / browser locale, pre-fill to avoid the field entirely when acceptable.
- **Format hints inline** (not in placeholder): `Format: +81 90 1234 5678` beneath the label, visible while typing. Placeholder text disappears on focus and is lost.
- **Character counters** for free-text fields with limits: show remaining, not used (`120 characters remaining` beats `30 / 150`).
- **Forgiving parsing**: strip spaces from credit-card numbers, normalize phone formats server-side. Do not reject input the user clearly intended.

## Submit-Button Friction

The submit button is the last opportunity to reassure or lose the lead. Treat it as a value-prop micro-LP, not a UI control.

**Button copy:**

| Anti-pattern | Replacement | Why |
|--------------|-------------|-----|
| "Submit" | "Get my free guide" | Generic = assumes shared context. Specific = restates value. |
| "Sign up" | "Start my 14-day trial" | Commitment feels smaller when reversible / time-bounded is surfaced. |
| "Register" | "Reserve my seat" | Possession framing (`my`) outperforms neutral (`your` / none). |
| "Send" | "Request demo" | Action verb aligned to downstream flow, not form mechanics. |

**Button state contract:**

- Disabled state only when form is demonstrably invalid (post-blur, not on initial render). Pre-blur disabled buttons feel locked and cause rage-click.
- Loading state: swap text to "Submitting…" and show a spinner. Never leave the button silent during network latency — users re-click and create duplicates.
- Success state: button disappears or transforms into "✓ Sent — check your inbox". Do not rely only on a redirect.

**Friction around the button:**

- Privacy line beneath the button (+11% trust): `We never share your email. Unsubscribe anytime.`
- No secondary CTA adjacent ("Or continue with Google"). Dual CTAs split attention and drop primary CV by 10-15%. If SSO is required, stack it above with a divider, not beside.
- Never include a reset / clear button on LP forms. Users rage-click it by mistake and abandon.

## Anti-Patterns

- ❌ Asking for phone number when follow-up is email-only.
- ❌ Keystroke-level email validation firing "Invalid email" before the user finishes typing.
- ❌ `autocomplete="off"` on signup password fields (blocks password managers, kills completion).
- ❌ Submit button disabled on initial render with no indication of what is required.
- ❌ Red border + "Required" on every empty field at page load — treats the user as already wrong.
- ❌ CAPTCHA before the user has tried to submit (adds friction unconditionally; use only after abuse signals).
- ❌ Multi-step form without save-on-step-1 — a Step 2 abandon loses the lead entirely.
- ❌ "Please fill in all required fields" as the only error on a 6-field form — must point to the specific fields.
- ❌ Placeholder text as the only label (disappears on focus, WCAG-fail).
- ❌ Optional fields styled identically to required fields.

## Handoff

**To Artisan** (production build):

- Final field list with types, `autocomplete`, `inputmode`, required/optional, validation-moment spec.
- Step structure (single / 2-step / multi-step) with transition behavior.
- Submit-button copy, disabled-state contract, loading-state contract, success-state contract.
- Error-message pattern (inline vs summary, aria-invalid wiring, error `id` scheme).

**To Prose** (copy polish):

- Field labels, placeholder hints, error-message shells. Prose returns voice/tone-aligned final wording.

**To Growth** (experimentation):

- Baseline field count and completion rate. Growth owns A/B variants (field removal, step-split, button-copy variants) and statistical readout.

**To Muse** (tokens):

- Input states needed: default, focus, filled, invalid, disabled, loading. Muse returns spacing / radius / color / focus-ring tokens.
