# SCAMPER Method

Reference for Riff's `scamper` recipe. A structured 7-lens dialogue that runs an idea through Substitute, Combine, Adapt, Modify/Magnify, Put-to-other-use, Eliminate, and Reverse — producing concrete variations, not abstract suggestions.

SCAMPER (Bob Eberle, 1971; building on Alex Osborn) is a checklist for breaking out of single-axis thinking. Riff treats each lens as a probing question pattern, surfacing 1-3 variations per lens, and converges at the end.

---

## 1. The Seven Lenses

Each lens transforms the idea along a specific axis. Apply lenses in sequence; do not bundle.

| Lens | Axis | Core question |
|------|------|---------------|
| **S** — Substitute | Replace a part | What if X were replaced by Y? |
| **C** — Combine | Merge with another | What if X were combined with Y? |
| **A** — Adapt | Borrow from elsewhere | What other domain solves this? Can we adapt their solution? |
| **M** — Modify / Magnify | Change scale or attribute | What if X were bigger / smaller / louder / slower / continuous? |
| **P** — Put to other use | Same thing, new context | Who else could use this? What else could it do? |
| **E** — Eliminate | Remove a part | What happens if we remove X? Is X actually needed? |
| **R** — Reverse / Rearrange | Invert the order or polarity | What if the order were reversed? What if the user did X instead of the system? |

---

## 2. Probing Questions per Lens

### S — Substitute

- What component / material / step / actor / channel could be replaced?
- What rule could be replaced with a different rule?
- What if the user role were swapped (admin → guest, paid → free)?
- What if the data source were replaced (live → cached, push → pull)?

### C — Combine

- What two flows could merge into one?
- What if X were bundled with Y to share a context?
- What unrelated tool, when combined, would reframe X?
- What if competitors' approaches were combined?

### A — Adapt

- What does this look like in a different industry (medicine, gaming, music)?
- What pattern from biology / physics / sociology applies here?
- What does this look like in a pre-digital era?
- What does this look like at a different organizational scale?

### M — Modify / Magnify

- What if it were 10× bigger? 10× smaller? 10× faster? 10× slower?
- What if the unit changed (per-user → per-team, per-second → per-day)?
- What if a hidden attribute were dialed up (frequency, intensity, density)?
- What if it became continuous instead of discrete (or vice versa)?

### P — Put to other use

- Who else has this same problem in a different form?
- What second-order use does this have if the primary use is solved?
- What does this become for a non-engineer audience?
- What if we exposed only the byproduct?

### E — Eliminate

- What step could be removed without breaking the outcome?
- What is the user doing that the system should do (or the reverse)?
- What feature would the user not miss if it disappeared?
- What if the *primary* feature were removed — what's left?

### R — Reverse / Rearrange

- What if the order of steps were inverted?
- What if the system became the user and the user became the system?
- What if input were output (or vice versa)?
- What if "after" came before "before" (preview vs commit)?

---

## 3. Sequencing Strategies

The default order S-C-A-M-P-E-R is fine for first-pass exploration. For specific situations, use these sequences:

| Situation | Recommended sequence |
|-----------|---------------------|
| Idea feels too generic | A → M → R (borrow, scale, invert) |
| Feature bloat suspected | E → S → P (cut, replace, find new use) |
| Stuck on one variation | R → A → C (invert, borrow, merge) |
| Pre-launch sharpening | M → E → S (scale, cut, replace) |
| Cross-domain expansion | P → A → C (new uses, borrow, merge) |

Skip lenses that produce nothing. Run only the ones that earn the turn.

---

## 4. Dialogue Template

```
Riff (RECEIVE):
  Idea recap: [one sentence]
  We'll run SCAMPER. I'll surface 1-3 variations per lens, then we converge.
  Should I run all seven lenses or focus on [subset]?

User: [confirms]

Riff (S — Substitute):
  Three substitutions:
  1. [variation]
  2. [variation]
  3. [variation]
  Which feels worth pulling on?

User: [picks]

Riff (C — Combine):
  ...
```

After the user picks promising variations across lenses, converge:

```
Riff (SYNTHESIZE):
  Strongest variations from this run:
  - From S: [variation X]
  - From M: [variation Y]
  - From R: [variation Z]
  These combine into: [hybrid concept]
  Open question: [decisive uncertainty]
  Suggested next: [agent or lens]
```

---

## 5. Variation Quality Bar

For each lens, every variation must satisfy:

- **Concrete**: a specific change, not a vague "improve X"
- **Testable**: can be reasoned about — what would this version look like, do, cost?
- **Differentiated**: not the same as another lens's output
- **Bounded**: either trivially implementable or scoped to a learnable experiment

If a lens produces only generic suggestions, skip it and move to the next.

---

## 6. Anti-Patterns

- **All seven, no depth**: one paragraph per lens, none deep enough to use. Better: 3 lenses, 3 sharp variations each.
- **Lens dressing**: relabeling the same idea seven times. If S and C produce the same concept, drop one.
- **User backseat**: Riff lists 21 variations; user is overwhelmed. Stop after 2-3 lenses if engagement drops.
- **Premature combine**: jumping to a hybrid before the user has weighed individual variations.
- **Reverse-as-gimmick**: forcing R when nothing meaningful inverts. Skip.

---

## 7. Output Format (SYNTHESIZE Section)

```markdown
## SCAMPER Session Summary

### Idea
[Original idea, one sentence]

### Lenses Run
[List of lenses applied — may be subset]

### Strongest Variations
| Lens | Variation | Why interesting |
|------|-----------|-----------------|
| S | [variation] | [reason] |
| M | [variation] | [reason] |
| R | [variation] | [reason] |

### Hybrid Candidate
[If two or more variations combine]

### Decisive Question
[What would resolve which variation to pursue]

### Open Lenses
[Lenses not yet run that may still surface value]

### Suggested Next
- Spark (if a variation is feature-ready)
- Steelman (if one variation is a leading candidate worth stress-testing)
- Magi (if the user wants to choose between variations formally)
```

---

## 8. Handoff Routing

| Outcome | Next agent | Why |
|---------|-----------|-----|
| Variation is feature-shaped | **Spark** | Convert to feature spec |
| User wants to choose between top variations | **Magi** | Formal multi-perspective deliberation |
| Variation needs stress-testing | Riff `steelman` | Strongest case for/against |
| Hybrid is unclear, needs more divergence | Riff `crazy8` | Rapid 8-variation pass |
| Variation is too packed, needs cutting | **Void** | YAGNI verification |
