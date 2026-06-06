# Craft Standards

The super-quality bar for Design, Animation, and Branding axes. These are the standards `lure` enforces upstream of and across Stages 4–7. Lighthouse and WCAG are the floor — this document defines the ceiling.

> A landing page that hits the perf budget but feels generic loses to a landing page that hits the same budget and feels inevitable. Craft is the difference.

---

## Design Discipline

### 1. Visual Hierarchy Rubric

Score each LP from 0–3 per criterion. **Ship target: ≥ 20/27**.

| Criterion | 3 — Excellent | 2 — Good | 1 — Weak | 0 — Broken |
|-----------|---------------|----------|----------|------------|
| **Hero-Contract Legibility** | What / for whom / why-now answerable in ≤ 5 seconds | 6–8 seconds | 8–12 seconds | Not answerable |
| **Primary focal point** | Single, unmistakable focal point above fold | One focal point with some competition | Multiple competing elements | No focal point |
| **Scale contrast** | Hero element ≥ 3× secondary | 2× contrast | 1.5× contrast | Flat |
| **Weight contrast** | Bold vs. regular vs. light used purposefully | Two weights with clear roles | Inconsistent weight use | Single weight everywhere |
| **Color hierarchy** | Accent reserved for actions/highlights; neutral palette carries body | Mostly disciplined | Accent overused | Accent everywhere |
| **Whitespace rhythm** | Section padding follows tokens; breathing room around CTAs | Mostly consistent | Cramped or arbitrary | No system |
| **Scan-pattern coherence** | Layout matches chosen pattern (F / Z / Layer-cake / Centered / Card-grid) per `ia-blueprint.md` | Mostly aligned | Some misalignment | Random placement |
| **Section identity** | Each section visually distinct yet cohesive | Mostly distinct | Sections blur into each other | All sections look the same |
| **Mobile fidelity** | Mobile is designed, not shrunk; tap targets ≥ 44×44 px; thumb-zone aware | Adapted; targets ≥ 40 px | Reactive only | Broken on mobile |

### 2. Typography Craft

- **Type scale**: modular (e.g., 1.25, 1.333, 1.5 ratio). Document the ratio in `tokens.json`. No off-scale sizes.
- **Display headline**: 1 family, 1–2 weights. Optical sizing if variable font. Pair with body for clear contrast (serif↔sans or display↔text).
- **Body line-height**: 1.5–1.7 for paragraphs, 1.2–1.35 for headlines, 1.1 for display.
- **Measure (line length)**: 45–75 characters for body. Enforce `max-width` per breakpoint.
- **Kerning + balance**: `text-wrap: balance` on headlines; `text-wrap: pretty` on paragraphs (where supported, with fallback).
- **Variable font axes**: use weight/optical-size/slant axes when available; ship single woff2 file under 100KB subsetted.
- **Numerical typography**: tabular numerals for pricing, stats, dashboards (`font-variant-numeric: tabular-nums`).
- **2026 trend awareness**: kinetic typography on hero (animated weight/width shift), pair with reduced-motion fallback.

### 3. Color Discipline

- **Token-only**: zero hardcoded color values in production code. Enforced at Build gate.
- **Semantic naming**: `--color-action-primary` not `--color-blue-500`. Surface vs. ink vs. accent vs. status.
- **Contrast ratios**:
  - Body text: ≥ 4.5:1 (AA)
  - Large text (18px+ bold or 24px+): ≥ 3:1 (AA)
  - UI components / focus indicators: ≥ 3:1 (AA)
  - **Stretch target**: AAA where feasible (7:1 body, 4.5:1 UI)
- **Color blindness**: verify against Deuteranopia + Protanopia + Tritanopia simulators; never rely on color alone for state.
- **Dark mode**: if in scope, use `color-mix()` for tonal variants; preserve hierarchy across modes.
- **Gradient usage**: purposeful, brand-coherent. Banned: rainbow gradients without semantic anchor. Encouraged: 2-stop subtle gradients on hero, mesh gradients with motion budget.

### 4. Whitespace Rhythm

