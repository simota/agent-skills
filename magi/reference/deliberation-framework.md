# Deliberation Framework

The three-perspective evaluation methodology that forms the core of Magi's decision-making process.

---

## The Three Perspectives

### Logos (The Analyst)

**Core Lens:** Technical correctness, data-driven analysis, logical consistency

**Evaluation Heuristics:**
- Does the evidence support the claim? (Empirical validation)
- What do the metrics say? (Quantitative assessment)
- Is the reasoning logically sound? (Deductive/inductive validity)
- What are the technical constraints? (Feasibility analysis)
- Are there proven precedents? (Historical data)

**Key Questions:**
1. What does the data show?
2. What are the technical risks and their probabilities?
3. Is this approach technically feasible within constraints?
4. What are the performance implications?
5. Does this follow engineering best practices?

**Typical Biases to Guard Against:**
- **Analysis paralysis**: Demanding perfect data before acting
- **Sunk cost fallacy**: Favoring technically elegant solutions that ignore human factors
- **Techno-optimism**: Overestimating technical solutions to human problems
- **Complexity bias**: Preferring sophisticated solutions when simple ones suffice

---

### Pathos (The Advocate)

**Core Lens:** User impact, team wellbeing, long-term maintainability, ethics

**Evaluation Heuristics:**
- How does this affect the people who use it? (User experience)
- What burden does this place on the team? (Developer experience)
- Will future developers understand this? (Maintainability)
- Who gets hurt if this goes wrong? (Impact assessment)
- Does this align with ethical standards? (Moral evaluation)

**Key Questions:**
1. How will users be affected by this decision?
2. What is the cognitive load on the development team?
3. Will this create technical debt that burdens future maintainers?
4. Are there accessibility or inclusivity concerns?
5. What is the worst-case human impact?

**Typical Biases to Guard Against:**
- **Status quo bias**: Resisting change to protect comfort
- **Empathy overextension**: Letting emotional considerations override all else
- **Scope creep through compassion**: Adding features for edge-case users at high cost
- **Risk aversion**: Blocking beneficial changes due to fear of disruption

---

### Sophia (The Strategist)

**Core Lens:** Business alignment, time-to-market, risk/return balance, harmony

**Evaluation Heuristics:**
- Does this serve the business objective? (Strategic alignment)
- What is the return on investment? (ROI analysis)
- How quickly can we deliver value? (Time-to-market)
- What is the risk-adjusted outcome? (Risk/return balance)
- Does this create or resolve tension? (Systemic harmony)

**Key Questions:**
1. Does this align with business goals and priorities?
2. What is the opportunity cost of this approach?
3. How does this affect time-to-market?
4. What is the competitive impact?
5. Does this create sustainable value or short-term gain?

**Typical Biases to Guard Against:**
- **Short-termism**: Optimizing for immediate results at long-term cost
- **Survivorship bias**: Copying strategies that worked elsewhere without context
- **Overconfidence in prediction**: Assuming market/business outcomes are certain
- **Compromise fallacy**: Seeking middle ground when one extreme is correct

---

## Perspective Independence Protocol

To ensure each perspective provides genuine, uninfluenced analysis:

### Sequential Isolation Rule

1. **Logos evaluates first** based purely on technical evidence
2. **Pathos evaluates second** based purely on human impact (without seeing Logos verdict)
3. **Sophia evaluates third** based purely on strategic value (without seeing prior verdicts)
4. **Synthesis happens only after all three perspectives are documented**

### Anti-Anchoring Measures

- Each perspective must state its position BEFORE seeing others
- Use structured prompts that focus on domain-specific criteria
- Explicitly note when a perspective has "nothing to add" (rather than forcing agreement)
- Flag when one perspective's conclusion was influenced by another's framing

---

## Engine Independence Protocol

When using Engine Mode, independence is achieved through **physical separation** rather than simulated isolation:

### Physical Independence

1. **Claude analyzes first** — completes integrated analysis before any external engine calls
2. **External engines execute in parallel** — Codex and Gemini receive identical context, run independently
3. **No cross-contamination** — Claude's analysis is stored before external outputs are collected
4. **Identical context delivery** — All engines receive the same decision framing and context

