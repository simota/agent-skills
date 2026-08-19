# Proportion & Spacing — Sourced Reference

Shared cross-skill reference. Web-collected knowledge on ratios, spacing scales, grids, vertical
rhythm, and the craft heuristics that govern margin/padding/space/layout quality. Every
substantive claim carries a source. Claims that circulate widely but could not be traced to a
primary source are labeled `UNVERIFIED (folklore)` — **do not upgrade them to fact when citing
this file.**

**Consumers:** `muse` (spacing/type/grid token values) · `vision` (direction justification,
composition) · `palette` (touch targets, measure, proximity grouping) · `nexus restyle` /
`runway` / `marquee` (rubric axis numbers) · `nexus crucible` (Tier-1/2 numbers as **pass
criteria** for condition cells — reflow, target size) · `nexus chorus` (Idiom-Gate citations
against Apple HIG / Material 3) · `nexus lattice` (defensible values when a system `gap` is
filled) · `nexus silhouette` (§1 tiers bound what may justify a distinctive move — Tier 4
folklore may not) · `funnel` / `funnel[premium]` (LP layout) · `native`
(platform margin conventions) · `forge` / `artisan` / `pixel` (implementation defaults) ·
`canvas` (diagram element counts — §6 "Cognitive-capacity numbers").

Read this when deciding spacing scales, container widths, type scales, or when justifying a
layout decision to a reviewer.

---

## 1. Evidence tiers — read this first

Layout knowledge is a mix of three very different things. Conflating them is the most common
authoring error in design docs.

| Tier | Meaning | Examples in this file |
|------|---------|----------------------|
| **Spec / legal** | Normative, testable, citable | WCAG 1.4.8 / 1.4.12 / 2.5.5 / 2.5.8, ISO 216, CSS specs |
| **Published system** | A vendor's actual shipped numbers | Material 3, Apple HIG, Tailwind, Carbon, Radix, Bootstrap |
| **Craft convention** | Practitioner consensus, works, unproven | 8pt grid "feels right", 2:1 button padding, optical center 1/8 up |
| **Contested / folklore** | Repeated as fact, evidence weak or against | Golden ratio as beauty law, Z-pattern, "Lin 2004" |

**Rule:** cite Tier 1-2 as requirements. Cite Tier 3 as convention with a reason. Never cite
Tier 4 as justification — use it only as a tiebreaker between otherwise equal options.

---

## 2. Ratio systems — what actually holds up

### Golden ratio (φ ≈ 1.6180339887)

Definition `a/b = (a+b)/a`; Euclid's "extreme and mean ratio", romanticized by Pacioli's
*Divina Proportione* (1509). Applied in UI as 1:1.618 rectangles, ~38.2%/61.8% sidebar splits,
and as one modular-scale multiplier.

**The debunking is stronger than the claim:**

- Markowsky, *Misconceptions about the Golden Ratio*, College Math Journal 23 (1992) — the
  canonical paper. Parthenon / Great Pyramid / human-anatomy claims fail because measurement
  points are chosen *after* the fact to produce ~1.618.
  <https://www.goldennumber.net/wp-content/uploads/George-Golden-Ratio-Misconceptions-MAA.pdf>
- Keith Devlin (Stanford): φ is irrational, so nothing physical can *be* φ — only approximate
  it; claims of deliberate Greek use are "without any evidence."
  <https://www.fastcompany.com/3044877/the-golden-ratio-designs-biggest-myth>

**Counter-evidence exists and is unresolved.** Fechner (1876) showed ~10 rectangles to several
hundred subjects; ~76% preferred the three nearest φ. Reanalyses (Livio and others) find φ as
the *mean/median* response but not reliably the *mode*. Roughly balanced support-vs-null results
across ~150 years, with large individual/cultural variance — which by itself refutes claims of
universality. <https://pmc.ncbi.nlm.nih.gov/articles/PMC9787369/>

**Verdict for practice:** treat φ as *one workable modular-scale ratio among several*
(1.2-1.618 all work if applied consistently), not as a law of beauty. Its real value —
like every ratio system — is **coordination**: predictable relationships across many outputs.

### Ratios worth knowing, with their actual reason to exist

