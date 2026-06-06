# Gap Analysis Report

**Purpose:** Detailed, multi-dimensional gap analysis report between a mockup and its implementation. Goes beyond the basic Comparison Report by adding quantified property-level deltas, root cause classification, remediation cost, expected post-fix fidelity, and structured Markdown + JSON output.

**Read when:**
- The user asks for a "gap analysis", "fidelity audit", "detailed diff report", "ギャップ分析レポート".
- VERIFY phase needs a structured, actionable report for stakeholders (designers, PMs, QA) — not just the internal REFINE loop.
- Handoff requires an auditable artifact (CI artifact, PR comment, design review).

**Related:** `visual-verification.md` (capture + diff image generation), `precision-spec.md` (Design Spec Sheet source of truth).

---

## Contents

- When to Generate
- Dimensions (8 axes)
- Severity Taxonomy
- Root Cause Taxonomy
- Quantified Delta Metrics
- Fidelity Score Formula
- Report Template (Markdown)
- Report Schema (JSON)
- Visual Artifacts
- Generation Workflow
- Example Report

---

## When to Generate

| Trigger | Report Scope |
|---------|--------------|
| VERIFY phase internal use | Lightweight (inline diff list) — use `visual-verification.md` template |
| User requests "gap analysis" / "audit" | Full report (this file) |
| PR / CI artifact | Full report + JSON + visual artifacts |
| Design review / stakeholder handoff | Full report + visual artifacts |
| Regression investigation | Full report with root cause focus |

Generation is additive — the REFINE loop still uses the lightweight diff report for speed; the detailed report is produced once on demand or at delivery.

---

## Dimensions (8 axes)

Expanded from the 5-axis Score Breakdown. Each dimension carries a weight and a per-property delta list.

| # | Dimension | Weight | Properties Checked |
|---|-----------|--------|--------------------|
| 1 | Layout | 20% | grid-template, flex direction, element positions, alignment, z-order |
| 2 | Color | 18% | background, text, border, accent, gradient stops — measured in ΔE |
| 3 | Typography | 16% | font-family, font-size, font-weight, line-height, letter-spacing |
| 4 | Spacing | 14% | margin, padding, gap — measured in px delta |
| 5 | Components | 10% | border-radius, shadow, icon shape, button shape |
| 6 | Accessibility | 10% | contrast ratio, alt text, semantic tags, focus order, ARIA |
| 7 | Responsive | 8% | breakpoint behavior, overflow, container-query adaptation |
| 8 | Motion | 4% | transition duration, easing, animation presence |

Weight rationale:
- Layout + Color + Typography = 54% (visible-first signal).
- Accessibility = 10% (non-negotiable baseline; penalized harder at severity CRITICAL).
- Motion = 4% (low weight; screenshots rarely capture motion fidelity reliably).

Weights are defaults. Project-specific overrides are allowed; document them in the report header.

---

## Severity Taxonomy

Five levels (expanded from CRITICAL / MODERATE / MINOR).

| Level | Definition | Threshold Example | Action |
|-------|------------|-------------------|--------|
| `BLOCKING` | Ships-broken: content unreadable, layout collapse, a11y violation | Contrast <3:1, layout overflow, broken semantic structure | Must fix before delivery |
| `CRITICAL` | Clearly wrong to a designer's eye | Wrong hero image, missing gradient, wrong column count | Fix in iteration 1 |
| `MAJOR` | Noticeable on direct comparison | 4px+ spacing delta, ΔE >5, wrong font-weight | Fix in iteration 2 |
| `MINOR` | Perceptible only on overlay | 1-3px delta, ΔE 2-5, ±1 font-weight step | Fix in iteration 3 if budget allows |
| `COSMETIC` | Imperceptible without pixel diff | ΔE <2, <1px delta, sub-pixel rendering | Document as known limitation |

Promotion rules:
- A11y violations (contrast <4.5:1 for body text, <3:1 for large text) are automatically promoted to `BLOCKING` regardless of visual delta magnitude.
- Any property flagged `LOW` confidence in the Design Spec Sheet is capped at `MAJOR` severity (the delta may be measurement error, not an actual difference).

