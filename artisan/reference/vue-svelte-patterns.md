# Vue 3 & Svelte 5 Patterns

Production-quality patterns for Vue 3.5+/3.6 Composition API (including Vapor Mode), Svelte 5 Runes, SvelteKit 2 remote functions, and Nuxt 4.

---

## Vue 3 Composition API

### Component with Props, Emits, and Reactivity

```vue
<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';

interface Props {
  userId: string;
  initialName?: string;
}

const props = withDefaults(defineProps<Props>(), {
  initialName: '',
});

const emit = defineEmits<{
  (e: 'update', value: string): void;
  (e: 'submit'): void;
}>();

const name = ref(props.initialName);
const isLoading = ref(false);
const isValid = computed(() => name.value.length >= 3);

watch(name, (newValue) => { emit('update', newValue); });

onMounted(async () => {
  isLoading.value = true;
  // fetch data...
  isLoading.value = false;
});

const handleSubmit = () => { if (isValid.value) emit('submit'); };
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <input v-model="name" :disabled="isLoading" />
    <button type="submit" :disabled="!isValid">Submit</button>
  </form>
</template>
```

---

## Vue 3.5 "Tengu" (September 2024)

### Reactive Props Destructure (Stable)

```vue
<script setup lang="ts">
// Vue 3.5+: destructured props are reactive — withDefaults deprecated for this pattern
const { userId, count = 0, title = 'Default' } = defineProps<{
  userId: string;
  count?: number;
  title?: string;
}>();

// `count` and `title` are reactive with defaults
// No need for withDefaults() when using destructure
const doubled = computed(() => count * 2);
</script>
```

### useTemplateRef

```vue
<script setup lang="ts">
import { useTemplateRef, onMounted } from 'vue';

// Type-safe template ref (replaces string-based ref())
const inputRef = useTemplateRef<HTMLInputElement>('input');

onMounted(() => {
  inputRef.value?.focus();
});
</script>

<template>
  <input ref="input" />
</template>
```

### useId

```vue
<script setup lang="ts">
import { useId } from 'vue';

// SSR-stable unique IDs (like React useId)
const id = useId();
</script>

<template>
  <label :for="id">Email</label>
  <input :id="id" type="email" />
</template>
```

### Lazy Hydration (SSR)

```vue
<script setup>
import { defineAsyncComponent, hydrateOnVisible, hydrateOnIdle, hydrateOnInteraction } from 'vue';

// Hydrate when element becomes visible
const HeavyChart = defineAsyncComponent({
  loader: () => import('./HeavyChart.vue'),
  hydrate: hydrateOnVisible(),
});

// Hydrate during idle time
const Analytics = defineAsyncComponent({
  loader: () => import('./Analytics.vue'),
  hydrate: hydrateOnIdle(2000), // timeout: 2s
});

// Hydrate on user interaction
const CommentSection = defineAsyncComponent({
  loader: () => import('./CommentSection.vue'),
  hydrate: hydrateOnInteraction(['click', 'focus']),
});
</script>
```

### Other 3.5 Improvements

| Feature | Details |
|---------|---------|
| `onWatcherCleanup()` | Cleanup function for `watch`/`watchEffect` — replaces `onCleanup` parameter |
| Reactive `v-bind` memory | ~56% reduction in memory usage |
| Deferred Teleport | `<Teleport defer>` — renders target after current update cycle |

---

## Vue 3.6 "Vapor Mode" (Beta — Q2 2026)

Vue 3.6 is in beta (v3.6.0-beta.x as of May 2026) with a major refactor of `@vue/reactivity` based on **alien-signals**. The headline feature is **Vapor Mode** — an opt-in compile-to-DOM strategy that **eliminates the virtual DOM** for components that enable it.

```vue
<script setup vapor lang="ts">
// Add the `vapor` attribute to <script setup> to opt into Vapor Mode
// Component is compiled to direct DOM operations — no VDOM diff
import { ref } from 'vue';

const count = ref(0);
</script>

<template>
  <button @click="count++">Count: {{ count }}</button>
</template>
```

**Status & rules:**
- **Feature-complete with VDOM mode**, but officially **unstable** — recommended for "partial usage in existing apps" or "small new apps." **Not production-stable yet.**
- Performance: parity with Solid.js and Svelte 5 in JS-Framework-Benchmark (mounts 100k components in ~100ms).
- `<script setup>` only — Options API is **not supported** in Vapor components.
- Not supported in Vapor: `getCurrentInstance()`, lifecycle events you can subscribe to from outside, global properties.
- Custom directives use a modified interface requiring reactive getters.
- **Opt-in per-component**: mix Vapor and VDOM components freely in the same app.
- **Roadmap (Vue team estimates):** Q3 2026 — Transition/KeepAlive compat; Q4 2026 — possible stable release; 2027 — possible default mode.

### Reactivity Refactor (3.6 — applies to all components)

The `@vue/reactivity` core was rewritten on top of alien-signals, delivering further memory and CPU wins across all 3.6 apps even without Vapor Mode. No code changes required — existing 3.5 code runs faster.

---

