# Crazy 8s

Reference for Riff's `crazy8` recipe. A time-boxed rapid-divergence dialogue that produces 8 distinct variations of the same idea under intentional time pressure, each constrained to one sentence and one differentiating axis.

Crazy 8s comes from the Google Ventures Design Sprint, where designers fold a paper into 8 boxes and sketch one variation per box per minute. Riff adapts the protocol to dialogue: the goal isn't sketches, it's 8 *named* variations on a single divergence axis, fast.

The constraint is the method. Without the constraint, divergence collapses into the 2-3 most obvious options.

---

## 1. When to Apply

Use the `crazy8` recipe when:

- The user has one idea and 0 alternatives — the option space is collapsed.
- The team converged too early and the chosen direction lacks confidence.
- A SCAMPER lens or steelman session needs more raw variation before deciding.
- The user is stuck on a single shape ("a dashboard for X") and needs to see other shapes.

Skip when:

- The user already has 5+ candidates and needs convergence (use `subtract` or **Magi**).
- The decision is already partially committed (use `steelman` instead).
- The user wants depth on one variation, not breadth (use `propose`).

---

## 2. The Constraint

Crazy 8s only works under explicit constraints. Riff enforces:

| Constraint | Reason |
|------------|--------|
| Exactly 8 variations | Fewer = lazy, more = unfocused |
| One sentence each | Forces the variation's essence to surface |
| One differentiating axis declared up front | Prevents "8 versions of the same idea" |
| Anti-repetition rule: each variation must change a *different* attribute | Prevents lens-drift |
| Time pressure (8 minutes total, ~1 min/variation) | Bypasses self-censorship |

If the user softens any constraint ("can we do 5?"), Riff politely declines and explains the protocol. Looser version → use SCAMPER.

---

## 3. Choosing the Divergence Axis

Before generating 8 variations, declare *what* is varying. Otherwise the 8 collapse into 8 small tweaks.

| Axis | Example variations |
|------|-------------------|
| **Form factor** | CLI / Web / extension / TUI / native app / chatbot / API / physical device |
| **Target user** | Senior dev / junior dev / PM / designer / SRE / hobbyist / teacher / kid |
| **Time horizon** | Real-time / batched daily / yearly recap / on-demand / scheduled / triggered |
| **Scale** | One person / small team / company / public / global |
| **Constraint** | No-deps / 100-LOC / offline / single-binary / paid-only / free-only |
| **Interaction model** | Voice / keyboard / drag-drop / passive / chat / form / gesture |
| **Data source** | User-provided / scraped / generated / observed / inferred |
| **Stance** | Helpful / playful / formal / minimal / opinionated / agnostic |
| **Polarity** | Read-only / write-only / observable / imperative / declarative |

Pick **one** axis. The 8 variations vary along it. Other dimensions stay roughly fixed.

---

## 4. Dialogue Template

```
Riff (RECEIVE):
  Idea recap: [one sentence]
  Crazy 8s mode: I'll generate 8 variations along one axis.
  Which axis should we vary? [present 3-4 from § 3]

User: [picks axis]

Riff (GENERATE — fast, 8 variations):
  1. [variation along axis]
  2. [variation along axis]
  3. [variation along axis]
  4. [variation along axis]
  5. [variation along axis]
  6. [variation along axis]
  7. [variation along axis]
  8. [variation along axis]
  Which 1-3 do you want to pull on?

User: [picks 1-3]

Riff (CONVERGE):
  Picks: [user's selection]
  Why these are interesting together: [pattern across picks]
  Decisive question: [what would resolve which to pursue]
  Suggested next: [agent or recipe]
```

---

## 5. Variation Quality Bar

Each of the 8 variations must:

- **Be a complete idea** — not "do X but better"
- **Be distinguishable** — readers can tell which variation is which
- **Vary along the declared axis** — not along a different one
- **Include a concrete noun** — not just adjectives ("a fast version")
- **Be at least slightly absurd in 1-2 of the 8** — Crazy is in the name

If a variation reads as a hedge ("either X or Y"), it's not a variation. Cut it; produce a sharper one.

---

## 6. Time Pressure (Adapted for Dialogue)

Riff doesn't enforce literal time, but signals pace:

- All 8 in one Riff turn — no back-and-forth between them
- Short sentence per variation (≤ 20 Japanese characters or ≤ 12 English words)
- No explanations between variations
- Numbered list, no bullets, no sub-lists
- After the list, immediately ask user to pick 1-3

This pace is the protocol. Lengthy explanations break the divergence engine.

---

## 7. Convergence After 8

The goal isn't 8 variations. It's a sharper choice across them. After the user picks 1-3:

| User picks | Riff's next move |
|-----------|------------------|
| 1 variation | Treat as new seed; offer `steelman` or `propose` |
| 2 variations | Compare on the decisive axis; offer **Magi** if the user wants verdict |
| 3+ variations | Run another Crazy 8s on the *intersection* (different axis) |
| None | Either pick a different axis or route back to `expand` |

---

## 8. Anti-Patterns

- **Lazy 8** — 4 variations of the obvious shape, 4 padding ideas. Reject; regenerate.
- **8 hedges** — "a tool that lets users decide whether to X or Y." Cut hedges, force commitment.
- **Axis drift** — variation 1 varies form factor, variation 5 varies user, variation 7 varies time. Stick to the declared axis.
- **No absurdity** — all 8 are plausible. Add at least 1 deliberately weird variation; it sharpens the others.
- **No convergence** — generate 8 and stop. The convergence step is half the value.

---

## 9. Output Format (SYNTHESIZE Section)

```markdown
## Crazy 8s Session Summary

### Idea
[Original, one sentence]

### Divergence Axis
[Single axis used]

### 8 Variations
1. [variation]
2. [variation]
3. [variation]
4. [variation]
5. [variation]
6. [variation]
7. [variation]
8. [variation]

### Picks
[1-3 user-selected variations]

### Pattern
[What the picks have in common — surfaces the user's hidden preference]

### Decisive Question
[What would resolve which to pursue]

### Suggested Next
- Riff `steelman` (stress-test one pick)
- Riff `propose` (deepen one pick into a concrete proposal)
- Riff `crazy8` again on a different axis (if 3+ picks)
- Spark / Accord (if a pick is ready to spec)
- Magi (if the user wants formal verdict between picks)
```

---

## 10. Handoff Routing

| Outcome | Next agent | Why |
|---------|-----------|-----|
| Single variation, deepening | Riff `propose` | Concretize the pick |
| Single variation, stress-testing | Riff `steelman` | Strongest case for/against |
| Multiple variations, choosing | **Magi** | Formal multi-perspective |
| Variation is feature-shaped | **Spark** | Feature seed |
| Hybrid of multiple | Riff `scamper` Combine lens | Merge picks via SCAMPER C |
| Need yet more divergence | Riff `crazy8` again | Different axis |
