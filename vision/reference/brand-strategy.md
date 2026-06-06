# Brand Strategy

Reference for Vision's `brand` recipe. Translate brand identity into UI direction: voice keywords, palette structure, typography pairing, multi-brand orchestration, and brand-fit scoring.

---

## 1. Brand Inputs Required

Before drafting any direction, gather:

| Input | Source | Required? |
|---|---|---|
| Brand purpose / mission | Brand book, founder interviews | ✓ |
| Voice & tone keywords (5+) | Brand book, marketing copy samples | ✓ |
| Anti-keywords (what we are NOT) | Repositioning workshop | ✓ |
| Primary logo + variants | Brand asset library | ✓ |
| Existing palette + usage rules | Brand book | ✓ |
| Existing type system | Brand book | ✓ if exists |
| Competitor visual references | Compete agent output | recommended |
| Current UI screenshots (3+ pages) | Live product | ✓ for redesign |
| Customer personas | Researcher / Cast | recommended |

If 3+ inputs are missing, request them before proceeding. Do not invent brand identity.

---

## 2. Voice Keyword Definition

Define 5 keywords + 5 anti-keywords. Force binary contrasts.

### Template
```markdown
## Brand voice

| Keyword (we are) | Anti-keyword (we are NOT) |
|---|---|
| Direct | Verbose |
| Confident | Boastful |
| Warm | Casual |
| Precise | Rigid |
| Playful | Childish |

Tone applies to: UI copy, marketing, error messages, onboarding.
```

Each keyword must map to **observable** UI properties:

| Keyword | UI manifestation |
|---|---|
| Direct | ≤ 6 words per CTA, no "click here", no exclamation marks |
| Confident | Bold sans-serif, no qualifiers ("might", "perhaps") |
| Warm | Rounded corners (8-12px), soft shadows, friendly emoji in non-critical states |
| Precise | Monospaced numerals, exact units, sentence-case labels |
| Playful | Spring-easing on micro-interactions, optional skeleton-screen Easter eggs |

If you can't translate a keyword to UI, it's brand fluff — drop it.

---

## 3. Palette Structure

### Single-brand product
```
Primary brand:    1 hue (anchor — logo color)
Primary tints:    9 steps (50-900 scale)
Neutrals:         9 steps (warm gray or cool gray, not pure)
Semantic:         success / warning / danger / info (4 hues × 9 steps)
Surface:          background / surface / surface-elevated
Accent:           1-2 secondary hues for emphasis
```

Total: ~70-90 raw color tokens, semantic-aliased to ~30-40 tokens.

