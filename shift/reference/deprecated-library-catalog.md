# Deprecated Library Catalog

## Date/Time Libraries

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `moment.js` | `Temporal API`, `date-fns`, `dayjs`, `luxon` | Legacy project in maintenance mode since 2020; team explicitly discourages new use. Temporal reached TC39 Stage 4 in March 2026 and ships in Chrome/Edge 144 + Firefox 139; use `@js-temporal/polyfill` until Safari ships. date-fns / dayjs remain the pragmatic interim (2KB vs 72KB). |
| `moment-timezone` | `Temporal.ZonedDateTime`, `Intl.DateTimeFormat`, `luxon` | Native `Intl` + Temporal handle timezone conversion without the 900KB IANA data bundle. |

```typescript
// Before: moment
import moment from 'moment';
const formatted = moment().format('YYYY-MM-DD');

// After: date-fns (tree-shakeable)
import { format } from 'date-fns';
const formatted = format(new Date(), 'yyyy-MM-dd');

// After: Native Intl (no dependency)
const formatted = new Intl.DateTimeFormat('sv-SE').format(new Date());
```

## HTTP Libraries

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `request` | native `fetch`, `undici`, `got` | Deprecated since 2020, no security patches. Native `fetch` is stable since Node 21; `undici` powers it and is the request-compatible replacement (v6 adds HTTP/3). For drop-in migration, use npm `overrides` to point `request` at `undici`. |
| `axios` (audit before use) | native `fetch` (simple) or `undici`/`got` (advanced) | **Axios maintainer account was compromised on 2026-03-31 (CISA alert 2026-04-20)** — versions `1.14.1` / `0.30.4` contained a RAT and were deprecated. Project itself remains active but treat as a supply-chain risk: verify provenance attestations and pin via lockfile + `trustPolicy: no-downgrade`. |
| `superagent` | native `fetch` | fetch with `AbortController` covers most cases. |
| `node-fetch` | native `fetch` | Native `fetch` shipped in Node 18 and is stable since 21 — `node-fetch` is no longer needed. |

```typescript
// Before: axios
import axios from 'axios';
const { data } = await axios.get('/api/users');

// After: Native fetch
const response = await fetch('/api/users');
const data = await response.json();
```

## Testing Libraries

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `enzyme` | `@testing-library/react` | Effectively dead — no adapter for React 18 or 19, no maintainer. React 19 also deprecated `react-test-renderer`, consolidating RTL as the standard. HubSpot/Slack/NYT documented 15K–76K test migrations as reference cases. |
| `sinon` (consider) | `node:test` mocks, `vitest.fn()`, `jest.fn()` | `node:test` ships built-in mock/spy APIs (stable in Node 22+). |
| `karma` | `vitest`, `playwright/test`, `node:test` | Karma was archived. Vitest covers JSDOM-style suites; Playwright handles real-browser tests. |
| `jest` (simple suites, consider) | `node:test` (`node --test`) | For lightweight unit tests, the built-in runner avoids the jest dependency tree entirely. Jest remains valid for snapshot-heavy or large monorepo setups. |
| `mocha` (consider) | `node:test`, `vitest` | Same rationale — keep mocha only where its plugin ecosystem is load-bearing. |

```typescript
// Before: Enzyme
import { shallow } from 'enzyme';
const wrapper = shallow(<MyComponent />);
expect(wrapper.find('.button').text()).toBe('Click');

// After: React Testing Library
import { render, screen } from '@testing-library/react';
render(<MyComponent />);
expect(screen.getByRole('button')).toHaveTextContent('Click');
```

## CSS/Styling Libraries

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `node-sass` | `sass` (dart-sass) | node-sass is deprecated. dart-sass is the primary implementation. |
| CSS-in-JS (runtime) | CSS Modules, Tailwind, vanilla-extract | Runtime CSS-in-JS has performance overhead. |
| `@emotion/core` | `@emotion/react` | Package renamed. |

## Utility Libraries

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `lodash` (full bundle) | native methods, `lodash-es` (tree-shake), `es-toolkit` | Most lodash use cases now native: `groupBy` → `Object.groupBy` (Baseline 2024), set ops → `Set.prototype.union/.intersection/.difference` (ES2025), chains → Iterator helpers (Baseline 2025-03), `cloneDeep` → `structuredClone`. Frequently flagged in 2026 npm vulnerability reports for prototype pollution. |
| `lodash.groupBy` | `Object.groupBy()` | Native since Chrome 117 / Firefox 119 / Safari 17.4 / Node 20.12. |
| `lodash.chain` / iteration | Iterator helpers | Native since Chrome 122 / Firefox 131 / Safari 18.4 / Node 22. |
| `underscore` | native ES6+ methods | Most utilities now built into JavaScript. |
| `uuid` | `crypto.randomUUID()` | Native in Node 19+ and all evergreen browsers (Secure Context required). |
| `classnames` | `clsx` or template literals | `clsx` is smaller (~250B) and faster; same API. |
| `dotenv` | `--env-file` flag | Native since Node 20. |
| `chalk` | `util.styleText()` | Stable since Node 22. |

