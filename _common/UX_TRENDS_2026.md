# UX Trends 2025-2026 — Design / IA / Frontend

> Cross-domain best practices, anti-patterns, and case studies collected from primary web sources (2025-2026).
> Reference this file when applying current standards across design, information architecture, or frontend implementation.
> All URLs verified by source research; cite them when recommending a pattern so reviewers can trace the claim.

## How to use

| Agent | Read primarily | Why |
|-------|----------------|-----|
| `vision` | §1 Design (OS design languages, brand systems) | Direction-setting needs current visual language |
| `muse` | §1 Design (tokens, OKLCH/P3, DTCG, dark-mode) | Token foundation must align with 2025-2026 standards |
| `frame` | §1 Design (DTCG format) + Code Connect ref | Figma-side spec is now stable; consume it correctly |
| `forge` | §3 Frontend (RSC, streaming, Suspense) | Prototype stacks have shifted; templates must match |
| `atelier` | All three sections | Cross-domain orchestration |
| `vitrine` | §3 Frontend (component patterns) + §1 Design (tokens) | Catalog conventions and token integration |
| `flow` | §1 Design (motion, linear() timing, reduced-motion) | New motion primitives + a11y requirements |
| `palette` | §2 IA (navigation, cognitive load) + §1 Design (a11y) | UX quality and inclusion |
| `prose` | §2 IA (agentic UX, llms.txt) | Voice/tone in the AI era |
| `echo` | §2 IA (NN/g methodologies) + §1 Design (a11y) | Validation methodology |

---

## 1. Design — Tokens / Visual / OS

### 1.1 Best practices

- **Design token 3-layer hierarchy (Primitive → Semantic → Component).** Name by intent (`color.text.error`), not by value (`color.red`). Keep the primitive layer private.
  - https://www.smashingmagazine.com/2024/05/naming-best-practices/
  - https://medium.com/eightshapes-llc/naming-tokens-in-design-systems-9e86c7444676
- **DTCG (Design Tokens Format Module) — first stable spec on 2025-10-28.** W3C Community Group. Use `.tokens.json`, MIME `application/design-tokens+json`. Style Dictionary / Tokens Studio / Penpot / Supernova have implementations.
  - https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/
  - https://www.designtokens.org/tr/drafts/format/
- **Apple Liquid Glass (WWDC25, 2025-06-09).** Shared across iOS / macOS / visionOS 26. The system honours Reduced Transparency / Increased Contrast / Reduced Motion automatically — your components must too.
  - https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass
- **Material 3 Expressive (Google I/O 2025, announced 2025-05-13).** Motion physics, 35 new shapes with shape-morphing, Dynamic Color extended across Google apps and Wear OS. UI-element recognition speed reportedly up to 4× in M3 research.
  - https://blog.google/products-and-platforms/platforms/android/material-3-expressive-android-wearos-launch/
  - https://m3.material.io/styles/motion/overview/specs
- **OKLCH + Display P3 colour pipelines.** Perceptually uniform, ~30% more chroma than sRGB. Tailwind v4 default palette is OKLCH/P3. Clamp values that fall outside P3.
  - https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl
  - https://bjango.com/articles/designsystemcolourspace/
- **Native `linear()` timing + spring physics in CSS.** Bouncy/spring motion without JS. Reserve decorative animation for microinteractions only.
  - https://www.joshwcomeau.com/animation/linear-timing-function/
  - https://www.nngroup.com/articles/animation-purpose-ux/
- **WCAG 2.2 AA is the compliance line (ISO/IEC 40500:2025).** WCAG 3.0 / APCA remains a Working Draft as of 2025-2026 — use APCA as a complementary signal, not the primary contrast standard.
  - https://www.w3.org/TR/WCAG22/
  - https://yatil.net/blog/wcag-3-is-not-ready-yet
  - https://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html

### 1.2 Anti-patterns

- **Token sprawl / naming collapse.** `--blue` (which blue?), `--color1` (meaningless), `--the-blue-on-homepage` (overspecific), value-based names like `color-text-red` break the moment hue changes. Use intent (`color-text-error`).
  - https://medium.com/@hereinthehive/new-to-design-tokens-and-find-naming-difficult-406cff7a38a4
  - https://www.alwaystwisted.com/articles/design-token-naming-conventions
