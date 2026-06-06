# Status and Progress Copy Reference

Purpose: Design status and progress microcopy for connection states (online / offline / syncing), save states (saving / saved / failed), and long-running tasks (progress, time remaining, cancel). Maps system states to calming, informative copy users can trust.

## Scope Boundary

- **prose `status`**: Connection / save / progress state copy (this document).
- **prose `microcopy` (elsewhere)**: General static UI copy.
- **prose `errors` (elsewhere)**: Failure recovery copy. Status copy shows *state*; errors explain *what went wrong*.
- **Flow (elsewhere)**: Loading spinner / skeleton animation. Prose owns the text; Flow owns the motion.
- **Beacon (elsewhere)**: Underlying health signals. Status copy *reflects* Beacon state; it does not define SLOs.

## State-to-Copy Mapping

### Save States

| State | Copy | Icon cue | Tone |
|-------|------|----------|------|
| Idle | (no text) | — | — |
| Typing / editing | "Unsaved changes" | dot indicator | calm |
| Saving | "Saving…" | spinner | calm |
| Saved | "Saved" (auto-hides after 2s) | check mark | confirming |
| Saved with timestamp | "Saved 2 min ago" | — | informative |
| Failed to save | "Couldn't save. Retry" | warning | actionable |
| Offline, queued | "Saved locally. Will sync when online" | cloud-offline | reassuring |

### Connection States

| State | Copy | Icon | Notes |
|-------|------|------|-------|
| Online | (no text; baseline) | — | default |
| Reconnecting | "Reconnecting…" | spinner | brief, auto-retries |
| Offline | "You're offline. Changes will sync when you reconnect." | cloud-offline | reassuring |
| Back online | "Reconnected. Syncing your changes…" | cloud + spinner | auto-dismiss after sync |
| Sync complete | "Up to date" | check | auto-hide |
| Sync conflict | "Changes conflict. Review to resolve." | warning | opens conflict resolution |

### Long-Running Task Progress

| Phase | Copy | Elements |
|-------|------|----------|
| Queued | "Waiting to start…" | spinner |
| Running (progress known) | "Uploading 45 of 120 files" + [====---] 45% | progress bar + count |
| Running (progress unknown) | "Processing your video…" | indeterminate spinner |
| Slow | (if > 10s) "This is taking longer than usual…" | no panic, no blame |
| Time estimate | "About 3 minutes remaining" | show only if confident (± 50%) |
| Near complete | "Almost done…" | 90%+ progress |
| Complete | "Done." + success action | check, clear CTA |
| Failed | "Upload failed. Try again." | error, retry button |
| Cancelled | "Upload cancelled" | neutral |

## Writing Principles

### 1. Show the present tense

- ✅ "Saving…" (currently happening)
- ❌ "Save is being processed" (passive, distant)

### 2. Use sentence case

- ✅ "Saved"
- ❌ "SAVED"
- ❌ "Saved!!!"

### 3. Avoid blame

- ✅ "Couldn't save. Retry"
- ❌ "You failed to save"
- ❌ "Network error. Contact admin."

### 4. Trim the "..." when the spinner already indicates motion

- "Saving" with spinner = clear
- "Saving…" with spinner = redundant but common; acceptable

### 5. Prefer concrete progress over percentages alone

- ✅ "Uploading 12 of 30 files (45%)"
- ❌ "45% complete" (45% of what?)

### 6. Show time remaining only when confident

- ✅ "About 2 minutes remaining" (if estimate within ± 50%)
- ❌ "4 minutes 13 seconds remaining" (false precision)
- ❌ Time remaining that jumps around wildly — omit instead

### 7. Offer cancel for long tasks

- Any task > 5s should allow cancel.
- Cancel button copy: "Cancel" (not "Abort", not "Stop").

## Accessibility Notes

- Wire save-state changes to `aria-live="polite"` region so screen readers announce "Saved" without interrupting.
- Progress bars need `role="progressbar"` + `aria-valuenow` / `aria-valuemax`.
- Indeterminate progress: `aria-busy="true"` + status text.
- Never rely on color alone (green check / red X) — always include text.
- For long tasks, announce only at meaningful milestones (0%, 50%, 100%) to avoid SR spam.

## Offline-First Pattern

Users disconnect constantly (subway, airplane, bad Wi-Fi). Copy should reassure:

```
[Editing] → [Offline detected]
          ↓
          "You're offline. Changes save locally."
          ↓
[Reconnected] → "Reconnected. Syncing your changes…"
             ↓
             (success) → "Up to date"
             (conflict) → "Changes conflict. Review to resolve."
```

Anti-pattern: showing a blocking modal "No internet connection" that prevents typing. This frustrates users who understand they're offline and just want to keep working.

## Connection Indicator Placement

