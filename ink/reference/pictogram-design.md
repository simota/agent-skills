# Pictogram Design

## Purpose

Pictograms are not icons. Icons live in UI; pictograms live in the world — wayfinding, safety, accessibility, public-information signage. Pictograms must be readable at distance, across cultures, by people who don't share a language. This reference covers ISO standards, design rules, and verification.

## Scope Boundary

- IN scope: ISO 7001 (public information), ISO 7010 (safety signs), AIGA Symbol Signs, ADA / accessibility pictograms, brand pictograms with cross-cultural intent, viewing-distance scaling.
- OUT of scope: UI icons (`icon`), illustrations (`illustration`), logos (`logo`), animation (`animate`), color theming (`theme`), pixel art (delegate to `dot`).

## Core Concepts

### Pictogram vs Icon vs Illustration

| Type | Audience | Distance | Color | Detail |
|------|----------|----------|-------|--------|
| UI icon | Users in product | screen 16-48 px | brand palette + currentColor | minimal, design-system-tuned |
| Pictogram | Public, multilingual | 5-200 m | high-contrast specific (ISO codes) | bold, simplified, recognizable in a glance |
| Illustration | Marketing / editorial | varies | full palette | rich, narrative |

Mixing them confuses users — wayfinding signage with UI-icon style fails in a noisy environment.

### Standards Map

| Standard | Domain | Symbols |
|----------|--------|---------|
| ISO 7001 | Public information signs | toilet, exit, parking, transit, services |
| ISO 7010 | Safety signs | prohibition (red circle), warning (yellow triangle), mandatory (blue circle), emergency (green square), fire (red square) |
| ISO 9186 | Pictogram comprehension testing | how to verify a pictogram works |
| AIGA Symbol Signs (1974) | US public-info signs | 50 transit pictograms (free for use) |
| ADA / Section 508 | US accessibility | barrier-free, hearing loop, accessible route |
| EN ISO 7239 | Public-information conventions in Europe | parallel to ISO 7001 |
| JIS Z 8210 | Japanese public-info standard | adapts ISO 7001 with Japan-specific signs |

For wayfinding in public spaces, **start from the standard** — don't reinvent established pictograms.

### ISO 7010 Color Code

The "if it's safety, it's color-coded" rule:

| Color | Meaning | Shape |
|-------|---------|-------|
| Red | Prohibition / fire | Circle with diagonal bar |
| Yellow + black | Warning / hazard | Triangle |
| Blue | Mandatory action | Circle |
| Green | Emergency / safety equipment | Square |
| Red + white | Fire-fighting equipment | Square |

These pairings are mandatory for safety pictograms — using red for "mandatory" violates the standard and creates real-world hazard.

### ISO 9186 Comprehension Test

Pictograms must reach a comprehension benchmark before deployment:

| Tier | Comprehension % | Status |
|------|----------------|--------|
| ISO 9186 acceptance | ≥ 67% (correctly understood without label) | acceptable |
| Strong | ≥ 85% | excellent |
| Marginal | 50-67% | needs label / re-design |
| Failing | < 50% | not deployable |

Test method:

1. 50+ participants across 3+ language / cultural groups.
2. Show pictogram in isolation.
3. Open-ended response: "what does this mean?"
4. Code responses against intended meaning.
5. Calculate comprehension rate.

### Cross-Cultural Considerations

| Pitfall | Example |
|---------|---------|
| Hand gestures vary | Thumbs-up offensive in some Middle East contexts |
| Animals carry meanings | Dog (Western pet) vs (Middle East unclean), pig (kosher / halal-prohibited) |
| Religious symbols | Cross / star / crescent specific to regions |
| Body postures | Praying gesture varies (Buddhism, Christianity, Islam) |
| Eating utensils | Fork (West), chopsticks (East Asia), hands (South Asia / Middle East) |
| Color symbolism | White = purity (West) / mourning (East Asia); red = celebration (China) / danger (West) |

When in doubt, lean on internationally tested standards. Custom pictograms for global audiences require multi-region testing.

### Visual Construction Rules