- Section vertical rhythm: based on a spacing scale (4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128 px). Tokenized.
- Above-fold spacing: hero copy ↔ CTA ≥ 24px; CTA ↔ trust strip ≥ 32px.
- Section padding: 64–128px desktop, 40–80px mobile, scaled by content density.
- Microspacing: 4/8/12px between elements within a card; never arbitrary `margin: 11px`.

### 5. Detail Craft

The differentiator between B+ and A+ LPs:

- **Cursor states**: every interactive element has a hover + focus + active state. No `cursor: default` on buttons.
- **Focus rings**: visible, branded, AA contrast against any background.
- **Empty states**: every list / search / filter has an explicit empty state with copy + illustration.
- **Loading states**: skeleton screens for any content > 100ms; spinner only for genuine indeterminate wait.
- **Error states**: every form field has specific error microcopy (Prose), never "Invalid input".
- **Icon system**: single icon family (Ink-produced or curated set). Stroke weight matches typography weight. Pixel-aligned at 16/20/24/32.
- **Image craft**: every hero / lifestyle / illustration has intentional crop, focal point, exposure consistency. No stock-photo bingo.

### 6. 2026 Design Trend Calibration

Read awareness, not mandatory adoption. Apply only when brand and audience justify.

| Trend | When to adopt | When to skip |
|-------|---------------|--------------|
| **Liquid Glass / dimensional UI** | Premium hardware / consumer apps / luxury B2C | Trust-critical B2B (banking, healthcare) |
| **Kinetic typography on hero** | Brand-led launches, creative-industry, design tools | Calm UI / clarity-led / accessibility-critical |
| **Mesh gradients + organic shapes** | Modern SaaS, creator economy, lifestyle | Enterprise SaaS / professional services |
| **Brutalist editorial** | Strong-POV brands, agencies, niche communities | Mass market / conversion-first |
| **Calm UI / generous whitespace** | Trust-critical (legal, finance, health, premium) | Direct-response / high-urgency campaigns |
| **3D / Spline / interactive demos** | Product-led demos, hardware showcases | Performance-budget-constrained pages |
| **AI-driven adaptive UI** | SaaS with rich behavioral data, ecom personalization | Trust-critical / fixed-message brand launches |
| **Variable-font dynamic typography** | Modern editorial, brand-led design tools | Multi-locale LPs (subsetting complexity) |
| **Spatial / Z-axis layering (non-XR depth)** | Premium hardware, creative tools, design portfolios | Information-dense B2B / dashboards |
| **Anti-AI-look / human craft signaling** | Heritage brands, craft / artisanal, anti-tech positioning | AI-native products (counter-message) |

**Mandatory rule**: when adopting AI-driven adaptive UI, an explainability affordance ("Why am I seeing this?") must be present and tested. This is gate-checked at DESIGN exit when the trend is in scope.

---

## Animation Discipline

### 1. Motion Tokens

Define in `tokens.json` under `motion.*`:

```json
{
  "motion": {
    "duration": {
      "instant": "75ms",
      "fast": "150ms",
      "base": "250ms",
      "slow": "400ms",
      "deliberate": "600ms"
    },
    "easing": {
      "standard": "cubic-bezier(0.4, 0, 0.2, 1)",
      "decelerate": "cubic-bezier(0, 0, 0.2, 1)",
      "accelerate": "cubic-bezier(0.4, 0, 1, 1)",
      "emphasized": "cubic-bezier(0.2, 0, 0, 1)",
      "spring-snappy": "linear(0, 0.5 25%, 1 50%, 0.85 65%, 1)"
    },
    "stagger": {
      "tight": "30ms",
      "comfortable": "60ms",
      "dramatic": "120ms"
    }
  }
}
```

### 2. Motion Principles

