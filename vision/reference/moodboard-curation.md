# Moodboard Curation

Reference for Vision's `moodboard` recipe. Curate visual moodboards in ENVISION phase, narrow 9 candidates → 3 finalists, define directional axes with anti-keywords.

---

## 1. Purpose of a Moodboard

A moodboard is a **decision instrument**, not decoration. Use it to:

- Force divergence before convergence
- Make competing directions visible side-by-side
- Anchor brand voice in observable references
- Surface stakeholder alignment / disagreement early
- Lock in 3 finalists with rationale before token / wireframe work

**Not** a Pinterest wall. Every reference must justify its inclusion against a directional axis.

---

## 2. Directional Axes

Pick 3-5 axes per moodboard. Each axis is a **bipolar spectrum** with brand-relevant tension.

### Common axes

| Axis | Pole A | Pole B |
|---|---|---|
| Density | Calm / sparse / breathing | Dense / utilitarian / power-user |
| Tone | Editorial / serious | Playful / illustrated |
| Surface | Flat / minimal | Tactile / glassmorphism / depth |
| Era reference | Modernist (Swiss / Bauhaus) | Contemporary (2026 maximal / experimental) |
| Color | Monochromatic / neutral | Vivid / brand-led / chromatic |
| Form language | Geometric / sharp | Organic / soft / bezier |
| Voice | Confident / direct | Friendly / conversational |
| Tech feel | Engineered / precise | Humanist / handcrafted |

Don't use all 8 — pick the 3-5 axes where brand has genuine tension or strategic choice.

---

## 3. Reference Selection

For each axis, source **2-3 references per pole** = ~12-30 raw references.

### Source mix
| Source | Why | Watch for |
|---|---|---|
| Direct competitors | Differentiation reference | Don't copy; identify what to avoid |
| Adjacent industries | Pattern transfer | Avoid forced metaphors |
| Award sites (Awwwards, SiteInspire, Lapa) | Production-grade quality bar | Filter for accessibility |
| Brand systems (Linear, Vercel, Stripe, Figma) | Operational design system reality | Avoid copying their voice |
| Editorial / print | Typography + layout discipline | Translates poorly to interactive |
| Apps you respect | Interaction model reference | Mobile vs desktop translation |

Avoid:
- Dribbble shots (concept art, often non-functional)
- Behance hero pages (unrepresentative of full system)
- AI-generated mockups (no real constraint negotiation)

---

## 4. Reference Annotation

Each reference needs ≥ 3 annotations:

```markdown
### Reference: Linear app — workspace screen
- URL / source: linear.app/screenshots/workspace
- Axis match: Density (sparse pole), Tone (editorial pole)
- What we'd take: restrained palette, tight typography, command-K affordance
- What we'd reject: monochrome only — our brand needs accent color
- WCAG check: text contrast appears > 7:1 ✓
```

Without annotations, references become Rorschach blots — everyone sees what they want.

---

## 5. The 9 → 3 Funnel

### Stage 1: 9 candidates
Combine references into 9 holistic directions, each spanning all axes. Name each:
```
Direction 1: "Editorial Calm" — sparse + editorial + monochromatic
Direction 2: "Confident Power" — dense + serious + brand-vivid
Direction 3: "Soft Workshop" — sparse + playful + organic + neutral
...
Direction 9: ...
```

Each direction = single-image composite + 2-line manifesto.

### Stage 2: filter to 5
Remove directions that:
- Conflict with brand anti-keywords
- Fail accessibility at the concept stage
- Mirror a direct competitor too closely
- Require tech the platform can't deliver
- Can't survive translation across all required surfaces (web + mobile + email)

### Stage 3: narrow to 3 finalists
Each finalist must:
- Differentiate from the other two
- Score ≥ 3 / 5 on brand-fit (see `brand-strategy.md`)
- Have a one-sentence elevator pitch
- Have a "why this beats X / Y" comparison

```markdown
## Finalist: Editorial Calm
- Pitch: "Linear-grade restraint with our brand voice as the only color signal."
- Beats Confident Power: maintains differentiation from competitors A/B who are loud.
- Beats Soft Workshop: matches enterprise audience expectation.
- Risk: may feel cold for marketing surfaces — apply only to product, not marketing.
```

---

## 6. Stakeholder Alignment Pattern

