# Frontend Performance Anti-Patterns

> React/frontend performance pitfalls, the impact of the React Compiler, and mistakes in rendering optimization

## 1. 10 Major React Performance Anti-Patterns

| # | Anti-Pattern | Problem | Solved by React Compiler? | Countermeasure |
|---|-------------|------|---------------------|------|
| **FP-01** | **Excessive memoization** | useMemo/useCallback on everything → code complexity increases, no real benefit | Yes (automated) | Confirm impact via measurement. In the Compiler era, reduce manual memoization |
| **FP-02** | **Defining a component inside its parent** | A new component is generated every render → state resets | No | Define components at the top level of the file |
| **FP-03** | **Inline objects/arrays** | New reference every render, e.g. `style={{}}` | Yes (automated) | Without a Compiler: useMemo / hoist to a constant |
| **FP-04** | **Giant Context** | All state in a single Context → all consumers re-render | No | Split Context by update frequency · separate State/Dispatch |
| **FP-05** | **Lifting state too far** | State lifted to an unnecessary parent → entire tree re-renders | No | Keep state in the minimal component that needs it |
| **FP-06** | **Misuse of the key attribute** | `key={index}` causes unintended reuse during array operations | No | Use a stable, unique ID as the key |
| **FP-07** | **Side effects during render** | API calls / DOM manipulation during render | No (violates Rules of React, so the Compiler skips it) | Move to useEffect / event handlers |
| **FP-08** | **Non-virtualized large lists** | Rendering 1000+ items to the DOM all at once | No | Virtualize with @tanstack/react-virtual |
| **FP-09** | **Unoptimized images** | Serving large images uncompressed and unresized | No | next/image · WebP/AVIF · lazy loading · srcset |
| **FP-10** | **Unrestricted loading of third-party scripts** | Loading analytics, ads, chat, etc. on every page | No | defer/async · lazy loading · Partytown |

---

## 2. Impact of the React Compiler (React Forget)

```
What the React Compiler is:
  - Operates as a Babel plugin
  - Automatically applies useMemo / useCallback / memo
  - Not included in React 19 (separate opt-in)
  - Rolling out incrementally across 2024-2026

What the Compiler solves:
  ✅ The management burden of manual memoization (FP-01, FP-03)
  ✅ Mistakes in dependency arrays
  ✅ Unnecessary re-renders from shallow prop comparison

What the Compiler does NOT solve:
  ❌ Context design problems (FP-04)
  ❌ State placement design problems (FP-05)
  ❌ The need for virtualization (FP-08)
  ❌ Data-fetching strategy
  ❌ Image optimization (FP-09)
  ❌ Code that violates the Rules of React (silently skipped → a new class of bug)

Strategy for the Compiler era (2025-2026):
  1. New code: avoid manual memoization, let the Compiler handle it
  2. Existing code: don't rush to remove working useMemo/useCallback
  3. Focus on architecture: component composition, state placement, Context design
  4. Strictly follow the Rules of React: violating code causes the Compiler to skip optimization

Note: In one Compiler test, only 1 out of 8 unnecessary
       re-renders was reportedly fixed.
  → The Compiler is not a silver bullet — architectural design still matters
```

---

## 3. The Correct Priority Order for Rendering Optimization

```
React rendering optimization in ROI order:

  1. Improve component composition (biggest impact)
     - "Move state down": relocate state to the component that uses it
     - "children pattern": pass unchanging parts as children
     - Composition over Memoization

  2. Optimize state management
     - Split Context (by update frequency)
     - State/Dispatch separation pattern
     - Selective subscriptions via external state management (Zustand, Jotai)

  3. Virtualization
     - Lists with 100+ items → @tanstack/react-virtual
     - Limit DOM node count with virtual scrolling

  4. Code splitting
     - Route-based: lazy(() => import('./pages/X'))
     - Component-based: lazy-load heavy components
     - Library-based: import only when used

  5. Memoization (smallest impact — the Compiler is set to automate this)
     - useMemo: cache expensive computations
     - useCallback: stabilize callbacks passed to child components
     - memo: prevent re-rendering of heavy components

Note: A pure JS operation (sorting 250 items) takes < 2ms,
      while rendering takes 20ms+.
  → Reducing re-renders is more effective than optimizing JS computation
```

---

## 4. Image and Media Optimization

| Technique | Effect | Implementation |
|------|------|------|
| **WebP/AVIF** | 25-50% smaller than JPEG | `<picture>` + `<source type="image/avif">` |
| **Responsive images** | Size matched to the device | `srcset` + `sizes` |
| **Lazy loading** | Reduces initial load | `loading="lazy"` (below-the-fold) |
| **Priority hints** | Prioritizes the LCP image | `fetchpriority="high"` (hero image) |
| **next/image** | Automatic optimization | Next.js's built-in optimization |
| **SVG optimization** | Removes unnecessary metadata | SVGO / svgo-loader |
| **Video alternatives** | GIF → MP4/WebM | `<video autoplay muted loop>` |

---

## 5. Third-Party Script Management

```
Problem: Third-party scripts are a major cause of TBT (Total Blocking Time)

Classification and priority:
  Critical (synchronous): auth · payment → inside <head>
  Important (defer): analytics → defer attribute
  Nice-to-have (lazy): chat · ads → after user interaction

Countermeasures:
  1. Proper use of defer/async attributes
  2. Partytown: run third-party scripts in a Web Worker
  3. Facade pattern: lightweight placeholder → load on interaction
     example: YouTube embed → thumbnail image → iframe on click
  4. Resource hints:
     - dns-prefetch: resolve DNS ahead of time
     - preconnect: establish TCP + TLS ahead of time
  5. Regular audits: check unused code percentage in the Coverage tab
```

---

## 6. Integration with Bolt

```
Usage within Bolt:
  1. Check FP-01 through FP-10 in the PROFILE phase
  2. Apply the rendering optimization priority order in the SELECT phase
  3. Implement with Compiler considerations in the OPTIMIZE phase
  4. Verify with React DevTools + Lighthouse in the VERIFY phase

Quality gates:
  - memo on every component → warn as excessive memoization (FP-01)
  - Component defined inside another component → require moving it out (FP-02)
  - Lists with 1000+ items → require virtualization (FP-08)
  - Unoptimized images → recommend next/image etc. (FP-09)
  - Rules of React violations → warn as a Compiler-skip risk (FP-07)
```

**Source:** [DeveloperWay: React Compiler & React 19](https://www.developerway.com/posts/react-compiler-soon) · [Medium: React Compiler Won't Save You](https://medium.com/@domwozniak/react-compiler-wont-save-you-from-this-performance-mistake-a257541fe533) · [DEV.to: React Performance Optimization 15 Best Practices 2025](https://dev.to/alex_bobes/react-performance-optimization-15-best-practices-for-2025-17l9) · [SitePoint: React 19 Compiler What Senior Developers Need to Know](https://www.sitepoint.com/why-react-19-s-compiler-changes-everything-for-senior-devs/)