| Principle | Rule |
|-----------|------|
| **Purpose** | Every animation answers: orient (where I am), feedback (what happened), delight (brand). No motion without one of these. |
| **Speed** | UI feedback < 200ms. Section transitions 250–400ms. Hero/atmospheric ≤ 600ms. Never longer unless cinematic and skippable. |
| **Easing** | Standard easing for most. Decelerate for entrances. Accelerate for exits. Emphasized for hero moments. Spring for playful brand. Never linear (except progress). |
| **Choreography** | Coordinated, not chaotic. Stagger reveals 30–120ms; one element starts, the next begins as the first crosses ~60% progress. |
| **Direction** | Motion direction matches information flow. Top-to-bottom for new content; left-to-right for forward; right-to-left for back. |
| **Reduced motion** | `@media (prefers-reduced-motion: reduce)` removes parallax, autoplay, infinite loops, attention-grabbing motion. Functional transitions can keep 100ms cross-fades. |
| **Performance** | Animate only `transform`, `opacity`, `filter`. Never layout-triggering properties (width/height/top/left). |
| **INP budget (HARD CEILING)** | Motion contribution to INP ≤ 50ms is a **hard ceiling, not a rubric criterion**. Failure to meet it triggers immediate Flow+Bolt repair (see `quality-gates.md` Oscillation Guard); motion rubric scoring continues only after the ceiling is met. |

### 3. Motion Patterns (named, reusable)

| Pattern | Use | Implementation |
|---------|-----|----------------|
| **Hero entrance** | Above-fold reveal | Stagger headline → sub → CTA → hero asset; decelerate 400ms |
| **Section enter** | Scroll-into-view | IntersectionObserver fade-up 24px, decelerate 300ms, once |
| **Scroll-driven progress** | Page progress, parallax | CSS `animation-timeline: scroll()` — no JS scroll listeners |
| **CTA hover** | Buttons / cards | 150ms transform scale 1.02 + shadow lift |
| **Form feedback** | Input focus / error | 200ms outline + 75ms shake (errors only, 1 cycle, low amplitude) |
| **Modal / sheet** | Overlay panels | View Transitions API where supported; fallback to 250ms slide+fade |
| **Loading skeleton** | Async content | Subtle linear gradient sweep, 1.5s loop, paused under reduced-motion |
| **Counter / stat reveal** | Numbers in social proof | requestAnimationFrame ease-out 800–1200ms, observed once |
| **Microinteraction confirm** | Successful submit / copy / save | 250ms checkmark draw + 600ms bloom + auto-dismiss |

### 4. Tool & Format Choice

| Asset | Tool | Format | When |
|-------|------|--------|------|
| Simple UI motion | CSS / WAAPI | n/a | Default for transforms, opacity, focus, hover |
| Scroll-driven | Native CSS `animation-timeline` | n/a | Modern browsers; no JS scroll listeners |
| Complex character / illustration | Lottie | `.lottie` (dotLottie) | Hero motion, brand mascot |
| Interactive vector | Rive | `.riv` | State-machine driven, lightweight |
| Page transitions | View Transitions API | n/a | SPA navigation, multi-step forms |
| 3D / dimensional | Spline / Three.js | embed / canvas | Premium product demos only |
| Video background | `.mp4` + poster | h.264 + AV1 | Atmospheric hero, with reduced-motion fallback |

### 5. Motion Quality Rubric

Ship target: ≥ 15/20.

| Criterion | 4 — Excellent | 3 — Good | 2 — Weak | 1 — Broken |
|-----------|---------------|----------|----------|------------|
| **Purpose clarity** | Every animation has a reason | Most do | Some decorative-only | Motion for motion's sake |
| **Choreography** | Sequenced reveals feel composed | Mostly coordinated | Some clashes | Everything moves at once |
| **Easing fit** | Easing matches motion type | Mostly | Some linear | All linear |
| **Reduced-motion respect** | Full alternative path | Most paths | Partial | Ignored |
| **Performance** | All on compositor; INP ≤ 200ms | Mostly | Some layout-triggering | Jank visible |

---

## Branding Discipline

### 1. Brand System Anatomy

Before any LP design, the brand system must be defined or referenced. Missing pieces → ask user or escalate to Vision/Saga. **Vision authors the Voice_Spectrum; Prose executes voice in copy**.

