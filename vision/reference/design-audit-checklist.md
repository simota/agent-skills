# Design Audit Checklist

Reference for Vision's `audit` recipe. REVIEW-mode design quality audit: Nielsen 10 heuristics, WCAG 2.2 AA pass/fail grid, token-drift detection, prioritized remediation backlog.

---

## 1. Audit Scope Definition

Before scoring, declare scope:

| Scope dimension | Options |
|---|---|
| Surface | marketing / product / docs / email / mobile / all |
| Pages | list specific URLs or screen names (≤ 10 for one audit cycle) |
| Component layers | tokens / primitives / patterns / templates |
| Audit depth | heuristic-only / + WCAG / + token-drift / + competitive |
| Output format | scorecard / remediation backlog / executive summary |

Cap one audit at ~10 surfaces / 90 minutes of evaluation. Larger scopes need batching.

---

## 2. Nielsen 10 Usability Heuristics

Score each surface 1-5 against:

| # | Heuristic | Pass signal | Fail signal |
|---|---|---|---|
| 1 | Visibility of system status | Loading / progress / save state visible | Silent operations, no spinners |
| 2 | Match between system and real world | Familiar terms, real-world metaphors | Jargon, system-centric labels |
| 3 | User control and freedom | Undo, cancel, back works | One-way actions, no escape |
| 4 | Consistency and standards | Same icons / colors mean same thing | Brand inconsistency across screens |
| 5 | Error prevention | Confirmations, constraints, validation | Easy to make irreversible mistakes |
| 6 | Recognition rather than recall | Visible options, autocomplete | Hidden menus, memorize-this-flag |
| 7 | Flexibility and efficiency | Shortcuts (cmd-K), power-user paths | Same path for novice + power user |
| 8 | Aesthetic and minimalist design | No irrelevant chrome | Visual noise, redundant info |
| 9 | Error recovery (clear messages) | Plain language, suggested fix | Codes only, blame user |
| 10 | Help and documentation | Inline help, contextual tips | Manual hidden, no help |

Aggregate: avg < 3.0 → P1 systemic remediation; 3.0-4.0 → targeted; ≥ 4.0 → polish.

---

## 3. WCAG 2.2 AA Pass/Fail Grid

Mandatory checks per surface:

| Check | Pass criterion | Tool |
|---|---|---|
| Text contrast | ≥ 4.5:1 (normal), ≥ 3:1 (large 24px+) | axe DevTools, Stark, Contrast app |
| UI component contrast | ≥ 3:1 (borders, icons, focus rings) | axe DevTools |
| Focus visible (2.4.7) | Every interactive element shows focus | Manual tab test |
| Focus not obscured (2.4.11, new in 2.2) | Focus indicator never hidden by sticky elements | Manual scroll + tab |
| Target size (2.5.8, new in 2.2) | Interactive targets ≥ 24×24 CSS pixels | DevTools box check |
| Dragging movements (2.5.7, new in 2.2) | Drag has single-pointer alternative | Manual try-without-drag |
| Consistent help (3.2.6, new in 2.2) | Help links in same relative location | Cross-page check |
| Redundant entry (3.3.7, new in 2.2) | Don't re-ask info already collected | Multi-step form check |
| Authentication (3.3.8, new in 2.2) | Don't require cognitive challenges (math, memorization) | Auth flow check |
| Keyboard navigation | All actions reachable via keyboard | Tab through entire flow |
| Skip links | "Skip to main content" present | Tab from page load |
| Heading hierarchy | h1 → h2 → h3 (no skips) | axe outline check |
| Image alt text | Decorative: alt=""; meaningful: descriptive | axe scan |
| Form labels | Every input has visible label | axe scan |
| Color not sole signal | Status conveyed by icon + color, not color alone | Visual scan |
| Motion / animation | Respects `prefers-reduced-motion` | DevTools emulation |

