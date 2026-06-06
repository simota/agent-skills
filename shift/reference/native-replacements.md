# Common Native Replacements

Snapshot of mainstream library → native API replacements (verified 2026-05). "Since" refers to first stable availability in the dominant runtime (browser baseline or Node.js LTS). Always confirm with caniuse / `node --version` against the target environment.

| Library | Native Alternative | Since |
|---------|-------------------|-------|
| moment.js / moment-timezone | `Temporal` (Stage 4, ES2026) + `Intl.DateTimeFormat` | Chrome/Edge 144 (2026-01), Firefox 139 (2025-05); Safari TP only — use `@js-temporal/polyfill` until Safari ships [TC39](https://tc39.es/proposal-temporal/) |
| lodash.get | Optional chaining (`?.`) | ES2020 (all evergreen browsers, Node 14+) |
| lodash.cloneDeep | `structuredClone()` | Node 17+, Chrome 98, Firefox 94, Safari 15.4 |
| lodash.groupBy | `Object.groupBy()` / `Map.groupBy()` | Baseline 2024 — Chrome 117, Firefox 119, Safari 17.4, Node 20.12+ |
| lodash set ops (union/intersection/difference) | `Set.prototype.union`/`.intersection`/`.difference`/`.symmetricDifference`/`.isSubsetOf`/`.isSupersetOf`/`.isDisjointFrom` | ES2025 — Chrome 122, Safari 17, Firefox 127, Node 22+ |
| lodash chain / iteration utilities | Iterator helpers (`.map`/`.filter`/`.take`/`.drop`/`.flatMap`/`.reduce`) | Baseline Newly Available 2025-03 — Chrome 122, Firefox 131, Safari 18.4, Node 22+ |
| `Promise.all` over async iterables | `Array.fromAsync()` | Chrome 121, Firefox 115, Safari 16.4; Baseline Widely Available target 2026-07 |
| uuid | `crypto.randomUUID()` | Node 19+, all evergreen browsers (Secure Context) |
| node-fetch / axios (simple cases) | global `fetch()` | Node 18+ (stable in 21+) |
| ws (WebSocket client) | native `WebSocket` | Node 22.4+ (stable) |
| glob | `fs.glob()` / `fs.promises.glob()` | Node 22+ (stable in 24) |
| path-to-regexp (route matching) | `URLPattern` (global) | Node 24+, Chrome 95, Safari 18, Firefox 142 |
| dotenv | `--env-file` flag | Node 20+ |
| ts-node / tsx (erasable syntax only) | Built-in TypeScript stripping | Node 24+ (default for `.ts`) |
| better-sqlite3 (embedded/prototype) | `node:sqlite` | Node 24+ (stable) |
| jest / mocha (simple suites) | `node:test` + `node:assert` | Node 20+ (stable) |
| chalk | `util.styleText()` | Node 21+ (stable in 22+) |
| classnames | Template literals or `clsx` (smaller) | Always |
| underscore | Array methods (`.map`/`.filter`/`.flat`/`.flatMap`) | ES2015+ / ES2019 |

Sources (verified 2026-05): [TC39 Temporal](https://tc39.es/proposal-temporal/), [Node.js v26 docs](https://nodejs.org/api/), [MDN Object.groupBy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/groupBy), [web.dev Iterator helpers Baseline](https://web.dev/blog/baseline-iterator-helpers), [Array.fromAsync feature explorer](https://web-platform-dx.github.io/web-features-explorer/features/array-fromasync/).
