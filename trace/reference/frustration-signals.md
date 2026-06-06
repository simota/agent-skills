# Frustration Signal Detection

Detailed frustration detection, classification, and scoring.

> **2026 detection baseline.** The leading session-replay tools (FullStory, LogRocket Galileo, Mouseflow Mina AI, Hotjar, PostHog) all ship **rage-click** and **dead-click** detection out of the box, and pair them with **AI-generated session summaries** that surface candidate frustration moments without manual filtering. Use the tool's signal as the *first-pass filter*; apply the threshold / weight tables below as the *audit gate* before pulling a finding into a report — vendor-defined "rage click" tuning varies between platforms and over-fires on UI patterns like double-tap-to-zoom or quick-checkbox-toggle that are not actual frustration.

---

## Signal Taxonomy

### Tier 1: High Severity (Immediate Attention)

| Signal | Definition | Detection Rule | Weight |
|--------|------------|----------------|--------|
| **Rage Click** | Rapid repeated clicks on same area | 3+ clicks within 1.5s, <50px apart | 3 |
| **Back Loop** | Quick return to previous page | Back within 5s, repeated 2+ times | 3 |
| **Form Abandonment** | Started but didn't submit | >2 fields filled, no submit, exit | 3 |
| **Error Loop** | Repeated error encounters | Same error 2+ times in session | 3 |

### Tier 2: Medium Severity (Investigation Required)

| Signal | Definition | Detection Rule | Weight |
|--------|------------|----------------|--------|
| **Scroll Thrash** | Rapid up/down scrolling | Direction change 3+ times in 3s | 2 |
| **Dead Click** | Click on non-interactive element | Click with no event handler | 2 |
| **Long Pause** | Extended inactivity on active page | 30s+ no interaction | 2 |
| **Zoom/Resize** | Accessibility adjustment | Pinch zoom or text resize | 2 |

### Tier 3: Low Severity (Monitor)

| Signal | Definition | Detection Rule | Weight |
|--------|------------|----------------|--------|
| **Help Seeking** | Opened help/FAQ | Help link clicked | 1 |
| **Search Refinement** | Multiple search attempts | 2+ searches in 30s | 1 |
| **Tab Switching** | Left and returned | Window blur/focus events | 1 |
| **Slow Scroll** | Hesitant reading | Scroll velocity <100px/s | 1 |

---

## Detection Algorithms

### Rage Click Detection

```yaml
RAGE_CLICK_ALGORITHM:
  parameters:
    time_window: 1500ms
    click_threshold: 3
    distance_threshold: 50px

  detection:
    1. Group clicks by time_window
    2. Calculate centroid of click positions
    3. Check if all clicks within distance_threshold of centroid
    4. If click_count >= click_threshold → RAGE_CLICK

  output:
    signal: "RAGE_CLICK"
    severity: "HIGH"
    location:
      page: "[URL]"
      element: "[CSS selector or coordinates]"
      element_type: "[button/link/image/other]"
    context:
      click_count: [number]
      duration: [ms]
      element_interactive: [true/false]
```

### Back Loop Detection

```yaml
BACK_LOOP_ALGORITHM:
  parameters:
    time_threshold: 5000ms
    min_occurrences: 2

  detection:
    1. Track page navigation sequence
    2. Identify A → B → A patterns
    3. Check if B → A transition < time_threshold
    4. Count occurrences in session
    5. If occurrences >= min_occurrences → BACK_LOOP

  output:
    signal: "BACK_LOOP"
    severity: "HIGH"
    pages:
      page_a: "[URL]"
      page_b: "[URL]"
    context:
      loop_count: [number]
      average_time_on_b: [ms]
      final_action: "[exit/proceed/help]"
```

### Scroll Thrash Detection

```yaml
SCROLL_THRASH_ALGORITHM:
  parameters:
    time_window: 3000ms
    direction_changes: 3
    velocity_threshold: 500px/s

  detection:
    1. Track scroll events with direction
    2. Within time_window, count direction reversals
    3. Check scroll velocity > velocity_threshold
    4. If direction_changes >= threshold → SCROLL_THRASH

  output:
    signal: "SCROLL_THRASH"
    severity: "MEDIUM"
    location:
      page: "[URL]"
      scroll_region: "[viewport coordinates]"
    context:
      direction_changes: [number]
      peak_velocity: [px/s]
      content_at_location: "[description]"
```

---

## Frustration Score Calculation

### Per-Session Score

```yaml
FRUSTRATION_SCORE_FORMULA:
  components:
    tier_1_signals: weight × 3
    tier_2_signals: weight × 2
    tier_3_signals: weight × 1

  calculation: |
    score = Σ(signal_count × signal_weight × tier_multiplier)

  example:
    - rage_clicks: 2 × 3 × 3 = 18
    - scroll_thrash: 3 × 2 × 2 = 12
    - help_seeking: 1 × 1 × 1 = 1
    - total: 31

  interpretation:
    0-5: "Low - Normal friction"
    6-15: "Medium - Notable issues"
    16-30: "High - Significant problems"
    31+: "Critical - Immediate attention"
```

### Per-Location Score