| Rule | Reason |
|------|--------|
| Solid silhouette over outline | Reads at distance; outlines disappear |
| One concept per pictogram | Multi-concept = ambiguous |
| Bold strokes (≥ 8% of viewbox at smallest delivery size) | Visible at 5+ m |
| Minimum size: smallest dimension ≥ 16 px UI / 50 mm physical signage | Distance-readable |
| Center-balanced composition | Eye lock |
| High-contrast (≥ 4.5:1 background) | WCAG and ISO requirement |
| No gradients | Flat fills only; gradients fail in print |
| No drop shadows | Flat-design only |
| Closed shapes | Recognition via outer silhouette |

### Viewing-Distance Scaling

A pictogram for a museum hallway differs from one in a smartphone app:

| Context | Viewing distance | Min height |
|---------|-----------------|-----------|
| Mobile UI | 30 cm | 24 dp |
| Desktop UI | 50 cm | 24 px |
| Wall sign (close) | 1-3 m | 100 mm |
| Wall sign (medium) | 3-10 m | 200 mm |
| Wall sign (far) | 10-50 m | 400-800 mm |
| Highway / runway | 100+ m | 1000 mm+ |

The same pictogram needs grid retargeting for each context — fine details vanish at distance.

### Grid Systems

| Grid | Use |
|------|-----|
| 24×24 | Mobile / web icons (UI overlap) |
| 32×32 / 48×48 | Print signage at small scale |
| ISO 7001 grid (typical 100×100) | Public-info signs; conforms to standard |
| Brand grid (per design system) | Branded pictograms |

Grid choice affects detail budget; smaller grid = simpler shapes.

### Modular Construction

Many pictograms decompose into reusable parts: head, torso, limbs, accessory. A pictogram set built modularly:

1. Defines a base "person" silhouette.
2. Replaces components for variation (sitting, walking, accessible chair).
3. Maintains visual coherence across the set.

This is how AIGA Symbol Signs achieves consistency across 50 transit pictograms.

### Brand Pictograms

For products / services with a distinctive aesthetic:

| Decision | Recommended |
|----------|------------|
| Stroke vs solid | Solid for safety / wayfinding; brand-consistent for marketing |
| Style coherence with logo | Yes — match curvature / weight / negative space |
| Color | Brand palette + ISO color override for safety contexts |
| Set size | 8-30 typically; > 30 fragments brand |
| Naming | Per concept, not per visual variant |

Brand pictograms still benefit from comprehension testing if they convey safety / info.

### Accessibility Pictograms

Disability + accessibility iconography requires special care:

| Pictogram | Convention |
|-----------|------------|
| Wheelchair user (modern) | Accessible Icon Project's dynamic version (2009) over the static ISO version (2026 update direction) |
| Hearing impaired | T-coil / hearing-loop sign |
| Visual impaired | White cane silhouette |
| Service animal | Always specify guide-dog, not generic "dog" |
| Universal access | All-mobility wheelchair icon + "All access" text |

Choice matters: the modern "Accessible Icon" depicts agency and motion; the older static seated figure has been criticized as passive.

### Verification Process

1. Sketch in pencil on paper at signage scale.
2. Build at standard grid (100×100 or 24×24).
3. Test at 4 distances (close, medium, far, screen).
4. Test at 2 luminance levels (bright, low-light).
5. Run comprehension test (50+ participants, 3+ cultures).
6. Iterate failing pictograms.
7. Submit for ISO / WCAG / EN compliance review (for safety-critical use).
8. Document in style guide with usage rules.

## Workflow

1. **Identify use case** — UI / public-info / safety / accessibility / brand.
2. **Map to standard** — ISO 7001 / 7010 / AIGA / ADA / brand-only.
3. **Choose color code** — match safety standard if applicable.
4. **Pick grid** — UI 24×24 or signage 100×100.
5. **Sketch silhouette** — solid, single concept, bold strokes.
6. **Design at grid** — viewBox + path.
7. **Test at viewing distance** — 4 distances minimum.
8. **Cross-cultural review** — flag hand gestures / animals / religious symbols.
9. **Comprehension test (ISO 9186)** — 50+ participants, ≥ 67% target.
10. **Iterate failing pictograms**.
11. **Document usage rules** — color, size, clear-space, do / don't.
12. **Hand off** — to `system` for icon-system inclusion or to print vendor.

## Output Template

