# Apple Platform Design Trends & Direction

Purpose: Use this file when the task involves design *direction and taste* for Apple platforms (iOS, iPadOS, macOS, watchOS, tvOS, visionOS) — what an app should feel like, not what a component must do.

## Scope + Boundary

This file answers "which direction, and why" for Apple-platform work. It does not restate normative rules — read the right file for the right question:

| Question | Read |
|----------|------|
| "What direction/taste should this Apple app take?" | This file |
| "What are the HIG rules for `.glassEffect()`, tab bars, Dynamic Type sizes?" | `native/reference/ios-hig.md` (normative, per-component) |
| "What are the actual token values (spacing, color, radius)?" | `muse/` |
| "Is this flow usable — tap targets, error recovery, cognitive load?" | `palette/` |
| "What icon style/weight fits this direction?" | `ink/` |

Rule of thumb: if the answer is a rule ("minimum touch target is 44×44pt"), it lives in `ios-hig.md`. If the answer is a judgment call ("should this app use Liquid Glass chrome or stay flat"), it lives here. Vision reads this file during `ENVISION`; it hands the chosen direction to Native for HIG-compliant implementation.

---

## The Liquid Glass Era

### What changed vs. the iOS 7–18 flat era

iOS 7 (2013) introduced flat design: no skeuomorphism, no gradients, no faux-material chrome — Helvetica Neue, thin strokes, solid color fills, deference expressed through *emptiness*. That language held, with incremental refinement (SF Pro replacing Helvetica Neue in 2017, subtle blur in Control Center/Notification Center), through iOS 18.

**Liquid Glass**, introduced at WWDC 2025 (2025-06-09) across iOS 26 / iPadOS 26 / macOS Tahoe 26 / watchOS 26 / tvOS 26 / visionOS 26, is the first system-wide material change since 2013. It is not a return to skeuomorphism — it does not simulate physical objects. It is a **real-time rendered material**: optical refraction, specular highlight, and content-adaptive blur applied to *chrome only* (navigation, controls, floating surfaces), never to content.

### Design intent behind it