- **3-tier tokens dropped onto a legacy codebase wholesale.** Skipping the semantic layer collapses the cascade. Rebrands documented as needing 2-tier or staged introduction.
  - https://medium.com/@robinwesterhoff/design-system-challenge-rebranding-100-touchpoints-in-under-9-months-ca5d9af416eb
- **Decorative motion overload.** Documented case: insurance homepage where 64% of users missed critical info because of background animation. Increases cognitive load and excludes motion-sensitive users.
  - https://medium.com/@sophie_paxtonUX/stop-gratuitous-ui-animation-9ece9aa9eb97
  - https://trevorcalabro.substack.com/p/most-ui-animations-shouldnt-exist
- **Ad-hoc density / spacing.** 4 / 5 / 6 pt base units break under cross-team scale; 8 pt base is the practical default.
  - https://medium.com/eightshapes-llc/space-in-design-systems-188bcbae0d62
- **Dark mode bolted on as a class flip.** Elevations stop physically resolving, light-mode accents go muddy. Treat dark as a first-class context with its own elevation and tokens.
  - https://chyshkala.com/blog/why-linear-design-systems-break-in-dark-mode-and-how-to-fix-them
- **Missing `prefers-reduced-motion` + no Pause/Stop/Hide controls.** Violates WCAG 2.2.2 and 2.3.3 — and induces vertigo for vestibular users.
  - https://blog.pope.tech/2025/12/08/design-accessible-animation-and-movement/

### 1.3 Case studies

- **Shopify Polaris Unified for Web (2025-10-01).** Admin / Checkout / Customer Accounts unified on Web Components. React dropped from core. UI extensions on Preact with a 64 KB cap. New API surface designed for LLM consumption.
  - https://www.shopify.com/partners/blog/polaris-unified-and-for-the-web
- **Material 3 Expressive stable (Google I/O 2025).** Motion physics + shape morphing rolled across Pixel and Wear OS.
  - https://io.google/2025/explore/technical-session-24/
- **Radix Themes 3.0 with P3 support.** Zero-runtime layout primitives, APCA-based contrast, wide-gamut alpha channel.
  - https://www.radix-ui.com/blog/themes-3
- **GitHub Primer inclusive colour system.** Light / dark / dimmed / high-contrast / colour-vision themes via Primer Primitives, available as both CSS and Figma variables.
  - https://github.blog/engineering/user-experience/unlocking-inclusive-design-how-primers-color-system-is-making-github-com-more-inclusive/

---

## 2. Information Architecture

### 2.1 Best practices

- **Mega menus** for large catalogues — 2D layout exploits recognition over recall and survives 2-3 sub-levels.
  - https://www.nngroup.com/articles/mega-menus-work-well/
- **Breadcrumbs as a supplement** to global/local navigation, not as a replacement. Mobile adoption is increasing (NN/g, 11 guidelines).
  - https://www.nngroup.com/articles/breadcrumbs/
- **NN/g menu-design 17-item checklist.** 7±2 limit, label specificity, state representation, sub-nav depth, visibility.
  - https://www.nngroup.com/articles/menu-design/
- **Command Palette (⌘K) as IA-skip.** Standard in Linear / Notion / Figma / Vercel / Raycast. Improves keyboard-first navigation and feature discovery during onboarding.
  - https://solomon.io/designing-command-palettes/
- **Card Sorting (generative) + Tree Testing (validation).** Optimal Sort / Treejack are the standard tools; cap card sorts at 30-50 to avoid fatigue.
  - https://www.nngroup.com/articles/card-sorting-tree-testing-differences/
  - https://www.nngroup.com/articles/tree-testing/
- **JTBD-based IA.** Structure by the job the user is trying to do, not by internal org categories. Higher invariance than personas.
  - https://www.nngroup.com/articles/personas-jobs-be-done/
- **Chunking + Hick's Law.** 4-7 items at top level, Progressive Disclosure shrinks decision time logarithmically.
  - https://lawsofux.com/chunking/
- **Agentic UX / AI-native IA.** Information architecture is knowledge architecture. IAA Framework: Intent Preview / Variable Autonomy / Graceful Escalation. Hybrid keyword + vector search (Algolia NeuralSearch) for semantic findability.
  - https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/
  - https://uxdesign.cc/from-products-to-systems-the-agentic-ai-shift-eaf6a7180c43
  - https://www.algolia.com/blog/ai/agentic-architecture

### 2.2 Anti-patterns

