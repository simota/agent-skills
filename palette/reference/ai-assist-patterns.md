# AI-Assist UI Patterns

Purpose: UX patterns for AI-powered features including chat, inline suggestions, confidence indicators, and generative UI.

## Contents

- Streaming responses
- Confidence indicators
- Inline suggestions
- Generative UI
- Core principles

## Streaming Responses

Show tokens as they arrive rather than waiting for a complete response.

| Rule | Rationale |
|------|-----------|
| Begin rendering on first token | Reduces perceived latency significantly |
| Use a typing indicator before first token arrives | Signals that the model is working |
| Provide a stop button during streaming | Gives users control over long outputs |
| Scroll to new content incrementally | Keeps the user oriented during generation |

Skeleton placeholder before first token:

```css
.ai-response-placeholder {
  background: linear-gradient(90deg, var(--surface-2) 25%, var(--surface-3) 50%, var(--surface-2) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

Respect `prefers-reduced-motion`: replace the shimmer with a static placeholder when the user prefers reduced motion.

## Confidence Indicators

| Signal | Use it when | Avoid |
|--------|-------------|-------|
| Percentage label | the model has calibrated probabilities | showing raw logits |
| Hedging language ("may", "likely") | the answer is uncertain by nature | labeling confident answers as uncertain |
| Source citation | factual claims can be grounded | fabricating sources |
| Disclaimer footer | the domain requires professional judgement | hiding uncertainty on high-stakes advice |

Never display confidence as a precise decimal when the underlying probability is not calibrated. Prefer qualitative tiers: High / Medium / Low.

## Inline Suggestions

Patterns for ghost-text and autocomplete:

| Pattern | Trigger | Accept | Dismiss |
|---------|---------|--------|---------|
| Ghost text | pause in typing | `Tab` or `→` | continue typing |
| Inline menu | explicit shortcut | `Enter` | `Escape` |
| Multi-option picker | ambiguous context | arrow keys + `Enter` | `Escape` |

Rules:

- ghost text must be visually distinct from user input (muted color, italic, or opacity)
- do not auto-insert suggestions without a deliberate accept gesture
- announce suggestions via `aria-live="polite"` so screen readers can read them
- provide a keyboard shortcut to cycle through alternatives

```css
.ghost-text {
  color: var(--text-muted);
  opacity: 0.6;
  font-style: italic;
  pointer-events: none;
  user-select: none;
}
```

## Generative UI

When AI produces structured output that renders as interactive UI:

| Rule | Rationale |
|------|-----------|
| Validate AI-generated structure before rendering | Prevents broken or injected content |
| Provide a plain-text fallback | Ensures content reaches all users |
| Mark AI-generated content with a visible label | Maintains trust and transparency |
| Limit interactive affordances in generated UI | Reduces attack surface and confusion |
| Support undo or regeneration | Gives users recovery paths |

Sanitize any AI-generated HTML before injection:

```typescript
import DOMPurify from 'dompurify';

const safeHtml = DOMPurify.sanitize(aiGeneratedHtml, {
  ALLOWED_TAGS: ['p', 'strong', 'em', 'ul', 'ol', 'li', 'a', 'code', 'pre'],
  ALLOWED_ATTR: ['href', 'class'],
});
```

## Agentic AI Patterns

When AI acts autonomously on behalf of the user (booking, purchasing, filing, editing):

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| Intent Preview | Pre-action consent — show what the agent plans to do | "I'm about to [action]. Proceed / Edit / Handle it myself" |
| Explainable Rationale | Transparency during action | Show why the agent chose this path, with source references |
| Confidence Signal | Calibrated uncertainty display | High/Medium/Low tiers; never false precision |
| Action Audit & Undo | Post-action safety net | Timestamped log of all agent actions; one-click undo within window |
| Escalation Pathway | Human fallback | Clear route to human support when agent confidence is low or stakes are high |

Rules:

- Never perform irreversible actions without explicit Intent Preview and user confirmation
- Log every autonomous action to an audit trail accessible to the user
- Provide undo for all reversible agent actions within a reasonable time window
- Display a persistent indicator when an agent is acting autonomously (not just a one-time notification)
- Announce agent state changes via `aria-live` for screen reader users
- When confidence is below threshold, escalate to user rather than proceeding

Trust calibration: users arrive with skepticism from consumer AI failures (NN/g 2026). Earn trust incrementally — start with low-stakes actions, demonstrate reliability, then offer higher autonomy levels.

## Core Principles

1. **Transparency**: always make AI involvement visible to the user.
2. **Control**: never perform irreversible actions without explicit user confirmation.
3. **Recovery**: every AI-generated output must be editable, dismissable, or regenerable.
4. **Fallback**: when the model fails or is slow, degrade gracefully to the manual workflow.
5. **Accessibility**: streaming, ghost text, and generative UI must all work with keyboard and screen readers.
6. **Privacy**: do not send sensitive user data (PII, credentials) to external AI APIs without explicit consent.
