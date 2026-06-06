# State Management Decision Guide

State classification, tool selection framework, RSC-era patterns, and anti-patterns.

---

## 1. State Classification

| Type | Description | Recommended Tool |
|------|-------------|-----------------|
| **Remote State** | API/DB data; needs fetch, cache, sync | TanStack Query v5 / SWR |
| **URL State** | UI state reflected in URL params | nuqs v2 / searchParams |
| **Local State** | Scoped to a single component | `useState` / `useReducer` |
| **Shared State** | Shared across distant components | Context (few) → Zustand (many) |

---

## 2. Decision Flowchart

```
Need state?
├── Server data? → TanStack Query / SWR
├── Should reflect in URL? → nuqs / useSearchParams
├── Single component? → useState / useReducer
└── Shared across components?
    ├── 2-3 levels of parent-child? → Props drilling (OK)
    ├── 1-2 concerns? → React Context
    └── 3+ concerns or high-frequency updates? → Zustand
```

---

## 3. Library Selection (2026)

| Library | Good fit | Poor fit |
|---------|----------|----------|
| **Zustand v5** | Default for shared React client state. Lightweight, selective re-renders, uses native `useSyncExternalStore`. Bundle ~1KB | Server data, RSC-only trees |
| **TanStack Query v5** | Standard for server state. Auto cache/dedup/invalidation, stable Suspense, 20% smaller than v4 | Pure client state |
| **Jotai (v2 → v3 in 2026)** | Fine-grained atom reactivity, many derived/computed values, Suspense-friendly. **v3 will drop React <18, `atomFamily` → `jotai-family` package, possibly drop `loadable` for `unwrap`** | Simple global state, server data |
| **Redux Toolkit + RTK Query** | Large enterprise apps, strict architecture, DevTools/time-travel required, built-in optimistic updates + websocket streaming + OpenAPI codegen | Small-to-mid apps, simple state |
| **XState v5** | Complex state machines (auth flows, multi-step forms, video/recording, onboarding). `setup()` + `createMachine`, fully type-safe, no Redux dep | Single-axis on/off state |
| **React Context** | Theme, locale, low-frequency updates | High-frequency state, large consumer trees |
| **Recoil** | ⚠️ **Archived January 1, 2025** — do not use for new projects | — |
| **Pinia 3 (Vue)** | Default Vue 3 store. Setup or Option style. Devtools, plugins | Vue 2 (use Pinia v2.x) |
| **Pinia Colada (Vue)** | Server state for Vue/Nuxt apps — TanStack-Query-equivalent companion to Pinia | Pure client state (use Pinia core) |
| **nuqs v2** | URL-as-state (filters, pagination, tabs) in Next.js App Router | Non-URL local state |
| **Signals (TC39 Stage 1)** | Cross-framework reactive primitive — Solid 2, Angular 20, Vue 3.5 (alien-signals), Svelte 5 runes, Preact Signals converge here. Future-proof mental model | Not yet a standalone runtime choice in React (use React Compiler) |

---

## 4. TanStack Query v5

### Migration from v4

| v4 | v5 | Notes |
|----|-----|-------|
| `onSuccess`/`onError`/`onSettled` in `useQuery` | **Removed** | Use `useEffect` or handle in `queryFn` |
| `cacheTime` | `gcTime` | Renamed for clarity |
| `isLoading` (first load only) | `isPending` | `isLoading` = `isPending && isFetching` |
| `useQuery({ queryKey, queryFn })` | Same | Object syntax only (no positional args) |

### Patterns

