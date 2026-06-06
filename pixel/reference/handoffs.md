# Handoff Templates

**Purpose:** Standardized handoff formats for Pixel's input and output partners.
**Read when:** You need to receive from or deliver to another agent in the ecosystem.

## Contents
- Handoff Overview
- Receiving Handoffs (Input)
- Sending Handoffs (Output)

---

## Handoff Overview

```
┌─────────────────┐          ┌───────┐          ┌──────────────────┐
│  INPUT FROM      │          │       │          │  OUTPUT TO        │
│  User (images)   │─────────▶│       │─────────▶│  Artisan          │
│  Vision (dir.)   │          │ Pixel │          │  Muse             │
│  Frame (exports) │          │       │          │  Growth           │
│  Nexus (context) │          │       │          │  Flow             │
└─────────────────┘          └───────┘          │  Voyager          │
                                                 │  Canon (gap audit)│
                                                 │  Judge (gap audit)│
                                                 └──────────────────┘
```

---

## Receiving Handoffs (Input)

### From User (Direct)

The most common input — user provides mockup images directly.

```yaml
PIXEL_INPUT:
  source: User
  mockup:
    path: "[image file path]"
    format: "PNG | JPG | Screenshot"
    viewport: "[estimated viewport width, if known]"
  requirements:
    framework: "[Vanilla | React | Vue | Svelte | auto]"
    scope: "[full-page | section-name | verify-only]"
    fidelity_target: "[percentage, default: 90%]"
  notes: "[any additional context from the user]"
```

### From Vision (Design Direction)

When Vision provides creative direction alongside or before a mockup.

```yaml
VISION_TO_PIXEL_HANDOFF:
  source: Vision
  design_direction:
    style: "[modern, minimal, bold, etc.]"
    color_mood: "[warm, cool, vibrant, muted]"
    typography_feel: "[geometric, humanist, serif]"
  constraints:
    brand_colors: ["#hex1", "#hex2"]
    typography: "[font family if specified]"
    tone: "[professional, playful, technical]"
  mockup_ref: "[path to mockup image if available]"
```

**Merge strategy**: When both mockup image and Vision direction exist, prefer the mockup for visual values (colors, sizes) and Vision for subjective decisions (tone, feel, fallback choices).

### From Frame (Figma Export)

When Frame provides extracted Figma design data as supplementary context.

```yaml
FRAME_TO_PIXEL_HANDOFF:
  source: Frame
  figma_context:
    source_url: "[Figma file URL]"
    file_version: "[version ID]"
    extracted: "[ISO timestamp]"
  design_data:
    colors:
      - { name: "primary", value: "#hex", variable: "colors/primary" }
    typography:
      - { name: "heading-1", size: "48px", weight: 700, family: "Inter" }
    spacing:
      - { name: "section-gap", value: "96px" }
    components:
      - { name: "Button/Primary", code_connect: true }
  assets:
    - { path: "[exported asset path]", type: "icon | image | logo" }
```

**Merge strategy**: Frame data provides HIGH confidence values. Override Pixel's image-based estimates with Frame's exact values when available.

### From Nexus (Task Context)

```yaml
_AGENT_CONTEXT:
  Role: Pixel
  Task: "[Specific task description]"
  Mode: AUTORUN
  Chain: ["[previous agents]"]
  Input: "[mockup path or handoff content]"
  Constraints:
    - "[constraint 1]"
    - "[constraint 2]"
  Expected_Output: "[what Nexus expects]"
```

---

## Sending Handoffs (Output)

### To Artisan (Production Quality)

Primary handoff — Artisan converts Pixel's HTML/CSS into production-quality components.

