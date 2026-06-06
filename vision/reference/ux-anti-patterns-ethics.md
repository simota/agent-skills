# UX Anti-Patterns & Ethical Design

Purpose: Use this file when reviewing dark patterns, cognitive overload, accessibility violations, or ethical-design requirements.

Contents:
- dark-pattern catalog
- cognitive-overload catalog
- accessibility violation catalog
- ethical design principles and gates

## Dark Patterns (`DP-01` to `DP-07`)

| ID | Pattern | Harm | Ethical alternative |
|----|---------|------|---------------------|
| `DP-01` | Trick Questions | accidental opt-in | plain affirmative labels |
| `DP-02` | Sneak into Basket | unwanted charges | explicit opt-in |
| `DP-03` | Roach Motel | hard cancellation | symmetric signup and cancellation |
| `DP-04` | Forced Continuity | unnoticed billing | reminders before renewal |
| `DP-05` | Bait and Switch | action/result mismatch | transparent outcome disclosure |
| `DP-06` | Privacy Zuckering | excessive data sharing | concise and accessible privacy choices |
| `DP-07` | Confirm Shaming | emotional manipulation | neutral language |

## Cognitive Overload (`CO-01` to `CO-06`)

| ID | Pattern | Response |
|----|---------|----------|
| `CO-01` | feature overload | progressive disclosure |
| `CO-02` | too many choices | keep primary choices around `5-7` |
| `CO-03` | visual noise | content-first reduction |
| `CO-04` | inconsistent UI patterns | unify through the design system |
| `CO-05` | dense information blocks | hierarchy and whitespace |
| `CO-06` | hidden navigation | keep primary routes visible |

## Accessibility Violations (`AV-01` to `AV-06`)

| ID | Violation | Rule | Response |
|----|-----------|------|----------|
| `AV-01` | low contrast | WCAG `1.4.3`, AA `4.5:1` | verify text contrast |
| `AV-02` | color-only status | WCAG `1.4.1` | add icon or text |
| `AV-03` | hidden focus indicator | WCAG `2.4.7` | visible focus ring |
| `AV-04` | unclear disabled state | WCAG `1.4.11`, AA `3:1` | visible distinction plus semantics |
| `AV-05` | keyboard-inaccessible interaction | WCAG `2.1.1` | full keyboard support |
| `AV-06` | excessive motion | WCAG `2.3.3` | support `prefers-reduced-motion` |

## Ethical Design Principles

1. Respect user autonomy.
2. Be transparent about data, AI, and consequences.
3. Design inclusively with `WCAG 2.2 AA` as the floor.
4. Consider sustainability and unnecessary resource use.
5. Favor long-term trust over short-term conversion tricks.

## Quality Gates

- text contrast must meet `4.5:1` where required
- status must not rely on color alone
- cancellation should not be meaningfully harder than signup
- default settings should favor the user, especially for privacy
- motion-heavy proposals must specify reduced-motion behavior

## Ethical AI Design Principles (2025-2026)

6. Disclose AI involvement: users must know when content or decisions are AI-generated.
7. Provide explainability: AI outputs must be explainable at a level appropriate to context.
8. Embed fairness from the start (Ethics-by-Design): apply bias testing during data collection, not only post-deployment.
9. Support human override: every AI-driven decision must have a clear path for human intervention.
10. Ethical refusal is valid: declining to deploy GenAI can be the right decision.

## AI-Specific Dark Patterns

| ID | Name | Impact | Fix |
|----|------|--------|-----|
| `DP-08` | AI Hallucination Concealment | Trust erosion when discovered | Disclose confidence levels; use Confidence Indicators |
| `DP-09` | Invisible AI Agency | Users unaware AI is acting on their behalf | Surface AI actions via Proposal Cards; require explicit validation |
| `DP-10` | Algorithmic Manipulation | Personalization exploiting vulnerabilities | Transparent recommendation logic; user-controllable personalization |

AI quality gates:
- AI-generated content must be labeled as such.
- Confidence indicators required for AI outputs in high-stakes contexts.
- Human override path must exist for every autonomous AI action.
- Bias testing must be documented before launching AI-driven personalization.