```typescript
// Before: lodash
import _ from 'lodash';
const result = _.uniq(array);

// After: Native Set
const result = [...new Set(array)];

// Before: uuid
import { v4 as uuidv4 } from 'uuid';
const id = uuidv4();

// After: Native crypto
const id = crypto.randomUUID();
```

## Build Tools

| Deprecated | Replacement | Migration Notes |
|------------|-------------|-----------------|
| `webpack` (consider) | `vite`, `rspack`, `turbopack`, `esbuild` | Vite is the default recommendation in the React docs since CRA sunset. `rspack` (Rust-based, webpack-compatible) is the migration path when webpack config must be preserved. |
| `create-react-app` | `vite`, `next.js`, `remix`, `tanstack/start` | **Officially deprecated by the React team on 2025-02-14** ("Sunsetting Create React App"). No security patches, no dependency updates. React docs now point new users to a framework or to Vite/Parcel/RSBuild. |
| `babel` (consider) | `swc`, `esbuild`, native TS stripping (Node 24+) | SWC/esbuild are 10–100× faster. Babel still required for some custom transforms. |
| `tslint` | `eslint` + `@typescript-eslint` | TSLint was officially deprecated. |
| `ts-node` / `tsx` (erasable syntax) | Native TS stripping (`node file.ts`) | Built-in in Node 24+ for erasable TS syntax (no enums / `namespace` / param-properties / `const enum`). Use `swc`/`tsx` only when those features are required. |
| `node-sass` | `sass` (dart-sass) | node-sass was deprecated; dart-sass is the primary implementation. |

## Node.js Built-in Removals (Node 24, Active LTS Oct 2025)

The following APIs were **removed** (not just deprecated) in Node.js 24. Code using them will throw at runtime.

| Removed API | Replacement | Notes |
|-------------|-------------|-------|
| `util.isArray(v)` | `Array.isArray(v)` | Deprecated since Node 4; removed in Node 24 |
| `util.isBoolean(v)` | `typeof v === 'boolean'` | Deprecated since Node 4; removed in Node 24 |
| `util.isBuffer(v)` | `Buffer.isBuffer(v)` | Deprecated since Node 4; removed in Node 24 |
| `util.isDate(v)` | `v instanceof Date` | Deprecated since Node 4; removed in Node 24 |
| `util.isError(v)` | `v instanceof Error` | Deprecated since Node 4; removed in Node 24 |
| `util.isFunction(v)` | `typeof v === 'function'` | Deprecated since Node 4; removed in Node 24 |
| `util.isNull(v)` | `v === null` | Deprecated since Node 4; removed in Node 24 |
| `util.isNumber(v)` | `typeof v === 'number'` | Deprecated since Node 4; removed in Node 24 |
| `util.isString(v)` | `typeof v === 'string'` | Deprecated since Node 4; removed in Node 24 |
| `SlowBuffer` | `Buffer.allocUnsafeSlow(size)` | Deprecated since Node 6; removed in Node 24 |