```tsx
// Custom hook encapsulating query
function useProducts(category?: string) {
  return useQuery({
    queryKey: ['products', { category }],
    queryFn: () => fetchProducts(category),
    staleTime: 5 * 60 * 1000,
  });
}

// Suspense-first query
function ProductList({ category }: { category: string }) {
  const { data } = useSuspenseQuery({
    queryKey: ['products', category],
    queryFn: () => fetchProducts(category),
  });
  return <ul>{data.map(p => <li key={p.id}>{p.name}</li>)}</ul>;
}

// Optimistic update mutation
function useUpdateProduct() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateProduct,
    onMutate: async (updated) => {
      await queryClient.cancelQueries({ queryKey: ['products'] });
      const prev = queryClient.getQueryData(['products']);
      queryClient.setQueryData(['products'], (old) =>
        old.map(p => p.id === updated.id ? { ...p, ...updated } : p)
      );
      return { prev };
    },
    onError: (_err, _vars, ctx) => {
      queryClient.setQueryData(['products'], ctx?.prev);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
}

// RSC hydration support
import { HydrationBoundary, dehydrate } from '@tanstack/react-query';

// Server Component (page.tsx)
export default async function Page() {
  const queryClient = new QueryClient();
  await queryClient.prefetchQuery({
    queryKey: ['products'],
    queryFn: fetchProducts,
  });
  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <ProductList />
    </HydrationBoundary>
  );
}
```

---

## 5. Zustand v5 Patterns

Zustand v5 (released late 2024, current minor 5.0.x in 2026) dropped React <18, TS <4.5, ES5, and `use-sync-external-store` (now uses the native React 18 hook). Bundle is significantly smaller.

```tsx
import { create } from 'zustand';
import { useShallow } from 'zustand/react/shallow';

// Split stores by concern
const useUIStore = create<UIState>()((set) => ({
  isSidebarOpen: false,
  theme: 'light' as const,
  toggleSidebar: () => set((s) => ({ isSidebarOpen: !s.isSidebarOpen })),
  setTheme: (theme) => set({ theme }),
}));

// Subscribe only to needed values (prevents unnecessary re-renders)
function Sidebar() {
  const isOpen = useUIStore((s) => s.isSidebarOpen);
  // Does not re-render when theme changes
}

// Selecting multiple values — wrap in useShallow to avoid infinite loops
function Header() {
  const { theme, toggleSidebar } = useUIStore(
    useShallow((s) => ({ theme: s.theme, toggleSidebar: s.toggleSidebar }))
  );
}
```

### v5 migration gotchas

| Change | Impact | Fix |
|--------|--------|-----|
| `create((set) => …)` curry | TS inference broke for some patterns | Use `create<State>()((set) => …)` (extra `()`) |
| Selector returning new reference | Can cause **infinite loops** under React 18's stricter equality | Wrap with `useShallow(selector)` or use `createWithEqualityFn` |
| `setState({}, true)` (replace flag) | Used to silently accept partial state | Now type-checked — must pass a **complete** state object |
| Custom equality function in `create` | Removed from default `create` | Import `createWithEqualityFn` from `zustand/traditional` |
| `use-sync-external-store` | Removed as direct dep | Now a peer dep — install if you support React 17 (not recommended) |

---

## 6. URL State with nuqs v2

```tsx
import { useQueryState, parseAsInteger } from 'nuqs';

// Client component
function ProductFilter() {
  const [category, setCategory] = useQueryState('category');
  const [page, setPage] = useQueryState('page', parseAsInteger.withDefault(1));
  // URL synced automatically: ?category=shoes&page=2
}

// Server-side parsing (Next.js App Router)
import { createSearchParamsCache, parseAsString } from 'nuqs/server';

const searchParamsCache = createSearchParamsCache({
  category: parseAsString.withDefault('all'),
  page: parseAsInteger.withDefault(1),
});

export default async function Page({ searchParams }: { searchParams: Promise<Record<string, string>> }) {
  const { category, page } = await searchParamsCache.parse(searchParams);
  const products = await fetchProducts({ category, page });
  return <ProductList products={products} />;
}
```

---

## 7. Redux Toolkit + RTK Query (2026)

Still the canonical choice when DevTools time-travel, large enterprise architecture, or strict review of every state mutation matters.

