# WCAG 2.2 and Inclusive Design

Purpose: Capture WCAG 2.2 additions, common accessibility violations, and inclusive-design rules that Palette should apply on top of WCAG 2.1 AA.

## Contents

- WCAG 2.2 additions
- AV anti-patterns
- Semantic HTML first
- Focus management
- Accessible authentication
- Reduced motion and inclusion

## WCAG 2.2 Additions

| Level | Criterion | Practical impact |
|-------|-----------|------------------|
| A | `2.4.11` Focus Not Obscured (Minimum) | sticky UI must not fully hide the focused element |
| A | `3.2.6` Consistent Help | help access stays in a predictable place |
| A | `3.3.7` Redundant Entry | do not force the same information twice in one session |
| AA | `2.4.12` Focus Not Obscured (Enhanced) | focused elements should stay fully visible |
| AA | `2.4.13` Focus Appearance | focus indicator must be visible and sufficiently strong |
| AA | `2.5.7` Dragging Movements | provide non-drag alternatives |
| AA | `2.5.8` Target Size (Minimum) | tap target minimum `24x24px` |
| AA | `3.3.8` Accessible Authentication (Minimum) | do not require cognitive tests |
| AA | `3.3.9` Accessible Authentication (Enhanced) | support password managers and equivalent aids |

## AV Anti-Patterns

| ID | Anti-pattern | Fix |
|----|--------------|-----|
| `AV-01` | div-as-button | use `<button>` |
| `AV-02` | placeholder-only labels | add persistent labels |
| `AV-03` | color-only error state | add text or icons |
| `AV-04` | sticky UI obscures focus | add `scroll-padding` and focus visibility handling |
| `AV-05` | drag-only interaction | add button or keyboard alternative |
| `AV-06` | ARIA overuse | prefer semantic HTML first |
| `AV-07` | small touch targets | enforce `24x24px` minimum, `44x44px` preferred |
| `AV-08` | overlay-widget dependency | fix the product code itself |

## Semantic HTML First

Decision ladder:

1. use native HTML if it already matches the interaction
2. use accessible primitives when custom widgets are needed
3. use manual ARIA only when native semantics cannot express the pattern

## Focus Management

- protect focused elements from sticky-header overlap
- maintain clear `:focus-visible` styling
- support keyboard alternatives for drag and reorder interactions
- avoid redundant entry across multi-step forms

## Accessible Authentication

Avoid:

- text or puzzle CAPTCHA
- blocking password-manager paste
- OTP flows that require manual entry only

Prefer:

- passkeys or WebAuthn
- magic links
- password-manager-compatible autocomplete
- `autocomplete="one-time-code"` for OTP

## Reduced Motion And Inclusion

- respect `prefers-reduced-motion`
- pause auto-motion by default for reduced-motion users
- keep inclusive alternatives for animation-heavy or drag-heavy interactions

## WCAG 3.0 Roadmap (2025-2026)

| Item | Status |
|------|--------|
| Working Draft published | September 2025 |
| WCAG 3 timeline plan | Target April 2026 |
| Candidate Recommendation | Expected Q4 2027 |
| W3C Recommendation | No earlier than 2028 |

Conformance model change:
- Bronze: roughly equivalent to WCAG 2.2 AA (current compliance baseline)
- Silver: holistic testing required (assistive technology + usability testing)
- Gold: highest standard

Current legal baseline remains WCAG 2.2 AA. Do not design for WCAG 3.0 compliance yet — treat it as a strategic signal only.

### WCAG 3.0 Scoring System Preview

WCAG 3.0 replaces binary Pass/Fail with a 0-4 scale per outcome:

| Score | Meaning |
|-------|---------|
| 0 | Very poor — critical barriers |
| 1 | Poor — significant barriers |
| 2 | Fair — noticeable barriers |
| 3 | Good — minor barriers |
| 4 | Excellent — no detectable barriers |

**Tier definitions**:
- **Bronze**: Minimum scores across all critical outcomes (≈ current AA). Required for legal compliance.
- **Silver**: Higher minimum scores + usability testing with disabled users. Expands cognitive disability coverage.
- **Gold**: Highest scores + comprehensive user testing. Covers non-literal language, complex interaction patterns.

**Design implications**:
- Cognitive accessibility becomes a first-class requirement (not optional AAA).
- Scoring incentivizes incremental improvement over binary compliance.
- Plan for Silver-readiness in new designs — Bronze will be the bare minimum.