| Intent | What it means in practice |
|--------|---------------------------|
| **Depth over flatness** | Chrome now has a z-position — it visibly sits *above* content, refracting what's beneath it, rather than sharing the content's plane |
| **Deference through translucency, not absence** | iOS 7 deferred to content by removing chrome ornamentation. Liquid Glass defers by making chrome context-aware — it changes appearance based on what's under it, so it never fights the content for attention |
| **Hierarchy via depth, not color/size** | Per `native/reference/ios-hig.md` — importance is communicated through translucency and refraction layering, not saturation or scale deltas |
| **One material, six platforms** | The same physical metaphor (glass over content) now spans watch face to spatial window, unifying the visual language Apple had let drift apart (Big Sur's macOS translucency, watchOS's flat circles, visionOS's glass panes were all different materials before 2025) |

### How it reads per platform

| Platform | Reading |
|----------|---------|
| **iOS** | Most complete expression — floating tab bars, Liquid Glass "islands" for search, edge-to-edge content behind translucent nav. Chrome feels like a physical pane of glass hovering over a phone-sized canvas |
| **iPadOS** | Same material, more surface area — sidebars and multi-column layouts mean more glass-over-content edges, raising the "what's under the glass" problem (see Pitfalls below) since iPad content is often denser/whiter |
| **macOS** | Least convincing expression **(reviewer consensus, not Apple messaging)**. Reviewers noted Liquid Glass "was not a Mac-first design" — much of Tahoe's chrome sits over plain white window backgrounds with nothing to refract, and mismatched corner radii between Finder's new floating sidebar and adjacent panes produced a "double bezel" complaint (Six Colors, MacStories, Reddit — 2025-08/09). Treat macOS Liquid Glass adoption as *selective*, not wall-to-wall — see macOS section below |
| **watchOS / tvOS** | Glass applied to a narrower surface (complications, focus chrome) — lower risk since these platforms already had minimal chrome to begin with |
| **visionOS** | Native habitat — visionOS's ornaments and window glass predate the 2025 unification and are the least changed; Liquid Glass elsewhere is visionOS's material exported to flat displays |

### How to use it tastefully vs. how apps get it wrong

**Tasteful use** (aligned with `native/reference/ios-hig.md` §1 "Where to apply"):
- Chrome only: tab bars, nav bars, toolbars, sheets, floating controls — never body content, list rows, or cards
- Let it adapt automatically — standard SwiftUI/AppKit components pick up Liquid Glass on recompile; don't hand-tune opacity per screen
- Use it to signal *layering* (this is chrome, floating above your content), not as a decorative texture
- Pair with real depth: content should be legible and self-sufficient with the glass hidden (Reduce Transparency on) — glass is an enhancement, not a crutch for hierarchy

**How apps get it wrong** (sourced from developer/press criticism, MacRumors 2025-09-17, UX Collective, Setproduct 2026):
- **Over-glassing**: applying `.glassEffect()` to content surfaces (cards, list rows, body text containers) that should stay opaque — concept redesigns of Spotify/Instagram with all-glass panels were called out as "eye candy overload," turning a chrome material into set dressing
- **Contrast failures**: glass over low-contrast or busy backgrounds (photos, colorful wallpapers, complex imagery) can drop text/icon contrast below WCAG 2.2 AA — Apple's own first developer beta shipped this problem and had to raise nav-bar opacity in later builds
- **Glass on scrolling content**: applying translucency to elements that scroll *with* content (rather than floating chrome that stays fixed) breaks the depth metaphor — users lose the "this is a separate layer" cue when the glass moves with the thing it's supposed to be layered over
- **Legibility over photos**: image-heavy surfaces (photo grids, media players) are the highest-risk case — validate every glass-over-photo combination against real content, not placeholder gradients, before shipping
- **Inconsistent adoption**: mixing flat chrome and glass chrome within one app reads as unfinished, not intentional — a documented Tahoe complaint ("some things are flat while others are glass")

**Direction rule**: when advising on Liquid Glass adoption, default to system components (automatic, correct glass behavior) over custom `.glassEffect()` usage. Custom glass is a deliberate craft decision requiring per-surface contrast validation — treat it as an "Ask First" item per `SKILL.md` Boundaries, same tier as brand color changes.

---

## Direction Archetypes for Apple Apps

Six named directions. Each includes: fit, signature moves, typography stance, color stance, motion stance, and failure mode.

### 1. System-Native / Deferential

**When it fits**: utilities, productivity tools, anything where the OS's credibility should transfer to the app (Settings-adjacent tools, system utilities, B2B tools evaluated on trustworthiness).

- **Signature moves**: standard `List`/`Form` components, system tab bars and nav bars untouched, automatic Liquid Glass (no custom chrome), `ContentUnavailableView` for empty states
- **Typography**: SF Pro exclusively, via Dynamic Type text styles (`Font.body`, never fixed point sizes)
- **Color**: semantic colors only (`Color.primary`, `.accentColor`) — app supplies at most one custom accent hue
- **Motion**: system presets only (`.smooth`, `.snappy`, `.bouncy`) — no custom springs
- **Failure mode**: reads as "no design effort" / generic — undifferentiated from every other utility in the App Store; wrong choice for consumer/brand-forward products

### 2. Editorial

**When it fits**: reading apps, news, long-form content, documentation apps — where typographic craft *is* the product.

- **Signature moves**: generous vertical rhythm, pull quotes, asymmetric image/text pairing, New York serif for body reading, large-title treatments that behave like magazine mastheads
- **Typography**: New York for long-form body, SF Pro Display for headlines — deliberate serif/sans pairing, `text-wrap: pretty`-equivalent orphan control
- **Color**: near-monochrome with one editorial accent (often warm — amber, terracotta) used sparingly for section markers, not UI chrome
- **Motion**: minimal — page-turn or cross-fade only, motion should never compete with reading
- **Failure mode**: over-designed chrome fighting the reading experience — editorial direction fails when navigation gets as much visual weight as the content

### 3. Expressive-Brand

**When it fits**: consumer social, entertainment, fitness/wellness with strong brand identity — apps that must feel unmistakably *themselves*, not Apple's.

- **Signature moves**: custom iconography and illustration system (hand off to `Ink`), branded motion signatures (celebration animations, custom transitions), custom color beyond system accent, bespoke empty/onboarding states
- **Typography**: custom or licensed display face for headlines/marketing surfaces; SF Pro retained for body/system-adjacent text (settings, forms) to preserve accessibility and Dynamic Type compliance
- **Color**: full brand palette, gradients, brand-specific dark mode treatment (not just inverted system colors)
- **Motion**: signature spring curves, branded micro-interactions (100-300ms per `reference/design-trends.md` guardrail), celebration moments tied to user goals, not platform goals
- **Failure mode**: fighting the OS on every touch target and gesture — if custom chrome breaks standard swipe/long-press/drag conventions, users' muscle memory from every other iOS app works against the product

### 4. Utility-Dense

**When it fits**: pro tools, data-heavy dashboards, finance/trading apps, anything where information density beats whitespace — iPad/Mac primary, iPhone secondary.

- **Signature moves**: `Table`/`Grid` over `List`, multi-column `NavigationSplitView`, inspector panels (iOS/iPad/Mac 17+), keyboard shortcuts as first-class (not an afterthought), compact but still 44×44pt-compliant controls
- **Typography**: SF Pro Text at smaller Dynamic Type steps (`callout`/`footnote` doing more of the work than `title`), SF Mono for tabular/numeric data
- **Color**: functional — status colors (success/warning/error) carry real meaning, not decoration; monochrome base so status color pops
- **Motion**: near-zero — data-dense UIs should feel instant, not springy; reserve motion for state transitions that need explaining
- **Failure mode**: density without hierarchy — cramming data without a clear primary/secondary read order produces cognitive overload, the opposite of "dense but scannable"

### 5. Spatial

**When it fits**: visionOS-primary apps, or iOS/iPadOS apps with meaningful AR/depth features.

- **Signature moves**: Z-axis layering per `reference/design-trends.md` §Spatial Computing UX (near/mid/far), ornaments instead of embedded toolbars, window-based (not screen-based) information architecture, passthrough-aware backgrounds
- **Typography**: SF Pro at visionOS-scaled sizes — text must be legible at arm's-length-plus viewing distances, larger baseline sizes than mobile
- **Color**: must work against variable real-world passthrough — avoid color-only state signals even more strictly than other platforms
- **Motion**: spatial audio-paired feedback, gaze-hover highlight → pinch-commit (never sustained gaze >2s per `reference/design-trends.md`)
- **Failure mode**: "3D decoration" — adding depth that doesn't communicate hierarchy is the single most-cited visionOS design mistake; start 2D, add depth only where it does information-architecture work

### 6. Calm / Restrained

**When it fits**: health, mental wellness, finance apps targeting anxiety reduction, AI-assistant surfaces where trust is the primary design problem — overlaps with `LINEAR_RESTRAINT` operating mode in `SKILL.md`.

- **Signature moves**: functional minimalism (large type, soft radius, generous spacing per `reference/design-trends.md` Calm UI principles), single primary action per screen, reduced notification/badge noise
- **Typography**: SF Pro Display for large reassuring numbers/headlines, generous line-height throughout
- **Color**: restrained palette, muted accents, avoids urgency-red except for genuine errors
- **Motion**: slow, settling easing — no bounce, no urgency cues; honors Reduce Motion as the default posture, not just a fallback
- **Failure mode**: restraint read as *emptiness* or lack of guidance — calm design still needs a clear next action; "nothing here" states without a path forward feel broken, not peaceful

---

## Awarded-App Pattern Analysis

Verified against Apple's official winner announcements. Only apps/years with a citable source are listed; unverifiable claims are marked `(unverified)`.

### 2025 Apple Design Award winners (announced 2025-06-04, WWDC 2025)

Six app categories: Delight and Fun — **CapWords** (HappyPlan Tech); Innovation — **Play** (Rabbit 3 Times); Interaction — **Taobao** (Zhejiang Taobao Network); Inclusivity — **Speechify** (Speechify); Social Impact — **Watch Duty** (Sherwood Forestry Service). [Source: MacRumors, 2025-06-03](https://www.macrumors.com/2025/06/03/apple-design-award-winners-2025/)

### 2026 Apple Design Award winners (announced 2026-06-02)

Delight and Fun (App) — **grug** (Ocho); Innovation (App) — **NBA: Live Games & Scores**; Interaction (App) — **Moonlitt: Moon Phase Tracker** (Flipping Hues Srls); Social Impact (App) — **Primary: News in Depth** (Wood Metal Rocks LLC); Visuals and Graphics (App) — **Tide Guide: Charts & Tables**. [Source: 9to5Mac, 2026-06-02](https://9to5mac.com/2026/06/02/apple-reveals-apple-design-awards-app-and-game-winners-for-2026/); [Apple Newsroom, 2026-06-02](https://www.apple.com/newsroom/2026/06/apple-reveals-winners-of-the-2026-apple-design-awards/)

### Concrete, observable patterns across winners

- **Single-purpose clarity**: CapWords (camera → flashcard), Watch Duty (wildfire tracking), Tide Guide (tide charts), Moonlitt (moon phase) — every winning app does one thing, and the UI has no competing primary action. This is the strongest, most consistent signal across both years.
- **Data made glanceable, not dense**: Moonlitt and Tide Guide both take numerically dense source data (astronomical/tidal tables) and present a single dominant visual (a moon phase, a tide curve) before any numbers — favors the Calm/Restrained and Editorial archetypes over Utility-Dense even for data-heavy source material.
- **Camera/sensor input as the primary interaction**, not typing: CapWords replaces text entry with camera capture — a recurring 2025-2026 winner pattern of replacing forms with capture-and-interpret flows, consistent with the `reference/design-trends.md` "Intent Canvas" AI-native pattern (accept messy input, deliver structured interpretation).
- **Social-impact utility apps win on trust, not decoration**: Watch Duty and Primary: News in Depth both won for information-critical, low-decoration UI — reinforces that System-Native/Deferential is a legitimate award-caliber direction, not just a "safe default."

`(unverified)`: any claim about specific screen-level visual treatments (exact color values, specific animation curves) beyond what the sourced articles describe — award pages do not publish design specs, only category/app/developer names.

---

## macOS-Specific Design Direction

macOS Tahoe 26 adopted Liquid Glass, but reviewer consensus (Six Colors, MacStories, MacRumors — 2025-08/09) is that the material is **less mature on Mac than on iOS**: "Liquid Glass was not a Mac-first design," and much of Tahoe's chrome sits over plain white content with nothing to refract. Design direction for Mac should treat this as a live constraint, not a solved problem.

### Sidebar-first information architecture

Mac apps default to `NavigationSplitView` (2–3 column) with a persistent sidebar — this is the single biggest structural difference from iPhone's stack/tab navigation. Sidebar-first is not optional polish; on macOS it *is* the primary navigation model (per `native/reference/ios-hig.md` §3 Multi-column). Design the sidebar's content hierarchy before any other screen.

### Window chrome and density

- Mac windows tolerate — and reward — higher information density than iPhone. Toolbar height, corner radius, and padding must stay *consistent* across a window's sidebar/content/inspector regions; Tahoe's own Finder redesign drew criticism for a "double bezel" effect where the floating sidebar's border didn't match the surrounding chrome (Reddit-sourced complaint, reported by multiple outlets, 2025-08/09). Treat mismatched corner radii between adjacent glass panes as a shipped-quality bug, not a style choice.
- Design for resizable windows as the default state, not an edge case — unlike iPhone's fixed viewport, Mac layouts must degrade gracefully from full-screen to a narrow floating window.

### Pointer / hover affordances

Mac is a pointer-first platform: hover states (button highlight on mouse-over, tooltip on dwell, cursor shape changes over draggable/resizable regions) are expected and their absence reads as "ported from iPad," not "native Mac." Every interactive element needs a hover state distinct from its pressed/active state — iOS/iPad touch targets have no equivalent affordance to reuse.

### Menu-bar-as-surface

macOS Tahoe made the system menu bar translucent/glass by default, and reviewers noted menu bar items now "fade into the background... strangely, more invisible" (multiple outlets, 2025-09). Two implications for app design: (1) don't assume the menu bar is a high-contrast, always-legible surface — validate custom menu bar extras against busy desktop backgrounds; (2) the traditional Mac menu bar (File/Edit/View/Window/Help) remains a first-class surface for full command coverage — don't treat it as legacy chrome to minimize, since Mac power users still expect complete menu parity with in-app actions.

### "Mac-assed Mac app" in the Liquid Glass era

The term — coined by Collin Donnell, popularized by Brent Simmons, entered wider use via John Gruber's Daring Fireball (2020-03-20) — describes an app that is unapologetically native: it adopts system controls, integrates with OS features (Services, Spotlight, drag-and-drop, Quick Look), and doesn't import a foreign design language. In the Liquid Glass era this means:

- Let system components pick up Liquid Glass automatically rather than hand-building "glass-look" custom chrome — a hand-rolled approximation will drift from the real material's behavior (context-adaptive refraction) the moment Apple tunes the system material again.
- Adopt Mac-specific conventions that have no iOS equivalent: menu bar completeness, drag-and-drop between apps, Services menu integration, multi-window support (not one modal-heavy window), keyboard-first workflows with full shortcut coverage.
- **Why iPad-app-on-Mac reads wrong**: Catalyst/scaled-iPad ports default to iPhone/iPad interaction assumptions — single-window modality, touch-sized (not pointer-refined) hit targets, sidebar as an optional collapse rather than the primary IA, and no hover states. Even pixel-accurate Liquid Glass rendering can't fix an interaction model built for touch; the tell isn't visual, it's behavioral (no hover feedback, no menu bar depth, single-window-only navigation).

---

## Cross-Platform Coherence

One brand across iOS/macOS/watchOS/etc. without homogenizing into "the same screen stretched to fit."

### Hold constant across platforms

| Element | Why |
|---------|-----|
| **Color** (brand accent + semantic palette) | Recognition — a user moving from iPhone to Mac to Watch should recognize "this is the same app" by color alone before reading any label |
| **Type ramp logic** (which weight/style means what — not exact point sizes) | Headline-vs-body-vs-caption relationships should be legible at a glance across platforms even though point sizes scale per device |
| **Iconography style** (line weight, corner treatment, metaphor language) | Hand off to `Ink` for a shared icon system — mixed icon styles across platforms is one of the fastest ways to break brand coherence |
| **Voice** (microcopy tone, error message style) | Hand off to `Prose` — a terse/formal iPhone app and a chatty Watch app reads as two different products |

### Must adapt per platform

| Element | Why |
|---------|-----|
| **Density** | iPhone: single-column, generous touch targets. iPad/Mac: multi-column, denser, pointer-refined. Watch: glanceable, near-zero density. Forcing one density ratio everywhere fails both ends |
| **Navigation model** | Tab bar (iPhone) vs. sidebar/`NavigationSplitView` (iPad/Mac) vs. Digital Crown + page navigation (Watch) vs. focus engine (tvOS) — these are not stylistic choices, they follow from the input device |
| **Input** | Touch vs. pointer+keyboard vs. Digital Crown vs. remote vs. gaze+pinch — each has different affordance requirements (hover only exists with a pointer; keyboard shortcuts only matter with a keyboard) |
| **Motion budget** | Watch and tvOS need faster, simpler motion (glanceable, distance-viewed); iPhone/iPad can sustain richer transitions; visionOS motion must respect physical comfort constraints (no >2s sustained gaze, ergonomic zones per `reference/design-trends.md`) |

**Direction check**: if a cross-platform design review finds the Mac version is "the iPad version in a resizable window," or the Watch version is "the iPhone version with things removed until it fits" — that's the homogenization failure mode. Each platform's design should look like it was *designed for* that input model, sharing brand DNA rather than sharing layout.

---

## Anti-Trend / Durability Check

Which current moves are likely to date, and how to test durability before committing.

| Move | Durability risk | Why |
|------|-----------------|-----|
| Custom hand-built "glass-look" chrome (not using system materials) | High | Tied to the exact current rendering of Liquid Glass — the moment Apple retunes blur/refraction parameters (as it already did mid-beta in 2025), hand-approximated glass will look dated or simply wrong, while system-component glass updates automatically |
| Heavy reliance on any single OS-era visual signature (skeuomorphism in 2012, flat-extreme minimalism in 2015, neumorphism in 2020) | High | Every prior Apple-adjacent visual trend cycle lasted roughly 5-7 years before a reset; treat any single-material aesthetic as a phase, not a foundation |
| Semantic color + Dynamic Type + system typography | Low | These are accessibility-load-bearing, not aesthetic — they survive redesigns because removing them breaks compliance, not just taste |
| Sidebar-first IA on Mac/iPad | Low | Structural, tied to multi-column screen real estate that isn't going away; predates Liquid Glass and will outlast it |
| Bento grid / oversized typography / neo-brutalism (per `reference/design-trends.md`) | Medium-High | Already flagged Medium/High risk in the general trend file; same caution applies on Apple platforms, arguably more so since they clash with system chrome conventions |

**The "will this survive the next OS redesign?" test**: ask whether the design decision is (a) a direct dependency on the *current* rendering of a system material, or (b) an information-architecture / accessibility decision that happens to look good under the current material. (a) needs a revisit note (`#TODO(agent)`) for the next major OS cycle; (b) generally survives. Apply this test explicitly before locking in any Liquid Glass-dependent visual signature as a brand-defining element.

---

## Direction Decision Table

| Product type | Recommended archetype | Key constraints |
|---------------|------------------------|------------------|
| System utility / B2B tool | System-Native / Deferential | Automatic Liquid Glass only; no custom chrome; semantic color only |
| News / long-form reading | Editorial | New York for body; minimal motion; single accent used sparingly |
| Consumer social / entertainment | Expressive-Brand | Custom iconography (→ `Ink`) and motion signature; SF Pro retained for system-adjacent surfaces (forms, settings) |
| Finance / trading / pro creative tool | Utility-Dense | iPad/Mac primary; `Table`/inspector patterns; near-zero decorative motion |
| visionOS-primary or AR-heavy | Spatial | Z-axis used for hierarchy only; ornaments not embedded toolbars; ergonomic-zone compliance |
| Health / wellness / AI-assistant trust surface | Calm / Restrained | Single primary action per screen; slow easing; explicit next-action even in empty states |
| Cross-platform (iOS+Mac+Watch) brand | Pick ONE primary archetype, adapt density/navigation per platform | See Cross-Platform Coherence — hold color/type-ramp-logic/icon/voice constant |

---

## Handoff Hooks

| Handoff | What Vision passes |
|---------|---------------------|
| **Vision → Native** | Chosen archetype + Liquid Glass adoption scope (automatic-only vs. custom `.glassEffect()` surfaces needing contrast validation) + which platforms are in scope. Native implements against `native/reference/ios-hig.md` normative rules. |
| **Vision → Muse** | Color stance (semantic-only vs. custom accent vs. full brand palette) and typography stance (SF-only vs. SF+custom) per archetype — Muse defines the actual token values and DTCG-formatted token architecture. |
| **Vision → Palette** | Density and navigation-model decisions per platform (sidebar vs. tab bar vs. Digital Crown) for usability validation — especially touch-target and hover-affordance checks on the chosen archetype. |
| **Vision → Ink** | Icon style/weight/metaphor language required by the archetype (e.g., Expressive-Brand needs a custom icon system; System-Native stays on SF Symbols). |

---

## Sources

- [Apple Newsroom — "Apple introduces a delightful and elegant new software design" (2025-06-09)](https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/)
- [Apple Developer — Liquid Glass technology overview](https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass)
- [MacRumors — "Apple Design Award Winners 2025" (2025-06-03)](https://www.macrumors.com/2025/06/03/apple-design-award-winners-2025/)
- [9to5Mac — "Apple reveals Apple Design Awards app and game winners for 2026" (2026-06-02)](https://9to5mac.com/2026/06/02/apple-reveals-apple-design-awards-app-and-game-winners-for-2026/)
- [Apple Newsroom — "Apple reveals winners of the 2026 Apple Design Awards" (2026-06-02)](https://www.apple.com/newsroom/2026/06/apple-reveals-winners-of-the-2026-apple-design-awards/)
- [MacRumors — "iOS 26's Liquid Glass Design Draws Criticism From Users" (2025-09-17)](https://www.macrumors.com/2025/09/17/ios-26-liquid-glass-critiques/)
- [Six Colors — "macOS 26 Tahoe review: Power under glass" (2025-09)](https://sixcolors.com/post/2025/09/macos-26-tahoe-review-power-under-glass/)
- [MacStories — "macOS 26 Tahoe: The MacStories Review" (2025-09)](https://www.macstories.net/stories/macos-26-tahoe-the-macstories-review/2/)
- [MacRumors — "macOS Tahoe Review: Spotlight Shines, Liquid Glass Disappoints" (2025-08-01)](https://www.macrumors.com/2025/08/01/macos-tahoe-review/)
- [Daring Fireball — "Mac-Assed Mac Apps" (2020-03-20)](https://daringfireball.net/linked/2020/03/20/mac-assed-mac-apps)
- [Setproduct — "Glassmorphism vs neumorphism vs liquid glass" (2026)](https://www.setproduct.com/blog/liquid-glass-vs-glassmorphism)