```yaml
BRAND_SYSTEM:
  Promise:
    Statement: "<the one-sentence outcome the brand delivers>"
    Type: "Functional | Emotional | Self-Expressive | Aspirational"
  Story:
    Hero: "<customer is the hero — OR — guide-as-hero for technical-developer / category-creator brands>"
    Guide: "<brand is the guide>"
    Problem: "<external + internal + philosophical>"
    Plan: "<3-step path>"
    Success: "<vivid after-state>"
    Failure: "<vivid stakes>"
  Positioning:
    Category: "<the category the brand competes in>"
    Differentiator: "<what makes it different>"
    For_Whom: "<primary audience>"
    Against_Whom: "<the alternative being displaced>"
    Anti_Archetype: "<what the brand explicitly is NOT — sharpens differentiation>"
  Verbal_Identity:
    Tagline: "<≤7 words, ownable, brand-voice-loaded — Saga + Prose>"
    Naming_Pattern: "<product nomenclature rule — e.g., verb-led, mythic, kebab-noun>"
    Claim_Ladder: ["<top claim>", "<supporting claim>", "<proof point>"]
    Big_Idea_Owner: "Compete + Funnel"
    Tagline_Owner: "Saga + Prose"
    Visual_Claim_Owner: "Vision"
  Voice_and_Tone:
    Personality: ["<3-5 adjectives>"]
    Voice_Spectrum:                          # Vision authors
      Formal_to_Casual: "<0..10>"
      Reserved_to_Enthusiastic: "<0..10>"
      Serious_to_Playful: "<0..10>"
      Mainstream_to_Bold: "<0..10>"
    Always_Say: ["<patterns>"]
    Never_Say: ["<anti-patterns>"]
    Tone_Variants:                           # Prose executes — DESIGN gate verifies all 5 are drafted
      Hero: "<bold, declarative>"
      Pricing: "<clear, no hedging>"
      Errors: "<helpful, never shaming>"
      Empty_State: "<warm, directive>"
      Legal: "<plain, scannable>"
  Visual_Identity:
    Archetype: "<Sage | Hero | Outlaw | Magician | Everyman | Lover | Jester | Caregiver | Ruler | Creator | Innocent | Explorer | Oracle/Agent | Operator>"
    Secondary_Archetype: { archetype: "<one of above>", mix_ratio: "70:30 | 60:40 | none" }
    Mood: ["<3-5 keywords>"]
    Color_Story: "<warm/cool/neutral + accent strategy>"
    Type_Story: "<display + body pairing rationale>"
    Image_Style: "<photography vs illustration vs 3D + treatment>"
    Image_License_Posture: "Commissioned | Licensed-stock | AI-generated | Mixed"
    Motion_Story: "<calm vs energetic vs precise vs playful>"
  Accessibility_Stance:
    Baseline: "WCAG 2.2 AA"
    Stretch: "AAA where feasible"
    Motion_Budget: "<reduced-motion mandatory; rich-motion default = on/off>"
  Evidence_Bank:
    Numeric_Proof: ["<stat with source and date>", ...]
    Named_Customers: ["<logo + outcome>", ...]
    Awards_Press: ["<source>", ...]
    Author_Authority: { person: "<name>", credentials: "<list>", sameAs: ["<LinkedIn>", "<ORCID>", "<Wikidata>"] }
```

Two added archetypes for 2026 LPs:
- **Oracle / Agent** — AI-native brands whose promise is autonomous outcomes; requires explainability affordance ("Why am I seeing this?") in any AI-driven adaptive surface.
- **Operator** — Linear / Stripe / Vercel cluster: Sage authority + Creator precision with deliberate personality restraint. Distinct from Sage in restraint discipline.

### 2. `direction.md` Minimum Payload Contract

When Vision emits `direction.md` to Muse, the file MUST contain (else Muse rejects and returns to Vision with a `brand` recipe):

