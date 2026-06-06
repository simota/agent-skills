# Subsystems

Darwin's 7 internal subsystems that compose the SENSE→ASSESS→EVOLVE→VERIFY→PERSIST framework.

> **Prior art Darwin's mutation operators borrow from (2026-05 refresh)**
> - **AlphaEvolve** (Google DeepMind, Gemini-powered evolutionary coding agent, arXiv 2506.13131): combines a MAP-Elites-inspired strategy with an island-based population model to maintain both performance and diversity. Notably discovered a 48-scalar-multiplication procedure for 4×4 complex matrix multiplication — the first improvement over Strassen's algorithm in 56 years — and was applied internally at Google to data-center scheduling and LLM training acceleration. Darwin's **Affinity Evolver** and **Fitness Scorer** treat MAP-Elites-style diversity preservation as the reference pattern: never collapse Dynamic AFFINITY into a single dominant agent stack when phase signals are mixed; preserve niche agents the way MAP-Elites preserves behavioral cells. Source: `https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/`.
> - **Anthropic Dreaming** (research preview, 2026-05-06): between-session memory consolidation that extracts patterns from past sessions, surfaces recurring mistakes, and keeps shared team preferences fresh. Darwin's **Journal Synthesizer** is the in-ecosystem analogue — both produce reusable patterns; both must be governed by a review-before-merge default to prevent silent memory drift. Source: `https://claude.com/blog/new-in-claude-managed-agents`.
> - **Anthropic Outcomes** (public beta, 2026-05-06): rubric-driven success criteria with measured +up-to-10 pp task-success lift. Darwin's **Trigger Engine** ET-02 (Quality Plateau) should now emit Outcomes-style rubrics as the proposed remediation, not just generic "improvement chain" text.

---

## 1. Lifecycle Detector

Determines the current project phase from environmental signals. Runs automatically at the start of every Darwin invocation and on ET-07 trigger.

**Process:**
1. Collect git metrics (commit frequency, file types, branch patterns)
2. Analyze file structure (test presence, CI configs, deploy configs)
3. Score each phase (0.0-1.0) based on signal matches
4. Select highest-scoring phase (or mixed if <0.60)
5. Compare with previous detection for transition events

## 2. Trigger Engine

Evaluates trigger conditions (ET-01 through ET-08 as the base set; ET-09 *Official Spec Conformance drift* in `official-fitness-criteria.md`; ET-10 *Framework End-of-Life drift* added 2026-05 — see `evolution-actions.md`) and fires appropriate evolution actions.

**Process:**
1. Check each trigger condition against current state
2. Prioritize triggered actions (ET-05 emergency > others)
3. Execute actions in priority order
4. Log trigger events to ECOSYSTEM.md

## 3. Journal Synthesizer

Analyzes `.agents/*.md` journals to extract cross-cutting patterns.

**Process:**
1. Scan all journal files for entries with `reusable: true` tag or high-value patterns
2. Cluster related entries across agents
3. Generate Pattern Cards: `{pattern_id, source_agents, insight, apply_when, confidence}`
4. Store in ECOSYSTEM.md Cross-Agent Discoveries section

## 4. Affinity Evolver

Computes Dynamic AFFINITY overrides based on lifecycle, usage, and feedback.

**Process:**
1. Get current lifecycle phase
2. Map phase to dominant agent profiles (see Lifecycle table)
3. Cross-reference with actual usage from PROJECT.md
4. Apply feedback modifiers from Reverse Feedback
5. Output override entries for ECOSYSTEM.md

## 5. Discovery Propagator

Creates knowledge transfer briefs when one agent's finding benefits others.

**Brief format:**
```
## DISCOVERY_BRIEF
Source: [agent]
Date: YYYY-MM-DD
Finding: [what was discovered]
Relevant to: [target agents]
Recommended action: [what target agents should consider]
Priority: HIGH/MEDIUM/LOW
```

## 6. Staleness Detector

Evaluates each agent's ongoing relevance to the current project.

**Process:**
1. Calculate RS for every agent in the ecosystem
2. Flag agents with RS <40 as Dormant
3. Flag agents with RS <20 as Sunset candidates
4. Cross-reference with lifecycle phase (some dormancy is expected)
5. Generate Staleness Report with recommended actions

## 7. Fitness Scorer

Calculates the Ecosystem Fitness Score (EFS) across 5 dimensions.

**Process:**
1. Calculate each dimension score (0-100)
2. Apply weights: Coverage(25%) + Coherence(20%) + Activity(20%) + Quality(20%) + Adaptability(15%)
3. Compute trend by comparing with previous EFS (up/down/stable)
4. Assign grade (S/A/B/C/D/F)
5. Generate dashboard summary
