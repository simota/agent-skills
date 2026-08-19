# React Patterns & Server Components
---
## React 19 Hooks
- **useActionState**
- **useFormStatus**
- **useOptimistic**
- **use()**
---
## 5. React 19 Breaking Changes
| Change | Migration |
|--------|-----------|
| `forwardRef` deprecated | Use `ref` as a regular prop: `function Input({ ref, ...props })` |
| `Context.Provider` deprecated | Use `<MyContext>` directly as the provider |
| `ref` callbacks get cleanup | Return a cleanup function from ref callbacks |
| Document metadata hoisting | `<title>`, `<meta>`, `<link>` in components hoist to `<head>` automatically |
### React 19.2 (October 2025 — stable)
| Feature | Purpose |
|---------|---------|
| `<Activity mode="visible \| hidden">` | Mount-preserving offscreen rendering — `hidden` unmounts effects + defers updates while keeping component state for back-nav / prefetch |
| `<ViewTransition>` | First-class wrapper around the View Transitions API. SSR Suspense reveals are now batched specifically to enable cross-stream transitions |
| `useEffectEvent` | Stable, non-reactive callback for "event-like" logic inside `useEffect`. **Do not** add to the deps array — `eslint-plugin-react-hooks@6` ignores it automatically |
| `cacheSignal()` (RSC) | `AbortSignal` tied to the lifetime of `cache()` — pass to `fetch` to cancel deduped requests when the render completes/aborts/fails |
| Partial Pre-rendering APIs | `prerender({prelude, postponed})` → `resume()` / `resumeAndPrerender()` for static shell + dynamic resume |
| Performance Tracks | Chrome DevTools "Scheduler ⚛" and "Components ⚛" custom tracks |
| `useId` prefix change | Default `:r:` → `_r_` (valid `view-transition-name` / XML 1.0 name) |
> **Security:** CVE-2025-55182 (React2Shell, CVSS 10.0) affects 19.0.0, 19.1.0–19.1.1, and 19.2.0 — unauthenticated RCE via unsafe deserialization in Server Actions. Pin to 19.0.1+, 19.1.2+, or 19.2.1+ (Next.js 15.1.4+ / 16+).
---
## 6. React Compiler (v1.0 Stable — October 2025)
| Before | With React Compiler |
|--------|-------------------|
| Manual `useMemo` / `useCallback` | **Auto-memoized** — not needed |
| `React.memo` wrapper | Compiler decides |
| Dependency array management | Compiler tracks (supports optional chains + array indices) |
| `eslint-plugin-react-compiler` | **Merged into** `eslint-plugin-react-hooks@6` |
**Rules:**
- New code: skip `useMemo`/`useCallback` entirely.
- Existing manual memoization: safe to keep (no harm). Removing it may change compilation output — test before removing.
- Requires Rules of React compliance (pure render, no side effects during render).
- Opt-out directive: `"use no memo"` at file/function level.
- Can memoize after conditional returns (impossible with manual hooks).
- Pin to exact version (`--save-exact`) if test coverage is thin — memoization behavior may shift between minor versions.
**New ESLint rules shipped in `react-hooks@6`:**
- `set-state-in-render` — render-loop detection
- `set-state-in-effect` — flags expensive effect work
- `refs` — unsafe ref access during render
**Framework integration (defaults):**
- **Next.js 16+**: `reactCompiler: true` in `next.config.ts` (stable, opt-in; requires `babel-plugin-react-compiler`).
- **Expo SDK 54+**: enabled by default.
- **Vite / `create-next-app`**: compiler-enabled template available.
- Compatible with React 17+ via `react-compiler-runtime`.
---
## 7. Server Components (RSC)
- **Composition: Push `'use client'` to Leaves**
### When to Use Client Components
| Condition | Server | Client |
|-----------|:---:|:---:|
| DB/API direct access | ✅ | — |
| Display-only (props) | ✅ | — |
| `onClick`/`onChange` handlers | — | ✅ |
| `useState`/`useEffect` | — | ✅ |
| Browser APIs (localStorage) | — | ✅ |
- **Suspense Streaming**
---
## 8. Server Actions
### Server Actions vs Route Handlers
| Use case | Server Actions | Route Handlers |
|----------|:---:|:---:|
| Form mutations | ✅ | — |
| UI data changes | ✅ | — |
| Public API / Webhooks | — | ✅ |
| Large file uploads | — | ✅ |
| External service calls | — | ✅ |
- **Cache & Revalidation (Next.js 15)**
### Next.js 16 — Cache Components + new cache APIs (October 2025)
| API | Runtime | Behavior |
|-----|---------|----------|
| `revalidateTag(tag, profile)` | Anywhere | SWR semantics; **profile arg is now required** (e.g. `'max'`, `'hours'`, `'days'`, or `{ expire: 3600 }`). Single-arg form is deprecated. |
| `updateTag(tag)` | Server Actions only | Read-your-writes — invalidates and reads fresh data in the same request. Use for forms/settings where users must see their change. |
| `refresh()` | Server Actions only | Refreshes **uncached** data only; does not touch cache. Complement to client `router.refresh()`. |
- `middleware.ts` → **`proxy.ts`** (Node.js runtime; old name deprecated).
- `params` / `searchParams` props and `cookies()` / `headers()` / `draftMode()` are now **async** — `await` is required.
- `experimental.ppr` and `experimental.dynamicIO` flags removed; PPR is now integrated into Cache Components.
- Turbopack is the **default bundler**; opt out with `next dev --webpack` / `next build --webpack`.
- Min Node.js 20.9, TypeScript 5.1, Chrome 111+/Edge 111+/Firefox 111+/Safari 16.4+.
### Next.js 16.2 (March 18, 2026)
| Feature | Impact |
|---------|--------|
| **Server Fast Refresh** | Fine-grained server-side hot reloading — RSC tree is patched without full reload |
| **Adapter API (stable)** | Typed, versioned output description; deploy to Cloudflare/Netlify/Vercel/AWS without vendor lock-in |
| **Turbopack filesystem caching** | Compiler artifacts persisted across restarts; large projects see 400–900% faster compile after first build |
| **React Compiler stable** | `reactCompiler: true` in `next.config.ts` is now stable (was experimental in 16.0) |
| **AGENTS.md in `create-next-app`** | Auto-generated AI agent context file with version-matched Next.js docs |
| **Hydration Diff Indicator** | Clear server/client diff in error overlay — reduces debugging time for RSC mismatches |
---
## 9. Form Handling Selection Guide
| Criteria | React Hook Form | React 19 Native | Conform | TanStack Form v1 |
|----------|:---:|:---:|:---:|:---:|
| Large/complex forms | ✅ | — | — | ✅ |
| Server Actions first | △ | ✅ | ✅ | — |
| Works without JS | — | ✅ | ✅ | — |
| Dynamic field arrays | ✅ | manual | ○ | ✅ |
| UI library integration | ✅ | — | — | ✅ |
| Type-safe field paths | — | — | — | ✅ |
| Cross-framework | React only | React only | React only | React/Vue/Angular/Solid/Lit |
| Bundle size | +8.6KB | 0KB | light | +12KB |
**Recommendations:** Complex forms → RHF + Zod v4 / Simple + Server Actions → React 19 native / Remix/Next.js PE → Conform / Dynamic/nested or cross-framework → TanStack Form v1
### Schema Validation (2026)
| Library | Bundle (gzip) | Speed vs Zod v3 | Best For |
|---------|--------------|-----------------|----------|
| **Zod v4** (Aug 2025) | 17.7KB standard / **1.9KB** `@zod/mini` | 14× faster parsing; 25k→175 TS instantiations | Default; deep ecosystem (RHF, tRPC, Drizzle). Use `"zod/mini"` import for edge/client bundles |
| **Valibot** | ~1.37KB | Fastest; still ~30% faster than Zod v4 | Edge functions (Cloudflare Workers, Vercel Edge) |
| **ArkType** | ~5KB | Comparable to Valibot | Advanced type inference, runtime generics |
---
## 10. Anti-Patterns
### Hooks
| # | Pattern | Problem | Fix |
|---|---------|---------|-----|
| 1 | Derived state via `useEffect` | Unnecessary re-renders | Compute directly in render |
| 2 | Raw `fetch` in `useEffect` | Memory leak, race conditions | TanStack Query |
| 3 | Conditional hook calls | Rules of Hooks violation | Always call + early return |
| 4 | Excessive `useMemo`/`useCallback` | Complexity without benefit | React Compiler / measure first |
| 5 | `use` prefix on non-hook functions | Misleading naming | Use regular function name |
### RSC
| # | Pattern | Problem | Fix |
|---|---------|---------|-----|
| 1 | Top-level `'use client'` | All children become Client Components | Push to leaves + Composition |
| 2 | Page-level `await` | Blocks entire shell | Suspense isolation |
| 3 | Serial data fetching | Server-side waterfall | `Promise.all` for parallel |
| 4 | Passing large objects across boundary | HTML payload bloat | Pass only needed fields |
| 5 | Missing `revalidate` after mutation | Stale UI | `revalidatePath`/`revalidateTag` |
| 6 | `await` in layouts | Delays entire app | Layouts sync, data in pages |
**Source:** [React 19 Blog](https://react.dev/blog/2024/12/05/react-19) · [React 19.2 Blog](https://react.dev/blog/2025/10/01/react-19-2) · [React Compiler v1.0](https://react.dev/blog/2025/10/07/react-compiler-1) · [Server Components](https://react.dev/reference/rsc/server-components) · [Next.js 16](https://nextjs.org/blog/next-16) · [Next.js 16.1](https://nextjs.org/blog/next-16-1) · [Next.js 16.2](https://nextjs.org/blog/next-16-2) · [Next.js 16 Upgrade Guide](https://nextjs.org/docs/app/guides/upgrading/version-16) · [`use cache` directive](https://nextjs.org/docs/app/api-reference/directives/use-cache) · [`eslint-plugin-react-hooks@6`](https://www.npmjs.com/package/eslint-plugin-react-hooks) · [TanStack Form v1](https://tanstack.com/blog/announcing-tanstack-form-v1) · [Zod v4](https://zod.dev/v4)
