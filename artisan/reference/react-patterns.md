# React Patterns & Server Components

Production-quality React patterns: components, hooks, error boundaries, React 19 hooks, React Compiler, RSC, Server Actions, and form handling.

---

## 1. Component Structure

### Compound Component Pattern

```tsx
interface CardProps {
  children: React.ReactNode;
  className?: string;
}

interface CardComponent extends React.FC<CardProps> {
  Header: typeof CardHeader;
  Body: typeof CardBody;
  Footer: typeof CardFooter;
}

const Card: CardComponent = ({ children, className }) => (
  <div className={cn("rounded-lg border", className)}>{children}</div>
);

const CardHeader: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="border-b p-4 font-semibold">{children}</div>
);

const CardBody: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="p-4">{children}</div>
);

const CardFooter: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="border-t p-4">{children}</div>
);

Card.Header = CardHeader;
Card.Body = CardBody;
Card.Footer = CardFooter;
```

---

## 2. Custom Hooks

```tsx
function useAsync<T>(asyncFn: () => Promise<T>, deps: unknown[] = []) {
  const [state, setState] = useState<{
    data: T | null;
    error: Error | null;
    isLoading: boolean;
  }>({ data: null, error: null, isLoading: true });

  useEffect(() => {
    let cancelled = false;
    setState(prev => ({ ...prev, isLoading: true }));
    asyncFn()
      .then(data => { if (!cancelled) setState({ data, error: null, isLoading: false }); })
      .catch(error => { if (!cancelled) setState({ data: null, error, isLoading: false }); });
    return () => { cancelled = true; };
  }, deps);

  return state;
}
```

---

## 3. Error Boundaries

```tsx
class ErrorBoundary extends React.Component<
  { fallback: React.ReactNode; children: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };
  static getDerivedStateFromError() { return { hasError: true }; }
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }
  render() {
    return this.state.hasError ? this.props.fallback : this.props.children;
  }
}
```

---

## 4. React 19 Hooks

### useActionState

```tsx
import { useActionState } from 'react';

function ContactForm() {
  const [state, formAction] = useActionState(
    async (prevState, formData: FormData) => {
      const name = formData.get('name') as string;
      const res = await submitContact({ name });
      if (!res.ok) return { error: 'Failed to submit' };
      return { success: true, message: `Thanks ${name}!` };
    },
    {}
  );

  return (
    <form action={formAction}>
      <input name="name" required />
      <SubmitButton />
      {state.error && <p role="alert">{state.error}</p>}
      {state.success && <p>{state.message}</p>}
    </form>
  );
}
```

### useFormStatus

```tsx
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}
```

### useOptimistic

```tsx
import { useOptimistic } from 'react';

function TodoList({ todos, addTodoAction }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo) => [...state, { ...newTodo, pending: true }]
  );

  return (
    <form action={async (formData) => {
      addOptimisticTodo({ text: formData.get('text'), id: crypto.randomUUID() });
      await addTodoAction(formData);
    }}>
      {optimisticTodos.map(todo => (
        <li key={todo.id} style={{ opacity: todo.pending ? 0.5 : 1 }}>{todo.text}</li>
      ))}
      <input name="text" />
      <button type="submit">Add</button>
    </form>
  );
}
```

### use()

Promise or Context in render. Can be called conditionally (exception to Rules of Hooks).

```tsx
import { use, Suspense } from 'react';

function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);
  return <h1>{user.name}</h1>;
}

function ThemeText({ showTheme }: { showTheme: boolean }) {
  if (showTheme) {
    const theme = use(ThemeContext); // OK inside conditional
    return <p>Current theme: {theme}</p>;
  }
  return <p>Theme hidden</p>;
}
```

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

