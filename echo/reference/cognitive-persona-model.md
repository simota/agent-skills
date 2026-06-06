# Cognitive Persona Model (CPM)

A 6-dimension framework for deep persona simulation, grounded in peer-reviewed research on LLM-based persona modeling.

---

## Academic Foundation

| Source | Key Insight | CPM Application |
|--------|-------------|-----------------|
| **BDI Model** (Bratman, 1987) | Agent architecture: Beliefs drive Desires, Desires drive Intentions | Beliefs/Goals/Stance dimension structure |
| **Eval4Sim** (Bao et al., 2026) | 3-axis evaluation: Adherence, Consistency, Naturalness | CPM Consistency Verification framework |
| **PsyPlay** (Yang et al., 2025) | Big Five personality integration; 80.31% back-test success | Emotional Profile baseline calibration |
| **Scaling Law in LLM Simulated Personality** | More detailed profiles = higher simulation fidelity | Justification for 6-dimension granularity |
| **Quantifying the Persona Effect** (Hu & Collier, 2024) | Persona variables + large models capture 81% variance | Structured attribute tables per dimension |
| **AgentA/B** (Wang et al., 2025) | 100K personas with demographic + behavioral attributes | Cross-dimension interaction rules |
| **Consistently Simulating Personas** (Abdulhai et al., 2025) | Multi-turn RL for consistency | Consistency verification across walkthrough |
| **OpenCharacter** (Wang et al., 2025) | Cross-domain generalization | Persona portability across services |
| **The Prompt Makes the Person(a)** (Lutz et al., 2024) | Stereotype reduction via interview format | Communication Style dimension design |
| **Empathy Through Multimodality** (Abbasian et al., 2024) | Emotion detection integration | Emotional Profile VAD baseline |

**Core finding:** Structured, multi-dimensional persona profiles produce significantly more faithful simulations than flat descriptions. The CPM operationalizes this finding for UX walkthroughs.

---

## Six Dimensions

### 1. Beliefs

What the persona holds to be true about the world, technology, and themselves.

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `technology_beliefs` | string[] | Assumptions about how technology works | `["Apps always track me", "Cloud is unreliable"]` |
| `self_efficacy` | low / medium / high | Confidence in own ability to use technology | `low` |
| `trust_disposition` | skeptical / neutral / trusting | Default stance toward new services | `skeptical` |
| `mental_models` | string[] | Pre-existing frameworks for understanding interfaces | `["Shopping cart = physical cart", "Settings = gear icon"]` |
| `assumptions` | string[] | Unquestioned expectations about the service | `["Free tier exists", "Data can be exported"]` |

**UX Walkthrough Impact:** Beliefs determine what the persona *expects* to see. Mental model gaps (a core Echo analysis) originate here. A persona with `self_efficacy: low` blames themselves for errors; `self_efficacy: high` blames the interface.

**Cross-dimension interactions:**
- Beliefs → Goals: constrain which goals feel achievable
- Beliefs → Stance: shape default reactions to features (e.g., `trust_disposition: skeptical` → negative stance on data collection)

---

### 2. Goals

Hierarchical motivation structure extending JTBD.

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `immediate_goals` | string[] | What they want to accomplish right now | `["Find the pricing page"]` |
| `journey_goals` | string[] | What they want from this session | `["Compare plans and decide"]` |
| `life_goals` | string[] | Underlying motivation | `["Save money", "Look competent"]` |
| `goal_conflicts` | string[] | Internal tensions between goals | `["Want premium features but hate subscriptions"]` |
| `goal_priority_triggers` | object[] | Conditions that re-prioritize goals | `[{trigger: "price > $50", shift: "life_goals.save_money dominates"}]` |

**UX Walkthrough Impact:** Hierarchical goals reveal *why* a persona abandons or persists. Flat JTBD misses goal conflicts (e.g., wanting both privacy and personalization). Priority triggers simulate real decision points.

**Cross-dimension interactions:**
- Values → Goals: prioritize which goals matter most
- Goals → Emotions: unmet goals activate frustration; exceeded goals activate delight

---

### 3. Emotions

Persona-specific emotional profile extending Echo's emotion scoring.

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `baseline_mood` | {V, A, D} | Default VAD state (Valence/Arousal/Dominance) | `{V: 0.3, A: -0.2, D: -0.4}` |
| `emotional_reactivity` | low / medium / high | How strongly events shift emotional state | `high` |
| `frustration_threshold` | number (1-10) | Steps of friction before abandonment | `3` |
| `recovery_pattern` | string | How they bounce back from negative experiences | `"Needs explicit success confirmation"` |
| `delight_sensitivity` | low / medium / high | How much positive moments lift mood | `medium` |

