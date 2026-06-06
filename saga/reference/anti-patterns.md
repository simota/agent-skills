# Saga Anti-Pattern Checklist (AP-1 ~ AP-9)

**Purpose:** Canonical anti-pattern reference for Saga narratives. Every narrative produced by any Saga recipe must pass this checklist in the REFINE phase before delivery.
**Read when:** REFINE phase, narrative audit, GROUND step of `multi` Recipe, or any time you need to validate a narrative.

---

## The Master Checklist

| # | Anti-Pattern | Check | Fix |
|---|-------------|-------|-----|
| AP-1 | **Feature Dump** — raw feature list, no arc | Does a story arc exist? | Restructure into challenge→resolution flow |
| AP-2 | **Hero Product** — product is the protagonist | Is the customer the subject? | Rewrite from customer perspective |
| AP-3 | **Missing Tension** — no challenge or conflict | Is the "Before" painful? | Add specific pain points |
| AP-4 | **No Transformation** — no change depicted | What changed in "After"? | Make Before→After explicit |
| AP-5 | **Generic Persona** — abstracted as "the user" | Does the persona have a name and context? | Add a concrete character |
| AP-6 | **Narrative Bias** — facts distorted to fit story | Is there evidence? | State assumptions, propose validation |
| AP-7 | **Jargon Wall** — jargon blocks empathy | Can non-technical readers understand? | Use plain language |
| AP-8 | **Happy Path Only** — no failure scenario | Were stakes depicted? | Add what is lost without action |
| AP-9 | **Ad Copy Disguise** — narrative reads as promotional copy | Does it sound like an ad? | Rewrite around user transformation, not product promotion |

---

## Checklist Output Format

When reporting AP results in a deliverable, use this format:

```markdown
### Anti-Pattern Check
- [ ] AP-1 Feature Dump: [PASS/FAIL — reason]
- [ ] AP-2 Hero Product: [PASS/FAIL — reason]
- [ ] AP-3 Missing Tension: [PASS/FAIL — reason]
- [ ] AP-4 No Transformation: [PASS/FAIL — reason]
- [ ] AP-5 Generic Persona: [PASS/FAIL — reason]
- [ ] AP-6 Narrative Bias: [PASS/FAIL — reason]
- [ ] AP-7 Jargon Wall: [PASS/FAIL — reason]
- [ ] AP-8 Happy Path Only: [PASS/FAIL — reason]
- [ ] AP-9 Ad Copy Disguise: [PASS/FAIL — reason]
```

All 9 checks must PASS before delivery. For short-form formats (BAB, ABT, micro-narrative), AP-8 may be marked "N/A" with rationale.

---

## Rejection Categories (used by `multi` Recipe GROUND step)

When a narrative fails grounding during tri-engine synthesis, classify with these codes:

| AP fail | Rejection code |
|---------|----------------|
| AP-1 Feature Dump | `REJECTED-NO-ARC` |
| AP-2 Hero Product | `REJECTED-HERO-PRODUCT` |
| AP-3 Missing Tension | `REJECTED-NO-TENSION` |
| AP-4 No Transformation | `REJECTED-NO-TRANSFORMATION` |
| AP-5 Generic Persona | `REJECTED-GENERIC-PERSONA` |
| AP-6 Narrative Bias | `NEEDS-INFO` (request validation) |
| AP-7 Jargon Wall | `REJECTED-JARGON` |
| AP-8 Happy Path Only | `REJECTED-NO-STAKES` |
| AP-9 Ad Copy Disguise | `REJECTED-AD-COPY` |
| Fabricated persona | `REJECTED-PERSONA-FABRICATED` |
| Fabricated evidence | `REJECTED-FABRICATED-EVIDENCE` |

---

## Recipe-Specific Emphasis

Each Saga recipe places extra weight on certain APs (see each recipe file for recipe-local anti-patterns):

| Recipe | Critical APs | Reason |
|--------|-------------|--------|
| `story` / `customer` | AP-3, AP-4, AP-5 | Use-case stories die without tension or named protagonist |
| `hero-journey` | AP-2, AP-4, AP-8 | Long-form transformation must keep customer as hero, show stakes |
| `bab` | AP-3, AP-7, AP-9 | Short copy easily slips into jargon or ad voice |
| `pyramid` | AP-1, AP-6, AP-7, AP-9 | Executive memos need MECE structure, evidence, no promo tone |
| `narrative` (Promised Land / SB7) | AP-2, AP-6, AP-9 | Strategic narratives must not become company-as-hero ad copy |
| `multi` (GROUND step) | All 9 (full audit on CANDIDATE) | Lightweight AP-2 + AP-9 spot-check on UNIVERSAL/LIKELY clusters |

Recipe files (`hero-journey.md`, `before-after-bridge.md`, `minto-pyramid.md`) carry their own **Anti-Patterns Specific to [recipe]** tables for craft-level pitfalls beyond the AP-1~AP-9 universals.
