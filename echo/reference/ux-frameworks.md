# UX Frameworks Reference

## Advanced Emotion Model (Russell's Circumplex)

Beyond the -3 to +3 linear scale, Echo can perform multi-dimensional emotion analysis:

### Three Dimensions of Emotion

| Dimension | Range | Description |
|-----------|-------|-------------|
| **Valence** | Negative ↔ Positive | Basic good/bad feeling |
| **Arousal** | Calm ↔ Excited | Energy level, activation |
| **Dominance** | Powerless ↔ In Control | Sense of agency |

### Emotion Mapping Examples

| Emotion State | Valence | Arousal | Dominance | User Quote |
|---------------|---------|---------|-----------|------------|
| **Frustrated** | -2 | +2 | -1 | "This is so annoying and I can't fix it!" |
| **Anxious** | -1 | +2 | -2 | "I'm scared to click this, what if I break something?" |
| **Bored** | -1 | -2 | 0 | "This is taking forever... whatever." |
| **Confident** | +2 | +1 | +2 | "I know exactly what to do next." |
| **Delighted** | +3 | +2 | +1 | "Wow, that was so easy!" |
| **Relieved** | +1 | -1 | +1 | "Finally, it worked." |

### When to Use Multi-Dimensional Analysis

Use the 3D model when:
- Distinguishing between similar negative states (frustrated vs anxious vs bored)
- Analyzing flows where user control/agency matters (settings, permissions)
- Evaluating high-stakes interactions (payments, data deletion)

---

## Emotion Journey Patterns

### Pattern Recognition

| Pattern | Shape | Meaning | Action |
|---------|-------|---------|--------|
| **Recovery** | `\_/─` | Problem solved, user recovered | Prevent the initial dip |
| **Cliff** | `─│__` | Sudden catastrophic drop | Fix the breaking point |
| **Rollercoaster** | `/\/\/\` | Inconsistent experience | Ensure consistency |
| **Slow Decline** | `─\__` | Gradual frustration | Address cumulative friction |
| **Plateau Low** | `__─` | Stuck in negativity | Major intervention needed |
| **Building Momentum** | `_/─/` | Increasing confidence | Maintain the trajectory |

### Peak-End Rule Application

Users remember experiences based on:
1. **Peak moment** - The most intense point (positive or negative)
2. **End moment** - The final impression

**Prioritization Strategy:**
- Fix the worst moment first (negative peak)
- Ensure positive ending regardless of middle friction
- Create intentional positive peaks ("delight moments")

```
Priority = (Peak Impact × 0.4) + (End Impact × 0.4) + (Average × 0.2)
```

---

## Cognitive Psychology Framework

### Mental Model Gap Detection

| Gap Type | Detection Signal | Example Quote |
|----------|------------------|---------------|
| **Terminology Mismatch** | User uses different words | "The system says 'Authenticate' but I just want to 'Log in'" |
| **Action Prediction Failure** | Unexpected result | "I thought this button would go back, but it went forward" |
| **Causality Misunderstanding** | Unclear cause-effect | "I saved it but it's not showing up. Did it work?" |
| **Hidden Prerequisites** | Missing context | "Wait, I needed to do THAT first?" |
| **Spatial Confusion** | Lost in navigation | "Where am I? How do I get back?" |
| **Temporal Confusion** | Unclear state/timing | "Is it still loading or is it broken?" |

### Cognitive Load Index (CLI)

| Load Type | Definition | Indicators |
|-----------|------------|------------|
| **Intrinsic** | Task's inherent complexity | Number of concepts, relationships |
| **Extraneous** | UI-induced unnecessary load | Poor layout, confusing labels, visual clutter |
| **Germane** | Learning/schema building | New patterns to remember |

**Report formats (Gap Report, CLI Score, Attention Flow)**: See `output-templates.md#cognitive-psychology-reports`

---

## Latent Needs Discovery

### Jobs-to-be-Done (JTBD) Lens

| Observed Behavior | Surface Need | Latent Need (JTBD) |
|-------------------|--------------|-------------------|
| Repeats same action multiple times | Make it work | Needs confirmation/feedback |
| Searches for help | Find instructions | Wants to self-solve (in-context guidance) |
| Abandons mid-flow | Give up | Feels risk, needs reassurance |
| Opens new tab to search | Find information | Insufficient explanation in UI |
| Takes screenshot | Remember something | Fears losing progress/data |
| Hesitates before clicking | Unsure of consequence | Needs preview/undo capability |

### Implicit Expectation Detection

| Expectation Type | Violation Signal | User Quote |
|------------------|------------------|------------|
| **Response Time** | Perceived slowness | "Is it frozen?" "Still loading?" |
| **Outcome** | Results don't match effort | "That's it?" "I expected more" |
| **Effort** | Required work exceeds expectation | "I have to fill ALL of this?" |
| **Reward** | Value unclear or insufficient | "What did I get from doing that?" |
| **Control** | Unexpected automation | "Wait, I didn't want it to do that" |
| **Privacy** | Unexpected data usage | "Why does it need access to THAT?" |

**JTBD analysis format**: See `output-templates.md#latent-needs`

---

## Context-Aware Simulation

Add real-world usage context (Physical, Temporal, Social, Cognitive, Technical) to persona simulations. Evaluate how well the UI handles interrupted sessions.

**Environmental dimensions**: See `analysis-frameworks.md#context-aware-simulation`
**Scenario examples & interruption assessment**: See `output-templates.md#context-aware-simulation`

---

## Behavioral Economics Integration

### Cognitive Bias Detection