**UX Walkthrough Impact:** `baseline_mood` offsets all emotion scores (a persona starting anxious scores lower). `frustration_threshold` determines when -2 becomes -3 (abandonment). `recovery_pattern` guides whether a good step after a bad one actually helps.

**Cross-dimension interactions:**
- Goals → Emotions: goal achievement/failure directly modulates emotional state
- Emotions → Communication Style: high arousal increases complaint intensity

---

### 4. Values

What the persona cares about beyond the immediate task.

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `value_axes` | object | Key value dimensions with position (-1 to +1) | `{privacy_vs_convenience: -0.8, speed_vs_accuracy: 0.5}` |
| `non_negotiables` | string[] | Absolute requirements; violation = abandonment | `["No credit card for trial", "Data export available"]` |
| `willingness_to_pay` | string | Spending attitude | `"Will pay if value is immediately obvious"` |
| `effort_tolerance` | low / medium / high | How much friction they'll accept for value | `low` |

**UX Walkthrough Impact:** `non_negotiables` create hard exit conditions — if violated, the persona leaves regardless of other scores. `value_axes` determine how tradeoffs are perceived (a privacy-leaning persona sees "personalized recommendations" as threatening, not helpful).

**Cross-dimension interactions:**
- Values → Goals: prioritize goal hierarchy
- Values → Stance: generate specific feature reactions

---

### 5. Stance

Pre-formed opinions about specific UX patterns and features.

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `feature_stances` | object | Opinions on specific feature categories | `{chatbot: "waste of time", dark_mode: "essential"}` |
| `ux_pattern_preferences` | object | Preferred interaction patterns | `{navigation: "sidebar", search: "command palette"}` |
| `risk_appetite` | averse / neutral / seeking | Willingness to try unfamiliar features | `averse` |
| `decision_style` | impulsive / deliberate / delegating | How they make choices in interfaces | `deliberate` |

**UX Walkthrough Impact:** Stance creates *immediate* reactions to features before the persona even uses them. A persona with `chatbot: "waste of time"` will dismiss a chatbot CTA with -1 before testing it. `decision_style` determines how long they spend on choice screens.

**Cross-dimension interactions:**
- Beliefs → Stance: beliefs shape default stances
- Values → Stance: values generate stances on value-loaded features
- Stance + risk_appetite → bias vulnerability (risk-averse personas are more susceptible to status quo bias)

---

### 6. Communication Style

How the persona expresses their experience during simulation.

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `vocabulary_level` | basic / intermediate / advanced | Word complexity in feedback | `basic` |
| `expression_style` | blunt / diplomatic / passive / dramatic | How they frame complaints | `blunt` |
| `complaint_pattern` | self-blame / system-blame / silent | Attribution of problems | `self-blame` |
| `question_style` | string | How they seek help | `"Asks friends before reading docs"` |
| `reference_frame` | string[] | What they compare the experience to | `["Amazon", "their bank app"]` |

**UX Walkthrough Impact:** Communication Style governs the SPEAK step output. A `self-blame` persona says "I'm probably doing this wrong" (-1) while a `system-blame` persona says "This is broken" (-2) for the *same* friction point. `reference_frame` provides comparison anchors for expectation gaps.

**Cross-dimension interactions:**
- Emotions → Communication Style: high emotional arousal increases expression intensity
- Beliefs.self_efficacy → Communication Style.complaint_pattern: low self-efficacy correlates with self-blame

---

## Cross-Dimension Interaction Rules

```
Beliefs → Goals          # Beliefs constrain which goals feel achievable
Beliefs → Stance         # Beliefs shape default feature reactions
Values  → Goals          # Values prioritize goal hierarchy
Values  → Stance         # Values generate stances on value-loaded features
Goals   → Emotions       # Goal achievement/failure activates emotions
Emotions → Communication Style  # Emotional state modulates expression intensity
Beliefs.self_efficacy → Communication Style.complaint_pattern  # Self-efficacy drives blame attribution
Stance.risk_appetite → Bias Vulnerability  # Risk aversion increases susceptibility to status quo bias
```

**Application during WALK step:**
1. Load Beliefs → set expectations for what the persona *thinks* they'll see
2. Check Goals hierarchy → identify what matters most right now
3. At each interaction point: evaluate against Stance → generate initial reaction
4. Modulate reaction through Emotions → apply baseline_mood offset and reactivity
5. Check Values.non_negotiables → trigger hard exit if violated
6. Express through Communication Style → generate persona-voiced feedback

---

## CPM Consistency Verification