### Popover API Accessibility Patterns

The native Popover API eliminates most manual ARIA for non-modal overlays:

```html
<button popovertarget="info">More info</button>
<div id="info" popover>
  <!-- Auto: light dismiss, focus management, top layer, ESC to close -->
</div>
```

- **Replaces**: Custom `aria-expanded`, `aria-controls`, focus trap, click-outside handlers.
- **Rule**: Use `popover` for non-modal content (tooltips, menus, info panels). Use `<dialog>` for modal content.
- **Focus**: Browser handles focus return to trigger on close. No manual `focus()` needed.

### Calm UI Evaluation Framework

Evaluate interfaces for cognitive clarity using these axes:

| Axis | Metric | Target |
|------|--------|--------|
| Information Density | Content elements per viewport | ≤7 primary items (craft default, not Miller's Law — see note) |
| Visual Noise | Decorative vs functional elements ratio | ≥80% functional |
| Operation Steps | Clicks/taps to complete primary task | ≤3 for core flows |
| Attention Load | Competing CTAs per viewport | 1 primary, ≤1 secondary |
| Animation Load | Simultaneous motion elements | ≤2 per viewport |

**Red flags**: Auto-playing carousels, notification badges on >3 items, competing urgency signals, decorative parallax on mobile.

> **Density target caveat.** The ≤7 figure is a craft default, not a research finding. Miller
> measured recall span and Cowan revised it down to ~4; neither bounds how many options may be
> visible on screen, because a visible list is recognition, not recall
> (`_common/PROPORTION_AND_SPACING.md` § Cognitive-capacity numbers). Density is legitimately
> higher for expert monitoring and comparison surfaces when columns, units, freshness, and a
> keyboard path are stable. Never fail a dense dashboard on the count alone — fail it on scanning
> cost, unstable ordering, or missing hierarchy.


---

## WCAG 3.0 Preview (SKILL.md excerpt)

- wcag3_preview: WCAG 3.0 awareness (0-4 scoring system, Bronze/Silver/Gold tiers, cognitive disability expansion — finalization 2028+, not yet a compliance target but informs design decisions; APCA contrast was removed from the WCAG 3.0 draft in July 2023 — continue to use WCAG 2.2 AA contrast targets)


## Litigation Trends (SKILL.md excerpt)

- Digital accessibility litigation is accelerating — 5,000+ lawsuits filed in 2025 (~20% increase over 2024), with demand letter settlements $1K–$25K and court judgments averaging $75K (UsableNet 2026).

## Component-Level Remediation (SKILL.md excerpt)

- Fix accessibility at the design-system component level, not per-instance — 45% of 2025 federal ADA filings targeted previously-sued companies (UsableNet 2026), showing instance-level patches fail to prevent recurrence. Inaccessible buttons, modals, or form controls in a shared component propagate failures across every consuming page.

## Overlay Tools Are Not Remediation (SKILL.md excerpt)

- Never rely on accessibility overlay tools as a substitute for genuine remediation — FTC settled with accessiBe for $1M (April 2025) over misleading compliance claims; 22.6% of H1 2025 ADA lawsuits (456 cases) targeted sites with overlays installed, as overlays signal awareness of obligations while failing to remediate (Accessibility.build 2026).

## Trigger Detail (SKILL.md excerpt)

- Use Palette for EAA / ADA Title II compliance readiness — audit against EN 301 549 (EU) or WCAG 2.1 AA (US federal) and identify gaps before enforcement deadlines. eCommerce faces highest litigation risk (70% of 2025 ADA lawsuits targeted e-commerce; UsableNet 2025).

- Use Palette for agentic AI interface review — evaluate Intent Preview (pre-action consent), Explainable Rationale, Confidence Signals, Action Audit & Undo, and Escalation Pathways for autonomous agent UIs (Smashing Magazine 2026).

- Use Palette for WCAG 3.0 readiness assessment — evaluate current conformance against the Bronze/Silver/Gold tiered scoring model in the WCAG 3.0 Working Draft (substantially complete draft early 2026; final Recommendation expected 2028–2030). Note: APCA contrast was removed from the WCAG 3.0 draft as of July 2023 and is not present in subsequent drafts; continue to use WCAG 2.2 AA contrast ratios (4.5:1 normal text / 3:1 large text or UI components) as the actionable target. [Source: W3C — W3C Accessibility Guidelines (WCAG) 3.0, Working Draft (https://www.w3.org/TR/wcag-3.0/)]
