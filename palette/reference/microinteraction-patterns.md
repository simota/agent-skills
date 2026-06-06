# Microinteraction Patterns

Purpose: Choose the correct feedback state, loading pattern, notification, and destructive-action safeguard for a small UI interaction.

## Contents

- Button feedback
- Validation feedback
- Loading states
- Notifications
- Destructive actions
- Coding standards

## Button Feedback

Standard state progression:

`idle -> hover -> pressed -> loading -> success/error`

Use it for any async action that changes visible state.

## Validation Feedback

| Pattern | Use it for |
|---------|------------|
| Real-time | format validation |
| On-blur | most text entry |
| Submit-time | cross-field validation |

Always reflect invalid state with semantic attributes.

## Loading States

| Pattern | Use it when |
|---------|-------------|
| Skeleton | content structure is known |
| Spinner | short action-level waits |
| Progressive loading | large lists or staged content |
| Optimistic update | the failure rate is very low and rollback is natural |

## Notifications

| Type | Suggested behavior |
|------|--------------------|
| Success toast | auto-dismiss around `3s` |
| Error toast | longer visibility or manual dismiss |
| Undo toast | show for around `5s` with an action |

Use `aria-live="polite"` for non-urgent success or undo feedback.

## Destructive Actions

| Pattern | Use it when |
|---------|-------------|
| Confirmation dialog | the action is permanent or high-risk |
| Soft delete + undo | recovery is possible and safer for flow continuity |

If the action cannot be undone, state that explicitly.

## View Transitions API

Use the View Transitions API for same-document and cross-document page transitions.

| Type | When to use | Notes |
|------|-------------|-------|
| Same-document | SPA route changes, tab switches, list-to-detail | wrap state update in `document.startViewTransition()` |
| Cross-document | MPA navigation, full page loads | add `@view-transition { navigation: auto; }` in CSS |

Same-document transition:

```javascript
if (!document.startViewTransition) {
  updateDOM(); // fallback for unsupported browsers
  return;
}

document.startViewTransition(() => {
  updateDOM();
});
```

Named element transitions (for shared-element effect):

```css
.card-thumbnail {
  view-transition-name: card-thumbnail;
}

::view-transition-old(card-thumbnail),
::view-transition-new(card-thumbnail) {
  animation-duration: 300ms;
  animation-timing-function: ease-in-out;
}
```

Rules:

- always provide a non-transition fallback for unsupported browsers
- respect `prefers-reduced-motion` — skip or simplify animations when set
- keep transition duration under `400ms` for navigation, under `200ms` for micro interactions
- do not use view transitions as a substitute for loading state feedback

## Haptic Feedback (Web Vibration API)

Use haptic feedback to reinforce physical interaction on supported mobile devices.

```typescript
function vibrate(pattern: number | number[]): void {
  if ('vibrate' in navigator) {
    navigator.vibrate(pattern);
  }
}

// Single tap confirmation
vibrate(10);

// Error pattern
vibrate([50, 30, 50]);

// Success pattern
vibrate([20, 10, 20, 10, 40]);
```

| Interaction | Pattern | Duration |
|-------------|---------|----------|
| Button tap confirmation | single pulse | `10ms` |
| Destructive action warning | double pulse | `[50, 30, 50]` |
| Success completion | rising pattern | `[20, 10, 20, 10, 40]` |
| Error / rejection | sharp burst | `[80, 20, 80]` |

Rules:

- haptic is an enhancement, never required for task completion
- do not vibrate on passive scrolling or hover events
- keep patterns short — user attention spans for vibration are under `200ms` total
- no vibration API support in Safari on iOS; iOS system haptics are triggered through native APIs

## Coding Standards

- keep feedback immediate and stateful
- do not leave async actions visually silent
- avoid optimistic UI on high-risk operations
- expose recovery whenever the action is recoverable