## Vue Composables (Custom Hooks)

```typescript
// composables/useAsync.ts
import { ref, type Ref } from 'vue';

export function useAsync<T>(asyncFn: () => Promise<T>): {
  data: Ref<T | null>; error: Ref<Error | null>;
  isLoading: Ref<boolean>; execute: () => Promise<void>;
} {
  const data = ref<T | null>(null) as Ref<T | null>;
  const error = ref<Error | null>(null);
  const isLoading = ref(false);

  const execute = async () => {
    isLoading.value = true;
    error.value = null;
    try { data.value = await asyncFn(); }
    catch (e) { error.value = e instanceof Error ? e : new Error(String(e)); }
    finally { isLoading.value = false; }
  };

  return { data, error, isLoading, execute };
}
```

---

## Pinia Store (v3 — Vue 3 only)

Pinia 3.0 (released 2025) is a "boring" major — no new features, drops legacy deprecated APIs. Object-form `defineStore({ id: ... })` is **removed**; use string-id form. Requires Vue 3 and TypeScript 5+.

```typescript
import { defineStore } from 'pinia';

// Option Store
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false,
  }),
  getters: {
    userName: (state) => state.user?.name ?? 'Guest',
  },
  actions: {
    async login(email: string, password: string) {
      const user = await authApi.login(email, password);
      this.user = user;
      this.isAuthenticated = true;
    },
    logout() {
      this.user = null;
      this.isAuthenticated = false;
    },
  },
});

// Setup Store (composition style — preferred for new code)
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useCounter = defineStore('counter', () => {
  const count = ref(0);
  const doubled = computed(() => count.value * 2);
  function increment() { count.value++; }
  return { count, doubled, increment };
});
```

**Pinia Colada** (companion async data layer, first stable release early 2026) handles server state — fetching, dedup, cache invalidation — concerns Pinia core intentionally leaves out of scope. Treat it as Vue's parallel to TanStack Query.

---

## Nuxt 4 (Released 2025-07)

Nuxt 4 is a stability-focused release. Most changes were already opt-in via `compatibilityVersion: 4` in Nuxt 3.

### `app/` Directory (biggest structural change)

```
my-nuxt-app/
├── app/              # NEW — all client + app code lives here
│   ├── pages/
│   ├── components/
│   ├── composables/
│   └── app.vue
├── server/           # server-only (API routes, middleware)
├── shared/           # code usable from both app/ and server/
├── public/
└── nuxt.config.ts
```

- Improves file-watcher performance (no longer watches `node_modules`/`.git`).
- Gives IDE clearer client vs. server context.
- Flat (Nuxt 3) structure still works if you prefer.

### Other key Nuxt 4 features

| Feature | Details |
|---------|---------|
| Smart data fetching | Multiple components calling `useFetch`/`useAsyncData` with the same key **share data automatically**; cache cleans up on unmount |
| Per-context tsconfig | Separate TS projects auto-generated for app / server / shared / builder — better autocomplete and type isolation. Still only **one `tsconfig.json`** at the project root |
| Faster CLI | Node.js compile caching, native file watching, socket-based CLI ↔ Vite communication |
| `vue-router` v5 | First major upgrade since Nuxt 3 |

**Breaking changes:** removed Nuxt 2 compat from `@nuxt/kit` (module-author impact), cleaned-up legacy utilities, new TS setup may surface previously hidden type issues. Nuxt 3 receives maintenance support through **July 2026**. **Nuxt 5** (Nitro v3 + h3 v2 + Vite Environment API) is the next major.

```bash
npx nuxt upgrade --dedupe   # safest upgrade path
```

---

## Svelte 5 Runes (Stable — October 2024)

### Component with $state, $derived, $effect

```svelte
<script lang="ts">
  interface Props {
    userId: string;
    initialCount?: number;
  }

  let { userId, initialCount = 0 }: Props = $props();

  let count = $state(initialCount);
  let name = $state('');
  let doubled = $derived(count * 2);
  let isValid = $derived(name.length >= 3);

  $effect(() => {
    console.log(`Count changed to ${count}`);
    return () => { console.log('Cleanup'); };
  });

  function increment() { count++; }
  function handleSubmit() { if (isValid) { /* submit */ } }
</script>

<div>
  <p>Count: {count} (doubled: {doubled})</p>
  <button onclick={increment}>Increment</button>

  <form onsubmit={handleSubmit}>
    <input bind:value={name} />
    <button type="submit" disabled={!isValid}>Submit</button>
  </form>
</div>
```

### Svelte 5 Migration Guide

| Svelte 4 | Svelte 5 | Notes |
|-----------|----------|-------|
| `export let prop` | `let { prop } = $props()` | Props via Runes |
| `$:` reactive | `$derived()` / `$effect()` | Explicit reactivity |
| `<slot>` | `{@render children()}` with Snippets | Type-safe composition |
| `on:click={handler}` | `onclick={handler}` | Standard DOM event attributes |
| `createEventDispatcher()` | Callback props | Pass functions as props |
| Stores (`$store`) | `$state` + context | Runes replace most store patterns |

### $bindable (Two-Way Binding)

