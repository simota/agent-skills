# Profiling Tools Reference

## Frontend Profiling

| Tool | Use Case | Command/Setup |
|------|----------|---------------|
| **React DevTools Profiler** | Component render timing | Browser extension |
| **Chrome DevTools Performance** | JS execution, layout, paint | F12 → Performance |
| **Lighthouse** | Core Web Vitals audit | F12 → Lighthouse |
| **web-vitals** | Real user metrics | `npm i web-vitals` |
| **why-did-you-render** | Unnecessary re-renders | `npm i @welldone-software/why-did-you-render` |

### React Profiling

```typescript
// Enable React Profiler in development
import { Profiler } from 'react';

function onRenderCallback(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number
) {
  console.log(`${id} ${phase}: ${actualDuration.toFixed(2)}ms`);
}

<Profiler id="MyComponent" onRender={onRenderCallback}>
  <MyComponent />
</Profiler>
```

---

## Backend Profiling

| Tool | Use Case | Command/Setup |
|------|----------|---------------|
| **Node.js --inspect** | CPU profiling, heap | `node --inspect app.js` |
| **clinic.js** | Node.js performance suite | `npx clinic doctor -- node app.js` |
| **0x** | Flame graphs | `npx 0x app.js` |
| **autocannon** | HTTP load testing | `npx autocannon http://localhost:3000` |

### Node.js Profiling Commands

```bash
# CPU profiling with Chrome DevTools
node --inspect-brk app.js
# Open chrome://inspect

# Generate flame graph with 0x
npx 0x app.js
# Creates interactive flame graph

# Load testing with autocannon
npx autocannon -c 100 -d 30 http://localhost:3000/api/users
# -c: connections, -d: duration in seconds

# Memory profiling
node --expose-gc --inspect app.js
# In DevTools: Memory tab → Take heap snapshot
```

---

## Bundle Analysis

```bash
# Next.js bundle analyzer
ANALYZE=true npm run build

# Webpack bundle analyzer
npx webpack-bundle-analyzer stats.json

# Source map explorer
npx source-map-explorer 'dist/**/*.js'

# Bundlephobia (check before installing)
# https://bundlephobia.com/package/lodash
```