### Anti-Contamination Rules

- Claude **must not** modify its analysis after seeing external engine outputs
- External engine prompts **must not** include Claude's position or reasoning
- If re-deliberation occurs, all engines re-evaluate independently

### Advantages Over Simulated Independence

| Aspect | Simple Mode (Simulated) | Engine Mode (Physical) |
|--------|-------------------------|------------------------|
| Independence guarantee | Best-effort isolation | True process separation |
| Model diversity | Single model, multiple prompts | Multiple models |
| Bias correlation | Correlated (same model) | Uncorrelated (different training) |
| Failure mode | Single point of failure | Graceful degradation |

---

## Confidence Scoring Guide

Each perspective assigns a confidence score to its assessment:

| Score | Level | Meaning | Basis |
|-------|-------|---------|-------|
| 90-100 | Certain | Mathematical/logical certainty | Formal proof, overwhelming data |
| 75-89 | High | Strong evidence supports conclusion | Multiple data points, clear precedent |
| 60-74 | Moderate | Reasonable confidence with some gaps | Limited data, some assumptions |
| 40-59 | Low | Significant uncertainty | Sparse data, many assumptions |
| < 40 | Speculative | Educated guess at best | No data, pure reasoning |

### Confidence Calibration Rules

- **Never claim 100** unless mathematically provable
- **Below 40** triggers mandatory "Uncertainty Disclaimer" in output
- **Average confidence below 50** across all perspectives triggers re-deliberation or escalation
- **Large confidence gap** (>30 points between perspectives) should be explicitly discussed

---

## Engine Confidence Scoring

Engine Mode uses the same 0-100 confidence scale, with additional considerations for cross-engine comparison.

### Cross-Engine Confidence Distribution

Different engines may have systematic confidence biases:

| Engine | Typical Range | Notes |
|--------|--------------|-------|
| Claude | 60-85 | Tends toward moderate confidence with calibrated uncertainty |
| Codex | 55-80 | May show lower confidence on non-code decisions |
| Gemini | 50-85 | Wider range, may be more decisive on strategic questions |

### Engine Confidence Rules

- **95 cap rule**: Same as Simple Mode — no engine should claim confidence > 95 unless mathematically provable
- **Cross-engine gap > 30**: Flag for review, may indicate different context interpretation
- **All engines < 50**: Re-deliberate with more context or fall back to Simple Mode
- **Single engine at 0**: Likely parse failure — check error log before including in vote

---

## Conflict Patterns and Their Meaning

### Logos vs Pathos (Technical vs Human)

**Pattern:** "Technically optimal but humanly costly"
**Typical scenario:** Performance optimization that makes code unmaintainable
**Resolution signal:** Pathos usually wins for internal tools; Logos for performance-critical systems

### Logos vs Sophia (Technical vs Business)

**Pattern:** "Technically correct but strategically wrong"
**Typical scenario:** Perfect architecture that takes too long to build
**Resolution signal:** Sophia usually wins for time-sensitive decisions; Logos for foundational decisions

### Pathos vs Sophia (Human vs Business)

**Pattern:** "Good for people but bad for business" (or vice versa)
**Typical scenario:** Developer experience improvement with no business ROI
**Resolution signal:** Context-dependent; often the dissenting voice carries important warnings

### All Three Conflict (Three-Way Split)

**Pattern:** Each perspective sees a fundamentally different problem
**Meaning:** The decision may be poorly framed or the scope too broad
**Action:** Reframe the question or decompose into smaller decisions

---

## Re-Deliberation Triggers

Restart deliberation when:

1. **New evidence emerges** that changes a perspective's assessment by >20 confidence points
2. **Constraints change** (budget, timeline, team composition)
3. **User provides additional context** that wasn't in the original framing
4. **Implementation reveals** assumptions were incorrect
5. **Split verdict (1-1-1)** and user requests deeper analysis
6. **All perspectives have confidence below 50**

### Re-Deliberation Protocol

1. Identify which perspective(s) are affected by new information
2. Re-evaluate only the affected perspective(s)
3. Conduct a new vote
4. Compare old and new verdicts
5. Document what changed and why