```svelte
<script lang="ts">
  // Child component with bindable prop
  let { value = $bindable('') }: { value: string } = $props();
</script>

<input bind:value={value} />

<!-- Parent usage -->
<script lang="ts">
  let searchQuery = $state('');
</script>
<SearchInput bind:value={searchQuery} />
```

### $state.raw (Large Data)

```svelte
<script lang="ts">
  // Skip deep reactivity for large, immutable datasets
  let items = $state.raw<Item[]>([]);

  async function loadItems() {
    const data = await fetchItems();
    items = data; // Replace entire array (no deep proxy overhead)
  }
</script>
```

### Snippets (Replacing Slots)

```svelte
<!-- Card.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    title: string;
    children: Snippet;
    footer?: Snippet;
  }

  let { title, children, footer }: Props = $props();
</script>

<div class="card">
  <header><h2>{title}</h2></header>
  <div class="card-body">{@render children()}</div>
  {#if footer}
    <footer>{@render footer()}</footer>
  {/if}
</div>

<!-- Usage -->
<Card title="My Card">
  <p>Card content</p>
  {#snippet footer()}
    <button>Action</button>
  {/snippet}
</Card>
```

### SvelteKit $app/state (2.12+)

```svelte
<script>
  import { page } from '$app/state';

  // Reactive access to page data (replaces $app/stores)
  // No need for $page store subscription
  const currentPath = $derived(page.url.pathname);
</script>

<nav>
  <a href="/" class:active={currentPath === '/'}>Home</a>
</nav>
```

### SvelteKit 2.50+ — Remote Functions (Experimental → Stabilizing 2026)

Type-safe RPC between client and server, defined as functions in `.remote.ts` files. Four variants — `query` (data), `form` (progressive-enhanced submit), `command` (JS-required mutation), `prerender` (build-time static).

```ts
// src/routes/todos.remote.ts
import { query, form, command, getRequestEvent } from '$app/server';
import { db } from '$lib/server/db';
import { z } from 'zod';

export const getTodos = query(async () => {
  return db.todo.findMany();
});

export const addTodo = form(
  z.object({ title: z.string().min(1) }),
  async ({ title }) => {
    await db.todo.create({ data: { title } });
    await getTodos().refresh(); // server permission required (2026 hardening)
  }
);

export const deleteTodo = command(z.string(), async (id) => {
  await db.todo.delete({ where: { id } });
});
```

```svelte
<!-- src/routes/+page.svelte -->
<script lang="ts">
  import { getTodos, addTodo, deleteTodo } from './todos.remote';

  const todos = getTodos();
</script>

<form {...addTodo}>
  <input name="title" {...addTodo.fields.title.as('text')} />
  <button {...addTodo.fields.action.as('submit', 'create')}>Add</button>
</form>

{#await todos then list}
  {#each list as t (t.id)}
    <li>{t.title} <button onclick={() => deleteTodo(t.id)}>×</button></li>
  {/each}
{/await}
```

**2026 hardening (kit@2.50+):**
- Client-requested query `refresh()` now requires explicit server permission.
- Caching keys are sorted for stable dedup.
- Queries restricted to render contexts (no calls from arbitrary client code).
- `field.as(type, value)` for default values; `buttonProps` removed — use `{...form.fields.action.as('submit', 'value')}` for multi-submit forms.
- TypeScript **6.0** supported as of May 2026.

---

## Vue Performance Hints

### v-memo

```vue
<template>
  <!-- Only re-render rows where selection changed -->
  <div v-for="item in items" :key="item.id" v-memo="[item.id === selectedId]">
    <ItemComponent :item="item" :selected="item.id === selectedId" />
  </div>
</template>
```

Use for: large lists (100+ rows), selection toggling, table row highlighting. `v-memo="[]"` equals `v-once`.

### markRaw

```ts
import { markRaw, ref } from 'vue';

// Skip reactivity for large third-party objects
const map = ref(markRaw(new MapLibreGL.Map({ /* ... */ })));
const chart = markRaw(new Chart(canvas, config));
const editor = markRaw(new Monaco.Editor(container));
```

Use for: map libraries, chart libraries, editor instances, immutable config objects.

**Source:** [Vue 3.5 Blog](https://blog.vuejs.org/posts/vue-3-5) · [Vue 3.6 Beta Release](https://github.com/vuejs/core/releases/tag/v3.6.0-beta.1) · [Vue Composition API](https://vuejs.org/guide/extras/composition-api-faq) · [Svelte 5 Docs](https://svelte.dev/docs/svelte) · [Svelte 5 Migration Guide](https://svelte.dev/docs/svelte/v5-migration-guide) · [SvelteKit Remote Functions](https://svelte.dev/docs/kit/remote-functions) · [SvelteKit $app/state](https://svelte.dev/docs/kit/$app-state) · [What's new in Svelte May 2026](https://svelte.dev/blog/whats-new-in-svelte-may-2026) · [Pinia v3 Migration](https://pinia.vuejs.org/cookbook/migration-v2-v3.html) · [Nuxt 4 Release](https://nuxt.com/blog/v4)