After 3 finalists, run alignment session:
- Present finalists side-by-side (not one at a time)
- Present in same format: 1 hero composite + 1 elevator pitch + 1 "what we trade away" line
- Let stakeholders rank, not score (forces choice)
- Capture dissent in writing
- Name a default winner based on rank distribution; don't average

If alignment fails after 1 round, the issue is brand strategy, not moodboard. Stop and revisit `brand-strategy.md`.

---

## 7. Tone Keywords vs Anti-Keywords

For each finalist, define:
```markdown
## Editorial Calm — keywords
- Restraint
- Editorial
- Confident
- Spacious
- Quiet

## Editorial Calm — anti-keywords
- Loud (no glow / saturated gradients)
- Decorative (no patterns, no textures)
- Casual (no rounded corner > 8px, no emoji in chrome)
- Bouncy (no spring easing on system-level interactions)
- Trendy (no glassmorphism, no hyper-personalization affordances)
```

Anti-keywords are the **most useful artifact** the moodboard produces — they prevent drift during execution.

---

## 8. Output Format (deliverable)

```markdown
# Moodboard — <Project Name>

## Brand context
- Voice keywords: <from brand-strategy>
- Anti-keywords: <from brand-strategy>
- Audience: ____

## Directional axes (3-5)
| Axis | Pole A | Pole B |
|---|---|---|
| ____ | ____ | ____ |
| ____ | ____ | ____ |
| ____ | ____ | ____ |

## Reference library (annotated)
[12-30 references with annotations]

## 9 candidates (composites)
[brief composite per candidate]

## 3 finalists
### Finalist 1: <name>
- Pitch
- Keywords / anti-keywords
- Hero composite
- Trade-offs

### Finalist 2: ...
### Finalist 3: ...

## Recommended winner
<name + 1 paragraph rationale>

## Risks
- ____
- ____

## Next steps
- → Vision direction (UNDERSTAND → ENVISION → SYSTEMATIZE)
- → Muse (token derivation)
- → Loom (Guidelines.md if Figma Make pipeline)
```

---

## 9. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| 50+ references without axes → unfilterable | Force 3-5 axes upfront |
| References without annotations → Rorschach test | ≥3 annotations per reference |
| Direct competitor copies (chasing instead of leading) | Use competitors only for differentiation, not aspiration |
| Dribbble / Behance heroes that don't survive a full system | Source from production design systems |
| Single direction presented as "the answer" | Always narrow to 3 finalists, never 1 |
| Anti-keywords missing → drift during execution | Mandatory; ≥ 5 per finalist |
| Stakeholder scoring instead of ranking → averages to mush | Force ranked choice |
| Moodboard output skipped, jumped to wireframes | ENVISION precedes SYSTEMATIZE; don't skip |
| AI-generated mockups passed off as references | Only use references that exist as real products |
| Brand strategy unclear → moodboard goes in circles | Resolve `brand-strategy.md` first |

---

## 10. Decision Walkthrough Template

```
Project: ____________
Brand voice + anti-keywords loaded: ✓ / ✗ (if ✗ → run `brand` first)

Directional axes (3-5):
  1. ____ : ____ ↔ ____
  2. ____ : ____ ↔ ____
  3. ____ : ____ ↔ ____
  4. ____ : ____ ↔ ____ (optional)
  5. ____ : ____ ↔ ____ (optional)

Reference targets:
  Direct competitors: ___
  Adjacent industries: ___
  Award sites: ___
  Production design systems: ___
  Editorial / print: ___

Total references: ___ (target: 12-30)
Each reference annotated: ✓ / ✗

9 candidates composed: ✓
Filter to 5: ✓ (which dropped + why: ____)
Narrow to 3 finalists:
  1. ____ — pitch: ____
  2. ____ — pitch: ____
  3. ____ — pitch: ____

Each finalist has:
  □ Keywords (≥ 5)
  □ Anti-keywords (≥ 5)
  □ Hero composite
  □ Trade-off statement
  □ "beats X / Y" comparison

Recommended winner: ____
Stakeholder alignment round 1: ✓ / ✗

Next handoff:
  □ Vision direction (continue UNDERSTAND → ENVISION)
  □ Muse (token derivation from finalist palette)
  □ Loom (Guidelines.md draft)
```

---

## 11. References
- IDEO Design Thinking divergence-convergence model
- Brad Frost, Style Tile methodology
- Linear, Vercel, Stripe, Figma — production design system references
- Awwwards / SiteInspire / Lapa — quality bar references