| Ratio | Value | Why it exists |
|-------|-------|---------------|
| **√2 (ISO 216 / A-series)** | 1.41421 | Self-similar: halving the long side preserves the aspect ratio. Lichtenberg 1786 → DIN 476 (1922) → ISO 216. A0 = 1 m²; A4 = 210×297 → 1.4143. The *only* ratio in this table with a mathematical justification for its use. <https://en.wikipedia.org/wiki/ISO_216> |
| **Rule of thirds** | 33.3% / 66.6% | J. T. Smith, *Remarks on Rural Scenery* (1797) — from Reynolds' light/dark balance discourses, **not** derived from φ. Dominant only after 1970s-80s viewfinder grids. Note it is *not* the "phi grid" (38.2%/61.8%). |
| **3:2** | 1.5 | 35mm film → DSLR/mirrorless sensors, print photography |
| **4:3** | 1.333 | Academy ratio (1920s 35mm stock) → CRT → still good for documents, video calls, reading panes |
| **16:9** | 1.778 | HDTV/streaming standard since the 2000s HD transition |
| **21:9** | 2.33 | Ultrawide monitors/gaming. Consumer 21:9 TVs (2010-2017) failed commercially — pillarboxing on 16:9 content |

### Modular scale ratios (musical-interval naming)

Multiply a base size geometrically. Names are borrowed from musical frequency ratios.

| Name | Ratio | Use |
|------|-------|-----|
| Minor second | 1.067 | Very dense UI, near-invisible steps |
| Major second | 1.125 | Dense product UI |
| Minor third | 1.200 | Product UI default |
| Major third | 1.250 | Balanced app/marketing |
| Perfect fourth | 1.333 | Editorial, clear hierarchy |
| Perfect fifth | 1.500 | Marketing, dramatic |
| Golden | 1.618 | Editorial/hero, very dramatic |

Tight ratios (1.067-1.2) → dense UI and mobile. Wide ratios (1.333-1.618) → editorial/marketing
needing dramatic hierarchy. Golden from 16px: 16 → 25.9 → 41.9 → 67.8.
Fibonacci (1,1,2,3,5,8,13,21…) is used the same way because consecutive ratios converge on φ.
<https://alistapart.com/article/more-meaningful-typography/> · <https://utopia.fyi/blog/css-modular-scales/>

### Canons of page construction (Bringhurst, *Elements of Typographic Style*)

- **Van de Graaf canon** — divides the page diagonal into ninths to place the text block. On a
  2:3 page: inner 1/9, outer 2/9 of width; top 1/9, bottom 2/9 of height → margin ratio
  **inner:top:outer:bottom = 2:3:4:6**. Raúl Rosarivo derived the same ninths construction
  independently. Works for any page proportion, including web.
- **Villard de Honnecourt diagram** — the medieval diagonal construction that is Van de Graaf's
  ancestor.
- **Tschichold's golden canon** — 2:3 page with golden-section-derived margin/text-block
  relationship; Bringhurst's aesthetic high point of the tradition.

`UNVERIFIED`: exact numeric margin fractions for Tschichold's variant come from secondary
summaries only (primary text pp. 141-151 not fetchable) — treat as approximate.
<https://en.wikipedia.org/wiki/Canons_of_page_construction>

---

## 3. Spacing scales — the real numbers

### 8pt vs 4pt: the reason is engineering, not beauty

8 divides cleanly into 1x/1.5x/2x/3x device pixel densities, so 8pt values land on whole
physical pixels at every density (no sub-pixel blur). Common breakpoints
(320/360/768/1024/1280/1440/1920) all divide by 8. `UNVERIFIED (craft folklore)`: the claim that
steps of 2-4 are "too subtle" and 16 "too jumpy" is repeated consistently by practitioners but
has no formal study behind it.

**4pt is a sub-step inside an 8pt system**, not a replacement — used for icon padding, border
spacing, dense tables. Material 3 layers exactly this way: base tokens step in 4dp
(xs 4, s 8, m 12, l 16, xl 28) while 8dp remains the component-layout baseline.
<https://m3.material.io/styles/spacing/tokens>

### Published scales

| System | Base | Scale (px) |
|--------|------|-----------|
| **Material 3** | 4dp | 4, 8, 12, 16, 20, 24, 28 (named xs→xl) |
| **Tailwind** | `--spacing: 0.25rem` (4px) | 0, 1(=4), 2(=8), 3(=12), 4(=16), 5(=20), 6(=24), 8(=32), 10(=40), 12(=48), 16(=64), 20(=80), 24(=96) … to 96 (24rem). Authored in **rem** → respects user zoom |
| **IBM Carbon** | 8px, with 2px mini-unit | 01=2, 02=4, 03=8, 04=12, 05=16, 06=24, 07=32, 08=40, 09=48 … |
| **Radix Themes** | 4px, × `--scaling` var | 1=4, 2=8, 3=12, 4=16, 5=24, 6=32, 7=40, 8=48, 9=64 (9 steps, global density knob) |
| **Shopify Polaris** | 4px | token name = % of base: space-100=4, space-200=8, space-400=16 |
| **Atlassian** | 8px = space.100 | 0-100 (0-8) compact · 150-300 (12-24) medium · 400-1000 (32-80) layout. Has **negative** tokens (space.negative.025…400) for overlap |
| **GitHub Primer** | 8px | spacer-1=4, then +8/step. `PARTIALLY VERIFIED` — old doc, check primer/primitives for current names |
| **Adobe Spectrum** | — | size-/spacing- token family (size-0…size-6000). `UNVERIFIED` — px mapping not extractable, page is JS-rendered |

