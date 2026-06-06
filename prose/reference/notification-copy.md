# Notification Copy Reference

Purpose: Design push, email, in-app, and SMS notification copy with channel-specific length budgets, tone rules, and CTA patterns. Each channel has distinct constraints; one notification copy does not fit all channels.

## Scope Boundary

- **prose `notification`**: Channel-specific notification copy (this document).
- **prose `microcopy` (elsewhere)**: Static UI copy. Notifications are transactional/triggered.
- **prose `errors` (elsewhere)**: Failure messages inside the UI. Notifications can be error-adjacent (e.g., "payment failed") but use the notification format.
- **relay (elsewhere)**: Messaging integration and delivery infrastructure. Prose owns copy; relay owns transport.
- **Bond (elsewhere)**: Re-engagement campaign *strategy*. Prose writes the copy; Bond decides who/when/what.

## Channel Length Budgets

| Channel | Primary | Secondary | Hard Limit |
|---------|---------|-----------|-----------|
| iOS push | Title ≤ 50 chars | Body ≤ 120 chars (lock screen truncates at ~60) | 178 chars combined |
| Android push | Title ≤ 50 chars | Body ≤ 120 chars | System varies; 240 combined is safe |
| Web push | Title ≤ 50 chars | Body ≤ 120 chars | Browser-dependent |
| Email subject | ≤ 50 chars (mobile inbox cuts at ~40) | — | Gmail truncates at ~70 on desktop |
| Email preheader | ≤ 100 chars (shown after subject) | — | Do not duplicate subject |
| Email body | Fit the ask above the fold | — | No hard cap; concise wins |
| In-app (toast / banner) | Body ≤ 160 chars | Optional CTA ≤ 24 chars | 160 preferred |
| In-app (modal) | Headline ≤ 60 chars | Body ≤ 2 paragraphs | Respect a11y focus |
| SMS | Message ≤ 160 chars (incl. opt-out) | — | Multi-part SMS costs more; avoid |

## Copy Structure Per Channel

### Push (iOS / Android / Web)

```
TITLE  : [subject — who/what happened]
BODY   : [value to user — why they should tap]
DEEPLINK: [exact screen / resource ID]
```

Rules:
- Title should stand alone on lock screen (user may not expand).
- Body adds value, not repetition: "Order delivered" / "Open to rate"  — not "Your order delivered. Your order was delivered".
- Never fake urgency (no "⚠️ URGENT" for non-urgent things).
- Use emoji sparingly; at most one, at position-0, only if brand-voice allows.

### Email

```
SUBJECT   : [benefit or clear action]
PREHEADER : [context that earns the open]
HEADER    : [headline matching subject]
BODY      : [single ask, one paragraph]
CTA       : [button text + URL]
FOOTER    : [unsubscribe, legal]
```

Rules:
- **Subject + preheader act as a pair** — preheader extends the subject, does not repeat it.
- One primary CTA above the fold. Secondary actions as text links.
- First 40 chars of subject are the most-seen real estate.
- Avoid all-caps and excessive punctuation (spam triggers).
- Identify sender clearly (brand name, not just "no-reply").

### In-App (toast / banner / modal)

```
TITLE (optional) : [verb-led outcome]
BODY             : [one sentence of context]
PRIMARY CTA      : [2-4 words]
DISMISS          : ["Dismiss" or "X" — always available]
```

Rules:
- Never block the user's primary task with a modal unless critical.
- Toasts auto-dismiss (5s default); do not hide critical info in toasts.
- Destructive / one-way actions need modal confirmation, not toast.

### SMS

```
MESSAGE: [BrandName] [short value + action]. [Reply STOP to opt out.]
```

Rules:
- Include brand identifier (carrier trust).
- Include opt-out phrase when regulated (TCPA, CASL, CAN-SPAM).
- Never send marketing SMS without prior consent.
- Short codes require pre-registration; long codes are more flexible.

## Notification Types

| Type | Example | Channel priority |
|------|---------|------------------|
| Transactional (user acted) | "Order shipped" | push + email + in-app |
| Social (someone acted toward user) | "Alice mentioned you" | push + in-app |
| System (state change) | "Trial ends in 3 days" | email + in-app banner |
| Re-engagement | "Haven't seen you in a while" | email (pull back), in-app (returning user) |
| Critical (security, billing) | "Password changed", "Payment failed" | email + push + in-app; SMS if severe |
| Summary / digest | "Your weekly summary" | email only |

Channel selection rules:
- High-urgency + short info → push.
- Medium-urgency + needs context → email.
- In-session acknowledgment → in-app toast.
- Critical compliance → multi-channel.

## Voice and Tone