```markdown
# direction.md

## Archetype
Primary: <archetype>
Secondary (optional): <archetype> mix <ratio>
Rationale: <2-3 sentences>

## Mood
Keywords: <3-5>
Reference moodboard: <path or links>

## Type Direction
Display family + weights: <names>
Body family + weights: <names>
Scale ratio: <e.g., 1.25 / 1.333 / 1.5>
Variable-axis usage (if any): <wght / opsz / slnt>
Kinetic typography: <on/off + scope>

## Palette Intent
Strategy: <warm/cool/neutral + accent strategy>
Surface ↔ ink contrast target: <AA / AAA>
Dark-mode posture: <single-mode | auto-switch | manual-toggle>

## Motion Intent
Motion story: <calm | energetic | precise | playful>
Tempo: <duration baseline e.g., 250ms>
Reduced-motion alternative declared: yes/no

## Scan-Pattern Preference
Primary pattern: <F / Z / Layer-cake / Centered axis / Card grid>
Rationale: <why this matches archetype + persona>

## Asset Direction
Image style: <photography / illustration / 3D / mixed>
License posture: <commissioned / licensed-stock / AI-generated>
AI-driven adaptive UI: <on/off; if on, explainability indicator location declared>
```

### 2. Brand Voice Application

Voice = consistent personality across all copy. Tone = situational adjustment.

- **Hero**: highest brand voice expression. Bold, distilled, memorable.
- **Body benefits**: voice slightly dialed back for clarity. Specifics + outcomes.
- **Microcopy / errors**: tone shifts to helpful + warm. Voice still present but quiet.
- **Legal / footer**: plain language, voice barely visible, but never robotic.

Prose owns voice execution. `lure` confirms the brand system is referenced.

### 3. Positioning Discipline

Use Compete's positioning map output. The LP must:

1. Name the category the brand operates in (explicit or implicit, never both unclear).
2. Make the differentiator visible above the fold or by section 2.
3. Address the "against whom" frame in objection handling.

Anti-pattern: feature-list LP that competes on parity instead of positioning.

### 4. Brand Coherence Check (Verify stage)

Three-channel coherence audit:

| Channel | What to check |
|---------|---------------|
| **Visual** | Token usage matches brand archetype. Imagery treatment matches image style. Motion matches motion story. |
| **Voice** | Sample 10 copy strings across LP. Score each on the voice spectrum. Variance < 1.5 points per axis. |
| **Experience** | Form fields, micro-interactions, success states all reinforce brand personality. Errors don't break voice. |

A regression on any channel = repair before Launch.

### 5. Brand Quality Rubric

**Ship target: ≥ 17/24** (6 criteria × 4 points).

| Criterion | 4 — Excellent | 3 — Good | 2 — Weak | 1 — Broken |
|-----------|---------------|----------|----------|------------|
| **Promise clarity** | One-sentence test passes in 5 seconds | Mostly clear | Hedged or generic | No discernible promise |
| **Voice consistency** | All copy reads as one author (variance < 1.5 per spectrum axis) | Mostly | Some inconsistency (variance 1.5–2.5) | Multiple voices clash (variance > 2.5) |
| **Positioning crispness** | Category + differentiator + against-whom + anti-archetype clear | Mostly | Two of four | None visible |
| **Visual coherence** | Archetype (incl. secondary mix) reads in <3 seconds | Mostly | Mixed signals | No archetype |
| **Story echo** | Hero arc visible (customer-as-hero by default; guide-as-hero acceptable for technical-developer brands when declared in Brand System) | Mostly | Implicit only | Brand-as-hero anti-pattern |
| **Trust-signal density** | ≥3 trust mechanics surfaced by section 2 (named-customer outcome / numeric proof / press / open-source / guarantee / author authority) | 2 mechanics | 1 mechanic | None — brand asks for action without credibility |

---

## Cross-Discipline Coordination

These rules govern how Design, Animation, and Branding stay aligned:

1. **Brand system precedes design tokens.** Vision + Saga define brand before Muse generates tokens. Tokens must encode brand decisions, not the inverse.
2. **Motion story comes from brand archetype.** A "Sage" brand uses deliberate, calm motion; a "Jester" brand uses snappy, playful motion. Flow consults Vision's `direction.md` before authoring motion tokens.
3. **Design rubric scoring happens before Build.** No production code on a < 18/24 design or < 15/20 motion or < 14/20 brand score. Repair or escalate.
4. **Detail craft is the Verify checklist's secret tier.** Judge re-walks for cursor states, focus rings, empty states, loading states, error states, icon consistency, image craft. Anything missing = P2 finding.
