# Vue 3 & Svelte 5 Patterns
---
## Vue 3.5 "Tengu" (September 2024)
- **Reactive Props Destructure (Stable)**
- **useTemplateRef**
- **useId**
- **Lazy Hydration (SSR)**
### Other 3.5 Improvements
| Feature | Details |
|---------|---------|
| `onWatcherCleanup()` | Cleanup function for `watch`/`watchEffect` — replaces `onCleanup` parameter |
| Reactive `v-bind` memory | ~56% reduction in memory usage |
| Deferred Teleport | `<Teleport defer>` — renders target after current update cycle |
---
## Vue 3.6 "Vapor Mode" (Beta — Q2 2026)
**Status & rules:**
- **Feature-complete with VDOM mode**, but officially **unstable** — recommended for "partial usage in existing apps" or "small new apps." **Not production-stable yet.**
- Performance: parity with Solid.js and Svelte 5 in JS-Framework-Benchmark (mounts 100k components in ~100ms).
- `<script setup>` only — Options API is **not supported** in Vapor components.
- Not supported in Vapor: `getCurrentInstance()`, lifecycle events you can subscribe to from outside, global properties.
- Custom directives use a modified interface requiring reactive getters.
- **Opt-in per-component**: mix Vapor and VDOM components freely in the same app.
- **Roadmap (Vue team estimates):** Q3 2026 — Transition/KeepAlive compat; Q4 2026 — possible stable release; 2027 — possible default mode.
- **Reactivity Refactor (3.6 — applies to all components)**
---
## Nuxt 4 (Released 2025-07)
### `app/` Directory (biggest structural change)
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
---
## Svelte 5 Runes (Stable — October 2024)
- **Component with $state, $derived, $effect**
### Svelte 5 Migration Guide
| Svelte 4 | Svelte 5 | Notes |
|-----------|----------|-------|
| `export let prop` | `let { prop } = $props()` | Props via Runes |
| `$:` reactive | `$derived()` / `$effect()` | Explicit reactivity |
| `<slot>` | `{@render children()}` with Snippets | Type-safe composition |
| `on:click={handler}` | `onclick={handler}` | Standard DOM event attributes |
| `createEventDispatcher()` | Callback props | Pass functions as props |
| Stores (`$store`) | `$state` + context | Runes replace most store patterns |
- **$bindable (Two-Way Binding)**
- **$state.raw (Large Data)**
- **Snippets (Replacing Slots)**
- **SvelteKit $app/state (2.12+)**
### SvelteKit 2.50+ — Remote Functions (Experimental → Stabilizing 2026)
**2026 hardening (kit@2.50+):**
- Client-requested query `refresh()` now requires explicit server permission.
- Caching keys are sorted for stable dedup.
- Queries restricted to render contexts (no calls from arbitrary client code).
- `field.as(type, value)` for default values; `buttonProps` removed — use `{...form.fields.action.as('submit', 'value')}` for multi-submit forms.
- TypeScript **6.0** supported as of May 2026.
---
## Vue Performance Hints
- **v-memo**
### markRaw
**Source:** [Vue 3.5 Blog](https://blog.vuejs.org/posts/vue-3-5) · [Vue 3.6 Beta Release](https://github.com/vuejs/core/releases/tag/v3.6.0-beta.1) · [Vue Composition API](https://vuejs.org/guide/extras/composition-api-faq) · [Svelte 5 Docs](https://svelte.dev/docs/svelte) · [Svelte 5 Migration Guide](https://svelte.dev/docs/svelte/v5-migration-guide) · [SvelteKit Remote Functions](https://svelte.dev/docs/kit/remote-functions) · [SvelteKit $app/state](https://svelte.dev/docs/kit/$app-state) · [What's new in Svelte May 2026](https://svelte.dev/blog/whats-new-in-svelte-may-2026) · [Pinia v3 Migration](https://pinia.vuejs.org/cookbook/migration-v2-v3.html) · [Nuxt 4 Release](https://nuxt.com/blog/v4)
