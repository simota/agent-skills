# Nielsen Heuristic Evaluation Reference

Purpose: Structured expert-review methodology applying Nielsen's 10 usability heuristics (1994, still the field's de-facto baseline) plus domain-specific extensions. Surfaces usability issues without user recruitment, at roughly 1/10 the cost of moderated testing, while preserving traceability from finding to heuristic violated.

## Scope Boundary

- **echo `heuristic`**: persona-agnostic heuristic review against Nielsen's 10 + extended sets. Produces severity-ranked issue list with heuristic-citation audit trail.
- **echo `walkthrough` (default)**: persona-based cognitive walkthrough — simulates specific user minds through a flow.
- **palette (elsewhere)**: remediation. Once heuristics surface violations, Palette owns the redesign.
- **canon `wcag` (elsewhere)**: WCAG compliance assessment. Heuristic evaluation is broader than accessibility — overlap exists around heuristic 4 (consistency) and heuristic 9 (recognize/recover errors).
- **researcher (elsewhere)**: empirical validation with real users. Heuristic evaluation predicts issues; research confirms them.

## Workflow

```
PREP     →  define scope (screens/flows), recruit 3-5 evaluators, agree heuristic set
         →  brief evaluators: independent passes first, group reconciliation second

PASS 1   →  each evaluator walks the interface alone, logs findings per heuristic
         →  issues independent — do not discuss until logged

PASS 2   →  evaluators walk the interface again with task scenarios in mind
         →  adds context-dependent violations missed in open exploration

RECONCILE →  merge findings, dedupe, assign severity (0-4), tag heuristic(s) violated
          →  resolve scoring disagreements via worst-case consensus

REPORT   →  severity-ranked issues with heuristic citation, evidence, and fix category
         →  hand off fix candidates to Palette; critical issues to Judge for gating
```

## The 10 Heuristics (Nielsen 1994, Refined 2020)

| # | Heuristic | Core question | Common violations |
|---|-----------|---------------|-------------------|
| 1 | Visibility of system status | Does the UI tell users what's happening? | Silent loading, hidden progress, unclear save state |
| 2 | Match real world | Does language match user mental models? | System jargon, reversed metaphors, cryptic icons |
| 3 | User control and freedom | Can users undo / escape? | No cancel on long operations, no confirm-undo pair, forced paths |
| 4 | Consistency and standards | Does it follow platform and product conventions? | Mixed button styles, inconsistent gestures, off-pattern modals |
| 5 | Error prevention | Does it prevent errors before they occur? | Destructive actions without confirm, free-text where constrained input possible |
| 6 | Recognition over recall | Are options visible rather than remembered? | Hidden menus, context-free icons, no recent/suggested values |
| 7 | Flexibility and efficiency | Does it serve novice and expert? | No shortcuts, no power-user batch ops, one-path-only design |
| 8 | Aesthetic and minimalist design | Is noise minimized? | Information overload, competing CTAs, decorative over functional |
| 9 | Recognize, diagnose, recover from errors | Are errors plain-language, diagnostic, recoverable? | "Error 500", no next step, no retry |
| 10 | Help and documentation | Is task-scoped help available? | Only general docs, no contextual tips, stale screenshots |

## Severity Scale (Nielsen)

| Score | Meaning | Action |
|-------|---------|--------|
| 0 | Not a usability problem | Dismiss |
| 1 | Cosmetic only | Fix if time permits |
| 2 | Minor — low-frequency or easy workaround | Low priority |
| 3 | Major — frequent or high-impact | Fix before launch |
| 4 | Catastrophic — blocks task, must fix | Ship-blocker |

Apply worst-case consensus: if evaluators split 3/4, use 4. Severity `≥3` items are the escalation set for launch gates.

## Evaluator Count Calibration

| Evaluators | Issues found | Cost multiplier |
|------------|--------------|-----------------|
| 1 | ~35% | 1.0× |
| 3 | ~60% | 3.0× |
| 5 | ~75% | 5.0× |
| 8 | ~85% | 8.0× (diminishing returns) |

Nielsen's published curve: 3-5 evaluators is the sweet spot. Below 3, coverage is unreliable. Above 5, cost grows faster than issue discovery. Prefer diverse evaluators (UX, accessibility, domain) over more homogeneous ones.

## Extended Heuristic Sets

Nielsen 10 covers general GUIs. Apply the right extension when the domain demands:

- **Mobile / touch**: fat-finger safety, one-handed reach zones, gesture discoverability (Kendall's 7, Bertini et al.)
- **Data-dense enterprise**: Shneiderman's 8 Golden Rules — emphasizes informative feedback, reversible actions, locus of control
- **Games**: Heuristic Evaluation for Playability (HEP) — Desurvire — goal clarity, reward feedback, difficulty progression
- **Voice / conversational**: Murad's 17 — interruption recovery, turn-taking, ambiguity resolution
- **XR / immersive**: Sutcliffe's XR heuristics — presence, motion sickness, embodiment

Cite the set used in the report header. Mixing sets without attribution masks domain-specific issues.

## Anti-Patterns

- One-evaluator reviews — single evaluators find ~35% of issues. Brand it "design review," not "heuristic evaluation."
- Skipping the independent pass — group-first reviews anchor on the loudest voice and miss ~40% of unique issues.
- Heuristic evaluation without task scenarios — open exploration misses context-dependent violations (state-specific, role-specific, frequency-specific).
- Reporting violations without severity — forces stakeholders to triage, and high-severity items get lost among cosmetic notes.
- Treating heuristic findings as empirical — they are predictive. Every critical finding should be validated with ≥5 real users before betting on the fix.
- Applying Nielsen-10 to voice, games, or XR — generic heuristics miss domain-specific issues; use the matching extended set.
- Omitting evaluator backgrounds — a heuristic review by 3 visual designers and a review by 1 visual + 1 a11y + 1 domain expert surface very different issues. Document the panel.

## Handoff

- **To Palette**: severity `≥3` issues with heuristic citation, affected element, and recommended fix category (feedback, affordance, content, error state).
- **To Canon `wcag`**: heuristic 4 (consistency) and 9 (error recovery) violations that overlap WCAG criteria — cross-validate against WCAG 2.2.
- **To Researcher**: severity `≥3` issues with ambiguous cause — escalate to 5-user moderated study for empirical validation.
- **To Judge**: catastrophic (severity 4) issues as ship-blockers with heuristic-cited evidence.
- **To Echo `walkthrough`**: reconcile heuristic findings against persona walkthrough. If walkthrough surfaced the same issue, confidence is higher.