```yaml
PIXEL_TO_ARTISAN_HANDOFF:
  source: Pixel
  code:
    files:
      - path: "[HTML file path]"
        type: "created"
        description: "Mockup-faithful HTML structure"
      - path: "[CSS file path]"
        type: "created"
        description: "Extracted design values as CSS"
  design_values:
    colors:
      - { role: "bg-base", value: "#ffffff", confidence: "HIGH" }
      - { role: "text-primary", value: "#111827", confidence: "MEDIUM" }
      - { role: "accent", value: "#2563eb", confidence: "MEDIUM" }
    typography:
      - { element: "h1", size: "3rem", weight: 700, confidence: "MEDIUM" }
      - { element: "body", size: "1rem", weight: 400, confidence: "HIGH" }
    spacing:
      - { context: "section-padding", value: "5rem", confidence: "MEDIUM" }
  verification:
    fidelity_score: "[percentage]"
    iterations_completed: "[1-3]"
    remaining_differences:
      - { area: "[description]", severity: "MINOR", reason: "[explanation]" }
  recommendations:
    - "Convert to React/Tailwind components"
    - "Add TypeScript interfaces for props"
    - "Implement error boundaries and loading states"
    - "LOW confidence font — verify Inter with designer"
  framework_suggestion: "[React | Vue | Svelte based on project context]"
```

### To Muse (Token Systemization)

When extracted design values should be formalized as design tokens.

```yaml
PIXEL_TO_MUSE_HANDOFF:
  source: Pixel
  extracted_tokens:
    colors:
      - { role: "bg-base", value: "#ffffff", confidence: "HIGH" }
      - { role: "bg-surface", value: "#f9fafb", confidence: "MEDIUM" }
      - { role: "text-primary", value: "#111827", confidence: "MEDIUM" }
      - { role: "text-secondary", value: "#6b7280", confidence: "MEDIUM" }
      - { role: "accent-primary", value: "#2563eb", confidence: "MEDIUM" }
      - { role: "border-default", value: "#e5e7eb", confidence: "MEDIUM" }
    spacing:
      - { name: "xs", value: "0.25rem", confidence: "MEDIUM" }
      - { name: "sm", value: "0.5rem", confidence: "MEDIUM" }
      - { name: "md", value: "1rem", confidence: "MEDIUM" }
      - { name: "lg", value: "1.5rem", confidence: "MEDIUM" }
      - { name: "xl", value: "2rem", confidence: "MEDIUM" }
      - { name: "section", value: "5rem", confidence: "MEDIUM" }
    typography:
      - { name: "display", size: "3rem", weight: 700, confidence: "MEDIUM" }
      - { name: "heading", size: "1.875rem", weight: 700, confidence: "MEDIUM" }
      - { name: "body", size: "1rem", weight: 400, confidence: "HIGH" }
      - { name: "small", size: "0.875rem", weight: 400, confidence: "MEDIUM" }
  source_mockup: "[mockup file path]"
  notes: "Extracted from image analysis. LOW confidence values should be verified."
  recommendations:
    - "Formalize as CSS custom properties or Tailwind theme extension"
    - "Verify font family with design team"
```

### To Growth (SEO/CRO)

When LP code needs SEO meta tags and CRO optimization.

```yaml
PIXEL_TO_GROWTH_HANDOFF:
  source: Pixel
  page:
    type: "Landing Page"
    sections: ["hero", "features", "pricing", "faq", "cta", "footer"]
    files:
      - path: "[HTML file path]"
  content:
    headings:
      - { level: "h1", text: "[hero headline]" }
      - { level: "h2", text: "[section headings]" }
    cta_buttons:
      - { text: "[CTA text]", location: "hero" }
      - { text: "[CTA text]", location: "final-cta" }
  needs:
    - "Meta tags (title, description, OGP)"
    - "JSON-LD structured data"
    - "Heading hierarchy optimization"
    - "CTA copy review for conversion"
```

### To Flow (Animation Specs)

When the mockup suggests animation or transition needs.

