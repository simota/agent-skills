# Empty State Copy Reference

Purpose: Design zero-data UI copy that converts absence into forward momentum. Classifies empty states into three types (first-use / user-cleared / search-no-results) and produces copy that educates, celebrates, or redirects — never nihilistic "Nothing here".

## Scope Boundary

- **prose `empty-state`**: Zero-data UI copy design (this document).
- **prose `microcopy` (elsewhere)**: General UI copy (buttons, tooltips). Empty state is a deeper pattern carved out.
- **prose `onboarding` (elsewhere)**: First-run experience across multiple screens. Empty state is one piece inside onboarding.
- **prose `errors` (elsewhere)**: Failure-state copy. Empty state is not a failure.
- **Palette (elsewhere)**: Empty-state illustration / layout direction. Prose owns copy; Palette owns visual.

## Three-Type Classification

```
┌────────────────────┬──────────────────────────────────────────┬─────────────────────────┐
│ Type               │ Trigger                                  │ Emotional tone          │
├────────────────────┼──────────────────────────────────────────┼─────────────────────────┤
│ First-use          │ User has never populated this surface    │ Invitational, educational│
│ User-cleared       │ User completed/deleted all items         │ Celebratory, next-action │
│ Search-no-results  │ Filter/search returned zero items        │ Acknowledging, helpful   │
└────────────────────┴──────────────────────────────────────────┴─────────────────────────┘
```

## Pattern 1 — First-Use

User arrives, surface is blank. Goal: show value, invite action, lower start cost.

### Structure
1. **Hero line** (1 sentence, 6-12 words): name the benefit.
2. **Supporting line** (1 sentence, 10-20 words): explain *how* or *why*.
3. **Primary CTA** (2-4 words, imperative): start the first action.
4. **Secondary CTA** (optional): tutorial, sample data, import.

### Examples

| Surface | Hero | Support | Primary CTA | Secondary |
|---------|------|---------|-------------|-----------|
| Task list (new workspace) | "Turn plans into progress." | "Add your first task to see how it flows across columns." | Add task | Try sample board |
| Analytics dashboard | "Your numbers will live here." | "Connect a data source or install the tracking snippet to begin." | Connect source | Install snippet |
| Inbox | "All messages will appear here." | "Invite teammates or forward your first email to get started." | Invite team | Forward email |

### Anti-patterns

- ❌ "No items."
- ❌ "Oops, empty!"
- ❌ "You haven't done anything yet." (accusatory)
- ❌ "We didn't find anything." (correct for search, wrong here)

## Pattern 2 — User-Cleared

User has *completed* or *deleted* all items. Goal: celebrate, confirm, offer next action.

### Structure
1. **Affirmation** (1 sentence): acknowledge completion.
2. **Next action** (optional but recommended): suggest a useful follow-up.

### Examples

| Surface | Affirmation | Next Action |
|---------|------------|-------------|
| Inbox zero | "Inbox zero. Nice." | View archived · Set up filters |
| Task list (all done) | "All tasks complete. Enjoy the moment." | Start next sprint · Review what shipped |
| Notifications | "You're all caught up." | Configure preferences |

### Rules

- Celebrate briefly — do not over-praise (single short line is enough).
- Offer only *one* primary next action to avoid decision fatigue.
- Tone: warm, not corporate ("Nice." works; "Congratulations on your productivity achievement!" does not).

## Pattern 3 — Search-No-Results

Filter or search returned zero. Goal: acknowledge query, preserve trust, offer reformulation path.

### Structure
1. **Query echo** (include what they searched): "No results for *"{query}"*"
2. **Suggestion** (1-2 bullets): spelling, fewer filters, broader term.
3. **Fallback action** (optional): reset, browse all, contact support.

### Examples

| Query | Copy |
|-------|------|
| "wireless kebyoard" (typo) | "No results for *"wireless kebyoard"*.<br>Try: check spelling, use fewer words, or browse keyboards →" |
| Filters all applied, empty | "No items match your filters.<br>Remove a filter · Clear all" |
| Out-of-stock exact match | "No *"red small widget"* in stock.<br>See similar items · Notify me when available" |

