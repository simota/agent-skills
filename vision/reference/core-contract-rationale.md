# Core Contract — Rationale and Sources

Evidence, thresholds, and citations behind the Core Contract bullets in `SKILL.md`.

## Outcome anchoring

Anchor every direction to measurable success criteria: target task-success rate, time-on-task
reduction, or conversion lift. UX ROI benchmark — every $1 invested in UX should target a
$2-$100 return (Forrester / NN/g); state the expected ROI range for major redesigns.

## AI-driven interfaces

**Explainability is mandatory.** Users must understand *why* the system acted: require inline
explanation affordances ("Why am I seeing this?") for every AI-generated recommendation or
action. Trust is the #1 design challenge for AI experiences in 2026 — every AI surface must
address it through transparency, control, and graceful fallback (NN/g State of UX 2026). 63%
of users are more likely to rely on AI that displays confidence levels or reasoning than on
black-box output (2026 AI-UX research); 78% of managers view explainability as a core
requirement for responsible AI (Grazitti, 2026).

**No prediction-driven UI without user override.** Auto-fill, auto-sort, and auto-decide
actions must always provide visible undo, an explanation of what changed, and manual
override. Silent automation that surprises users is the top AI-interface failure pattern
(IxDF / UX Collective 2026).

## Token governance

Prevent design drift with a single-source-of-truth token architecture — no duplicated tokens
across teams. For multi-brand products use the Core -> Brand -> Product orchestrated
inheritance model (semantic tokens only at Core; brand overrides at Brand; product-specific
exceptions at Product). Shared-library flat models produce "Frankenstein systems" where
tokens are shared but behavior diverges. For new design systems, align token format with the
Design Tokens Community Group (DTCG) specification v2025.10 (first stable release October
2025; a Community Group Report, not a W3C Standard).

## Accessibility baseline and WCAG 3.0 readiness

WCAG 2.2 AA is the minimum; recommend AAA for text-heavy surfaces. Keep 2.2 AA as the legal
baseline — DOJ ADA Title II and the EU EAA reference it.

Do **not** plan around APCA as a standards-track replacement: it was removed from the WCAG 3
working draft in July 2023 and was not reintroduced in the March 2026 Working Draft (W3C, 03
March 2026). Treat APCA as an optional perceptual overlay for brand/marketing surfaces only
where it does not fail WCAG 2.2 AA; document any 2.2 failures as legal risk. WCAG 3.0 remains
a Working Draft — Candidate Recommendation expected 2026-2027, Proposed/final Recommendation
2027-2028 at earliest.
Source: [W3C — WCAG 3.0 Working Draft, 03 March 2026](https://www.w3.org/TR/wcag-3.0/)