```yaml
PIXEL_TO_FLOW_HANDOFF:
  source: Pixel
  animation_needs:
    - element: "[CSS selector]"
      type: "[hover | scroll | load | interaction]"
      description: "[What animation the mockup suggests]"
      confidence: "LOW"
  files:
    - path: "[HTML file path]"
    - path: "[CSS file path]"
  notes: "Animation requirements inferred from static mockup. Confirm with designer."
```

### To Voyager (Visual Regression)

When setting up regression testing baselines.

```yaml
PIXEL_TO_VOYAGER_HANDOFF:
  source: Pixel
  baseline:
    mockup: "[mockup file path]"
    screenshot: "[captured screenshot path]"
    fidelity_score: "[percentage]"
    viewport: "[width x height]"
  test_setup:
    page_url: "[URL or file path]"
    sections:
      - { selector: ".hero", name: "Hero section" }
      - { selector: ".features", name: "Features section" }
    viewports:
      - { name: "mobile", width: 375, height: 812 }
      - { name: "tablet", width: 768, height: 1024 }
      - { name: "desktop", width: 1440, height: 900 }
  recommendations:
    - "Set up Playwright visual comparison tests"
    - "Use captured screenshot as baseline for regression"
    - "Monitor fidelity score in CI/CD"
```

### To Canon (Gap Analysis → Standards Mapping)

When a gap analysis report has been produced and accessibility / standards mapping is needed.

```yaml
PIXEL_TO_CANON_HANDOFF:
  source: Pixel
  gap_report:
    markdown_path: "[./artifacts/gap-analysis-report.md]"
    json_path: "[./artifacts/gap-analysis-report.json]"
    schema_version: "1.0"
  a11y_focus:
    blocking_items:
      - { id: "G-001", wcag_candidate: "1.4.3", dimension: "Accessibility", delta: { contrast_ratio: -1.3 } }
    scores:
      accessibility_raw: "[0-100]"
      accessibility_adjusted: "[0-100]"
  needs:
    - "Map BLOCKING a11y gaps to specific WCAG 2.2 success criteria"
    - "Cross-reference against ISO 25010 usability sub-characteristics if relevant"
    - "Produce compliance verdict (PASS / PASS_WITH_CAVEATS / FAIL) with citations"
  artifacts:
    side_by_side: "./artifacts/side-by-side.png"
    heatmap: "./artifacts/heatmap.png"
  note: "Pixel quantifies visual fidelity; Canon normatively evaluates standards conformance. No overlap — Canon's output is the authoritative WCAG verdict."
```

### To Judge (Gap Analysis → Fidelity Review)

When the gap analysis report itself should be adversarially reviewed before delivery (PR artifact, design review, external stakeholder).

```yaml
PIXEL_TO_JUDGE_HANDOFF:
  source: Pixel
  review_target:
    type: "Gap Analysis Report"
    markdown_path: "[./artifacts/gap-analysis-report.md]"
    json_path: "[./artifacts/gap-analysis-report.json]"
  scope:
    - "Severity classification accuracy (BLOCKING/CRITICAL/MAJOR/MINOR/COSMETIC thresholds)"
    - "Root cause assignment reasonableness (RC-EXT vs RC-COMP vs RC-MOCKUP)"
    - "Delta quantification correctness (ΔE, px, contrast ratio math)"
    - "Remediation cost estimates (S/M/L) vs actual fix scope"
    - "Expected post-fix fidelity claims"
  context:
    iteration: "[1-3]"
    raw_fidelity: "[0-100]"
    adjusted_fidelity: "[0-100]"
    total_gaps: "[N]"
  needs:
    - "Flag any gap whose severity is mis-escalated or under-called"
    - "Verify RC-EXT cluster signals (if 30%+ are RC-EXT, extraction is the bottleneck — escalate to Pixel self-improvement)"
    - "Block delivery if BLOCKING a11y items lack WCAG citation"
  note: "Judge reviews the report's internal consistency, not the underlying implementation. Use findings to sharpen future Pixel iterations."
```
