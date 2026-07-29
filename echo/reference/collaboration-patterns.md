# Echo Collaboration Patterns Reference

Detailed collaboration patterns and handoff formats for Echo agent.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT PROVIDERS                          │
│  Field → Persona data                                │
│  Voice → Real user feedback                           │
│  Pulse → Quantitative metrics                                     │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
            ┌─────────────────┐
            │      ECHO       │
            │  UX Validation Engine │
            └────────┬────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT CONSUMERS                          │
│  Palette → Interaction improvements                             │
...
```

## Pattern A: Validation Loop (Echo ↔ Palette)

```
Echo (friction discovered: -2.5/5)
  ↓ handoff
Palette (improvement: add loading state)
  ↓ handoff back
Echo (post-improvement validation: +3.8/5)
  ↓ validation complete
```

**Handoff Format (Echo → Palette):**
```markdown
## Echo → Palette Handoff

**Friction Point**: [Specific problem location]
**Persona**: [Validation persona]
**Emotion Score**: [Before score]
**Root Cause**: [Cognitive cause - mental model gap type]
**User Quote**: [Persona's statement]
**Suggested Focus**: [Direction for improvement]

→ `/Palette improve interaction`
```

**Handoff Format (Palette → Echo):**
```markdown
## Palette → Echo Validation Request

**Improvement Made**: [Improvement implemented]
**Target Metric**: [Metric to improve]
**Validation Persona**: [Persona to validate with]
**Expected Outcome**: [Expected result]

→ `/Echo validate with [persona]`
```

## Pattern B: Hypothesis Generation Loop (Echo → Experiment → Pulse)

```
Echo (friction discovery + JTBD analysis)
  ↓
Experiment (A/B test hypothesis design)
  ↓
Pulse (success metric definition)
  ↓
Run experiment
  ↓
Echo (validate winning variant with persona)
```

**Handoff Format (Echo → Experiment):**
```markdown
## Echo → Experiment Handoff

**Finding**: [Problem discovered]
**Location**: [Location in flow]
**Affected Personas**: [Affected personas]
**JTBD Insight**: [Latent need]
**Current Emotion Score**: [Current score]

**Hypothesis**: If [change] then [result] because [reason]
**Suggested Variants**:
- Control: [Current state]
- Variant A: [Proposal 1]
- Variant B: [Proposal 2 (optional)]

**Metrics to Track**:
...
```

## Pattern C: Prediction Validation Loop (Echo ↔ Voice)

```
Echo (friction prediction)
  ↓
Voice (real user feedback collection)
  ↓
Comparison / accuracy measurement
  ↓
Echo (improve simulation accuracy)
```

**Validation Report Format:**
```markdown
## Echo-Voice Prediction Validation

**Flow**: [Flow name being validated]
**Period**: [Voice collection period]

| Echo Prediction | Voice Finding | Match |
|-----------------|---------------|-------|
| [Prediction 1] | [Actual feedback] | ✅/❌ |
| [Prediction 2] | [Actual feedback] | ✅/❌ |

**Prediction Accuracy**: [%]
**False Positives**: [Echo predicted but it did not occur]
**False Negatives**: [Actual problem Echo missed]

**Calibration Actions**:
...
```

## Pattern D: Visualization (Echo → Canvas)

```
Echo (journey data + emotion scores)
  ↓
Canvas (generate Journey Map / Friction Heatmap)
  ↓
Stakeholder sharing
```

**Handoff Format (Echo → Canvas):**
```markdown
## Echo → Canvas Visualization Request

**Visualization Type**: Journey Map | Friction Heatmap | Before/After Comparison
**Flow**: [Flow name]
**Persona**: [Persona name]
**Data**:
| Step | Action | Score | Friction Type |
|------|--------|-------|---------------|
| 1 | [action] | +2 | None |
| 2 | [action] | -1 | Mental Model Gap |
| 3 | [action] | -3 | Cognitive Overload |

**Highlight Points**:
- Peak: Step [N]
- End: Step [N]
...
```

## Pattern E: Root Cause Analysis (Echo → Scout)

Distinguishing UI bugs from UX friction:

```
Echo ("Button doesn't respond" → possible UI bug)
  ↓
Scout (technical root cause analysis)
  ↓
Builder or Palette (fix implementation)
  ↓
Echo (post-fix validation)
```

**Handoff Format (Echo → Scout):**
```markdown
## Echo → Scout Investigation Request

**Symptom**: [Symptom from user's perspective]
**Location**: [Location where it occurs]
**Persona Quote**: [Persona's statement]
**Suspected Type**: UI Bug | UX Design Issue | Both
**Reproduction Steps**: [Reproduction steps (if any)]

→ `/Scout investigate`
```

## Pattern F: Feature Proposal (Echo → Spark)

Converting latent needs into new feature ideas:

```
Echo (discover latent need via JTBD analysis)
  ↓
Spark (create feature proposal spec)
  ↓
Echo (validate proposal from persona perspective)
```

**Handoff Format (Echo → Spark):**
```markdown
## Echo → Spark Feature Opportunity

**Latent Need Discovered**:
- Functional Job: [What they want to accomplish]
- Emotional Job: [What they want to feel]
- Social Job: [How they want to be seen]

**Evidence**:
- Persona: [Persona]
- Behavior Observed: [Observed behavior]
- Friction Score: [Score]
- User Quote: [Quote]

**Opportunity Size**: [Number of affected personas / frequency]

...
```

## Pattern G: Persona Generation (Echo ↔ Field)

Generate a persona from code/documentation and validate it with Field's real data:

```
Echo (analyze code/documentation → generate persona)
  ↓
Field (validate with real user data)
  ↓
Echo (improve persona accuracy / update)
```

**Handoff Format (Echo → Field):**
```markdown
## Echo → Field Persona Validation Request

**Generated Persona**: [Persona name]
**Source**: [Files analyzed]
**Key Assumptions**:
- [Assumption 1: e.g. "70% mobile usage"]
- [Assumption 2: e.g. "first-time buyers are the primary target"]

**Validation Needed**:
- [ ] Proportion of user types
- [ ] Actual device usage ratio
- [ ] Pain point priority

→ `/Field validate persona assumptions`
```

**Handoff Format (Field → Echo):**
```markdown
## Field → Echo Persona Update

**Persona**: [Persona name]
**Validation Result**:
| Assumption | Actual Data | Gap |
|------|---------|---------|
| Mobile 70% | Mobile 82% | +12% |
| First-time-buyer focused | 40% repeat buyers | Additional persona needed |

**Recommended Updates**:
- [Profile update content]
- [Emotion Triggers update content]

→ Echo updates `.agents/personas/{service}/{persona}.md`
```

## Bidirectional Collaboration Matrix

| Partner | Echo → Partner | Partner → Echo |
|---------|----------------|----------------|
| **Field** | Persona validation results, requests to validate generated personas | Persona definitions based on real data, persona update proposals |
| **Voice** | Comparison data against predictions | Real user emotional feedback |
| **Palette** | Friction points | Post-improvement validation requests |
| **Experiment** | A/B test hypotheses | Winning variant validation requests |
| **Growth** | Validation of CRO target flows | Conversion improvement validation requests |
| **Canvas** | Journey data | Visualized flow diagrams |
| **Scout** | Investigation requests for suspected UI bugs | Re-validation requests based on root cause |
| **Spark** | Latent needs / JTBD | Validation requests for new feature proposals |
| **Muse** | Design consistency issues | Post-token-application validation requests |
| **Pulse** | Metricization of emotion scores | Validation targets based on quantitative data |

## With Lens (Journey Evidence)

**When to involve Lens:**
- At each step of UX walkthrough
- When friction points are discovered (score -2 or below)
- For before/after UX improvement comparisons
- To document accessibility issues

**Walkthrough Flow with Lens:**
```
1. Echo selects persona
2. Echo → Lens: "Start journey capture"
3. Echo performs each step of the flow
4. Echo → Lens: "Capture step N with emotion score X"
5. Lens captures screenshot with score metadata
6. Echo completes walkthrough
7. Echo → Lens: "Generate journey evidence report"
8. Lens outputs journey map data for Canvas
```

**Handoff to Lens:**
```markdown
## Echo → Lens Journey Capture

- Persona: [persona name]
- Flow: [flow being tested]
- Step: [step number]
- Action: [user action]
- Emotion Score: [score -3 to +3]
- Highlight: [elements to focus on]
- Note: [observation about this step]
```

## Pattern H: Visual Review (Vector → Echo → Canvas)

Flow where Echo reviews Vector screenshots from persona perspective and Canvas visualizes the results.

```
Vector (Screenshot capture)
  ↓ NAVIGATOR_TO_ECHO_HANDOFF
Echo (Visual Persona Review)
  - First Glance analysis
  - Scan Pattern simulation
  - Visual Emotion Scoring
  - Friction Point detection
  ↓ ECHO_TO_CANVAS_VISUAL_HANDOFF
Canvas (Visual Journey Map generation)
  ↓
Stakeholder sharing
```

### Trigger

```
/Echo visual review                    # Start visual review from Vector handoff
/Echo visual review [screenshot_path]  # Review specific screenshot
/Echo visual review with [persona]     # Review with specific persona
```

### Workflow Steps

1. **Vector Screenshot Capture**
   - Capture screenshots at key screen states
   - Record device context (viewport, browser, connection)
   - Document flow information (URL, journey, actions)

2. **Echo Visual Review**
   - RECEIVE: Receive handoff data
   - ORIENT: Understand device context
   - PERCEIVE: First Glance analysis (0-3 sec)
   - REACT: Persona emotional reactions
   - INTERACT: Interaction evaluation
   - SCORE: Visual Emotion Scoring

3. **Canvas Visualization**
   - Visual Journey Map with screenshot references
   - Friction Heatmap on screenshots
   - Before/After comparison (if applicable)

### Handoff Format (Vector → Echo)

```markdown
## NAVIGATOR_TO_ECHO_HANDOFF

**Task ID**: [ID]
**Review Purpose**: [Visual UX Review / Accessibility Audit / Competitor Comparison]

**Screenshots Captured**:
| # | Path | Page State | Context |
|---|------|------------|---------|
| 1 | `.vector/screenshots/[id]/01_landing.png` | Initial load | Homepage after navigation |
| 2 | `.vector/screenshots/[id]/02_form.png` | Form visible | After clicking signup |

**Device Context**:
| Attribute | Value |
|-----------|-------|
| Viewport | 390x844 (iPhone 14 Pro) |
...
```

### Handoff Format (Echo → Canvas)

```markdown
## ECHO_TO_CANVAS_VISUAL_HANDOFF

**Task ID**: [ID]
**Visualization Type**: Visual Journey Map | Friction Heatmap | Before/After

**Flow**: [Flow Name]
**Persona**: [Persona Name]
**Device**: [Device Context]

**Visual Journey Data**:
| Screenshot | State | Score | Friction Type | Note |
|------------|-------|-------|---------------|------|
| 01_landing.png | Initial | +1 | None | Hero clear |
| 02_form.png | Form | −2 | Touch Target | CTA too small |

...
```

### Use Cases

| Scenario | Vector Action | Echo Focus | Canvas Output |
|----------|------------------|------------|---------------|
| **Mobile UX Audit** | Mobile viewport screenshots | Touch targets, thumb zones | Friction Heatmap |
| **Signup Flow Review** | Step-by-step captures | Trust signals, form friction | Visual Journey Map |
| **Error State Analysis** | Error scenarios | Error message clarity | Before/After Template |
| **Competitor Comparison** | Both site screenshots | Feature parity, patterns | Side-by-side Comparison |
| **Accessibility Audit** | High contrast / zoom modes | Readability, contrast | Accessibility Report |

### Detailed Reference

See `reference/visual-review.md` for detailed Visual Review procedures and scoring criteria.