**Cross-system pattern.** Every major system's base unit is 4px or 8px; token counts cluster at
9-14 steps; and **every shipped scale is linear/arithmetic, not geometric.** Geometric/Fibonacci
spacing scales (8, 16, 24, 40, 64, 104…) appear in editorial/marketing token tutorials but in no
shipped product system found. Linear = predictability for dense UI; geometric = drama for
landing pages. Systems cap near 10-14 steps because adjacent values stop being distinguishable
(`UNVERIFIED` as formal research; practitioner consensus).

### Base-unit disagreement worth flagging

8px is the majority *stated* base (Material, Carbon, Primer, Atlassian), but Tailwind and Radix
effectively use **4px** as the true step unit — their "8" token is 2 base units. Don't assume
"8pt system" means the same thing across two design systems.

### Units and modern CSS

- **rem** for spacing tokens (Tailwind, Radix) — scales with root font-size, i.e. accessibility
  zoom. **px** at the primitive/pixel-snapped layer. **em** avoided (compounds with nested
  font-size). **ch** niche — text measure only.
- **`clamp()` fluid spacing** — `gap: clamp(1rem, 0.5rem + 1.5vw, 2rem)` scales continuously
  instead of jumping at breakpoints (the Utopia methodology). `clamp()` has been baseline since
  ~2020; specific support percentages from practitioner blogs are `UNVERIFIED-precise`.
- **Logical properties** — `padding-inline` / `padding-block` / `margin-inline-start` so tokens
  survive RTL and vertical writing modes (W3C CSS Logical Properties).
- **`gap`** preferred over sibling margins — no first/last-child margin-collapse hacks.
- **Container queries** shift spacing from viewport-relative to *container*-relative (a card's
  padding responding to its own container). Broad support since ~2023; **none of the token
  systems above reflect this yet** — they are all still viewport/global-scale.

### Touch targets — a 2× spread between legal and platform

| Source | Minimum | Note |
|--------|---------|------|
| **WCAG 2.2 SC 2.5.8** (AA) | **24×24 CSS px** | Or: a 24px circle centered on the target must not intersect another target's circle (the spacing escape hatch). Exceptions: inline links, essential sizing, UA-controlled, equivalent alternative. <https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html> |
| **WCAG 2.2 SC 2.5.5** (AAA) | **44×44 CSS px** | No spacing exception <https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html> |
| **Apple HIG** | **44×44 pt** | pt ≠ px; HIG's base layout unit |
| **Material 3** | **48×48 dp** | ≥8dp between targets; ≥16dp between side-by-side buttons |

**Practice:** 24px is the AA floor everywhere; design primary/frequent controls at 44-48 to
match platform convention.

---

## 4. Inner vs outer space — the single highest-leverage rule

**Space *inside* a group ≤ space *between* groups.** This operationalizes Gestalt proximity:
closer elements read as related. Violating it (equal inner/outer padding) is the most reliable
tell of unpolished UI. Practitioner rule of thumb: 16px internal gaps → ~32px (2×) to the next
card.

Canonical treatment: Nathan Curtis, *Space in Design Systems* (EightShapes)
<https://medium.com/eightshapes-llc/space-in-design-systems-188bcbae0d62> ·
NN/g proximity <https://www.nngroup.com/articles/gestalt-proximity/>

Evidence tier: **evidence-backed** (Gestalt psychology + NN/g), though the specific 2× multiplier
is convention.

---

## 5. Typographic proportion

### Measure (line length)

| Source | Range | Note |
|--------|-------|------|
| Bringhurst | **45-75 chars**, ideal **66** | 40-50 for multi-column. Tightest/purist |
| Butterick | 45-90 | "2-3 lowercase alphabets" |
| Dyson & Haselgrove | ~55 cpl | Fast + accurate reading |
| **WCAG 1.4.8** (AAA) | ≤ **80 chars** (40 CJK) | Legal ceiling, *not* a design target. Also: no justified text |