ADA Title II reminder: as of 2026-04-24 (state/local pop. ≥ 50K), WCAG 2.1 AA is mandated; penalties up to $150K/violation. Document failures as legal risk.

---

## 4. Token Drift Detection

Scan for hardcoded values where tokens should exist:

| Pattern | Risk | Remediation |
|---|---|---|
| Inline color hex (`color: #FF5722`) | Brand drift | Replace with `var(--color-action-primary)` |
| Inline px spacing (`padding: 12px`) | Spacing scale drift | Replace with `var(--space-md)` |
| Inline font-size (`font-size: 17px`) | Type scale drift | Replace with `var(--text-base)` |
| Magic-number radii (`border-radius: 7px`) | Inconsistent corner language | Snap to scale (`--radius-md`) |
| Duplicate tokens across themes | "Frankenstein system" | Consolidate; cascade Core → Brand |
| Token defined but never referenced | Dead token | Remove; reduce noise |
| Token referenced but undefined | Build break / silent fallback | Define or remove reference |

Tools: design-system-linter, Theo, Style Dictionary's `validate`, Figma Variables API, custom regex on CSS-in-JS.

Drift score:
```
drift % = (hardcoded_values / total_style_declarations) × 100
```
- < 5% → healthy
- 5-15% → targeted cleanup
- > 15% → systemic; pause feature work

---

## 5. Design System Anti-Pattern Scan

| Anti-pattern | Detect by | Remediation |
|---|---|---|
| Component sprawl (5+ button variants) | Inventory components | Consolidate to ≤ 4 variants |
| Atomic-rigidity in multi-brand | Tokens shared but behavior diverges | Apply Core → Brand → Product cascade |
| Mixed paradigm (some BEM, some Tailwind) | grep class patterns | Pick one paradigm |
| Spacing values not on scale | All px values used | Snap to 4 / 8 / 16 / 24 / 32 / 48 / 64 |
| Type ramp > 8 steps | Inventory font-sizes | Reduce to 5-7 steps |
| Color palette > 12 hues | Inventory hue values | Reduce to 5-7 hues × shades |
| Shadow palette > 6 levels | Inventory box-shadows | Reduce to 4 levels |
| Z-index unbounded (z: 9999) | grep z-index values | Use named tokens (`--z-modal`, `--z-toast`) |
| Modal-in-modal | UX walkthrough | Convert nested modal to drawer or page |
| Loading without skeleton | Visual scan | Add skeleton screens |

---

## 6. Performance + UX Crossovers

| Check | Target | Source |
|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | Core Web Vitals |
| CLS (Cumulative Layout Shift) | < 0.1 | Core Web Vitals |
| INP (Interaction to Next Paint) | < 200ms | Core Web Vitals |
| Bounce rate | < 55% | Hotjar 2026 |
| Page weight | < 1.5MB on initial load | Performance budget |
| Time to interactive | < 3s perceived | Google |

Performance regressions are UX regressions — flag in audit.

---

## 7. Prioritized Remediation Backlog

Score each finding on **Effort × Impact**:

| Effort | Impact | Priority |
|---|---|---|
| Low | High | P1 — do first |
| Low | Med | P2 |
| Low | Low | P3 (or skip) |
| Med | High | P1 |
| Med | Med | P2 |
| Med | Low | P4 |
| High | High | P2 (plan over sprints) |
| High | Med | P3 |
| High | Low | drop |

Output format:
```markdown
## Remediation backlog

| ID | Finding | Heuristic / WCAG | Surface | Effort | Impact | Priority | Owner |
|---|---|---|---|---|---|---|---|
| F-01 | Focus ring missing on tabs | WCAG 2.4.7 | Settings | L | H | P1 | Palette |
| F-02 | Inline color hex on CTAs | Token drift | All | L | M | P2 | Muse |
| F-03 | Modal-in-modal in flow X | Anti-pattern | Checkout | M | H | P1 | Vision |
| ... |
```

---

## 8. Stakeholder Communication

Audit deliverable layers (most stakeholders read only the top):