- **Over-deep hierarchy.** Beyond 3 levels, click count and label-comprehension load explode.
  - https://www.nngroup.com/articles/flat-vs-deep-hierarchy/
- **"Flatten everything".** 50+ items in one level breaks under Hick's Law. Flat works up to ~10 items; beyond that, use a two-part menu (popular + alphabetised) or introduce hierarchy.
  - https://www.nngroup.com/articles/ia-questions-navigation-menus/
- **Hamburger menu overuse.** >50% of users do not open it, or open it and fail to find the target. Replace with tab bar / bottom nav / partial reveal — the 2025 trend.
  - https://www.nngroup.com/articles/hamburger-menu-icon-recognizability/
  - https://smart-interface-design-patterns.com/articles/avoid-hamburger-menus/
- **Orphan / dead-end pages.** No inbound links collapses discovery, SEO, and authority distribution. Enforce related-link blocks.
  - https://linkilo.co/blog/dead-end-pages/
- **Search as an escape hatch.** "Just search for it" is the signal that the IA itself has failed. Use Tree Testing to repair the IA, not to apologise for it.
  - https://www.nngroup.com/articles/search-visible-and-simple/
- **Split buttons in navigation.** Label + dropdown ambiguity causes mis-taps and extra clicks.
  - https://www.nngroup.com/articles/split-buttons-navigation/

### 2.3 Case studies

- **Slack 2024 redesign.** Tabs unified into Home / DMs / Activity / Later / More; Directories added; Canvases and Lists relocated under Files; Tools replaces Automations.
  - https://slack.design/articles/how-we-redesigned-slack-for-the-ipad/
- **Vercel Docs + AI SDK + `llms.txt`.** Entire docs surface published as Markdown for LLM navigation. AI Gateway / Agents / MCP Servers sections segmented by job.
  - https://vercel.com/docs
- **Figma Schema 2025 / Config 2025.** Code Connect UI, Extended Collections (multi-brand), Slots. Standardised IA: Foundations → Components → Patterns → Recipes.
  - https://www.figma.com/blog/schema-2025-design-systems-recap/
- **Algolia NeuralSearch / Agent Studio.** Keyword + vector hybrid, RAG-as-a-service. Concrete example of "IA defines what the agent can do".
  - https://www.algolia.com/blog/ai/rag-is-not-dead

---

## 3. Frontend

### 3.1 Best practices

- **React 19.2 (2025-10).** Activity / cacheSignal / useEffectEvent. RSC-first split: `.server.tsx` / `.client.tsx` with one-way Server → Client imports.
  - https://react.dev/blog/2025/10/01/react-19-2
- **Svelte 5 Runes (GA 2024-10).** Explicit `$state` / `$derived` / `$effect`. `.svelte.ts` brings reactivity to plain TS files.
  - https://svelte.dev/blog/runes
- **Vue 3.6 Vapor Mode.** No virtual DOM, performance approaching Solid.
  - https://www.vuemastery.com/blog/the-future-of-vue-vapor-mode/
- **Tailwind v4 (2025-01-22).** Rust-based Oxide engine, 5× full / 100× incremental builds. CSS-first `@theme` config, native `@property` / `color-mix()` / cascade layers / `not-*` variants.
  - https://tailwindcss.com/blog/tailwindcss-v4
- **Core Web Vitals INP.** 200 ms threshold. Long-task splitting, Web Workers, `requestIdleCallback`.
  - https://web.dev/articles/inp
- **View Transitions API — same-document Baseline Newly Available (2025-10).** `document.startViewTransition()` + `view-transition-class` + `view-transition-name: match-element`. Speculation Rules erase LCP cost on cross-document variants.
  - https://developer.chrome.com/blog/view-transitions-in-2025
  - https://web.dev/blog/same-document-view-transitions-are-now-baseline-newly-available
- **TanStack Query v5 + Zustand split.** Server state in Query (set `staleTime` / `gcTime`), UI state in small Zustand stores. Never duplicate server state into Zustand.
  - https://tanstack.com/query/latest/docs/framework/react/guides/request-waterfalls
- **CSS Container Queries / Cascade Layers / `@scope`.** Interop 2025 stabilises `@scope`, giving component-scoped CSS natively.
  - https://blog.logrocket.com/cascade-layers-subgrid-container-queries-whats-new-css/
