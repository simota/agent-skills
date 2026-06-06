# Loading States

## Purpose

Loading is not waiting — it's a designed experience. The right loading state turns latency into trust, the wrong one turns 800ms into "is it broken?" This reference defines latency bands, skeleton vs spinner vs shimmer choices, optimistic UI, perceived-speed tactics, and the async-state handoff to error and empty.

## Scope Boundary

- IN scope: latency-band strategy, skeleton / spinner / progress / shimmer / shimmer-vs-skeleton, optimistic UI rules, perceived-speed tactics, partial loading, prefetch hints.
- OUT of scope: data-fetching architecture (delegate to `artisan`), animation timing curves and easing (delegate to `flow`), backend latency reduction (`bolt`), Core Web Vitals (`growth/vitals`), exact copy (`prose`).

## Core Concepts

### Latency Bands

The right loading treatment depends on actual duration. From research (Doherty, Nielsen, Bhatt):

| Band | Range | User Perception | Treatment |
|------|-------|-----------------|-----------|
| Instant | 0–100 ms | Direct manipulation; no UI needed | None |
| Fast | 100–400 ms | Slight delay tolerated | Subtle UI (button → loading) |
| Hesitation | 400–1,000 ms | Doubt sets in | Skeleton / inline spinner |
| Wait | 1–10 s | Active waiting | Skeleton with progress hint or spinner |
| Long | 10 s – 1 min | Need engagement | Determinate progress + status text |
| Background | > 1 min | Should not block | Notification when complete |

Match treatment to band. Spinner for 200ms = jarring flash. Spinner for 8s = "is this stuck?".

### Skeleton vs Spinner vs Shimmer

| Treatment | Best For |
|-----------|----------|
| Skeleton (gray boxes) | Predictable layouts where structure matters; reading-context (articles, profiles, lists) |
| Spinner | Indeterminate operations under 4s with no clear structure to preview |
| Progress bar (determinate) | Operations with measurable progress (uploads, downloads, multi-step) |
| Progress bar (indeterminate) | Sub-operations within a process with no structure preview |
| Shimmer effect | Scanning across skeleton — preferred over static gray; signals "loading", not "broken" |
| Inline spinner | Per-button or per-row local operations |
| No UI | < 100ms operations |

Skeleton + shimmer is the modern default for content-heavy pages. The user reads structure while content arrives.

### Optimistic UI

Apply the change immediately, send the mutation, roll back on failure:

| Apply Optimistic | Don't |
|------------------|-------|
| Likes, reactions, toggles | Payments |
| Reorders, moves | Deletes without undo |
| Form-field edits | Auth changes |
| Marking read / favorite | Anything irreversible |
| Soft-deletes (with undo toast) | Hard-deletes |

Pattern:

1. Update UI immediately.
2. Fire mutation.
3. On success: subtle confirmation (toast or icon).
4. On failure: roll back with explicit error toast + retry.

Optimistic UI is **the** difference between feeling fast and being fast. Used appropriately, perceived speed jumps without backend changes.

### Skeleton Design

| Rule | Reason |
|------|--------|
| Skeleton matches actual layout | "Trust the placeholder" — disorienting if final layout differs |
| Skeleton boxes have realistic widths | Vary widths to signal sentence length, not all uniform |
| Don't over-skeleton | Page shells, headers, navigation — render statically |
| Limit skeleton items | 3–6 placeholders for lists, not 100; user gets the idea fast |
| Use system colors | Skeleton bg = `surface-variant` or `gray-200`; not pure black/white |
| Animate via shimmer | Static gray = "broken"; shimmer = "loading" |
| Respect `prefers-reduced-motion` | No shimmer animation when reduced-motion is set |

### Progressive Loading

Don't wait for everything. Render available chunks as they arrive:

| Order | Content |
|-------|---------|
| 1 | Layout shell (header, nav, sidebar) |
| 2 | Above-fold critical content |
| 3 | Below-fold lazy content |
| 4 | Off-screen / on-interaction |

Patterns:

- **React Suspense / streaming SSR** — yields HTML in chunks.
- **Stale-while-revalidate** — show cached, fetch fresh, swap silently.
- **Pagination / infinite scroll** — load N items, fetch more on intersection.
- **Cursor pagination over offset** — better for stable position during loads.

### Indicator Hierarchy on a Page

A page often has multiple loading regions. Avoid the "spinner soup":

| Level | Treatment |
|-------|-----------|
| Page-level (initial load) | Skeleton or top-of-page progress bar |
| Section-level (panel, card) | Skeleton matching the panel structure |
| Inline (per-row, per-button) | Inline spinner / disabled state |
| Global async (background sync) | Subtle top-corner indicator, non-blocking |

Two simultaneous spinners on one screen confuse — design hierarchy.

### Perceived-Speed Tactics

Without changing backend latency:

| Tactic | Lift |
|--------|------|
| Optimistic UI | Mutations feel instant |
| Skeleton with realistic shape | Reduces "wait" perception by ~30% (Bhatt 2018) |
| Progress text ("Uploading 2 of 5…") | Replaces uncertainty with structure |
| Pre-fetch on hover / focus | First click feels instant |
| Render LCP early; defer below-fold | Time-to-interactive feels lower |
| Stale-while-revalidate | Cached page renders, fresh data swaps |
| Skeleton during route transition | Prevents flash-of-blank |
| Disable button during submit | Prevents double-submit + signals action received |

### Long Operations (> 10s)

For uploads, exports, AI generations:

| Element | Purpose |
|---------|---------|
| Determinate progress | "65% — about 12 seconds remaining" |
| Status text | "Compressing video" → "Uploading" → "Processing" |
| Cancel button | User control; reduces frustration |
| Backgroundable | Allow user to leave and get notified |
| Recovery on disconnect | Resume rather than restart |

Never leave a > 10s operation as a bare spinner.

### Loading and Empty / Error Handoff

```
[loading state]
  ├── success → render content
  ├── empty   → empty-states.md (variant: post-load)
  └── error   → error-states.md (variant: server / network)
```

Each transition must be designed; don't ship loading and forget the empty / error siblings.

### Accessibility

- `aria-busy="true"` on the loading region; `aria-busy="false"` when done.
- `aria-live="polite"` for status announcements ("Loading projects" → "5 projects loaded").
- Maintain focus when content loads — don't reset to body.
- Skeleton: prefer `aria-hidden="true"` with a single live-region announcement instead of announcing every box.
- Don't trap users in a loading state with no cancel after 10s.
- Spinners should have accessible names ("Loading projects", not "Spinner").

### Mobile Considerations

- Skeleton on slow networks (3G simulation): show within 200ms; the wait will be longer than desktop.
- Pull-to-refresh: use the native gesture pattern; show progress inline.
- Battery: avoid animation-heavy shimmer on long lists; stop animation off-screen.
- Network status: pair offline indicator with queued mutations.

### Loading Without Latency

For genuinely instant operations, **never** add a fake spinner for "feel". 200ms artificial delays are condescending and detected by users.

## Workflow

1. **Measure actual latency** — p50 / p95 / p99 from RUM, not synthetic.
2. **Map each operation to a band** — instant / fast / hesitation / wait / long / background.
3. **Choose treatment** per operation — skeleton / spinner / progress / inline / none.
4. **Decide optimistic UI** — apply only to reversible low-stakes mutations.
5. **Design progressive loading** — what renders first, second, third.
6. **Resolve indicator hierarchy** — page / section / inline / global; no soup.
7. **Specify perceived-speed tactics** — pre-fetch, stale-while-revalidate, skeletons.
8. **Design long-operation UX** — progress / cancel / backgroundable / resumable.
9. **Pair with empty / error** — handoff transitions.
10. **Verify accessibility** — `aria-busy`, focus, motion preferences.
11. **Test on slow network** (3G simulator) — perception is most extreme there.

## Output Template

