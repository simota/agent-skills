# Heatmap Synthesis and Hotspot Extraction Reference

Purpose: Synthesize aggregate engagement density from click, mouse-movement, and scroll events into actionable hotspots and dead zones, with responsive-layout-aware coordinates, clustering-based hotspot extraction, and privacy-safe overlays.

## Scope Boundary

- **trace `heatmap`**: aggregate density synthesis, hotspot clustering, scroll-depth curves, attention-vs-action distinction, tool-feature comparison, privacy overlay rules.
- **canvas (elsewhere)**: final visualization output (diagram or overlay rendering). Trace specifies what to render; Canvas renders it.
- **pulse (elsewhere)**: page-level quantitative metrics (sessions, bounce rate, time-on-page). Trace supplements with *where* on the page attention goes.
- **palette (elsewhere)**: remediation based on dead zones (CTA repositioning, content re-prioritization).
- **cloak (elsewhere)**: privacy rules — form masking, PII redaction, consent gating for heatmap capture.

## Workflow

```
CAPTURE   →  choose heatmap type (click / move / scroll) based on question
          →  sample aggregation (full-capture vs sampled; 10-20% typical for move maps)

NORMALIZE →  viewport-relative vs absolute coordinates per breakpoint
          →  exclude sessions below min-interaction threshold (e.g., <3s, <2 events)

DENSIFY   →  density estimation (gaussian KDE for smooth, grid bucketing for fast)
          →  threshold hotspots at p95 density

CLUSTER   →  DBSCAN or k-means on event points -> labeled hotspots
          →  compute scroll-depth percentile curve

INTERPRET →  attention (move / scroll) vs action (click) distinction
          →  flag dead zones (content above fold with no clicks + high move density)

REPORT    →  hotspot list with element + density + breakpoint + recommendation
```

## Heatmap Type Selection

| Type | Answers | Watch out |
|------|---------|-----------|
| Click heatmap | Where do users actually act? | Noisy on non-interactive elements — overlay with DOM interactivity to separate dead clicks |
| Move heatmap | Where does attention go? (eye-tracking proxy) | ~60-80% mouse-gaze correlation on desktop, near zero on touch devices — do not use on mobile |
| Scroll heatmap | How far down the page do users reach? | Lazy-loaded content shifts the "fold" — always record viewport-relative + page-relative |
| Attention heatmap | Where do users *pause*? (dwell + move stillness) | Proprietary to some tools; approximate with move-density + dwell-time composite |

Pick by the question being asked. Running all four generates noise; scope to one primary heatmap per analysis.

## Density Computation

Two main methods. Pick based on dataset size and smoothness need.

| Method | Pros | Cons | Use when |
|--------|------|------|----------|
| Gaussian KDE | Smooth, publication-quality, handles sparse data | Compute-heavy, bandwidth tuning required | n<50k events, exploratory analysis |
| Grid bucketing | Fast, predictable, easy to cache | Blocky, sensitive to bucket size | n>100k events, dashboards, responsive aggregates |

KDE bandwidth tuning: Silverman's rule-of-thumb (`h = 1.06 * sigma * n^(-1/5)`) is a safe default. Manual tuning required when the page has both dense hotspots and sparse regions (bimodal density).

Grid bucket size: 20-50 CSS pixels typical. Too small = noisy; too large = hides hotspots.

## Responsive Coordinate Handling

Absolute pixel coordinates are meaningless across breakpoints. Always capture:

- `viewport_width_bucket` (e.g., `<768`, `768-1024`, `1024-1440`, `>1440`)
- `x_viewport_pct` (0-100, horizontal position as % of viewport width)
- `y_page_pct` (0-100, vertical position as % of total page height — for scroll heatmaps)
- `element_selector` (stable CSS/ARIA path — enables element-anchored aggregation across layouts)

Aggregate heatmaps per breakpoint bucket. Mixing breakpoints produces blurry heatmaps where hotspots appear as smeared clouds. When comparing breakpoints, element-anchored aggregation is more robust than coordinate-anchored.

## Hotspot Extraction via Clustering

After density estimation, extract discrete hotspot objects via clustering:

- **DBSCAN**: density-based, no k required, handles irregular shapes, ignores noise. Default for click hotspots.
  - Params: `eps` = 20-40 CSS px, `minPts` = 5-10 events.
- **k-means**: fast, requires k, assumes roughly circular clusters. Use when k is known from page layout (e.g., known CTA count).
- **HDBSCAN**: hierarchical DBSCAN, better on varying-density data. Use when page has both dense (CTAs) and diffuse (content reading) regions.

