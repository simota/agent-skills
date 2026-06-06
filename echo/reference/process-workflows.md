# Process & Workflows Reference

## Daily Process (6-Step)

### 1. PRE-SCAN - Predictive Analysis

Before starting the walkthrough:
1. Run pattern-based friction detection on the flow
2. Identify high-risk areas (forms, checkout, settings)
3. Note predicted issues to validate during walkthrough
4. Generate Pre-Walkthrough Risk Assessment

### 2. MASK ON - Select Persona + Context

Choose from Core, Extended, or **Saved Service-Specific** personas AND add environmental context:
1. Check for saved personas in `.agents/personas/{service}/`
   - If found: offer to use saved personas (ON_PERSONA_REVIEW)
   - If not found: offer to generate (BEFORE_PERSONA_GENERATION)
2. Select primary persona (e.g., "Mobile User" or "first-time-buyer")
3. Add context scenario (e.g., "Rushing Parent" or "Commuter")
4. Adjust requirements based on context
5. Consider multi-persona comparison if comprehensive analysis needed
6. **Activate Cognitive Profile (if present)**:
   a. Load Beliefs → set mental model expectations for gap detection
   b. Load Hierarchical Goals → identify session objective and conflict points
   c. Load Emotional Profile → set baseline mood and frustration threshold
   d. Load Values → configure non-negotiable exit conditions
   e. Load Stance → prime UX pattern reactions
   f. Load Communication Style → set voice parameters for SPEAK step

### 3. WALK - Traverse the Path

1. Pick a scenario: "Sign up," "Reset Password," "Search for Item," "Checkout"
2. Simulate the steps mentally based on the current UI/Code
3. Assign emotion scores using:
   - Basic: -3 to +3 linear scale
   - Advanced: Valence/Arousal/Dominance (when detailed analysis needed)
   - CPM-adjusted: Apply baseline_mood offset and frustration_threshold (if Cognitive Profile active)
4. Track cognitive load at each step (Intrinsic/Extraneous/Germane)
5. Detect mental model gaps when confusion occurs
   - CPM: Cross-reference with Beliefs.mental_models (if Cognitive Profile active)
6. Monitor for cognitive biases and dark patterns
   - CPM: Factor in Values.non_negotiables as exit triggers; Stance.risk_appetite for bias vulnerability (if Cognitive Profile active)
7. Note implicit expectation violations
8. Identify latent needs (JTBD analysis)
   - CPM: Use Hierarchical Goals to contextualize needs (if Cognitive Profile active)
9. For Accessibility persona: Run the WCAG checklist
10. For Competitor persona: Note expectation gaps
    - CPM: Use Communication Style.reference_frame for comparison anchors (if Cognitive Profile active)
11. Evaluate interruption recovery capability
12. CPM Decision Point Simulation (if Cognitive Profile active):
    - Evaluate goal_conflicts at choice screens
    - Apply value_axes to tradeoff decisions
    - Use decision_style to determine time spent and approach

### 4. SPEAK - Voice the Friction

- Describe the experience in the first person ("I feel...")
- Point out exactly where confidence was lost
- Highlight text that didn't make sense
- Include emotion score with each observation
- Explain the cognitive mechanism behind confusion
- Articulate unmet latent needs
- Flag any dark patterns detected
- CPM Communication Style integration (if Cognitive Profile active):
  - Match vocabulary_level and expression_style to persona voice
  - Apply complaint_pattern (self-blame vs system-blame vs silent)
  - Use Emotional Profile.reactivity to modulate score magnitude

### 5. ANALYZE - Deep Pattern Recognition

1. Identify emotion journey pattern (Recovery, Cliff, Rollercoaster, etc.)
2. Apply Peak-End Rule to prioritize fixes
3. Calculate Cognitive Load Index totals
4. Generate JTBD analysis for key friction points
5. If multi-persona: Create cross-persona comparison matrix
6. Run CPM Consistency Check (if Cognitive Profile was active):
   - Axis 1: Adherence — did simulation match defined profile?
   - Axis 2: Consistency — were dimensions internally coherent throughout?
   - Axis 3: Naturalness — did it feel like a real person, not a checklist?
   - Calculate Fidelity Score (15-item checklist → percentage → High/Moderate/Low)
   - See `reference/cognitive-persona-model.md` for full checklist

### 6. PRESENT - Report the Experience

Create a report including:
- **Persona Profile**: Name, context scenario, goal
- **Emotion Score Summary**: Table with steps, actions, scores
- **The Journey**: Step-by-step with scores, feelings, expectations, gaps
- **Key Friction Points**: Priority ordered with JTBD analysis
- **Dark Pattern Detection**: Severity and patterns found
- **Canvas Journey Data**: Mermaid journey diagram for visualization

---

## Simulation Standards

**Good feedback**: Specific persona, emotional, scored, non-technical
- "Persona: 'Rushing Mom' | Score: -3 😡 I clicked 'Buy', but nothing happened. Did it work?"

**Bad feedback**: Technical solutions, vague, developer perspective
- ❌ "The API response time is too high" (users don't say "API")
- ❌ "It's hard to use" (why? who? how hard?)
- ❌ "This works as designed" (users don't care)

---

## Multi-Engine Mode

Three AI engines each play a different user persona to validate UI flows (**Persona pattern**). Triggered by Echo's own judgment or when instructed via Nexus with `multi-engine`.

### Engine × Persona Mapping

| Engine | Persona | Command | Fallback |
|--------|---------|---------|----------|
| Codex | Senior Engineer | `codex exec --full-auto` | Claude subagent |
| Antigravity | Beginner User | `agy -p --dangerously-skip-permissions --log-file <path>` (silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection`) | Claude subagent |
| Claude | Accessibility User | Claude subagent (Task) | — |

> Persona assignments are not fixed. Echo may choose the optimal combination for the target UI.
> When an engine is unavailable (`which` fails), Claude subagent takes over.

### Loose Prompt Design

Pass only: (1) Persona profile (age, tech level, context in 2-3 lines), (2) Target UI flow (transitions/steps), (3) Output format (confusion points: location, emotion, reason). Do NOT pass evaluation checklists or heuristic lists.

### Result Integration

1. Collect walkthrough results from all 3 personas
2. Consolidate findings (multiple personas confused = higher severity)
3. Organize by location while preserving each persona's perspective
4. Echo composes final report with cross-persona priority ranking

---

## AUTORUN _STEP_COMPLETE Format

```text
_STEP_COMPLETE:
  Agent: Echo
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output: [Persona / Flow tested / Average score / Key friction points]
  Next: Palette | Muse | Canvas | Builder | VERIFY | DONE
```

---

## NEXUS_HANDOFF Format

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: Echo
- Summary: 1-3 lines
- Key findings / decisions:
  - Persona used: [Persona name]
  - Flow tested: [Flow name]
  - Average emotion score: [Score]
  - Critical friction points: [List]
- Artifacts (files/commands/links):
  - Echo report (markdown)
  - Journey map data (mermaid)
- Risks / trade-offs:
  - [Accessibility issues found]
  - [Competitor gaps identified]
- Open questions (blocking/non-blocking):
  - [Clarifications needed]
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name if any]
  - Question: [Question for user]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] -> A: [User's answer]
- Suggested next agent: Palette | Muse | Canvas | Builder
- Next action: CONTINUE (Nexus automatically proceeds)
```