| Prominence | Use case |
|------------|----------|
| Status bar (persistent, subtle) | Long-running editor with save state |
| Toast (ephemeral) | Transitions: "Reconnected", "Synced" |
| Banner (persistent) | Critical interruption requiring user awareness |
| Modal | Only for unrecoverable loss — e.g., "Session expired, reload" |

Default to subtle. Escalate only when user action is required.

## Save State Timing Rules

- **Debounce save**: trigger save after 500-1500ms of inactivity to avoid excessive requests.
- **Optimistic UI**: show "Saved" immediately on user action; show "Syncing…" for backend confirmation if network-dependent.
- **Auto-hide "Saved"**: 2 seconds is standard. Too short = user misses it; too long = clutter.
- **Retry invisibly first**: if save fails, retry once silently before showing an error.
- **Surface hard failures**: after 2 failed retries, show a visible "Couldn't save" with action.

## Progress Copy by Task Length

| Task length | Pattern |
|------------|---------|
| < 200ms | No feedback (feels instant) |
| 200ms - 1s | Subtle loading indicator (spinner) |
| 1s - 5s | Spinner + task name ("Loading your dashboard") |
| 5s - 30s | Progress bar + text ("Processing 45% complete") |
| 30s - 5min | Full progress + cancel + time estimate (if confident) |
| > 5min | Async pattern: allow user to leave, notify on completion |

Never block user's ability to navigate for tasks > 30s.

## Output Template

```markdown
## Status & Progress Copy: [Feature]

### States Identified
| State | Trigger | Copy | Icon | A11y announcement |
|-------|---------|------|------|-------------------|
| saving | user stops typing 500ms | "Saving…" | spinner | "Saving" |
| saved | server confirms | "Saved" | check | "Saved" |
| offline | network lost | "Offline. Changes save locally." | cloud-offline | "Offline, changes saved locally" |
| failed | server error | "Couldn't save. Retry" | warning | "Save failed. Retry button available." |

### Timing
- Debounce: [ms]
- Auto-hide "saved": [ms]
- Retry budget before showing error: [count]

### Long Task Pattern (if applicable)
- Task: [name]
- Expected duration: [range]
- Progress format: [concrete count / percentage / indeterminate]
- Time estimate: [shown / hidden]
- Cancel affordance: [required if > 5s]

### Connection Handling
- Offline copy: "..."
- Reconnecting copy: "..."
- Sync conflict copy: "..."
- Banner vs toast vs modal rationale: [notes]

### A11y Integration
- `aria-live` region: [polite / assertive]
- Progress bar markup: [role/aria-valuenow/aria-valuemax]
- Milestone announcements: [which %]

### Handoffs
- Artisan (implementation)
- Flow (spinner / motion)
- Polyglot (i18n)
- Beacon (underlying health signals)
```

## Anti-Patterns

| Anti-pattern | Why | Fix |
|--------------|-----|-----|
| "Error: Save failed due to error code E_NETWORK_002" | Blames user, shows internal codes | "Couldn't save. Retry" |
| "Loading..." for 10+ seconds with no progress | User thinks app is frozen | Show concrete progress + cancel |
| "Saved!" with exclamation | Overly enthusiastic for routine action | "Saved" (no punctuation) |
| "Saving..." that never disappears | Stuck state | Add timeout + error handling |
| Time estimate that jumps 10min → 30s → 5min | Worse than silence | Show only when stable |
| Blocking modal "No internet" | Prevents work | Subtle indicator + offline mode |
| "Sync error occurred" | Vague | "Couldn't sync. Check your connection." |
| No cancel for long task | User feels trapped | Cancel button for anything > 5s |
| Flashing / blinking status | Distracting | Subtle color + icon |
| Time shown as "4 min 13 sec 247 ms" | False precision | "About 4 minutes remaining" |

## Deliverable Contract

When `status` completes, emit:

- **State map** (all states from idle → error) with copy, icon, a11y.
- **Timing rules** (debounce, auto-hide, retry budget).
- **Long-task pattern** if applicable (progress format, estimate visibility, cancel).
- **Connection handling** (offline / reconnecting / conflict copy).
- **A11y integration plan** (aria-live, progressbar markup).
- **Handoffs**: Artisan, Flow, Polyglot, Beacon.

## References

- Apple HIG — Feedback, Progress indicators
- Material Design — Progress indicators, snackbars
- Jakob Nielsen — "Response Times: The 3 Important Limits" (0.1s / 1s / 10s thresholds)
- Web Content Accessibility Guidelines (WCAG) 2.2 — Status messages (SC 4.1.3)
- Google Material — Save state and connection patterns
- Adam Fields — "Save Early, Save Often" (save state design)
- Offline-first / PWA patterns — Google web.dev
