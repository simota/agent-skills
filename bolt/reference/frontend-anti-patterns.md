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
## 6. Integration with Bolt
**Source:** [DeveloperWay: React Compiler & React 19](https://www.developerway.com/posts/react-compiler-soon) · [Medium: React Compiler Won't Save You](https://medium.com/@domwozniak/react-compiler-wont-save-you-from-this-performance-mistake-a257541fe533) · [DEV.to: React Performance Optimization 15 Best Practices 2025](https://dev.to/alex_bobes/react-performance-optimization-15-best-practices-for-2025-17l9) · [SitePoint: React 19 Compiler What Senior Developers Need to Know](https://www.sitepoint.com/why-react-19-s-compiler-changes-everything-for-senior-devs/)
