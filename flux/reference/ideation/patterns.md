# Brainstorming Patterns

**Purpose:** Session patterns and mode transition reference for Flux.
**Read when:** You need pattern definitions, session structure, or mode transition guidance.

---

## Double Diamond Pattern

The primary dialogue structure. Two diverge→converge cycles to deepen thinking.

```
Phase 1: Discover (EXPAND)     → Define (EVALUATE)
Phase 2: Develop (PROPOSE)     → Deliver (SUBTRACT)
```

### Phase 1: Problem Space Exploration

| Step | Mode | Purpose | Turn estimate |
|------|------|---------|---------------|
| 1. Confirm understanding | - | Summarize and confirm the idea | 1 |
| 2. Broaden perspectives | EXPAND | Multi-angle questions to widen the view | 2-3 |
| 3. Evaluate and select | EVALUATE | Choose promising directions | 1-2 |

### Phase 2: Solution Space Exploration

| Step | Mode | Purpose | Turn estimate |
|------|------|---------|---------------|
| 4. Concretize | PROPOSE | Shape selected direction into tangible ideas | 2-3 |
| 5. Extract essence | SUBTRACT | Strip excess, distill to core | 1-2 |
| 6. Summarize | - | Session outcome summary | 1 |

---

## Quick Flux Pattern

A focused 4-5 turn session concentrating on a single mode.

```
1. Receive the idea (1 turn)
2. Deep-dive in one selected mode (2-3 turns)
3. Wrap up with insights (1 turn)
```

| Mode | When to use | Central question |
|------|-------------|-----------------|
| Quick EXPAND | Stuck / need fresh perspective | "List 3 assumptions. What if you reversed one?" |
| Quick PROPOSE | Direction clear, needs shape | "What's the smallest step you can start tomorrow?" |
| Quick EVALUATE | Have options, need to choose | "Compare on 3 axes: technical / user / business?" |
| Quick SUBTRACT | Over-packed | "If you had to cut half, which half stays?" |

---

## Devil's Advocate Pattern

Intentionally take the opposing stance to stress-test an idea's strength.

```
1. Understand: Fully grasp the idea
2. Steelman: Present the best interpretation first (fairness)
3. Challenge: Attack from 3 angles
   - Technical barriers
   - User acceptance
   - Market / business fit
4. Rebuild: Ask user to improve based on the challenges
```

**Warning:** Always preface with "I'm deliberately presenting counterarguments — I'm not rejecting the idea itself."

---

## Mode Transition Signals

Reference for judging mode transitions from conversational cues.

### EXPAND → EVALUATE

- User: "Lots of ideas now, but..."
- User: "Which one is better?"
- Flux judges: 3+ directions have emerged

### EVALUATE → PROPOSE

- User: "I want to go this direction"
- User: "How do we make it concrete?"
- Flux judges: 1-2 directions have been selected

### PROPOSE → SUBTRACT

- User: "Maybe I'm packing too much in"
- User: "Can we simplify?"
- Flux judges: Concrete plan has 3+ elements

### Any → EXPAND

- User: "I'm stuck"
- User: "Any other perspectives?"
- Flux judges: 2+ turns circling the same point


---

## Per-Recipe Behavior Notes (SKILL.md excerpt)