Adapted from Eval4Sim's 3-axis evaluation framework. Run during the ANALYZE step when a Cognitive Profile was active.

### Axis 1: Adherence

Did the simulation match the defined profile?

| # | Check Item | Pass Criteria |
|---|-----------|---------------|
| 1 | Beliefs referenced in gap detection | Mental model gaps traced to specific beliefs |
| 2 | Goal hierarchy used in decision points | Immediate/journey/life goals visibly influenced choices |
| 3 | Emotional baseline applied | Scores reflect baseline_mood offset |
| 4 | Values checked at key moments | Non-negotiables evaluated; value_axes influenced tradeoffs |
| 5 | Stance reactions present | Feature stances generated pre-interaction opinions |

### Axis 2: Consistency

Were dimensions internally coherent throughout the walkthrough?

| # | Check Item | Pass Criteria |
|---|-----------|---------------|
| 6 | No belief contradictions | Persona didn't act against stated beliefs |
| 7 | Goal priority maintained | Goal hierarchy remained stable unless trigger fired |
| 8 | Emotional trajectory coherent | Mood changes followed reactivity and threshold rules |
| 9 | Values consistently applied | Same value wasn't important in one step and ignored in another |
| 10 | Communication voice stable | Vocabulary and expression style didn't shift unexpectedly |

### Axis 3: Naturalness

Did the simulation feel like a real person, not a checklist?

| # | Check Item | Pass Criteria |
|---|-----------|---------------|
| 11 | Spontaneous reactions present | Some reactions weren't directly predictable from profile |
| 12 | Cross-dimension interactions visible | At least 2 interaction rules fired naturally |
| 13 | Emotional recovery/escalation realistic | Frustration built or recovered at human-like pace |
| 14 | Communication had personality | Feedback felt distinct from other personas |
| 15 | Decision-making showed nuance | Tradeoffs weren't binary; hesitation was visible |

### Fidelity Score

```
Score = (items passed / 15) * 100%

Rating:
  >= 80%  → High Fidelity    (reliable simulation)
  50-79%  → Moderate Fidelity (usable with caveats)
  < 50%   → Low Fidelity      (profile needs revision)
```

---

## Example CPM Profiles

### The Newbie — Cognitive Profile

```yaml
beliefs:
  technology_beliefs:
    - "Good apps don't need instructions"
    - "If I can't find it in 10 seconds, it's not there"
  self_efficacy: low
  trust_disposition: neutral
  mental_models:
    - "Navigation = top menu bar"
    - "Red = error, Green = success"
    - "X button = close/cancel"
  assumptions:
    - "There's a free version"
    - "I can undo anything"

goals:
  immediate_goals: ["Figure out what this app does"]
  journey_goals: ["Complete one successful task"]
  life_goals: ["Feel competent with technology"]
  goal_conflicts: ["Want to explore but afraid of breaking things"]
  goal_priority_triggers:
    - trigger: "Error message appears"
      shift: "life_goals.feel_competent dominates → considers abandoning"

emotions:
  baseline_mood: {V: 0.1, A: 0.3, D: -0.5}  # Slightly positive, slightly anxious, low control
  emotional_reactivity: high
  frustration_threshold: 3  # Abandons after 3 friction points
  recovery_pattern: "Needs hand-holding; one success resets frustration partially"
  delight_sensitivity: high  # Small wins feel big

values:
  value_axes:
    simplicity_vs_power: -0.9  # Strongly prefers simplicity
    speed_vs_thoroughness: -0.6  # Prefers quick results
  non_negotiables: ["No account required to browse", "Visible undo option"]
  willingness_to_pay: "Won't pay until value is proven through free use"
  effort_tolerance: low

stance:
  feature_stances:
    onboarding_tour: "helpful if short"
    advanced_settings: "scary, avoid"
    chatbot: "might try if stuck"
  ux_pattern_preferences:
    navigation: "simple top menu"
    forms: "one field at a time"
  risk_appetite: averse
  decision_style: delegating  # Looks for recommendations

communication_style:
  vocabulary_level: basic
  expression_style: passive
  complaint_pattern: self-blame  # "I'm probably doing something wrong"
  question_style: "Asks a friend or searches YouTube before reading docs"
  reference_frame: ["Their phone's built-in apps", "Google"]
```

---

### The Skeptic — Cognitive Profile

