# Persona Integration Patterns

Detailed collaboration patterns with Researcher and Echo.

---

## Integration Overview

```
┌──────────────────────────────────────────────────────────┐
│                    PERSONA LIFECYCLE                      │
│                                                          │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐     │
│  │ Researcher │ →  │   Trace    │ →  │   Echo     │     │
│  │  Creates   │    │ Validates  │    │ Simulates  │     │
│  └────────────┘    └────────────┘    └────────────┘     │
│        ↑                  │                  │           │
│        └──────────────────┴──────────────────┘           │
│                    Feedback Loop                         │
└──────────────────────────────────────────────────────────┘
```

---

## Pattern A: Researcher → Trace (Segmentation)

Use Researcher-defined personas to segment sessions for analysis.

### Input Format

```yaml
PERSONA_DEFINITION:
  source: Researcher
  persona:
    name: "Cautious Comparison Shopper"
    id: "CCS-001"

    # Identifiable characteristics
    behavioral_markers:
      - views_multiple_products: ">3 products before cart"
      - compares_prices: "Visits competitor sites"
      - reads_reviews: "Scrolls to review section"
      - long_consideration: ">5 min on product page"

    # Technical markers (for filtering)
    technical_markers:
# ...
```

### Trace Processing

```yaml
SEGMENTATION_PROCESS:
  1. Filter sessions by technical_markers
  2. Score sessions against behavioral_markers
  3. Classify sessions with confidence score

  output:
    persona: "Cautious Comparison Shopper"
    sessions_matched: 1247
    confidence_distribution:
      high: 45%    # 4/4 markers match
      medium: 35%  # 3/4 markers match
      low: 20%     # 2/4 markers match
```

### Output Format

```yaml
SEGMENT_ANALYSIS:
  persona: "Cautious Comparison Shopper"
  analysis_period: "2025-01-01 to 2025-01-31"
  sessions_analyzed: 1247

  behavior_patterns:
    expected_vs_actual:
      - marker: "views_multiple_products"
        expected: ">3 products"
        actual_average: 4.7
        match: true

      - marker: "reads_reviews"
        expected: "Scrolls to review section"
        actual_rate: 67%
# ...
```

---

## Pattern B: Trace → Researcher (Validation)

Validate and update persona definitions based on real data analysis.

### Validation Report Format

```yaml
PERSONA_VALIDATION_REPORT:
  persona: "Cautious Comparison Shopper"
  validation_date: "2025-01-31"
  sessions_analyzed: 1247

  validation_results:
    overall_match: 72%

    by_marker:
      - marker: "views_multiple_products"
        expected: ">3 products"
        actual_match: 89%
        status: "VALIDATED"

      - marker: "compares_prices"
# ...
```

### Handoff to Researcher

```markdown
## RESEARCHER_HANDOFF (from Trace)

### Persona Validation: Cautious Comparison Shopper

**Analysis Period:** 2025-01-01 to 2025-01-31
**Sessions Analyzed:** 1,247

### Validation Summary

| Marker | Expected | Match Rate | Status |
|--------|----------|------------|--------|
| Multiple product views | >3 products | 89% | ✅ Validated |
| Compares prices | Competitor visits | 34% | ⚠️ Needs review |
| Reads reviews | Scrolls to reviews | 67% | 🔶 Partial |

...
```

---

## Pattern C: Trace → Echo (Problem Handoff)

Hand off discovered problems to Echo for simulation verification.

### Problem Discovery Format

```yaml
PROBLEM_DISCOVERY:
  id: "PROB-2025-0131-001"
  discovery_date: "2025-01-31"

  location:
    page: "/checkout/payment"
    element: "#submit-payment-btn"

  evidence:
    sessions_analyzed: 3421
    frustration_score: 23.7 (High)

    signals:
      rage_clicks:
        rate: 18%
# ...
```

### Handoff to Echo

```markdown
## ECHO_HANDOFF (from Trace)

### Problem: Payment Submit Button Frustration

**Frustration Score:** 23.7 (High)
**Sessions Analyzed:** 3,421

### Evidence

| Signal | Rate | Detail |
|--------|------|--------|
| Rage clicks | 18% | Average 4.2 clicks before success |
| Back loops | 34% | Return to cart, re-add items |
| Abandonment | 28% | Exit after 2+ submit attempts |

...
```

---

## Pattern D: Echo → Trace (Prediction Validation)

Validate Echo's simulation predictions with real session data.

### Prediction Input

```yaml
ECHO_PREDICTION:
  prediction_id: "ECHO-PRED-001"
  prediction_date: "2025-01-25"

  persona: "Senior User"
  flow: "Account settings"

  predicted_friction:
    - location: "Password change form"
      issue: "Font size too small"
      confidence: 0.85
      expected_signals:
        - zoom_gestures
        - long_form_completion_time

# ...
```

### Validation Process

```yaml
TRACE_VALIDATION:
  prediction_id: "ECHO-PRED-001"
  validation_date: "2025-01-31"

  segment_criteria:
    age_group: "60+"
    flow: "Account settings"

  sessions_analyzed: 234

  validation_results:
    - prediction: "Font size too small"
      status: "CONFIRMED"
      confidence_delta: +0.10  # Higher than predicted
      evidence:
# ...
```

### Validation Report

```markdown
## Echo Prediction Validation Report

**Prediction ID:** ECHO-PRED-001
**Persona:** Senior User
**Flow:** Account settings
**Sessions Analyzed:** 234

### Results

| Prediction | Confidence | Status | Evidence |
|------------|------------|--------|----------|
| Font size too small | 0.85 → 0.95 | ✅ CONFIRMED | 78% zoom, 3.2x time |
| Low color contrast | 0.72 → 0.57 | 🔶 PARTIAL | 8% dead clicks |

### Confirmed: Font Size Issue
...
```

---

## Persona Segment Mapping

### Default Segment Mappings

| Researcher Persona | Trace Technical Filters | Behavioral Markers |
|-------------------|-------------------------|-------------------|
| Mobile-first Millennial | device=mobile, age=25-35 | fast_navigation, gesture_heavy |
| Cautious Shopper | session_duration>10min | multiple_product_views, review_reader |
| Senior User | age=60+ | slow_pace, zoom_gestures |
| Power User | visits>10/month | keyboard_shortcuts, direct_navigation |
| First-time Visitor | visit_count=1 | help_seeking, exploration_pattern |

### Custom Segment Definition

```yaml
CUSTOM_SEGMENT:
  name: "[Persona Name]"

  technical_filters:
    # Demographic
    age_range: "[min]-[max]"
    location: "[region/country]"

    # Device
    device_type: "[mobile/desktop/tablet/any]"
    browser: "[specific or any]"

    # Behavioral (quantitative)
    session_duration: "[operator] [value]"
    pages_per_session: "[operator] [value]"
# ...
```
