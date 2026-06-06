# Empty States

## Purpose

An empty state is not nothing — it's the first thing many users see. Designed well, it teaches; designed poorly, it abandons. Every list, search, dashboard, and inbox needs four explicit empty variants and a deliberate next action.

## Scope Boundary

- IN scope: empty-state classification, illustration vs minimal choice, primary-action selection, onboarding cue vs invitation copy, post-clear and post-error variants.
- OUT of scope: exact copy (delegate to `prose`), illustration drawing (delegate to `ink`), first-time-user journey design (`vision` for full onboarding flow), loading state (`loading`), error state (`error`).

## Core Concepts

### Four Empty Variants

A single screen can have 4 distinct "empty" states. Designing only the first leaves the others looking broken.

| Variant | When | Goal |
|---------|------|------|
| First use | User has never created any data | Teach the value, drop one example, invite first action |
| Zero results | Search / filter returned nothing | Help refine; suggest alternatives |
| Post-clear | User intentionally deleted everything | Acknowledge; offer reset / undo / continue |
| Post-error | Load failed; collection couldn't be retrieved | Show retry; preserve mental model |

Common bug: shipping only first-use, leaving zero-results showing the same "Welcome!" copy.

### First-Use State Anatomy

| Element | Purpose |
|---------|---------|
| Visual (illustration / icon / spot graphic) | Friendly anchor; sets tone |
| Headline | Name the empty state in one short sentence |
| Body (1–2 lines) | Explain the value of filling it |
| Primary action | Most likely next step (button) |
| Secondary action | Alternative (templates, import, sample data) |
| Optional: video / tour link | For complex products only |

The primary action should be the **single most likely next step**, not a menu of options. If you offer 4 actions, you've designed a panic, not an entry point.

### Templates and Sample Data

Two strong patterns for first-use:

| Pattern | When |
|---------|------|
| One-tap template | Show 3–5 starter templates; one tap creates a populated record |
| Fill with sample data | Pre-populate the empty surface with example rows + an "Use my own data" toggle |

Templates dramatically reduce the empty-state cliff. Cold first-uses kill activation rates; pre-populated examples let users see what "full" looks like.

### Illustration vs Minimal

| Choice | When |
|--------|------|
| Illustration | Consumer products, low-density screens, brand-personality opportunity |
| Spot icon | Most B2B / SaaS — friendly without taking real estate |
| Text only | Dense data tools, technical products where illustrations feel patronizing |
| Pure data placeholder | Dashboards where structure communicates more than illustration |

If you choose illustration, it must:

- Reinforce the page's purpose (not generic "people working").
- Avoid stock-tropes (handshakes, lightbulbs, gears).
- Match the system's illustration language (consistent across all empties).
- Be accessible — alt text describes the illustration, not "decorative image".

### Zero-Results Anatomy

A search returning zero results is a **critical** moment — the user took action and got nothing. Failure modes:

| Failure | Fix |
|---------|-----|
| Generic "No results" with no help | Suggest spell-fix, related terms, broader category |
| Same illustration as first-use | Distinct empty state for "you searched, nothing matched" |
| No clear-filter button | Always offer to clear filters / reset search |
| No guess at what user meant | "Did you mean: ___ ?" |
| Promotes signup over resolving the search | Wrong moment for upsell |

Best practice: zero-results echoes the query ("No results for **rebar**") and offers concrete next steps (clear filters, broaden category, view trending, manual support).

### Post-Clear State

User cleared all items intentionally — different mental model from first-use:

- Don't repeat onboarding ("Welcome!" — they're not new).
- Acknowledge the action ("You've cleared all items.") and provide path forward (undo / restore / continue).
- If clearing is rare, offer a brief celebration ("Nice — inbox zero!").
- If clearing is frequent (e.g., trash empty), keep it minimal.

### Post-Error State

Load failed, list returned no data, user lost context:

- Don't show first-use copy — misleading.
- Show the error (see `error-states.md`) + retry affordance.
- Preserve filter / search state visually so user knows the load context.
- Avoid suggesting "create your first item" when the user already had items they cannot see.

### Copy Voice

| Tone | When |
|------|------|
| Encouraging | First-use ("Let's get started.") |
| Functional | Zero-results ("No results matching 'rebar'.") |
| Acknowledging | Post-clear ("All clear.") |
| Honest | Post-error ("We couldn't load this. Retry?") |

The voice shifts per variant. Identical copy across all four is a tell that nobody designed the four cases.

### Accessibility

- Decorative illustrations: `aria-hidden="true"` and let the headline carry meaning.
- Informative illustrations: meaningful `alt` text.
- Primary action: focusable, keyboard-reachable, with explicit label.
- For zero-results, `aria-live="polite"` announces the result count change.
- Don't lock the empty state into one viewport — long descriptions of templates need scrollable area.

### Mobile Considerations

- Compress illustrations on small screens; hero illustrations rarely earn the vertical space on mobile.
- Primary action at thumb zone; never hidden in a scroll-required area.
- Templates as horizontal scrollers if 3+; vertical stack if 1–2.
- Text size: keep empty-state copy at body scale; don't shrink for small screens.

### Empty State as Onboarding