```tsx
// useEffectEvent — see latest props/state without re-subscribing
function ChatRoom({ roomId, theme }: { roomId: string; theme: string }) {
  const onConnected = useEffectEvent(() => {
    showNotification('Connected!', theme); // always sees latest theme
  });

  useEffect(() => {
    const connection = createConnection(serverUrl, roomId);
    connection.on('connected', onConnected);
    connection.connect();
    return () => connection.disconnect();
  }, [roomId]); // theme intentionally omitted — onConnected captures it
}

// Activity — preserve state without rendering cost
<Activity mode={isVisible ? 'visible' : 'hidden'}>
  <ExpensivePage />
</Activity>

// cacheSignal — abort deduped fetch when render unwinds
import { cache, cacheSignal } from 'react';
const dedupedFetch = cache(fetch);
async function Component() {
  const res = await dedupedFetch(url, { signal: cacheSignal() });
  // ...
}
```

> **Security:** CVE-2025-55182 (React2Shell, CVSS 10.0) affects 19.0.0, 19.1.0–19.1.1, and 19.2.0 — unauthenticated RCE via unsafe deserialization in Server Actions. Pin to 19.0.1+, 19.1.2+, or 19.2.1+ (Next.js 15.1.4+ / 16+).

---

## 6. React Compiler (v1.0 Stable — October 2025)

Auto-memoization for components and hooks. No manual `useMemo`/`useCallback`/`React.memo` needed. Battle-tested in Meta production (Quest Store saw +12% initial load, 2.5× faster interactions).

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

**Install:**
```bash
npm i -D --save-exact babel-plugin-react-compiler@latest
npm i -D eslint-plugin-react-hooks@latest  # also enables compiler-powered lints
```

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

### Composition: Push `'use client'` to Leaves

```tsx
// Bad: top-level 'use client' — all children become Client Components
'use client';
export function Layout() {
  const [isOpen, setIsOpen] = useState(false);
  return <ServerHeavyComponent />; // loses server execution
}

// Good: Composition pattern — pass Server Component as children
'use client';
export function InteractiveShell({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  return <div>{children}</div>;
}

// page.tsx (Server Component)
export default function Page() {
  return (
    <InteractiveShell>
      <ServerHeavyComponent /> {/* runs on server */}
    </InteractiveShell>
  );
}
```

### When to Use Client Components

| Condition | Server | Client |
|-----------|:---:|:---:|
| DB/API direct access | ✅ | — |
| Display-only (props) | ✅ | — |
| `onClick`/`onChange` handlers | — | ✅ |
| `useState`/`useEffect` | — | ✅ |
| Browser APIs (localStorage) | — | ✅ |

### Suspense Streaming

```tsx
// Bad: top-level await blocks entire shell
export default async function Home() {
  const analytics = await getAnalytics(); // slow
  return <div><Header /><AnalyticsWidget data={analytics} /></div>;
}

// Good: Suspense sends shell immediately, streams slow parts
export default function Home() {
  return (
    <div>
      <Header />
      <Suspense fallback={<AnalyticsSkeleton />}>
        <AnalyticsWidget />
      </Suspense>
    </div>
  );
}

async function AnalyticsWidget() {
  const data = await getAnalytics(); // blocks only within Suspense
  return <Dashboard data={data} />;
}
```

---

## 8. Server Actions

```tsx
// app/actions.ts
'use server';
import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const TodoSchema = z.object({
  title: z.string().min(1, 'Title is required'),
});

export async function createTodo(prevState: any, formData: FormData) {
  const result = TodoSchema.safeParse({ title: formData.get('title') });
  if (!result.success) return { errors: result.error.flatten().fieldErrors };
  await db.todo.create({ data: result.data });
  revalidatePath('/todos');
  return { success: true };
}
```

### Server Actions vs Route Handlers

| Use case | Server Actions | Route Handlers |
|----------|:---:|:---:|
| Form mutations | ✅ | — |
| UI data changes | ✅ | — |
| Public API / Webhooks | — | ✅ |
| Large file uploads | — | ✅ |
| External service calls | — | ✅ |

### Cache & Revalidation (Next.js 15)