| Context | Tone |
|---------|------|
| Transactional confirmation | Warm, concrete ("Order #1234 is on its way") |
| Social | Conversational, human ("Alice gave your post a high-five") |
| System / billing | Calm, direct ("Your trial ends on Friday") |
| Critical security | Unambiguous, actionable ("Your password was changed. Not you? Tap to secure.") |
| Re-engagement | Inviting, low-pressure ("Come back to see what's new") |
| Marketing | Respectful of the opt-in ("A 20% code, because you're a member") |

Follow `reference/voice-tone-framework.md` for brand-level voice.

## Deeplink Contract

Every push notification should carry a deeplink so tapping opens the exact screen:

```json
{
  "notification": {
    "title": "Your order shipped",
    "body": "Order #1234 is on its way. Track it live."
  },
  "data": {
    "deeplink": "app://orders/1234/tracking",
    "type": "order_shipped",
    "order_id": "1234"
  }
}
```

Missing deeplink = tap drops user in home screen = low CTR.

## Accessibility Notes

- Push notifications should be concise — screen readers read them verbatim on unlock.
- Use plain language; no ambiguous abbreviations.
- For in-app toasts: wire to `aria-live="polite"` region for SR announcement.
- For critical alerts: use `aria-live="assertive"` *sparingly* (interrupts screen reader).
- Provide a visible dismiss affordance — do not rely on time-out alone for a11y.

## Opt-Out / Preferences

- Every channel must respect user preferences.
- First-time push permission prompt must have a pre-permission UI explaining value.
- Email unsubscribe = one-click (CAN-SPAM), accessible within 10 seconds.
- SMS opt-out = reply "STOP" (honored within 24h per TCPA).
- Never send further messages after opt-out.
- In-app notification center: allow user to set quiet hours, types, and frequency.

## Output Template

```markdown
## Notification Copy: [Event Name]

### Scenario
- **Trigger**: [what triggers this notification]
- **Recipient**: [persona / segment]
- **Urgency**: [critical / high / medium / low]
- **Channel(s) selected**: [push / email / in-app / SMS — with rationale]

### Copy per Channel

#### Push
- Title (≤50 chars): "..."
- Body (≤120 chars): "..."
- Deeplink: `app://...`

#### Email
- Subject (≤50 chars): "..."
- Preheader (≤100 chars): "..."
- Body paragraphs: [...]
- Primary CTA: "..." → `https://...`

#### In-app
- Style: [toast / banner / modal]
- Title (optional): "..."
- Body (≤160 chars): "..."
- Primary CTA: "..."

#### SMS (if applicable)
- Message (≤160 chars incl. opt-out): "[Brand] ... Reply STOP to opt out."

### Tone & Voice
- Selected tone: [see voice-tone-framework]
- Rationale: [why this tone for this message]

### Telemetry (Pulse)
- Event: `notification_sent` / `notification_opened` / `notification_dismissed`
- Payload: channel, type, deeplink destination, user segment

### Compliance Check
- [ ] Opt-in verified
- [ ] Opt-out copy present (SMS / marketing email)
- [ ] Quiet hours respected
- [ ] Regional compliance (TCPA, CAN-SPAM, GDPR, CASL)

### Handoffs
- relay (delivery infrastructure)
- Polyglot (i18n)
- Pulse (open / CTR measurement)
- Bond (campaign strategy)
- Cloak / Oath (regulated channels)
```

## Anti-Patterns

| Anti-pattern | Why | Fix |
|--------------|-----|-----|
| "🚨 URGENT" on everything | Habituation, distrust | Reserve for true urgency |
| Marketing push without opt-in | TCPA / app-store violation | Require explicit opt-in |
| Email subject = preheader | Wastes real estate | Preheader extends subject |
| Push without deeplink | User lands on home, drops off | Always deeplink |
| SMS without opt-out | Regulatory violation | Include "Reply STOP" |
| Same copy across channels | Ignores channel constraints | Rewrite per channel |
| No sender identity on SMS | Carrier spam filter | Start with "[Brand]" |
| All-caps subject | Spam filter | Title case |
| "no-reply@" as sender | Lowers open rate, blocks replies | Use a monitored address or clear brand name |
| Push waking user at 3 AM | Lost trust | Respect timezone + quiet hours |

## Deliverable Contract

When `notification` completes, emit:

- **Channel selection** with rationale per type and urgency.
- **Per-channel copy block** respecting length budgets.
- **Deeplink** (for push) and **URL** (for email) pointing to exact resource.
- **Tone alignment** with voice framework.
- **Telemetry plan** (Pulse events).
- **Compliance checklist** (opt-in / opt-out / quiet hours / regional law).
- **Handoffs**: relay, Polyglot, Pulse, Bond, Cloak/Oath.

## References

- Apple HIG — Notifications
- Material Design — Notifications
- CAN-SPAM / TCPA / CASL / GDPR / ePrivacy — opt-in and opt-out law
- Intercom — "The Rules of Re-engagement" (notification cadence)
- Airship / Braze / OneSignal — push notification best practices
- Mailchimp / Litmus — email subject line and preheader studies