```markdown
# Design Audit — <project>

## TL;DR (5 lines max)
- Surfaces audited: ___
- Heuristic avg: ___ / 5
- WCAG 2.2 AA pass rate: ___ %
- Token drift: ___ %
- P1 issues: ___ items

## Top 3 risks
1. ____ (legal/UX/brand)
2. ____
3. ____

## Top 3 wins (preserve these)
1. ____
2. ____
3. ____

## Detailed findings
[full backlog table]

## Methodology
- Heuristics scored by ___
- WCAG checked with ___ tools
- Drift detected by ___
```

---

## 9. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Audit scope too broad → useless avg scores | Cap at ~10 surfaces; batch larger scope |
| Score without specific finding → unactionable | Every score links to ≥ 1 finding ID |
| WCAG checked only with auto-tools (~30% catch rate) | Manual keyboard + screen reader pass mandatory |
| Findings without effort/impact → wishlist, not backlog | Score every finding |
| Token drift % not measured → vibes-based | Use linter; quantify |
| Anti-patterns identified but no replacement pattern | Pair every anti-pattern with the recommended pattern |
| Audit produced, then shelved | Hand off to specific owner per finding |
| Audit re-run not scheduled | Quarterly cadence; track delta over time |
| Performance ignored | LCP / CLS / INP are UX metrics; include |
| Brand-fit not audited | Use brand-strategy.md scoring rubric in parallel |

---

## 10. Decision Walkthrough Template

```
Audit scope:
  Surfaces (≤ 10): ____
  Audit depth: heuristic / + WCAG / + drift / + competitive
  Output: scorecard / backlog / executive

Heuristic scores (1-5):
  H1 status: ___  H2 real-world: ___  H3 control: ___  H4 consistency: ___  H5 prevention: ___
  H6 recognition: ___  H7 flexibility: ___  H8 aesthetic: ___  H9 error: ___  H10 help: ___
  Avg: ___ → action class: cosmetic / targeted / systemic

WCAG 2.2 AA grid:
  Text contrast pass rate: ___ %
  UI contrast pass rate: ___ %
  Focus visible (2.4.7): ✓ / ✗
  Focus not obscured (2.4.11): ✓ / ✗
  Target size (2.5.8): ✓ / ✗
  Dragging movements (2.5.7): ✓ / ✗
  Consistent help (3.2.6): ✓ / ✗
  Redundant entry (3.3.7): ✓ / ✗
  Authentication (3.3.8): ✓ / ✗
  Keyboard nav: ✓ / ✗
  ADA Title II compliance status: compliant / at risk
  Overall pass rate: ___ %

Token drift:
  Hardcoded color: ___ %
  Hardcoded space: ___ %
  Hardcoded type: ___ %
  Total drift: ___ %  → < 5 healthy / 5-15 cleanup / > 15 systemic

Anti-pattern scan results:
  □ Component sprawl
  □ Atomic-rigidity in multi-brand
  □ Mixed paradigm
  □ Off-scale spacing
  □ Bloated type ramp
  □ Bloated palette
  □ Bloated shadows
  □ Unbounded z-index
  □ Modal-in-modal
  □ Loading without skeleton

Performance:
  LCP: ___s  CLS: ___  INP: ___ms

Backlog generated: ___ items
  P1: ___  P2: ___  P3: ___  P4: ___

Owners assigned: ✓ / ✗
Re-audit scheduled: <date>

Handoff:
  → Muse (token drift remediation)
  → Palette (WCAG fixes)
  → Builder (component fixes)
  → Beacon (performance regressions)
  → Comply / Clause (legal-risk findings)
```

---

## 11. References
- Nielsen Norman Group, 10 Usability Heuristics
- W3C WCAG 2.2 (October 2023, current AA standard)
- DOJ ADA Title II final rule (2026 compliance deadline)
- Core Web Vitals (Google)
- DTCG specification v2025.10
- Adrian Roselli on APCA / WCAG 3 status