```yaml
pictogram_design:
  use_case: wayfinding_museum
  standards:
    primary: iso_7001
    safety: iso_7010
    accessibility: ada_section_508
  color_code:
    info: blue + white
    emergency: green + white
    fire: red + white
    warning: yellow + black + black_triangle
  grid: 100x100
  pictograms:
    - id: P-01
      concept: "accessible_route"
      style: solid
      stroke_min_pct: 8
      visual_test:
        distance_m: [1, 5, 20, 50]
        passes: yes
        luminance: [bright, low_light]
      cross_cultural_review:
        gestures: none
        animals: none
        religious: none
        passes: yes
      comprehension_iso_9186:
        participants: 60
        cultures: [en_us, ja_jp, zh_cn]
        rate: 92
        status: strong
    - id: P-02
      concept: "no_food_or_drink"
      style: solid
      color_iso7010: red_circle_with_bar
      grid: 100x100
      comprehension_rate: 88
  brand_consistency:
    matches_design_system: yes
    set_size: 18
  delivery:
    sizes: [24px, 48px, 200mm, 400mm]
    formats: [svg, eps, png_at_3_dpi_levels]
  documentation:
    usage_rules: yes
    do_dont_examples: 5
    clear_space_rule: 0.5_x_pictogram_width
```

## Anti-Patterns

- UI icons used as wayfinding pictograms — too thin / detailed for distance.
- Outline-only pictograms in public signage — disappears at distance.
- Custom safety colors — violates ISO 7010; legal / liability risk.
- Multi-concept pictogram ("no food and no phone") — ambiguous.
- Cultural symbol used without testing — alienates target audience.
- Comprehension < 67% deployed without label — wayfinding fails.
- Animal / hand-gesture pictogram for global audience without cross-cultural review.
- Gradient or drop-shadow on pictogram — fails in print and at distance.
- Tiny detail (eye, finger, etc.) at sign-readable distance — disappears.
- Re-inventing ISO 7001 pictogram (toilet, exit) — confuses; use standard.
- Color-only differentiation — fails for color-blind users; violates WCAG 1.4.1.
- Pictogram without grid system — inconsistent across set.
- Mixing standard pictograms with custom in same signage — visual incoherence.
- No comprehension test before deployment — discovery-by-failure in field.
- Brand pictograms applied to safety contexts — overrides ISO 7010 color code.
- Dynamic Accessible Icon used in regulatory-required signage where static ISO version is mandated — compliance risk.
- Pictograms designed at 24 px and scaled up to 200 mm — bake-in fine detail that vanishes.

## Deliverable Contract

A pictogram package is complete when:

- Standard chosen (ISO 7001 / 7010 / AIGA / ADA / brand).
- Color code matches standard for safety-critical pictograms.
- Grid established (UI 24×24 or signage 100×100).
- Each pictogram tested at 4 viewing distances.
- Cross-cultural review done.
- Comprehension test (ISO 9186) ≥ 67% per pictogram.
- Brand-consistency check passes.
- Deliverables in multiple sizes / formats.
- Usage rules documented (clear space, color, size minimum, do/don't).

## References

- ISO 7001:2023 — Graphical symbols — Public information symbols (latest revision 2023; supersedes 2007 edition).
- ISO 7010:2019/Amd 6:2024 — Graphical symbols — Safety colours and safety signs (registered signs base, periodically amended).
- ISO 9186-1:2014, ISO 9186-2:2008, ISO 9186-3:2014 — Pictogram comprehension and legibility testing methodology.
- ISO 22727 — Pictogram development principles.
- AIGA / DOT Symbol Signs (1974) — public-domain transit pictograms.
- Henry Dreyfuss, *Symbol Sourcebook* (1972) — foundational reference.
- Sara Hendren et al., *The Accessible Icon Project* (2009) — modern accessibility icon.
- Otl Aicher, Munich 1972 Olympics pictograms — modern grid system.
- ANSI Z535 — US safety-sign standard.
- JIS Z 8210 — Japanese public-information standard.
- Society for Experiential Graphic Design (SEGD) — wayfinding-design standards.
- Don Norman, *The Design of Everyday Things* — affordance and signifier theory.
- Edward Tufte, *Envisioning Information* — visual-encoding principles.
- W3C WCAG 2.2 (W3C Recommendation 2023-10-05) — SC 1.4.1 use of color, 1.4.3 contrast, 1.4.11 non-text contrast, 2.5.8 target size.
- ADA Standards for Accessible Design (2010) — pictogram requirements for public accommodations.
- Architectural Graphic Standards — physical signage scale and placement.