---

## Root Cause Taxonomy

Every gap must carry a root cause classification. This drives the fix owner and the expected resolution path.

| Code | Root Cause | Typical Fix Owner | Example |
|------|------------|-------------------|---------|
| `RC-EXT` | Extraction error in EXTRACT phase | Pixel | Wrong HEX extracted from JPEG-compressed mockup |
| `RC-COMP` | Composition error in COMPOSE phase | Pixel | Incorrect CSS variable wiring; magic number slipped in |
| `RC-ASSET` | Asset mismatch (images, icons, fonts) | Pixel + User | Placeholder icon vs real brand icon |
| `RC-RENDER` | Browser/OS rendering difference | Infra | macOS vs Windows font anti-aliasing |
| `RC-PLATFORM` | Platform divergence (retina vs non-retina, mobile vs desktop) | Pixel | Non-retina screenshot vs 2x mockup |
| `RC-MOCKUP` | Mockup itself is ambiguous or low-fidelity | User + Designer | Compressed JPEG, sub-720p source, gradient bands |
| `RC-FONT` | Font family unavailable or substituted | User | Brand font not licensed locally, fallback rendering |
| `RC-DYN` | Dynamic content interfering with capture | Pixel | Timestamp, ads, live counters not masked |
| `RC-SPEC` | Requirement unstated in mockup (interactivity, state) | User | Hover state, empty state, error state not shown |

Attach one primary `RC-*` per gap. Multi-cause gaps list additional codes under `contributing_causes`.

---

## Quantified Delta Metrics

All deltas are numeric. Do not rely on adjectives ("slightly smaller", "a bit off").

### Color Delta (ΔE)

Use CIEDE2000 in OKLCH or Lab space. Thresholds:

| ΔE | Perception | Severity cap |
|----|------------|--------------|
| <1 | Imperceptible | COSMETIC |
| 1-2 | Perceptible by close inspection | COSMETIC |
| 2-5 | Perceptible at a glance | MINOR |
| 5-10 | Clearly different colors | MAJOR |
| >10 | Completely different | CRITICAL |

JPEG compression alone can shift hues by 5-10 ΔE. When source is lossy, cap color gaps at `MAJOR` unless corroborated by a higher-resolution asset.

### Spacing Delta (px / rem)

| Delta | Severity cap |
|-------|--------------|
| ≤1px | COSMETIC |
| 2-3px | MINOR |
| 4-7px | MAJOR |
| 8-15px | CRITICAL |
| >15px | BLOCKING (likely layout collapse) |

Snap all targets to 4px/8px grid first; a "3px delta" that resolves by snapping is COSMETIC.

### Typography Delta

| Property | MINOR | MAJOR | CRITICAL |
|----------|-------|-------|----------|
| font-size | ±1px | ±2-3px | ±4px+ |
| font-weight | ±100 | ±200 | ±300+ |
| line-height | ±0.05 | ±0.1 | ±0.2+ |
| letter-spacing | ±0.01em | ±0.02em | ±0.05em+ |

font-family mismatches are always `MAJOR` minimum and tagged `RC-FONT`.

### Layout Delta

| Metric | MAJOR | CRITICAL | BLOCKING |
|--------|-------|----------|----------|
| Column count | — | ±1 column | ±2+ columns |
| Element position | 4-15px shift | 16-40px shift | >40px or overflow |
| Alignment | Off by 1 step | Wrong alignment axis | Flex/grid structure wrong |

### Accessibility Delta

| Check | MAJOR | BLOCKING |
|-------|-------|----------|
| Contrast ratio (body) | 4.0-4.4 | <4.0 |
| Contrast ratio (large text) | 2.5-2.9 | <2.5 |
| Missing alt | — | Any `<img>` without alt |
| Semantic structure | Missing landmark | Broken heading hierarchy |
| Focus order | Visual/DOM mismatch | Unreachable focus |

---

## Fidelity Score Formula

Two scores are reported: **Raw Fidelity** and **Confidence-Adjusted Fidelity**.

### Raw Fidelity

```
Raw = Σ (weight_i × dimension_score_i)
```

