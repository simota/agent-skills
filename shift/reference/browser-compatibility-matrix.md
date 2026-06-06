# Browser Compatibility Matrix

Native API browser support reference for migration decisions.

## Modern APIs - Safe to Use

| API | Chrome | Firefox | Safari | Edge | Node.js | Polyfill |
|-----|--------|---------|--------|------|---------|----------|
| `fetch` | 42+ | 39+ | 10.1+ | 14+ | 18+ | node-fetch |
| `Promise` | 32+ | 29+ | 8+ | 12+ | 0.12+ | - |
| `async/await` | 55+ | 52+ | 10.1+ | 15+ | 7.6+ | - |
| `Intl.DateTimeFormat` | 24+ | 29+ | 10+ | 12+ | 13+ | - |
| `Intl.NumberFormat` | 24+ | 29+ | 10+ | 12+ | 13+ | - |
| `IntersectionObserver` | 51+ | 55+ | 12.1+ | 15+ | - | intersection-observer |
| `ResizeObserver` | 64+ | 69+ | 13.1+ | 79+ | - | resize-observer-polyfill |
| `AbortController` | 66+ | 57+ | 11.1+ | 16+ | 15+ | abort-controller |
| `crypto.randomUUID` | 92+ | 95+ | 15.4+ | 92+ | 19+ | uuid |
| `structuredClone` | 98+ | 94+ | 15.4+ | 98+ | 17+ | - |
| `URL` / `URLSearchParams` | 32+ | 29+ | 10+ | 12+ | 7+ | - |

## Modern APIs - Check Support

| API | Chrome | Firefox | Safari | Edge | Node.js | Fallback |
|-----|--------|---------|--------|------|---------|----------|
| `Intl.RelativeTimeFormat` | 71+ | 65+ | 14+ | 79+ | 12+ | relative-time-format |
| `Intl.ListFormat` | 72+ | 78+ | 14.1+ | 79+ | 12+ | - |
| `BroadcastChannel` | 54+ | 38+ | 15.4+ | 79+ | - | broadcast-channel |
| `<dialog>` element | 37+ | 98+ | 15.4+ | 79+ | - | dialog-polyfill |
| `CSS Container Queries` | 105+ | 110+ | 16+ | 105+ | - | - |
| `View Transitions API` | 111+ | ❌ | ❌ | 111+ | - | - |
| `Temporal API` | ❌ | ❌ | ❌ | ❌ | ❌ | @js-temporal/polyfill |

## Baseline Compatibility Targets

```javascript
// browserslist (package.json or .browserslistrc)
// Option 1: Baseline Widely Available (safe)
"browserslist": [
  "last 2 years",
  "> 0.5%",
  "not dead"
]

// Option 2: Modern Only
"browserslist": [
  "last 2 Chrome versions",
  "last 2 Firefox versions",
  "last 2 Safari versions",
  "last 2 Edge versions"
]

// Option 3: With Legacy Support
"browserslist": [
  "> 0.5%",
  "last 2 versions",
  "Firefox ESR",
  "not dead",
  "not IE 11"
]
```

## Migration Decision Tree

```
Is the API in "Safe to Use"?
├── Yes → Use native, no polyfill needed
└── No → Check target browsers
         ├── All targets support → Use native
         ├── Some targets missing → Add polyfill or use library
         └── No targets support → Keep using library
```