Converged sweet spot **65-75 chars** → ~600-800px prose containers at 16-20px body
(cf. Tailwind Typography's `65ch`). Below ~45 forces re-fixation per line; above ~90 the eye
loses the return sweep.

App-shell/dashboard widths of **1200-1440px** are `UNVERIFIED (folklore)` — ubiquitous (matches
Bootstrap xl/xxl and artboard defaults) but no study fixes them as optimal.

### Line-height / leading

- Butterick: **1.2-1.45** for body, *inversely tied to measure* — longer lines need more leading
  because the return sweep is longer and more error-prone.
  `UNVERIFIED`: no source gives a numeric coefficient for measure→leading.
- Convention: body **1.4-1.6**, display/headings **1.1-1.25**. Larger type needs proportionally
  *less* leading (larger x-height/ascenders already separate lines); tight leading also keeps big
  headlines reading as one block.
- **WCAG 1.4.12 Text Spacing** (AA) — user override must survive: line-height **≥1.5×** font
  size, paragraph spacing **≥2×** font size, letter-spacing **≥0.12em**, word-spacing
  **≥0.16em**. Derived from Wayne Dick's analysis of the McLeish study (gains flatten ~0.20em;
  WG chose 0.12em as a safer floor), validated across ~480 languages.
  <https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html>
- **WCAG 1.4.8** (AAA) — line spacing ≥**1.5×**; paragraph spacing ≥**1.5× the line spacing**.

> **Do not conflate 1.4.8 and 1.4.12.** Their paragraph-spacing metrics differ
> (1.5× line-height vs 2× font-size). They are separate success criteria.

### Vertical rhythm / baseline grid

Rhythm = using `line-height` (not font-size) as the repeating unit so block heights are multiples
of a base leading value. Print-derived; entered CSS practice mid-2000s.

**Why strict baseline grids fail on the web** (practitioner consensus, not measured): browser
line-boxes add asymmetric half-leading whose size varies per typeface; text reflows at arbitrary
widths and zoom; mixed sizes on one line break simple multiples.

**The emerging fix — `text-box-trim` / `text-box-edge`**: trims half-leading above/below glyphs
so a text box can align to a grid without negative-margin hacks. Chrome/Edge 133 (Feb 2025),
Safari 18.2 (Dec 2024), **no Firefox as of Jan 2026**. Formerly proposed as `leading-trim`.
<https://developer.chrome.com/blog/css-text-box-trim>

### Type scales, published

- **Material 3** — 15 tokens, 5 roles × 3 sizes (px): Display 57/45/36 · Headline 32/28/24 ·
  Title 22/16/14 · Body 16/14/12 · Label 14/12/11. <https://m3.material.io/styles/typography/type-scale-tokens>
- **Apple HIG iOS** (pt): Large Title 34 · Title1 28 · Title2 22 · Title3 20 · Headline 17
  (semibold) · Body 17 · Callout 16 · Subheadline 15 · Footnote 13 · Caption1 12 · Caption2 11.
  Dynamic Type adds xSmall→xxxLarge + AX1-AX5. Apple cites **11pt as practical legible minimum**.
  `PARTIALLY VERIFIED` — HIG pages are JS-rendered; values corroborated via secondary reproductions.
- **Fluid (Utopia)** — define scale at two viewport poles (e.g. 320px / 1500px), generate
  `clamp()` expressions that interpolate; removes breakpoint font-size jumps.
  <https://utopia.fyi/type/calculator/>

### Heading space asymmetry

Headings get **more space above than below**, so a heading attaches visually to the content it
introduces rather than floating between blocks. `UNVERIFIED` as a canonical named rule — no
W3C/Apple/Material source quantifies a ratio; editorial-design consensus. Block whitespace
generally scales with the type's **leading**, not raw font-size, to preserve the rhythm unit.

---

## 6. Grids, breakpoints, containers

### Grid theory

Müller-Brockmann, *Grid Systems in Graphic Design* (1981) formalized columns + rows + margins +
gutters as structure that "enables freedom." Karl Gerstner (*Designing Programmes*) generalized
it to programmatic grids that generate many valid layouts from one rule-set.

**Why 12 columns:** 12 is divisible by 2, 3, 4, 6 → halves/thirds/quarters/sixths with no
fractional columns. 4/8-column variants serve compact/tablet breakpoints.

### Published breakpoint/container numbers

**Material 3** window size classes: Compact 0-599dp · Medium 600-839 · Expanded 840-1199 ·
Large 1200-1599 · Extra-large 1600+ (heights 0-479 / 480-899 / 900+).
<https://m3.material.io/foundations/layout/breakpoints/overview>
Columns 4 (compact) / 8 (medium) / 12 (expanded+). Body margins 16dp compact → 24dp medium →
~32dp expanded, scaling much larger on very wide canvases; gutters commonly 24dp at ≥600dp.
`CORROBORATED, NOT PRIMARY-VERIFIED` — the applying-layout page did not return full body text.

**Apple HIG** — trait-based, **no published px breakpoint table**: regular/compact size classes
per dimension, plus layout guides `safeAreaLayoutGuide` (excludes bars, Dynamic Island, camera
housing), `layoutMarginsGuide`, `readableContentGuide` (constrains measure). Standard content
margins 16-20pt from screen edges; 8/16/24pt increments.
> Do not force Apple into a px-table format alongside Material/Bootstrap — that misrepresents the model.