```ts
// src/services/products.ts
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const productsApi = createApi({
  reducerPath: 'productsApi',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  tagTypes: ['Product'],
  endpoints: (build) => ({
    listProducts: build.query<Product[], { category?: string }>({
      query: ({ category }) => ({ url: 'products', params: { category } }),
      providesTags: (result) =>
        result
          ? [...result.map(({ id }) => ({ type: 'Product' as const, id })), 'Product']
          : ['Product'],
    }),
    updateProduct: build.mutation<Product, Partial<Product> & { id: string }>({
      query: ({ id, ...body }) => ({ url: `products/${id}`, method: 'PATCH', body }),
      // Optimistic update
      async onQueryStarted({ id, ...patch }, { dispatch, queryFulfilled }) {
        const patchResult = dispatch(
          productsApi.util.updateQueryData('listProducts', {}, (draft) => {
            const product = draft.find((p) => p.id === id);
            if (product) Object.assign(product, patch);
          })
        );
        try { await queryFulfilled; } catch { patchResult.undo(); }
      },
      invalidatesTags: (_r, _e, { id }) => [{ type: 'Product', id }],
    }),
  }),
});

export const { useListProductsQuery, useUpdateProductMutation } = productsApi;
```

RTK Query strengths in 2026: built-in pagination/infinite scroll, streaming cache updates over WebSocket/SSE, experimental OpenAPI/GraphQL code generation, and tag-based invalidation that integrates with `useMutation` automatically.

---

## 8. Signals Convergence (Cross-Framework, 2026)

Solid 2.x, Angular 20 signals, Vue 3.5 (alien-signals refactor) / 3.6 Vapor, Svelte 5 runes, and Preact Signals all share the same primitive model. The **TC39 Signals proposal (Stage 1)** is the lingua-franca target.

| Concept | Solid | Vue 3.5+ | Svelte 5 | Preact | React (via Compiler) |
|---------|-------|----------|----------|--------|----------------------|
| Atomic state | `createSignal()` | `ref()` / `shallowRef()` | `$state()` | `signal()` | `useState()` (auto-memoized) |
| Derived | `createMemo()` | `computed()` | `$derived()` | `computed()` | derived in render (auto-memoized) |
| Effect | `createEffect()` | `watchEffect()` / `watch()` | `$effect()` | `effect()` | `useEffect()` (+ `useEffectEvent`) |

When designing reactive state for code likely to outlive framework choices, model in this primitive form (atomic getter/setter, derived, effect) so migration is mechanical.

> **Solid 2.0 (beta, March 2026):** first-class async (computations can return Promises), reworked Suspense with deterministic batching, self-healing error boundaries, mutable derivations, lazy memos, pull-based SSR.

---

## 9. Anti-Patterns

| # | Anti-pattern | Problem | Fix |
|---|-------------|---------|-----|
| 1 | Server data in Zustand/Redux | Manual cache/sync/dedup reimplementation | Delegate to TanStack Query |
| 2 | Monolithic Context | Unrelated updates re-render all consumers | Split Context by concern |
| 3 | Providers Hell (5+ nested) | Poor readability, hard to debug | Consolidate with Zustand or compose utility |
| 4 | Over-globalizing local state | Modal open/close in global store | Component-level `useState` |
| 5 | `useState` + `useEffect` for URL sync | Sync bugs | nuqs / useSearchParams |
| 6 | Client-only data in RSC era | Ignores server-side benefits | Read in RSC, client stores for interactive parts only |
| 7 | `onSuccess` callbacks in v5 queries | Removed API — silent failures | Move logic to `queryFn` or use `useEffect` on `data` |

**Source:** [TanStack Query v5 Migration](https://tanstack.com/query/latest/docs/framework/react/guides/migrating-to-v5) · [`useSuspenseQuery`](https://tanstack.com/query/latest/docs/framework/react/reference/useSuspenseQuery) · [nuqs Docs](https://nuqs.47ng.com/) · [Announcing Zustand v5](https://pmnd.rs/blog/announcing-zustand-v5/) · [Zustand v5 Migration](https://zustand.docs.pmnd.rs/migrations/migrating-to-v5) · [RTK Query Overview](https://redux-toolkit.js.org/rtk-query/overview) · [Pinia v3 Migration](https://pinia.vuejs.org/cookbook/migration-v2-v3.html) · [Solid 2.0 Beta — InfoQ](https://www.infoq.com/news/2026/05/solidjs-2-async/) · [TC39 Signals Proposal](https://github.com/tc39/proposal-signals) · [Recoil archived (2025-01-01)](https://github.com/facebookexperimental/Recoil)