Dimension score is the per-axis percentage after penalizing each gap:

```
dimension_score = 100
  − (BLOCKING_count × 30)
  − (CRITICAL_count × 15)
  − (MAJOR_count × 6)
  − (MINOR_count × 2)
  − (COSMETIC_count × 0.5)
```

Floor at 0, cap at 100.

### Confidence-Adjusted Fidelity

Discounts the score when the Design Spec Sheet has low-confidence values in that dimension:

```
Adjusted = Raw × (1 − 0.05 × LOW_count_in_dimension / total_values_in_dimension)
```

Report both. A large gap between Raw and Adjusted signals the real bottleneck is extraction accuracy, not implementation.

### Expected Post-Fix Fidelity

For each gap, compute "if fixed". Sum the removed penalty and re-run the formula. This lets the report answer: *"If we fix only the BLOCKING + CRITICAL items, what fidelity do we reach?"*

---

## Report Template (Markdown)

```markdown
# Gap Analysis Report

## Metadata
- **Mockup**: `mockup.png` (1920×3200, PNG)
- **Implementation**: `index.html` @ commit `abc1234`
- **Viewport**: 1440×900 desktop, 375×812 mobile
- **Playwright config**: `threshold: 0.15, maxDiffPixelRatio: 0.01, animations: disabled`
- **Date**: YYYY-MM-DD
- **Iteration**: 2/3

## Executive Summary
- **Raw Fidelity**: 87.4%
- **Confidence-Adjusted Fidelity**: 82.1%
- **Expected Post-Fix (BLOCKING+CRITICAL only)**: 94.6%
- **Verdict**: REFINE (1 more iteration recommended)
- **Top Root Cause**: RC-EXT (extraction errors in 4/12 gaps)
- **Key Risk**: 2 a11y BLOCKING items require immediate attention before delivery.

## Score Breakdown

| Dimension | Weight | Raw | Adjusted | BLOCKING | CRITICAL | MAJOR | MINOR | COSMETIC |
|-----------|--------|-----|----------|----------|----------|-------|-------|----------|
| Layout | 20% | 92 | 92 | 0 | 0 | 1 | 2 | 1 |
| Color | 18% | 78 | 70 | 0 | 1 | 2 | 3 | 4 |
| Typography | 16% | 88 | 85 | 0 | 0 | 2 | 1 | 2 |
| Spacing | 14% | 90 | 90 | 0 | 0 | 1 | 3 | 2 |
| Components | 10% | 95 | 95 | 0 | 0 | 0 | 2 | 1 |
| Accessibility | 10% | 70 | 70 | 2 | 0 | 1 | 0 | 0 |
| Responsive | 8% | 92 | 88 | 0 | 0 | 1 | 1 | 0 |
| Motion | 4% | 100 | 100 | 0 | 0 | 0 | 0 | 0 |

## Gap Details

### G-001 · BLOCKING · Accessibility
- **Location**: `.hero-cta` (viewport desktop, line 42)
- **Expected**: Contrast ratio ≥ 4.5:1 (WCAG AA body text)
- **Actual**: 3.2:1 (foreground `#6B7280` on background `#E5E7EB`)
- **Delta**: −1.3 ratio points
- **Root Cause**: RC-EXT (extracted CTA background `#E5E7EB` appears lighter than mockup's `#D1D5DB`)
- **Contributing**: RC-MOCKUP (JPEG artifacts near button edges)
- **Fix**: Update `--color-cta-bg` from `#E5E7EB` to `#D1D5DB`; re-verify contrast.
- **Cost**: S (single variable change)
- **Expected post-fix**: Contrast 4.7:1, dimension score +10pt

### G-002 · CRITICAL · Color
- **Location**: Hero background gradient
- **Expected**: `linear-gradient(135deg, #1E3A8A 0%, #7C3AED 100%)`
- **Actual**: `linear-gradient(135deg, #1E40AF 0%, #8B5CF6 100%)`
- **Delta**: ΔE 11.4 (stop 1), ΔE 8.7 (stop 2)
- **Root Cause**: RC-EXT (gradient stops under-sampled)
- **Fix**: Update `--gradient-hero-from` and `--gradient-hero-to`.
- **Cost**: S
- **Expected post-fix**: ΔE < 2 for both stops, dimension score +15pt

<!-- repeat per gap, lowest ID first -->

## Root Cause Distribution

| Code | Count | % |
|------|-------|---|
| RC-EXT | 4 | 33% |
| RC-COMP | 2 | 17% |
| RC-FONT | 2 | 17% |
| RC-MOCKUP | 2 | 17% |
| RC-PLATFORM | 1 | 8% |
| RC-ASSET | 1 | 8% |

## Remediation Plan

| Priority | Gaps | Est. Cost | Expected Fidelity After |
|----------|------|-----------|-------------------------|
| P0 (BLOCKING) | G-001, G-003 | S+S | 91.2% |
| P1 (CRITICAL) | G-002 | S | 94.6% |
| P2 (MAJOR) | G-004..G-010 | M | 97.8% |
| P3 (MINOR+COSMETIC) | G-011..G-020 | M | 99.1% |

Cost legend: S (≤15 min, single variable), M (15-60 min, multiple properties / small refactor), L (>60 min, structural change or designer escalation).

## Known Limitations

- Font family `Inter` rendered via system fallback on Linux; visual match on macOS/Windows is HIGH, on Linux MEDIUM.
- Mockup source is JPEG (80% quality); color deltas <ΔE 5 are within compression noise floor.

## Visual Artifacts

- `./artifacts/side-by-side.png` — mockup / screenshot / diff triptych
- `./artifacts/heatmap.png` — pixelmatch overlay highlighting gap locations
- `./artifacts/thumbnails/` — per-section crops (hero, features, pricing, ...)

## Recommended Next Action

REFINE — 1 iteration targeting G-001 (BLOCKING) + G-002 (CRITICAL). Projected fidelity: 94.6%.
```

---

## Report Schema (JSON)

Emit alongside the Markdown so downstream agents (Canon, Judge, Voyager) can consume structured data.

```json
{
  "schema_version": "1.0",
  "metadata": {
    "mockup_path": "mockup.png",
    "implementation_ref": "abc1234",
    "viewport": [
      { "name": "desktop", "width": 1440, "height": 900 },
      { "name": "mobile", "width": 375, "height": 812 }
    ],
    "playwright_config": {
      "threshold": 0.15,
      "maxDiffPixelRatio": 0.01,
      "animations": "disabled"
    },
    "iteration": 2,
    "max_iterations": 3,
    "date": "YYYY-MM-DD"
  },
  "scores": {
    "raw_fidelity": 87.4,
    "confidence_adjusted_fidelity": 82.1,
    "expected_post_fix": {
      "blocking_only": 91.2,
      "blocking_and_critical": 94.6,
      "all_gaps": 99.1
    },
    "dimensions": [
      {
        "name": "Layout",
        "weight": 0.20,
        "raw": 92,
        "adjusted": 92,
        "severity_counts": { "BLOCKING": 0, "CRITICAL": 0, "MAJOR": 1, "MINOR": 2, "COSMETIC": 1 }
      }
    ]
  },
  "gaps": [
    {
      "id": "G-001",
      "dimension": "Accessibility",
      "severity": "BLOCKING",
      "location": ".hero-cta",
      "viewport": "desktop",
      "expected": { "contrast_ratio": 4.5 },
      "actual": { "contrast_ratio": 3.2, "fg": "#6B7280", "bg": "#E5E7EB" },
      "delta": { "contrast_ratio": -1.3 },
      "root_cause_primary": "RC-EXT",
      "contributing_causes": ["RC-MOCKUP"],
      "fix": {
        "summary": "Update --color-cta-bg to #D1D5DB",
        "css_variables_changed": ["--color-cta-bg"],
        "cost": "S"
      },
      "expected_post_fix": { "contrast_ratio": 4.7, "dimension_score_delta": 10 },
      "confidence": "HIGH"
    }
  ],
  "root_cause_distribution": {
    "RC-EXT": 4,
    "RC-COMP": 2,
    "RC-FONT": 2,
    "RC-MOCKUP": 2,
    "RC-PLATFORM": 1,
    "RC-ASSET": 1
  },
  "verdict": "REFINE",
  "known_limitations": [
    "Font rendering variance on Linux",
    "JPEG compression noise floor ΔE ≤ 5"
  ],
  "artifacts": {
    "side_by_side": "./artifacts/side-by-side.png",
    "heatmap": "./artifacts/heatmap.png",
    "thumbnails_dir": "./artifacts/thumbnails/"
  }
}
```

---

## Visual Artifacts

Three artifacts accompany the report.

### Side-by-side triptych

Horizontally stack: mockup | screenshot | pixelmatch diff. Label with viewport.

### Heatmap overlay

Pixelmatch diff with severity colors (BLOCKING=red, CRITICAL=orange, MAJOR=yellow, MINOR/COSMETIC=blue). Cluster adjacent pixels to avoid noise.

### Per-section thumbnails

Crop by detected section (hero, features, pricing, etc.) at 2x density. Each thumbnail carries its own local fidelity score so reviewers can scan deltas quickly.

Suggested script (requires `pngjs`, `pixelmatch`, `sharp`):

```javascript
// generate-artifacts.js
// 1. Read mockup.png and screenshot.png
// 2. Normalize dimensions (resize screenshot to mockup width preserving aspect)
// 3. pixelmatch → diff.png
// 4. sharp.join([mockup, screenshot, diff]) → side-by-side.png
// 5. Crop per section using locator bounding boxes exported during VERIFY
// 6. Emit heatmap: recolor diff by severity clusters
```

Keep the script under 120 lines; prefer composing existing npm libs over bespoke algorithms.

---

## Generation Workflow

```
VERIFY complete
  │
  ├─ Collect gap list from per-property verification
  ├─ Classify each gap: dimension, severity, root cause, delta
  ├─ Compute scores (raw, adjusted, post-fix scenarios)
  ├─ Rank gaps: severity DESC, then dimension weight DESC, then delta magnitude DESC
  ├─ Generate artifacts (side-by-side, heatmap, thumbnails)
  ├─ Emit Markdown report + JSON schema
  └─ Attach to delivery / PR / CI artifact
```

Checklist before emitting the report:

- [ ] Every gap has `severity` + `root_cause_primary` + numeric `delta`.
- [ ] BLOCKING items include a11y check references (WCAG criterion ID).
- [ ] LOW-confidence Spec Sheet values are flagged; severity capped at MAJOR.
- [ ] Raw vs Adjusted fidelity both reported.
- [ ] Expected post-fix computed for BLOCKING-only and BLOCKING+CRITICAL.
- [ ] Artifacts generated at same viewport as the capture.
- [ ] JSON passes schema validation (schema_version, required fields).

---

## Example Report

See the template above. A real example accompanies the `examples.md` file under section "Gap Analysis Report — E-commerce Pricing Page".

---

## Handoff Hints

| Downstream | What to include |
|------------|-----------------|
| Artisan | Full Markdown + JSON + Design Spec Sheet; Artisan fixes via CSS variables |
| Muse | JSON `gaps[*].fix.css_variables_changed` to extract token regressions |
| Voyager | JSON `artifacts.side_by_side` and `heatmap` as baseline candidates |
| Canon | JSON for WCAG compliance mapping on BLOCKING a11y gaps |
| Judge | Full Markdown for quality review; highlight RC-EXT cluster (signals Pixel self-improvement need) |

---

## Anti-Patterns

- **Adjective-only deltas**: "slightly off", "a bit bright" — always quantify (ΔE, px, ratio).
- **Severity by feel**: use the taxonomy thresholds, not intuition.
- **Ignoring root cause**: a gap without RC is a bug report without a fix path.
- **Hiding LOW-confidence impact**: Adjusted Fidelity must be shown; do not silently paper over extraction uncertainty.
- **Oversized reports**: if the gap list exceeds 40 items, cluster COSMETIC items into aggregate rows ("12 sub-pixel border-radius deltas, ΔE < 1 average").
- **Artifacts out of sync**: regenerate heatmap/thumbnails if any CSS variable changes after the last capture.