**Bootstrap 5** — breakpoints xs 0 / sm 576 / md 768 / lg 992 / xl 1200 / xxl 1400.
Container max-widths 540 / 720 / 960 / 1140 / 1320 — **intentionally narrower than the
breakpoint**, gutter room baked in.

**Tailwind** — sm 640 / md 768 / lg 1024 / xl 1280 / 2xl 1536 (rem-based).
`container` snaps to the breakpoint's **own min-width** and has no built-in centering/padding.
> Bootstrap and Tailwind containers are **not equivalent systems**. Bootstrap narrows; Tailwind matches.

**Android/Material default margins:** 16dp screen edge (8/24 alternates, avoid <16dp);
72dp margin for icon/avatar-associated content; card inner padding 8dp with ≥12dp to card edge.

### Whitespace — what research actually says

Terminology **macro** (margins, gutters, section gaps) vs **micro** (line/letter spacing) is
standard in UX writing but untraceable to one originating source — `folklore-standard terminology`
for a real effect.

Verifiable findings:

- **Chaparro, Shaikh & Baker** — enhanced layout (headers/indentation/figure placement) did not
  change reading speed or comprehension, but raised satisfaction and lowered fatigue.
- **Chaparro et al.** (white-space layouts) — margins affected both reading speed *and*
  comprehension vs a no-margin control; leading affected preference but not performance.
- **Chaparro & Bernard** — *moderate* whitespace preferred over low or high; no task-performance
  difference.
- **"Lin 2004"** — could not be located. `UNVERIFIED` — cite Chaparro instead.

<https://portfolio.erau.edu/en/publications/reading-online-text-a-comparison-of-four-white-space-layouts/>

### Gestalt → layout

**Proximity** (grid gutters and whitespace *are* the grouping mechanism) · **Similarity**
(shared size/color/shape = shared function; repeating cards/lists) · **Common region** (a shared
boundary/background groups contents regardless of proximity — the formal justification for cards;
note this is a *later addition*, not from the original 1920s Gestalt set) · **Closure** (mind
completes shapes; more relevant to icons than grids).
<https://ixdf.org/literature/topics/gestalt-principles>

### Scan patterns — unequal evidence

- **F-pattern** — NN/g eyetracking, 232 users (2006), revisited 2017. NN/g **itself** says it is
  not universal: variants include E, single-stripe/inverted-L, plus separately catalogued
  **spotted**, **layer-cake** (fixations on headings), **commitment** (thorough reading),
  **lawn-mower** (row-by-row comparison), **zigzag**. F applies to text-heavy, *un-optimized*
  pages — strong visual hierarchy deliberately breaks it. NN/g explicitly **recommends against**
  alternating image/text zigzag layouts (less efficient scanning).
  <https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/>
- **Z-pattern** — `UNVERIFIED (folklore)`. Widely cited for sparse hero/landing layouts, but no
  NN/g eyetracking study found; design-blog convention.
> Never present F and Z with equal authority.

**Optical vs geometric center** — optical center sits above true center, commonly cited at ~12.5%
(1/8) of height upward and slightly right. Consistent secondary agreement, no controlled study →
`design-practice convention, not an experimental constant`. Practical use: hero headlines/images
slightly above dead center to read as centered.

**Rule of thirds in hero sections** — `UNVERIFIED (folklore)` for web UX specifically;
well-established in visual-art composition, imported without dedicated web research.

### Cognitive-capacity numbers — misapplied research

Two findings are routinely promoted from "research about X" to "UI limit on Y". Both promotions
are invalid, and both circulate inside this repo. Cite this subsection instead of the bare number.

**"7±2 items" — does not bound on-screen item counts.**
Miller measured *immediate memory span* — how many chunks a person can hold and reproduce from
memory — and explicitly treated the recurrence of the number as a coincidence worth suspecting,
not a design constant. Cowan's reconsideration puts the pure-capacity estimate nearer **4**, which
is *lower* than 7±2 and still says nothing about menus. The mismatch is the task type: a visible
menu, nav bar, or diagram is a **recognition** task with every option on screen, so nothing has to
be retained. Retention capacity does not cap what may be displayed.

- Miller, G. A. (1956). *The magical number seven, plus or minus two.* Psychological Review 63(2), 81-97.
- Cowan, N. (2001). *The magical number 4 in short-term memory.* Behavioral and Brain Sciences 24(1), 87-114.

