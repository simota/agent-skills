# Web Analysis Checklist (SURVEY phase)

Use this checklist to audit a web codebase before producing any native architecture mapping. Every blueprint section downstream depends on the survey being concrete and grounded in the actual codebase, not assumed.

> **2026-05 baseline assumptions:** React 19.1 (RN 0.80+ ships it); Next.js 15 App Router with Turbopack stable; Vue 3.5+; Svelte 5 (runes); Angular 19+; Nuxt 4. Capacitor 7 (2025-04, Android 15 / iOS 18 + SPM-only iOS) and Tauri 2 mobile (stable 2025-01) are now realistic "web-shell" web→native bridges if pure-native is not chosen.

---

## 1. Stack Detection

| Read | Look for |
|------|----------|
| `package.json` (root + each workspace) | Framework: `react`, `vue`, `svelte`, `@angular/core`, `next`, `nuxt`, `@sveltejs/kit`, `solid-js`, `qwik`, `astro` |
| `package.json` engines / `nvmrc` | Node version baseline |
| `tsconfig.json` | TS strict flags, path aliases |
| `vite.config.*` / `webpack.config.*` / `next.config.*` / `nuxt.config.*` / `svelte.config.*` / `angular.json` | Build target, code splitting strategy, plugins |
| `pnpm-workspace.yaml` / `yarn workspaces` / `turbo.json` / `nx.json` | Monorepo layout |
| `.env*` files (key names only, never values) | Runtime config and feature flags |

**Output:** Framework, version, language (JS/TS), build tool, monorepo layout, Node baseline.

---

## 2. Routing & Rendering

| Detection | What to record |
|-----------|----------------|
| Client-side router | `react-router`, `vue-router`, `@tanstack/router`, Angular Router, SvelteKit / Next.js / Nuxt file-based routing |
| Rendering mode | CSR, SSR, SSG, ISR, RSC (React Server Components), edge SSR |
| Route definitions | Static list of all routes + lazy-loaded boundaries |
| Layouts / nested routes | Layout hierarchy, slot patterns |
| Auth-gated routes | Which routes require auth, redirect targets |
| Dynamic segments | `[id]`, `:slug`, query params semantically used as state |

**Output:** Route inventory (path → component → auth-gating → render-mode), with screen-count.

> **Why this matters:** SPA history-stack semantics do not map 1:1 to iOS `NavigationStack` or Compose `NavHost`. RSC / SSR boundaries collapse on mobile — every route becomes client-driven and pulls data through the API client.

---

## 3. State Management

| Look for | Notes |
|----------|-------|
| Global stores: `redux`, `@reduxjs/toolkit`, `zustand`, `jotai`, `recoil`, `pinia`, `vuex`, `mobx`, `effector`, `@ngrx/store`, `@ngrx/signals`, `@tanstack/store` | Count stores; identify cross-feature coupling |
| Server-state libs: `@tanstack/query`, `swr`, `@apollo/client`, `urql`, `react-query`, `@tanstack/svelte-query` | Server-cache strategy maps to iOS/Android equivalents |
| Form state: `react-hook-form`, `formik`, `vee-validate`, `@tanstack/react-form` | Form complexity per screen |
| Context providers / signals (`useState`, `useReducer`, `signal`, `ref`) | Per-feature local state patterns |
| Persistence middleware: `redux-persist`, `pinia-plugin-persistedstate`, `zustand/persist` | Storage targets, what gets persisted |

**Output:** Store inventory with count, scope (global / feature / local), persistence flag.

---

## 4. Data Layer & API Clients

| Look for | Notes |
|----------|-------|
| HTTP clients: `axios`, `ky`, native `fetch`, generated SDK clients | Base URL, interceptors, retry logic, auth header injection |
| GraphQL: `@apollo/client`, `urql`, `relay`, `graphql-request`, generated hooks | Schema location, persisted queries, normalized cache |
| WebSocket / SSE: `socket.io-client`, native `EventSource`, custom WS | Connection lifecycle, reconnection strategy |
| File upload | Multipart, presigned URL, chunked, resumable |
| Pagination patterns | Cursor, offset, infinite scroll, polling |
| Caching: `swr`, `react-query`, browser HTTP cache, service worker | TTLs, invalidation rules |
| Real-time: Firestore, Supabase Realtime, Pusher, Ably | Subscription model, fan-out scope |

**Output:** API surface (endpoints + payloads + auth), real-time channels, upload flows, pagination patterns. Flag mobile-unfriendly endpoints (chatty, large payloads, no pagination).

---

## 5. Storage Usage

| Mechanism | Sensitivity | Native equivalent (preview) |
|-----------|-------------|----------------------------|
| `localStorage` | Plaintext, persistent | UserDefaults (iOS, non-secret) / DataStore (Android, non-secret) |
| `sessionStorage` | Plaintext, tab-scoped | In-memory state only |
| `cookies` (HTTP-only) | Server-managed | Translate to token-in-Keychain / EncryptedSharedPreferences |
| `cookies` (JS-readable) | Mixed | **Never reuse**; redesign as token storage |
| `IndexedDB` | Plaintext (queryable) | Core Data / SwiftData (iOS), Room (Android) |
| `Cache API` / Service Worker | HTTP responses | URLCache / OkHttp cache, plus Tier-T1+ for offline |
| `WebSQL` | Deprecated | Treat same as IndexedDB |
| `BroadcastChannel` / `SharedWorker` | Cross-tab | Not portable; redesign as in-process eventing |