```tsx
const data = await fetch(url, { cache: 'force-cache' });         // static (build-time)
const data = await fetch(url, { cache: 'no-store' });            // dynamic (per-request)
const data = await fetch(url, { next: { revalidate: 3600 } });   // time-based (ISR)
const data = await fetch(url, { next: { tags: ['products'] } }); // tag-based
// After mutation:
revalidateTag('products');
```

### Next.js 16 — Cache Components + new cache APIs (October 2025)

Next.js 16 flipped from implicit caching to **explicit, opt-in caching** via Cache Components. All dynamic code in pages/layouts/API routes runs at request time by default; cacheable surfaces are marked with `"use cache"`.

```ts
// next.config.ts
const nextConfig = { cacheComponents: true, reactCompiler: true };
export default nextConfig;
```

```tsx
// File-, component-, or function-level cache directive
"use cache";
export default async function ProductList() {
  const products = await db.products.findMany();
  return <ul>{/* ... */}</ul>;
}
```

| API | Runtime | Behavior |
|-----|---------|----------|
| `revalidateTag(tag, profile)` | Anywhere | SWR semantics; **profile arg is now required** (e.g. `'max'`, `'hours'`, `'days'`, or `{ expire: 3600 }`). Single-arg form is deprecated. |
| `updateTag(tag)` | Server Actions only | Read-your-writes — invalidates and reads fresh data in the same request. Use for forms/settings where users must see their change. |
| `refresh()` | Server Actions only | Refreshes **uncached** data only; does not touch cache. Complement to client `router.refresh()`. |

Other Next.js 16 changes that affect Artisan implementations:
- `middleware.ts` → **`proxy.ts`** (Node.js runtime; old name deprecated).
- `params` / `searchParams` props and `cookies()` / `headers()` / `draftMode()` are now **async** — `await` is required.
- `experimental.ppr` and `experimental.dynamicIO` flags removed; PPR is now integrated into Cache Components.
- Turbopack is the **default bundler**; opt out with `next dev --webpack` / `next build --webpack`.
- Min Node.js 20.9, TypeScript 5.1, Chrome 111+/Edge 111+/Firefox 111+/Safari 16.4+.

### Next.js 16.2 (March 18, 2026)

Key improvements that affect day-to-day Artisan work:

| Feature | Impact |
|---------|--------|
| **Server Fast Refresh** | Fine-grained server-side hot reloading — RSC tree is patched without full reload |
| **Adapter API (stable)** | Typed, versioned output description; deploy to Cloudflare/Netlify/Vercel/AWS without vendor lock-in |
| **Turbopack filesystem caching** | Compiler artifacts persisted across restarts; large projects see 400–900% faster compile after first build |
| **React Compiler stable** | `reactCompiler: true` in `next.config.ts` is now stable (was experimental in 16.0) |
| **AGENTS.md in `create-next-app`** | Auto-generated AI agent context file with version-matched Next.js docs |
| **Hydration Diff Indicator** | Clear server/client diff in error overlay — reduces debugging time for RSC mismatches |

[Source: nextjs.org/blog/next-16-2](https://nextjs.org/blog/next-16-2) · [nextjs.org/blog/next-16-2-turbopack](https://nextjs.org/blog/next-16-2-turbopack)

---

## 9. Form Handling Selection Guide

TanStack Form reached **v1 stable** (March 2025). Supports React, Vue, Angular, Solid, and Lit with type-safe field paths — misspelled field names are compiler errors. [Source: tanstack.com/blog/announcing-tanstack-form-v1](https://tanstack.com/blog/announcing-tanstack-form-v1)

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

[Source: zod.dev/v4](https://zod.dev/v4) · [Zod v4 — InfoQ Aug 2025](https://www.infoq.com/news/2025/08/zod-v4-available/) · [Valibot vs Zod v4 — pkgpulse.com](https://www.pkgpulse.com/guides/valibot-vs-zod-v4-typescript-validator-2026)

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