> **Rule:** never justify an item-count cap by citing 7±2, Miller, or Cowan. What actually drives
> the cost is scanning effort, label distinctiveness, grouping, information scent, and whether
> search is available. A count cap may still be a reasonable **craft default** (Tier 3) — state it
> as one, with its own reason, and never attribute it to the memory literature.

**Fitts's Law — ranks alternatives, does not emit a pixel minimum.**
Fitts's Law models movement time as a function of *distance to* and *width of* a target
(`MT = a + b·log₂(2D/W)`). It is comparative: it tells you a bigger or nearer target is faster,
and by roughly how much. It contains no absolute constant, so it cannot produce "44×44px". The
44pt and 48dp figures are **Apple HIG and Material vendor numbers (Tier 2)**; WCAG 2.5.8's 24×24
is **Tier 1**. Writing "Fitts's Law: 44×44px" launders a vendor default into a law and makes the
number unfalsifiable in review.

- Fitts, P. M. (1954). *The information capacity of the human motor system…* J. Experimental Psychology 47(6), 381-391.
- MacKenzie, I. S. (1992). *Fitts' law as a research and design tool in HCI.* Human-Computer Interaction 7(1), 91-139.

> **Rule:** cite the platform (Apple/Material) or the spec (WCAG) for any absolute size, and cite
> Fitts only for a *relative* claim — that enlarging a target or moving it closer to the pointer's
> resting position reduces acquisition time, or that adjacent-target spacing trades off against
> mis-tap rate. See §3 "Touch targets" for the numbers themselves.

**The general failure both share.** A study establishes a relationship under stated conditions; a
guideline needs a number. Substituting the study's incidental constant for the missing number
gives the guideline borrowed authority it did not earn. When you catch yourself attaching a
researcher's name to a fixed dimension, screen count, or item count, the citation is almost
certainly doing that.

### Density modes

Material comfortable/compact, Carbon and Spectrum size tokens — these change **component padding
and row height**, keyed off the same spacing scale. They do **not** change column/gutter/margin
structure. Density is a component concern, not a grid concern.

---

## 7. Craft heuristics that separate polished from amateur

### Refactoring UI (Wathan & Schoger)

1. **Start with too much whitespace, then remove** — never add padding to a cramped layout after
   the fact.
2. **No two scale steps within ~25% of each other** (they suggest ~1.618) — applied to both type
   size and spacing. This is the concrete cure for "too many spacing values."
3. **"Most interface problems are hierarchy problems."** Fix by *de-emphasizing* secondary
   elements, not amplifying the primary one.
4. Hierarchy from **weight/color/letter-spacing**, not font-size alone.

Tier: craft consensus (practitioner book, near-universally cited). <https://refactoringui.com>

### Erik Kennedy, *7 Rules for Creating Gorgeous UI*