**Output:** Storage inventory with classification: secret / personal / cache / preference. Each row maps to a native target in `data-and-auth-porting.md`.

---

## 6. Auth Flow

| Check | Capture |
|-------|---------|
| Auth provider | Auth0, Cognito, Firebase Auth, Supabase Auth, Clerk, NextAuth/Auth.js, custom |
| Identity flow | Email/password, OAuth (which providers), OIDC, SAML, magic link, passkey |
| Token model | Session cookie, JWT (where stored), refresh token (where stored), token rotation |
| MFA / 2FA | TOTP, SMS, push approval, WebAuthn |
| Session lifecycle | Idle timeout, sliding session, server-revoked logout |
| SSO | Same-domain shared session, federation |
| Sensitive flows | Password reset, account deletion, email change, payment |

**Output:** Auth flow diagram (textual is fine), with token-storage location and lifecycle.

> **Critical:** If auth uses `localStorage`-stored JWT, this **must** move to Keychain / EncryptedSharedPreferences in the port. Never replicate insecure web patterns.

---

## 7. Third-Party SDKs and Web-Only APIs

For every dependency in `package.json` or external `<script>` tag, classify:

| Class | Examples | Native action |
|-------|----------|---------------|
| Has native SDK | Stripe, Sentry, Mixpanel, Amplitude, Segment, Firebase, OneSignal, Auth0 | Map to native SDK; verify min-OS support |
| Web-only with REST API | Many analytics/marketing tools | Replace with native SDK if available; otherwise direct REST calls |
| Web-only and no native path | Some embed widgets, browser-only libs | Flag as risk: redesign or drop feature |
| Browser API direct | `navigator.geolocation`, `navigator.mediaDevices`, `navigator.bluetooth`, `WebRTC`, `WebUSB`, `WebGL`, `Web Audio API`, `Web Share API`, Service Worker, Push API, `BroadcastChannel`, `File System Access API` | Map to platform equivalent; some have no Android/iOS equivalent |

**Output:** SDK / Web-API inventory with native-mapping verdict per row. Any "no native path" entry is a parity-matrix risk.

---

## 8. Build, Bundle, and Performance

| Check | Notes |
|-------|-------|
| Total bundle size | Initial + per-route chunks |
| Lazy boundaries | Count of `import()` / dynamic-route splits |
| Tree-shaking effectiveness | Unused exports, side-effect imports |
| Asset pipeline | Images (responsive, formats), fonts (woff2, subset), icons (SVG sprites) |
| i18n | Locale count, library (`react-i18next`, `vue-i18n`, `next-intl`), RTL support |
| a11y baseline | aria-\*, focus management, keyboard nav, axe report |
| PWA features | Service worker, manifest, install prompt, push, background sync |

**Output:** Performance budget data (cold load, FID/INP), lazy-route count (informs feature modules), i18n locale list, a11y baseline.

---

## 9. Domain Logic Concentration

For each major feature, identify where the business rules live:

- Pure functions in `lib/` / `utils/` / `domain/` → strong KMP candidates
- Hooks / composables / pinia stores → mostly UI-coupled, do not port logic directly
- Backend-only rules → do not touch in port
- Form validation → re-implement in native validation layer

**Output:** "Pure logic" inventory — rules that could be reused via Kotlin Multiplatform if hybrid is on the table. (Even if pure-native is the chosen path, this list helps the implementer understand which rules to mirror exactly.)

---

## 10. Web-Native Capability Gaps

Identify web features that have **no direct native counterpart** and must be re-conceived:

- Print-to-PDF (web `window.print()`)
- Browser file picker behavior (vs platform document picker)
- Right-click context menus
- Drag-and-drop with HTML5 DnD API
- Browser back-button semantics inside an SPA flow
- Multi-window / popup workflows
- URL-as-state-handle (deep state in querystring)
- Cross-tab synchronization
- Browser extension integration

Each becomes a parity-matrix entry with a verdict (`Adapted` to platform-native UX, or `Dropped`).

---

## SURVEY Output Skeleton

```markdown
# Web Survey: <App Name>

## Stack
- Framework / version: …
- Language: …
- Build tool: …
- Monorepo layout: …

## Routing
- Route count: N (auth-gated: M)
- Render modes: CSR=N SSR=N SSG=N RSC=N
- Top-level layouts: …

## State
- Global stores: …
- Server-state lib: …
- Persistence: …

## Data
- API style: REST / GraphQL / mixed
- Real-time: …
- Pagination patterns: …
- Mobile-unfriendly endpoints: [list]

## Storage
- Secret data targets: …
- Personal data targets: …
- Cache targets: …

## Auth
- Provider: …
- Flow: …
- Token storage: …
- Sensitive flows: …

## Third-party SDKs
| SDK | Native SDK? | Min-OS | Verdict |
| …   | …           | …      | …       |

## Web-only API usage
| API | Native equivalent | Verdict |
| …   | …                 | …       |

## Domain logic concentration
- Pure modules: …
- UI-coupled rules: …

## Capability gaps (web-only)
- …

## Pre-MAP risks
- …
```

This survey is the input to `MAP`. Do not skip ahead.