- **Vite 7 (2025-06) / Turbopack stable (Next.js 16, 2025-10).** Rolldown gives 4-16× builds; Turbopack 2-5× compiles with filesystem cache.
  - https://vite.dev/blog/announcing-vite7
  - https://nextjs.org/blog/next-16
- **Forms: React Hook Form + Standard Schema (Valibot / ArkType / Zod).** Resolvers share a unified API. SSR-first stacks use Conform.
  - https://github.com/react-hook-form/resolvers
- **A11y: React Aria > Radix Themes.** Adobe React Aria strictly implements 40+ patterns; Radix Themes provides pre-styled system on top.
  - https://www.radix-ui.com/primitives/docs/overview/accessibility

### 3.2 Anti-patterns

- **`useEffect` to sync derived state.** Use render-time computation or `useMemo`. React docs explicitly warn against this.
  - https://react.dev/learn/you-might-not-need-an-effect
- **Context API for high-frequency state.** Every consumer re-renders. Move to selector-aware stores (Zustand / Jotai).
  - https://blog.logrocket.com/solving-prop-drilling-react-apps/
- **Render-fetch waterfalls.** Sequential parent→child fetching balloons time-to-data. Parallel fetch / RSC co-location / Suspense boundaries solve it.
  - https://blog.sentry.io/fetch-waterfall-in-react/
- **Server state duplicated into Zustand / Redux.** Causes stale data and double fetches. Single source of truth is Query.
  - https://www.nextsteps.dev/en/posts/federated-state-done-righ/
- **`useEffect` dep-array drift.** Missing or stale closures cause infinite loops. React 19.2's `useEffectEvent` removes most of the typical cases.
- **A11y bolted on after the fact.** Custom modal / combobox / menu missing focus trap, keyboard, ARIA. Replace with React Aria or Radix Primitives.
  - https://www.radix-ui.com/primitives
- **SSR vs CSR mis-routing.** Auth-heavy personalised UIs on SSG, SEO-critical LPs on CSR — both fail. RSC + streaming + Suspense is the modern default.
  - https://blog.madrigan.com/en/blog/202512041544/

### 3.3 Case studies

- **Shopify Hydrogen + RSC.** Vite-based RSC ahead of upstream React. Hydrogen v2 absorbs Remix, ships nested routing and LCP improvements.
  - https://shopify.engineering/react-server-components-best-practices-hydrogen
- **Vercel running Turbopack in production.** vercel.com / v0.app / nextjs.org behind Turbopack handle 1.2 B+ requests; Next.js 16 turns it on by default.
  - https://nextjs.org/blog/next-16
- **Linear Sync Engine.** MobX-backed in-memory object graph plus a bespoke sync engine for partial sync / offline / undo-redo. CTO-acknowledged reverse-engineering writeup available.
  - https://github.com/wzhudev/reverse-linear-sync-engine
  - https://newsletter.pragmaticengineer.com/p/linear
- **GitHub Web Components + ViewComponent.** Rails ViewComponent and Custom Elements map 1:1, giving back-end / front-end a single abstraction.
  - https://github.blog/2021-05-04-how-we-use-web-components-at-github/
- **RSC in production.** ~38% faster initial load measured on WebPageTest (2025-02). Suspense streaming removes waterfalls.
  - https://vercel.com/blog/understanding-react-server-components

---

## Cross-domain themes

| Theme | Design | IA | Frontend |
|-------|--------|----|---------|
| AI / LLM adaptation | Liquid Glass adaptive surfaces | Agentic UX, `llms.txt`, vector + keyword search | React Aria + agent integration, MCP |
| A11y promoted to baseline | WCAG 2.2, `prefers-reduced-motion` mandatory | NN/g inclusive navigation research | React Aria / Radix Primitives, INP budget |
| Three-layer structure | Primitive → Semantic → Component tokens | Foundations → Components → Patterns → Recipes | Server ↔ Client components, Standard Schema |
| The "bolt-on" trap | Dark mode added late, a11y last | Search as escape hatch, hamburger overuse | `useEffect` for sync, server state in Zustand |
| OS-native expression flowing into the web | Liquid Glass, M3 Expressive | Command Palette (OS-like) | View Transitions, native `@scope` |

---

## Source provenance

All entries above were collected via web research in 2026-05; each item is paired with a primary source (vendor blog, W3C, NN/g, web.dev, framework release notes, or design-system author).
When citing, prefer the linked source over secondary aggregators. Re-verify URLs and dates before quoting in user-facing deliverables, as the landscape moves quickly.