- **"Double your whitespace"** — default HTML/mockup spacing reads amateur because everything is
  smashed toward the top; generous breathing room (~2× the text's own height in his example) is
  what reads as designed.
- **Design in grayscale first** — color is often used to fake polish that spacing and hierarchy
  should actually deliver. Corollary: prefer whitespace + contrast over bordered boxes and
  low-contrast dividers.

`UNVERIFIED`: the specific phrase "gray on gray" could not be attributed verbatim to Kennedy —
the underlying idea is well attested. <https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html>

### Optical corrections

- **Icon/text alignment** — calibrate icon internal padding to the font's cap-height/line-height.
  Naive bounding-box centering looks wrong because circles, triangles, and squares have different
  optical mass.
- **Button padding asymmetry** — horizontal > vertical (conventionally ~2:1, e.g. 8/16). Some
  systems center on cap-height rather than the raw box. `UNVERIFIED (craft folklore)` for the 2:1
  figure specifically — widely practiced, no canonical source.
- **Hanging punctuation / optical margin alignment** — pull quotes, hyphens, and low-mass
  punctuation slightly past the flush edge so *letterforms* align, not character boxes. Standard
  in print (InDesign "Optical Margin Alignment"); CSS `hanging-punctuation` exists (CSS Text L3)
  but is **Safari-only since 2016** — real implementations fake it with negative text-indent.
- **Uppercase/small-caps tracking** — add ~5-12% letter-spacing to all-caps runs (caps are
  metric-fitted to sit beside lowercase). 0.05-0.1em for short acronyms, 0.2-0.25em for full
  uppercase headings; smaller relative size needs more tracking.
  <https://css-tricks.com/keeping-track-letter-spacing-guidelines/>
- **Round vs square optical weight** — real effect, `not independently sourced in this pass`.

### Failure modes checklist

- Uniform spacing everywhere → no hierarchy
- Ad-hoc spacing values instead of a scale (cure: the ~25%-step rule)
- **Equal inner and outer padding** → violates proximity; the #1 tell
- Over-wide text columns (>90ch)
- Cramped touch targets (<24px)
- Inconsistent optical alignment across an icon set
- **Borders/dividers as a crutch** for spacing + contrast that were never fixed

---

## 8. What can be automated, and what cannot

**Machine-checkable:**
- Raw spacing values vs token scale — e.g. `stylelint-plugin-rhythmguard` flags `p-[13px]` /
  `padding:16px` instead of `var(--spacing-4)`, and can autofix by snapping to the nearest token.
- Touch-target size (24×24 / 44×44 per WCAG)
- Color contrast ratios
- Cumulative Layout Shift (a Core Web Vital — about *stability*, not aesthetic spacing)

**Not machine-checkable** — needs human or heuristic review:
- Whether inner < outer spacing actually *reads* as a coherent group
- Optical alignment quality
- Whether whitespace "feels" generous rather than merely large

---

## 9. Decision defaults (when you have no other constraint)

| Decision | Default | Why |
|----------|---------|-----|
| Spacing base unit | **4px step, 8px rhythm** | Pixel-snapping at all densities; matches every major system |
| Spacing scale shape | **Linear**, 9-14 steps | What every shipped product system actually does |
| Spacing unit | **rem** tokens, px primitives | Survives user zoom |
| Type scale ratio | **1.2-1.25** product UI, **1.333-1.5** editorial | Density vs drama |
| Body line-height | **1.5** | Satisfies WCAG 1.4.12 with no override needed |
| Prose max-width | **65ch** (~600-800px) | Bringhurst's 66 ideal, under WCAG's 80 cap |
| Grid columns | **12** (4 compact / 8 medium) | Divisibility |
| Group spacing | **inner : outer = 1 : 2** | Proximity, made concrete |
| Touch target | **44-48px** primary, **24px** absolute floor | Platform convention over legal minimum |
| Button padding | **vertical : horizontal = 1 : 2** | Convention; adjust optically |
| Fluid spacing/type | **`clamp()`** two-pole (Utopia) | No breakpoint jumps |
| Directional properties | **logical** (`padding-inline`) | RTL / vertical writing modes |

---

## 10. Contradictions to keep visible

1. **Golden ratio**: contested (Markowsky/Devlin) vs Fechner's preference data, unresolved after
   150 years. Never assert it as a beauty law.
2. **Base unit**: "8pt system" means 8px steps in Material/Carbon/Atlassian but 4px steps in
   Tailwind/Radix.
3. **Touch targets**: WCAG AA 24px vs Apple 44pt vs Material 48dp — a 2× spread to reconcile
   per platform.
4. **Measure**: Bringhurst 45-75 vs Butterick 45-90 vs WCAG's 80 ceiling. The last is compliance,
   not a target.
5. **WCAG 1.4.8 vs 1.4.12**: different paragraph-spacing metrics. Do not merge.
6. **Containers**: Bootstrap narrows below the breakpoint; Tailwind matches it exactly.
7. **Apple vs Material model**: trait-based size classes vs numeric breakpoints — not
   interconvertible.
8. **F-pattern vs Z-pattern**: rigorous-but-caveated vs unsourced.
9. **Scale shape**: geometric scales are recommended in token tutorials but absent from every
   shipped product system audited.
10. **Sub-4px tokens**: Carbon ships a 2px mini-unit; most systems treat anything finer than 4px
    as a border-width concern.
11. **7±2 as an item cap**: Miller measured recall span, Cowan revised it *down* to ~4, and
    neither studied on-screen options. Item-count caps are craft defaults, never memory findings.
12. **Fitts's Law vs 44/48px**: the law is comparative and yields no absolute size. The pixel
    minimums are Apple/Material (Tier 2) and WCAG (Tier 1). Do not attribute them to Fitts.

---

## Source index

**Specs / standards**
- WCAG 2.2 SC 2.5.8 Target Size (Minimum) — <https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html>
- WCAG 2.2 SC 2.5.5 Target Size (Enhanced) — <https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html>
- WCAG 1.4.12 Text Spacing — <https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html>
- WCAG 1.4.8 Visual Presentation — <https://www.w3.org/WAI/WCAG21/Understanding/visual-presentation.html>
- WCAG 2.0 Technique C21 (line spacing in CSS) — <https://www.w3.org/TR/WCAG20-TECHS/C21.html>
- ISO 216 — <https://en.wikipedia.org/wiki/ISO_216> · <https://www.cl.cam.ac.uk/~mgk25/iso-paper.html>
- MDN `text-box-trim` — <https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-box-trim>
- MDN `hanging-punctuation` — <https://developer.mozilla.org/en-US/docs/Web/CSS/hanging-punctuation>
- Chrome — CSS text-box-trim — <https://developer.chrome.com/blog/css-text-box-trim>

**Design systems**
- Material 3 spacing tokens — <https://m3.material.io/styles/spacing/tokens>
- Material 3 grids & spacing — <https://m3.material.io/foundations/layout/understanding-layout/spacing>
- Material 3 breakpoints — <https://m3.material.io/foundations/layout/breakpoints/overview>
- Material 3 type scale tokens — <https://m3.material.io/styles/typography/type-scale-tokens>
- Material 2 spacing methods — <https://m2.material.io/design/layout/spacing-methods.html>
- Android canonical layouts — <https://developer.android.com/develop/ui/views/layout/canonical-layouts>
- Apple HIG — <https://developer.apple.com/design/human-interface-guidelines>
- Apple HIG Layout — <https://developer.apple.com/design/human-interface-guidelines/foundations/layout/>
- Tailwind margin/spacing — <https://tailwindcss.com/docs/margin>
- Tailwind responsive design — <https://tailwindcss.com/docs/responsive-design>
- IBM Carbon spacing — <https://carbondesignsystem.com/elements/spacing/overview/>
- Atlassian spacing — <https://atlassian.design/foundations/spacing>
- Radix Themes spacing — <https://www.radix-ui.com/themes/docs/theme/spacing>
- Shopify polaris-tokens — <https://github.com/Shopify/polaris-tokens/blob/main/README.md>
- GitHub Primer spacing — <https://styleguide.github.com/primer/support/spacing/>
- Adobe Spectrum spacing — <https://spectrum.adobe.com/page/spacing/>

**Research / debunking**
- Markowsky, *Misconceptions about the Golden Ratio* (1992) — <https://www.goldennumber.net/wp-content/uploads/George-Golden-Ratio-Misconceptions-MAA.pdf>
- Devlin on the golden ratio myth — <https://www.fastcompany.com/3044877/the-golden-ratio-designs-biggest-myth>
- Golden-ratio aesthetics review (PMC) — <https://pmc.ncbi.nlm.nih.gov/articles/PMC9787369/>
- Chaparro et al., white-space layouts — <https://portfolio.erau.edu/en/publications/reading-online-text-a-comparison-of-four-white-space-layouts/>
- NN/g F-shaped pattern — <https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/>
- NN/g text scanning patterns — <https://www.nngroup.com/articles/text-scanning-patterns-eyetracking/>
- NN/g zigzag layouts — <https://www.nngroup.com/articles/zigzag-page-layout/>
- NN/g proximity — <https://www.nngroup.com/articles/gestalt-proximity/>
- Baymard, optimal line length — <https://baymard.com/blog/line-length-readability>
- IxDF Gestalt principles — <https://ixdf.org/literature/topics/gestalt-principles>

**Typography / craft**
- Bringhurst via webtypography.net — <http://webtypography.net/2.1.2>
- Butterick, line length — <https://practicaltypography.com/line-length.html>
- Butterick, line spacing — <https://practicaltypography.com/line-spacing.html>
- Canons of page construction — <https://en.wikipedia.org/wiki/Canons_of_page_construction>
- A List Apart, more meaningful typography — <https://alistapart.com/article/more-meaningful-typography/>
- Utopia type calculator — <https://utopia.fyi/type/calculator/>
- Utopia CSS modular scales — <https://utopia.fyi/blog/css-modular-scales/>
- Smashing, fluid type & space scales — <https://www.smashingmagazine.com/2021/04/designing-developing-fluid-type-space-scales/>
- CSS-Tricks letter-spacing guidelines — <https://css-tricks.com/keeping-track-letter-spacing-guidelines/>
- Pimp My Type, all-caps spacing — <https://pimpmytype.com/spacing-all-caps/>
- Google Fonts, hanging punctuation — <https://fonts.google.com/knowledge/using_type/working_with_hanging_punctuation>
- Nathan Curtis, *Space in Design Systems* — <https://medium.com/eightshapes-llc/space-in-design-systems-188bcbae0d62>
- Refactoring UI — <https://refactoringui.com>
- Erik Kennedy, 7 Rules for Gorgeous UI — <https://www.learnui.design/blog/7-rules-for-creating-gorgeous-ui-part-1.html>
- Optical effects in user interfaces — <https://medium.com/design-bridges/optical-effects-in-user-interfaces-for-true-nerds-9fca82b4cd9a>
- Button size styles — <https://blog.damato.design/posts/button-size-styles/>
- Müller-Brockmann, *Grid Systems in Graphic Design* — <https://archive.org/details/GridSystemsInGraphicDesignJosefMullerBrockmann>
- 8-Point Grid (spec.fm) — <https://spec.fm/specifics/8-pt-grid>
- stylelint-plugin-rhythmguard — <https://github.com/PetriLahdelma/stylelint-plugin-rhythmguard>