Additionally, OpenSSL 3.5 (bundled in Node 24) raises the default security level to 2: RSA/DSA/DH keys < 2048 bits and ECC keys < 224 bits are rejected. Source: [nodejs.org deprecated APIs v22](https://nodejs.org/docs/latest-v22.x/api/deprecations.html)

## Python 3.13 stdlib Removals (PEP 594 — Dead Batteries)

All 19 modules below were removed in Python 3.13 (DeprecationWarning since 3.11):

`aifc`, `audioop`, `cgi`, `cgitb`, `chunk`, `crypt`, `imghdr`, `mailcap`, `msilib`, `nis`, `nntplib`, `ossaudiodev`, `pipes`, `sndhdr`, `spwd`, `sunau`, `telnetlib`, `uu`, `xdrlib` + `2to3`/`lib2to3`.

Python 3.12 is the last release that ships these modules. Replacement strategies:
- `cgi` / `cgitb` → use a web framework (Flask, FastAPI, Django)
- `crypt` → `hashlib` + `secrets` (or `passlib` / `bcrypt` for password hashing)
- `telnetlib` → `asyncssh`, `paramiko`, or raw `socket`/`asyncio`

Source: [peps.python.org/pep-0594](https://peps.python.org/pep-0594/), [docs.python.org whatsnew 3.13](https://docs.python.org/3/whatsnew/3.13.html)

## Java Platform Removals (2025–2026)

| Removed/Disabled | Version | JEP | Replacement |
|------------------|---------|-----|-------------|
| `SecurityManager` (permanently disabled) | JDK 24 (2025) | JEP 486 | No direct replacement; use OS/container-level sandboxing |
| `java.applet.*`, `javax.swing.JApplet` (removed) | JDK 26 (Mar 2026) | JEP 504 | `javax.sound.SoundClip` (JDK 25) for audio; no browser applet replacement |
| `Object.finalize()` (deprecated for removal) | JDK 18+ | JEP 421 | `java.lang.ref.Cleaner`, `PhantomReference`, `AutoCloseable` |

Sources: [openjdk.org/jeps/486](https://openjdk.org/jeps/486), [openjdk.org/jeps/504](https://openjdk.org/jeps/504), [inside.java applet removal](https://inside.java/2025/12/03/applet-removal/)

## Web Platform Sunsets (2025–2026)

| API | Status | Notes |
|-----|--------|-------|
| Privacy Sandbox APIs (Topics, Protected Audience, Attribution Reporting, etc.) | Deprecated Oct 2025 | Google retired all 10 remaining APIs; Chrome M144 formal deprecation, M150 removal targeted. No replacement from Google. |
| Third-party cookies | Not deprecated in Chrome (reversal Apr 2025) | Safari/Firefox already block by default. Chrome deferred phase-out indefinitely; do not rely on a Chrome deadline. |
| WebSQL | Removal ongoing | Deprecated in third-party contexts; full removal in progress ([chromestatus](https://chromestatus.com/feature/5134293578285056)) |

Source: [chromestatus.com Privacy Sandbox deprecation](https://chromestatus.com/feature/5684870116278272)

## Go 1.24 Crypto Deprecations (Feb 2025)

| Deprecated API | Replacement | Reason |
|----------------|-------------|--------|
| `crypto/cipher.NewOFB` | AEAD (`cipher.NewGCM`) or `NewCTR` | OFB is unauthenticated; enables active attacks |
| `crypto/cipher.NewCFBEncrypter` | AEAD or `NewCTR` | CFB is unauthenticated |
| `crypto/cipher.NewCFBDecrypter` | AEAD or `NewCTR` | CFB is unauthenticated |
| `runtime.GOROOT()` | `go env GOROOT` via `exec.Command` | Prefer system path |

Source: [go.dev/doc/go1.24](https://go.dev/doc/go1.24)

## PHP 8.4 Deprecations (Nov 2024)

- **Implicit nullable parameters** — `function foo(Foo $x = null)` now emits `DeprecationWarning`; update to `function foo(?Foo $x = null)` or `function foo(Foo|null $x = null)`.
- **`trigger_error(E_USER_ERROR)`** — deprecated; use exceptions.
- **New `#[Deprecated]` attribute** — can mark user-land functions, methods, and class constants; PHP auto-emits deprecation messages on use.

Source: [php.net/releases/8.4](https://www.php.net/releases/8.4/en.php), [php.watch Deprecated attribute](https://php.watch/versions/8.4/Deprecated)

## Ruby 3.4 Deprecations (Dec 2024)

- **`syslog` and `base64` removed from default gems** — add `gem 'syslog'` / `gem 'base64'` to `Gemfile` explicitly.
- **Mutable string literals** — emit deprecation warning without `# frozen_string_literal: true`; enable with `-W:deprecated`.
- **`rb_gc_force_recycle` C API removed** — gem authors must update native extensions.

Source: [ruby-lang.org Ruby 3.4 released](https://www.ruby-lang.org/en/news/2024/12/25/ruby-3-4-0-released/)

---

## Sources (verified 2026-05)

- React team: [Sunsetting Create React App](https://react.dev/blog/2025/02/14/sunsetting-create-react-app) (2025-02-14)
- TC39: [Temporal proposal](https://tc39.es/proposal-temporal/) reached Stage 4 (March 2026 plenary)
- CISA: [Supply Chain Compromise Impacts Axios npm Package](https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager) (2026-04-20)
- Node.js: [Modules: TypeScript](https://nodejs.org/api/typescript.html), [WebSocket](https://nodejs.org/learn/getting-started/websocket), [release schedule](https://nodejs.org/en/about/previous-releases)
- Node.js 24 removals: [Deprecated APIs v22](https://nodejs.org/docs/latest-v22.x/api/deprecations.html) (2025)
- Python PEP 594: [peps.python.org/pep-0594](https://peps.python.org/pep-0594/) — Dead Batteries removed in Python 3.13
- Java JEP 486: [openjdk.org/jeps/486](https://openjdk.org/jeps/486) — SecurityManager permanently disabled JDK 24 (2025)
- Java JEP 504: [openjdk.org/jeps/504](https://openjdk.org/jeps/504) — Applet API removed JDK 26 (2026-03)
- Go 1.24: [go.dev/doc/go1.24](https://go.dev/doc/go1.24) — crypto deprecations (Feb 2025)
- Web Platform: [chromestatus Topics API](https://chromestatus.com/feature/5684870116278272) — Privacy Sandbox retired Oct 2025
- PHP 8.4: [php.watch/versions/8.4/Deprecated](https://php.watch/versions/8.4/Deprecated) (Nov 2024)
- Ruby 3.4: [ruby-lang.org](https://www.ruby-lang.org/en/news/2024/12/25/ruby-3-4-0-released/) (Dec 2024)
- MDN: [Object.groupBy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/groupBy), [Set methods](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)
- web.dev: [Iterator helpers Baseline](https://web.dev/blog/baseline-iterator-helpers) (2025-03)
