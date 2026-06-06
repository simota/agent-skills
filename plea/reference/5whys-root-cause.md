# 5 Whys Root-Cause Reference

Purpose: Drive past surface symptoms to the true unmet need by iteratively asking "why?" until a root cause — not another symptom — is reached. Originated by Sakichi Toyoda, formalized inside the Toyota Production System by Taiichi Ohno. In Plea's hands, the technique is applied to *user demand* rather than manufacturing defects: when a user asks for X, why do they really want it? Stops solution-first thinking and exposes the latent job underneath.

## Scope Boundary

- **plea `5whys`**: iterative why-chain on a stated user request, ending in a root-cause demand (not a feature). Outputs cause-tree + restated unmet need.
- **plea `request` (default)**: collects requests as stated. Use `5whys` when a request feels solution-flavored or shallow.
- **plea `need`**: surveys multiple blind spots laterally. `5whys` drills vertically into one.
- **plea `jtbd`**: structures the job around forces and stages. `5whys` is faster, lighter, and complementary — often used to clean up a request *before* JTBD modeling.
- **Researcher (elsewhere)**: owns root-cause analysis grounded in real interview transcripts. Plea generates synthetic why-chains as hypothesis; Researcher validates.
- **Scout (elsewhere)**: applies 5 Whys to *bug* root causes. Plea applies it to *demand* root causes — symptom is "user said X," not "system did Y."
- **Voice (elsewhere)**: real feedback. 5 Whys on real review text is Voice + Researcher; 5 Whys on hypothetical user voice is Plea.

## Workflow

```
SYMPTOM   →  capture the user request verbatim ("I want X")
          →  tag it as the level-0 symptom

WHY-CHAIN →  ask "why does the user want this?" — answer in user voice
          →  repeat at least 5 times. Each answer becomes the next level's symptom.
          →  stop when the next "why" yields the same answer (root reached) or
          →  when you cross from product-domain to life-domain (out of scope)

LATERAL   →  at each level, also ask "what other reasons could cause this?"
          →  this turns the chain into a fishbone (Ishikawa) — multiple roots possible

CAUSAL    →  verify each link is causal ("because") not sequential ("and then")
          →  reject any link that's "after" instead of "because"

RESTATE   →  rewrite the original request as the root-level unmet need
          →  e.g. "Add dark mode" → root: "I work at night and feel the product
          →  ignores my context"

DELIVER   →  hand restated need + cause-tree to Spark or Accord
```

## When to Stop (Vertical vs Lateral Why)

**Vertical why** descends into deeper causes. Stop vertical descent when:
1. The next "why" answer is identical to the current one — you've hit the root.
2. The cause crosses outside the product's reach (the user's life situation, identity, broader market) — note it, but don't try to "fix" it.
3. You've reached an emotional or identity-level need ("I want to feel competent at work") — these are usually genuine roots.
4. You've reached 5+ levels and the chain still feels real — that's typical, not a problem.

**Lateral why** explores siblings of the current cause. Stop lateral expansion when:
1. You have 3-5 independent branches at a level — broader than that adds noise.
2. New branches are restatements of existing ones in different words.

A good 5-Whys output is shaped like a fishbone, not a single line.

## Causal vs Sequential Trap

Each link must be **because**, not **and then**.

| Trap | Example | Why it fails |
|------|---------|--------------|
| Sequential | "User clicks export → and then waits → and then gets frustrated" | Describes timeline, not causation |
| Causal | "User is frustrated *because* exports take 90s *because* the report runs uncached *because* the cache invalidates on every save" | Each link explains the prior |
| Blame | "User is wrong because they don't read docs" | Targets a person, not a cause |
| Tautology | "User wants speed because they want speed" | Restates without explaining |

If you cannot say "because" between two links and have it make sense, the link is wrong.

## Fishbone Integration (Ishikawa Diagram)

When the chain branches at the first or second why, structure the result as an Ishikawa diagram:

```
                               [Root unmet need]
                                       ↑
   ┌─────────┬─────────┬───────────────┼───────────────┬─────────┐
   │         │         │               │               │         │
[Process] [Tooling] [Knowledge]   [Environment]   [Social]   [Identity]
   │         │         │               │               │         │
  why?      why?      why?            why?            why?      why?
```

The 6 standard Ishikawa categories (People / Process / Tools / Materials / Environment / Measurement) translate for product demand to: Knowledge / Process / Tooling / Content / Environment / Identity. Use whichever spread makes the cause-tree balanced.

## Why-Chain Template

```yaml
WHY_CHAIN:
  level_0_symptom: "[Verbatim user request]"
  persona: "[Channeled persona name]"
  chain:
    - why_1:
        question: "Why does the persona want this?"
        answer: "[In user voice]"
        causal_check: "Confirms 'because' link to level_0"
    - why_2:
        question: "Why does that matter?"
        answer: "[In user voice]"
    - why_3: { ... }
    - why_4: { ... }
    - why_5: { ... }
  lateral_branches:
    - "[Alternative cause at level 2]"
    - "[Alternative cause at level 3]"
  root_unmet_need: "[Rewritten request at root level]"
  out_of_scope_root: "[If root crosses out of product domain, note it here]"
```

## Anti-Patterns

- **Jumping to solutions**: answering "why?" with another feature ("because we should add Y"). The answer must be a *cause*, not a *fix*.
- **Blaming people**: "because users don't read docs / are lazy / don't understand." Reroute to system causes.
- **Single-thread assumption**: forcing a linear 1→2→3→4→5 chain when reality has multiple roots. Use the fishbone.
- **Stopping at level 2 or 3**: the first 2 whys usually surface only restated symptoms. Push to 5+.
- **Crossing into life-domain and trying to fix it**: if the root is "I want to feel valued at my job," your product can't fix that — note it as out-of-scope and stop.
- **Tautological loops**: "wants speed because needs speed" — fail the causal check.
- **Skipping the lateral pass**: vertical-only chains miss 60-70% of root causes. Always branch at least once.
- **Treating the root as proven**: the chain is a synthetic hypothesis. Tag `synthetic: true` and hand off to Researcher / Voice for confirmation.

## Handoff

- **To Researcher**: synthetic root-need as hypothesis for real-user follow-up interviews. Researcher tests whether real users articulate the same root.
- **To Voice**: cross-check root against existing review/support text — search for keywords from the root statement; convergence raises confidence.
- **To Spark**: hand off the *restated root unmet need*, not the original surface request. Spark designs against the root, which usually surfaces more diverse solution candidates.
- **To Accord**: root-need becomes a top-level requirement; surface symptoms become acceptance criteria sub-bullets.
- **To Scout**: when the root reveals a likely *implementation* defect rather than missing functionality, route to Scout for code-level root-cause analysis.
- **To Cast**: if certain personas consistently bottom out at the same root, that's a persona-archetype signal worth feeding back.