Each hotspot record: `{cluster_id, centroid_x_pct, centroid_y_pct, event_count, density, nearest_element_selector, breakpoint_bucket}`.

## Scroll-Depth Percentile Curves

```
depth_reached_pct_p50 = median depth across sessions
depth_reached_pct_p90 = 90th percentile (most engaged)
depth_reached_pct_p10 = 10th percentile (bounce surface)
```

Plot as a cumulative curve: x=page depth %, y=% of sessions reaching that depth. Inflection points reveal:

- **Steep drop near 20-30%**: the fold — expected; concerning only if >60% never scroll past.
- **Plateau at 50-70%**: content wall or dead zone — users stop reading mid-content.
- **Long tail to 100%**: strong engagement on that page segment — candidate to move key CTAs above the plateau.

## Attention vs Action Distinction

A common error: treating move-heatmap hotspots as evidence of interest in clickable affordances. They may be unrelated.

- **Move density high, click density low**: either the element is decorative (correct non-click), or it looks clickable but isn't (affordance bug — flag to Palette), or the cursor simply parks there while reading.
- **Click density high, move density low**: direct purposeful action — good.
- **Both high**: engaged interaction zone.
- **Both low**: dead zone — if it's above the fold, content-priority question.

## Tool Feature Comparison

| Tool | Click | Move | Scroll | Attention | Mobile-aware | Privacy masking |
|------|-------|------|--------|-----------|--------------|-----------------|
| Hotjar | Yes | Yes | Yes | Via integrations | Partial | Opt-in masking |
| Crazy Egg | Yes | Yes | Yes | Confetti view | Limited | Opt-in masking |
| Mouseflow | Yes | Yes | Yes | Attention heatmap | Partial | Opt-in masking |
| Microsoft Clarity | Yes | Yes | Yes | Via session replay | Yes | Automatic sensitive-field masking |
| Contentsquare | Yes | Yes | Yes | Zone-based attention | Yes | Enterprise-grade |
| FullStory | Via analytics | Limited | Yes | No | Yes | Element-level block rules |

Selection criteria: (1) native mobile-aware coordinate handling, (2) automatic form-field masking by default, (3) API access for pipeline aggregation, (4) responsive breakpoint support.

## Privacy Considerations

Heatmap overlays can leak PII if naively rendered.

- **Never render move heatmaps inside form regions** — cursor dwell over a name/email field with the underlying DOM exposed leaks the field's content via overlay positioning.
- **Mask all `input`, `textarea`, `select`, and `contenteditable` regions** at the capture layer — opt-in unmask only for whitelisted non-sensitive fields.
- **Apply client-side redaction** before data leaves the browser (SDK-layer masking), not post-ingest — matches Trace's privacy-by-default stance and provides CIPA wiretap safe harbor.
- **Exclude GPC-positive sessions** from heatmap capture at the SDK layer — 2026 state privacy laws mandate automated GPC signal recognition.
- **Low-traffic pages (<100 sessions)** can unmask individual users via unique click patterns — suppress heatmap generation below a threshold.
- **Session count disclosure** on every heatmap — "based on 1,240 sessions" — enables reviewers to judge reliability and flag small-sample risk.

## Anti-Patterns

- Rendering heatmaps that mix breakpoints into one overlay — smears hotspots and hides breakpoint-specific issues.
- Using move heatmaps on mobile — cursor-gaze correlation is desktop-specific; touch devices produce misleading move maps.
- Inferring intent from move heatmaps without click evidence — a long dwell may be reading, confusion, or idle.
- Showing heatmap overlays with form fields unmasked — privacy + legal risk.
- Aggregating scroll heatmaps across pages with different page lengths — normalize to % of page height, not absolute pixels.
- Treating a hotspot on a decorative element as a design win — users click logos out of habit, not intent.
- Reporting heatmaps without session count — reviewers cannot assess reliability.

## Handoff

- **To Canvas**: hotspot record list + breakpoint specification + recommended visualization type for rendering.
- **To Palette**: dead-zone regions + above-fold CTA miss-placement + scroll plateau positions for content reflow recommendations.
- **To Pulse**: page-level engagement metrics (avg scroll depth, hotspot click concentration) to wire as tracked KPIs.
- **To Experiment**: A/B hypothesis when repositioning a CTA from a cold zone to a documented hotspot — include Hypothesis Readiness Score.
- **To Cloak**: form-field masking rules and GPC exclusion configuration for heatmap capture SDK.