### Brand-fit rules
- Primary brand color: WCAG 2.2 AA contrast ≥ 4.5:1 against light surface AND dark surface
- If primary fails contrast, use a tint as the interactive accent (not the hex from the logo)
- Pure black (#000) and pure white (#FFF) almost never appear; use neutrals (#0F172A / #F8FAFC)

### Logo color vs UI color
A logo color is a brand asset; a UI accent is an interaction signal. They overlap, not equate. Document explicitly:
```markdown
- Logo: #FF5722 — used in logomark, splash, watermark only
- Interactive accent: #E64A19 — same hue, darker, passes 4.5:1 on white
```

---

## 4. Typography Pair

Choose **2 typefaces max** for product UI:

| Role | Typeface | Weights | Usage |
|---|---|---|---|
| Display | Variable sans (e.g., Inter, Geist) | 400, 500, 600, 700 | Headlines, hero, large numerals |
| Body | Same family or system stack | 400, 500 | Paragraphs, labels, UI text |
| (optional) Monospace | JetBrains Mono / system mono | 400 | Code, IDs, exact data |

Avoid:
- Decorative display fonts in product UI (reserve for marketing)
- 3+ families (incoherent)
- Weight 100-300 below 16px (illegible at small size)
- Font superfamilies with mismatched x-heights (visual jitter)

Brand-fit signal: typography choice should evoke 2-3 of the brand voice keywords. "Confident + Direct" → geometric sans (Geist, Inter). "Warm + Playful" → humanist sans (Recoleta, Söhne). "Precise + Editorial" → modern serif + clean sans pair.

---

## 5. Multi-Brand Orchestration

For multi-brand products, use **Core → Brand → Product** cascade:

```
@core/                         (semantic tokens only — never branded values)
  --color-bg-primary
  --color-text-primary
  --color-action-primary
  --space-md
  --radius-md

@brand-A/                      (brand-specific overrides)
  --color-action-primary: #E64A19   # Brand A orange
  --font-display: 'Inter'

@brand-B/                      (brand-specific overrides)
  --color-action-primary: #2563EB   # Brand B blue
  --font-display: 'Söhne'

@product-X/                    (brand inheritance + product exceptions)
  → inherits from @brand-A
  --color-bg-marketing-hero: linear-gradient(...)  (only on marketing pages)
```

Rules:
- Core defines **semantic intent** (what does this token MEAN), never specific colors
- Brand layers override **values** for that semantic token, never add new ones
- Product layers may add **product-specific exceptions** but cannot redefine core semantics
- No flat shared library across brands — that's the "Frankenstein system" anti-pattern

Document the cascade in Guidelines.md.

---

## 6. Brand-Fit Scoring

Score existing UI against brand voice on a 5-axis rubric:

| Axis | Score 1 | Score 5 |
|---|---|---|
| Voice match (copy aligns with keywords) | Generic AI copy | Distinctive, on-brand voice |
| Visual identity (logo + palette + type) | Mishmash, brand inconsistency | Cohesive, recognizable |
| Tone consistency across surfaces | Marketing ≠ product ≠ docs | Unified across all touchpoints |
| Anti-keyword absence | Triggers anti-keywords often | No anti-keyword violations |
| Brand differentiation vs competitors | Indistinguishable | Clearly own visual position |

Average ≤ 2.5 → fundamental brand work needed before redesign. 2.5-3.5 → targeted improvements. ≥ 3.5 → polish only.

---

## 7. Repositioning Triggers

Before any major redesign, check if brand strategy itself is shifting:

- Target audience changed (e.g., SMB → enterprise)
- Market positioning shifted (e.g., budget → premium)
- Product category expanded (single tool → platform)
- Competitor landscape shifted (new dominant aesthetic emerged)
- Customer feedback signals confusion about "who you are"

If any of these triggers fired, brand strategy must precede UI strategy. A redesign on shifting brand foundation produces incoherence.

---

## 8. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| "Brand refresh" without new strategy → cosmetic only | Force purpose / audience / positioning revisit |
| Logo color used as interactive accent (fails contrast) | Use logo as asset, derive accent from logo hue + WCAG check |
| 3+ typefaces — no hierarchy | Cap at 2; lean on weight + size for hierarchy |
| Voice keywords too abstract ("modern", "innovative") | Force concrete, observable keywords |
| Anti-keywords missing | Bias toward what brand IS leaves ambiguity; add 5 NOT-words |
| Multi-brand: shared flat token library | Apply Core → Brand → Product cascade |
| Brand-fit not measured against competitors | Use Compete output; differentiate, don't blend |
| Marketing brand ≠ product brand | One identity, one cascade; allow tone shifts within it |
| Token names tied to brand color (`--color-orange`) | Use semantic names (`--color-action-primary`) — survives rebrands |
| Brand book cited but never grounded in current UI | Audit current screens against book; quantify drift |

---

## 9. Decision Walkthrough Template

```
Brand inputs gathered:
  □ Purpose / mission
  □ Voice keywords (5)
  □ Anti-keywords (5)
  □ Logo + variants
  □ Existing palette + rules
  □ Type system
  □ Competitor refs (Compete output)
  □ Current UI screenshots (3+)
  □ Personas (Researcher / Cast)

Voice keywords:
  1. ____  → UI manifestation: ____
  2. ____  → UI manifestation: ____
  3. ____  → UI manifestation: ____
  4. ____  → UI manifestation: ____
  5. ____  → UI manifestation: ____

Anti-keywords:
  1. ____  2. ____  3. ____  4. ____  5. ____

Palette:
  Primary: ____ (passes 4.5:1 on light: ✓ / ✗, dark: ✓ / ✗)
  Interactive accent (if primary fails): ____
  Logo-only color (if different): ____
  Neutrals: warm / cool / pure

Typography pair:
  Display: ____  weights: ____
  Body: ____  weights: ____
  Mono (if needed): ____

Multi-brand cascade needed: ✓ / ✗
  If ✓: brands = ____, products per brand = ____

Brand-fit score (existing UI):
  Voice: ___ / 5
  Visual: ___ / 5
  Tone consistency: ___ / 5
  Anti-keyword absence: ___ / 5
  Differentiation: ___ / 5
  Avg: ___ / 5  → action: cosmetic / targeted / fundamental

Repositioning triggers fired: ____  → block redesign until brand work done?: ✓ / ✗

Handoff:
  → Muse (token system)
  → Prose (voice & tone in copy)
  → Loom (Guidelines.md brand section)
```

---

## 10. References
- Marty Neumeier, The Brand Gap
- DTCG (Design Tokens Community Group) v2025.10
- Brad Frost, Atomic Design — multi-brand cascade
- Refactoring UI (Adam Wathan & Steve Schoger) — palette generation
- WCAG 2.2 AA contrast requirements
