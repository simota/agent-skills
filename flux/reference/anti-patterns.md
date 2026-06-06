# Anti-Patterns

**Purpose:** Thinking traps that undermine Flux's output quality, and how to detect/prevent them.
**Read when:** You need to quality-check your output before CRYSTALLIZE, or when output feels shallow.

---

## Contents
- Anti-Pattern Catalog
- Detection Checklist
- Recovery Strategies

---

## Anti-Pattern Catalog

### 1. Surface Reframing (表層的リフレーミング)

**What it is:** Changing the words without changing the thinking. The "reframed" problem is just a synonym or rephrasing of the original.

**Example:**
- Original: "User retention is low."
- Bad reframe: "We're losing users." (same thing, different words)
- Good reframe: "Our product is optimized for first impressions, not for habits." (genuinely different lens)

**Detection signals:**
- The reframing suggests the exact same actions as the original.
- Removing the reframed statement changes nothing about the approach.
- The reframing doesn't challenge any assumption.

**Prevention:**
- Apply the "action test": Does this reframing suggest at least one action the original would not?
- Trace back to the framework: Which specific framework step produced this? If you can't trace it, it's likely surface-level.
- Check assumption challenge: Which assumption was reversed or eliminated to produce this reframing?

---

### 2. Framework Abuse (フレームワーク乱用)

**What it is:** Mechanically filling in framework templates without genuine thought. The framework becomes a checkbox exercise.

**Example:**
- Running SCAMPER and producing: "Substitute: substitute X with Y. Combine: combine X and Z..." without any genuine insight.
- Listing assumptions that are trivially true just to hit the "10-20" target.

**Detection signals:**
- Outputs feel formulaic — could have been generated for any problem.
- Framework-specific terminology dominates over problem-specific insight.
- The 10th assumption is as insightful as the 1st (no deepening).

**Prevention:**
- Quality over quantity: 7 genuine assumptions beat 20 shallow ones.
- Problem-specific language: Output should use the user's domain vocabulary, not just framework vocabulary.
- Surprise check: Would the user find at least 3 items genuinely unexpected?

---

### 3. Convergence Failure (収束不足)

**What it is:** Generating many divergent ideas without converging them into actionable reframings. The output is a brainstorm dump, not a synthesized insight.

**Example:**
- 30 assumption reversals, 15 SCAMPER ideas, 10 lateral thinking prompts... but no clear reframed problem statements.

**Detection signals:**
- Output is a long list without prioritization or synthesis.
- No Insight Matrix or ranking.
- No actionable next steps or hypotheses.
- The user would need to do significant work to extract value.

**Prevention:**
- Always complete the CRYSTALLIZE phase — never stop at COMBINE or SHIFT.
- Force ranking: Every insight must be rated on novelty and actionability.
- Limit reframings to 3-5 and make each one fully developed.
- Include Action Hypotheses for top reframings.

---

### 4. False Insight (偽の洞察)

**What it is:** An insight that sounds new and profound but actually says the same thing as conventional wisdom in different words.

**Example:**
- "The real problem isn't technology, it's people." (This is almost always true and rarely actionable.)
- "We need to focus on the user." (Too generic to be an insight.)

**Detection signals:**
- The insight is true for virtually any problem, not just this one.
- No one would disagree with it.
- It doesn't suggest a specific, non-obvious action.

**Prevention:**
- Specificity test: Does this insight apply to this problem and not others?
- Disagreement test: Would a reasonable person potentially disagree?
- Action test: Does it suggest a concrete, non-obvious next step?
- Novelty test: Would the user have this insight without Flux's intervention?

---

### 5. Anchoring to the First Reframe (初回アンカリング)

**What it is:** The first reframing dominates all subsequent ones. Later reframings are variations on the first, not genuinely independent perspectives.

**Detection signals:**
- All reframings share the same underlying assumption.
- Later reframings feel like elaborations of the first.
- The Insight Matrix shows all insights from the same framework.

**Prevention:**
- Generate reframings from different frameworks independently.
- Check: Can I trace each reframing to a different framework or combination?
- Apply Serendipity Injection specifically to break the first frame's gravity.

---

### 6. Complexity Theater (複雑さの演出)

**What it is:** Making the output look sophisticated (matrices, diagrams, scores) while the underlying thinking is shallow.

**Detection signals:**
- Removing the formatting reveals empty or repetitive content.
- Scores and ratings feel arbitrary (no clear basis).
- The matrix could be filled in randomly with similar results.

**Prevention:**
- Content-first: Write the insight in plain language first, then format.
- Justify scores: Every H/M/L rating should have a one-line justification.
- Peer check: Would a domain expert find the content valuable after removing formatting?

---

### 7. Domain Blindness (ドメイン盲目)

**What it is:** Applying frameworks without understanding the problem domain, producing reframings that are technically possible but practically irrelevant.

**Detection signals:**
- Reframings ignore key domain constraints.
- Cross-domain analogies are structurally incorrect.
- The user would immediately dismiss the output as naive.

**Prevention:**
- Spend adequate time in CLASSIFY understanding the domain.
- Check each reframing against stated constraints.
- Include domain-specific considerations in the Blind Spot Report.
- When domain knowledge is insufficient, flag it explicitly.

---

## Detection Checklist

Run this checklist before finalizing CRYSTALLIZE output:

```markdown
## Quality Gate

### Reframing Quality
- [ ] Each reframing suggests at least one action the original would not (Action Test)
- [ ] Each reframing traces to a specific framework application (Traceability Test)
- [ ] Reframings are genuinely independent (not variations of the same idea)
- [ ] At least one reframing challenges a high-confidence assumption

### Insight Quality
- [ ] Insights are specific to this problem (Specificity Test)
- [ ] At least 3 insights would surprise the user (Surprise Test)
- [ ] A reasonable person could disagree with at least 2 insights (Disagreement Test)
- [ ] Insights suggest concrete, non-obvious actions (Action Test)

### Process Quality
- [ ] Assumptions list goes beyond the obvious (deepening achieved)
- [ ] Serendipity Injection produced at least one unexpected connection
- [ ] Output is converged (3-5 reframings, not a dump)
- [ ] Scores/ratings are justified, not arbitrary

### Domain Quality
- [ ] Domain constraints are respected
- [ ] Cross-domain analogies are structurally valid
- [ ] Domain-specific vocabulary is used correctly
- [ ] Insufficient domain knowledge is flagged explicitly
```

---

## Recovery Strategies

When an anti-pattern is detected mid-pipeline:

| Anti-Pattern | Recovery Action |
|-------------|----------------|
| Surface Reframing | Return to CHALLENGE phase; reverse a different, deeper assumption |
| Framework Abuse | Stop the framework; ask "What do I actually know about this specific problem?" |
| Convergence Failure | Force immediate CRYSTALLIZE; pick top 3-5 and develop fully |
| False Insight | Apply the 4 tests (Specificity, Disagreement, Action, Novelty); discard failures |
| First-Reframe Anchoring | Apply Serendipity Injection; force next reframing from a different pillar |
| Complexity Theater | Strip formatting; rewrite in plain language; add formatting only where it adds clarity |
| Domain Blindness | Pause and gather more domain context; ask user if needed |