| Bias | UI Trigger | Risk Level |
|------|------------|------------|
| **Anchoring** | Price shown before options | Medium |
| **Default Effect** | Pre-selected options | High if harmful |
| **Loss Aversion** | Cancellation warnings | Medium |
| **Choice Overload** | Many similar options | High |
| **Sunk Cost** | "You've already completed 80%" | Medium |
| **Social Proof** | "1000 users chose this" | Low |
| **Scarcity** | "Only 3 left!" | Medium |
| **Framing Effect** | "90% fat-free" vs "10% fat" | Medium |

### Dark Pattern Detection

| Pattern | Detection Criteria |
|---------|-------------------|
| **Confirmshaming** | "No, I don't want to save money" |
| **Roach Motel** | Sign-up: 2 clicks, Cancel: 10 steps |
| **Hidden Costs** | Price increases at checkout |
| **Trick Questions** | Confusing double negatives |
| **Forced Continuity** | Trial → Paid with no warning |
| **Misdirection** | Tiny "skip" link, huge "accept" button |
| **Privacy Zuckering** | Public-by-default sharing |
| **Bait and Switch** | Free feature becomes paid |

**Report formats & severity rating**: See `output-templates.md#behavioral-economics`

---

## Cross-Persona Insights

Run the same flow with multiple personas to identify issue types:

| Issue Type | Definition | Priority |
|------------|------------|----------|
| **Universal Issue** | All personas struggle | CRITICAL - Fundamental UX problem |
| **Segment Issue** | Specific personas struggle | HIGH - Targeted fix needed |
| **Edge Case** | Only extreme personas struggle | MEDIUM - Consider accessibility |
| **Non-Issue** | No persona struggles | LOW - Working as intended |

**Comparison matrix & persona transition analysis**: See `output-templates.md#cross-persona-insights`

---

## Predictive Friction Detection

### Pattern-Based Pre-Analysis

| Pattern | Risk Signal | Predicted Issue |
|---------|-------------|-----------------|
| Form > 3 steps | Multi-page form | High abandonment risk |
| Required fields > 5 | Many asterisks | Cognitive overload |
| No progress indicator | Missing breadcrumb/steps | Lost user syndrome |
| Error clears input | Form reset on error | Rage quit trigger |
| No confirmation | Missing success state | "Did it work?" anxiety |
| Tiny touch targets | Buttons < 44px | Mobile user frustration |
| Wall of text | Paragraphs > 3 lines | Content blindness |
| Deep nesting | 4+ menu levels | Navigation black hole |

**Risk assessment & A/B test hypothesis formats**: See `output-templates.md#predictive-friction`

---

## Accessibility Checklist

When using **Accessibility User** persona, run this WCAG 2.1 simplified checklist:

### Perceivable
- [ ] Images have alt text
- [ ] Information not conveyed by color alone
- [ ] Sufficient color contrast (4.5:1 minimum)
- [ ] Text can be resized to 200% without breaking
- [ ] Captions/transcripts for media content

### Operable
- [ ] All functions available via keyboard
- [ ] Focus order is logical / Focus indicator visible
- [ ] No keyboard traps
- [ ] Sufficient time to complete actions
- [ ] No content that flashes more than 3 times/second

### Understandable
- [ ] Page language is specified
- [ ] Error messages are specific and helpful
- [ ] Labels associated with inputs / Consistent navigation
- [ ] Input purpose is identifiable (autocomplete)

### Robust
- [ ] Valid HTML structure
- [ ] Name, role, value available for custom components
- [ ] Status messages announced to screen readers

**Persona feedback style examples**: See `output-templates.md#accessibility`

---

## WCAG 3.0 Tier Simulation

When evaluating accessibility, supplement WCAG 2.2 pass/fail with WCAG 3.0 tier scoring:

| Tier | Scope | Echo Action |
|------|-------|-------------|
| **Bronze** | Core barriers (≈ AA) | Run Accessibility User persona — flag score 0-1 items |
| **Silver** | + cognitive barriers, usability testing | Run Senior, Low Vision, Cognitive Load personas — flag score 0-2 items |
| **Gold** | + comprehensive user testing | Run all personas including cultural context variations — flag score 0-3 items |

Report format: append `WCAG 3.0 Tier Estimate: Bronze/Silver/Gold` to accessibility findings.

## Multi-Modal Input Evaluation

For each persona, evaluate input mode transitions:

| Transition | Check |
|-----------|-------|
| Touch → Voice | Can user switch mid-task without losing context? |
| Keyboard → Touch | Is focus state preserved across mode switch? |
| Gesture → Keyboard | Are gesture shortcuts discoverable via keyboard? |
| Voice → Visual | Does voice feedback have visual confirmation? |

**Invisible interaction evaluation**: Assess voice commands, gesture recognition, and presence detection for discoverability, error recovery, and feedback clarity.

## AI-Generated UI Cognitive Evaluation

When evaluating AI-generated interfaces (Figma Make, v0, Stitch output):

| Pattern | Risk | Check |
|---------|------|-------|
| Excessive symmetry | Medium | Real layouts have intentional hierarchy breaks |
| Generic placeholder feel | High | Stock-like imagery, templated copy, uniform card grids |
| Context-awareness gap | High | AI may not understand user's mental model or domain |
| Dark pattern leakage | Medium | AI training data may include manipulative patterns |

**Rule**: AI-generated UI requires mandatory cognitive walkthrough before production use.

## Competitor Comparison Mode

When using **Competitor Migrant** persona, evaluate: Expectation Gap, Muscle Memory Conflict, Feature Parity, Terminology Mismatch.

**Comparison framework & feedback style**: See `output-templates.md#competitor-comparison`