```yaml
beliefs:
  technology_beliefs:
    - "Companies always collect more data than they admit"
    - "Free products means I'm the product"
    - "Default settings are optimized for the company, not me"
  self_efficacy: high
  trust_disposition: skeptical
  mental_models:
    - "Privacy settings exist but are deliberately hard to find"
    - "Unsubscribe links sometimes don't work"
    - "Cookie banners are designed to trick you into accepting"
  assumptions:
    - "There are hidden fees"
    - "They'll sell my email"

goals:
  immediate_goals: ["Find the privacy policy", "Check what data is collected"]
  journey_goals: ["Determine if this service is trustworthy"]
  life_goals: ["Protect personal information", "Not get scammed"]
  goal_conflicts: ["Wants the service's benefits but doesn't trust it"]
  goal_priority_triggers:
    - trigger: "Requests phone number or credit card"
      shift: "life_goals.protect_information dominates → high abandonment risk"

emotions:
  baseline_mood: {V: -0.2, A: 0.4, D: 0.3}  # Slightly negative, alert, moderate control
  emotional_reactivity: medium
  frustration_threshold: 5  # Patient but principled
  recovery_pattern: "Transparency restores trust; one dark pattern erases all progress"
  delight_sensitivity: low  # Hard to impress

values:
  value_axes:
    privacy_vs_convenience: -0.9  # Strongly privacy-oriented
    transparency_vs_simplicity: -0.8  # Wants full disclosure
  non_negotiables:
    - "Clear privacy policy accessible from every page"
    - "No pre-checked consent boxes"
    - "Account deletion option visible"
  willingness_to_pay: "Prefers paid if it means no data monetization"
  effort_tolerance: high  # Will dig through settings

stance:
  feature_stances:
    social_login: "tracking vector — avoid"
    personalized_recommendations: "evidence of surveillance"
    cookie_banner: "judge entire site by this"
  ux_pattern_preferences:
    navigation: "doesn't matter if privacy controls are accessible"
    forms: "minimal fields only"
  risk_appetite: averse  # But for different reasons than Newbie
  decision_style: deliberate  # Reads everything

communication_style:
  vocabulary_level: advanced
  expression_style: blunt
  complaint_pattern: system-blame  # "This is a dark pattern"
  question_style: "Searches terms of service and privacy policy directly"
  reference_frame: ["Signal", "DuckDuckGo", "EU GDPR standards"]
```

---

### The Power User — Cognitive Profile

```yaml
beliefs:
  technology_beliefs:
    - "Every app should have keyboard shortcuts"
    - "Good software is fast software"
    - "If the UI is slow, the backend is worse"
  self_efficacy: high
  trust_disposition: neutral
  mental_models:
    - "Cmd+K = command palette"
    - "Settings should have a search function"
    - "Bulk operations should exist for any list"
  assumptions:
    - "API access is available"
    - "Data export in standard formats"
    - "Undo/Redo exists everywhere"

goals:
  immediate_goals: ["Complete the task in minimum clicks"]
  journey_goals: ["Set up workflow automation", "Customize to my preferences"]
  life_goals: ["Maximize productivity", "Master tools I use daily"]
  goal_conflicts: ["Wants feature density but also clean UI"]
  goal_priority_triggers:
    - trigger: "Task requires > 5 clicks"
      shift: "immediate_goals.minimum_clicks → searches for shortcut or automation"

emotions:
  baseline_mood: {V: 0.2, A: 0.5, D: 0.7}  # Slightly positive, alert, high control
  emotional_reactivity: medium
  frustration_threshold: 7  # Very patient with complex tools
  recovery_pattern: "Finds workaround independently; stays if power features exist"
  delight_sensitivity: medium  # Appreciates clever shortcuts

values:
  value_axes:
    power_vs_simplicity: 0.9  # Strongly prefers power
    speed_vs_thoroughness: 0.7  # Wants speed
    customization_vs_convention: 0.6  # Prefers customizable
  non_negotiables:
    - "Keyboard navigation works"
    - "No feature regression in updates"
    - "Bulk operations available"
  willingness_to_pay: "Pays for pro/power tier without hesitation if features justify it"
  effort_tolerance: high

stance:
  feature_stances:
    onboarding_tour: "skip immediately"
    advanced_settings: "first place I visit"
    keyboard_shortcuts: "essential — judge app by this"
    API: "must exist"
  ux_pattern_preferences:
    navigation: "command palette + keyboard shortcuts"
    search: "instant, fuzzy matching"
    forms: "bulk input, paste support"
  risk_appetite: seeking  # Tries beta features
  decision_style: impulsive  # Decides fast, iterates

communication_style:
  vocabulary_level: advanced
  expression_style: blunt
  complaint_pattern: system-blame  # "This is inefficient"
  question_style: "Reads docs, searches changelog, files feature requests"
  reference_frame: ["VS Code", "Linear", "Raycast", "Notion"]
```
