# Funnel Handoff Templates

**Purpose:** Standardized handoff formats for inter-agent communication.
**Read when:** Receiving input from or sending output to another agent.

---

## Incoming Handoffs

### From Vision (Design Direction)

```yaml
VISION_TO_FUNNEL_HANDOFF:
  design_direction:
    mood: "[modern/clean/bold/minimal]"
    color_palette: "[primary, secondary, accent]"
    typography: "[font family, scale]"
    imagery_style: "[photo/illustration/3D/abstract]"
  brand_guidelines:
    logo_usage: "[placement rules]"
    brand_voice: "[formal/casual/technical]"
    restrictions: "[prohibitions]"
  target_impression: "[desired first impression]"
```

### From Cast (Persona Data)

```yaml
CAST_TO_FUNNEL_HANDOFF:
  persona:
    name: "[persona name]"
    demographics: "[age, job, industry]"
    pain_points: ["[pain 1]", "[pain 2]", "[pain 3]"]
    goals: ["[goal 1]", "[goal 2]"]
    objections: ["[objection 1]", "[objection 2]"]
    decision_factors: ["[factor 1]", "[factor 2]"]
    device_preference: "[mobile/desktop/both]"
```

### From Prose (Copy Drafts)

```yaml
PROSE_TO_FUNNEL_HANDOFF:
  copy:
    headline_options: ["[option 1]", "[option 2]", "[option 3]"]
    subheadline: "[subheadline]"
    benefit_statements: ["[benefit 1]", "[benefit 2]"]
    cta_options: ["[CTA 1]", "[CTA 2]"]
    voice_tone: "[tone setting]"
```

---

## Outgoing Handoffs

### To Artisan (Production Implementation)

This is the primary handoff — Funnel's main deliverable.

```yaml
FUNNEL_TO_ARTISAN_HANDOFF:
  lp_spec:
    framework: "[AIDA/PAS/BAB/4Ps]"
    section_map:
      - section: hero
        purpose: "[first view — attention capture]"
        copy:
          headline: "[headline]"
          subheadline: "[subheadline]"
          cta: "[CTA text]"
        layout: "[Pattern A/B/D]"
      - section: pain
        purpose: "[problem statement]"
        copy: "[section copy]"
      # ... all sections
    responsive:
      breakpoints: [375, 768, 1024, 1440]
      mobile_specific:
        - "Sticky CTA bar"
        - "Image hidden or reduced"
        - "Single-column stack"
    performance:
      LCP_target: "≤ 2.5s"
      CLS_target: "< 0.1"
      INP_target: "< 200ms"
      TTFB_target: "< 800ms"
      preload: ["[hero image]", "[critical font]"]
      preconnect: ["[external origins]"]
    accessibility:
      focus_visible: required
      tap_target: "≥ 44px"
      contrast: "≥ 4.5:1"
      autocomplete: required on all form fields
      prefers_reduced_motion: required
    assets:
      images: ["[image list]"]
      fonts: ["[font list]"]
    seo:
      canonical: "[canonical URL]"
      noindex_pages: ["[thank-you page]", "[UTM variants]"]
      json_ld: ["FAQPage", "Product (if pricing section)"]
```

### To Growth (SEO/CRO Optimization)

```yaml
FUNNEL_TO_GROWTH_HANDOFF:
  lp_context:
    url: "[LP URL]"
    cv_goal: "[conversion goal]"
    current_metrics:
      bounce_rate: "[rate]"
      conversion_rate: "[rate]"
    optimization_requests:
      - type: seo
        detail: "[meta/OGP/JSON-LD setup]"
      - type: cro
        detail: "[CTA/form optimization]"
```

### To Echo (Persona Validation)

```yaml
FUNNEL_TO_ECHO_HANDOFF:
  validation_request:
    lp_url: "[URL or file path]"
    target_persona: "[persona name/definition]"
    validation_focus:
      - "Headline resonance"
      - "CTA clarity"
      - "Form ease of completion"
      - "Mobile usability"
```

### To Experiment (A/B Variants)

```yaml
FUNNEL_TO_EXPERIMENT_HANDOFF:
  ab_test_request:
    hypothesis: "[changing X will improve CV rate]"
    control:
      description: "[control description]"
      key_elements:
        headline: "[current headline]"
        cta: "[current CTA]"
    variants:
      - id: "variant_a"
        changes: ["[change 1]", "[change 2]"]
    metrics:
      primary: conversion_rate
      secondary: [scroll_depth, bounce_rate]
```

### To Flow (Animation Specs)

```yaml
FUNNEL_TO_FLOW_HANDOFF:
  animation_requests:
    - element: "[element name]"
      type: "[fade_in_up/stagger/pulse]"
      trigger: "[on_load/scroll_into_view]"
      duration: "[duration]"
  constraints:
    - "Must not cause CLS"
    - "prefers-reduced-motion support required"
    - "Lightweight on mobile"
```
