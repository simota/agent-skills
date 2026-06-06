# Node.js Version Compatibility

Feature availability by Node.js version for backend modernization.

## LTS Timeline

As of 2026-05, Node.js 24 is the recommended Active LTS, Node.js 22 is in Maintenance LTS, and Node.js 26 has just shipped as Current (entering LTS October 2026). Node.js 18 and 20 have reached End-of-Life. Node.js 26 is the last release line under the current schedule; Node.js 27 starts a new schedule with a 6-month Alpha phase. Sources: [nodejs.org/en/about/previous-releases](https://nodejs.org/en/about/previous-releases), [endoflife.date/nodejs](https://endoflife.date/nodejs).

| Version | Codename | Status (2026-05) | Released | Active LTS Ends | EOL (Maintenance Ends) |
|---------|----------|------------------|----------|-----------------|------------------------|
| 18.x | Hydrogen | **EOL** | 2022-04-19 | 2023-10-18 | 2025-04-30 |
| 20.x | Iron | **EOL** | 2023-04-18 | 2024-10-22 | 2026-04-30 |
| 22.x | Jod | Maintenance LTS | 2024-04-24 | 2025-10-21 | 2027-04-30 |
| 24.x | Krypton | **Active LTS (recommended)** | 2025-05-06 | 2026-10-20 | 2028-04-30 |
| 26.x | TBD | Current (enters LTS 2026-10) | 2026-05-05 | 2027-10-27 | 2029-04-30 |

## Feature Matrix

Node 18 and 20 are listed for legacy reference only — both are EOL as of 2026-05. New projects should target Node 22 LTS or Node 24 LTS.

| Feature | Node 20 (EOL) | Node 22 | Node 24 | Replaces |
|---------|---------------|---------|---------|----------|
| Native `fetch` (stable) | ✅ | ✅ | ✅ | node-fetch, axios |
| Native test runner (`node:test`) | ✅ | ✅ | ✅ | jest, mocha (simple suites) |
| `--watch` mode | ✅ | ✅ | ✅ | nodemon |
| `crypto.randomUUID` | ✅ | ✅ | ✅ | uuid |
| `structuredClone` | ✅ | ✅ | ✅ | lodash.cloneDeep |
| `--env-file` flag | ✅ | ✅ | ✅ | dotenv |
| Native WebSocket client (stable in 22.4+) | ❌ | ✅ | ✅ | ws |
| `fs.glob` / `fs.promises.glob` | ❌ | ✅ | ✅ (stable) | glob package |
| `URLPattern` (global) | ❌ | ❌ | ✅ | path-to-regexp |
| TypeScript stripping (`.ts` direct exec) | ❌ | ❌ (flag) | ✅ (default for erasable syntax) | ts-node, tsx |
| `node:sqlite` (stable) | ❌ | ❌ (exp) | ✅ | better-sqlite3 |
| Permission model | ✅ (exp) | ✅ (exp) | ✅ (stable) | - |
| Single executable applications | ✅ (exp) | ✅ | ✅ | pkg |
| ESM by default | ✅ | ✅ | ✅ | - |
| Top-level await | ✅ | ✅ | ✅ | - |

## Upgrade Path Recommendations

### Node.js Upgrade Checklist

**From 18.x (EOL) → 22.x LTS (urgent):**
- [ ] Replace node-fetch with native `fetch`
- [ ] Remove dotenv in favor of `--env-file`
- [ ] Migrate to `node:test` for new suites (jest/mocha can remain)
- [ ] Audit OpenSSL v3-dependent code paths
- [ ] Run `npm audit` — no security patches will land on 18.x

**From 20.x (EOL 2026-04-30) → 22.x or 24.x LTS (urgent):**
- [ ] Replace `ws` with native WebSocket client (stable since 22.4)
- [ ] Enable Permission Model (stable in 24, experimental in 22)
- [ ] Consider Single Executable Applications for distribution
- [ ] Review experimental features that are now stable

**From 22.x → 24.x LTS:**
- [ ] **Remove all `util.is*()` calls** — `util.isArray`, `util.isBoolean`, `util.isBuffer`, `util.isDate`, `util.isError`, `util.isFunction`, `util.isNull`, `util.isNumber`, `util.isString`, etc. are **removed** (not just deprecated). Replace with native equivalents (`Array.isArray`, `typeof`, `instanceof`). Source: [nodejs.org deprecated APIs](https://nodejs.org/docs/latest-v22.x/api/deprecations.html)
- [ ] **Replace `SlowBuffer`** with `Buffer.allocUnsafeSlow(size)` — removed in Node 24.
- [ ] **Audit crypto key sizes** — OpenSSL 3.5 (Node 24) rejects RSA/DSA/DH < 2048 bits and ECC < 224 bits at runtime; update key generation and certificate validation logic.
- [ ] Adopt native TypeScript stripping (drop ts-node / tsx where erasable-only syntax is used)
- [ ] Replace `glob` package with `fs.glob` / `fs.promises.glob`
- [ ] Replace `path-to-regexp` (route matching) with global `URLPattern`
- [ ] Migrate `better-sqlite3` to `node:sqlite` for embedded/prototype use cases
- [ ] V8 13.6 / npm 11 — re-run full test suite
- [ ] Drop runtime polyfills for Set methods, `Object.groupBy`, Iterator helpers, `Array.fromAsync` (all native in V8 13.6)

## package.json Engine Specification

For new projects in 2026, target Node 22 LTS minimum (Node 20 is EOL 2026-04-30). Target Node 24 LTS to unlock native TypeScript stripping, `URLPattern`, and stable `node:sqlite`.

```json
{
  "engines": {
    "node": ">=22.0.0",
    "npm": ">=10.9.0"
  }
}
```

For projects using OIDC Trusted Publishing on npm, require Node ≥ 22.14.0 and npm ≥ 11.5.1 (Trusted Publishing prerequisites, per npm docs).
