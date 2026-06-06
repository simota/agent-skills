# SCAMPER Creativity Technique Reference

Purpose: Structured idea-modification checklist developed by Bob Eberle (1971), adapting Alex Osborn's earlier creative-thinking questions into seven prompt lenses — **S**ubstitute, **C**ombine, **A**dapt, **M**odify (magnify/minify), **P**ut to other use, **E**liminate, **R**everse. SCAMPER fires best when an existing object, process, or service exists and the goal is incremental transformation rather than first-principles reinvention.

## Scope Boundary

- **flux `scamper`**: lens-by-lens transformation of an existing artifact. Produces a 7-cell idea matrix with prompt-bank-driven ideation per lens.
- **flux `reframe` (default)**: full DEEP pipeline — assumptions, cross-domain combine, perspective shift, crystallize. Use when the *frame*, not the artifact, is stuck.
- **flux `cross`**: cross-domain Bisociation only. SCAMPER is intra-artifact modification; `cross` is inter-domain knowledge transfer.
- **flux `challenge`**: First Principles and Assumption Reversal. Use when the question is "should this exist at all?" not "how do we modify it?".
- **flux `analogy`**: structural mapping from a source domain. SCAMPER lens A (Adapt) is analogy-adjacent but shallower — `analogy` goes deeper into structural alignment.
- **riff (elsewhere)**: iterative dialogue brainstorming. SCAMPER is a single-pass checklist; Riff is multi-turn co-creation.
- **spark (elsewhere)**: feature proposal from data. SCAMPER feeds Spark with raw idea candidates.

## Workflow

```
ENTER    →  receive target artifact (product, process, feature, service)
         →  verify it is concrete enough for lens-by-lens probing

PROBE    →  apply each of 7 lenses with its prompt bank
         →  generate ≥3 ideas per lens (minimum 21 raw ideas)

FILTER   →  ASN test per idea (Actionability / Specificity / Novelty)
         →  drop synonym-substitutions and trivially-true modifications

MATRIX   →  arrange surviving ideas into 7-lens × N-ideas grid
         →  flag lens-pair tensions (e.g., Eliminate vs Combine)

DELIVER  →  hand to Spark (feature proposals) or Magi (decision among
            modified variants) with lens citations
```

## The 7 Lenses (Eberle 1971)

| Lens | Core question | Prompt bank | Fires best when |
|------|---------------|-------------|-----------------|
| **S** Substitute | What can be swapped? | Swap material, person, rule, ingredient, place, approach | Component is taken for granted |
| **C** Combine | What can be merged? | Combine purposes, audiences, products, ideas, services | Two adjacent things share users |
| **A** Adapt | What can be borrowed? | Adapt from nature, other industry, history, child's view | Stuck on novel problem with old precedent |
| **M** Modify | What can be magnified or minified? | Larger, smaller, faster, slower, stronger, lighter, more frequent | Scale or intensity is wrong |
| **P** Put to other use | What else could this serve? | New audience, new context, new market, new lifecycle stage | Asset is underutilized |
| **E** Eliminate | What can be removed? | Drop step, feature, role, constraint, decoration, dependency | Bloat or YAGNI suspected |
| **R** Reverse | What can be inverted? | Reverse order, roles, polarity, direction, cause-effect | Flow feels arbitrary |

## Lens Selection Heuristics

| Symptom | Strongest lenses |
|---------|------------------|
| "It's too complicated" | E (Eliminate), M (minify) |
| "It's too generic" | S (Substitute), P (other use) |
| "It's too slow" | M (modify timing), E (eliminate steps), R (reverse order) |
| "Users don't understand it" | A (adapt familiar metaphor), S (substitute language) |
| "Competitors copy us" | C (combine unique pairs), R (reverse industry default) |
| "We've optimized everything" | R (reverse), P (other use) |

## Anti-Patterns

- Running SCAMPER alone as the entire reframing — produces incremental ideas, never paradigm shifts. Always pair with `challenge` or `shift` upstream.
- Stopping at the first idea per lens — the first idea is usually the obvious one. Push to ≥3 per lens to escape the local maximum.
- Treating "Combine" as "list features side by side" — Combine means *fusion* (shared mechanism, shared user, shared moment), not concatenation.
- Skipping Reverse because it feels silly — Reverse is the highest-novelty lens; silliness is the signal it is working.
- Substitute-as-synonym — "use blue instead of red" passes Substitute syntactically but fails ASN. Substitute the *function*, not the label.
- Eliminate without asking *what depends on this* — produces fragile suggestions Builder cannot ship.
- Applying SCAMPER to a vague target ("our company") — lenses need a concrete artifact. Narrow scope first.
- Reporting all 21+ raw ideas without filtering — overwhelms downstream agents. CRYSTALLIZE to top 5-7 cross-lens candidates.

## Handoff

- **To Spark**: surviving ideas with lens citations as feature proposal candidates.
- **To Magi**: when 3+ modified variants compete and a decision is needed.
- **To Riff**: when one cell looks promising but underdeveloped — open iterative dialogue on that cell.
- **To Omen**: Eliminate and Reverse cells that may carry hidden failure modes — pre-mortem before committing.
- **To `analogy`**: Adapt-lens hits that deserve deeper structural mapping, not just surface borrowing.