```yaml
loading_design:
  surface: "projects list page"
  measurements:
    p50_ms: 240
    p95_ms: 720
    p99_ms: 1850
  band: hesitation
  page_load:
    treatment: skeleton
    item_count_placeholders: 4
    shimmer: yes
    respects_reduced_motion: yes
    aria_busy: yes
    aria_live: "polite ('Loading projects' / 'X projects loaded')"
  optimistic_mutations:
    - mutation: toggle_favorite
      apply: optimistic
      rollback_on_error: yes
      confirmation: subtle_toast
    - mutation: rename_inline
      apply: optimistic
      rollback_on_error: yes
    - mutation: archive
      apply: optimistic_with_undo_toast
    - mutation: delete_permanent
      apply: never_optimistic   # destructive
  perceived_speed:
    prefetch_on_hover: yes
    stale_while_revalidate: yes
    route_transition_skeleton: yes
  long_operation:
    operation: "csv export"
    treatment: determinate_progress
    cancel: yes
    backgroundable: yes
    completion_notification: yes
  hierarchy:
    page_level: skeleton_with_shimmer
    section_level: section_skeleton
    inline_level: button_spinner_disabled
    global_async: top_corner_indicator
  handoff:
    to_empty: empty-states.md (post-load variant)
    to_error: error-states.md (server / network variant)
  mobile:
    skeleton_on_3g: yes
    pull_to_refresh: native_pattern
    animation_off_screen: paused
```

## Anti-Patterns

- Spinner for < 100ms operations — flash of UI; jarring.
- Spinner for > 4s operations with no progress — "is it stuck?".
- Skeleton that doesn't match final layout — disorienting jolt on swap.
- Multiple spinners simultaneously — soup; user can't tell what's loading.
- Optimistic UI on payments / deletes / auth changes — risk of false confirmation.
- Static gray skeleton boxes — read as broken state, not loading.
- Shimmer animation respecting nothing — fails `prefers-reduced-motion`.
- Top-of-page progress bar that runs to 90% in 200ms then sits forever — fake.
- Synthetic 1s loading delay "for trust" — condescending to users.
- "Loading…" text with no time / progress hint for > 5s operations — uncertainty.
- No cancel button for > 10s operations — user trapped.
- Long operation that resets on disconnect — wastes user effort.
- Page-load that doesn't show layout shell first — flash of blank.
- Pull-to-refresh without progress feedback — gesture feels broken.
- Loading state that doesn't transition to empty / error — dead-end on failure.
- Spinner with no accessible name — screen reader silence.
- Skeleton announcing every box to screen readers — noise.

## Deliverable Contract

A loading-state design is complete when:

- Latency measured at p50 / p95 / p99 (RUM, not synthetic).
- Operations mapped to bands.
- Treatment chosen per operation.
- Optimistic UI policy stated per mutation.
- Progressive loading order specified.
- Hierarchy resolved (page / section / inline / global).
- Perceived-speed tactics listed.
- Long-operation UX (> 10s) designed with progress / cancel / backgroundable.
- Empty-state and error-state handoff documented.
- Accessibility verified (aria-busy, aria-live, focus, reduced-motion).
- Mobile + slow-network behavior specified.
- No fake delays added for feel.

## References

- Walter Doherty & Ahrvind Thadani, *The Economic Value of Rapid Response Time* (IBM, 1982) — original 0.4s threshold.
- Jakob Nielsen, *Response Times: The 3 Important Limits* (NN/g, 1993) — 0.1s / 1.0s / 10s bands.
- Robert Miller, *Response time in man-computer conversational transactions* (1968) — earliest treatment.
- Vinay Bhatt, *Skeleton Screens vs. Spinners: A Quantitative Study* (2018).
- Material Design 3, *Progress indicators*.
- Apple HIG, *Progress indicators*.
- Luke Wroblewski, *Mobile First* — mobile loading patterns.
- W3C WAI-ARIA Authoring Practices, *Status / progressbar / live region*.
- React Suspense documentation — streaming SSR / progressive rendering.
- SWR / TanStack Query / Apollo — stale-while-revalidate library implementations.
- Addy Osmani, *Image Loading Best Practices* (web.dev) — visual loading priorities.
- Vercel & Linear engineering blogs — production optimistic-UI patterns.
- Brad Frost, *The Pace of Change* — loading and trust framing.