- `expand`: Double Diamond mode. RECEIVE → EXPAND (multiple turns) → SYNTHESIZE. Focus on the divergence phase.
- `propose`: Quick Flux mode. RECEIVE → PROPOSE (4-5 turns) → SYNTHESIZE. Quickly generate concrete proposals.
- `evaluate`: Devil's Advocate mode. RECEIVE → Steelman → 3-angle challenge → rebuild.
- `subtract`: Lead with SUBTRACT mode. Narrow down excess ideas to extract the essence.
- `steelman`: Read `reference/ideation/steelman-protocol.md` first. Strict 5 phases: RECEIVE → STEELMAN FOR → STEELMAN AGAINST → SYNTHESIZE → SOFT VERDICT. Build FOR and AGAINST sequentially (no parallel construction); suppress counter-arguments while building each side. Quality test (internal): "would the most thoughtful proponent / skeptic recognize this as their actual view?". Forbid lukewarm both-sides, sandwich softening, premature synthesis, hidden vote, and verdict creep. Fatal flaws (technical impossibility / ethical issue / known failure pattern) must headline the AGAINST phase, not appear as a caveat. SOFT VERDICT must hand back in the structure "for FOR to win, X must be true / for AGAINST to win, Y / cheapest experiment is Z"; route formal Go/No-Go to **Magi**.
- `scamper`: Read `reference/ideation/scamper-method.md` first. Apply 7 lenses (Substitute / Combine / Adapt / Modify-Magnify / Put-to-other-use / Eliminate / Reverse) sequentially; for each lens, surface 1-3 concrete variations and let the user pick. Sequencing is situational: generic idea → A→M→R; feature bloat suspected → E→S→P; stuck → R→A→C; pre-launch → M→E→S. Variation quality bar: concrete / testable / differentiated / bounded must all hold; skip any lens that cannot meet it. Forbid all-seven-no-depth, lens dressing (relabeling the same idea 7 times), user backseat (21 variations overwhelming the user), premature combine, and reverse-as-gimmick. In SYNTHESIZE, present the strongest variations as a table along with the hybrid candidate and the decisive question.
- `crazy8`: Read `reference/ideation/crazy-eights.md` first. Strict constraints: exactly 8 variations / one sentence each (≤ 20 JP chars / ≤ 12 EN words) / one divergence axis declared up front / each variation changes a different attribute / fast pace. Have the user pick one axis from the catalog (form-factor / target-user / time-horizon / scale / constraint / interaction-model / data-source / stance / polarity). Present all 8 numbered variations in a single turn with no inter-variation explanation, then immediately ask "pick 1-3". Quality bar: complete idea / distinguishable / axis-aligned / contains a concrete noun / 1-2 deliberately absurd. Politely decline user softening like "let's do 5" and recommend SCAMPER instead. Forbid lazy 8 (4 padding), 8 hedges, axis drift, no absurdity, and no convergence. After picks, route to propose / steelman / another-axis crazy8 / Magi based on selection count.
- `multi`: Read `reference/ideation/tri-engine-ideate.md` first. Parallel brainstorm round — spawn `flux-ideate-codex` / `flux-ideate-agy` / `flux-ideate-claude` subagents in one Agent-tool message; each produces 3-4 ideas independently for the active mode (Expand by default; pick from dialogue signals: vague theme → expand / direction clear → propose / multiple candidates → evaluate / over-packed → subtract). Loose prompts: pass only Role + Theme + Active mode + Output format — never pass SCAMPER lenses, Crazy-8 axes, Steelman protocol, or any other Flux Recipe templates (those are applied in SYNTHESIZE only). Pattern D scoring within each mode: `UNIVERSAL` (3/3), `LIKELY` (2/3), `VERIFIED-DIVERGENT` (1/3 after grounding). **Ideate-specific inversion**: in EXPAND mode, `UNIVERSAL` ideas are suspect of being the obvious framing the user could have reached alone — lead synthesis with VERIFIED-DIVERGENT. In SUBTRACT mode, UNIVERSAL signals are usually correct. GROUND step (Flux main context): theme connection / mode fit / hallucinated entity / sugar-coat / duplicate-of-prior-turn. SYNTHESIZE = single dialogue turn carrying idea cards (each in Flux's Receive → Challenge → Prompt voice) ordered VERIFIED-DIVERGENT → LIKELY → UNIVERSAL, closing with "which 1-3 to go deeper on?". With `multi --all-modes`: 4 modes × 3 engines = up to 36 ideas, output as a 4 × N matrix with a "diamond reading" interpretation and top-breakthrough callout. Multi is **one turn inside dialogue**, not a replacement for it; the user's pick seeds the next normal Flux turn. Degraded modes (1 engine missing / 2 down / all down): see common protocol; Ideate-specific addition — `multi --all-modes` over 36 ideas caps each engine at 8 and trims UNIVERSAL first.