### Rules

- **Always echo the query**. Users need to see that the system received their input. Missing echo feels like the system ignored them.
- **Suggest action, not self-flagellation**. "We couldn't find anything" → "No results for X. Try Y."
- **Never** show "0 results" as the only copy — always pair with suggestion or reset.

## Tone Calibration

| Context | Empty-state tone |
|---------|------------------|
| Consumer productivity | Playful, encouraging |
| Enterprise / B2B | Direct, task-oriented |
| Financial / health | Calm, factual |
| Marketplace | Solution-oriented, trust-preserving |
| Gaming / social | Celebratory, animated |

Follow the voice defined in `reference/voice-tone-framework.md`.

## Accessibility Notes

- Icon-only empty states are inaccessible. Always include text with sufficient heading hierarchy.
- If using illustration, pair with meaningful alt text or `role="img"` + `aria-label`.
- CTA buttons must have descriptive labels (not "Click here").
- Screen-reader announcement sequence: heading → explanation → CTA. Avoid CTA-before-context order.

## Implementation Notes

- **String key naming**: `emptyState.{surface}.{type}.{role}` (e.g., `emptyState.tasks.firstUse.hero`).
- **Translation**: avoid concatenation. Whole sentences only. Punctuation inside strings.
- **A/B testing**: label variants with `v1`, `v2` keys; emit `empty_state_viewed` + `empty_state_cta_clicked` events for Pulse.

## Output Template

```markdown
## Empty State Copy: [Surface]

### Type
[First-use / User-cleared / Search-no-results]

### Copy

| Role | Copy | Notes |
|------|------|-------|
| Hero | "[copy]" | Benefit-focused |
| Support | "[copy]" | How / why |
| Primary CTA | "[copy]" | 2-4 words, imperative |
| Secondary CTA | "[copy]" | Optional escape |
| A11y alt (if illustration) | "[alt text]" | Short, descriptive |

### Readability
- Flesch-Kincaid grade: [score]
- Target: 6-8 (consumer), 10-12 (enterprise)

### Variants (A/B)
- Variant A: [copy]
- Variant B: [copy]
- Metric to optimize: CTA click-through

### Implementation Notes
- String keys: [path]
- Telemetry: [event names]
- Handoff: Artisan (implementation) · Palette (visual direction) · Pulse (measurement)
```

## Anti-Pattern Ledger

| Anti-pattern | Why it fails | Fix |
|--------------|--------------|-----|
| "No data." | No value, no path forward | Replace with first-use hero + CTA |
| "You have no tasks yet." | Accusatory | "Add your first task to see it flow." |
| "Oops, nothing here." | Dismissive | Celebrate (cleared) or invite (first-use) |
| Long paragraph | Nobody reads walls of text | 2 lines max for hero + support |
| Illustration without alt text | Inaccessible | Always pair with a11y text |
| "Click here" | Unhelpful with screen readers | Verb + object, e.g., "Add task" |
| 4+ CTAs | Decision fatigue | 1 primary, 0-1 secondary |
| Corporate superlatives | Feels hollow | Natural, warm, concrete |

## Deliverable Contract

When `empty-state` completes, emit:

- **Type classification** (first-use / user-cleared / search-no-results).
- **Copy block** (hero, support, primary CTA, secondary CTA, a11y alt).
- **Readability score** (Flesch-Kincaid).
- **2-3 variants** for A/B testing where applicable.
- **String keys** and **translation notes** (no concatenation).
- **Telemetry events** for Pulse.
- **Handoffs**: Artisan (code), Palette (visual), Pulse (measurement), Polyglot (i18n).

## References

- UX Movement — "The 3 Types of Empty States"
- Nielsen Norman Group — "Beyond Blank Canvas: Three Types of Empty States"
- Shopify Polaris — Empty state patterns
- Material Design — Empty states
- Intercom — "The Dribbblisation of Design" (illustration + copy coupling)