```yaml
LOCATION_FRUSTRATION_SCORE:
  aggregation: |
    For each page/element:
      score = Σ(session_scores) / session_count × frequency_multiplier

  frequency_multiplier:
    - ">50% of sessions": 1.5
    - "25-50% of sessions": 1.2
    - "10-25% of sessions": 1.0
    - "<10% of sessions": 0.8

  output:
    location: "[Page/Element]"
    aggregate_score: [number]
    affected_sessions: [count]
    top_signals: [list]
```

---

## Context Enrichment

### Environmental Factors

```yaml
CONTEXT_FACTORS:
  device:
    mobile:
      adjust: +20%  # Higher frustration threshold
      reason: "Touch interactions less precise"
    tablet:
      adjust: +10%
    desktop:
      adjust: 0%  # Baseline

  network:
    slow_connection:
      indicator: "Page load >3s or API response >2s"
      adjust: -10%  # Lower score, frustration may be network-related

  time_of_day:
    late_night:
      indicator: "Sessions 11pm-5am local"
      adjust: +10%  # Fatigue may amplify frustration
```

### User Journey Position

```yaml
JOURNEY_POSITION_CONTEXT:
  early_funnel:
    pages: [landing, browse, search]
    interpretation: "Exploration frustration - may indicate discoverability issues"

  mid_funnel:
    pages: [product, comparison, cart]
    interpretation: "Evaluation frustration - may indicate information gaps"

  late_funnel:
    pages: [checkout, payment, confirmation]
    interpretation: "Commitment frustration - CRITICAL, directly impacts conversion"
    score_multiplier: 1.5  # Higher weight for late-funnel friction
```

---

## Signal Combinations (Patterns)

### Critical Patterns

| Pattern | Signals | Interpretation | Priority |
|---------|---------|----------------|----------|
| **Checkout Desperation** | Rage click + Back loop at payment | User wants to buy but can't | P0 |
| **Search Failure** | Search refinement + Scroll thrash + Exit | Can't find what they need | P0 |
| **Form Struggle** | Error loop + Long pause + Abandon | Form is broken or confusing | P0 |

### Warning Patterns

| Pattern | Signals | Interpretation | Priority |
|---------|---------|----------------|----------|
| **Confused Explorer** | Dead clicks + Scroll thrash | UI unclear | P1 |
| **Help Dependent** | Help seeking + Tab switch + Return | Needs guidance to proceed | P1 |
| **Accessibility Barrier** | Zoom + Long pause + Slow scroll | Content not accessible | P1 |

### Monitor Patterns

| Pattern | Signals | Interpretation | Priority |
|---------|---------|----------------|----------|
| **Comparison Shopper** | Tab switch + Multiple product views | Normal shopping behavior | P3 |
| **Careful Reader** | Slow scroll + Long pause | Engaged, thorough reading | P3 |

---

## False Positive Handling

### Common False Positives

| Signal | False Positive Scenario | Detection Rule |
|--------|------------------------|----------------|
| Rage Click | Double-click interface | Check if element expects double-click |
| Back Loop | Intentional comparison | Check if products in loop differ |
| Long Pause | Multimedia content | Check for video/audio on page |
| Scroll Thrash | Parallax effects | Check page scroll behavior type |

### Filtering Rules

```yaml
FALSE_POSITIVE_FILTERS:
  rage_click:
    exclude_if:
      - element_type: "double-click-action"
      - time_between_clicks: ">500ms average"
      - subsequent_action: "successful_interaction"

  back_loop:
    exclude_if:
      - different_products_viewed: true
      - explicit_compare_action: true
      - time_on_page_b: ">30s"

  scroll_thrash:
    exclude_if:
      - page_has_scroll_effects: true
      - scroll_ends_at_target: true
      - search_or_nav_follows: true
```

---

## Reporting Format

### Signal Summary Table

```markdown
## Frustration Signal Summary

**Analysis Period:** [Date range]
**Sessions Analyzed:** [Count]

### By Signal Type

| Signal | Count | % Sessions | Avg per Session | Trend |
|--------|-------|------------|-----------------|-------|
| Rage Click | [n] | [%] | [avg] | [↑/↓/→] |
| Back Loop | [n] | [%] | [avg] | [↑/↓/→] |
| ... | ... | ... | ... | ... |

### Top Frustration Locations

| Rank | Location | Score | Top Signal | Sessions |
|------|----------|-------|------------|----------|
| 1 | [Page/Element] | [score] | [signal] | [count] |
| 2 | ... | ... | ... | ... |
```

### Individual Signal Detail

```markdown
### Signal: Rage Click on [Element]

**Location:** [Page URL] → [Element selector]
**Frequency:** [count] occurrences in [sessions] sessions ([%])
**Severity:** [HIGH/MEDIUM/LOW]

**Pattern:**
- Average clicks: [n]
- Average duration: [ms]
- Element is interactive: [Yes/No]
- Subsequent action: [Success/Abandon/Help]

**Affected Personas:**
- [Persona 1]: [%] affected
- [Persona 2]: [%] affected

**Example Sessions:**
- Session #A1B2: [Brief description]
- Session #C3D4: [Brief description]

**Hypothesis:** [What might be causing this]
**Recommendation:** [Suggested action]
```