For products where setup is the first session, the empty state IS the onboarding tutorial:

- First card is "Try it" — pre-populated.
- Second card is "Add your own".
- Third card is "Connect data source".
- Each card collapses after completion to reveal the next.

This pattern (Notion, Linear, Vercel) outperforms separate onboarding modals — the work happens in context.

### Anti-Pattern: The Cliff

The "empty cliff" — generic empty state with no clear next action — is the highest-impact UX failure on dashboards and lists. Sample of bad copy: "Nothing here yet." Period. End of state.

## Workflow

1. **Identify the surface** — list / dashboard / search / inbox / tag detail / etc.
2. **Enumerate the 4 variants** — first-use, zero-results, post-clear, post-error.
3. **Decide visual treatment** — illustration / spot icon / text only / data placeholder per variant.
4. **Compose the headline + body** for each variant.
5. **Pick the primary action** for first-use — single most likely next step.
6. **Add templates / sample-data** for first-use if activation is critical.
7. **Design zero-results recovery** — clear filters, related terms, broader category.
8. **Design post-clear acknowledgement** — undo / restore / next thing.
9. **Design post-error retry** — see `error-states.md`.
10. **Verify accessibility** — alt text, aria-live, keyboard reach, mobile thumb zone.
11. **Hand off illustration** to `ink` if needed; copy to `prose`.

## Output Template

```yaml
empty_state_design:
  surface: "projects list"
  variants:
    - id: first_use
      visual: illustration
      illustration_brief: "Hand placing a card on an empty board; warm tones; matches sibling illustrations"
      headline: "プロジェクトをはじめよう"
      body: "1つのプロジェクトに目標、メンバー、進捗をまとめて管理できます"
      primary_action:
        label: "新しいプロジェクトを作成"
        action: open_create_modal
      secondary_action:
        label: "テンプレートから選ぶ"
        action: open_template_gallery
      templates_count: 5
      sample_data_toggle: yes
    - id: zero_results
      visual: spot_icon
      headline: "「{query}」に一致するプロジェクトはありません"
      body: ""
      primary_action:
        label: "フィルターをクリア"
        action: clear_filters
      secondary_action:
        label: "全プロジェクトを表示"
        action: reset_search
      did_you_mean: yes
    - id: post_clear
      visual: text_only
      headline: "すべて整理されました"
      body: "新しいプロジェクトはいつでも作成できます"
      primary_action:
        label: "新規作成"
        action: open_create_modal
    - id: post_error
      visual: spot_icon
      handoff: error-states.md
      headline: "プロジェクトを読み込めませんでした"
      body: "通信を確認して再試行してください"
      primary_action:
        label: "再試行"
        action: retry_load
      secondary_action:
        label: "サポートに連絡"
        action: open_support
  a11y:
    illustration_alt: per_variant
    aria_live_zero_results: polite
    keyboard_reach_primary: yes
    mobile_thumb_zone: yes
  copy_handoff: prose
  illustration_handoff: ink
```

## Anti-Patterns

- A single empty state for all four variants — looks broken in three of them.
- Generic "Nothing here yet." with no next action — the cliff.
- Hero illustration on mobile dominating the viewport — pushes the action below fold.
- Stock-illustration tropes — handshakes, lightbulbs, gears, abstract networks.
- Multiple primary actions in first-use — paralysis.
- Zero-results state that promotes signup or upgrade — wrong moment.
- "Welcome!" copy on post-clear — user isn't new.
- "Get started" on post-error — user already started; load failed.
- No templates / no sample data when activation is critical — activation cliff.
- `alt=""` on illustrations that carry meaning.
- Templates as a 12-item grid — choice overload; cap at 5.
- Empty state that ignores the active filter — looks the same with or without filter applied.
- Empty state with no exit affordance from search / filter context.
- Illustration that doesn't match the system's other illustrations — visual incoherence.
- Onboarding video on first-use as the primary action — high-friction.
- Empty state as the only place users learn the product's value proposition — should be one of several teaching moments.

## Deliverable Contract

An empty-state design is complete when:

- All 4 variants designed (first-use, zero-results, post-clear, post-error).
- Each variant has visual treatment, headline, body, primary action.
- First-use has templates or sample-data path if activation is critical.
- Zero-results has clear-filters / broaden / suggest path.
- Post-error hands off to `error-states.md`.
- Accessibility documented (alt text policy, aria-live, keyboard reach).
- Mobile layout specified.
- Copy handed off to `prose`; illustrations to `ink` (if used).

## References

- Pavel Samsonov, *Empty States: 8 Examples and Best Practices* (UX Pickle, 2024).
- Therese Fessenden, *Empty States: 4 Reasons to Design Them* (NN/g, 2022).
- Lucia Cerchie, *State of Empty States* (Smashing Magazine, 2025).
- Material Design — *Empty states* pattern.
- Apple HIG — *Empty States*.
- Atlassian Design System — *Empty state component*.
- IBM Carbon — *Empty states pattern*.
- W3C WAI-ARIA Authoring Practices — *Live region* pattern for zero-results announcements.
- Linear, Notion, Vercel — production patterns for empty-as-onboarding.
- Andrew Chen, *The Cold Start Problem* — empty-state activation framing.
