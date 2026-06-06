# Codemod Patterns Reference

## Codemod Tools by Language (2026-05 snapshot)

| Language | Tool | AST Library | Use for |
|----------|------|-------------|---------|
| JavaScript/TypeScript | jscodeshift | recast + ast-types | React migrations, API transforms (deep AST control); still the default for codemods that need imperative control |
| JavaScript/TypeScript | jssg (ast-grep JS) | ast-grep + Tree-sitter | Pattern-first rules, multi-language, typed DX; significantly faster on large repos than jscodeshift — preferred for repo-scale scans |
| JavaScript/TypeScript | **Codemod.com Studio + Hypermod** | jssg + jscodeshift hybrid | Visual authoring + managed run service; the de facto 2026 destination for "migrate my repo across React 18 → 19 / Next.js 15 → 16" workflows |
| TypeScript | ts-morph | TypeScript Compiler API | Type-aware transforms, import rewriting |
| Python | LibCST | libcst | Concrete syntax tree preserving formatting |
| Go | go/ast + golang.org/x/tools | go/ast | Go API migrations |
| Rust | syn + quote | syn | Macro-based transforms |
| Multi-language | ast-grep | Tree-sitter | Pattern matching across languages, repo-scale scanning |
| Java / Kotlin / Python | **OpenRewrite** | Lossless Semantic Trees (LST) | High-fidelity Java/Kotlin transforms (Spring Boot 3→4, Jakarta namespace, dependency upgrades); operates on type-resolved semantic model, not raw AST — prefer over jscodeshift for JVM migrations. Run via `./mvnw rewrite:run`. Source: [OpenRewrite Docs](https://docs.openrewrite.org/) |

### How To Pick Between jscodeshift and ast-grep / jssg

| Signal | Reach for |
|--------|-----------|
| Need to **mutate** the AST with imperative logic (read X, decide, build new Y) | jscodeshift / ts-morph |
| Need to **match** a pattern across hundreds of files and rewrite a localised diff | ast-grep / jssg |
| Need to run the same transform across **JS, TS, Python, Go** with one tool | ast-grep (Tree-sitter-based) |
| Want a visual / managed runner so non-codemod-experts can review the diff | Codemod.com Studio + Hypermod |
| The framework ships an **official codemod** already (`react-codemod`, `vue-codemod`, `@next/codemod`, `npx sv migrate`, OpenRewrite recipes) | Use the official set first; reach for the tools above only for the residual delta |
| React 19 upgrade specifically | Use [codemod.com React 18→19 guide](https://docs.codemod.com/guides/migrations/react-18-19) — React team co-published official codemods there (`Context.Provider`, `forwardRef`, `useContext→use`) |

## jscodeshift Patterns

### Basic transform structure
```javascript
// transform.js
module.exports = function(fileInfo, api) {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);

  // Find and replace pattern
  root
    .find(j.CallExpression, { callee: { name: 'oldFunction' } })
    .replaceWith(path => {
      return j.callExpression(
        j.identifier('newFunction'),
        path.node.arguments
      );
    });

  return root.toSource({ quote: 'single' });
};
```

### Execution
```bash
# Dry run (preview changes)
npx jscodeshift --dry --print -t transform.js src/

# Execute
npx jscodeshift -t transform.js src/

# With TypeScript parser
npx jscodeshift --parser=tsx -t transform.ts src/
```

## React Migration Codemods

### Class component → Function component with hooks
```javascript
// Handles: state, lifecycle, refs
module.exports = function(fileInfo, api) {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);

  root.find(j.ClassDeclaration, {
    superClass: {
      type: 'MemberExpression',
      object: { name: 'React' },
      property: { name: 'Component' }
    }
  }).forEach(path => {
    const className = path.node.id.name;
    const body = path.node.body.body;

    // Extract state from constructor
    const stateFields = extractStateFromConstructor(body);

    // Convert lifecycle methods to hooks
    const hooks = convertLifecyclesToHooks(body, j);

    // Build function component
    const funcComponent = j.variableDeclaration('const', [
      j.variableDeclarator(
        j.identifier(className),
        j.arrowFunctionExpression(
          [j.identifier('props')],
          j.blockStatement([
            ...stateFields,
            ...hooks,
            ...extractRenderReturn(body)
          ])
        )
      )
    ]);

    j(path).replaceWith(funcComponent);
  });

  return root.toSource();
};
```

### useEffect cleanup → React 19 patterns
```javascript
// Before: useEffect for data fetching
useEffect(() => {
  let cancelled = false;
  fetchData().then(data => {
    if (!cancelled) setData(data);
  });
  return () => { cancelled = true; };
}, [id]);

// After: React 19 use() hook
const dataPromise = fetchData(id);
const data = use(dataPromise);
```

## Vue 2 → Vue 3 Migration

### Options API → Composition API
```javascript
// ts-morph transform for Vue SFC
import { Project, SyntaxKind } from 'ts-morph';

function migrateVueComponent(sourceFile) {
  // Find export default { ... }
  const exportDefault = sourceFile.getFirstDescendantByKind(
    SyntaxKind.ExportAssignment
  );

  const objectLiteral = exportDefault.getExpression();

  // Extract data() → ref()/reactive()
  const dataProperty = objectLiteral.getProperty('data');
  if (dataProperty) {
    const dataFields = extractDataFields(dataProperty);
    // Convert to: const field = ref(initialValue)
  }

  // Extract computed → computed()
  // Extract methods → regular functions
  // Extract watch → watch()/watchEffect()
  // Extract lifecycle → onMounted()/onUnmounted()
}
```

### Key Vue 2→3 changes
| Vue 2 | Vue 3 | Codemod complexity |
|-------|-------|--------------------|
| `data()` | `ref()` / `reactive()` | Medium |
| `computed: {}` | `computed(() => ...)` | Low |
| `watch: {}` | `watch(source, cb)` | Medium |
| `created/mounted` | `onMounted()` | Low |
| `$emit` | `defineEmits()` | Medium |
| `$refs` | `useTemplateRef()` | Low |
| Vuex | Pinia | High (different API) |
| `Vue.filter()` | Removed (use functions) | Low |
| `$on/$off/$once` | mitt / tiny-emitter | Medium |

## CJS → ESM Migration

### Transform rules
```javascript
// require → import
const fs = require('fs');           → import fs from 'fs';
const { readFile } = require('fs'); → import { readFile } from 'fs';
const pkg = require('./package.json'); → import pkg from './package.json' assert { type: 'json' };

// module.exports → export
module.exports = MyClass;           → export default MyClass;
module.exports.helper = fn;         → export { fn as helper };
exports.helper = fn;                → export { fn as helper };

// __dirname / __filename
__dirname                           → import.meta.dirname  // Node 21.2+
__filename                          → import.meta.filename
path.join(__dirname, 'file')        → new URL('./file', import.meta.url).pathname

// Dynamic require
const mod = require(dynamicPath);   → const mod = await import(dynamicPath);
```

### package.json changes
```json
{
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs"
    }
  }
}
```

## JavaScript → TypeScript Migration

### Gradual typing strategy
1. **Phase 1: Infrastructure** — `tsconfig.json` with `allowJs: true`, rename entry points to `.ts`
2. **Phase 2: Strict boundaries** — Type external API boundaries (API responses, DB models)
3. **Phase 3: Module by module** — Rename `.js` → `.ts`, add types, fix errors
4. **Phase 4: Strict mode** — Enable `strict: true`, eliminate `any`

### tsconfig.json for gradual migration
```json
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": false,
    "strict": false,
    "noImplicitAny": false,
    "target": "ES2022",
    "module": "NodeNext",
    "outDir": "./dist"
  },
  "include": ["src/**/*"]
}
```

### ast-grep pattern for quick transforms
```yaml
# Find untyped function parameters
id: untyped-params
language: typescript
rule:
  kind: formal_parameters
  has:
    kind: required_parameter
    not:
      has:
        kind: type_annotation
```

## API Version Migration

### Versioned adapter pattern
```typescript
// Adapter that translates between API versions
interface UserResponseV1 {
  name: string;
  email: string;
}

interface UserResponseV2 {
  firstName: string;
  lastName: string;
  emailAddress: string;
  createdAt: string;
}

function v1ToV2(v1: UserResponseV1): UserResponseV2 {
  const [firstName, ...rest] = v1.name.split(' ');
  return {
    firstName,
    lastName: rest.join(' '),
    emailAddress: v1.email,
    createdAt: new Date().toISOString(), // Default for migrated records
  };
}

// Deprecation header middleware
function deprecationMiddleware(version: string, sunsetDate: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (req.path.startsWith(`/api/${version}`)) {
      res.setHeader('Deprecation', 'true');
      res.setHeader('Sunset', sunsetDate);
      res.setHeader('Link', `</api/v2${req.path.slice(7)}>; rel="successor-version"`);
    }
    next();
  };
}
```

## Verification Patterns

### Before/after snapshot testing
```typescript
// Capture behavior before migration
async function captureSnapshot(endpoints: string[]): Promise<SnapshotMap> {
  const snapshots: SnapshotMap = {};
  for (const endpoint of endpoints) {
    const response = await fetch(endpoint);
    snapshots[endpoint] = {
      status: response.status,
      headers: Object.fromEntries(response.headers),
      body: await response.json(),
    };
  }
  return snapshots;
}

// Compare after migration
function compareSnapshots(before: SnapshotMap, after: SnapshotMap): Diff[] {
  const diffs: Diff[] = [];
  for (const [endpoint, beforeSnap] of Object.entries(before)) {
    const afterSnap = after[endpoint];
    if (!afterSnap) {
      diffs.push({ endpoint, type: 'missing', severity: 'critical' });
      continue;
    }
    if (beforeSnap.status !== afterSnap.status) {
      diffs.push({ endpoint, type: 'status_change', before: beforeSnap.status, after: afterSnap.status, severity: 'high' });
    }
    // Deep compare body (ignoring timestamps, IDs)
    const bodyDiff = deepDiff(beforeSnap.body, afterSnap.body, { ignore: ['updatedAt', 'requestId'] });
    if (bodyDiff.length > 0) {
      diffs.push({ endpoint, type: 'body_change', changes: bodyDiff, severity: 'medium' });
    }
  }
  return diffs;
}
```
